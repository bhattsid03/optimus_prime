import requests

# Define your Slack API token
SLACK_BOT_TOKEN = "your-bot-token"

def post_message(channel, text):
    """
    Post a message to a Slack channel.
    
    :param channel: Slack channel ID where the message will be sent
    :param text: The message text to send
    :return: Response from Slack API
    """
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def get_channel_info(channel):
    """
    Get information about a Slack channel.
    
    :param channel: Slack channel ID to get information about
    :return: Response from Slack API
    """
    url = "https://slack.com/api/conversations.info"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    params = {
        "channel": channel
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# You can add more functions to interact with Slack APIs as needed
