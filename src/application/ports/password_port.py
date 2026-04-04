from abc import ABC, abstractmethod


class PasswordServicePort(ABC):
    """
    Port for password hashing and verification.
    Implementation lives in infrastructure layer.
    """

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass
