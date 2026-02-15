import pprint
from json import loads

import pytest

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount
from helpers.account_helper import AccountHelper
import time




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
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account_helper.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Смена почты для пользователя {login} неуспешна"

    # Попытка входа с 403 ошибкой
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data={
        "login": login,
        "password": password,
        "remember_me": True
    })
    assert response.status_code == 403, f"Пользователь {login} не авторизован"

    # Поиск нового активационного токена на почте. Получение письма, нахождение нужного токена
    response = account_helper.mailhog.mailhog_api.get_api_v2_messages()
    pprint.pprint(response.json())
    assert response.status_code == 200, "Письма не были получены"

    token = get_activation_token_by_login(login, response)
    pprint.pprint(response.json())
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация обновленного пользователя
    response = account_helper.dm_account_api.account_api.put_v1_account_token(token=token)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Пользователь {login} не был активирован"

    # Повторная попытка авторизации
    account_helper.user_login(login=login, password=password, remember_me=True)


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
