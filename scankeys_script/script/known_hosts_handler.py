import asyncio.subprocess


async def scan_hosts(conn_data: list):
    host, port, *tmp = conn_data
    proc = await asyncio.subprocess.create_subprocess_shell(
        cmd=f"ssh-keyscan.exe -t rsa,dsa -p {port} {host}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode('utf-8')


async def write_to_file(known_hosts_location: str, keys: list, reset_file_request: bool = False):
    # if reset_file_request:
    #     os.remove(known_hosts_location)
    #
    # with open(known_hosts_location, 'a') as known_hosts:
    #     pass
    #         # if proc.stderr is not None:
    #         #     return None
    #         # else:
    #         #     known_hosts.write(proc.stdout.decode('utf-8'))
    pass


def known_hosts_diff(known_hosts_location: str, hosts: list):
    # with open(known_hosts_location, 'r') as known_hosts:
    #     # первой выполняется функция map, далее функция map передает результат filter и тот отсекает пустые массивы
    #     diff = list(filter(
    #         lambda y: y is not None,
    #         map(lambda x: x[0] if len(x) != 0 else None, [host.split() for host in known_hosts.read().split('\n')])
    #     ))
    #
    #
    #     scan_hosts(conn_data=hosts)
    #
    #     if len(hosts) < len(diff):
    #
    #         write_to_file(
    #             keys=keys, known_hosts_location=known_hosts_location, reset_file_request=True
    #         )
    #     elif len(hosts) == len(diff):
    #         pass
    #     else:
    #         write_to_file(
    #             keys=keys[len(diff):], known_hosts_location=known_hosts_location
    #         )
    pass