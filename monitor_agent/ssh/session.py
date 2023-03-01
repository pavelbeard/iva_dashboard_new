import asyncio
from typing import Type

import asyncssh
import paramiko
from asyncssh import PermissionDenied
from binascii import hexlify
from logging import DEBUG

from paramiko.ssh_exception import SSHException, AuthenticationException, NoValidConnectionsError

from monitor_agent.agent import get_logger
from monitor_agent.logic.pass_handler import decrypt_pass
from monitor_agent.settings import ENCRYPTION_KEY

logger = get_logger(__name__)


class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    """Класс, реализующий автодобавление открытых ключей с целевых хостов"""

    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


class SSHSession:
    @staticmethod
    def _check_command_output_data(data):
        if data == '':
            return "command not found."

        return data

    async def arun_cmd_on_target(
            self, address: str, port: int, username: str,
            password: str, commands: dict, timeout: int
    ):
        try:
            host_key = await asyncssh.get_server_host_key(host=address, port=port)

            options = asyncssh.SSHClientConnectionOptions()
            options.key = host_key

            password = decrypt_pass(ENCRYPTION_KEY, password)

            result_dict = {}
            for key, command in commands.items():
                async with asyncssh.connect(
                        host=address, port=port, username=username, password=password,
                        options=options, known_hosts=None
                ) as conn:
                    if "sudo" in command:
                        result_sudo = await conn.run(f"echo {password} | sudo -S {command}")
                        result_dict[key] = self._check_command_output_data(result_sudo.stdout)
                    else:
                        result = await conn.run(command)
                        result_dict[key] = self._check_command_output_data(result.stdout)

            return result_dict
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError
        except ConnectionRefusedError:
            raise ConnectionRefusedError
        except PermissionDenied as e:
            raise PermissionDenied(e.reason)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def run_cmd_on_target(
            address: str, port: int, username: str,
            password: str, commands: dict, timeout: int) -> dict | Type[SSHException]:
        """
        Запускает ssh-клиент, который в свою очередь, выполняет команды на целевом хосте.\n
        :param address: адрес целевого хоста.
        :param port: порт.
        :param username: имя пользователя для входа в систему.
        :param password: пароль.
        :param commands: команды для выполения на целевом хосте.
        :param timeout: Время ожидания соединения с сервером.
        :return: В случае успеха str, в случае, если учетные данные неправильные
        или нет связи с сервером - SSHException.
        """
        result_dict = {}
        commands.pop('record_id')

        for key, command in commands.items():
            try:
                with paramiko.SSHClient() as client:
                    client.set_missing_host_key_policy(AutoAddPolicy)
                    decrypted_password = decrypt_pass(ENCRYPTION_KEY, password)

                    client.connect(address, port, username, decrypted_password, timeout=timeout)
                    stdin, stdout, stderr = client.exec_command(command, get_pty=True, timeout=timeout)

                    if "sudo" in command:
                        stdin.write(decrypted_password + "\n")
                        stdin.flush()

                    _out_ = stdout.read().decode('utf-8').replace(decrypted_password + "\r", "")
                    _err_ = stderr.read().decode('utf-8')

                    if len(_err_) > 0:
                        logger.warning(_err_)

                    result_dict[key] = _out_
            except TimeoutError as e:
                raise TimeoutError
            except AuthenticationException:
                raise AuthenticationException
            except NoValidConnectionsError as e:
                raise OSError(e.errors)
            except OSError as e:
                result_dict[key] = e
            except EOFError as e:
                result_dict[key] = e
            except Exception as e:
                result_dict[key] = e

        return result_dict