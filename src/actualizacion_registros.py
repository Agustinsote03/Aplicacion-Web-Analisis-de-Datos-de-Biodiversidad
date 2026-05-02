import csv
from pathlib import Path

def buscar_registros(ruta_archivo, filtros, separador="\t"):
    """
        Busca y retorna registros de un dataset que cumplan con los criterios de filtrado
    """
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

def actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones, separador="\t"):
    registro_actualizado = False

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
        open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:
            if fila.get("occurrenceID", "").strip() == str(id_registro).strip():
                for columna, nuevo_valor in modificaciones.items():

                    if columna in fila:
                        fila[columna] = nuevo_valor
                registro_actualizado = True
            escritor.writerow(fila)
    
    return registro_actualizado


def actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, separador="\t"):
    registro_actualizado = False
    errores = [] #Lista para guardar errores de validacion

    # Abrimos archivo original(lectura) y nuevo(escritura)
    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
        open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        # Leemos el CSV como diccionarios
        lector = csv.DictReader(archivo_original, delimiter=separador)
        #Preparamos el archivo de salida con las mismas columnas
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader() #Escribimos encabezado

        #Recorremos todos los registros
        for fila in lector:
            
            # Buscamos el registro por occurrenceID
            if fila.get("occurrenceID", "").strip() == str(id_registro).strip():

                # Validar antes de cambiar
                for columna, nuevo_valor in modificaciones.items():
                    # Validamos campos de texto
                    if columna in ["country", "stateProvince"]:
                        if not isinstance[nuevo_valor, str] or nuevo_valor.strip() == "":
                            errores.append(f"{columna} invalido")

                    # Validamos ID (debe ser numerico)
                    if columna == "occurrenceID":
                        if not str(nuevo_valor).isdigit():
                            errores.append("occurrenceID invalido")
                
                # Actualizar si no hay errores
                if not errores:
                    for columna, nuevo_valor in modificaciones.items():
                        if columna in fila:
                            fila[columna] = nuevo_valor
                    registro_actualizado = True
                else:   
                    # Si hay errores no se modifica
                    print("Errores:", errores)
            
            # Escribimos la fila (modificada o  no) en el nuevo archivo
            escritor.writerow(fila)
    
    # Si no se actualizo nada
    if not registro_actualizado:
        print("No se realizaron cambios")

    return registro_actualizado


def actualizar_un_campo_validando(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, separador="\t"):
    modificaciones = {columna: nuevo_valor}

    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, separador)


