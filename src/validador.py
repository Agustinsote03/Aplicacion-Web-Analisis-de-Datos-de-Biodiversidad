import csv
from utils import cantidad_registros
from datetime import datetime

# Cotas aproximadas de América del Sur
LAT_MIN= -56.0
LAT_MAX= 13.0
LON_MIN= -82.0
LON_MAX = -35.0
#------------------------------------------Funciones auxiliares---------------------------------------#

def es_coordenada_valida(valor, limite_min, limite_max):
    """
    Retorna True si el valor puede convertirse a número y está dentro del rango dado.
    """
    # Quitamos espacios en blanco
    valor = valor.strip()
    # Si está vacío se retorna False directamente
    if not valor:
        return False   
    # Se convierte  en float() para comparar
    numero = float(valor)
    es_valida = limite_min <= numero <= limite_max

    return es_valida

def es_fecha_valida(fecha_str, formato):
    """
    Valida si un string puede convertirse a fecha segun el formato dado
    """

    # Usa try/except porque datetime.strptime muestra ValueError si falla
    try:
        fecha = datetime.strptime(fecha_str, formato)
        # Convierte el string a objeto datetime si el formato es correcto 
        return True, fecha
    
    except ValueError:
    # Ocurre si el formato es incorrecto o la fecha es invalida
        return False, None

def es_incertidumbre_valida(incertidumbre_str):
    """
    Retorna True si el valor es un número entre 0 y 100.
    """
    try:
        # Se intenta convertir a decimal
        incertidumbre_float = float(incertidumbre_str)

        # Se evalúan rangos: si es negativo o mayor a 100, es inválida(retorna False)
        if incertidumbre_float < 0 or incertidumbre_float > 100:
            return False
            
        return True
        
    except ValueError:
        # Si el valor no es numérico, también es inválido
        return False
#------------------------------------------Funciones principales---------------------------------------#

def validar_coordenadas(ruta_archivo, separador,  col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Recorre el dataset y retorna la cantidad y lista de registros con coordenadas inválidas.
    """
    # Se inicializa una lista que contendrá los registros inválidos
    registros_invalidos = []
    cont = 0
    with open(ruta_archivo, "r", encoding = "utf-8", newline= "") as file_csv:
        csv_reader = csv.DictReader(file_csv, delimiter=separador)
        
        # Se recorre cada fila del archivo

        for fila in csv_reader:
            # Extreamos la latitud y longitud
            lat = fila.get(col_lat, " ")
            lon = fila.get(col_lon, " ")
            
            # Validación de coordenadas
            lat_valida = es_coordenada_valida(lat, -90, 90)
            lon_valida = es_coordenada_valida(lon, -180, 180)

            # Si 'es_coordenada_valida' devuelve false, se agrega a 'registros_invalidos'
            if not lat_valida or not lon_valida:
                registros_invalidos.append(fila)
        
        return len(registros_invalidos), registros_invalidos

def detectar_coordenadas_incompletas(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Retorna la cantidad y lista de registros que tienen solo latitud o solo longitud, pero no ambas.
    """
    registros = []
    with open(ruta_archivo, "r", encoding = "utf-8", newline = "") as file_csv:
             csv_reader = csv.DictReader(file_csv, delimiter=separador)

             for fila in csv_reader:
                # if not (fila.get("decimalLatitude", "")).strip() or not (fila.get("decimalLongitude", "")).strip(): registros.append(fila)
                lon = (fila.get(col_lon,"")).strip()
                lat = (fila.get(col_lat,"")).strip()

                if (lat and not lon) or (lon and not lat):
                    registros.append(fila)
    return len(registros), registros

def validar_fechas(ruta_archivo, nombre_columna, separador="\t"):
    """
    Retorna la cantidad y lista de registros con fechas vacías, con formato inválido o futuras.
    """
    registros_invalidos = []
    
    formato = "%d/%m/%y"
    # Defino el formato esperado de las fechas (dia/mes/año)

    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            fecha_str = (fila.get(nombre_columna, "")).strip()
            # Se usa get para evitar errores si la columna no existe

            if not fecha_str:
                registros_invalidos.append(fila)
                continue
                # Si el campo de fecha está vacío, se considera inválido

            es_valida, fecha = es_fecha_valida(fecha_str, formato)
            # Uso de la funcio¿ón auxiliar
            
            if not es_valida:
                registros_invalidos.append(fila)
                # Para los formatos inválidos o fechas imposibles

            elif fecha > datetime.now():
                registros_invalidos.append(fila)
                # Si la fecha es futura, se considera inválida

    return len(registros_invalidos), registros_invalidos

def detectar_duplicados(ruta_archivo, separador="\t", col_id="occurrenceID"):
    """
    Retorna la cantidad y conjunto de IDs que aparecen más de una vez en el dataset.
    """
    ids_duplicados = set()
    ids_totales = set()
    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            registro_id = fila.get(col_id,"").strip()

            # Si existe el id, se añade a uno de los dos conjuntos
            if registro_id:

                if registro_id in ids_totales:
                    ids_duplicados.add(registro_id)
                else:
                    ids_totales.add(registro_id)

    return len(ids_duplicados), ids_duplicados

def detectar_country_codes_invalidos(ruta_archivo, separador):
    """
    Retorna la cantidad y lista de registros cuyo countryCode no pertenece a la lista de códigos válidos.
    """
    codigos_validos = {"AR", "CL", "BR", "UY", "PY", "BO", "PE", "EC", "CO", "VE"}
    registros_invalidos = []

    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=separador)

            for fila in csv_reader:
                # Se normaliza el código
                codigo = fila.get("countryCode", "").strip().upper()

                if codigo not in codigos_validos:
                    registros_invalidos.append(fila)
            
            return len(registros_invalidos), registros_invalidos
        
def detectar_incertidumbres_invalidas(ruta_archivo, separador):
    """
    Retorna la cantidad y lista de registros con coordinateUncertaintyInMeters inválida.
    """
    registros_invalidos = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)

        for fila in csv_reader:
            # Se normaliza el valor
            incertidumbre_str = fila.get("coordinateUncertaintyInMeters", "").strip()
            if not es_incertidumbre_valida(incertidumbre_str):
                registros_invalidos.append(fila)

    return len(registros_invalidos), registros_invalidos


def ejecutar_analisis_calidad(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Recorre el dataset una sola vez y detecta todos los problemas de calidad: coordenadas inválidas o incompletas, fechas inválidas, taxonomía vacía e IDs duplicados.
    Imprime un resumen por pantalla y retorna un diccionario con los registros problemáticos por categoría.
    """
    # Se inicializan los registros
    coordenada_invalida = []
    coordenada_incompleta = []
    fecha_invalida = []
    taxonomia_invalida = []
    ids_duplicados = set()
    ids_totales = set()

    # Se incializa contador de filas
    cont = 0
    # Formato esperado de las fechas
    formato = "%Y-%m-%d"

    with open(ruta_archivo, "r", encoding = "utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter = separador)

        for fila in csv_reader:

            # Se inicializa el conteo de filas
            cont += 1

            # Se valida por taxonomia:
            taxonomia = fila.get("scientificName","").strip()
            if not taxonomia:
                taxonomia_invalida.append(fila)

            # Se evaluan las coordenadas
            lon = (fila.get(col_lon,"")).strip()
            lat = (fila.get(col_lat,"")).strip()
            if (lat and lon):
                lat_valida = es_coordenada_valida(lat, -90, 90)
                lon_valida = es_coordenada_valida(lon, -180, 180)
                if not (lat_valida and lon_valida):
                    coordenada_invalida.append(fila)
            elif (lat and not lon) or (lon and not lat):
                coordenada_incompleta.append(fila)
                
            # Se evaluan las fechas(deltipo "2015-06-23T00:00:00Z")
            fecha_str = (fila.get("eventDate","")).strip()[:10]
            if fecha_str:
                es_valida, fecha = es_fecha_valida(fecha_str, formato)
                if not es_valida:
                    fecha_invalida.append(fila)
                elif datetime.now() < fecha: 
                    fecha_invalida.append(fila)
            
            # Se evalua la duplicidad de los IDs
            registro_id = fila.get("occurrenceID","").strip()
            if registro_id: # Evita procesar IDs vacíos
                if registro_id in ids_totales:
                    ids_duplicados.add(registro_id)
                else:
                    ids_totales.add(registro_id)

    # Este bloque imprime los resultados
    print(f"Total de filas: ", cont)
    print(f"Cantidad de IDs duplicados: ", len(ids_duplicados))
    print(f"Cantidad de filas con fecha inválida: ", len(fecha_invalida))
    print(f"Cantidad de filas con taxonomia inválida: ", len(taxonomia_invalida))
    print(f"Cantidad de filas con coordenadas inválidas", len(coordenada_invalida))
    print(f"Cantidad de filas con coordenadas incompletas: ", len(coordenada_incompleta))
    
    return {"idDuplicado":ids_duplicados, "fechaInvalida":fecha_invalida,"taxonomiaInvalida":taxonomia_invalida,"coordenadaInvalida":coordenada_invalida}

def esta_en_territorio(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Retorna la cantidad y lista de registros cuyas coordenadas están fuera del territorio definido por las constantes LAT_MIN, LAT_MAX, LON_MIN, LON_MAX.
    """
    registro_invalido = []

    with open(ruta_archivo, "r", encoding="utf-8",newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        for fila in csv_reader:
            lat = fila.get(col_lat, "")
            lon = fila.get(col_lon, "")

            if lat and lon:
                es_lat_valida = es_coordenada_valida(lat,LAT_MIN,LAT_MAX)
                es_lon_valida = es_coordenada_valida(lon, LON_MIN,LON_MAX)
                if not(es_lat_valida and es_lon_valida):
                    registro_invalido.append(fila)

    return len(registro_invalido), registro_invalido

def validar_latitud(ruta_archivo, separador, col_lat="decimalLatitude"):
    """
     Esta función recibe la latitud, y evalua:
      -Que exista
      -Que sea efectivamente una coordenada
      -Que pertenezca al territorio de América del Sur
    """
    registros_invalido = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        for fila in csv_reader:
            lat = fila.get(col_lat,"")
            if lat:
                es_lat_valida = es_coordenada_valida(lat,-90,90)
                if es_lat_valida:
                    pertenece = es_coordenada_valida(lat,LAT_MIN,LAT_MAX)
                    if not pertenece:
                        registros_invalido.append(fila)
                else:
                    registros_invalido.append(fila)
            else:
                registros_invalido.append(fila)

    return len(registros_invalido), registros_invalido

def validar_longitud(ruta_archivo, separador, col_lon="decimalLongitude"):
    """
     Esta función recibe la latitud, y evalua:
      -Que exista
      -Que sea efectivamente una coordenada
      -Que pertenezca al territorio de América del Sur
    """
    registros_invalido = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        for fila in csv_reader:
            lon = fila.get(col_lon,"")
            if lon:
                es_lon_valida = es_coordenada_valida(lon,-180,180)
                if es_lon_valida:
                    pertenece = es_coordenada_valida(lon,LON_MIN,LON_MAX)
                    if not pertenece:
                        registros_invalido.append(fila)
                else:
                    registros_invalido.append(fila)
            else:
                registros_invalido.append(fila)

    return len(registros_invalido), registros_invalido



