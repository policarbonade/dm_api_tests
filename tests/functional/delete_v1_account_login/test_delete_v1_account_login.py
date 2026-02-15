def test_logout(auth_account_helper):
    token = auth_account_helper.dm_account_api.account_api.session.headers.get("x-dm-auth-token")
    header_token = {
        "x-dm-auth-token": token
    }
    auth_account_helper.logout(header_token=header_token)
