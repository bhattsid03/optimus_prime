from src.api_integration.jenkins_api import JenkinsAPI
from src.api_integration.jira_api import JiraAPI 
from src.api_integration.gerrit_api import GerritAPI 
import logging

logger = logging.getLogger(__name__)

def handle_jenkins_url(jenkins_url, say):
    logger.info(f"Received Jenkins URL: {jenkins_url}")
    
    try:
        error_log, error_message = JenkinsAPI.get_jenkins_error_log(jenkins_url)
        if error_message:
            say(f"Error identified in Jenkins build: {error_message}")
            say(f"Here is the relevant Jenkins log:\n{error_log}")

            logger.info(f"Jenkins error log for {jenkins_url}:\n{error_log}")

            jira_api = JiraAPI()
            jira_tickets_response = jira_api.find_jira_tickets(error_message)

            if jira_tickets_response.startswith("No Jira tickets found"):
                say("No relevant Jira tickets found.")
                logger.info(f"No relevant Jira tickets found for the error.")
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
    change_id = extract_change_id(gerrit_url)
    if change_id:
        gerrit_api = GerritAPI(base_url="https://gerrit.eng.nutanix.com")
        
        try:
            cr_status = gerrit_api.get_cr_status(gerrit_url)
            if cr_status:
                merge_status = cr_status.get("merge_status", "UNKNOWN")
                verification_score = cr_status.get("verification_score", "Not Available")
                
                say(f"The current merge status of the CR is: {merge_status}")
                say(f"Verification score: {verification_score}")
                
                build_url = gerrit_api.get_build_url(gerrit_url)
                if build_url:
                    handle_jenkins_url(build_url, say)
                else:
                    say("Could not retrieve the Jenkins build URL.")
            else:
                say("Could not retrieve change request status.")
        
        except Exception as e:
            say("An error occurred while processing the Gerrit URL.")
            say(f"Error details: {str(e)}")
    else:
        say("Invalid Gerrit URL provided. Please check the format and try again.")


def extract_change_id(gerrit_url):
    """Extract the change ID from the Gerrit URL."""
    try:
        # Assuming the change ID is the last segment after the last '/'
        return gerrit_url.split('/')[-1]
    except Exception as e:
        return None
