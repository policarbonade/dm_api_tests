from datetime import datetime
from assertpy import assert_that, soft_assertions
from models.user_envelope import UserRole
from hamcrest import (
    assert_that as hamcrest_that,
    has_property,
    empty,
    is_not,
    all_of,
    instance_of,
    has_properties,
    equal_to
)


class GetV1Account:
    @classmethod
    def check_get_v1_account_values(cls, response):
        hamcrest_that(
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

        with soft_assertions():
            assert_that(response.resource.login).is_equal_to("joepeach9")
            assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
            assert_that(response.resource.online).is_instance_of(datetime)