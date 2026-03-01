import allure


@allure.title("Тест активации нового пользователя")
def test_put_v1_account_token(prepare_user, account_helper):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user(login=login, password=password, email=email)
