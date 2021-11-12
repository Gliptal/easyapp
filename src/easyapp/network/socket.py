from dataclasses import dataclass
import enum
from ipaddress import IPv4Address
import socket
import types

import logging


logger = logging.getLogger(__name__)


@dataclass
class Address:
    # yapf: disable
    ip   : IPv4Address
    port : int
    # yapf: enable


class BlockingMode(enum.Enum):
    # yapf: disable
    NON_BLOCKING = 0
    BLOCKING     = 1
    # yapf: enable


class UdpReceiver:

    def __init__(self, address: Address, blocking: BlockingMode = BlockingMode.NON_BLOCKING, timeout: float = 1.0, size: int = 1024 * 128):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.address = address
        self.blocking = blocking
        self.timeout = timeout
        self.size = size

    def __del__(self):
        logger.debug(f"closing UDP socket on {self.address.ip}:{self.address.port}")
        self.socket.close()

    def __enter__(self):
        logger.debug(f"opening {self.blocking.name.lower()} UDP socket on {self.address.ip}:{self.address.port} ({self.timeout}s timeout)")
        self.socket.bind((self.address.ip, self.address.port))

        return self

    def __exit__(self, etype: BaseException, eval: BaseException, traceback: types.TracebackType):
        self.socket.close()

    @property
    def address(self) -> Address:
        return self.__address

    @address.setter
    def address(self, value: Address):
        self.__address = value

    @property
    def blocking(self) -> BlockingMode:
        return self.__blocking

    @blocking.setter
    def blocking(self, value: BlockingMode):
        self.__blocking = value

        self.socket.setblocking(bool(self.blocking))

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value: float):
        self.__timeout = value

        self.socket.settimeout(self.timeout)

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, value: int):
        self.__size = value

    @property
    def buffer(self) -> bytes:
        try:
            return self.socket.recv(self.size)
        except socket.timeout:
            logger.warning(f"no message received within {self.timeout} seconds")
            raise TimeoutError
        except BlockingIOError:
            return b""
