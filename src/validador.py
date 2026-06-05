import csv
from utils import cantidad_registros, manejar_archivo_no_encontrado
from datetime import datetime

#Cotas aproximadas de América del Sur
LAT_MIN= -56.0
LAT_MAX= 13.0
LON_MIN= -82.0
LON_MAX = -35.0

#Mapa de códigos de países válidos en América del Sur 
codigos_validos = {"AR", "CL", "BR", "UY", "PY", "BO", "PE", "EC", "CO", "VE"}

#Formato de fechas esperado
formato = "%Y-%m-%d"
#------------------------------------------Funciones auxiliares---------------------------------------#

def es_coordenada_valida(valor, limite_min, limite_max):
    """
        Valida si un valor de coordenada es numérico y está dentro de los límites especificados.
        Retorna True si es válido, False si no lo es.
    """
    try:
        #Quitamos espacios en blanco
        valor = valor.strip()
        #Si está vacío se retorna False directamente
        if not valor:
            return False   
        #Se convierte  en float() para comparar
        numero = float(valor)
        es_valida = limite_min <= numero <= limite_max
    except ValueError:
        es_valida = False

    return es_valida

#Valida si un string puede convertirse a fecha segun el formato dado
def validar_y_convertir_fecha(fecha_str):
    """
    Valida si un string de fecha es correcto según el formato esperado y lo convierte a un objeto datetime.
    Retorna una tupla (es_valida, fecha) donde es_valida es True o False, y fecha es el objeto datetime si es válida o None si no lo es.
    """
    #Usa try/except porque datetime.strptime muestra ValueError si falla
    try:
        fecha = datetime.strptime(fecha_str, formato)
        #Convierte el string a objeto datetime si el formato es correcto 
        return True, fecha
    
    except ValueError:
    #Ocurre si el formato es incorrecto o la fecha es invalida
        return False, None

def es_incertidumbre_valida(incertidumbre_str):
    """
    Valida si el valor de coordinateUncertaintyInMeters es un número entre 0 y 100.
    Retorna True si es válido, False si no lo es.
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

@manejar_archivo_no_encontrado
def validar_coordenadas(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Valida que los campos de latitud y longitud sean numéricos y estén dentro de los rangos geográficos válidos.
    Retorna la cantidad de registros con coordenadas inválidas y una lista de esos registros.
    """

    #Se inicializa una lista que contendrá los registros inválidos
    registros_invalidos = []
    
    with open(ruta_archivo, "r", encoding = "utf-8", newline= "") as file_csv:
        csv_reader = csv.DictReader(file_csv, delimiter=separador)
        
        #Se recorre cada fila del archivo

        for fila in csv_reader:
            lat = fila.get(col_lat, "") or fila.get("latitudeDecimal", "")
            lon = fila.get(col_lon, "") or fila.get("longitudeDecimal", "")
            
            lat_valida = es_coordenada_valida(lat, -90, 90)
            lon_valida = es_coordenada_valida(lon, -180, 180)
            
            #Si 'es_coordenada_valida' devuelve false, se agrega a 'registros_invalidos'
            if not lat_valida or not lon_valida:
                registros_invalidos.append(fila)
        
    return len(registros_invalidos), registros_invalidos

@manejar_archivo_no_encontrado
def detectar_coordenadas_incompletas(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"):
    """
    Detecta registros que tienen una coordenada (latitud o longitud) pero no la otra
    Retorna la cantidad de registros con coordenadas incompletas y una lista de esos registros.
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

@manejar_archivo_no_encontrado
def validar_fechas(ruta_archivo, nombre_columna, separador="\t", formato="%Y-%m-%d", contar_vacios=False):
    """
    Valida que los campos de fecha sean correctos según el formato esperado y no sean futuras.
    Retorna la cantidad de registros con fechas inválidas y una lista de esos registros.
    """
    
    registros_invalidos = []

    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            fecha_str = (fila.get(nombre_columna, "")).strip()[:10]
            # Tomamos solo los primeros 10 caracteres (YYYY-MM-DD)

            if not fecha_str:
                if contar_vacios:
                    registros_invalidos.append(fila)
                continue
                #Si la fecha está vacía, se cuenta como inválida solo si contar_vacios es True

            es_valida, fecha = validar_y_convertir_fecha(fecha_str)
            #Uso de la función auxiliar
            
            if not es_valida:
                registros_invalidos.append(fila)
                #Para los formatos inválidos o fechas imposibles

            elif fecha > datetime.now():
                registros_invalidos.append(fila)
                #Si la fecha es futura, se considera inválida

    return len(registros_invalidos), registros_invalidos

@manejar_archivo_no_encontrado
def detectar_duplicados(ruta_archivo, nombre_columna, separador="\t"):
    """
    Detecta registros con IDs duplicados en la columna especificada.
    Retorna la cantidad de IDs duplicados y un conjunto con esos IDs.
    """
    ids_duplicados = set()
    ids_totales = set()
    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            registro_id = fila.get(nombre_columna,"").strip()

            #Si existe el id, se añade a uno de los dos conjuntos
            if registro_id:

                if registro_id in ids_totales:
                    ids_duplicados.add(registro_id)
                else:
                    ids_totales.add(registro_id)

    return len(ids_duplicados), ids_duplicados

@manejar_archivo_no_encontrado
def detectar_country_codes_invalidos(ruta_archivo, separador):
    """
    Valida que los códigos de país en la columna 'countryCode' sean válidos según el conjunto de códigos definidos para América del Sur.
    Retorna la cantidad de registros con códigos de país inválidos y una lista de esos registros
    """
    registros_invalidos = []

    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)

        for fila in csv_reader:
            #Se normaliza el código
            codigo = fila.get("countryCode", "").strip().upper()

            if codigo not in codigos_validos:
                registros_invalidos.append(fila)
            
    return len(registros_invalidos), registros_invalidos

@manejar_archivo_no_encontrado     
def detectar_incertidumbres_invalidas(ruta_archivo, separador):  
    """
    Valida que los valores de incertidumbre en la columna 'coordinateUncertaintyInMeters' sean válidos.
    Retorna la cantidad de registros con incertidumbres inválidas y una lista de esos registros.
    """
    registros_invalidos = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)

        for fila in csv_reader:
            #Se normaliza el valor
            incertidumbre_str = fila.get("coordinateUncertaintyInMeters", "").strip()
            if not es_incertidumbre_valida(incertidumbre_str):
                registros_invalidos.append(fila)

    return len(registros_invalidos), registros_invalidos

@manejar_archivo_no_encontrado 
def obtener_registros_fuera_de_territorio(ruta_archivo, separador, col_lat="decimalLatitude", col_lon="decimalLongitude"): 
    """
    Valida que los campos de latitud y longitud se encuentren dentro de las cotas 
    geográficas definidas para América del Sur.
    """
    registros_invalido = []
    
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        
        for fila in csv_reader:
            # Extraemos ambas coordenadas
            lat = fila.get(col_lat, "")
            lon = fila.get(col_lon, "")
            
            # Verificamos que ambas existan 
            if lat and lon:
                # Usamos tu función auxiliar y las constantes globales
                lat_en_sudamerica = es_coordenada_valida(lat, LAT_MIN, LAT_MAX)
                lon_en_sudamerica = es_coordenada_valida(lon, LON_MIN, LON_MAX)
                
                # Si alguna de las dos cae fuera del territorio, el registro es inválido
                if not lat_en_sudamerica or not lon_en_sudamerica:
                    registros_invalido.append(fila)
            else:
                # Si falta alguna de las coordenadas, no se puede ubicar en el mapa
                registros_invalido.append(fila)
                
    return len(registros_invalido), registros_invalido

@manejar_archivo_no_encontrado
def validar_latitud(ruta_archivo, separador, col_lat="decimalLatitude"):
    """
    Agrupa validaciones de latitud: formato (-90 a 90) y pertenencia a Sudamérica.
    Ignora registros sin coordenada (eso lo cubre el ejercicio 3.B).
    """
    registros_invalido = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        for fila in csv_reader:
            lat = fila.get(col_lat, "").strip()
            if lat:
                if not es_coordenada_valida(lat, -90, 90) or not es_coordenada_valida(lat, LAT_MIN, LAT_MAX):
                    registros_invalido.append(fila)

    return len(registros_invalido), registros_invalido


@manejar_archivo_no_encontrado
def validar_longitud(ruta_archivo, separador, col_lon="decimalLongitude"):
    """
    Agrupa validaciones de longitud: formato (-180 a 180) y pertenencia a Sudamérica.
    Ignora registros sin coordenada (eso lo cubre el ejercicio 3.B).
    """
    registros_invalido = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)
        for fila in csv_reader:
            lon = fila.get(col_lon, "").strip()
            if lon:
                if not es_coordenada_valida(lon, -180, 180) or not es_coordenada_valida(lon, LON_MIN, LON_MAX):
                    registros_invalido.append(fila)
    return len(registros_invalido), registros_invalido
