import csv
from pathlib import Path 

def calcular_porcentaje_nulos_logica(iterador_filas, columnas):
    """
    Recibe un iterador de diccionarios (fila por fila) y las columnas.
    Retorna un diccionario con el porcentaje de nulos por columna.
    """
    conteo_nulos = {col: 0 for col in columnas}
    total_filas = 0
    
    for fila in iterador_filas:
        total_filas += 1
        for col in columnas:
            # get() previene errores si la fila está malformada y le falta una clave
            valor = fila.get(col, "")
            if valor is None or str(valor).strip() == "":
                conteo_nulos[col] += 1
                
    #Se calcula el porcentaje final
    porcentajes = {}
    if total_filas > 0:
        for col, nulos in conteo_nulos.items():
            porcentajes[col] = (nulos / total_filas) * 100
            
    return porcentajes


def manejar_archivo_no_encontrado(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"No se encontró el archivo: {e.filename}")
    return wrapper

@manejar_archivo_no_encontrado
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