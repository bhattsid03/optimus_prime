import requests
#Additional functionalities to be added

class GerritAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

    def get_change_status(self, change_id):
        try:
            url = f"{self.base_url}/changes/{change_id}/detail"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting change status: {e}")

    def get_change_messages(self, change_id):
        try:
            url = f"{self.base_url}/changes/{change_id}/messages"
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting change messages: {e}")