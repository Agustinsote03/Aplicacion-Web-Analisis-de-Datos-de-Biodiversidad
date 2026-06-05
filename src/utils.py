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
    """
        Decorador para manejar la excepción FileNotFoundError y proporcionar un mensaje de error más claro.
    """
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


def cumple_filtro(valor_fila, valor_buscado, modo="exacto"):
    """
    Evalúa si un valor de una fila cumple con el filtro.
    Modos:
      - "exacto": coincidencia exacta (2.B)
      - "contiene": coincidencia de carácteres
    """
    if not valor_fila and not valor_buscado:
        return True
    if not valor_fila or not valor_buscado:
        return False
    
    valor_fila = str(valor_fila).strip()
    valor_buscado = str(valor_buscado).strip()
    
    if modo == "contiene":
        return valor_buscado.lower() in valor_fila.lower()
    return valor_fila.lower() == valor_buscado.lower()


def buscar_registros_logica(filas, columnas, filtros = None, modo="exacto", **kwargs):
    """
    Lógica pura de búsqueda reutilizable.
    - filas: iterador de diccionarios
    - columnas: columnas válidas del dataset
    - filtros: {columna: valor_buscado}
    - modo: "exacto" o "contiene"
    """
    if filtros:
        filtros_validos = {col: val for col, val in filtros.items() if col in columnas}
        
        registros_encontrados = []
        for fila in filas:
            if all(cumple_filtro(fila.get(col, ""), val, modo) for col, val in filtros_validos.items()):
                registros_encontrados.append(fila)
    else:
        registros_encontrados = list(filas)
    return registros_encontrados