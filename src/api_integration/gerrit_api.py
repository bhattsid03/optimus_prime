import re
import requests
import os
import logging
from requests.exceptions import HTTPError

class GerritAPI:
    def __init__(self, base_url, user=None, password=None):
        self.base_url = base_url.rstrip("/")  # Ensuring no trailing slash
        self.user = user or os.getenv("GERRIT_USER")
        self.password = password or os.getenv("GERRIT_PASSWORD")

    def get_cr_status(self, gerrit_link):
        """Fetch and interpret the status of a Gerrit change request (CR) using the provided link.
        :return: Dictionary with the status of the merge status and verification score, or None if an error occurs
        """
        try:
            response = requests.get(gerrit_link, auth=(self.user, self.password))
            response.raise_for_status()  # Raise exception for bad responses
            cr_data = response.json()  # Assuming it returns JSON data

            # Parse the merge status
            merge_status = cr_data.get("status", "UNKNOWN")

            # Parse the verification score
            verification_label = cr_data.get("labels", {}).get("Verified", {})
            verification_score = verification_label.get("value", "Not Available")

            # Format a summary for the user
            status_summary = {
                "merge_status": merge_status,
                "verification_score": verification_score
            }

            logging.info(f"Successfully retrieved and parsed CR status from {gerrit_link}")
            return status_summary

        except HTTPError as http_err:
            logging.error(f"HTTP error occurred while fetching CR status: {http_err}")
        except Exception as err:
            logging.error(f"Error occurred while fetching CR status: {err}")
        return None


    def get_cr_comments(self, gerrit_link):
        """Fetch comments directly from the main CR response."""
        try:
            response = requests.get(gerrit_link, auth=(self.user, self.password))
            response.raise_for_status()
            cr_data = response.json()  # Full JSON data

            # Assuming comments are embedded within this data under a 'comments' field
            comments = cr_data.get("comments")
            if comments:
                logging.info(f"Successfully retrieved comments for CR from {gerrit_link}")
                return comments
            else:
                logging.error(f"No comments found in the CR data for {gerrit_link}")
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred while fetching CR comments: {http_err}")
        except Exception as err:
            logging.error(f"Error occurred while fetching CR comments: {err}")
        return None


    def get_build_url(self, gerrit_link):
        """Extract the Jenkins build URL from the last comment on a Gerrit change request.
        :param gerrit_link: Full URL of the Gerrit change request.
        :return: The Jenkins build URL or None if not found.
        """
        comments = self.get_cr_comments(gerrit_link)
        
        if comments:
            # Assuming the last comment is the latest one with the Jenkins URL
            last_comment_text = comments[-1].get('message', '')
            
            # Regular expression to match Jenkins URLs
            jenkins_url_pattern = r'https?://[\w.-]+/job/[\w.-]+/?[\w./-]*'
            match = re.search(jenkins_url_pattern, last_comment_text)
            
            if match:
                build_url = match.group(0)
                logging.info(f"Found Jenkins build URL: {build_url}")
                return build_url
            else:
                logging.error(f"No Jenkins build URL found in the last comment of {gerrit_link}")
        else:
            logging.error(f"No comments found for Gerrit link {gerrit_link}")
        
        return None
