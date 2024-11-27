import re
import requests
import os
import logging
from requests.exceptions import HTTPError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GerritAPI:
    def __init__(self, base_url=None, token=None):
        self.base_url = base_url or os.getenv("GERRIT_BASE_URL")
        self.token = token or os.getenv("GERRIT_API_TOKEN")
        if not self.token:
            raise ValueError("GERRIT_API_TOKEN is not set in the environment variables.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

    def get_cr_status(self, gerrit_link):
        """Fetch and interpret the status of a Gerrit change request (CR) using the provided link."""
        try:
            response = self.session.get(gerrit_link, verify=False)
            response.raise_for_status()  # Raise exception for bad responses
            cr_data = response.json()
            logging.debug(f"CR Data: {cr_data}")
            logging.debug(f"Response text: {response.text}")

            merge_status = cr_data.get("status", "UNKNOWN")

            verification_label = cr_data.get("labels", {}).get("Verified", {})
            verification_score = verification_label.get("value", "Not Available")

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
            response = self.session.get(gerrit_link, verify=False)
            response.raise_for_status()
            cr_data = response.json()

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

    def get_build_failure_url(self, gerrit_link):
        """Fetch the Jenkins build failure URL from the change log."""
        try:
            # Construct the API endpoint for messages
            messages_url = f"{gerrit_link}/messages"
            response = self.session.get(messages_url, verify=False)
            response.raise_for_status()
            messages = response.json()  # List of messages

            # Iterate over messages to find one from Jenkins Build.svc with "Build Failed"
            for message in reversed(messages):  # Check from most recent to oldest
                if message.get("author", {}).get("name") == "Jenkins Build.svc" and "Build Failed" in message.get("message", ""):
                    # Extract URLs from the message content
                    failure_url_pattern = r'https?://[\w.-]+/job/[\w.-]+/[\d]+/ : FAILURE'
                    match = re.search(failure_url_pattern, message["message"])
                    if match:
                        failure_url = match.group(0).split(" :")[0]  # Remove " : FAILURE"
                        logging.info(f"Found Jenkins failure URL: {failure_url}")
                        return failure_url
            logging.error("No Jenkins failure URL found in the Gerrit change log.")
            return None

        except requests.RequestException as e:
            logging.error(f"Error fetching change log messages: {e}")
            return None

    def get_build_url(self, gerrit_link):
        # Attempt to fetch the failure URL from change log messages
        failure_url = self.get_build_failure_url(gerrit_link)
        if failure_url:
            return failure_url

        # Fallback: Extract from user comments
        comments = self.get_cr_comments(gerrit_link)
        if comments:
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
