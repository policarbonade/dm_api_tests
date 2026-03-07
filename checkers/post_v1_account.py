from datetime import datetime

import allure
from assertpy import assert_that
from hamcrest import (
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to
)


class PostV1Account:
    @classmethod

    @allure.step("Валидация значений ответа")
    def check_response_values(cls, response, login):
        today = datetime.now().strftime("%Y_%m_%d")
        assert_that(str(response.resource.registration), starts_with(today))
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