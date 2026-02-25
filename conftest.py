import pytest
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailHogApi
from helpers.account_helper import AccountHelper
from datetime import datetime
from collections import namedtuple
import structlog
from pathlib import Path
from vyper import v

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
)


def pytest_addoption(parser):
    parser.addoption("--env", action="store_true", default="stage", help="run stage")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../").joinpath("config")
    config_name = request.config.getoption("--env")
    print(config)
    print(config_name)
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"))
    account = DmApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=False)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get("user.login"),
        password=v.get("user.password")
    )
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    date = now.strftime('%d_%m_%Y_%H_%M_%S_%f')
    login = f'polinad_{date}'
    password = v.get("user.password")
    email = f'{login}@mail.ru'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, email=email, password=password)
    return user


@pytest.fixture
def prepare_password():
    now = datetime.now()
    date = now.strftime('%d_%m_%Y_%H_%M_%S_%f')
    password = date
    return password
