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

