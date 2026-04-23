import csv

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
                

