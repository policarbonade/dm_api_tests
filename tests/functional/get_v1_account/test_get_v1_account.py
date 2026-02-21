from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


def test_get_v1_account_auth(auth_account_helper):
    """
    Test auth user with authorized client
    :param auth_account_helper:
    """
    with check_status_code_http("", 200):
        response = auth_account_helper.get_account(is_validated=True)
        GetV1Account.check_get_v1_account_values(response)


def test_get_v1_account_no_auth(account_helper):
    """
    Test auth user with unauthorized client
    :param account_helper:
    """
    with check_status_code_http("User must be authenticated", 401):
        response = account_helper.get_account()
