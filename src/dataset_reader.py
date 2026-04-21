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

#Cuenta la cantidad de registros (filas) que tiene el dataset
def cantidad_registros(ruta_archivo, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter=separador)

        next(reader)
        #Saltea la primera fila (encabezados)

        contador = 0
        for fila in reader:
            contador += 1
       
    return contador
 
#Cuenta la cantidad de registros que tienen al menos un valor nulo (vacío) en alguna de sus columnas
def columnas_con_nulos(ruta_archivo, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter=separador)

        columnas = next(reader)
        #Nombre de columnas

        columnas_con_nulo = set()
        #Uso set para evitar repetidos

        for fila in reader:
            for i, valor in enumerate(fila):
                if valor == "":
                    columnas_con_nulo.add(columnas[i])
                    #Guarda el nombre de la columna con valor nulo

    return list(columnas_con_nulo)

#Calcula el porcentaje de registros nulos por cada columna del dataset
def porcentaje_nulos_por_columna(ruta_archivo, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter=separador)

        columnas = next(reader)
        #Nombres de columnas

        n_cols = len(columnas)

        conteo_nulos = [0] * n_cols
        #Lista para contar nulos por columna

        total_registros = 0
        #Contador total de filas

        for fila in reader:
            total_registros += 1

            for i in range(n_cols):
                if i < len(fila) and fila[i] == "":
                    conteo_nulos[i] += 1
                #Detecta nulos y los cuenta por columna

    porcentajes = {}
    for i, col in enumerate(columnas):
        porcentajes[col] = (conteo_nulos[i] / total_registros) * 100
        #Calcula el porcentaje de nulos por columnas

    return porcentajes

#Devuelve la cantidad de valores distintos que tiene una columna específica del dataset
def valores_distintos_columna(ruta_archivo, nombre_columna, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter=separador)

        columnas = next(reader)

        if nombre_columna not in columnas:
            print("La columna no existe")
            return None

        indice = columnas.index(nombre_columna)
        #Encuentra el índice de la columna

        valores = set()
        #Uso un set para eliminar duplicados automáticamente

        for fila in reader:
            valores.add(fila[indice])

    return len(valores)

#Devuelve la frecuencia de cada valor distinto que tiene una columna específica del dataset
def frecuencia_valores_columna(ruta_archivo, nombre_columna, separador="\t"):
    ruta = Path(ruta_archivo)

    with ruta.open(encoding="utf-8", newline="") as archivo:
        reader = csv.reader(archivo, delimiter=separador)

        columnas = next(reader)

        if nombre_columna not in columnas:
            print("La columna no existe")
            return None

        indice = columnas.index(nombre_columna)

        frecuencias = {}
        #Diccionario de conteo de frecuencias por valor

        for fila in reader:
            valor = fila[indice]

            if valor in frecuencias:
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1

    return frecuencias