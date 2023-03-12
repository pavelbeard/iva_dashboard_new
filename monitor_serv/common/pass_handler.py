import base64

from app_logging import app_logger
from cryptography.fernet import Fernet

logger = app_logger.get_logger(__name__)


def encrypt_pass(encryption_key: str | bytes, password: str) -> str | None:
    try:
        __pass = password
        cipher_pass = Fernet(encryption_key)
        encrypted_pass = cipher_pass.encrypt(password.encode('ascii'))
        complete_encrypt_pass = base64.urlsafe_b64encode(encrypted_pass).decode('ascii')

        return complete_encrypt_pass
    except (TypeError, ValueError) as te:
        logger.error(te.__class__.__name__, exc_info=True)
        return None


def decrypt_pass(encryption_key: str | bytes, password: str) -> str | None:
    try:
        __pass = base64.urlsafe_b64decode(password)
        cipher_pass = Fernet(encryption_key)
        decode_pass = cipher_pass.decrypt(__pass).decode('ascii')

        return decode_pass
    except (TypeError, ValueError) as te:
        logger.error(te.__class__.__name__, exc_info=True)
        return None
