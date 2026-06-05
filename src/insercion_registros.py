import csv
from pathlib import Path
from validador import *
from logger import registrar_operacion
from utils import manejar_archivo_no_encontrado

#-----------------FUNCIONES AUXILIARES---------------------#
# Se ingresa un nuevo registro por teclado solicitando al usuario los campos principales del dataset 
def ingresar_registro_por_teclado_iadiza():
    """
    Solicita al usuario los campos principales del registro IADIZA por teclado y retorna el registro creado.
    """
    print("Ingrese los datos del nuevo registro:")

    # Pido los campos principales del dataset al usuario
    license = input("License: ")
    institutionCode = input("Institution Code: ")
    collectionCode = input("Collection Code: ")
    basisOfRecord = input("Basis of Record: ")
    occurrenceStatus = input("Occurrence Status (PRESENT/ABSENT): ")
    recordedBy = input("Recorded By: ")
    eventDate = input("Event Date (YYYY-MM-DD): ")
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")
    countryCode = input("Country Code: ")
    stateProvince = input("State/Province: ")
    locality = input("Locality: ")
    decimalLatitude = input("Latitude: ")
    decimalLongitude = input("Longitude: ")
    scientificName = input("Scientific Name: ")

    # Uso la función de creación de estructura para generar un nuevo registro con los datos ingresados
    registro = crear_estructura_registro_iadiza(
        license=license,
        institutionCode=institutionCode,
        collectionCode=collectionCode,
        basisOfRecord=basisOfRecord,
        occurrenceStatus=occurrenceStatus,
        recordedBy=recordedBy,
        eventDate=eventDate,
        year=year,
        month=month,
        day=day,
        countryCode=countryCode,
        stateProvince=stateProvince,
        locality=locality,
        decimalLatitude=decimalLatitude,
        decimalLongitude=decimalLongitude,
        scientificName=scientificName
    )

    return registro

def ingresar_registro_por_teclado_xeno_canto():
    """
    Solicita al usuario los campos principales del registro Xeno-canto por teclado y retorna el registro creado.
    """
    print("Ingrese los datos del nuevo registro:")

    # Pido los campos principales del dataset al usuario
    basisOfRecord=input("Basis of Record: ")
    collectionCode=input("Collection Code: ")
    genus=input("Genus: ")
    scientificName=input("Scientific Name: ")
    taxonRank=input("Taxon Rank: ")
    kingdom=input("Kingdom: ")
    family=input("Family: ")
    longitudeDecimal=input("Longitude Decimal: ")
    latitudeDecimal=input("Latitude Decimal: ")
    country=input("Country: ")
    locality=input("Locality: ")
    recordedBy=input("Recorded By: ")
    eventDate=input("Event Date (YYYY-MM-DD): ")
    eventTime=input("Event Time: ")
    behavior=input("Behavior: ")
    sex=input("Sex: ")
    lifeStage=input("Life Stage: ")
    license=input("License: ")

    # Uso la función de creación de estructura para generar un nuevo registro con los datos ingresados
    registro = crear_estructura_registro_xeno_canto(
        basisOfRecord=basisOfRecord,
        collectionCode=collectionCode,
        genus=genus,
        scientificName=scientificName,
        taxonRank=taxonRank,
        kingdom=kingdom,
        family=family,
        longitudeDecimal=longitudeDecimal,
        latitudeDecimal=latitudeDecimal,
        country=country,
        locality=locality,
        recordedBy=recordedBy,
        eventDate=eventDate,
        eventTime=eventTime,
        behavior=behavior,
        sex=sex,
        lifeStage=lifeStage,
        license=license
    )

    return registro

def ingresar_registro_por_teclado_inaturalist():
    """
    Solicita al usuario los campos principales del registro iNaturalist por teclado y retorna el registro creado.
    """
    print("Ingrese los datos del nuevo registro:")

    # Pido los campos principales del dataset al usuario
    basisOfRecord=input("Basis of Record: ")
    institutionCode=input("Institution Code: ")
    recordedBy=input("Recorded By: ")
    identifiedBy=input("Identified By: ")
    captive=input("Captive: ")
    eventDate=input("Event Date (YYYY-MM-DD): ")
    eventTime=input("Event Time: ")
    decimalLatitude=input("Decimal Latitude: ")
    decimalLongitude=input("Decimal Longitude: ")
    coordinateUncertaintyInMeters=input("Coordinate Uncertainty in Meters: ")
    countryCode=input("Country Code: ")
    stateProvince=input("State Province: ")
    scientificName=input("Scientific Name: ")
    taxonRank=input("Taxon Rank: ")
    kingdom=input("Kingdom: ")
    family=input("Family: ")
    genus=input("Genus: ")
    license=input("License: ")
    sex=input("Sex: ")
    lifeStage=input("Life Stage: ")
    vitality=input("Vitality: ")

    # Uso la función de creación de estructura para generar un nuevo registro con los datos ingresados
    registro = crear_estructura_registro_inaturalist(
        basisOfRecord=basisOfRecord,
        institutionCode=institutionCode,
        recordedBy=recordedBy,
        identifiedBy=identifiedBy,
        captive=captive,
        eventDate=eventDate,
        eventTime=eventTime,
        decimalLatitude=decimalLatitude,
        decimalLongitude=decimalLongitude,
        coordinateUncertaintyInMeters=coordinateUncertaintyInMeters,
        countryCode=countryCode,
        stateProvince=stateProvince,
        scientificName=scientificName,
        taxonRank=taxonRank,
        kingdom=kingdom,
        family=family,
        genus=genus,
        license=license,
        sex=sex,
        lifeStage=lifeStage,
        vitality=vitality
    )

    return registro

#---------------------FUNCIONES PRINCIPALES---------------------#

def crear_estructura_registro_generica(campos):
    """
    Crea y retorna un diccionario con los campos recibidos, inicializados con string vacío si no tienen valor.
    """
    return {campo: valor for campo, valor in campos.items()}


def crear_estructura_registro_xeno_canto(
    basisOfRecord="", collectionCode="", genus="", scientificName="",
    taxonRank="", kingdom="", family="", longitudeDecimal="",
    latitudeDecimal="", country="", locality="", recordedBy="",
    eventDate="", eventTime="", behavior="", sex="", lifeStage="", license=""
):
    """
    Crea y retorna un diccionario con los campos del dataset Xeno-canto.
    """
    return crear_estructura_registro_generica(locals())


def crear_estructura_registro_inaturalist(
    basisOfRecord="", institutionCode="", recordedBy="", identifiedBy="",
    captive="", eventDate="", eventTime="", decimalLatitude="",
    decimalLongitude="", coordinateUncertaintyInMeters="", countryCode="",
    stateProvince="", scientificName="", taxonRank="", kingdom="",
    family="", genus="", license="", sex="", lifeStage="", vitality=""
):
    """
    Crea y retorna un diccionario con los campos del dataset iNaturalist.
    """
    return crear_estructura_registro_generica(locals())

def crear_estructura_registro_iadiza(
    license="", modified="", institutionCode="", collectionCode="",
    basisOfRecord="", occurrenceStatus="", recordedBy="", catalogNumber="",
    eventDate="", year="", month="", day="",
    countryCode="", stateProvince="", county="", locality="",
    decimalLatitude="", decimalLongitude="", coordinateUncertaintyInMeters="", scientificName="",
    kingdom="", phylum="", taxonClass="", order="",
    family="", genus="", specificEpithet="", taxonRank="", vernacularName=""
):
    """
    Crea y retorna un diccionario con los campos del dataset IADIZA.
    """
    campos = locals()
    campos["class"] = campos.pop("taxonClass")
    return crear_estructura_registro_generica(campos)

COLUMNAS_ID = {"gbifID", "occurrenceID", "catalogNumber"}

# Recibe una lista de columnas y devuelve un diccionario con esas columnas como claves y valores vacíos.
def crear_registro_vacio(columnas):
    """
    Retorna un diccionario con las columnas dadas como claves y valores vacíos, excluyendo las columnas de ID.
    """
    return {col: "" for col in columnas if col not in COLUMNAS_ID}

CODIGOS_PAIS_VALIDOS = {"AR","CL","BR","UY","PY","BO","PE","EC","CO","VE"}
FORMATO_FECHA = "%Y-%m-%d"

def validar_registro_iadiza(registro):
    """
    Valida los campos de un registro IADIZA.
    Reutiliza las funciones auxiliares ya desarrolladas.
    """
    errores = []

    # Coordenadas
    lat = registro.get("decimalLatitude", "")
    lon = registro.get("decimalLongitude", "")
    if lat != "" and not es_coordenada_valida(lat, -90, 90):
        errores.append(f"decimalLatitude inválida: '{lat}'. Debe estar entre -90 y 90")
    if lon != "" and not es_coordenada_valida(lon, -180, 180):
        errores.append(f"decimalLongitude inválida: '{lon}'. Debe estar entre -180 y 180")

    # Fecha
    event_date = registro.get("eventDate", "").strip()
    if event_date != "":
        es_valida, fecha = validar_y_convertir_fecha(event_date)
        if not es_valida:
            errores.append(f"eventDate inválida: '{event_date}'. Formato esperado: {FORMATO_FECHA}")
        elif fecha is not None and fecha > datetime.now():
            errores.append(f"eventDate inválida: '{event_date}'. La fecha no puede ser futura")

    # countryCode
    country_code = registro.get("countryCode", "").strip().upper()
    if country_code != "" and country_code not in CODIGOS_PAIS_VALIDOS:
        errores.append(f"countryCode inválido: '{country_code}'. Valores permitidos: {CODIGOS_PAIS_VALIDOS}")

    # Incertidumbre
    incertidumbre = registro.get("coordinateUncertaintyInMeters", "").strip()
    if incertidumbre != "" and not es_incertidumbre_valida(incertidumbre):
        errores.append(f"coordinateUncertaintyInMeters inválida: '{incertidumbre}'. Debe ser un número entre 0 y 100")

    # occurrenceStatus
    status = registro.get("occurrenceStatus", "").strip()
    if status != "" and status.upper() not in {"PRESENT", "ABSENT"}:
        errores.append(f"occurrenceStatus inválido: '{status}'. Valores permitidos: PRESENT, ABSENT")

    return len(errores) == 0, errores


def validar_registro_xeno_canto(registro):
    """
    Valida los campos de un registro Xeno-canto.
    Reutiliza las funciones auxiliares ya desarrolladas.
    """
    errores = []

    # Coordenadas (Xeno-canto usa nombres distintos)
    lat = registro.get("latitudeDecimal", "")
    lon = registro.get("longitudeDecimal", "")
    if lat != "" and not es_coordenada_valida(lat, -90, 90):
        errores.append(f"latitudeDecimal inválida: '{lat}'. Debe estar entre -90 y 90")
    if lon != "" and not es_coordenada_valida(lon, -180, 180):
        errores.append(f"longitudeDecimal inválida: '{lon}'. Debe estar entre -180 y 180")

    # Fecha
    event_date = registro.get("eventDate", "").strip()
    if event_date != "":
        es_valida, fecha = validar_y_convertir_fecha(event_date)
        if not es_valida:
            errores.append(f"eventDate inválida: '{event_date}'. Formato esperado: {FORMATO_FECHA}")
        elif fecha is not None and fecha > datetime.now():
            errores.append(f"eventDate inválida: '{event_date}'. La fecha no puede ser futura")

    return len(errores) == 0, errores


def validar_registro_inaturalist(registro):
    """
    Valida los campos de un registro iNaturalist.
    Reutiliza las funciones auxiliares ya desarrolladas.
    """
    errores = []

    # Coordenadas
    lat = registro.get("decimalLatitude", "")
    lon = registro.get("decimalLongitude", "")
    if lat != "" and not es_coordenada_valida(lat, -90, 90):
        errores.append(f"decimalLatitude inválida: '{lat}'. Debe estar entre -90 y 90")
    if lon != "" and not es_coordenada_valida(lon, -180, 180):
        errores.append(f"decimalLongitude inválida: '{lon}'. Debe estar entre -180 y 180")

    # Fecha
    event_date = registro.get("eventDate", "").strip()
    if event_date != "":
        es_valida, fecha = validar_y_convertir_fecha(event_date)
        if not es_valida:
            errores.append(f"eventDate inválida: '{event_date}'. Formato esperado: {FORMATO_FECHA}")
        elif fecha is not None and fecha > datetime.now():
            errores.append(f"eventDate inválida: '{event_date}'. La fecha no puede ser futura")

    # countryCode
    country_code = registro.get("countryCode", "").strip().upper()
    if country_code != "" and country_code not in CODIGOS_PAIS_VALIDOS:
        errores.append(f"countryCode inválido: '{country_code}'. Valores permitidos: {CODIGOS_PAIS_VALIDOS}")

    # Incertidumbre
    incertidumbre = registro.get("coordinateUncertaintyInMeters", "").strip()
    if incertidumbre != "" and not es_incertidumbre_valida(incertidumbre):
        errores.append(f"coordinateUncertaintyInMeters inválida: '{incertidumbre}'. Debe ser un número entre 0 y 100")

    return len(errores) == 0, errores


@manejar_archivo_no_encontrado
def max_numero_dataset(ruta_archivo, separador, columna, extraer_numero):
    """
    Recorre el dataset y retorna el mayor número encontrado en la columna indicada,
    usando la función extraer_numero para obtener el número de cada valor.
    """
    max_num = 0
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=separador)
        for fila in reader:
            valor = fila.get(columna, "").strip()
            num = extraer_numero(valor)
            if num is not None and num > max_num:
                max_num = num
    return max_num

def max_catalog_number_iadiza(ruta_archivo, separador="\t"):
    """
    Obtiene el máximo número de catalogNumber en el dataset IADIZA, considerando solo los valores que son dígitos.
    """
    return max_numero_dataset(ruta_archivo, separador, "catalogNumber",
        lambda v: int(v) if v.isdigit() else None)

def max_catalog_number_xeno_canto(ruta_archivo, separador=","):
    """
    Obtiene el máximo número de catalogNumber en el dataset XENO_CANTO, considerando solo los valores que empiezan con "XC" seguidos de dígitos.
    """
    return max_numero_dataset(ruta_archivo, separador, "catalogNumber",
        lambda v: int(v[2:]) if v.startswith("XC") and v[2:].isdigit() else None)

def max_catalog_number_inaturalist(ruta_archivo, separador=","):
    """
    Obtiene el máximo número de catalogNumber en el dataset INATURALIST, considerando solo los valores que son dígitos.
    """
    return max_numero_dataset(ruta_archivo, separador, "id",
        lambda v: int(v) if v.isdigit() else None)


def preparar_estructura_generica(registro, ruta_archivo, columnas, separador, obtener_max_num, construir_ids):
    """
    Toma un registro y lo completa con todas las columnas del dataset,
    delegando la obtención del máximo número y la construcción de IDs a funciones específicas.
    """
    max_num = obtener_max_num(ruta_archivo, separador)
    nuevo_num = max_num + 1

    registro_completo = {col: "" for col in columnas}
    for campo, valor in registro.items():
        if campo in registro_completo:
            registro_completo[campo] = valor

    ids = construir_ids(nuevo_num)
    registro_completo.update(ids)

    return registro_completo

def preparar_estructura_iadiza(registro, ruta_archivo, columnas, nombre_dataset, separador="\t"):
    """
    Prepara la estructura completa de un nuevo registro para el dataset IADIZA, asignando los IDs correspondientes.
    """
    return preparar_estructura_generica(
        registro, ruta_archivo, columnas, separador,
        obtener_max_num=lambda r, s: max_catalog_number_iadiza(r, s),
        construir_ids=lambda n: {
            "gbifID": "",
            "occurrenceID": f"{nombre_dataset}:COI:{str(n).zfill(6)}",
            "catalogNumber": str(n).zfill(6)
        }
    )

def preparar_estructura_xeno_canto(registro, ruta_archivo, columnas, separador=","):
    """
    Prepara la estructura completa de un nuevo registro para el dataset XENO_CANTO, asignando los IDs correspondientes.
    """
    return preparar_estructura_generica(
        registro, ruta_archivo, columnas, separador,
        obtener_max_num=lambda r, s: max_catalog_number_xeno_canto(r, s),
        construir_ids=lambda n: {
            "id": f"{n}@XC",
            "occurrenceID": f"https://data.biodiversitydata.nl/xeno-canto/observation/XC{n}",
            "catalogNumber": f"XC{n}"
        }
    )

def preparar_estructura_inaturalist(registro, ruta_archivo, columnas, separador=","):
    """
    Prepara la estructura completa de un nuevo registro para el dataset INATURALIST, asignando los IDs correspondientes.
    """
    return preparar_estructura_generica(
        registro, ruta_archivo, columnas, separador,
        obtener_max_num=lambda r, s: max_catalog_number_inaturalist(r, s),
        construir_ids=lambda n: {
            "id": str(n),
            "occurrenceID": f"https://www.inaturalist.org/observations/{n}",
            "catalogNumber": str(n)
        }
    )

@manejar_archivo_no_encontrado
def insertar_registro(ruta_origen, ruta_destino, registro, nombre_dataset, preparar_fn, validar_fn, separador="\t"):
    """
    Valida e inserta un único registro al final del dataset, guardando el resultado en un nuevo archivo.
    Si el registro es inválido no se realiza ninguna inserción.
    """
    es_valido, errores = validar_fn(registro)

    if not es_valido:
        registrar_operacion(nombre_dataset, "INSERT", 0, error=True)
        return  

    with open(ruta_origen, "r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in, delimiter=separador)
        columnas = reader.fieldnames

        registro_completo = preparar_fn(registro, ruta_origen, columnas)

        with open(ruta_destino, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter=separador, extrasaction='ignore')
            writer.writeheader()

            for fila in reader:
                writer.writerow(fila)

            writer.writerow(registro_completo)

    registrar_operacion(nombre_dataset, "INSERT", 1)
    # Si el registro es válido se registra la operación con éxito indicando que se insertó 1 registro

# Función para insertar múltiples registros ingresados por teclado
@manejar_archivo_no_encontrado
def insertar_multiples_registros(ruta_origen, ruta_destino, nombre_dataset, preparar_fn, validar_fn, ingresar_fn, separador="\t"):
    """
    Solicita registros por teclado en un loop, valida cada uno y los inserta al final del dataset.
    La carga termina cuando el usuario deja el campo license vacío.
    """
    registros = []

    print("Carga de múltiples registros (dejar vacío 'license' para terminar)")

    while True:
        registro = ingresar_fn()

        if registro.get("license", "") == "":
            break
        
        es_valido, errores = validar_fn(registro)

        if es_valido:
            registros.append(registro)
            print("Registro agregado\n")
        else:
            print("Registro inválido:")
            for e in errores:
                print("-", e)
            print()

    if not registros:
        registrar_operacion(nombre_dataset, "INSERT", 0, error=True)
        return

    with open(ruta_origen, "r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in, delimiter=separador)
        columnas = reader.fieldnames
        filas = list(reader)

    with open(ruta_destino, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter=separador)
        writer.writeheader()

        for fila in filas:
            writer.writerow(fila)

        for i, registro in enumerate(registros, start=1):
            registro_completo = preparar_fn(registro, ruta_origen, columnas)
            writer.writerow(registro_completo)

    registrar_operacion(nombre_dataset, "INSERT", len(registros))
    # Si se ingresaron registros válidos se registra la operación con éxito indicando la cantidad de registros insertados
