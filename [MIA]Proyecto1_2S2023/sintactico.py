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


# # Cadena de entrada
# mkdisk -size=10 -unit=M -path="/home/misdiscos/Disco5.dsk"
# fdisk -size=200 -add=10  -type=E -unit=K -path="/home/misdiscos/Disco5.dsk" -name="Particion5"
# fdisk -size=100 -add=10  -type=P -unit=K -path="/home/misdiscos/Disco5.dsk" -name="Particion6"
# fdisk -size=1 -add=10  -type=L -unit=K -path="/home/misdiscos/Disco5.dsk" -name="Particion2"
# fdisk -delete=full -path=/home/misdiscos/Disco5.dsk -name="Particion2" 





# comandos de fdisk
#Crea una partición primaria llamada Particion1 de 300 kb
#con el peor ajuste en el disco Disco1.dsk
#                                                                           fdisk -size=300 -path="/home/misdiscos/Disco5.dsk" -name=Particion1
# #Crea una partición extendida dentro de Disco2 de 300 kb
# #Tiene el peor ajuste
#                                                                           fdisk -type=E -path="/home/misdiscos/Disco5.dsk" -unit=K -name=Particion2 -size=100
# #Crea una partición lógica con el mejor ajuste, llamada Partición 3,
# #de 1 Mb en el Disco3
#                                                                           fdisk -size=1 -type=L -unit=K -fit=BF -path="/home/misdiscos/Disco5.dsk" -name="Particion3"
# #Intenta crear una partición extendida dentro de Disco2 de 200 kb
# #Debería mostrar error ya que ya existe una partición extendida
# #dentro de Disco2
#                                                                           fdisk -type=E -path="/home/misdiscos/Disco5.dsk" -name=Part3 -unit=K -size=200
# #Elimina de forma rápida una partición llamada Partición 1
#                                                                           fdisk -delete=full -name="Particion2" -path="/home/misdiscos/Disco5.dsk"
# #Elimina de forma completa una partición llamada Partición 1
#                                                                           fdisk -name=Particion2 -delete=full -path="/home/misdiscos/Disco5.dsk"
# #Quitan 500 Kb de Partición 4 en Disco4.dsk
# #Ignora los demás parámetros (s)
# #Se toma como válido el primero que aparezca, en este caso add
#                                                                           fdisk -add=-500 -size=10 -unit=K -path="/home/misdiscos/Disco5.dsk" -name=”Particion4”
# #Agrega 1 Mb a la partición Partición 4 del Disco4.dsk
# #Se debe validar que haya espacio libre después de la partición
#                                                                           fdisk -add=1 -unit=M -path="/home/misdiscos/Disco5.dsk" -name="Particion4"










# cadena = 'rmdisk -path="/home/misdiscos/Disco5.dsk"

# # Parsea la cadena de entrada
# result = parser.parse(cadena)

# def resultado(cadena):
#     result = parser.parse(cadena)
#     return result

# # Imprimir los valores de los parámetros
# print("Ejecutar:", result)
# print("Ejecutar:", result[1])
# print("Ejecutar:", result[1][1])
