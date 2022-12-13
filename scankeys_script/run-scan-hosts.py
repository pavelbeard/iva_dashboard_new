import asyncio
import os
import sys
import yaml
from script import scan_hosts


async def scanner(path_hosts: str,):
    with open(path_hosts, 'r') as h:
        config = yaml.safe_load(h)
        hosts = config.get('hosts')
        known_hosts_file = config.get('settings').get('known_hosts_location')

        keys = [asyncio.create_task(scan_hosts(conn_data=list(host.values()))) for host in hosts]

        done, pending = await asyncio.wait(keys, timeout=10, return_when=asyncio.FIRST_EXCEPTION)

        if os.path.exists(known_hosts_file):
            os.remove(known_hosts_file)

        with open(known_hosts_file, 'w') as file, open(known_hosts_file, 'r') as out:
            for done_task in done:
                if done_task.exception() is None:
                    file.write(done_task.result())
                else:
                    print(done_task.exception())
            for pending_task in pending:
                result = await pending_task.result()
                file.write(result)
            else:
                print("hosts are scanned!\n", out.read())


if __name__ == '__main__':
    try:
        if sys.argv[1] == "--path" or sys.argv[1] == "-p" and sys.argv != "":
            asyncio.run(scanner(path_hosts=sys.argv[2]))

        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(
                """
                Скрипт для создания файла servers_known_hosts для создания SSH-ключей\n 
                соединений агента дашборда IVA с машинами, которые он мониторит\n
                
                    - параметр -h | --help вызывает справку
                    - параметр -p | --path определяет путь, где сохранен файл <hosts>.yml, подлежащих мониторингу
                                
                Для того, чтобы запустить скрипт нужно написать: run-scan-hosts.py --path <путь к списку хостов> 
                """
            )
        else:
            raise IndexError
    except IndexError:
        print(
            """
            Для вызова справки напиши "-h" или "--help"
            """
        )
