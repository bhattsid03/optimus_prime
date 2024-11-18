import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.nlp_processing.inference import process_with_gpt_j
from src.handlers.build_url_handler import handle_gerrit, handle_jenkins_url
from src.handlers.cr_status_handler import handle_gerrit_url
from src.utils.logging import setup_logging

class SlackBot:
    def __init__(self):
        self.app = App(token=os.getenv("SLACK_BOT_TOKEN"))
        self.logger = setup_logging()
        self.register_event_handlers()

    def register_event_handlers(self):
        @self.app.event("app_mention")
        def handle_mention_events(event, say):
            text = event.get('text', '')
            thread_ts = event.get('ts') or event.get('ts')

            result = process_with_gpt_j(text, thread_ts)
            intent = result["intent"]
            urls = result["urls"]

            # Ensure there's at least one URL extracted
            if not urls:
                say("Please provide a valid URL in your request.")
                return
            
            url = urls[0]
            if "gerrit" in url:
                # Handle Gerrit URL
                if intent == "Build_Status" or intent == "Build Failure":
                    say("Checking build status from Gerrit...")
                    handle_gerrit(url, say)
                elif intent == "CR Status":
                    say("Fetching CR status from Gerrit...")
                    handle_gerrit_url(url, say)
                else:
                    say("Sorry, I didn't understand that. Please specify if you need to check build status or CR status.")

            elif "jenkins" in url:
                # Handle Jenkins URL
                if intent == "Build_Status" or intent == "Build Failure":
                    say("Checking the latest Jenkins build status...")
                    handle_jenkins_url(url, say)
                else:
                    say("Sorry, I didn't understand that. Please specify if you need to check for build failure, status, etc.")
            else:
                say("Unsupported URL provided. Please provide a valid Jenkins or Gerrit URL.")


    def start(self):
        SocketModeHandler(self.app, os.getenv("SLACK_APP_TOKEN")).start()

if __name__ == "__main__":
    slack_bot = SlackBot() 
    slack_bot.start()
