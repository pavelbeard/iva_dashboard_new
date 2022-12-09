

class NoKeyscanData(Exception):
    def __init__(self, address: str, port: str | int):
        self.address = address
        self.port = port
        self.message = f"No key data from {address}:{port}. " \
                       f"Host is down or connection rejected by firewall!"


class NoConnectionWithServer(TimeoutError):
    def __init__(self, address: str, port):
        self.address = address
        self.port = port
        self.message = f"No connection to {address}:{port}. " \
                       f"Host is down or connection rejected by firewall!"
