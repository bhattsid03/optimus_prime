import os
from jira import JIRA

class JiraAPI:
    def __init__(self):
        self.load_auth_details()
    
    def load_auth_details(self):
        # Load auth details from environment variables
        server_url = os.environ.get("JIRA_SERVER_URL")
        username = os.environ.get("JIRA_USERNAME")
        token = os.environ.get("JIRA_API_TOKEN")
        self.jira = JIRA(server=server_url, basic_auth=(username, token))

    # Search Jira for tickets related to the error
    def search_issues_for_error(self, error_message):
        try:
            # Construct JQL to search for the error message in summary or description
            jql = f'summary ~ "{error_message}" OR description ~ "{error_message}"'
            issues = self.jira.search_issues(jql)
            return issues
        except Exception as e:
            print(f"Error searching issues in Jira: {e}")
            return []

    # Full workflow to find Jira tickets related to Jenkins error
    def find_jira_tickets(self, error_message):
        # Search Jira for tickets related to the error
        jira_issues = self.search_issues_for_error(error_message)
        if not jira_issues:
            return f"No Jira tickets found related to the error: {error_message}"

        # Return the relevant Jira tickets to the user with links
        response = f"Found {len(jira_issues)} Jira ticket(s) related to the error: {error_message}\n"
        for issue in jira_issues:
            # Construct the URL for each Jira issue using the stored server URL
            issue_url = f"{self.server_url}/browse/{issue.key}"
            response += f"- {issue.key}: {issue.fields.summary} (Status: {issue.fields.status.name})\n"
            response += f"  Link: {issue_url}\n"
        return response
