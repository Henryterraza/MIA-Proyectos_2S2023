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
    'COMILLA'
]

# Definición de tokens con expresiones regulares
# t_MKDISK = r'mkdisk'
# t_UNIT = r'unit'
# t_PATH = r'path'
# t_FIT = r'fit'
t_IGUAL = r'='
t_MENOS = r'-'
t_RUTA = r'/[ \w]+(/[ \w]+)*\.\w+'
t_ignore = ' \t'  # Ignorar espacios en blanco y tabulaciones
t_COMILLA = r'"'

# Regla para el token SIZE

# Nueva regla para el token SIZE_VALUE
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

def t_error(t):
    print(f"Carácter inesperado: {t.value[0]}")
    t.lexer.skip(1)

# Crear el analizador léxico
lexer = lex.lex()

# # Cadena de entrada
# cadena = 'mkdisk -size=10 -unit=K -path="/home/misdiscos/Disco5.dsk"'

# # Pasar la cadena de entrada al analizador léxico
# lexer.input(cadena)

# # Imprimir los tokens reconocidos
# for token in lexer:
#     print(token)