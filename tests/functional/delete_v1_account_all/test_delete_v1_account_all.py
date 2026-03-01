import allure
import os



@allure.title("Тест на проверку логаута пользователя")
def test_logout(auth_account_helper):
    print(f'ТЕКУЩАЯ ДИРЕКТОРИЯ {os.getcwd()}')
    auth_account_helper.logout_all()
