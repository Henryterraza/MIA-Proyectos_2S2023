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

class SuperBlock(Objeto):
    # Constructor
    def __init__(self, filesystem_type, inodes_count , blocks_count, free_blocks_count, free_inodes_count, mtime, umtime, mnt_count, magic, inode_s, block_s, firts_ino,first_blo,bm_inode_start, bm_block_start,inode_start,block_start):
        self.filesystem_type = filesystem_type          # int
        self.inodes_count = inodes_count                # int
        self.blocks_count = blocks_count                # int
        self.free_blocks_count = free_blocks_count      # int
        self.free_inodes_count = free_inodes_count      # int
        self.mtime = mtime                              # int
        self.umtime = umtime                            # int
        self.mnt_count = mnt_count                      # int
        self.magic = magic                              # int
        self.inode_s = inode_s                          # int
        self.block_s = block_s                          # int
        self.firts_ino = firts_ino                      # int
        self.first_blo = first_blo                      # int
        self.bm_inode_start = bm_inode_start            # int
        self.bm_block_start = bm_block_start            # int
        self.inode_start = inode_start                  # int
        self.block_start = block_start                  # int

    def get_bytes(self):
        bytes = bytearray()
        bytes += self.filesystem_type.to_bytes(4, byteorder='big')      
        bytes += self.inodes_count.to_bytes(4, byteorder='big')           
        bytes += self.blocks_count.to_bytes(4, byteorder='big')           
        bytes += self.free_blocks_count.to_bytes(4, byteorder='big')      
        bytes += self.free_inodes_count.to_bytes(4, byteorder='big')      
        bytes += self.mtime.to_bytes(4, byteorder='big')                  
        bytes += self.umtime.to_bytes(4, byteorder='big')                 
        bytes += self.mnt_count.to_bytes(4, byteorder='big')              
        bytes += self.magic.to_bytes(4, byteorder='big')                  
        bytes += self.inode_s.to_bytes(4, byteorder='big')                
        bytes += self.block_s.to_bytes(4, byteorder='big')                
        bytes += self.firts_ino.to_bytes(4, byteorder='big')              
        bytes += self.first_blo.to_bytes(4, byteorder='big')              
        bytes += self.bm_inode_start.to_bytes(4, byteorder='big')         
        bytes += self.bm_block_start.to_bytes(4, byteorder='big')         
        bytes += self.inode_start.to_bytes(4, byteorder='big')            
        bytes += self.block_start.to_bytes(4, byteorder='big')            
        return bytes

    def set_bytes(self, bytes):
        self.filesystem_type = int.from_bytes(bytes[0:4], byteorder='big')      
        self.inodes_count = int.from_bytes(bytes[4:8], byteorder='big')
        self.blocks_count = int.from_bytes(bytes[8:12], byteorder='big')
        self.free_blocks_count = int.from_bytes(bytes[12:16], byteorder='big')
        self.free_inodes_count = int.from_bytes(bytes[16:20], byteorder='big')
        self.mtime = int.from_bytes(bytes[20:24], byteorder='big') 
        self.umtime = int.from_bytes(bytes[24:28], byteorder='big') 
        self.mnt_count = int.from_bytes(bytes[28:32], byteorder='big')
        self.magic = int.from_bytes(bytes[32:36], byteorder='big')                  
        self.inode_s = int.from_bytes(bytes[36:40], byteorder='big') 
        self.block_s = int.from_bytes(bytes[40:44], byteorder='big')
        self.firts_ino = int.from_bytes(bytes[44:48], byteorder='big')
        self.first_blo = int.from_bytes(bytes[48:52], byteorder='big')
        self.bm_inode_start = int.from_bytes(bytes[52:56], byteorder='big')
        self.bm_block_start = int.from_bytes(bytes[56:60], byteorder='big')
        self.inode_start = int.from_bytes(bytes[60:64], byteorder='big')
        self.block_start = int.from_bytes(bytes[64:68], byteorder='big')
        
        return self

    def get_size(self):
        size = 0
        size += 4 * 17
        return size
        