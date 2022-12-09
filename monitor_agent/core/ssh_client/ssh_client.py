import asyncssh

async def run_client(conn_data: dict, cmd: str) -> str | TimeoutError:
    """
    Функция запускает ssh-соединение и вытаскивает с хоста нужную информацию.\n
    :param conn_data: Данные для подключения.
    :param cmd: Команда(ы) для мониторинга
    :return: str | TimeoutError
    """
    host, port, username, password, keys = list(conn_data.values())

    async with asyncssh.connect(
        host=host, port=int(port), username=username, password=password,
        known_hosts=asyncssh.import_known_hosts(keys)
    ) as session:
        result = await session.run(cmd, check=True)
        return result.stdout
