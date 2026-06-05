from utils import manejar_archivo_no_encontrado
from validador import es_coordenada_valida, validar_y_convertir_fecha
from datetime import datetime
import csv


@manejar_archivo_no_encontrado
def ejecutar_analisis_calidad(ruta_archivo, separador, col_lat ="decimalLatitude", col_lon ="decimalLongitude"):

    #Se inicializan los registros
    coordenada_invalida = []
    coordenada_incompleta = []
    fecha_invalida = []
    taxonomia_invalida = []
    ids_duplicados = set()
    ids_totales = set()

    #Se incializa contador de filas
    cont = 0   
    with open(ruta_archivo, "r", encoding = "utf-8", newline="") as archivo:
        csv_reader = csv.DictReader(archivo, delimiter = separador)

        for fila in csv_reader:

            #Se inicializa el conteo de filas
            cont += 1

            #Se valida por taxonomia:
            taxonomia = fila.get("scientificName","").strip()
            if not taxonomia:
                taxonomia_invalida.append(fila)

            #Se evaluan las coordenadas
            lon = (fila.get(col_lon,"")).strip()
            lat = (fila.get(col_lat,"")).strip()
            if (lat and lon):
                lat_valida = es_coordenada_valida(lat, -90, 90)
                lon_valida = es_coordenada_valida(lon, -180, 180)
                if not (lat_valida and lon_valida):
                    coordenada_invalida.append(fila)
            elif (lat and not lon) or (lon and not lat):
                coordenada_incompleta.append(fila)
                    
            #Se evaluan las fechas(deltipo "2015-06-23T00:00:00Z")
            fecha_str = (fila.get("eventDate","")).strip()[:10]
            if fecha_str:
                es_valida, fecha = validar_y_convertir_fecha(fecha_str)
                if not es_valida:
                    fecha_invalida.append(fila)
                elif datetime.now() < fecha: 
                    fecha_invalida.append(fila)
                
            #Se evalua la duplicidad de los IDs
            registro_id = fila.get("occurrenceID","").strip()
            if registro_id: # Evita procesar IDs vacíos
                if registro_id in ids_totales:
                    ids_duplicados.add(registro_id)
                else:
                    ids_totales.add(registro_id)

    #Este bloque imprime los resultados
    print(f"Total de filas: ", cont)
    print(f"Cantidad de IDs duplicados: ", len(ids_duplicados))
    print(f"Cantidad de filas con fecha inválida: ", len(fecha_invalida))
    print(f"Cantidad de filas con taxonomia inválida: ", len(taxonomia_invalida))
    print(f"Cantidad de filas con coordenadas inválidas", len(coordenada_invalida))
    print(f"Cantidad de filas con coordenadas incompletas: ", len(coordenada_incompleta))
    
    return {"idDuplicado":ids_duplicados,
            "fechaInvalida":fecha_invalida,
            "taxonomiaInvalida":taxonomia_invalida,
            "coordenadaInvalida":coordenada_invalida}