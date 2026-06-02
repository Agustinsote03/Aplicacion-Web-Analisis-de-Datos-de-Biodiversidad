import csv
from pathlib import Path
from logger import registrar_operacion
from validador import es_coordenada_valida, es_fecha_valida, es_incertidumbre_valida
from datetime import datetime
FORMATO_FECHA = "%Y-%m-%d"

def buscar_registros(ruta_archivo, filtros, separador="\t"):
    """
        Busca y retorna registros de un dataset que cumplan con los criterios de filtrado
    """
    registros_encontrados = []  
    # Lista donde voy a guardar resultados
    try:
        with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)

            for fila in lector:  
            # Recorro todo el dataset

                cumple_condicion = True  
                # Asumo que cumple

                # Recorro los filtros que se pasaron por parámetro
                for columna, valor in filtros.items():

                    # Comparo valor del CSV con el filtro
                    if fila.get(columna, "").strip() != str(valor).strip():
                        cumple_condicion = False
                        break  
                        # Si no cumple, corto el bucle

                if cumple_condicion:
                    registros_encontrados.append(fila)
                    # Si cumple todas las condiciones, guardo el registro en la lista de resultados
    except FileNotFoundError:
        raise

    return registros_encontrados

def actualizar_un_campo(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, nombre_dataset, separador="\t"):
    """
        Actualiza un campo especifico de un registro basado en su ID y genera un nuevo archivo con la actualización
    """
    registros_actualizados = 0
    #Contador en lugar de booleano para poder registrar cantidad de registros actualizados

    try:
        with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
            open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
            
            lector = csv.DictReader(archivo_original, delimiter=separador)

            escritor = csv.DictWriter((archivo_nuevo), fieldnames=lector.fieldnames, delimiter=separador)

            escritor.writeheader()

            for fila in lector:
                if fila.get("occurrenceID","").strip() == str(id_registro).strip():
                    fila[columna] = nuevo_valor
                    registros_actualizados += 1
            
                escritor.writerow(fila)

            if registros_actualizados > 0:
                registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados)
            else:
                registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)
    except FileNotFoundError:
        raise

    return registros_actualizados

def actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset,separador="\t", columna_id="occurrenceID"):
    """
    Actualiza múltiples campos de un registro identificado por su ID, sin validar los nuevos valores.
    """
    registros_actualizados = 0
    #Contador en lugar de booleano para poder registrar cantidad de registros actualizados

    try:
        with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
            open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

            lector = csv.DictReader(archivo_original, delimiter=separador)
            escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

            escritor.writeheader()

            for fila in lector:
                if fila.get(columna_id, "").strip() == str(id_registro).strip():
                    for columna, nuevo_valor in modificaciones.items():

                        if columna in fila:
                            fila[columna] = nuevo_valor
                    registros_actualizados += 1
                escritor.writerow(fila)

            if registros_actualizados > 0:
                registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados)
            else:
                 registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)

    except FileNotFoundError:
        raise

    return registros_actualizados


def actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset, separador="\t", columna_id="occurrenceID"):
    """
    Actualiza múltiples campos de un registro identificado por su ID, validando los nuevos valores antes de aplicar los cambios.
    Si algún valor es inválido no se realiza ninguna modificación y se muestran los errores.
    """
    #Validación una sola vez antes del loop
    errores = []
    #Lista para guardar errores de validacion

    for columna, nuevo_valor in modificaciones.items():
        if columna in ["countryCode", "stateProvince"]:
            if not isinstance(nuevo_valor, str) or nuevo_valor.strip() == "":
                errores.append(f"{columna} invalido")
        elif columna == "decimalLatitude":
            if not es_coordenada_valida(str(nuevo_valor), -90, 90):
                errores.append(f"decimalLatitude inválida: '{nuevo_valor}'")
        elif columna == "decimalLongitude":
            if not es_coordenada_valida(str(nuevo_valor), -180, 180):
                errores.append(f"decimalLongitude inválida: '{nuevo_valor}'")
        elif columna == "eventDate":
            es_valida, fecha = es_fecha_valida(str(nuevo_valor), FORMATO_FECHA)
            if not es_valida:
                errores.append(f"eventDate inválida: '{nuevo_valor}'")
            elif fecha and fecha > datetime.now():
                errores.append(f"eventDate futura: '{nuevo_valor}'")
        elif columna == "coordinateUncertaintyInMeters":
            if not es_incertidumbre_valida(str(nuevo_valor)):
                errores.append(f"coordinateUncertaintyInMeters inválida: '{nuevo_valor}'")
    
    #Recién acá se abren los archivos y se recorren las filas
    registro_actualizado = False    

    if errores:
        registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)
        return False
    
    # Abrimos archivo original(lectura) y nuevo(escritura)
    try:
        with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
            open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

            # Leemos el CSV como diccionarios
            lector = csv.DictReader(archivo_original, delimiter=separador)
            #Preparamos el archivo de salida con las mismas columnas
            escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

            escritor.writeheader() #Escribimos encabezado

            # Recorremos todos los registros
            for fila in lector:
                if str(fila.get(columna_id, "")).strip() == str(id_registro).strip():
                    for columna, nuevo_valor in modificaciones.items():
                        if columna in fila:
                            fila[columna] = nuevo_valor
                    registro_actualizado = True
                escritor.writerow(fila)

        if registro_actualizado:
            registrar_operacion(nombre_dataset, "UPDATE", 1)
        else:
            registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)

    except FileNotFoundError:
        raise

    return registro_actualizado


def actualizar_un_campo_validando(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, nombre_dataset,separador="\t"):
    """
    Actualiza un único campo de un registro identificado por su ID, validando el nuevo valor.
    Es un caso particular de actualizar_multiples_campos_validando.
    """
    modificaciones = {columna: nuevo_valor}

    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset, separador)


