from sintactico import parser
from Structs.structs import MBR, particion
from Structs.struct_EBR import EBR
from Structs.structmount import mount
from Structs.strSuperBlock import SuperBlock
from Structs.StrInodos import Inodo
from Structs.StrBloques import Carpeta, Archivo, Apuntadores 
from Structs.StrJournaling import Journaling
from graphviz import Digraph
import os
import datetime
import random
import subprocess
import math

ListMount = []


def menu():
  
    while True:
        comando = input("\nIngrese comando: ")
        result = parser.parse(comando)
        print(result)

        ListComand = result[0][1]

        if result[0][0] == "execute":
            if "path" in ListComand:
                path = ListComand[ListComand.index("path") + 1]

                respuesta = Obtener_Cont_Archivo(path)

                if respuesta != None:
                    result2 = parser.parse(respuesta)
                    for comando in result2:
                        print(comando)
                        verificar_Comando(comando[0], comando[1])
                else:
                    print("No existe el archivo")
            else:
                print("El comando execute requiere del parametro path")
        else:
            verificar_Comando(result[0][0], ListComand)


       

def verificar_Comando(comando, ListComand):
    if comando== "mkdisk":
        comando_mkdisk(ListComand)

    elif comando == "rmdisk":
        if "path" in ListComand:
            path = ListComand[ListComand.index("path") + 1]
            eliminar_archivo(path)
        else:
            print("comando requiere del path")
    elif comando == "fdisk":
        comando_fdisk(ListComand)
    elif comando == "mount":
        comando_mount(ListComand)
    elif comando == "unmount":
        comando_unmount(ListComand)
    elif comando == "rep":
        comando_rep(ListComand)
    elif comando == "mkfs":
        comando_mkfs(ListComand)

    elif comando == "pause":
        if ListComand == None:
            while True:
                entrada = input("Presione Enter para continuar...")

                if entrada == "":
                    break
                else:
                    print("Entrada inválida. Solo presione Enter.")
        else:
            print("comando pausa no requiere de parametros")
    else:
        print("comando no aceptado")

def Obtener_Cont_Archivo(path):
    contenido = ""
    if os.path.exists(path):
        with open(path, "r") as archivo:
            contenido = archivo.read()

    else:
        contenido = None
    
    return contenido
    
def comando_mkfs(ListComand):
    if "id" in ListComand:
        id = ListComand[ListComand.index("id") + 1]

        if "type" in ListComand:
            type = ListComand[ListComand.index("type") + 1]
            if type != "full":
                print("el parametro type requiere de full")
                return
        else:
            type = "full"

        if "fs" in ListComand:
            fs = ListComand[ListComand.index("fs") + 1]

            if fs != "2fs" and fs != "3fs":
                print("el parametro fs requiere de 2fs/3fs")
                return
        else:
            fs = "2fs"

        IdExist = buscar_id(id)

        if IdExist.tipo != "E":

            if IdExist != None and IdExist.status != 0:
                seekInicio = IdExist.SeekDSKInicio
                seekFin = IdExist.SeekDSKFin
                path = IdExist.path

                
                if fs == "2fs":
                    byteParticion = OptenerByte_archivo(path, seekInicio, seekFin - seekInicio)
                    
                    temp = SuperBlock(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

                    Objeto = temp.set_bytes(byteParticion)


                    if Objeto.filesystem_type == 0:
                        # n = (tamaño_particion - sizeOf(superblock) / (1 + 3 * 1 + 1 * sizeOf(inodos) + 3 *1 * sizeOf(block))
                        n = ((seekFin-seekInicio) - 68) / (1+3+89+(3*64))
                        numero_structuras = math.floor(n)

                        PInodo= (seekInicio + 68 + numero_structuras) + (numero_structuras * 3)
                        pBloque= PInodo + (numero_structuras * 89)

                        Sup_Block = SuperBlock(2, numero_structuras, 3* numero_structuras, 3*numero_structuras, numero_structuras, 0, 0, 0, 0xEF53, 89, 64, PInodo, pBloque, seekInicio + 68, seekInicio + 68 + numero_structuras, PInodo, pBloque )
                        byteSupBLock = Sup_Block.get_bytes()
                        
                        
            
                        bytes = bytearray()

                        ceros = [0] * (4*numero_structuras)

                        for cero in ceros:
                            bytes += cero.to_bytes(1, byteorder="big")
                        

                        temp = Inodo(0,0,0,0,0,0,"",0)
                        for cont in range(numero_structuras):
                            bytes += temp.get_bytes()

                        temp = Carpeta(".","..",0,0,"","",-1,-1)
                        for cont in range((3*numero_structuras)):
                            bytes += temp.get_bytes()

                        byteSupBLock += bytes 

                        byteModPaticion = byteSupBLock + byteParticion[len(byteSupBLock):]

                        Guardar_enArchivo(path, byteModPaticion, seekInicio, seekFin )
                        print(f"Se formatio la particion a EXT2 ")
                    else:
                        print(f"ya existe un formateo de EXT{Objeto.filesystem_type} ")


                else:
                    
                    byteParticion = OptenerByte_archivo(path, seekInicio, seekFin - seekInicio)
                    

                    temp = SuperBlock(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

                    Objeto = temp.set_bytes(byteParticion)

                    if Objeto.filesystem_type == 0:
                        # n = (tamaño_particion - sizeOf(superblock) / (1 + 1 * 2310+3*1 + 1 * sizeOf(inodos) + 3 *1 * sizeOf(block))
                    
                        n = ((seekFin-seekInicio) - 68) / (1+2310+3+89+(3*64))
                        numero_structuras = math.floor(n)

                        PInodo= (seekInicio + 68 + (numero_structuras*2310) + numero_structuras + (3*numero_structuras) )
                        pBloque= PInodo + (numero_structuras*89)

                        Sup_Block = SuperBlock(3, numero_structuras, 3* numero_structuras, 3*numero_structuras, numero_structuras, 0, 0, 0, 0xEF53, 89, 64, PInodo, pBloque, seekInicio + 68 + (numero_structuras*2310), seekInicio + 68 + (numero_structuras*2310) + numero_structuras, PInodo, pBloque )
                        byteSupBLock = Sup_Block.get_bytes()
                        
                    
            
                        bytes = bytearray()

                        temp = Journaling("","","",0)
                        for i in range(numero_structuras):
                            bytes += temp.get_bytes()
                            

                        ceros = [0] * (4*numero_structuras)
                        for cero in ceros:
                            bytes += cero.to_bytes(1, byteorder="big")
                        

                        temp = Inodo(0,0,0,0,0,0,"",0)
                        for cont in range(numero_structuras):
                            bytes += temp.get_bytes()
                        
                        temp = Carpeta(".","..",0,0,"","",-1,-1)
                        for cont in range((3*numero_structuras)):
                            bytes += temp.get_bytes()
                        

                        byteSupBLock += bytes

                        byteModPaticion = byteSupBLock + byteParticion[len(byteSupBLock):]

                        Guardar_enArchivo(path, byteModPaticion, seekInicio, seekFin )
                        print(f"Se formatio la particion a EXT3 ")

                    else:
                        print(f"ya existe un formateo de EXT{Objeto.filesystem_type} ")

            else:
                print("id no encontrado")
        else:
            print("El formateo no se puede realizar en una particion extendida")


    else:
        print("El comando requiere del parametro id")

def comando_rep(ListComand):
    if "name" in ListComand and "path" in ListComand and "id" in ListComand:
        name = ListComand[ListComand.index("name") + 1]
        path = ListComand[ListComand.index("path") + 1]
        id = ListComand[ListComand.index("id") + 1]
        IdExist = buscar_id(id)

        if IdExist != None and IdExist.status != 0 :
            PathDSK = IdExist.path

            if name == "mbr":
                ReporteMBR(path, PathDSK)
            elif name == "disk":
                reporte_disk(path, PathDSK, IdExist)
            elif name == "sb":
                reporte_sb(path, PathDSK, IdExist)
            elif name == "bm_inode":
                reporte_bm_inode(path, PathDSK, IdExist)
            elif name == "bm_bloc":
                reporte_bm_bloc(path, PathDSK, IdExist)
            else:
                print(f"El valor del parametro -name={name} no es aceptado ")
        else:
            print("id no encontrado")
    else:
        print("El comando rep requiere de los parametros name, path, id")

def reporte_bm_inode(path, PathDSK, IdExist):
    seekInicio = IdExist.SeekDSKInicio
    seekFin = IdExist.SeekDSKFin

    byte_recivido = OptenerByte_archivo(PathDSK, seekInicio, (seekFin - seekInicio))

    temp = SuperBlock(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

    Objeto_Reciv = temp.set_bytes(byte_recivido)

    if IdExist.tipo != "E":
        if Objeto_Reciv.filesystem_type != 0:

            seekInodeInit = Objeto_Reciv.bm_inode_start
            seekInodeFin = Objeto_Reciv.inode_start + Objeto_Reciv.inodes_count 

            byte_recivido = OptenerByte_archivo(PathDSK, seekInodeInit, Objeto_Reciv.inodes_count)

            ListInodos = []

            cont = 0
            for count in range(Objeto_Reciv.inodes_count):
                ListInodos.append(int.from_bytes(byte_recivido[cont:(1+cont)], byteorder='big'))
                cont += 1

            contenido = ""
            cont= 1
            for bm_inode in ListInodos:
                contenido += f"{bm_inode}   "
                
                if cont == 20:
                    contenido += "\n"
                    cont=1
                else:
                    cont += 1

                


            crear_archivotxt(path, contenido)


            print("Reporte de bm_inodes generado con exito")

        else:
            print("No existe un formateo  EXT2/EXT3 en esta particion")
    else:
        print("No se puede realizar el reporte SUPERBLOQUE es una particion Extendida")


def reporte_bm_bloc(path, PathDSK, IdExist):
    seekInicio = IdExist.SeekDSKInicio
    seekFin = IdExist.SeekDSKFin

    byte_recivido = OptenerByte_archivo(PathDSK, seekInicio, (seekFin - seekInicio))

    temp = SuperBlock(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

    Objeto_Reciv = temp.set_bytes(byte_recivido)

    if IdExist.tipo != "E":
        if Objeto_Reciv.filesystem_type != 0:

            seekInodeInit = Objeto_Reciv.bm_block_start
            seekInodeFin = Objeto_Reciv.inode_start + Objeto_Reciv.inodes_count 

            byte_recivido = OptenerByte_archivo(PathDSK, seekInodeInit, Objeto_Reciv.blocks_count)

            ListInodos = []

            cont = 0
            for count in range(Objeto_Reciv.blocks_count):
                ListInodos.append(int.from_bytes(byte_recivido[cont:(1+cont)], byteorder='big'))
                cont += 1

            contenido = ""
            cont= 1
            for bm_inode in ListInodos:
                contenido += f"{bm_inode}   "
                
                if cont == 20:
                    contenido += "\n"
                    cont=1
                else:
                    cont += 1

            crear_archivotxt(path, contenido)


            print("Reporte de bm_bloc generado con exito")

        else:
            print("No existe un formateo  EXT2/EXT3 en esta particion")
    else:
        print("No se puede realizar el reporte SUPERBLOQUE es una particion Extendida")

def crear_archivotxt(path, contenido):
    ruta_archivo, archivo = os.path.split(path)
    ruta_archivo = ruta_archivo.replace(" ", "_")
    # print(ruta_archivo)
    # Comando para crear el archivo en la ruta especificada (con sudo)
    comando_creacion_directorio = f"sudo mkdir -p  {ruta_archivo}"

    # Comando para crear un archivo de texto dentro del directorio
    comando_creacion_archivo = f"sudo touch {path}"

    # Comando para cambiar los permisos del archivo (opcional, si es necesario)
    comando_chmod = f"sudo chmod 777 {path}"

    # Ejecutar el comando para crear el archivo utilizando os.system
    os.system(comando_creacion_directorio)
    os.system(comando_creacion_archivo)

    # Ejecutar el comando para cambiar los permisos (opcional)
    os.system(comando_chmod)

    # Verificar si el archivo se creó correctamente
    if os.path.exists(path):
        with open(path, "w") as file:

            file.seek(0)
            file.write(contenido)

        print(f"Se ha creado el archivo en: {path}")
    else:
        print(f"No se pudo crear el archivo en: {path}")



def reporte_sb(path, PathDSK, IdExist):

    seekInicio = IdExist.SeekDSKInicio
    seekFin = IdExist.SeekDSKFin

    byte_recivido = OptenerByte_archivo(PathDSK, seekInicio, (seekFin - seekInicio))

    temp = SuperBlock(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

    Objeto_Reciv = temp.set_bytes(byte_recivido)

    if IdExist.tipo != "E":
        if Objeto_Reciv.filesystem_type != 0:

            ContenidoPNG = ("""node [shape=plaintext];
                // Crea un nodo con una tabla HTML de 2 columnas
                    subgraph cluster_level1 {"""
                    + f"""
                label = "Super Bloque";
                mi_nodo [label=<
                    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
                        <TR>
                        <TD colspan="2"> Reporte de SUPERBLOQUE</TD>
                    </TR>
                    <TR>
                        <TD>sb_nombre_hd</TD>
                        <TD>{IdExist.nameDSK}</TD>
                    </TR>
                    <TR>
                        <TD>sb_sistema_archivo</TD>
                        <TD>{Objeto_Reciv.filesystem_type}</TD>
                    </TR>
                    <TR>
                        <TD>sb_inodes_count </TD>
                        <TD>{Objeto_Reciv.inodes_count}</TD>
                    </TR>
                    <TR>
                        <TD>sb_blocks_count  </TD>
                        <TD>{Objeto_Reciv.blocks_count}</TD>
                    </TR>
                    <TR>
                        <TD>sb_ifree_blocks_count </TD>
                        <TD>{Objeto_Reciv.free_blocks_count}</TD>
                    </TR>
                    <TR>
                        <TD>sb_free_inodes_count  </TD>
                        <TD>{Objeto_Reciv.free_inodes_count }</TD>
                    </TR>
                    <TR>
                        <TD>sb_mtime </TD>
                        <TD>{Objeto_Reciv.mtime}</TD>
                    </TR>
                    <TR>
                        <TD>sb_umtime </TD>
                        <TD>{Objeto_Reciv.umtime }</TD>
                    </TR>
                    <TR>
                        <TD>sb_mnt_count  </TD>
                        <TD>{Objeto_Reciv.mnt_count }</TD>
                    </TR>
                    <TR>
                        <TD>sb_magic</TD>
                        <TD>{Objeto_Reciv.magic}</TD>
                    </TR>
                    <TR>
                        <TD>sb_inode_s </TD>
                        <TD>{Objeto_Reciv.inode_s}</TD>
                    </TR>
                    <TR>
                        <TD>sb_block_s  </TD>
                        <TD>{Objeto_Reciv.block_s }</TD>
                    </TR>
                    <TR>
                        <TD>sb_firts_ino </TD>
                        <TD>{Objeto_Reciv.firts_ino}</TD>
                    </TR>
                    <TR>
                        <TD>sb_first_blo</TD>
                        <TD>{Objeto_Reciv.first_blo}</TD>
                    </TR>
                    <TR>
                        <TD>sb_bm_inode_start  </TD>
                        <TD>{Objeto_Reciv.bm_inode_start }</TD>
                    </TR>
                    <TR>
                        <TD>sb_bm_block_start  </TD>
                        <TD>{Objeto_Reciv.bm_block_start }</TD>
                    </TR>
                    <TR>
                        <TD>sb_inode_start </TD>
                        <TD>{Objeto_Reciv.inode_start}</TD>
                    </TR>
                    <TR>
                        <TD>sb_block_start </TD>
                        <TD>{Objeto_Reciv.block_start}</TD>
                    </TR>"""
                    )
             

            ContenidoPNG += (
                    """    </TABLE>
                    >]; }"""
                )
            

            Generar_png(path, ContenidoPNG)

        else:
            print("No existe un formateo  EXT2/EXT3 en esta particion")
    else:
        print("No se puede realizar el reporte SUPERBLOQUE es una particion Extendida")



def reporte_disk(path, PathDSK, IdExist):
    temp = MBR(0, 0, 0, "")

    byte_recivido = OptenerByte_archivo(PathDSK, 0, 121)

    objetoMBR = temp.set_bytes(byte_recivido)

    SeekInicio = 0

    TamanoDSK = objetoMBR.size

    porcent = (121 * 100) / TamanoDSK

    ContenidoPNG = (
        """  rankdir = LR;
    subgraph cluster_level2 {
        label ="""
        + f''' "{IdExist.nameDSK}";
    mux [shape=record,label="'''
        + "{"
        + f"""MBR\\n{round(porcent, 3)}% """
    )

    for i in range(len(objetoMBR.particions) - 1):
        particion = objetoMBR.particions[i]
        particion_sig = objetoMBR.particions[i + 1]
        sizePart = objetoMBR.particions[i].size

        SeekInicio = particion.start

        SeekInicio_sig = particion_sig.start
        SeekFin_sig = SeekInicio + particion_sig.size

        res = SeekInicio_sig - SeekInicio

        if particion.type == "P":
            if particion_sig.status == "1" or particion_sig.status == "E":
                if res == sizePart:
                    if particion.status != "E":
                        porcent = (sizePart * 100) / TamanoDSK
                        ContenidoPNG += f"|Primaria\\n{round(porcent, 3)}%"
                    else:
                        porcent = (sizePart * 100) / TamanoDSK
                        ContenidoPNG += f"|Libre\\n{round(porcent, 3)}%"

                else:
                    if particion.status != "E":
                        porcent = (sizePart * 100) / TamanoDSK
                        ContenidoPNG += f"|Primaria\\n{round(porcent, 3)}%"

                        porcent = ((res - sizePart) * 100) / TamanoDSK
                        ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
                    else:
                        porcent = (res * 100) / TamanoDSK
                        ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
            else:
                porcent = (sizePart * 100) / TamanoDSK
                ContenidoPNG += f"|Primaria\\n{round(porcent, 3)}%"

                porcent = ((TamanoDSK - sizePart - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"

        elif particion.type == "E":
            ContenidoPNG += "|{Extendida|{"

            if (particion_sig.status == "1" or particion_sig.status == "E"):  # verifica si existe otra particion despues de la extendida
                if (res == sizePart):  # como existe otra particion verifica si el tamano es completo o proporcinal
                    # ContenidoPNG += '|{Extendida|{'

                    ContenidoPNG += ExtendidaPNG(SeekInicio, PathDSK, TamanoDSK, sizePart)

                else:
                    ContenidoPNG += ExtendidaPNG(SeekInicio, PathDSK, TamanoDSK, sizePart)

                    porcent = (res - sizePart * 100) / TamanoDSK
                    ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
            else:
                # ContenidoPNG += '|{Extendida|{'

                ContenidoPNG += ExtendidaPNG(SeekInicio, PathDSK, TamanoDSK, sizePart)

                # Este codigo va al final por si no existe otra particion al final de particion extendida
                porcent = ((TamanoDSK - sizePart - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"

    if objetoMBR.particions[-1].status == "1" or objetoMBR.particions[-1].status == "E":
        particion = objetoMBR.particions[-1]
        sizePart = objetoMBR.particions[-1].size

        SeekInicio = particion.start

        SeekInicio_sig = SeekInicio + sizePart

        res = SeekInicio_sig - SeekInicio

        if particion.type == "P":

            if particion.status != "E":
                porcent = (sizePart * 100) / TamanoDSK
                ContenidoPNG += f"|Primaria\\n{round(porcent, 3)}%"

                porcent = ((TamanoDSK - sizePart - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
            else:
                porcent = ((TamanoDSK - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"


        elif particion.type == "E":
            ContenidoPNG += "|{Extendida|{"


            if particion.status != "E":
                ContenidoPNG += ExtendidaPNG(SeekInicio, PathDSK, TamanoDSK, sizePart)

                # Este codigo va al final por si no existe otra particion al final de particion extendida
                porcent = ((TamanoDSK - sizePart - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
            else:
                porcent = ((TamanoDSK - SeekInicio) * 100) / TamanoDSK
                ContenidoPNG += f"|libre\\n{round(porcent, 3)}%"
                

    ContenidoPNG += """}"];}"""

    Generar_png(path, ContenidoPNG)


def ExtendidaPNG(SeekInicio, PathDSK, TamanoDSK, sizePart):
    ContenidoPNG = """ """
    existeEBR = True
    SeekEBRNext = SeekInicio
    EspLibreExt = 0

    while existeEBR:
        byte_recivido = OptenerByte_archivo(PathDSK, SeekEBRNext, SeekEBRNext + 30)
        tmpEBR = EBR("", "", 0, 0, 0, "")
        objetoEBR = tmpEBR.set_bytes(byte_recivido)

        if objetoEBR.status == "1" or objetoEBR.status == "E":
            EspLibreExt += objetoEBR.size

            if objetoEBR.next != -1:
                restEBR = objetoEBR.next - objetoEBR.start

                if restEBR == objetoEBR.size:
                    if objetoEBR.status != "E":
                        porcent = ((objetoEBR.size) * 100) / TamanoDSK
                        ContenidoPNG += f"EBR|logica\\n{round(porcent, 3)}%|"
                    else:
                        porcent = ((objetoEBR.size) * 100) / TamanoDSK
                        ContenidoPNG += f"Libre\n{round(porcent, 3)}%|"

                else:
                    if objetoEBR.status != "E":
                        porcent = ((objetoEBR.size) * 100) / TamanoDSK
                        ContenidoPNG += f"EBR|logica\\n{round(porcent, 3)}%|"
                        porcent = ((restEBR - objetoEBR.size) * 100) / TamanoDSK
                        ContenidoPNG += f"Libre\\n{round(porcent, 3)}%|"
                    else:
                        porcent = ((objetoEBR.size) * 100) / TamanoDSK
                        ContenidoPNG += f"Libre\\n{round(porcent, 3)}%|"

                SeekEBRNext = objetoEBR.next

            else:
                if objetoEBR.status != "E":
                    porcent = ((objetoEBR.size) * 100) / TamanoDSK
                    ContenidoPNG += f"EBR|logica\\n{round(porcent, 3)}%|"
                    porcent = ((sizePart - EspLibreExt) * 100) / TamanoDSK
                    ContenidoPNG += f"Libre\\n{round(porcent, 3)}%" + "}}"
                else:
                    porcent = ((sizePart) * 100) / TamanoDSK
                    ContenidoPNG += f"Libre\\n{round(porcent, 3)}%" + "}}"
                
                existeEBR = False

        else:
            porcent = ((sizePart) * 100) / TamanoDSK
            ContenidoPNG += f"libre\\n{round(porcent, 3)}%" + "}}"
            existeEBR = False

    return ContenidoPNG


def buscar_id(id):
    for i, Mount in enumerate(ListMount):
        if Mount.id == id:
            return Mount
    else:
        return None


def comando_unmount(ListComand):
    if "id" in ListComand:
        id = ListComand[ListComand.index("id") + 1]

        status = 2

        for i, Mount in enumerate(ListMount):
            if Mount.id == id:
                status = Mount.status
                Mount.status = 0
                break

        if status == 1:
            print(f"se ha desmontado correctamente el id")
        else:
            print(f"no existe el id")

    else:
        print("comando requiere del parametro id")


def Generar_png(path, content):
    ruta_deseada = path

    dot_code = "digraph G {" + content + "}"

    # Crear el directorio si no existe
    # directorio_destino = os.path.dirname(ruta_deseada)
    # if not os.path.exists(directorio_destino):
    #     os.makedirs(directorio_destino)

    ruta_archivo, archivo = os.path.split(ruta_deseada)
    ruta_archivo = ruta_archivo.replace(" ", "_")
    # print(ruta_archivo)
    # Comando para crear el archivo en la ruta especificada (con sudo)
    comando_creacion_directorio = f"sudo mkdir -p  {ruta_archivo}/"

    os.system(comando_creacion_directorio)

    # Generar el gráfico en formato DOT

    # Usar sudo para escribir el archivo DOT y luego renderizarlo
    with open("/tmp/graph.dot", "w") as dot_file:
        dot_file.write(dot_code)

    comando_chmod = f"sudo chmod 777 {ruta_archivo}"

    os.system(comando_chmod)

    archivo = archivo.split(".")

    ruta_deseada = ruta_archivo + "/" + archivo[0] + ".png"

    # Usar sudo para renderizar el archivo DOT como imagen PNG en la ubicación deseada
    comando_renderizado = f"sudo dot -Tpng /tmp/graph.dot -o {ruta_deseada}"
    subprocess.run(comando_renderizado, shell=True)
    print(f"Se genero con exito la imagen en la ruta: {ruta_deseada}")


def ReporteMBR(path, PathDSK):
    temp = MBR(0, 0, 0, "")

    byte_recivido = OptenerByte_archivo(PathDSK, 0, 121)

    objetoMBR = temp.set_bytes(byte_recivido)

    SeekInicio = 0
    SeekFin = 0
    SeekUbicacionDisco = 13

    fecha = datetime.datetime.fromtimestamp(objetoMBR.date)

    ContenidoPNG = (
        """node [shape=plaintext];
    // Crea un nodo con una tabla HTML de 2 columnas
        subgraph cluster_level1 {"""
        + f"""
    label = "MBR";
    mi_nodo [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
            <TR>
            <TD colspan="2"> REPORTE DE MBR</TD>
        </TR>
        <TR>
            <TD>mbr_tamaño</TD>
            <TD>{str(objetoMBR.size)}</TD>
        </TR>
        <TR>
            <TD>mbr_fecha_creacion</TD>
            <TD>{fecha}</TD>
        </TR>
        <TR>
            <TD>mbr_disk_signature</TD>
            <TD>{str(objetoMBR.signature)}</TD>
        </TR>"""
    )
    

    contenidoPNGEBR = ""

    for particion in objetoMBR.particions:
        SeekInicio = particion.start
        SeekFin = SeekInicio + particion.size
        if particion.type == "P":
            ContenidoPNG += f"""  
                <TR>
                    <TD colspan="2"> Particion</TD>
                </TR>
                <TR>
                    <TD>mbr_status</TD>
                    <TD>{particion.status}</TD>
                </TR>
                <TR>
                    <TD>mbr_type</TD>
                    <TD>{particion.type}</TD>
                </TR>
                <TR>
                    <TD>mbr_fit</TD>
                    <TD>{particion.fit}</TD>
                </TR>
                <TR>
                    <TD>mbr_start</TD>
                    <TD>{str(particion.start)}</TD>
                </TR>
                <TR>
                    <TD>mbr_size</TD>
                    <TD>{str(particion.size)}</TD>
                </TR>
                <TR>
                    <TD>mbr_name</TD>
                    <TD>{particion.name}</TD>
                </TR>"""

        else:
            # pass
            if particion.type == "E":
                contenidoPNGEBR = """
                    // Crea un nodo con una tabla HTML de 2 columnas
                    subgraph cluster_level2 {
                    label = "EBR";
                    mi_nodo2 [label=<
                    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">"""

                ContenidoPNG += f"""  
                <TR>
                    <TD colspan="2"> Particion</TD>
                </TR>
                <TR>
                    <TD>mbr_status</TD>
                    <TD>{particion.status}</TD>
                </TR>
                <TR>
                    <TD>mbr_type</TD>
                    <TD>{particion.type}</TD>
                </TR>
                <TR>
                    <TD>mbr_fit</TD>
                    <TD>{particion.fit}</TD>
                </TR>
                <TR>
                    <TD>mbr_start</TD>
                    <TD>{str(particion.start)}</TD>
                </TR>
                <TR>
                    <TD>mbr_size</TD>
                    <TD>{str(particion.size)}</TD>
                </TR>
                <TR>
                    <TD>mbr_name</TD>
                    <TD>{particion.name}</TD>
                </TR>"""

                existeEBR = True
                SeekEBRNext = SeekInicio

                while existeEBR:
                    byte_recivido = OptenerByte_archivo(
                        PathDSK, SeekEBRNext, SeekEBRNext + 30
                    )
                    tmpEBR = EBR("", "", 0, 0, 0, "")
                    objetoEBR = tmpEBR.set_bytes(byte_recivido)

                    if objetoEBR.status != "":
                        ContenidoPNG += """  
                            <TR>
                                <TD colspan="2"> Particion Logica</TD>
                            </TR> """

                        contenidoPNGEBR += """  
                            <TR>
                                <TD colspan="2"> Particion</TD>
                            </TR> """

                        contenidotabla = f"""
                            <TR>
                                <TD>mbr_status</TD>
                                <TD>{objetoEBR.status}</TD>
                            </TR>
                            <TR>
                                <TD>mbr_next</TD>
                                <TD>{str(objetoEBR.next)}</TD>
                            </TR>
                            <TR>
                                <TD>mbr_fit</TD>
                                <TD>{objetoEBR.fit}</TD>
                            </TR>
                            <TR>
                                <TD>mbr_start</TD>
                                <TD>{str(objetoEBR.start)}</TD>
                            </TR>
                            <TR>
                                <TD>mbr_size</TD>
                                <TD>{str(objetoEBR.size)}</TD>
                            </TR>
                            <TR>
                                <TD>mbr_name</TD>
                                <TD>{objetoEBR.name}</TD>
                            </TR>"""

                        ContenidoPNG += contenidotabla
                        contenidoPNGEBR += contenidotabla

                        if objetoEBR.next != -1:
                            SeekEBRNext = objetoEBR.next

                        else:
                            existeEBR = False
                    else:
                        contenidoPNGEBR += """  
                            <TR>
                                <TD></TD>
                            </TR> """

                        existeEBR = False

                contenidoPNGEBR += """    </TABLE>
                >]; }"""

        SeekUbicacionDisco += particion.get_size()

    ContenidoPNG += (
        """    </TABLE>
        >]; }"""
        + contenidoPNGEBR
    )

    Generar_png(path, ContenidoPNG)


def comando_mount(ListComand):
    if "name" in ListComand and "path" in ListComand:
        path = ListComand[ListComand.index("path") + 1]
        name = ListComand[ListComand.index("name") + 1]

        Particion = ObtenerParticion(path, name)

        if Particion != None:
            path2 = path.split("/")
            NameArc = path2[-1]
            NameDSK = NameArc.split(".")

            cont = 1

            exist = False

            status = 0

            for Mount in ListMount:
                if Mount.nameDSK == NameArc and Mount.namePart != name:
                    cont += 1
                else:
                    if Mount.status != 1:
                        status = Mount.status = 1
                        Mount.path = path

                        if Particion[0] == "MBR":
                            tipo = Particion[1].type

                        else:
                            tipo = "L"

                        Mount.tipo = tipo
                        Mount.SeekDSKInicio = Particion[3]
                        Mount.SeekDSKFin = Particion[4]
                    exist = True
                    break

            id = "62" + str(cont) + NameDSK[0]

            if not exist:
                if Particion[0] == "MBR":
                    tipo = Particion[1].type

                else:
                    tipo = "L"

                objMount = mount(
                    1, id, path, tipo, NameArc, name, Particion[3], Particion[4]
                )
                ListMount.append(objMount)

                print(
                    f"Se ha realizado con exito la montacion de la {name} su id es: {id}"
                )
            else:
                if status == 1:
                    print(
                        f"Se ha realizado con exito la montacion de la {name} su id es: {id}"
                    )
                else:
                    print(
                        f"Ya existe la montacion de la particion {name} su id es: {id} "
                    )

            print("\nMontaciones actuales:", end= " ")

            for Mount in ListMount:
                if Mount.status != 0:
                    print(Mount.id, end="  ")

        else:
            print("Montacion no realizada particion no existe")

    else:
        print("comando requiere de los path y name")


def comando_fdisk(ListComand):
    size = 0
    unit = ""
    type = ""
    fit = ""

    if "size" in ListComand:
        size = ListComand[ListComand.index("size") + 1]
        try:
            size = int(size)
        except ValueError:
            print("el parametro size debe ser entero")
            return

    if "unit" in ListComand:
        unit = ListComand[ListComand.index("unit") + 1]
        if unit == "M":
            size = size * 1024 * 1024
        elif unit == "K":
            size = size * 1024
        elif unit != "B":
            print("el parametro unit requiere de K/M/B")
            return
    else:
        unit = "K"
        size = size * 1024

    if "fit" in ListComand:
        fit = ListComand[ListComand.index("fit") + 1]
        if fit == "BF":
            fit = "B"
        elif fit == "FF":
            fit = "F"
        elif fit == "WF":
            fit = "W"
        else:
            print("el parametro fit requiere de BF/FF/WF")
            return
    else:
        fit = "W"

    if "type" in ListComand:
        type = ListComand[ListComand.index("type") + 1]
        if type != "P" and type != "E" and type != "L":
            print("el parametro type requiere de P/E/L")
            return
    else:
        type = "P"

    if "delete" in ListComand:
        delete = ListComand[ListComand.index("delete") + 1]
        if delete != "full":
            print("el parametro delete requiere del valor full")
            return

    if "name" in ListComand and "path" in ListComand:
        path = ListComand[ListComand.index("path") + 1]
        name = ListComand[ListComand.index("name") + 1]

        if "size" in ListComand:
            if "add" == ListComand[0]:
                pass
            elif "delete" == ListComand[0]:
                eliminar_parcion(path, name)
            else:
                if size > 0:
                    crear_Particion(path, "1", type, fit, size, name)
                else:
                    print("el parametro size debe ser mayor a 0")
        elif "delete" in ListComand:
            eliminar_parcion(path, name)
        elif "add" in ListComand:
            pass
        else:
            print(
                """Faltan parametros
                      -size     para crear una particion
                      -add      para agregar/elimnar espacio en una particion
                      -delete   para eliminar una particion
                      """
            )
    else:
        print("comando requiere de los path y name")


def leer_MBR(path):
    datos = None
    if os.path.exists(path):
        with open(path, "rb") as file:
            file.seek(0)
            Read_bytes = file.read(121)
            temp = MBR(0, 0, 0, "")
            datos = temp.set_bytes(Read_bytes)
            # datos = datos.particions
    else:
        print("No existe el disco duro")

    return datos


def OptenerByte_archivo(path, SeekInicio, SeekFin):
    Read_bytes = None
    if os.path.exists(path):
        with open(path, "rb") as file:
            file.seek(SeekInicio)
            Read_bytes = file.read(SeekFin)
            # datos = datos.particions
    else:
        print("No existe el disco duro")

    return Read_bytes


def eliminar_parcion(path, name):
    temp = MBR(0, 0, 0, "")

    byte_recivido = OptenerByte_archivo(path, 0, 121)

    if byte_recivido != None:

        objetoMBR = temp.set_bytes(byte_recivido)

        SeekInicio = 0
        SeekFin = 0

        for particion in objetoMBR.particions:
            SeekInicio = particion.start
            SeekFin = SeekInicio + particion.size
            if (
                (particion.type == "E" or particion.type == "P")
                and particion.name == name
                and particion.status == "1"
            ):
                particion.status = "E"
                byte_objeto = objetoMBR.get_bytes()
                Guardar_enArchivo(path, byte_objeto, 0, objetoMBR.get_size())

                byte = bytearray().ljust(particion.size, b"\x00")
                Guardar_enArchivo(path, byte, SeekInicio, SeekFin)
                print("Particion eliminado con exito")
                return
            else:
                if particion.type == "E" and particion.status == "1":
                    existeEBR = True
                    SeekEBRNext = SeekInicio

                    while existeEBR:
                        byte_recivido = OptenerByte_archivo(
                            path, SeekEBRNext, SeekEBRNext + 30
                        )
                        tmpEBR = EBR("", "", 0, 0, 0, "")
                        objetoEBR = tmpEBR.set_bytes(byte_recivido)

                        if objetoEBR.status == "1":
                            if objetoEBR.name == name:
                                objetoEBR.status = "E"

                                byte_objeto = objetoEBR.get_bytes()

                                byte = bytearray().ljust(objetoEBR.size - 30, b"\x00")

                                byte_objeto += byte

                                Guardar_enArchivo(
                                    path,
                                    byte_objeto,
                                    SeekEBRNext,
                                    SeekEBRNext + objetoEBR.size,
                                )
                                print("Particion eliminado con exito")
                                return

                            else:
                                if objetoEBR.next != -1:
                                    SeekEBRNext = objetoEBR.next
                                else:
                                    existeEBR = False
                        else:
                            if objetoEBR.next != -1:
                                SeekEBRNext = objetoEBR.next

                            else:
                                existeEBR = False

        print("No existe la particion: " + name)


def ObtenerParticion(path, name):
    temp = MBR(0, 0, 0, "")

    byte_recivido = OptenerByte_archivo(path, 0, 121)

    if byte_recivido != None:

        objetoMBR = temp.set_bytes(byte_recivido)

        SeekInicio = 0
        SeekFin = 0
        SeekUbicacionDisco = 13

        for particion in objetoMBR.particions:
            SeekInicio = particion.start
            SeekFin = SeekInicio + particion.size
            if (
                (particion.type == "E" or particion.type == "P")
                and particion.name == name
                and particion.status == "1"
            ):
                return "MBR", particion, SeekUbicacionDisco, SeekInicio, SeekFin
            else:
                if particion.type == "E" and particion.status == "1":
                    existeEBR = True
                    SeekEBRNext = SeekInicio

                    while existeEBR:
                        byte_recivido = OptenerByte_archivo(
                            path, SeekEBRNext, SeekEBRNext + 30
                        )
                        tmpEBR = EBR("", "", 0, 0, 0, "")
                        objetoEBR = tmpEBR.set_bytes(byte_recivido)

                        if objetoEBR.status == "1":
                            if objetoEBR.name == name:
                                return (
                                    "EBR",
                                    objetoEBR,
                                    SeekEBRNext,
                                    SeekEBRNext + 30,
                                    SeekEBRNext + objetoEBR.size,
                                )

                            else:
                                if objetoEBR.next != -1:
                                    SeekEBRNext = objetoEBR.next
                                else:
                                    existeEBR = False
                        else:
                            if objetoEBR.status != "":
                                if objetoEBR.next != -1:
                                    SeekEBRNext = objetoEBR.next

                                else:
                                    existeEBR = False
                            else:
                                existeEBR = False

            SeekUbicacionDisco += particion.get_size()

    return None


def Guardar_enArchivo(path, bytes, seekInicio, seekFIn):
    if os.path.exists(path):
        with open(path, "rb") as archivo:
            contenido = archivo.read()

        contenido = contenido[:seekInicio] + bytes + contenido[seekFIn:]

        with open(path, "wb") as file:
            file.seek(0)
            file.write(contenido)
    else:
        print("No existe el disco duro")


def crear_Particion(path, status, type, fit, size, name):
    DatosMBR = leer_MBR(path)

    bytes = DatosMBR.get_bytes()

    start = DatosMBR.get_size()

    # print(bytes)

    ExisteE = False
    Partvacio = True

    if DatosMBR != None:
        # Verifica si existe espacio libre para crear particiones
        for particion in DatosMBR.particions:
            if particion.status == " " or particion.status == "E":
                Partvacio = False
                break

        if not Partvacio or type == "L":
            # Verifica si existe la particion extendida
            for particion in DatosMBR.particions:
                if particion.status == "1" and particion.type == "E":
                    ExisteE = True
                    break

            for particion in DatosMBR.particions:
                if particion.status != "E" and particion.name == name:
                    print("El nombre de la particion ya existe")
                    return

            for particion in DatosMBR.particions:
                if status == "1":
                    if type == "E":
                        if not ExisteE:
                            if particion.status == " " or particion.status == "E":
                                particion.status = status
                                particion.type = type
                                particion.fit = fit
                                if particion.status != "E":
                                    particion.start = start
                                particion.size = size
                                particion.name = name
                                #  GUARDA LOS DATOS MODIFICADOS
                                bytes = DatosMBR.get_bytes()
                                Guardar_enArchivo(path, bytes, 0, DatosMBR.get_size())
                                print("Particion extendida creada con exito!")
                                break
                            else:
                                start += particion.size
                        else:
                            print("ya existe una particion extendida")
                            break
                    elif type == "L":
                        if ExisteE:
                            if particion.type == "E":
                                seekInicio = particion.start
                                seekFin = seekInicio + particion.size

                                bytes_Ext = OptenerByte_archivo(
                                    path, seekInicio, seekFin
                                )

                                primerEBR = EBR("", "", 0, 0, 0, "")
                                tmp = primerEBR.set_bytes(bytes_Ext[:30])

                                if tmp.status == "":
                                    InicioEBR = EBR(
                                        "1", fit, seekInicio, size, -1, name
                                    )
                                    bytesEBR = InicioEBR.get_bytes()

                                    nuevo_byte = bytearray(bytesEBR + bytes_Ext[30:])
                                    Guardar_enArchivo(
                                        path, nuevo_byte, seekInicio, seekFin
                                    )
                                else:
                                    ExisteEBR = True

                                    sumaBytes = 0
                                    temp2 = tmp
                                    while ExisteEBR:
                                        if tmp.name != name:
                                            if tmp.status == "1":
                                                if tmp.next != -1:
                                                    sumaBytes = tmp.next - seekInicio
                                                    temp2 = tmp
                                                    tmp = primerEBR.set_bytes(
                                                        bytes_Ext[
                                                            sumaBytes : sumaBytes + 30
                                                        ]
                                                    )
                                                else:
                                                    tmp.next = tmp.start + tmp.size
                                                    bytestmp2 = tmp.get_bytes()
                                                    # bytes_Ext[0:sumaBytes] se optienen los bytes anteriores
                                                    # bytestmp2 como next ya fue modificado se convirtio en bytes para agregarlo la modificacion a la particion extendida
                                                    # bytes_Ext[sumaBytes + 30:] y se agrega el resto de codigo que sigue despues del EBR
                                                    nuevo_byte = bytearray(
                                                        bytes_Ext[0:sumaBytes]
                                                        + bytestmp2
                                                        + bytes_Ext[sumaBytes + 30 :]
                                                    )
                                                    bytes_Ext = nuevo_byte
                                                    # Guardar_enArchivo(path, nuevo_byte, seekInicio, seekFin)

                                            elif tmp.status == "":
                                                nuevoEBR = EBR(
                                                    "1",
                                                    fit,
                                                    seekInicio + sumaBytes,
                                                    size,
                                                    -1,
                                                    name,
                                                )
                                                bytestmp2 = nuevoEBR.get_bytes()

                                                nuevo_byte = bytearray(
                                                    bytes_Ext[0:sumaBytes]
                                                    + bytestmp2
                                                    + bytes_Ext[sumaBytes + 30 :]
                                                )
                                                Guardar_enArchivo(
                                                    path,
                                                    nuevo_byte,
                                                    seekInicio,
                                                    seekFin,
                                                )
                                                ExisteEBR = False
                                            elif tmp.status == "E":
                                                pass

                                        else:
                                            print("El nombre de la particion ya existe")
                                            ExisteEBR = False
                                            return

                                print("Particion logica creada con exito!")
                                break
                        else:
                            print("Se requiere que de una particion extendida")
                            break
                    else:
                        if particion.status == " " or particion.status == "E":
                            particion.status = status
                            particion.type = type
                            particion.fit = fit
                            if particion.status != "E":
                                particion.start = start
                            particion.size = size
                            particion.name = name
                            # GUARDA LOS BYTES MODIFICADOS
                            bytes = DatosMBR.get_bytes()
                            Guardar_enArchivo(path, bytes, 0, DatosMBR.get_size())
                            print("Particion primaria creada con exito!")
                            break
                        else:
                            start += particion.size
        else:
            print("Se tiene ya ocupada las 4 particiones del disco")


def comando_mkdisk(ListComand):
    if "size" in ListComand and "path" in ListComand:
        size = ListComand[ListComand.index("size") + 1]
        path = ListComand[ListComand.index("path") + 1]

        try:
            size = int(size)
            if size > 0:
                if "unit" in ListComand:
                    unit = ListComand[ListComand.index("unit") + 1]
                else:
                    unit = "M"

                if unit == "K" or unit == "M":
                    fit = ""
                    if "fit" in ListComand:
                        fit = ListComand[ListComand.index("size") + 1]

                        if fit == "BF":
                            fit = "B"
                        elif fit == "FF":
                            fit = "F"
                        elif fit == "WF":
                            fit == "W"
                        else:
                            print("el parametro fit requiere de BF/FF/WF")

                    else:
                        fit = "W"

                    crear_archivo(size, path, unit, fit)
                else:
                    print("el parametro unit requiere de K/M")
            else:
                print("el parametro size debe ser mayor a 0")
        except ValueError:
            print("el parametro size debe ser entero")

    else:
        print("comando requiere de los path y size")


def crear_archivo(size, path, unit, fit):
    ruta_archivo, archivo = os.path.split(path)
    ruta_archivo = ruta_archivo.replace(" ", "_")
    # print(ruta_archivo)
    # Comando para crear el archivo en la ruta especificada (con sudo)
    comando_creacion_directorio = f"sudo mkdir -p  {ruta_archivo}"

    # Comando para crear un archivo de texto dentro del directorio
    comando_creacion_archivo = f"sudo touch {path}"

    # Comando para cambiar los permisos del archivo (opcional, si es necesario)
    comando_chmod = f"sudo chmod 777 {path}"

    # Ejecutar el comando para crear el archivo utilizando os.system
    os.system(comando_creacion_directorio)
    os.system(comando_creacion_archivo)

    # Ejecutar el comando para cambiar los permisos (opcional)
    os.system(comando_chmod)

    # Verificar si el archivo se creó correctamente
    if os.path.exists(path):
        with open(path, "wb") as file:
            if unit == "K":
                size_byte = 1024
            else:
                size_byte = 1024 * 1024

            for i in range(0, size):
                file.write(b"\x00" * size_byte)

            timestamp = datetime.datetime.now().timestamp()
            timestamp = int(timestamp)

            numRandom = random.randint(1, 100)

            tempMBR = MBR(size_byte * size, timestamp, numRandom, fit)
            tempMBR.particions.append(particion(" ", "", "", 0, 0, ""))
            tempMBR.particions.append(particion(" ", "", "", 0, 0, ""))
            tempMBR.particions.append(particion(" ", "", "", 0, 0, ""))
            tempMBR.particions.append(particion(" ", "", "", 0, 0, ""))

            bytes = tempMBR.get_bytes()
            # total = tempMBR.get_size()

            # print(total)
            # print(bytes)

            file.seek(0)
            file.write(bytes)

        print(f"Se ha creado el archivo en: {path}")
    else:
        print(f"No se pudo crear el archivo en: {path}")


def eliminar_archivo(path):
    # Comando para eliminar el archivo en la ruta especificada (con sudo)
    path = path.replace(" ", "_")
    comando_eliminar_directorio = f"sudo rm  {path}"

    # Verificar si el archivo se creó correctamente
    if os.path.exists(path):
        # Ejecutar el comando para eliminar el archivo utilizando os.system
       while True:
            entrada = input("Deseea eliminar el disco (y/n)")

            if entrada == "Y" or entrada == "y":
                os.system(comando_eliminar_directorio)
                print("Disco duro eliminado con exito")
                break
            elif entrada == "N" or entrada == "n":
                print("No se elimino el disco duro")
                break
            else:
                print("Entrada inválida. Presione (y/n).")
        
    else:
        print("No existe el disco duro")


menu()
