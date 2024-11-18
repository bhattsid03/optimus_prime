import os
import requests
from error_handling.exceptions import SlackAPIError, APIRequestError
from src.utils.logging import logger

class SlackAPI:
    def __init__(self):
        self.token = os.environ.get("SLACK_BOT_TOKEN")
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        logger.info("Slack API initialized.")

    def post_message(self, channel, text):
        url = f"{self.base_url}/chat.postMessage"
        payload = {
            "channel": channel,
            "text": text
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise HTTP error for bad responses (4xx, 5xx)
            data = response.json()
            
            if not data.get("ok"):
                raise SlackAPIError(f"Slack API error: {data.get('error', 'Unknown error')}")
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting message to {channel}: {e}")
            raise APIRequestError(f"Failed to post message to Slack: {str(e)}")

    def get_channel_info(self, channel):
        url = f"{self.base_url}/conversations.info"
        params = {
            "channel": channel
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Raise HTTP error for bad responses (4xx, 5xx)
            data = response.json()
            
            if not data.get("ok"):
                raise SlackAPIError(f"Slack API error: {data.get('error', 'Unknown error')}")
            logger.info(f"Channel info retrieved for {channel}.")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving channel info for {channel}: {e}")
            raise APIRequestError(f"Failed to retrieve Slack channel info: {str(e)}")
