import csv 
from pathlib import Path

#Abre el archivo e imprime las primeras 10 filas
def imprimir_primeras_filas(ruta_archivo, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        
        contador = 0
        for fila in lector:
            print(fila)
            contador += 1
            
            if contador == 10:
                return
            
#Retorna una lista completa de columnas del dataset
def obtener_columnas(path_archivo):
    path = Path(path_archivo)

    with path.open(newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo)
        columnas = next(reader) 
        #Primera fila del CSV (encabezados)

    return columnas

#Retorna la posición (índice) de cada columna dentro del dataset
def posiciones_columnas(ruta_archivo):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter="\t")
        columnas = next(reader)

    posiciones = {}
    for i, col in enumerate(columnas):
        posiciones[col] = i

    return posiciones
 