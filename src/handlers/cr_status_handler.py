import os
from src.api_integration.gerrit_api import GerritAPI
from src.utils.logging import logger

gerrit_api = GerritAPI(base_url=os.getenv("GERRIT_BASE_URL"))

def handle_gerrit_url(gerrit_url, say):
    logger.info(f"Handling Gerrit URL: {gerrit_url}")
    change_id = extract_change_id(gerrit_url)

    if change_id:
        logger.info(f"Extracted change ID: {change_id}")
        
        try:
            cr_status = gerrit_api.get_cr_status(gerrit_url)
            if cr_status:
                merge_status = cr_status.get("merge_status", "UNKNOWN")
                verification_score = cr_status.get("verification_score", "Not Available")
                
                status_message = (
                    f"Change ID: {change_id}\n"
                    f"Merge Status: {merge_status}\n"
                    f"Verification Score: {verification_score}"
                )
                logger.info(f"CR status retrieved: {merge_status}, Verification Score: {verification_score}")
                say(status_message)
                
                comments = gerrit_api.get_cr_comments(gerrit_url)
                if comments:
                    comments_message = "Comments:\n" + "\n".join(comment['message'] for comment in comments)
                    logger.info(f"Comments retrieved for Change ID {change_id}")
                    say(comments_message)
                else:
                    logger.warning(f"No comments found for Change ID {change_id}")
            else:
                logger.error(f"Could not retrieve CR status for Change ID {change_id}")
                say("Could not retrieve CR status. Please check the change ID.")
        
        except Exception as e:
            logger.error(f"Error processing Gerrit URL: {gerrit_url}, Error: {str(e)}")
            say("An error occurred while processing the Gerrit URL.")
            say(f"Error details: {str(e)}")
    else:
        logger.warning(f"Invalid Gerrit URL provided: {gerrit_url}")
        say("Invalid Gerrit URL. Could not extract change ID.")

def extract_change_id(gerrit_url):
    """Extract the change ID from the Gerrit URL."""
    try:
        parts = gerrit_url.split("/")
        change_id = parts[-1] if parts else None
        if not change_id:
            raise ValueError("Failed to extract change ID")
        logger.info(f"Extracted change ID: {change_id} from URL: {gerrit_url}")
        return change_id
    except Exception as e:
        logger.error(f"Error extracting change ID from Gerrit URL: {gerrit_url}, Error: {str(e)}")
        return None
