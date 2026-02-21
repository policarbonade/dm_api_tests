from datetime import datetime
import pytest
from checkers.http_checkers import check_status_code_http
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to
)


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, is_validated=True)
    assert_that(
        response, all_of(
            has_property("resource", has_property("login", starts_with(login))),
            has_property("resource", has_property("registration", instance_of(datetime))),
            has_property(
                "resource", has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )


@pytest.mark.parametrize(
    # Тут, в принципе, везде одна ошибка 400 и одинаковый текст
    # для всех тестов, поэтому не передаю их в качестве параметров
    ("login", "email", "password"),
    [
        ("keyloack", "keyloack@mail.ru", "12345"),
        ("keyloack", "keyloack@@mail.ru", "123456"),
        ("k", "keyloack@mail.ru", "123456")
    ]
)
def test_post_v1_account_invalid_data(account_helper, login, email, password):
    with check_status_code_http(expected_message="Validation failed", expected_status_code=400):
        account_helper.post_v1_account_isolation(login=login, email=email, password=password)
