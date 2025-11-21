from abc import ABC

from sdk.request.register_parameters import RegisterRequestParameters


class AbstractRepository(ABC):
    def create_user(self, register_parameters: RegisterRequestParameters) -> str:
        return NotImplemented