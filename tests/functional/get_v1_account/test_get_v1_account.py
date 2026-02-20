from datetime import datetime
from hamcrest import (
    assert_that,
    has_property,
    empty,
    is_not,
    all_of,
    instance_of,
    has_properties,
    equal_to
)


def test_get_v1_account_auth(auth_account_helper):
    """
    Test auth user with authorized client
    :param auth_account_helper:
    """
    response = auth_account_helper.get_account(is_validated=True)
    assert_that(
        response, all_of(
            has_property("resource", has_properties({
                "info": equal_to(""),
                "online": instance_of(datetime),
                "registration": instance_of(datetime),
                "roles": instance_of(list),
                "settings": is_not(empty()),
                "rating": has_properties({
                    "enabled": equal_to(True),
                    "quality": equal_to(0),
                    "quantity": equal_to(0)
                })
            }))
        )
    )


def test_get_v1_account_no_auth(account_helper):
    """
    Test auth user with unauthorized client
    :param account_helper:
    """
    response = account_helper.get_account()
    assert response.status_code == 401, "Authorized user is retrieved"
