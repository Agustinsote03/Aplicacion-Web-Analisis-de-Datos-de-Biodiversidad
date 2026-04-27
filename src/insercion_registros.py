import csv
from pathlib import Path
from validador import *

# Se crea estructura que representa un registro del dataset
def crear_estructura_registro(
    license="",
    modified="",
    institutionCode="",
    collectionCode="",
    basisOfRecord="",
    occurrenceStatus="",
    recordedBy="",
    catalogNumber="",
    eventDate="",
    year="",
    month="",
    day="",
    countryCode="",
    stateProvince="",
    county="",
    locality="",
    decimalLatitude="",
    decimalLongitude="",
    coordinateUncertaintyInMeters="",
    scientificName="",
    kingdom="",
    phylum="",
    taxonClass="",
    order="",
    family="",
    genus="",
    specificEpithet="",
    taxonRank="",
    vernacularName=""
):
  
    # Devuelve un diccionario con los campos principales del dataset
    return {
        "license": license,
        "modified": modified,
        "institutionCode": institutionCode,
        "collectionCode": collectionCode,
        "basisOfRecord": basisOfRecord,
        "occurrenceStatus": occurrenceStatus,
        "recordedBy": recordedBy,
        "catalogNumber": catalogNumber,
        "eventDate": eventDate,
        "year": year,
        "month": month,
        "day": day,
        "countryCode": countryCode,
        "stateProvince": stateProvince,
        "county": county,
        "locality": locality,
        "decimalLatitude": decimalLatitude,
        "decimalLongitude": decimalLongitude,
        "coordinateUncertaintyInMeters": coordinateUncertaintyInMeters,
        "scientificName": scientificName,
        "kingdom": kingdom,
        "phylum": phylum,
        "class": taxonClass,
        "order": order,
        "family": family,
        "genus": genus,
        "specificEpithet": specificEpithet,
        "taxonRank": taxonRank,
        "vernacularName": vernacularName,
    }



#Recibe una lista de columnas y devuelve un diccionario con esas columnas como claves y valores vacíos.
def crear_registro_vacio(columnas):
    return {col: "" for col in columnas if col != "id"}


CODIGOS_PAIS_VALIDOS = {"AR","CL","BR","UY","PY","BO","PE","EC","CO","VE"}
FORMATO_FECHA = "%d/%m/%y"

def validar_registro(registro):
    errores = []

    #Validación de coordenadas
    lat = registro.get("decimalLatitude", "")
    lon = registro.get("decimalLongitude", "")

    if lat != "" and not es_coordenada_valida(lat, -90, 90):
        errores.append(f"decimalLatitude inválida: '{lat}'. Debe estar entre -90 y 90")

    if lon != "" and not es_coordenada_valida(lon, -180, 180):
        errores.append(f"decimalLongitude inválida: '{lon}'. Debe estar entre -180 y 180")

    #Validación de fecha
    event_date = registro.get("eventDate", "").strip()
    if event_date != "":
        es_valida, fecha = es_fecha_valida(event_date, FORMATO_FECHA)
        if not es_valida:
            errores.append(
                f"eventDate inválida: '{event_date}' "
                f"Formato esperado: {FORMATO_FECHA} (ej: 15/03/85)"
            )
        elif fecha is not None:
            from datetime import datetime
            if fecha > datetime.now():
                errores.append(
                    f"eventDate inválida: '{event_date}'. La fecha no puede ser futura"
                )

    #Validación de countryCode
    country_code = registro.get("countryCode", "").strip().upper()
    if country_code != "" and country_code not in CODIGOS_PAIS_VALIDOS:
        errores.append(
            f"countryCode inválido: '{country_code}' "
            f"Valores permitidos: {CODIGOS_PAIS_VALIDOS} "
        )
    
    #Validación de incertidumbre de coordenada
    incertidumbre = registro.get("coordinateUncertaintyInMeters", "").strip()
    if incertidumbre != "" and not es_incertidumbre_valida(incertidumbre):
        errores.append(
            f"coordinateUncertaintyInMeters inválida: '{incertidumbre}' "
            "Debe ser un número entre 0 y 100"
        )

    #Validar que occurrenceStatus tenga un valor conocido si está presente
    status = registro.get("ocurrenceStatus", "").strip()
    valores_validos_status = {"PRESENT", "ABSENT"}
    if status != "" and status.upper() not in valores_validos_status:
        errores.append(
            f"occurrenceStatus inválido: '{status}' "
            f"Valores permitidos: {valores_validos_status} "
        )

    es_valido = len(errores) == 0
    return es_valido, errores