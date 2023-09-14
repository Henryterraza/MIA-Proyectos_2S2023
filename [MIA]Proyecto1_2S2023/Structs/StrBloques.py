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


class Carpeta(Objeto):
    # Constructor
    def __init__(self, padre, actual, ApunPadre, ApuntActual, NameCarpArch1, NameCarpArch2, Apun1, Apunt2):
        self.padre = padre                  # char[12]
        self.actual = actual                # char[12]
        self.ApunPadre = ApunPadre          # int
        self.ApuntActual = ApuntActual      # int
        self.NameCarpArch1 = NameCarpArch1  # char[12]
        self.NameCarpArch2 = NameCarpArch2  # char[12]
        self.Apun1 = Apun1                  # int
        self.Apunt2 = Apunt2                # int

    def get_bytes(self):
        bytes = bytearray()

        bytes += self.padre.encode("utf-8").ljust(12, b"\x00")
        bytes += self.actual.encode("utf-8").ljust(12, b"\x00")
        bytes += self.ApunPadre.to_bytes(4, byteorder="big")
        bytes += self.ApuntActual.to_bytes(4, byteorder="big")
        bytes += self.NameCarpArch1.encode("utf-8").ljust(12, b"\x00")
        bytes += self.NameCarpArch2.encode("utf-8").ljust(12, b"\x00")
        bytes += self.Apun1.to_bytes(4, byteorder="big", signed=True)
        bytes += self.Apunt2.to_bytes(4, byteorder="big", signed=True)
        return bytes

    def set_bytes(self, bytes):

        self.padre  = bytes[0:12].decode("utf-8").rstrip("\x00")
        self.actual = bytes[12:24].decode("utf-8").rstrip("\x00")
        self.ApunPadre = int.from_bytes(bytes[24:28], byteorder="big")
        self.ApuntActual = int.from_bytes(bytes[28:32], byteorder="big")
        self.NameCarpArch1 = bytes[32:44].decode("utf-8").rstrip("\x00")
        self.NameCarpArch2 = bytes[44:56].decode("utf-8").rstrip("\x00")
        self.Apun1 = int.from_bytes(bytes[56:60], byteorder="big")
        self.Apunt2 = int.from_bytes(bytes[60:64], byteorder="big")

        return self

    def get_size(self):
        size = 0
        size += 4 * 12
        size += 4 * 4

        return size
    

class Archivo(Objeto):
    # Constructor
    def __init__(self, contenido):
        self.contenido = contenido                  # char[64]

    def get_bytes(self):
        bytes = bytearray()

        bytes += self.contenido.encode("utf-8").ljust(64, b"\x00")
      
        return bytes

    def set_bytes(self, bytes):

        self.contenido  = bytes[0:64].decode("utf-8").rstrip("\x00")
        return self

    def get_size(self):
        size = 64

        return size
    
class Apuntadores(Objeto):
    # Constructor
    def __init__(self):
        self.apuntadores = []                  # char[64]

        for apuntador in  range(0,16):
            self.apuntadores.append(-1)


    def get_bytes(self):
        bytes = bytearray()

        for apuntador in self.apuntadores:
            bytes += apuntador.to_bytes(4, byteorder="big", signed=True)
      
        return bytes

    def set_bytes(self, bytes):
        self.apuntadores = []

        sick = 0
        for i in range(0, 16):
            self.apuntadores.append(int.from_bytes(bytes[0 + sick : 4 + sick], byteorder="big", signed=True))
            sick += 4

        return self

    def get_size(self):
        size = 64

        return size