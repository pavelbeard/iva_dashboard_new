from binascii import hexlify
from logging import DEBUG
from typing import Type

import asyncssh
import paramiko
from paramiko.ssh_exception import SSHException


class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    """Класс, реализующий автодобавление открытых ключей с целевых хостов"""
    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


async def run_cmd_on_client(data: dict) -> str | TimeoutError:
    """
    Функция запускает ssh-соединение и вытаскивает с хоста нужную информацию.\n
    :param data: Данные для подключения и команды для выполнения на удаленном хосте.
    :return: str | TimeoutError
    """
    host, port, username, password, keys, cmd = list(data.values())

    async with asyncssh.connect(
            host=host, port=int(port), username=username, password=password,
            known_hosts=asyncssh.import_known_hosts(keys)
    ) as session:
        result = await session.run(cmd)
        return result.stdout


def run_cmd_on_target_host(conn_data: dict) -> str | Type[SSHException]:
    """
    Запускает ssh-клиент, который в свою очередь, выполняет команды на целевом хосте.\n
    :param conn_data: Данные для подключения: хост, порт, имя пользователя, пароль и команда
    :return: В случае успеха str, в случае, если учетные данные неправильные
    или нет связи с сервером - SSHException
    """
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy)
        hostname, port, username, password, cmd = list(conn_data.values())

        try:
            client.connect(hostname, port, username, password, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmd)
            return bytes.decode(stdout.read(), encoding='utf-8')

        except paramiko.ssh_exception.AuthenticationException:
            raise paramiko.ssh_exception.AuthenticationException
        except paramiko.ssh_exception.SSHException:
            return paramiko.ssh_exception.SSHException
