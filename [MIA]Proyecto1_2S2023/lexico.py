import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    # 'MKDISK',
    'PATH',
    'IGUAL',
    'RUTA',
    'UNIT',
    'SIZE',
    'CADENA',
    'ENTERO',  # Nuevo token para el valor numérico de SIZE
    'MENOS',
    'FIT',
    'COMILLA',
    'COMENTARIO' 
]

# Definición de tokens con expresiones regulares    
# t_MKDISK = r'mkdisk'
# t_UNIT = r'unit'
# t_PATH = r'path'
# t_FIT = r'fit'
t_IGUAL = r'='
t_MENOS = r'-'
t_RUTA = r'/[ \w]+(/[ \w]+)*\.\w+'

t_COMILLA = r'"'

# Regla para el token SIZE

# Nueva regla para el token SIZE_VALUE
def t_COMENTARIO(t):
    r'\#.*'
    # return t  # Los comentarios se ignoran
    pass

def t_CADENA(t):
    r'\w+'
    return t

def t_ENTERO(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t



t_ignore = ' \t\n'  # Ignorar espacios en blanco y tabulaciones

def t_error(t):
    print(f"Carácter inesperado: {t.value[0]}")
    t.lexer.skip(1)

# Crear el analizador léxico
lexer = lex.lex()

# # Cadena de entrada
# cadena = '''#CREACION DE DISCOS
# Mkdisk -s=50 -u=M -path=/home/archivos/Disco1.dsk -f=FF
# Mkdisk -u=k -s=51200 -path=/home/archivos/Disco2.dsk -f=BF
# mkDisk -s=10 -path=/home/archivos/Disco3.dsk
# mkdisk -s=51200 -path="/home/archivos/mis archivos/Disco4.dsk" -u=K
# mkDisk -s=20 -path="/home/archivos/mis archivos/Disco5.dsk" -u=M -f=WF

# #Deberia dar error
# mkdisk -param=x -s=30 -path=/home/archivos/Disco.dsk

# #ELIMINACION DE DISCOS
# #El primero deberia dar error
# rmDisk -path=/home/Disco3.dsk
# rmDisk -path=/home/archivos/Disco3.dsk
# RMDISK -path="/home/archivos/mis archivos/Disco4.dsk"

# #CREACION DE PARTICIONES
# #Particiones en el disco1
# fdisk -t=P -u=K -name=Part1 -s=7680 -path=/home/archivos/Disco1.dsk -f=BF #7.5 MB
# fdisk -t=E -u=K -name=Part2 -s=7680 -path=/home/archivos/Disco1.dsk -f=FF
# fdisk -t=E -u=K -name=Part3 -s=7680 -path=/home/archivos/Disco1.dsk -f=WF #Deberia dar error
# fdisk -t=P -u=K -name=Part3 -s=7680 -path=/home/archivos/Disco1.dsk -f=WF
# fdisk -t=P -u=K -name=Part4 -s=7680 -path=/home/archivos/Disco1.dsk -f=BF
# FDISK -t=L -u=k -name=Part5 -s=1280 -path=/home/archivos/Disco1.dsk -f=BF #1.25 MB
# fdisk -t=L -u=K -name=Part6 -s=1280 -path=/home/archivos/Disco1.dsk -f=WF
# fdisk -t=L -u=K -name=Part7 -s=1280 -path=/home/archivos/Disco1.dsk -f=wf
# fdisk -t=L -u=K -name=Part8 -s=1280 -path=/home/archivos/Disco1.dsk -f=ff
# fdisk -t=L -u=K -name=Part9 -s=1280 -path=/home/archivos/Disco1.dsk -f=bf
# fdisk -t=L -u=K -name=Part9 -s=1024 -path=/home/archivos/Disco1.dsk -f=BF #ERROR nombre "'''

# # Pasar la cadena de entrada al analizador léxico
# lexer.input(cadena)

# # Imprimir los tokens reconocidos
# for token in lexer:
#     print(token)