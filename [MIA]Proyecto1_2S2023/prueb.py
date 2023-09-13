import subprocess
import os

# Agregar nodos al gráfico
dot_code = '''
digraph G {
    node1;
    node2;
    node3;

    node1 -> node2 [label="linea1adfasfas"];
    node1 -> node3 [label="linea2"];
    node2 -> node3 [label="linea3"];
}
'''

# # Definir la ruta deseada para guardar la imagen (requiere permisos de administrador)
# ruta_deseada = '/ruta/deseada/para/guardar/imagen.png'

# # Crear el directorio si no existe
# # directorio_destino = os.path.dirname(ruta_deseada)
# # if not os.path.exists(directorio_destino):
# #     os.makedirs(directorio_destino)

# ruta_archivo, archivo = os.path.split(ruta_deseada)
# ruta_archivo = ruta_archivo.replace(" ", "_")
# # print(ruta_archivo)
# # Comando para crear el archivo en la ruta especificada (con sudo)
# comando_creacion_directorio = f'sudo mkdir -p  {ruta_archivo}'

# os.system(comando_creacion_directorio)

# # Generar el gráfico en formato DOT

# # Usar sudo para escribir el archivo DOT y luego renderizarlo
# with open('/tmp/graph.dot', 'w') as dot_file:
#     dot_file.write(dot_code)

# comando_chmod = f'sudo chmod 777 {ruta_archivo}'

# os.system(comando_chmod)

# # Usar sudo para renderizar el archivo DOT como imagen PNG en la ubicación deseada
# comando_renderizado = f'sudo dot -Tpng /tmp/graph.dot -o {ruta_deseada}'
# subprocess.run(comando_renderizado, shell=True)

# # Ahora, la imagen se ha generado y guardado en la ubicación deseada con permisos de administrador, creando el directorio si es necesario.






ruta_deseada = "/home/user/reports/reporte1.jpg"


# Crear el directorio si no existe
# directorio_destino = os.path.dirname(ruta_deseada)
# if not os.path.exists(directorio_destino):
#     os.makedirs(directorio_destino)

ruta_archivo, archivo = os.path.split(ruta_deseada)
ruta_archivo = ruta_archivo.replace(" ", "_")
# print(ruta_archivo)
# Comando para crear el archivo en la ruta especificada (con sudo)
comando_creacion_directorio = f'sudo mkdir -p  {ruta_archivo}' + "/"

os.system(comando_creacion_directorio)

# Generar el gráfico en formato DOT

# Usar sudo para escribir el archivo DOT y luego renderizarlo
with open('/tmp/graph.dot', 'w') as dot_file:
    dot_file.write(dot_code)

comando_chmod = f'sudo chmod 777 {ruta_archivo}'

os.system(comando_chmod)

archivo = archivo.split(".")

ruta_deseada = ruta_archivo + "/" + archivo[0] + ".png"

# Usar sudo para renderizar el archivo DOT como imagen PNG en la ubicación deseada
comando_renderizado = f'sudo dot -Tpng /tmp/graph.dot -o {ruta_deseada}'
subprocess.run(comando_renderizado, shell=True)
print(f"Se genero con exito la imagen en la ruta: {ruta_deseada}")
