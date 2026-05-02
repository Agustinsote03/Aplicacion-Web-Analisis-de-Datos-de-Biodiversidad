import csv
from pathlib import Path

def eliminar_por_id(ruta_original, ruta_nueva, columna, valor, separador="\t"):
    eliminado = False

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         # Crea un archivo, no modifica el originla
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

