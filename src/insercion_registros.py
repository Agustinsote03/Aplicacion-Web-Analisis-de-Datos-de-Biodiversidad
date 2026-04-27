import csv
from pathlib import Path

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



