import unittest
from src.bot import SlackBot  # Import the bot class
from unittest.mock import patch

class TestSlackBot(unittest.TestCase):

    @patch('src.bot.SlackBot.register_event_handlers')
    def test_bot_initialization(self, mock_register_event_handlers):
        """Test if the bot initializes correctly with event handlers."""
        bot = SlackBot()
        self.assertIsNotNone(bot.app)  # Ensure Slack app instance is created
        mock_register_event_handlers.assert_called_once()  # Ensure event handlers are registered

    @patch('src.api_integration.slack_api.SlackAPI.send_message')
    def test_send_message(self, mock_send_message):
        """Test if the bot sends a message correctly."""
        bot = SlackBot()
        mock_send_message.return_value = {'ok': True}
        
        response = bot.send_message("Test Channel", "Test Message")
        
        self.assertTrue(response['ok'])
        mock_send_message.assert_called_once_with("Test Channel", "Test Message")

    @patch('src.handlers.cr_status_handler.get_cr_status')
    def test_handle_cr_status(self, mock_get_cr_status):
        """Test CR status handler."""
        bot = SlackBot()
        mock_get_cr_status.return_value = "Status: Approved"
        
        result = bot.handle_event('cr_status', "CR123")
        self.assertEqual(result, "Status: Approved")
        mock_get_cr_status.assert_called_once_with("CR123")

    @patch('src.api_integration.jenkins_api.get_build_status')
    def test_handle_build_status(self, mock_get_build_status):
        """Test build status handler."""
        bot = SlackBot()
        mock_get_build_status.return_value = "Build Successful"
        
        result = bot.handle_event('build_status', "Build123")
        self.assertEqual(result, "Build Successful")
        mock_get_build_status.assert_called_once_with("Build123")
    
    # Add more tests based on different events or API integrations.

if __name__ == "__main__":
    unittest.main()
