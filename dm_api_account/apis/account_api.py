from models.change_password import ChangePassword
from models.registration import Registration
from models.reset_password import ResetPassword
from models.user_details_envelope import UserDetailsEnvelope
from models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):
    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :param registration:
        :return:
        """
        url = f"/v1/account"
        response = self.post(
            path=url,
            json=registration.model_dump(exclude_none=True, by_alias=True)
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
        UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            registration: Registration
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        url = f"/v1/account/email"
        response = self.put(
            path=url,
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        UserEnvelope(**response.json())
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
        UserDetailsEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            **kwargs
    ):
        """
        Change registered user email
        :return:
        """
        url = f"/v1/account/password"
        response = self.put(
            path=url,
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        UserEnvelope(**response.json())
        return response

    def post_v1_account_password(
        self,
        reset_password: ResetPassword,
        **kwargs
    ):
        """
        Reset registered user email
        :return:
        """
        url = f"/v1/account/password"
        response = self.post(
            path=url,
            json=reset_password.model_dump(exclude_none=True),
            **kwargs
        )
        UserEnvelope(**response.json())
        return response
