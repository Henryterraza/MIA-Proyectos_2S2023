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


class Journaling(Objeto):
    # Constructor
    def __init__(self, operacion, path, contenido, fecha):
        self.operacion = operacion          # char[6]
        self.path = path                    # char[300] 
        self.contenido = contenido          # char[7000] if file or char[1] if dir
        self.fecha = fecha                  # int

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.operacion.encode("utf-8").ljust(6, b"\x00")  
        bytes += self.path.encode("utf-8").ljust(300, b"\x00")
        bytes += self.contenido.encode("utf-8").ljust(2000, b"\x00")
        bytes += self.fecha.to_bytes(4, byteorder="big")

        return bytes

    def set_bytes(self, bytes):
        self.operacion = bytes[0:6].decode("utf-8").rstrip("\x00")  
        self.path = bytes[6:306].decode("utf-8").rstrip("\x00")
        self.contenido = bytes[306:2306].decode("utf-8").rstrip("\x00")
        self.fecha = int.from_bytes(bytes[2306:2310], byteorder="big")
        return self

    def get_size(self):
        size = 0
        size += 6
        size += 300
        size += 2000
        size += 4

        return size
    
# hola = Journaling("mkfile", "dhfkashdj", "jdfhaskf", 46153165)
# bytes = hola.get_bytes()

# # print(bytes)

# hola2 = Journaling("", "", "", 0)
# objeto = hola2.set_bytes(bytes)

# print(objeto.operacion)
# print(objeto.path)
# print(objeto.contenido)
# print(objeto.fecha)
# print(objeto.get_size())

