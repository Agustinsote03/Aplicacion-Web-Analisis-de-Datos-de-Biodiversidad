import csv
from pathlib import Path

def eliminar_por_id(ruta_original, ruta_nueva, columna, valor, separador="\t"):
    eliminado = False

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        # Lee el dataset
        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:

            # Busca el occurrenceID
            if str(fila.get(columna, "")).strip() == str(valor).strip():
                eliminado = True
                # Elimina la fila correctamente
                continue  

            escritor.writerow(fila)

    #Detecta si no encontro nada
    if not eliminado:
        print("Error: no se encontró el registro")

    return eliminado


import csv

def eliminar_por_lista(ruta_original, ruta_nueva, columna, valores_a_eliminar, separador="\t"):
    eliminados = 0

    # normalizo la lista (por si viene con espacios)
    valores_a_eliminar = [str(v).strip() for v in valores_a_eliminar]

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:

            valor = str(fila.get(columna, "")).strip()

            # si está en la lista lo elimino (no escribo)
            if valor in valores_a_eliminar:
                eliminados += 1
                continue

            escritor.writerow(fila)

    if eliminados == 0:
        print("No se eliminaron registros")

    return eliminados

import csv

def eliminar_por_condicion(ruta_original, ruta_nueva, columna, operador, valor, separador="\t"):
    eliminados = 0

    # Abrimos archivo original (lectura) y nuevo (escritura)
    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        # Recorremos todas las filas del dataset
        for fila in lector:
            # Obtenemos el valor de la columna indicada
            dato = fila.get(columna, "").strip()

            # Intentamos convertir a número (por si es year, cantidad, etc.)
            try:
                dato_val = float(dato)
                valor_val = float(valor)
            except:
                # Si no se puede convertir, lo tratamos como texto
                dato_val = dato
                valor_val = valor

            cumple = False # Asumimos que NO cumple la condicion

            # Evaluamos la condicion segun el operador
            if operador == "==":
                cumple = dato_val == valor_val
            elif operador == "!=":
                cumple = dato_val != valor_val
            elif operador == ">":
                cumple = dato_val > valor_val
            elif operador == ">=":
                cumple = dato_val >= valor_val
            elif operador == "<":
                cumple = dato_val < valor_val
            elif operador == "<=":
                cumple = dato_val <= valor_val

            # Si cumple eliminamos la fila 
            if cumple:
                eliminados += 1
                continue
            
            #Si no se elimino nada aviso: 
            escritor.writerow(fila)

    if eliminados == 0:
        print("No se eliminaron registros")

    return eliminados

