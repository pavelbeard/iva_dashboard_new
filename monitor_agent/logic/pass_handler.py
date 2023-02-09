import base64

from cryptography.fernet import Fernet
from monitor_agent.agent.agent_logger import get_logger

logger = get_logger(__name__)


def decrypt_pass(encryption_key: str | bytes, password: str) -> str | None:
    try:
        __pass = base64.urlsafe_b64decode(password)
        cipher_pass = Fernet(encryption_key)
        decode_pass = cipher_pass.decrypt(__pass).decode('ascii')

        return decode_pass
    except (TypeError, ValueError) as te:
        logger.error(te.__class__.__name__, exc_info=True)
        return None
