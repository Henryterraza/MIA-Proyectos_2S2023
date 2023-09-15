import ply.yacc as yacc
from lexico import tokens  # Asegúrate de que los tokens estén definidos en "lexico.py"

# Diccionario para mantener un seguimiento de los parámetros y sus valores
params = {
    'execute': False,
    'path': None,
    'fit': None,
    'unit': None,
    'size': None,
}

# Regla para el manejo de parámetros


def p_inicio(p):
    '''
    inicio : param
            | inicio param
    '''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_param(p):
    '''
    param : CADENA parametros 
    '''

    p[0] = p[1], p[2]

def p_parametros(p):
    '''parametros : parametros parametro
                | parametro
                | empty
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_parametro(p):
    '''parametro : MENOS CADENA IGUAL RUTA 
                | MENOS CADENA IGUAL COMILLA RUTA COMILLA
                | MENOS CADENA IGUAL COMILLA CADENA COMILLA
                | MENOS CADENA IGUAL CADENA
                | MENOS CADENA IGUAL ENTERO
    '''
# | MENOS CADENA IGUAL COMILLA RUTA COMILLA

    # print(len(p))

    if len(p) == 5:
        p[0] = p[2], p[4]
    else:
        p[0] = p[2], p[5]

    

def p_empty(p):
    'empty :'
    pass

# Regla para el manejo de errores de sintaxis
def p_error(p):
    print("Error de sintaxis")

# Crea el parser
parser = yacc.yacc()









# cadena = '''Mkdisk -s=50 -u=M -path=/home/archivos/Disco1.dsk -f=FF
# Mkdisk -u=k -s=51200 -path=/home/archivos/Disco2.dsk -f=BF'''
# # '''mkDisk -s=10 -path=/home/archivos/Disco3.dsk
# # mkdisk -s=51200 -path="/home/archivos/mis archivos/Disco4.dsk" -u=K
# # mkDisk -s=20 -path="/home/archivos/mis archivos/Disco5.dsk" -u=M -f=WF'''

# # Parsea la cadena de entrada
# result = parser.parse(cadena)

# def resultado(cadena):
#     result = parser.parse(cadena)
#     return result

# # Imprimir los valores de los parámetros
# print("Ejecutar:", result)
# print("Ejecutar:", result[1])
# print("Ejecutar:", result[1][1])
