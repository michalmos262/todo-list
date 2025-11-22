from exceptions.user_exceptions import UserAlreadyExists, AuthenticationFailed
from repository.postgres_repository import PostgresRepository
from sdk.request.login_parameters import LoginRequestParameters
from sdk.request.register_parameters import RegisterRequestParameters


class UserLogic:
    def __init__(self):
        self.repository = PostgresRepository()

    def register(self, register_parameters: RegisterRequestParameters):
        if self.repository.is_user_exist_by_email(register_parameters.email):
            raise UserAlreadyExists(f"Registration failed: user already exists with email {register_parameters.email}", 409)

        return self.repository.create_user(register_parameters)

    def login(self, login_parameters: LoginRequestParameters):
        user_token = self.repository.get_user_auth_token(login_parameters)
        if not user_token:
            raise AuthenticationFailed(f"Authentication failed: email or password is not correct", 401)
        return user_token