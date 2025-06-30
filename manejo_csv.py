import csv
import os

def leer_csv_dict(ruta_archivo):
    """Lee un archivo CSV y devuelve una lista de diccionarios."""
    if not os.path.exists(ruta_archivo):
        return []
    with open(ruta_archivo, newline="") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def escribir_csv_dict(ruta_archivo, campos, lista_diccionarios):
    """Escribe una lista de diccionarios en un archivo CSV con los campos dados."""
    with open(ruta_archivo, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(lista_diccionarios)

def agregar_csv_dict(ruta_archivo, campos, diccionario):
    """Agrega un solo diccionario como nueva fila en el archivo CSV."""
    existe = os.path.exists(ruta_archivo)
    with open(ruta_archivo, "a", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        if not existe or os.path.getsize(ruta_archivo) == 0:
            escritor.writeheader()
        escritor.writerow(diccionario)

def leer_csv_lista(ruta_archivo):
    """Lee un archivo CSV y devuelve una lista de listas."""
    if not os.path.exists(ruta_archivo):
        return []
    with open(ruta_archivo, newline="") as archivo:
        lector = csv.reader(archivo)
        return list(lector)

def escribir_csv_lista(ruta_archivo, lista_de_listas):
    """Escribe una lista de listas en un archivo CSV."""
    with open(ruta_archivo, "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(lista_de_listas)
