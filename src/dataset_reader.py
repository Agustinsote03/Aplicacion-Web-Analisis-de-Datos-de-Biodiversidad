import csv 
from pathlib import Path

#Punto 2A - Abre el archivo e imprime las primeras 10 filas
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
            
#Punto 2B - Retorna una lista completa de columnas del dataset
def obtener_columnas(path_archivo):
    path = Path(path_archivo)

    with path.open(newline="", encoding="utf-8") as archivo:
        reader = csv.reader(archivo)
        columnas = next(reader)  # primera fila del CSV (encabezados)

    return columnas