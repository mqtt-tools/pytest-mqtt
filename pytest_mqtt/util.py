import socket
import threading


def delay(seconds: float = 0.075) -> None:
    """
    Wait for designated number of seconds.
    """
    threading.Event().wait(seconds)


def probe_tcp_connect(host: str, port: int) -> bool:
    """
    Test connecting to a remote TCP socket.
    https://github.com/lovelysystems/lovely.testlayers/blob/0.7.0/src/lovely/testlayers/util.py#L6-L13
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ex = s.connect_ex((host, port))
    if ex == 0:
        s.close()
        return True
    return False
