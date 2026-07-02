import csv
from pathlib import Path
from logger import registrar_operacion
from validador import es_coordenada_valida, validar_y_convertir_fecha, es_incertidumbre_valida, codigos_validos
from datetime import datetime
from utils import buscar_registros_logica, manejar_archivo_no_encontrado
FORMATO_FECHA = "%Y-%m-%d"

@manejar_archivo_no_encontrado
def buscar_registros_generica(ruta_archivo, filtros, separador="\t"):
    """ 
    Busca y retorna registros de un dataset que cumplan con los criterios de filtrado 
    """
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = lector.fieldnames
        return buscar_registros_logica(lector, columnas, filtros)

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

@manejar_archivo_no_encontrado
def actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, nombre_dataset, separador="\t", columna_id="occurrenceID"):
    """
        Actualiza un campo especifico de un registro basado en su ID y genera un nuevo archivo con la actualización
    """

    if Path(ruta_original) == Path(ruta_nueva):
        raise ValueError("La ruta de origen y destino no pueden ser la misma.")
    registros_actualizados = 0
    #Contador en lugar de booleano para poder registrar cantidad de registros actualizados

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
        open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
            
        lector = csv.DictReader(archivo_original, delimiter=separador)

        escritor = csv.DictWriter((archivo_nuevo), fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:
            if fila.get(columna_id, "").strip() == str(id_registro).strip():
                fila[columna] = nuevo_valor
                registros_actualizados += 1
            
            escritor.writerow(fila)

    if registros_actualizados > 0:
        registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados)
    else:
        registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados, error=(registros_actualizados == 0))

    return registros_actualizados > 0 

def actualizar_un_campo_iadiza(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    """
        Actualiza un campo específico de un registro en el dataset IADIZA.
    """
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="iadiza", separador="\t")

def actualizar_un_campo_xeno_canto(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    """
        Actualiza un campo específico de un registro en el dataset XENO_CANTO.
    """
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="xeno_canto", separador=",")

def actualizar_un_campo_inaturalist(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor):
    """
        Actualiza un campo específico de un registro en el dataset INATURALIST.
    """
    return actualizar_un_campo_generica(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor,
                                        nombre_dataset="inaturalist", separador=",")

@manejar_archivo_no_encontrado
def actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset,separador="\t", columna_id="occurrenceID"):
    """
    Actualiza múltiples campos de un registro identificado por su ID, sin validar los nuevos valores.
    """
    registros_actualizados = 0
    #Contador en lugar de booleano para poder registrar cantidad de registros actualizados

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
            registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados, error=(registros_actualizados == 0))

    return registros_actualizados > 0

@manejar_archivo_no_encontrado
def actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset, separador="\t", columna_id="occurrenceID"):
    """
    Actualiza múltiples campos de un registro identificado por su ID, validando los nuevos valores antes de aplicar los cambios.
    Si algún valor es inválido no se realiza ninguna modificación y se muestran los errores.
    """
    #Validación una sola vez antes del loop
    errores = []
    #Lista para guardar errores de validacion

    for columna, nuevo_valor in modificaciones.items():
        if columna == "countryCode":
            # Antes solo chequeaba que no estuviera vacío; ahora valida contra los códigos
            # de país permitidos, igual que al insertar
            codigo = str(nuevo_valor).strip().upper()
            if codigo != "" and codigo not in codigos_validos:
                errores.append(f"countryCode inválido: '{nuevo_valor}'")
        elif columna in ("decimalLatitude", "latitudeDecimal"):
            # latitudeDecimal es el nombre que usa Xeno-canto; antes no se validaba
            if not es_coordenada_valida(str(nuevo_valor), -90, 90):
                errores.append(f"{columna} inválida: '{nuevo_valor}'")
        elif columna in ("decimalLongitude", "longitudeDecimal"):
            # longitudeDecimal es el nombre que usa Xeno-canto; antes no se validaba
            if not es_coordenada_valida(str(nuevo_valor), -180, 180):
                errores.append(f"{columna} inválida: '{nuevo_valor}'")
        elif columna == "eventDate":
            es_valida, fecha = validar_y_convertir_fecha(str(nuevo_valor))
            if not es_valida:
                errores.append(f"eventDate inválida: '{nuevo_valor}'")
            elif fecha and fecha > datetime.now():
                errores.append(f"eventDate futura: '{nuevo_valor}'")
        elif columna == "coordinateUncertaintyInMeters":
            if not es_incertidumbre_valida(str(nuevo_valor)):
                errores.append(f"coordinateUncertaintyInMeters inválida: '{nuevo_valor}'")
        elif columna == "occurrenceStatus":
            # Antes no se validaba; solo aplica a IADIZA
            estado = str(nuevo_valor).strip().upper()
            if estado != "" and estado not in {"PRESENT", "ABSENT"}:
                errores.append(f"occurrenceStatus inválido: '{nuevo_valor}'")
    
    
    #Recién acá se abren los archivos y se recorren las filas
    registros_actualizados = 0    
    #Contador en lugar de booleano para poder registrar cantidad de registros actualizados

    if errores:
        registrar_operacion(nombre_dataset, "UPDATE", 0, error=True)
        return False
    
    # Abrimos archivo original(lectura) y nuevo(escritura)
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
                registros_actualizados += 1
            escritor.writerow(fila)

    if registros_actualizados > 0:
        registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados)
    else:
        registrar_operacion(nombre_dataset, "UPDATE", registros_actualizados, error=(registros_actualizados == 0))

    return registros_actualizados > 0


def actualizar_un_campo_validando(ruta_original, ruta_nueva, id_registro, columna, nuevo_valor, nombre_dataset,separador="\t"):
    """
    Actualiza un único campo de un registro identificado por su ID, validando el nuevo valor.
    Es un caso particular de actualizar_multiples_campos_validando.
    """
    modificaciones = {columna: nuevo_valor}

    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones, nombre_dataset, separador)

def actualizar_multiples_campos_iadiza(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos de un registro en el dataset IADIZA.
    """
    return actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones,
                                       nombre_dataset="iadiza", separador="\t")

def actualizar_multiples_campos_xeno_canto(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos de un registro en el dataset Xeno-canto.
    """
    return actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones,
                                       nombre_dataset="xeno_canto", separador=",")

def actualizar_multiples_campos_inaturalist(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos de un registro en el dataset iNaturalist.
    """
    return actualizar_multiples_campos(ruta_original, ruta_nueva, id_registro, modificaciones,
                                       nombre_dataset="inaturalist", separador=",")

def actualizar_multiples_campos_validando_iadiza(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos validados de un registro en el dataset IADIZA.
    """
    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones,
                                                  nombre_dataset="iadiza", separador="\t")

def actualizar_multiples_campos_validando_xeno_canto(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos validados de un registro en el dataset Xeno-canto.
    """
    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones,
                                                  nombre_dataset="xeno_canto", separador=",")

def actualizar_multiples_campos_validando_inaturalist(ruta_original, ruta_nueva, id_registro, modificaciones):
    """
    Actualiza múltiples campos validados de un registro en el dataset iNaturalist.
    """
    return actualizar_multiples_campos_validando(ruta_original, ruta_nueva, id_registro, modificaciones,
                                                  nombre_dataset="inaturalist", separador=",")
