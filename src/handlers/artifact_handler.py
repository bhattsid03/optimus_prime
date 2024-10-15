import os
import requests
import logging

class ArtifactHandler:
    def __init__(self, slack_client):
        self.jenkins_url = os.getenv('JENKINS_URL')
        self.jenkins_user = os.getenv('JENKINS_USER')
        self.jenkins_token = os.getenv('JENKINS_TOKEN')
        self.slack_client = slack_client

    def fetch_artifacts(self, job_name, build_number):
        """
        Fetches artifacts for a given job and build number from Jenkins.

        :param job_name: Name of the Jenkins job
        :param build_number: Build number to fetch artifacts from
        :return: List of artifact URLs or an empty list if none found
        """
        try:
            url = f"{self.jenkins_url}/job/{job_name}/{build_number}/api/json"
            response = requests.get(url, auth=(self.jenkins_user, self.jenkins_token))

            if response.status_code != 200:
                logging.error(f"Failed to fetch build details: {response.status_code} {response.text}")
                return []

            build_info = response.json()
            artifacts = build_info.get('artifacts', [])
            artifact_urls = [f"{self.jenkins_url}/job/{job_name}/{build_number}/artifact/{artifact['relativePath']}"
                             for artifact in artifacts]
            return artifact_urls

        except Exception as e:
            logging.error(f"Error fetching artifacts: {str(e)}")
            return []

    def validate_artifact(self, artifact_url):
        """
        Validates the artifact URL to ensure it's accessible.

        :param artifact_url: URL of the artifact
        :return: True if the artifact is valid, False otherwise
        """
        try:
            response = requests.head(artifact_url)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Error validating artifact: {str(e)}")
            return False

    def post_artifact_to_slack(self, channel, artifact_urls):
        """
        Posts artifact URLs to a specified Slack channel.

        :param channel: Slack channel to post the artifact URLs
        :param artifact_urls: List of artifact URLs to post
        """
        for url in artifact_urls:
            if self.validate_artifact(url):
                message = f"Artifact available: <{url}|Download Here>"
                self.slack_client.chat_postMessage(channel=channel, text=message)
            else:
                logging.error(f"Artifact URL is not valid: {url}")
