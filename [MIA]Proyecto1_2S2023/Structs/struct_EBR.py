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

class EBR(Objeto):
    # Constructor
    def __init__(self, status, fit, start, size, next, name):
        self.status = status     # char (1 byte)
        self.fit = fit           # char (1 byte)
        self.start = start       # int
        self.size = size         # int
        self.next = next         # int 
        self.name = name         # char (16 byte) 

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.status.encode('utf-8').ljust(1, b'\x00')
        bytes += self.fit.encode('utf-8').ljust(1, b'\x00')
        bytes += self.start.to_bytes(4, byteorder='big')
        bytes += self.size.to_bytes(4, byteorder='big')
        bytes += self.next.to_bytes(4, byteorder='big', signed=True)
        bytes += self.name.encode('utf-8').ljust(16, b'\x00')
        return bytes

    def set_bytes(self, bytes):
        self.status = bytes[0:1].decode('utf-8').rstrip('\x00')
        self.fit = bytes[1:2].decode('utf-8').rstrip('\x00')
        self.start = int.from_bytes(bytes[2:6], byteorder='big')
        self.size = int.from_bytes(bytes[6:10], byteorder='big')
        self.next = int.from_bytes(bytes[10:14], byteorder='big', signed=True)
        self.name = bytes[14:30].decode('utf-8').rstrip('\x00')
        return self

    def get_size(self):
        size = 0
        size += 1
        size += 1
        size += 4
        size += 4
        size += 4
        size += 16
        return size
        

# mbr = MBR(1234, 4123412, 79, 'B')
# mbr.particions.append(particion('w','w','w',0,0,'w'))
# mbr.particions.append(particion('','','',0,0,''))
# mbr.particions.append(particion('','','',0,0,''))
# mbr.particions.append(particion('','','',0,0,''))

# bytes = mbr.get_bytes()

# print(bytes)

# tmp = MBR(0, 0, 0, '')

# tmp.set_bytes(bytes)

# print(tmp.size)
# print(tmp.date)
# print(tmp.signature)
# print(tmp.fit)

# for elemen in tmp.particions:
#     print(elemen.name)

