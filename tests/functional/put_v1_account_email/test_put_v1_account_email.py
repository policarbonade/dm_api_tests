import pprint
from json import loads
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration


def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051')

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    # Регистрация пользователя
    login = 'polinad45'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не создан, {response.json()}"

    # Получить письма с почтового сервера
    response = mailhog_api.get_api_v2_messages()
    pprint.pprint(response.json())
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    pprint.pprint(response.json())
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Пользователь {login} не был активирован"

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Пользователь {login} не авторизован"

    # Смена емайл
    email = f'{login}+11@mail.ru'
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Смена почты для пользователя {login} неуспешна"

    # Попытка входа с 403 ошибкой
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 403, f"Пользователь {login} не авторизован"

    # Поиск нового активационного токена на почте. Получение письма, нахождение нужного токена
    response = mailhog_api.get_api_v2_messages()
    pprint.pprint(response.json())
    assert response.status_code == 200, "Письма не были получены"

    token = get_activation_token_by_login(login, response)
    pprint.pprint(response.json())
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация обновленного пользователя
    response = account_api.put_v1_account_token(token=token)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Пользователь {login} не был активирован"

    # Повторная попытка авторизации
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Пользователь {login} не авторизован"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        print(token)
    return token