import requests
from restclient.client import RestClient


class MailhogApi(RestClient):
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
        url = f"/api/v2/messages"
        response = self.get(
            path=url,
            params=params,
            verify=False
        )
        return response
