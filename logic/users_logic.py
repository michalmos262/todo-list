from repository.postgres_repository import PostgresRepository
from sdk.request.register_parameters import RegisterRequestParameters


class UserLogic:
    def __init__(self):
        self.repository = PostgresRepository()

    def register(self, register_parameters: RegisterRequestParameters):
        return self.repository.create_user(register_parameters)
