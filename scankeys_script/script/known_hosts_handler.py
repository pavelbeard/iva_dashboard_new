import asyncio.subprocess


async def scan_hosts(conn_data: list):
    host, port, *_ = conn_data
    proc = await asyncio.subprocess.create_subprocess_shell(
        cmd=f"ssh-keyscan.exe -t rsa,dsa -p {port} {host}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode('utf-8')
