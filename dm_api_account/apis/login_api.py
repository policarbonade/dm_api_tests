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

        response = self.post(
            path="/v1/account/login",
            json=json_data
        )

        print(response.json())
        return response

    def delete_v1_account_login(
        self,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/login"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response

    def delete_v1_account_login_all(
        self,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/login/all"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response
