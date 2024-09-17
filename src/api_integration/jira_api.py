from jira import JIRA
import requests

class JiraAPI:
    def __init__(self, server_url, username, token):
        self.jira = JIRA(server=server_url, basic_auth=(username, token))

    # Step 1: Extract Jenkins log content
    def get_jenkins_log(self, log_url):
        try:
            response = requests.get(log_url)  # Get Jenkins log from the provided URL
            response.raise_for_status()
            return response.text  # Return the log content as text
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving Jenkins log: {e}")
            return None

    # Step 2: Extract error message from Jenkins log
    def extract_error_from_log(self, log_text):
        try:
            # Extract the first occurrence of an error, or use regex for more advanced parsing
            error_lines = [line for line in log_text.split('\n') if "ERROR" in line]
            return error_lines[0] if error_lines else None
        except Exception as e:
            print(f"Error extracting error from log: {e}")
            return None

    # Step 3: Search Jira for tickets related to the error
    def search_issues_for_error(self, error_message):
        try:
            # Construct JQL to search for the error message in summary or description
            jql = f'summary ~ "{error_message}" OR description ~ "{error_message}"'
            issues = self.jira.search_issues(jql)
            return issues
        except Exception as e:
            print(f"Error searching issues in Jira: {e}")
            return []

    # Step 4: Full workflow to find Jira tickets related to Jenkins error
    def find_jira_tickets_from_jenkins_log(self, log_url):
        # Step 1: Get Jenkins log content
        log_text = self.get_jenkins_log(log_url)
        if log_text is None:
            return "Could not retrieve Jenkins log."

        # Step 2: Extract the error message from the log
        error_message = self.extract_error_from_log(log_text)
        if not error_message:
            return "No errors found in Jenkins log."

        # Step 3: Search Jira for tickets related to the error
        jira_issues = self.search_issues_for_error(error_message)
        if not jira_issues:
            return f"No Jira tickets found related to the error: {error_message}"

        # Step 4: Return the relevant Jira tickets to the user
        response = f"Found {len(jira_issues)} Jira ticket(s) related to the error: {error_message}\n"
        for issue in jira_issues:
            response += f"- {issue.key}: {issue.fields.summary} (Status: {issue.fields.status.name})\n"
        return response
