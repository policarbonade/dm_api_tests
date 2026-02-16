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
    response = account_helper.put_account_email(json_data=json_data)
    assert response.status_code == 200, f"Смена почты для пользователя {login} неуспешна"

    # Попытка входа с 403 ошибкой
    response = account_helper.user_login(login=login, password=password, remember_me=True)
    assert response.status_code == 403, f"Пользователь {login} не авторизован"

    account_helper.activate(login=login)

    # Повторная попытка авторизации
    account_helper.user_login(login=login, password=password, remember_me=True)
