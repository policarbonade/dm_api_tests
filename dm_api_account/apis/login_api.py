import allure

from models.login_credentials import LoginCredentials
from models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):
    @allure.step("Авторизоваться")
    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            is_validated=False
    ):
        """
        Authenticate via credentials
        :param is_validated:
        :param login_credentials:
        :return:
        """

        response = self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if is_validated:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Деавторизация")
    def delete_v1_account_login(
        self,
        **kwargs
    ):
        """
        Logout
        :return:
        """
        url = f"/v1/account/login"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response

    @allure.step("Полная деавторизация")
    def delete_v1_account_login_all(
        self,
        **kwargs
    ):
        """
        Logout all active sessions
        :return:
        """
        url = f"/v1/account/login/all"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response
