import csv
from pathlib import Path

def buscar_registros(ruta_archivo, filtros, separador="\t"):

    registros_encontrados = []  
    #Lista donde voy a guardar resultados

    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)

        for fila in lector:  
        #Recorro todo el dataset

            cumple_condicion = True  
            #Asumo que cumple

            #Recorro los filtros que se pasaron por parámetro
            for columna, valor in filtros.items():

                #Comparo valor del CSV con el filtro
                if fila.get(columna, "").strip() != str(valor).strip():
                    cumple_condicion = False
                    break  
                    #Si no cumple, corto el bucle

            if cumple_condicion:
                registros_encontrados.append(fila)
                #Si cumple todas las condiciones, guardo el registro en la lista de resultados

    return registros_encontrados

def actualizar_un_campo(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, separador="\t"):
    """
        Actualiza un campo especifico de un registro basado en su ID y genera un nuevo archivo con la actualización
    """
    registro_actualizado = False

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
        open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
        
        lector = csv.DictReader(archivo_original, delimiter=separador)

        escritor = csv.DictWriter((archivo_nuevo), fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:
            if fila.get("ocurrenceID","").strip() == str(id_registro).strip():
                fila[columna] = nuevo_valor
                registro_actualizado = True
        
        escritor.writerow(fila)
    return registro_actualizado
