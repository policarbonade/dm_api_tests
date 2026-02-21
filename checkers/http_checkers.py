import requests
from requests.exceptions import HTTPError
from contextlib import contextmanager


@contextmanager
def check_status_code_http(
        expected_message: str = "",
        expected_status_code: requests.codes = requests.codes.OK
):

    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Expected status code {expected_status_code} but request succeeded")
        if expected_message:
            raise AssertionError(f"Expected to receive '{expected_message}' message")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()["title"] == expected_message