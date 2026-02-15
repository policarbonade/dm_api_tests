def test_get_v1_account_auth(auth_account_helper):
    """
    Test auth user with authorized client
    :param auth_account_helper:
    """
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, "Authorized user is not retrieved"


def test_get_v1_account_no_auth(account_helper, prepare_user):
    """
    Test auth user with unauthorized client
    :param account_helper:
    """
    response = account_helper.dm_account_api.account_api.get_v1_account()
