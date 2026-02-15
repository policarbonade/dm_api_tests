from restclient.client import RestClient


class AccountApi(RestClient):
    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        url = f"/v1/account"
        response = self.post(
            path=url,
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        url = f"/v1/account/{token}"
        headers = {
            'Accept': 'text/plain'
        }
        response = self.put(
            path=url,
            headers=headers,
            params=token
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        url = f"/v1/account/email"
        response = self.put(
            path=url,
            json=json_data
        )

        print(response.json())
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        url = f"/v1/account"
        response = self.get(
            path=url,
            **kwargs
        )
        return response

    def put_v1_account_password(
            self,
            **kwargs
    ):
        """
        Change registered user email
        :return:
        """
        url = f"/v1/account/password"
        response = self.put(
            path=url,
            **kwargs
        )

        print(response.json())
        return response

    def post_v1_account_password(
        self,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/password"
        response = self.post(
            path=url,
            **kwargs
        )

        print(response.json())
        return response

    def delete_v1_account_login(
        self,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/login"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response

    def delete_v1_account_login_all(
        self,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/login/all"
        response = self.delete(
            path=url,
            **kwargs
        )

        return response
