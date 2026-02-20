from checkers.http_checkers import check_status_code_http


def test_put_v1_account_email(prepare_user, account_helper):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user(email=email, password=password, login=login)

    # Авторизоваться
    account_helper.user_login(login=login, password=password, remember_me=True)

    # Смена емайл
    email = f'{login}+24@mail.ru'
    response = account_helper.put_account_email(login, password, email)
    assert response.status_code == 200, f"Смена почты для пользователя {login} неуспешна"

    # Попытка входа с 403 ошибкой
    with check_status_code_http(
        expected_message="User is inactive. Address the technical support for more details",
        expected_status_code=403
    ):
        account_helper.user_login(login=login, password=password, remember_me=True)

    account_helper.activate(login=login)

    # Повторная попытка авторизации
    account_helper.user_login(login=login, password=password, remember_me=True)
