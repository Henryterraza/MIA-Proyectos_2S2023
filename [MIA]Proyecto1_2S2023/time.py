import datetime

# Entero que representa la fecha en formato UNIX (timestamp)
timestamp = 1631424000  # Ejemplo: 13 de septiembre de 2021

# Crear un objeto datetime a partir del timestamp
fecha = datetime.datetime.fromtimestamp(timestamp)

print(f'Fecha como objeto datetime: {fecha}')
