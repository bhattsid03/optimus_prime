import requests
import jenkins
import os
import logging
import re

class JenkinsAPI:
    def __init__(self, server_url, username=None, password=None):
        self.username = username or os.getenv("JENKINS_USER")
        self.password = password or os.getenv("JENKINS_TOKEN")
        self.server = jenkins.Jenkins(server_url, username=self.username, password=self.password)

    def get_build_info(self, job_name, build_number):
        try:
            build_info = self.server.get_build_info(job_name, build_number)
            return build_info
        except jenkins.JenkinsException as e:
            logging.error(f"Error getting build info for {job_name} build number {build_number}: {e}")
            return None

    def get_job_info(self, job_name):
        try:
            job_info = self.server.get_job_info(job_name)
            return job_info
        except jenkins.JenkinsException as e:
            logging.error(f"Error getting job info for {job_name}: {e}")
            return None

    def get_build_log(self, job_name, build_number):
        """Get the console output log of a specific build."""
        try:
            build_log = self.server.get_build_console_output(job_name, build_number)
            return build_log
        except jenkins.JenkinsException as e:
            logging.error(f"Error getting build log for {job_name} build number {build_number}: {e}")
            return None

    def get_last_build_status(self, job_name):
        """Get the last build status of the specified job."""
        try:
            job_info = self.get_job_info(job_name)
            if job_info and 'lastBuild' in job_info:
                last_build_number = job_info['lastBuild']['number']
                build_info = self.get_build_info(job_name, last_build_number)
                return build_info['result'] if build_info else None
            else:
                logging.warning(f"No builds found for job: {job_name}")
                return None
        except Exception as e:
            logging.error(f"Error getting last build status for {job_name}: {e}")
            return None
        
    def transform_jenkins_url(self, input_url):
        # Regex pattern to match required parts of the URL
        pattern = r"https://(.*?)/blue/organizations/jenkins/(.*?)/detail/(.*?)/(\d+)/pipeline"
        match = re.match(pattern, input_url)

        if match:
            base_url = match.group(1)
            pipeline_name = match.group(2)
            branch_name = match.group(3)
            run_number = match.group(4)

            # Construct the new URL based on the extracted information
            transformed_url = f"https://{base_url}/blue/rest/organizations/jenkins/pipelines/{pipeline_name}/branches/{branch_name}/runs/{run_number}/log/?start=0"
            return transformed_url
        else:
            raise ValueError("Invalid URL format")
        
    def get_jenkins_error_log(self, jenkins_url):
        try:
            # Request the build log from the Jenkins URL
            log_url = self.transform_jenkins_url(jenkins_url)
            response = requests.get(log_url)
            response.raise_for_status() 
            
            build_log = response.text.splitlines() 
            error_log_lines = []
            error_message = None
            context_lines = 10  # Number of lines of context before each error line

            for i, line in enumerate(build_log):
                if "ERROR" in line or "Exception" in line:
                    if error_message is None:
                        error_message = line
                    
                    start_idx = max(0, i - context_lines)  # Calculate the starting index
                    if not error_log_lines or start_idx > error_log_lines[-1][1]:
                        error_log_lines.append((start_idx, i + 1))

            error_log = "\n".join(
                build_log[start_idx:end_idx] 
                for start_idx, end_idx in error_log_lines
            )
            
            if not error_log:
                error_log = "No errors found in the build log."

            return error_log, error_message

        except requests.RequestException as err:
            print(f"Error retrieving Jenkins error log: {err}")
            return None, None

