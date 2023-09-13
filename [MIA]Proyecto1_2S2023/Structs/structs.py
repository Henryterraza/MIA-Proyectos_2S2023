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

class particion(Objeto):
    # Constructor
    def __init__(self, status, type, fit, start, size, name):
        self.status = status    # char[1]
        self.type = type        # char[1]
        self.fit = fit          # char[1]
        self.start = start      # int[4]
        self.size = size        # int[4]
        self.name = name        # char[16]
    
    def get_bytes(self):
        bytes = bytearray()
        bytes += self.status.encode('utf-8').ljust(1, b'\x00')
        bytes += self.type.encode('utf-8').ljust(1, b'\x00')
        bytes += self.fit.encode('utf-8').ljust(1, b'\x00')
        bytes += self.start.to_bytes(4, byteorder='big')
        bytes += self.size.to_bytes(4, byteorder='big')
        bytes += self.name.encode('utf-8').ljust(16, b'\x00')
        return bytes

    def set_bytes(self, bytes):
        self.status = bytes[0:1].decode('utf-8').rstrip('\x00')
        self.type = bytes[1:2].decode('utf-8').rstrip('\x00')
        self.fit = bytes[2:3].decode('utf-8').rstrip('\x00')
        self.start = int.from_bytes(bytes[3:7], byteorder='big')
        self.size = int.from_bytes(bytes[7:11], byteorder='big')
        self.name = bytes[11:27].decode('utf-8').rstrip('\x00')
        return self


    def get_size(self):
        size = 0
        size += 1
        size += 1
        size += 1
        size += 4
        size += 4
        size += 16
        return size
    
class MBR(Objeto):
    # Constructor
    def __init__(self, size, date, signature, fit):
        self.size = size            # int
        self.date = date            # int
        self.signature = signature  # int
        self.fit = fit              # char (1 byte)
        self.particions = []         # lista de parciciones 

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.size.to_bytes(4, byteorder='big')
        bytes += self.date.to_bytes(4, byteorder='big')
        bytes += self.signature.to_bytes(4, byteorder='big')
        bytes += self.fit.encode('utf-8').ljust(1, b'\x00')

        for particion in self.particions:
            bytes += particion.get_bytes()
        return bytes

    def set_bytes(self, bytes):
        self.size = int.from_bytes(bytes[0:4], byteorder='big')
        self.date = int.from_bytes(bytes[4:8], byteorder='big')
        self.signature = int.from_bytes(bytes[8:12], byteorder='big')
        self.fit = bytes[12:13].decode('utf-8')
        
        # tmep = particion('','','',0,0,'')
        # self.particions.append(tmep.set_bytes(bytes[13:40]))
        # print(self.particions)

        sick = 13
        for i in range(0, 4):
            tmep = particion('','','',0,0,'')
            self.particions.append(tmep.set_bytes(bytes[sick:sick+27]))
            sick += 27 
        
        return self

    def get_size(self):
        size = 0
        size += 4
        size += 4
        size += 4
        size += 1
        for particion in self.particions:
            size += particion.get_size()
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

