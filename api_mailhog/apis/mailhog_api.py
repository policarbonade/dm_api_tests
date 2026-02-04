import requests


class MailhogApi:
    def __init__(self, host, headers=None):
        self.headers = headers
        self.host = host

    def get_api_mailhog_messages(
            self,
            limit=50
    ):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': 50
        }
        url = f"{self.host}/api/v2/messages"
        response = requests.get(
            url=url,
            params=params,
            verify=False
        )
        return response
