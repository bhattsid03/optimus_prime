import unittest
from unittest.mock import patch, MagicMock

import requests
from src.api_integration.gerrit_api import GerritAPI

class TestGerritAPI(unittest.TestCase):

    @patch('src.api_integration.gerrit_api.requests.get')  # Mock the 'requests.get' method
    def test_get_cr_status_success(self, mock_get):
        # Mock a successful response from Gerrit API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "MERGED",
            "change_id": "12345",
            "subject": "Fix bug in code"
        }
        mock_get.return_value = mock_response

        # Instantiate the API class and call the method
        gerrit = GerritAPI(base_url="https://gerrit.example.com", auth_token="test-token")
        response = gerrit.get_cr_status("12345")

        # Verify the method's behavior
        self.assertEqual(response["status"], "MERGED")
        self.assertEqual(response["change_id"], "12345")
        self.assertEqual(response["subject"], "Fix bug in code")

    @patch('src.api_integration.gerrit_api.requests.get')
    def test_get_cr_status_http_error(self, mock_get):
        # Mock a failed response (HTTP error)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError  # Simulate an HTTPError
        mock_get.return_value = mock_response

        # Instantiate the API class and call the method
        gerrit = GerritAPI(base_url="https://gerrit.example.com", auth_token="test-token")

        # Test that the method raises an HTTPError or handles it properly
        with self.assertRaises(requests.exceptions.HTTPError):  # Adjust based on how you handle errors in your code
            gerrit.get_cr_status("invalid-change-id")

    @patch('src.api_integration.gerrit_api.requests.get')
    def test_get_cr_comments_success(self, mock_get):
        # Mock a successful response from Gerrit API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"comment": "Looks good to me", "author": "Reviewer 1"},
            {"comment": "Please fix this issue", "author": "Reviewer 2"}
        ]
        mock_get.return_value = mock_response

        # Instantiate the API class and call the method
        gerrit = GerritAPI(base_url="https://gerrit.example.com", auth_token="test-token")
        response = gerrit.get_cr_comments("12345")

        # Verify the method's behavior
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["author"], "Reviewer 1")
        self.assertEqual(response[1]["comment"], "Please fix this issue")

if __name__ == '__main__':
    unittest.main()
