import allure


@allure.title("Тест на проверку полного логаута пользователя")
def test_logout(auth_account_helper):
    auth_account_helper.logout()
