import unittest
from unittest.mock import patch
from src.api_integration.jenkins_api import JenkinsAPI
import jenkins

class TestJenkinsAPI(unittest.TestCase):

    def setUp(self):
        self.jenkins_api = JenkinsAPI("http://fake-jenkins-url.com", "user", "token")

    # Test initialization
    def test_initialization(self):
        self.assertEqual(self.jenkins_api.server.server, "http://fake-jenkins-url.com")
        self.assertEqual(self.jenkins_api.server.auth, ("user", "token"))

    # Test get_build_info success case
    @patch('jenkins.Jenkins.get_build_info')
    def test_get_build_info_success(self, mock_get_build_info):
        mock_get_build_info.return_value = {"result": "SUCCESS", "duration": 1200}
        result = self.jenkins_api.get_build_info("fake-job", 1)
        self.assertEqual(result["result"], "SUCCESS")
        self.assertEqual(result["duration"], 1200)

    # Test get_build_info failure case (Job not found)
    @patch('jenkins.Jenkins.get_build_info')
    def test_get_build_info_job_not_found(self, mock_get_build_info):
        mock_get_build_info.side_effect = jenkins.JenkinsException("Job not found")
        result = self.jenkins_api.get_build_info("fake-job", 1)
        self.assertIsNone(result)

    # Test get_build_info network error
    @patch('jenkins.Jenkins.get_build_info')
    def test_get_build_info_network_error(self, mock_get_build_info):
        mock_get_build_info.side_effect = jenkins.JenkinsException("Connection error")
        result = self.jenkins_api.get_build_info("fake-job", 1)
        self.assertIsNone(result)

    # Test get_build_info with invalid response (missing keys)
    @patch('jenkins.Jenkins.get_build_info')
    def test_get_build_info_invalid_response(self, mock_get_build_info):
        # Return a response missing expected keys
        mock_get_build_info.return_value = {}
        result = self.jenkins_api.get_build_info("fake-job", 1)
        self.assertIsNone(result)  # Assuming your API handles it by returning None

    # Test get_job_info success case
    @patch('jenkins.Jenkins.get_job_info')
    def test_get_job_info_success(self, mock_get_job_info):
        mock_get_job_info.return_value = {"name": "fake-job", "lastBuild": {"number": 100}}
        result = self.jenkins_api.get_job_info("fake-job")
        self.assertEqual(result["name"], "fake-job")
        self.assertEqual(result["lastBuild"]["number"], 100)

    # Test get_job_info failure case (Job not found)
    @patch('jenkins.Jenkins.get_job_info')
    def test_get_job_info_job_not_found(self, mock_get_job_info):
        mock_get_job_info.side_effect = jenkins.JenkinsException("Job not found")
        result = self.jenkins_api.get_job_info("non-existent-job")
        self.assertIsNone(result)

    # Test get_job_info unauthorized access
    @patch('jenkins.Jenkins.get_job_info')
    def test_get_job_info_unauthorized(self, mock_get_job_info):
        mock_get_job_info.side_effect = jenkins.JenkinsException("Unauthorized")
        result = self.jenkins_api.get_job_info("unauthorized-job")
        self.assertIsNone(result)

    # Test get_job_info with invalid response (missing keys)
    @patch('jenkins.Jenkins.get_job_info')
    def test_get_job_info_invalid_response(self, mock_get_job_info):
        # Return a response missing expected keys
        mock_get_job_info.return_value = {}
        result = self.jenkins_api.get_job_info("fake-job")
        self.assertIsNone(result)  # Assuming your API handles it by returning None

    # Test get_build_logs success case
    @patch('jenkins.Jenkins.get_build_console_output')
    def test_get_build_logs_success(self, mock_get_build_logs):
        mock_get_build_logs.return_value = "Build log content"
        result = self.jenkins_api.get_build_logs("fake-job", 1)
        self.assertEqual(result, "Build log content")

    # Test get_build_logs network error
    @patch('jenkins.Jenkins.get_build_console_output')
    def test_get_build_logs_network_error(self, mock_get_build_logs):
        mock_get_build_logs.side_effect = jenkins.JenkinsException("Connection error")
        result = self.jenkins_api.get_build_logs("fake-job", 1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
