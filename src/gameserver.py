from gevent.monkey import patch_all; patch_all() #noqa
from db import PlayersDB
import gevent
import socket
import logging
import sys
import msg
import msg.login


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
        return ClientConnection(socket, address)
    

class ClientConnection:
    def __init__(self, socket, address):
        logger.info(f"Got connection from {address}")
        self.socket = socket
        self.address = address
        self.socket.settimeout(5.0)
        self.players = PlayersDB()
        self.is_running = True
        self.username = None
        self.connect()

    def close(self):
        logger.info(f"Disconnecting from {self.address}")
        self.socket.close()

    def send(msgtype, msgcontext):
        self.socket.send(msgtype + msgcontext)

    def connect(self):
        self.username = self.recv(1024)
        password = self.palyers.players_password(self.username)
        if password is None:
            self.send(msg.LOGIN, msg.login.FAILED)
            self.is_running = False
            logger.info(f"User {self.username} not found")
        else:
            self.send(msg.LOGIN, msg.login.SUCCESS)
            userpass = sefl.recv(1024)
            if userpass != password:
                self.send(msg.LOGIN, msg.login.FAILED)
                logger.warn(f"User {self.username} entered wrong password")
                self.is_running = False
            else:
                self.send(msg.LOGIN, msg.login.SUCCESS)

    def run(self):
        while self.is_running:
            try:
                msg = self.socket.recv(1024)
                if not msg:
                    self.is_running = False
                logger.info(f"Received {msg}")
            except socket.timeout:
                pass
        self.close()

        
class GameServer:
    def __init__(self, port=1234):
        self.tcp_connection = TcpSocket(port=port)

    def run(self):
        threads = []
        while True:
            client = self.tcp_connection.accept()
            threads.append(gevent.spawn(client.run))
