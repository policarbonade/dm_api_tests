import allure


@allure.title("Тест для авторизации пользователя после регистрации")
def test_post_v1_account_login(prepare_user, account_helper):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, remember_me=True)
    assert response.status_code == 200, "User is not authorized"
