import allure
import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


@allure.suite("Тесты на проверку метода создания пользователя")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1Account:
    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, is_validated=True)
        PostV1Account.check_response_values(response, login)

    @allure.title("Проверка регистрации с невалидными данными")
    @pytest.mark.parametrize(
        ("login", "email", "password"),
        [
            ("keyloack", "keyloack@mail.ru", "12345"),
            ("keyloack", "keyloack@@mail.ru", "123456"),
            ("k", "keyloack@mail.ru", "123456")
        ]
    )
    def test_post_v1_account_invalid_data(self, account_helper, login, email, password):
        with check_status_code_http(expected_message="Validation failed", expected_status_code=400):
            account_helper.post_v1_account_isolation(login=login, email=email, password=password)
