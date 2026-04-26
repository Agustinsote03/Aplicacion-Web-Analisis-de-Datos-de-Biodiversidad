import csv
from pathlib import Path 

def cantidad_registros(ruta_archivo, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        contador = 0
        for fila in reader:
            contador += 1
       
    return contador