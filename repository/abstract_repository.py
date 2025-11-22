from abc import ABC

from sdk.request.login_parameters import LoginRequestParameters
from sdk.request.register_parameters import RegisterRequestParameters


class AbstractRepository(ABC):
    def is_user_exist_by_email(self, email: str) -> bool:
        return NotImplemented

    def create_user(self, register_parameters: RegisterRequestParameters) -> str:
        return NotImplemented

    def get_user_auth_token(self, login_parameters: LoginRequestParameters) -> str | None:
        return NotImplemented