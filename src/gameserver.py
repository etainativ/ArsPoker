from gevent.monkey import patch_all; patch_all() #noqa
import gevent
import socket
import logging
import sys


logformat = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
logging.basicConfig(
        level=logging.DEBUG,
        format=logformat,
        datefmt="%H:%M:%S",
        stream=sys.stdout)
logger = logging.getLogger("main")


class TcpSocket:
    def __init__(self, port, address="0.0.0.0"):
        self.address = address
        self.port = port
        self.socket = self._init_socket()
        self._bind_socket(self.socket, self.address, self.port)

    def _init_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _bind_socket(self, socket, address, port):
        logger.info(f"Binding to {address}:{port}")
        socket.bind((address, port))
        socket.listen(128)

    def accept(self):
        socket, address = self.socket.accept()
        logger.info(f"Got connection from {address}")
        return ClientConnection(socket)
    

class ClientConnection:
    def __init__(self, socket):
        self.socket = socket
        self.socket.settimeout(5.0)


    def run(self):
        if not self.do_handshake():
            return

    def do_handshake(self):
        username = self.socket.recv(1024)
        self.socket.send(b"\x01")
        password = self.socket.recv(1024)
        self.socket.send(b"\x01")
        logger.info(f"User: {username} connected with pwd {password}")

        
class GameServer:
    def __init__(self, port=1234):
        self.tcp_connection = TcpSocket(port=port)

    def run(self):
        threads = []
        while True:
            client = self.tcp_connection.accept()
            threads.append(gevent.spawn(client.run))
