import asyncssh
import aioredis

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


async def scankey_client(data: dict):

    pass
