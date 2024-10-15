import unittest
from unittest.mock import patch
from src.api_integration.slack_api import SlackAPI

class TestSlackAPI(unittest.TestCase):

    def setUp(self):
        self.slack_api = SlackAPI("fake-token")  # Initialize Slack API with a mock token

    # Test sending a message
    @patch('src.api_integration.slack_api.SlackClient.chat_postMessage')
    def test_send_message(self, mock_post_message):
        mock_post_message.return_value = {"ok": True}
        
        response = self.slack_api.send_message(channel="general", text="Hello, World!")
        self.assertTrue(response["ok"])
        mock_post_message.assert_called_once_with(channel="general", text="Hello, World!")

    # Test handling a Slack event (e.g., message received)
    @patch('src.api_integration.slack_api.SlackClient')
    def test_receive_event(self, mock_client):
        mock_event = {
            "type": "message",
            "channel": "C12345",
            "user": "U67890",
            "text": "Hi bot!"
        }
        
        response = self.slack_api.handle_event(mock_event)
        self.assertTrue(response)  # Assuming some response is expected

    # Test error handling
    @patch('src.api_integration.slack_api.SlackClient.chat_postMessage')
    def test_send_message_error(self, mock_post_message):
        mock_post_message.side_effect = Exception("API call failed")
        
        with self.assertRaises(Exception):
            self.slack_api.send_message(channel="general", text="This should fail")

if __name__ == '__main__':
    unittest.main()
