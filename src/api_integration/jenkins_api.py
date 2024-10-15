import requests
import jenkins
import os
import logging

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
        
    def get_jenkins_error_log(self, jenkins_url):
        """
        :return: A tuple of (error_log, error_message). If no errors, returns (None, None).
        """
        try:
            # Request the build log from the Jenkins URL
            response = requests.get(f"{jenkins_url}/log") # 
            response.raise_for_status()  # Raise exception if the request failed
            
            build_log = response.text  # Get the full build log as text

            # Filter for lines containing "ERROR" or "Exception", creates 
            # a list of error lines and joins them into a string error_log using \n.
            error_log = "\n".join([line for line in build_log.splitlines() if "ERROR" in line or "Exception" in line])

            # Extract the first error message (if any)
            error_message = None
            for line in build_log.splitlines():
                if "ERROR" in line or "Exception" in line:
                    error_message = line
                    break

            # If no errors found, return None
            if not error_log:
                error_log = "No errors found in the build log."
            
            return error_log, error_message
        
        except requests.RequestException as err:
            print(f"Error retrieving Jenkins error log: {err}")
            return None, None
