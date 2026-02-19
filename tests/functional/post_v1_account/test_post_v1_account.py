from hamcrest import assert_that, has_property, starts_with


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, is_validated=True, validate_headers=True)
    print(response)
    # assert_that(response, has_property("json", "resource", has_property("login", starts_with(login))))
    # print(response)
