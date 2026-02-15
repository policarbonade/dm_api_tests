def test_put_v1_account_password(account_helper, prepare_user, prepare_password):
    login = prepare_user.login
    password = prepare_user.password
    new_password = prepare_password
    email = prepare_user.email

    # Register user
    account_helper.register_user(
        login=login,
        password=password,
        email=email
    )

    # Authorization
    response = account_helper.user_login(
        login=login,
        password=password
    )

    # Смена пароля с пробросом авторизационного токена в хэдэры
    header_token = response.headers["X-Dm-Auth-Token"]

    response = account_helper.change_password(
        login=login,
        header_token=header_token,
        old_password=password,
        new_password=new_password
    )
