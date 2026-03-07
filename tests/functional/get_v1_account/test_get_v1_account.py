import allure

from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


@allure.suite("Тесты на проверку метода получения данных пользователя")
class TestGetV1Account:
    @allure.title("Получить аккаунт авторизованного пользователя")
    def test_get_v1_account_auth(self, auth_account_helper):
        """
        Test auth user with authorized client
        :param auth_account_helper:
        """
        with check_status_code_http("", 200):
            response = auth_account_helper.get_account(is_validated=True)
            GetV1Account.check_get_v1_account_values(response)

    @allure.title("Получить аккаунт неавторизованного пользователя")
    def test_get_v1_account_no_auth(self, account_helper):
        """
        Test auth user with unauthorized client
        :param account_helper:
        """
        with check_status_code_http("User must be authenticated", 401):
            response = account_helper.get_account()
