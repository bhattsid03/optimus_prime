from src.api_integration.jenkins_api import JenkinsAPI
from src.api_integration.jira_api import JiraAPI 
from src.api_integration.gerrit_api import GerritAPI 
import logging

logger = logging.getLogger(__name__)

def handle_jenkins_url(jenkins_url, say):
    logger.info(f"Received Jenkins URL: {jenkins_url}")
    
    try:
        # Get Jenkins error log and identified error
        error_log, error_message = JenkinsAPI.get_jenkins_error_log(jenkins_url)
        if error_message:
            say(f"Error identified in Jenkins build: {error_message}")
            say(f"Here is the relevant Jenkins log:\n{error_log}")

            logger.info(f"Jenkins error log for {jenkins_url}:\n{error_log}")

            # Initialize the Jira API
            jira_api = JiraAPI()

            # Search for Jira tickets related to the error message
            jira_tickets_response = jira_api.find_jira_tickets(error_message)

            if jira_tickets_response.startswith("No Jira tickets found"):
                say("No relevant Jira tickets found.")
                logger.info(f"No relevant Jira tickets found for error: {error_message}")
            else:
                say(f"Found relevant Jira tickets:\n{jira_tickets_response}")
                logger.info(f"Relevant Jira tickets found")
        else:
            say("No errors identified in the Jenkins build. Please try re-triggering the build.")
            logger.info(f"No errors found in Jenkins build")
    
    except Exception as e:
        logger.error(f"An error occurred while processing the Jenkins URL: {jenkins_url}. Error details: {str(e)}")
        say("An error occurred while processing the Jenkins URL.")
        say(f"Error details: {str(e)}")

def handle_gerrit(gerrit_url, say):
    # Extract change ID from Gerrit URL
    change_id = extract_change_id(gerrit_url)
    
    if change_id:
        gerrit_api = GerritAPI(base_url="https://gerrit.eng.nutanix.com")
        
        try:
            # Fetch CR status and comments
            cr_status = gerrit_api.get_cr_status(change_id)
            if cr_status:
                # Check build status accordingly
                build_status = cr_status.get("current_revision", {}).get("status", "")
                if build_status == "FAILED":
                    say("The build has failed.")
                    
                    # Retrieve the build ID (assuming it is available in CR status, ***check once***)
                    build_id = cr_status.get("current_revision", {}).get("commit", "")
                    
                    # Get the Jenkins build URL
                    build_url = gerrit_api.get_build_url(build_id)
                    if build_url:
                        # Now you can call get_jenkins_error_log using the Jenkins URL
                        handle_jenkins_url(build_url, say)
                    else:
                        say("Could not retrieve the Jenkins build URL.")
                else:
                    say(f"The current status of the CR is: {build_status}")
            else:
                say("Could not retrieve change request status.")
        
        except Exception as e:
            say("An error occurred while processing the Gerrit URL.")
            say(f"Error details: {str(e)}")
            # Log the error if necessary
    else:
        say("Invalid Gerrit URL provided. Please check the format and try again.")

def extract_change_id(gerrit_url):
    """Extract the change ID from the Gerrit URL."""
    try:
        # Assuming the change ID is the last segment after the last '/'
        return gerrit_url.split('/')[-1]
    except Exception as e:
        return None
