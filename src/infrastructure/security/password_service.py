import bcrypt

from src.application.ports.password_port import PasswordServicePort


class PasswordService(PasswordServicePort):
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # bcrypt.checkpw requires bytes
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        # bcrypt.hashpw requires bytes, returns bytes. Decode to store as string.
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
