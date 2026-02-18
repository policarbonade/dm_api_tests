from models.change_password import ChangePassword
from models.login_credentials import LoginCredentials
from models.registration import Registration
from models.reset_password import ResetPassword
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

        registration = Registration(
            login=login,
            email=email,
            password=password
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не создан, {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь {login} не был активирован"
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials)
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
            try:
                user_data = loads(item['Content']['Body'])
                user_login = user_data['Login']
                if user_login == login:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            except Exception:
                print("Битый формат ответа")
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
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=True
        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials)
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        return token

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):

        # Authorization
        response = self.user_login(
            login=login,
            password=old_password
        )

        # Смена пароля с пробросом авторизационного токена в хэдэры
        header_token = response.headers["X-Dm-Auth-Token"]

        reset_password = ResetPassword(
            login=login,
            email=email
        )

        self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        reset_token = self.get_reset_token_by_login(
            login=login
        )
        assert reset_token is not None, f"Обновленный токен для пользователя {login} не был получен"

        change_password = ChangePassword(
            login=login,
            token=reset_token,
            old_password=old_password,
            new_password=new_password
        )

        headers = {
            "X-Dm-Auth-Token": header_token
        }

        response = self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_password,
            headers=headers
        )

        assert response.status_code == 200, f"Смена емайл для пользователя {login} неуспешна"
        return response

    def logout(self):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, f"User is not logged out"

    def logout_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, f"User is not logged out out of every session"

    def get_account(self):
        response = self.dm_account_api.account_api.get_v1_account()
        return response

    def put_account_email(self, login, password, email):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(registration=registration)
        return response

    def activate(self, login):
        # Поиск нового активационного токена на почте. Получение письма, нахождение нужного токена
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        token = self.get_activation_token_by_login(login)
        assert token is not None, f"Токен для пользователя не был получен"

        # Активация обновленного пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Пользователь не был активирован"
