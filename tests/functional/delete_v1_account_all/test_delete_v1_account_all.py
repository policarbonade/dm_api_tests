import allure


@allure.title("Тест на проверку логаута пользователя")
def test_logout(auth_account_helper):
    auth_account_helper.logout_all()
