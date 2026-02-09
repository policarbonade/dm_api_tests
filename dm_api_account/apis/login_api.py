import requests
from restclient.client import RestClient


class LoginApi(RestClient):
    def post_v1_account_login(
            self,
            json_data
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        url = f"/v1/account/login"
        response = self.post(
            path=url,
            json=json_data
        )

        print(response.json())
        return response
