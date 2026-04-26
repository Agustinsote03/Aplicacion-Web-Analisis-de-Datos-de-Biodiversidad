import csv
from datetime import datetime

#------------------------------------------Funciones auxiliares---------------------------------------#

def es_coordenada_valida(valor, limite_min, limite_max):
    #Quitamos espacios en blanco
    valor = valor.strip()
    #Si está vacío se retorna False directamente
    if not valor:
        return False   
    #Se convierte  en float() para comparar
    numero = float(valor)
    es_valida = limite_min <= numero <= limite_max

    return es_valida

#Valida si un string puede convertirse a fecha segun el formato dado
def es_fecha_valida(fecha_str, formato):
    #Usa try/except porque datetime.strptime muestra ValueError si falla
    try:
        fecha = datetime.strptime(fecha_str, formato)
        #Convierte el string a objeto datetime si el formato es correcto 
        return True, fecha
    
    except ValueError:
    #Ocurre si el formato es incorrecto o la fecha es invalida
        return False, None

def es_incertidumbre_valida(incertidumbre_str):
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

def validar_coordenadas(ruta_archivo, separador):

    #Se inicializa una lista que contendrá los registros inválidos
    registros_invalidos = []
    with open(ruta_archivo, "r", encoding = "utf-8", newline= "") as file_csv:
        csv_reader = csv.DictReader(file_csv, delimiter=separador)
        
        #Se recorre cada fila del archivo

        for fila in csv_reader:
            #Extreamos la latitud y longitud
            lat = fila.get("decimalLatitude", " ")
            lon = fila.get("decimalLongitude", " ")
            
            #Validación de coordenadas
            lat_valida = es_coordenada_valida(lat, -90, 90)
            lon_valida = es_coordenada_valida(lon, -100, 180)

            #Si 'es_coordenada_valida' devuelve false, se agrega a 'registros_invalidos'
            if not lat_valida or not lon_valida:
                registros_invalidos.append(fila)
        
        return len(registros_invalidos), registros_invalidos

def detectar_coordenadas_incompletas(ruta_archivo, separador):
        
        registros = []
        with open(ruta_archivo, "r", encoding = "utf-8", newline = "") as file_csv:
             csv_reader = csv.DictReader(file_csv, delimiter=separador)

             for fila in csv_reader:
                # if not (fila.get("decimalLatitude", "")).strip() or not (fila.get("decimalLongitude", "")).strip(): registros.append(fila)
                lon = (fila.get("decimalLongitude","")).strip()
                lat = (fila.get("decimalLatitude","")).strip()

                if (lat and not lon) or (lon and not lat):
                    registros.append(fila)
        return len(registros), registros

def validar_fechas(ruta_archivo, nombre_columna, separador="\t"):
    
    registros_invalidos = []
    
    formato = "%d/%m/%y"
    #Defino el formato esperado de las fechas (dia/mes/año)

    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            fecha_str = (fila.get(nombre_columna, "")).strip()
            #Se usa get para evitar errores si la columna no existe

            if not fecha_str:
                registros_invalidos.append(fila)
                continue
                #Si el campo de fecha está vacío, se considera inválido

            es_valida, fecha = es_fecha_valida(fecha_str, formato)
            #Uso de la funcio¿ón auxiliar
            
            if not es_valida:
                registros_invalidos.append(fila)
                #Para los formatos inválidos o fechas imposibles

            elif fecha > datetime.now():
                registros_invalidos.append(fila)
                #Si la fecha es futura, se considera inválida

    return len(registros_invalidos), registros_invalidos

def detectar_duplicados(ruta_archivo, nombre_columbna, separador="\t"):
    ids_duplicados = set()
    ids_totales = set()
    with open(ruta_archivo, encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo, delimiter=separador)

        for fila in reader:
            registro_id = fila.get("occurrenceID","").strip()

            #Si existe el id, se añade a uno de los dos conjuntos
            if registro_id:

                if registro_id in ids_totales:
                    ids_duplicados.add(registro_id)
                else:
                    ids_totales.add(registro_id)

    return len(ids_duplicados), ids_duplicados

def detectar_country_codes_invalidos(ruta_archivo, separador):
        codigos_validos = {"AR", "CL", "BR", "UY", "PY", "BO", "PE", "EC", "CO", "VE"}
        registros_invalidos = []

        with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=separador)

            for fila in csv_reader:
                #Se normaliza el código
                codigo = fila.get("countryCode", "").strip().upper()

                if codigo not in codigos_validos:
                    registros_invalidos.append(fila)
            
            return len(registros_invalidos), registros_invalidos
        
def detectar_incertidumbres_invalidas(ruta_archivo, separador):
        
    registros_invalidos = []
    with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter=separador)

        for fila in csv_reader:
            #Se normaliza el valor
            incertidumbre_str = fila.get("coordinateUncertaintyInMeters", "").strip()
            if not es_incertidumbre_valida(incertidumbre_str):
                registros_invalidos.append(fila)

    return len(registros_invalidos), registros_invalidos
