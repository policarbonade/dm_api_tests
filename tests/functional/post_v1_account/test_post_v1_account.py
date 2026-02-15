import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DmApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051')

    account = DmApiAccount(configuration=dm_api_configuration)

    # Регистрация пользователя
    login = 'polinad63'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не создан, {response.json()}"
