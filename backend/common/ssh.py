import paramiko

from binascii import hexlify
from paramiko.common import DEBUG
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError

from app_logging.app_logger import get_logger

logger = get_logger(__name__)


class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    """Класс, реализующий автодобавление открытых ключей с целевых хостов"""

    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


def ssh_scraper(command, **conn_data):
    host = conn_data.get('host')
    port = conn_data.get('port')
    username = conn_data.get('username')
    password = conn_data.get('password')

    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy)

        try:
            client.connect(hostname=host, port=port,
                           username=username, password=password, timeout=3)

            if 'sudo' in command:
                command = str.replace(command, "sudo", "")
                stdin, stdout, stderr = client.exec_command(
                    f"echo {password} | sudo -S {command}"
                )
                return stdout.read().decode('utf8')

            stdin, stdout, stderr = client.exec_command(command)
            return stdout.read().decode('utf-8')
        except TimeoutError as e:
            logger.error(e.args[0])
            return None
        except AuthenticationException as e:
            logger.error(e.args[0])
            return None
        except NoValidConnectionsError as e:
            logger.error(e.args[0])
            return None
        except Exception as e:
            logger.error(e.args[0])
            return None
