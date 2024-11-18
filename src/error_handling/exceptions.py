class SlackAPIError(Exception):
    def __init__(self, message="An error occurred with the Slack API"):
        self.message = message
        super().__init__(self.message)

class NLPProcessingError(Exception):
    def __init__(self, message="An error occurred during NLP processing"):
        self.message = message
        super().__init__(self.message)

class APIRequestError(Exception):
    def __init__(self, message="Failed to complete the API request"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(Exception):
    def __init__(self, message="Invalid or missing Slack API token"):
        self.message = message
        super().__init__(self.message)