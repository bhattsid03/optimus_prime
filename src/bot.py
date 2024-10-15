import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.nlp_processing.inference import process_with_gpt_j
from src.handlers.build_url_handler import handle_jenkins_url
from src.handlers.cr_status_handler import handle_gerrit_url
from src.utils.logging import setup_logging

class SlackBot:
    def __init__(self):
        # Initialize the Slack Bolt app
        self.app = App(token=os.getenv("SLACK_BOT_TOKEN"))
        # Set up logging
        self.logger = setup_logging()
        # Register event handlers
        self.register_event_handlers()

    def register_event_handlers(self):
        @self.app.event("app_mention")
        def handle_mention_events(event, say):
            text = event.get('text', '')

            # Process the message with the fine-tuned GPT model to detect intent and extract URLs
            result = process_with_gpt_j(text)
            intent = result["intent"]
            urls = result["urls"]

            # Ensure there's at least one URL extracted
            if not urls:
                say("Please provide a valid URL in your request.")
                return
            
            # Check the type of URL (Gerrit or Jenkins)
            url = urls[0]
            if "gerrit" in url:
                # Handle Gerrit URL
                if intent == "check_build_status" or intent == "build_failure":
                    say("Checking build status from Gerrit...")
                    handle_gerrit_url(url, say)
                elif intent == "check_cr_status":
                    say("Fetching CR status from Gerrit...")
                    handle_gerrit_url(url, say)
                else:
                    say("Sorry, I didn't understand that. Please specify if you need to check build status or CR status.")

            elif "jenkins" in url:
                # Handle Jenkins URL
                if intent == "check_build_status" or intent == "build_failure":
                    say("Checking the latest Jenkins build status...")
                    handle_jenkins_url(url, say)
                else:
                    say("Sorry, I didn't understand that. Please specify if you need to check for build failure, status, etc.")
            else:
                say("Unsupported URL provided. Please provide a valid Jenkins or Gerrit URL.")


    def start(self):
        # Start the bot using Socket Mode
        SocketModeHandler(self.app, os.getenv("SLACK_APP_TOKEN")).start()

if __name__ == "__main__":
    slack_bot = SlackBot()  # Create an instance of SlackBot
    slack_bot.start()  # Start the bot
