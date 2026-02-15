from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailHogApi
from json import loads
from retrying import retry


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


class AccountHelper:
    def __init__(self, dm_account_api: DmApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_user(self, login:str, password:str, email:str):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан, {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login} не был активирован"
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        # Закомменченно, так как подходит не для всех тестов, где-то жду 403
        # assert response.status_code == 200, f"Пользователь {login} не авторизован"
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
        return token

    def get_reset_token_by_login(
            self,
            login: str
    ):
        auth_token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            print(f'USERDATALOGIN {user_data}')
            if user_login == login:
                try:
                    auth_token = user_data['ConfirmationLinkUri'].split('/')[-1]
                    print("Element is found")
                    break
                except KeyError:
                    print("Element not found")
            print(auth_token)
        return auth_token

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={"login": login, "password": password}
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def change_password(
            self,
            login: str,
            header_token: str,
            old_password: str,
            new_password: str
    ):

        self.dm_account_api.account_api.post_v1_account_password(
            json={
                "login": f"{login}",
                "email": f"{login}@mail.ru"
            }
        )

        auth_token = self.get_reset_token_by_login(
            login=login
        )
        assert auth_token is not None, f"Обновленный токен для пользователя {login} не был получен"

        json_data = {
            'login': login,
            'token': auth_token,
            'oldPassword': old_password,
            'newPassword': new_password
        }

        headers = {
            "X-Dm-Auth-Token": header_token
        }

        response = self.dm_account_api.account_api.put_v1_account_password(
            json=json_data,
            headers=headers
        )

        assert response.status_code == 200, f"Смена емайл для пользователя {login} неуспешна"
