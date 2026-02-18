from models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):
    def post_v1_account_login(
            self,
            login_credentials=LoginCredentials
    ):
        """
        Authenticate via credentials
        :param login_credentials:
        :return:
        """

        response = self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )

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
