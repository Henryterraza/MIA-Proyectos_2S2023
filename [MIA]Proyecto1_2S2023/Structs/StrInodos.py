from abc import ABC, abstractmethod


class Objeto(ABC):
    @abstractmethod
    def get_bytes(self):
        pass

    @abstractmethod
    def set_bytes(self, bytes):
        pass

    @abstractmethod
    def get_size(self):
        pass


class Inodo(Objeto):
    # Constructor
    def __init__(self, uid, gid, size, atime, ctime, mtime, type, perm):
        self.uid = uid  # int
        self.gid = gid  # int
        self.size = size  # int
        self.atime = atime  # int
        self.ctime = ctime  # int
        self.mtime = mtime  # int
        self.type = type  # char[1]
        self.perm = perm  # int
        self.blocks = []  # lista[60]
        for block in range(0, 15):
            self.blocks.append(-1)

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.uid.to_bytes(4, byteorder="big")
        bytes += self.gid.to_bytes(4, byteorder="big")
        bytes += self.size.to_bytes(4, byteorder="big")
        bytes += self.atime.to_bytes(4, byteorder="big")
        bytes += self.ctime.to_bytes(4, byteorder="big")
        bytes += self.mtime.to_bytes(4, byteorder="big")
        bytes += self.type.encode("utf-8").ljust(1, b"\x00")
        bytes += self.perm.to_bytes(4, byteorder="big")

        for block in self.blocks:
            bytes += block.to_bytes(4, byteorder="big", signed=True)

        return bytes

    def set_bytes(self, bytes):
        self.uid = int.from_bytes(bytes[0:4], byteorder="big")
        self.gid = int.from_bytes(bytes[4:8], byteorder="big")
        self.size = int.from_bytes(bytes[8:12], byteorder="big")
        self.atime = int.from_bytes(bytes[12:16], byteorder="big")
        self.ctime = int.from_bytes(bytes[16:20], byteorder="big")
        self.mtime = int.from_bytes(bytes[20:24], byteorder="big")
        self.type = bytes[24:25].decode("utf-8").rstrip("\x00")
        self.perm = int.from_bytes(bytes[25:29], byteorder="big")
        self.blocks = []

        sick = 4
        for i in range(0, 15):
            self.blocks.append(int.from_bytes(bytes[25 + sick : 29 + sick], byteorder="big", signed=True))
            sick += 4

        return self

    def get_size(self):
        size = 0
        size += 4 * 7
        size += 1
        size += 4 * 15

        return size