import csv
from pathlib import Path 

def manejar_archivo_no_encontrado(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"No se encontró el archivo: {e.filename}")
    return wrapper


def cantidad_registros(ruta_archivo, separador="\t"):
    """
    Retorna la cantidad de registros del dataset sin contar el encabezado.
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        contador = 0
        for fila in reader:
            contador += 1
       
    return contador

