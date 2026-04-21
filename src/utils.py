import csv
from pathlib import Path 

def obtener_lector(ruta_archivo, separador="\t"):
    archivo = Path(ruta_archivo).open(encoding="utf-8", newline="")
    lector = csv.DictReader(archivo, delimiter=separador)
    return archivo,lector