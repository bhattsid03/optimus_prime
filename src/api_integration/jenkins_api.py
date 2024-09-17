import jenkins
#Additional functionalities to be added

class JenkinsAPI:
    def __init__(self, server_url, username, password):
        self.server = jenkins.Jenkins(server_url, username=username, password=password)

    def get_build_info(self, job_name, build_number):
        try:
            build_info = self.server.get_build_info(job_name, build_number)
            return build_info
        except jenkins.JenkinsException as e:
            print(f"Error getting build info: {e}")

    def get_job_info(self, job_name):
        try:
            job_info = self.server.get_job_info(job_name)
            return job_info
        except jenkins.JenkinsException as e:
            print(f"Error getting job info: {e}")