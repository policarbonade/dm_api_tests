import pprint
from json import loads
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount
from helpers.account_helper import AccountHelper


def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051')

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # Регистрация пользователя
    login = 'polinad62'
    password = '123456789'
    email = f'{login}@mail.ru'

    account_helper.register_user(email=email, password=password, login=login)

    # Авторизоваться
    account_helper.user_login(login=login, password=password, remember_me=True)

    # Смена емайл
    email = f'{login}+22@mail.ru'
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account.account_api.put_v1_account_email(json_data=json_data)
    pprint.pprint(response.json())
    assert response.status_code == 200, f"Смена почты для пользователя {login} неуспешна"

    # Попытка входа с 403 ошибкой
    response = account_helper.user_login(login=login, password=password, remember_me=True)
    assert response.status_code == 403, f"Пользователь {login} не авторизован"

    # Поиск нового активационного токена на почте. Получение письма, нахождение нужного токена
    response = mailhog.mailhog_api.get_api_v2_messages()
    pprint.pprint(response.json())
    assert response.status_code == 200, "Письма не были получены"

    token = get_activation_token_by_login(login, response)
    pprint.pprint(response.json())
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация обновленного пользователя
    response = account.account_api.put_v1_account_token(token=token)
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
