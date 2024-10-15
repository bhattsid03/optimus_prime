import requests
import os
import logging
from requests.exceptions import HTTPError

class GerritAPI:
    def __init__(self, base_url, user=None, password=None):
        self.base_url = base_url.rstrip("/")  # Ensuring no trailing slash
        self.user = user or os.getenv("GERRIT_USER")
        self.password = password or os.getenv("GERRIT_PASSWORD")

    def get_cr_status(self, change_id):
        """Fetch the status of a Gerrit change request (CR).
        :return: JSON response with the status of the change request, or None if an error occurs
        """
        url = f"{self.base_url}/changes/{change_id}/detail" #Modify
        try:
            response = requests.get(url, auth=(self.user, self.password))
            response.raise_for_status()  # Raise exception for bad responses
            logging.info(f"Successfully retrieved CR status for {change_id}")
            return response.json()
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred while fetching CR status: {http_err}")
        except Exception as err:
            logging.error(f"Error occurred while fetching CR status: {err}")
        return None

    def get_cr_comments(self, change_id):
        """Fetch comments for a Gerrit change request (CR).
        :return: JSON response with comments, or None if an error occurs
        """
        url = f"{self.base_url}/changes/{change_id}/comments"
        try:
            response = requests.get(url, auth=(self.user, self.password))
            response.raise_for_status()
            logging.info(f"Successfully retrieved comments for CR {change_id}")
            return response.json()
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred while fetching CR comments: {http_err}")
        except Exception as err:
            logging.error(f"Error occurred while fetching CR comments: {err}")
        return None

    def find_postcommit_build(self, change_id):
        """
        Find the post-commit build related to the change request.
        :return: The build URL associated with the post-commit, or None if not found
        """
        try:
            # Fetch the change detail from Gerrit to find related builds
            change_detail = self.get_cr_status(change_id)
            if not change_detail:
                logging.error(f"Could not retrieve change details for {change_id}")
                return None

            # Assuming there's a build info field in the change details (adjust based on your Gerrit setup)
            if 'builds' in change_detail:
                build_id = change_detail['builds'][0]['id']  # Picking the first build in the list
                build_url = self.get_build_url(build_id)
                logging.info(f"Found post-commit build URL: {build_url}")
                return build_url
            else:
                logging.error(f"No builds found for change request {change_id}")
                return None
        except Exception as err:
            logging.error(f"Error finding postcommit build for {change_id}: {err}")
        return None

    def get_build_url(self, build_id):
        """Get build URL from Gerrit or another source.
        :return: The build URL or None if the build isn't found
        """
        try:
            # Fetch build URL from Jenkins or another build service using build ID
            jenkins_base_url = os.getenv("JENKINS_BASE_URL", "https://jenkins.example.com")
            build_url = f"{jenkins_base_url}/job/{build_id}"
            logging.info(f"Build URL found: {build_url}")
            return build_url
        except Exception as err:
            logging.error(f"Error retrieving build URL for build {build_id}: {err}")
        return None
