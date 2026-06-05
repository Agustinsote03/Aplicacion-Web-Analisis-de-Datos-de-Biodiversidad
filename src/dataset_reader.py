import csv 
#Se importa 'manejar_archivo_no_encontrado' que todavia no está en esta rama
from utils import cantidad_registros, manejar_archivo_no_encontrado, calcular_porcentaje_nulos_logica
from pathlib import Path 

@manejar_archivo_no_encontrado
def imprimir_primeras_filas(ruta_archivo, separador="\t"):
    """
    Abre el archivo e imprime las primeras 10 filas
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        
        contador = 0
        for fila in lector:
            print(fila)
            contador += 1
            
            if contador == 10:
                return

@manejar_archivo_no_encontrado   
def obtener_columnas(path_archivo, separador="\t"):
    """
    Retorna una lista completa de columnas del dataset
    """
    path = Path(path_archivo)

    with path.open(newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        columnas = reader.fieldnames
        # Primera fila del CSV (encabezados)

    return columnas

@manejar_archivo_no_encontrado
def posiciones_columnas(ruta_archivo, separador="\t"):
    """
    Retorna la posición (índice) de cada columna dentro del dataset
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)
        columnas = reader.fieldnames

    posiciones = {}
    for i, col in enumerate(columnas):
        posiciones[col] = i

    return posiciones

@manejar_archivo_no_encontrado
def columnas_con_nulos(ruta_archivo, separador="\t"):
    """
    Cuenta la cantidad de registros que tienen al menos un valor nulo (vacío) en alguna de sus columnas
    """""
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        columnas_con_nulo = set()
        # Uso set para evitar repetidos

        for fila in reader:
            for col, valor in fila.items():
                if valor == "":
                    columnas_con_nulo.add(col)
                    # Guarda el nombre de la columna con valor nulo

    return columnas_con_nulo

@manejar_archivo_no_encontrado
def porcentaje_nulos_por_columna(ruta_archivo, separador="\t"):
    """
    Calcula el porcentaje de registros nulos por cada columna del dataset
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        columnas = reader.fieldnames
        # Nombres de columnas

        conteo_nulos = {col: 0 for col in columnas}
        # Diccionario para contar nulos por columna

        total_registros = 0
        # Contador total de filas

        for fila in reader:
            total_registros += 1

            for col in columnas:
                if fila[col] == "":
                    conteo_nulos[col] += 1
                # Detecta nulos y los cuenta por columna

    if total_registros == 0:
        return {}
        # Evita la división por 0 si el dataset está vacío
     
    porcentajes = {}
    for col in columnas:
        porcentajes[col] = (conteo_nulos[col] / total_registros) * 100
        # Calcula el porcentaje de nulos por columnas

    return porcentajes

@manejar_archivo_no_encontrado
def valores_distintos_columna(ruta_archivo, nombre_columna, separador="\t"):
    """
    Devuelve la cantidad de valores distintos que tiene una columna específica del dataset
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        if nombre_columna not in reader.fieldnames:
            raise KeyError (f"La columna {nombre_columna} no existe en el dataset")

        valores = set()
        # Uso un set para eliminar duplicados automáticamente

        for fila in reader:
            valores.add(fila[nombre_columna])

    return len(valores)

@manejar_archivo_no_encontrado
def frecuencia_valores_columna(ruta_archivo, nombre_columna, separador="\t"):
    """
    Devuelve la frecuencia de cada valor distinto que tiene una columna específica del datase
    t"""
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        if nombre_columna not in reader.fieldnames:
            raise KeyError (f"La columna {nombre_columna} no existe en el dataset")

        frecuencias = {}
        # Diccionario de conteo de frecuencias por valor

        for fila in reader:
            valor = fila[nombre_columna]
            if valor == "" or valor is None:
                valor = "(nulo)"
                
            if valor in frecuencias:
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1

    return frecuencias

@manejar_archivo_no_encontrado
def resumen_columna(ruta_archivo, nombre_columna, tipo, separador="\t"):
    """
    Calcula un resumen de una columna específica del dataset dependiendo de su tipo (numérico, coordenada o texto)
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        if nombre_columna not in reader.fieldnames:
            raise KeyError (f"La columna {nombre_columna} no existe en el dataset")
            # Verifica si la columna existe

        valores = []

        for fila in reader:
            valor = fila[nombre_columna]

            if valor != "":
                valores.append(valor)
            # Filtra valores válidos y arma una lista con todos los datos de la columna

    if len(valores) == 0:
        return None

    # Tipo numérico: calcula mínimo, máximo y promedio
    if tipo == "numeric":
        numeros = []
        for v in valores:
            try:
                numeros.append(float(v))
            except ValueError:
                continue

        if not numeros:
            return None
        
        minimo = min(numeros)
        maximo = max(numeros)
        promedio = sum(numeros) / len(numeros)

        return {
            "min": minimo,
            "max": maximo,
            "promedio": promedio
        }

    # Tipo coordinate: calcula mínimo y máximo
    elif tipo == "coordinate":
        numeros = []

        for v in valores:
            try:
                numeros.append(float(v))
            except ValueError:
                continue

        if not numeros:
            return None

        minimo = min(numeros)
        maximo = max(numeros)

        return {
            "min": minimo,
            "max": maximo
        }

    # Tipo text: calcula longitud mínima y máxima de los textos
    elif tipo == "text":
        longitudes = [len(v) for v in valores]

        minimo = min(longitudes)
        maximo = max(longitudes)

        return {
            "min longitud": minimo,
            "max longitud": maximo
        }

    else:
        raise ValueError(f"Tipo no válido: '{tipo}'. Los tipos aceptados son: 'numeric', 'coordinate', 'text'")
    
@manejar_archivo_no_encontrado
def porcentaje_nulos_2F(ruta_archivo, separador="\t"):
    """
    Se encarga únicamente de abrir el archivo con csv y delegar 
    el cálculo a la función matemática.
    """
    # Usamos open clásico, sin pathlib
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = lector.fieldnames
        
        # Le pasamos el iterador directamente a la lógica
        return calcular_porcentaje_nulos_logica(lector, columnas)
    
@manejar_archivo_no_encontrado
def columnas_totalmente_nulas(ruta_archivo, separador="\t"):
    """
    Retorna una lista de columnas cuyos valores son nulos en todos los registros.
    """
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)
        columnas = reader.fieldnames
        conteo_nulos = {col: 0 for col in columnas}
        total = 0

        for fila in reader:
            total += 1
            for col in columnas:
                if fila[col] == "":
                    conteo_nulos[col] += 1

    if total == 0:
        return list(columnas)

    return [col for col in columnas if conteo_nulos[col] == total]