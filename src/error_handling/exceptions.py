class SlackAPIError(Exception):
    """Exception raised for errors in the Slack API."""
    def __init__(self, message="An error occurred with the Slack API"):
        self.message = message
        super().__init__(self.message)

class NLPProcessingError(Exception):
    """Exception raised for errors in NLP processing."""
    def __init__(self, message="An error occurred during NLP processing"):
        self.message = message
        super().__init__(self.message)

class APIRequestError(Exception):
    """Exception raised for failed API requests."""
    def __init__(self, message="Failed to complete the API request"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(Exception):
    """Exception raised when the Slack API token is invalid or missing."""
    def __init__(self, message="Invalid or missing Slack API token"):
        self.message = message
        super().__init__(self.message)