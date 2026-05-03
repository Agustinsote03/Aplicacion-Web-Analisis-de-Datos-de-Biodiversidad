import csv
from pathlib import Path
from validador import *
from logger import registrar_operacion

#-----------------FUNCIONES AUXILIARES---------------------#
#Se ingresa un nuevo registro por teclado solicitando al usuario los campos principales del dataset 
def ingresar_registro_por_teclado():
    print("Ingrese los datos del nuevo registro:")

    #Pido los campos principales del dataset al usuario
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

    #Uso la función de creación de estructura para generar un nuevo registro con los datos ingresados
    registro = crear_estructura_registro(
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

#---------------------FUNCIONES PRINCIPALES---------------------#

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
FORMATO_FECHA = "%Y-%m-%d"

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
                f"Formato esperado: {FORMATO_FECHA} (ej: 2024-03-15)"
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
    status = registro.get("occurrenceStatus", "").strip()
    valores_validos_status = {"PRESENT", "ABSENT"}
    if status != "" and status.upper() not in valores_validos_status:
        errores.append(
            f"occurrenceStatus inválido: '{status}' "
            f"Valores permitidos: {valores_validos_status} "
        )

    es_valido = len(errores) == 0
    return es_valido, errores


# Recorre el dataset y retorna el mayor catalogNumber encontrado
def max_catalog_number(ruta_archivo):
    max_num = 0
    with open(ruta_archivo, "r", encoding = "utf-8", newline = "") as f:
        reader = csv.DictReader(f, delimiter = "\t")
        for fila in reader:
            catalog = fila.get("catalogNumber", "").strip()
            if catalog.isdigit():
                num = int(catalog)
                if num > max_num:
                    max_num = num
    return max_num


# Recibe estructura del inciso 4.A y retorna un diccionario listo para añadir al CSV
def preparar_estructura(registro, ruta_archivo, columnas, nombre_dataset):
    max_num = max_catalog_number(ruta_archivo)
    nuevo_num = max_num + 1
    
    # Se usa zfill para rellenar el número con ceros a la izquierda respetando el patrón de ocurrenceID
    nuevo_catalog = str(nuevo_num).zfill(6) # Lo rellena hasta tener 6 dígitos
    nuevo_occurrence_id = f"{nombre_dataset}:COI:{nuevo_catalog}"

    # Se arma el registro completo con todas las columnas del dataset
    registro_completo = {col: "" for col in columnas}    

    # Se copian los campos del registro recibido
    for campo, valor in registro.items():
        if campo in registro_completo:
            registro_completo[campo] = valor
    
    # Se setean los IDs
    registro_completo["gbifID"] = "" # Asignado externamente por GBIF
    registro_completo["occurrenceID"] = nuevo_occurrence_id
    registro_completo["catalogNumber"] = nuevo_catalog

    return registro_completo

#Inserta un nuevo registro correctamente formateado al final del dataset conservando la estructura original 
def insertar_registro(ruta_origen, ruta_destino, registro, nombre_dataset):

    #Valida el registro antes de intentar insertarlo, mostrando los errores encontrados si no es válido
    es_valido, errores = validar_registro(registro)

    if not es_valido:
        print("Registro inválido. No se insertó.")
        for e in errores:
            print("-", e)
        return  #Corta la función si hay errores
    
    #Abre el dataset original en modo lectura
    with open(ruta_origen, "r", encoding="utf-8", newline="") as f_in:

        reader = csv.DictReader(f_in, delimiter="\t")
        columnas = reader.fieldnames
        #Guarda el nombre de las columnas

        #Genera el registro listo para insertar, asignando un nuevo catalogNumber y occurrenceID
        registro_completo = preparar_estructura(registro, ruta_origen, columnas, nombre_dataset)

        #Abre el archivo destino en modo escritura y copia el contenido del original, luego agrega el nuevo registro
        with open(ruta_destino, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter="\t")

            writer.writeheader()
            #Escribe la primera fila (nombre de columnas)

            #Copia todas las filas del dataset original
            for fila in reader:
                writer.writerow(fila)

            #Agrega el nuevo registro al final del archivo
            writer.writerow(registro_completo)

    print("Registro insertado correctamente")

    registrar_operacion(nombre_dataset, "INSERT", 1)

#Función para insertar múltiples registros ingresados por teclado
def insertar_multiples_registros(ruta_origen, ruta_destino, nombre_dataset):

    registros = []
    #Lista donde se guardarán los registros válidos

    print("Carga de múltiples registros (dejar vacío 'scientificName' para terminar)")

    #Loop para ingresar varios registros por teclado
    while True:
        registro = ingresar_registro_por_teclado()
        #Pide datos al usuario para crear un nuevo registro

        #Condición de corte, si no se escribe scientificName se termina la carga de registros
        if registro.get("license", "") == "":
            break
        
        #Valida cada registro ingresado
        es_valido, errores = validar_registro(registro)

        if es_valido:
            registros.append(registro)
            print("Registro agregado\n")
            #Si es válido se agrega a la lista de registros
        else:
            print("Registro inválido:")
            for e in errores:
                print("-", e)
                #Si no es válido se muestran los errores y no se agrega a la lista
            print()

    #Si no se ingresó ningún registro válido se termina la función
    if not registros:
        print("No se ingresaron registros válidos")
        return

    #Abrimos dataset original
    with open(ruta_origen, "r", encoding="utf-8", newline="") as f_in:

        reader = csv.DictReader(f_in, delimiter="\t")
        columnas = reader.fieldnames
        #Nombre de las columnas del dataset

        filas = list(reader)  
        #Guardamos todas las filas originales en memoria

    max_num = max_catalog_number(ruta_origen)
    #Calculo el último catalogNumber una sola vez para luego asignar nuevos números a los registros ingresados, evitando recorrer el dataset repetidamente

    #Creo el nuevo archivo
    with open(ruta_destino, "w", encoding="utf-8", newline="") as f_out:

        writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter="\t")
        writer.writeheader()
        #Escribo los encabezados del dataset

        for fila in filas:
            writer.writerow(fila)
            #Copio el dataset original al nuevo archivo

        #Agrego los nuevos registros al final del archivo
        for i, registro in enumerate(registros, start=1):

            #Genero nuevos IDs para cada registro sin repetir
            nuevo_num = max_num + i
            nuevo_catalog = str(nuevo_num).zfill(6)
            nuevo_occurrence_id = f"{nombre_dataset}:COI:{nuevo_catalog}"

            registro_completo = {col: "" for col in columnas}
            #Creo estructura completa con todas las columnas del dataset

            for campo, valor in registro.items():
                if campo in registro_completo:
                    registro_completo[campo] = valor
                #Copio los datos del usuario

            registro_completo["gbifID"] = ""
            registro_completo["occurrenceID"] = nuevo_occurrence_id
            registro_completo["catalogNumber"] = nuevo_catalog
            #Seteo los IDs para cada registro

            writer.writerow(registro_completo)
            #Escribo el registro en el nuevo archivo

    print("Registros insertados correctamente")

    registrar_operacion(nombre_dataset, "INSERT", len(registros))