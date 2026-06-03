import csv
from pathlib import Path
from logger import registrar_operacion
from validador import es_coordenada_valida, validar_y_convertir_fecha, es_incertidumbre_valida
from datetime import datetime
from utils import manejar_archivo_no_encontrado
FORMATO_FECHA = "%Y-%m-%d"

def buscar_registros_generica(ruta_archivo, filtros, separador="\t"):
    """ 
    Busca y retorna registros de un dataset que cumplan con los criterios de filtrado 
    """
    registros_encontrados = []
    
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)
            
            #Se recorre cada fila del dataset
            for fila in lector:
                cumple_filtros = True
                
                #Se verifica si la fila cumple con todos los filtros del diccionario
                for columna, valor_buscado in filtros.items():

                    if fila.get(columna) != str(valor_buscado):
                        cumple_filtros = False
                        break  
                
                #Si la fila pasó todos los filtros, se agrega los resultados
                if cumple_filtros:
                    registros_encontrados.append(fila)
        
    return registros_encontrados

def buscar_registros_iadiza(ruta_archivo, filtros):
    """
        Busca registros en el dataset de IADIZA utilizando tabulaciones como separador
    """
    return buscar_registros_generica(ruta_archivo, filtros, separador="\t")

def buscar_registros_xeno_canto(ruta_archivo, filtros):
    """
        Busca registros en el dataset de XENO utilizando comas como separador
    """
    return buscar_registros_generica(ruta_archivo, filtros, separador=",")

def buscar_registros_inaturalist(ruta_archivo, filtros):
    """
        Busca registros en el dataset de INAT utilizando comas como separador
    """
    return buscar_registros_generica(ruta_archivo, filtros, separador=",")

def actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, nombre_dataset, separador="\t", columna_id="occurrenceID"):
    """
        Actualiza un campo especifico de un registro basado en su ID y genera un nuevo archivo con la actualización
    """
    registro_actualizado = False
    try:
        with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
            open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
            
            lector = csv.DictReader(archivo_original, delimiter=separador)

            escritor = csv.DictWriter((archivo_nuevo), fieldnames=lector.fieldnames, delimiter=separador)

            escritor.writeheader()

            for fila in lector:
                if fila.get(columna_id, "").strip() == str(id_registro).strip():
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

def actualizar_un_campo_iadiza(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="iadiza", separador="\t")

def actualizar_un_campo_xeno_canto(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="xeno_canto", separador=",")

def actualizar_un_campo_inaturalist(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="inaturalist", separador=",")


def actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset,separador="\t", columna_id="occurrenceID"):
    """
    Actualiza múltiples campos de un registro identificado por su ID, sin validar los nuevos valores.
    """
    registro_actualizado = False
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
                    registro_actualizado = True
                escritor.writerow(fila)

            if registro_actualizado:
                registrar_operacion(nombre_dataset, "UPDATE", 1)
            else:
                 registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)

    except FileNotFoundError:
        raise

    return registro_actualizado


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


