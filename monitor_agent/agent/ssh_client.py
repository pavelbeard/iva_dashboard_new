import logging
import paramiko
from binascii import hexlify
from logging import DEBUG
from typing import Type
from paramiko.ssh_exception import SSHException
from .agent_logger import get_logger


logger = get_logger(__name__)


class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    """Класс, реализующий автодобавление открытых ключей с целевых хостов"""
    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


def run_cmd_on_target_host(conn_data: dict, timeout: int) -> str | Type[SSHException]:
    """
    Запускает ssh-клиент, который в свою очередь, выполняет команды на целевом хосте.\n
    :param conn_data: Данные для подключения: хост, порт, имя пользователя, пароль и команда.
    :param timeout: Время ожидания соединения с сервером.
    :return: В случае успеха str, в случае, если учетные данные неправильные
    или нет связи с сервером - SSHException.
    """
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy)
        hostname, port, username, password, cmd = list(conn_data.values())

        try:
            client.connect(hostname, port, username, password, timeout=timeout)
            stdin, stdout, stderr = client.exec_command(cmd, timeout*2)
            return bytes.decode(stdout.read(), encoding='utf-8')

        except paramiko.ssh_exception.AuthenticationException:
            logger.error("AuthenticationException", exc_info=True)
            raise paramiko.ssh_exception.AuthenticationException
        except paramiko.ssh_exception.NoValidConnectionsError:
            logger.error("NoValidConnectionsError", exc_info=True)
            raise paramiko.ssh_exception.NoValidConnectionsError
        except TimeoutError:
            logger.error("TimeoutError", exc_info=True)
            raise TimeoutError
        except PermissionError:
            logger.error("PermissionError", exc_info=True)
            raise PermissionError
        except OSError:
            logger.error("OSError", exc_info=True)
            raise OSError

