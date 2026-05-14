import csv
from pathlib import Path
from datetime import datetime
from validador import (es_coordenada_valida, es_fecha_valida, es_incertidumbre_valida)
from logger import registrar_operacion

def eliminar_por_id(ruta_original, ruta_nueva, columna, valor, nombre_dataset, separador="\t"):
    """
    Elimina del dataset el registro que coincida con el valor indicado en la columna dada.
    """
    eliminado = False

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        # Lee el dataset
        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:

            # Busca el occurrenceID
            if str(fila.get(columna, "")).strip() == str(valor).strip():
                eliminado = True
                # Elimina la fila correctamente
                continue  

            escritor.writerow(fila)

    #Detecta si no encontro nada
    if not eliminado:
        print("Error: no se encontró el registro")

    if eliminado:
        registrar_operacion(nombre_dataset, "DELETE", 1)
    else:
        registrar_operacion(nombre_dataset, "DELETE", 0, error=True)
    #Si se elimino algun registro se registra la operacion, sino se registra un error

    return eliminado


def eliminar_por_lista(ruta_original, ruta_nueva, columna, valores_a_eliminar, nombre_dataset, separador="\t"):
    """
    Elimina todos los registros cuyo valor en la columna indicada pertenezca a la lista dada.
    """
    eliminados = 0

    # normalizo la lista (por si viene con espacios)
    valores_a_eliminar = [str(v).strip() for v in valores_a_eliminar]

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        for fila in lector:

            valor = str(fila.get(columna, "")).strip()

            # si está en la lista lo elimino (no escribo)
            if valor in valores_a_eliminar:
                eliminados += 1
                continue

            escritor.writerow(fila)

    if eliminados == 0:
        print("No se eliminaron registros")
        registrar_operacion(nombre_dataset, "DELETE", 0, error=True)
    else:
        registrar_operacion(nombre_dataset, "DELETE", eliminados)
    #Si se elimino algun registro se registra la operación, sino se registra un error
    
    return eliminados


def eliminar_por_condicion(ruta_original, ruta_nueva, columna, operador, valor, nombre_dataset, separador="\t"):
    """
    Elimina todos los registros que cumplan la condición indicada sobre una columna.
    Soporta los operadores ==, !=, >, >=, <, <=.
    """
    eliminados = 0

    # Abrimos archivo original (lectura) y nuevo (escritura)
    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:

        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)

        escritor.writeheader()

        # Recorremos todas las filas del dataset
        for fila in lector:
            # Obtenemos el valor de la columna indicada
            dato = fila.get(columna, "").strip()

            # Intentamos convertir a número (por si es year, cantidad, etc.)
            try:
                dato_val = float(dato)
                valor_val = float(valor)
            except:
                # Si no se puede convertir, lo tratamos como texto
                dato_val = dato
                valor_val = valor

            cumple = False # Asumimos que NO cumple la condicion

            # Evaluamos la condicion segun el operador
            if operador == "==":
                cumple = dato_val == valor_val
            elif operador == "!=":
                cumple = dato_val != valor_val
            elif operador == ">":
                cumple = dato_val > valor_val
            elif operador == ">=":
                cumple = dato_val >= valor_val
            elif operador == "<":
                cumple = dato_val < valor_val
            elif operador == "<=":
                cumple = dato_val <= valor_val

            # Si cumple eliminamos la fila 
            if cumple:
                eliminados += 1
                continue
            
            # Si no cumple la condicion, conservamos la fila
            escritor.writerow(fila)

    if eliminados == 0:
        print("No se eliminaron registros")
        registrar_operacion(nombre_dataset, "DELETE", 0, error=True)
    else:
        registrar_operacion(nombre_dataset, "DELETE", eliminados)

    return eliminados


def validar_fila(fila):
    """
    Valida los campos de una fila del dataset y retorna una lista con los motivos de invalidez.
    Si la lista está vacía, la fila es válida.
    """
    codigos_pais_validos = {"AR","CL","BR","UY","PY","BO","PE","EC","CO","VE"}
    formato_fecha = "%Y-%m-%d"
    
    motivos = []

    #Validar latitud
    lat = fila.get("decimalLatitude", "").strip()
    if lat and not es_coordenada_valida(lat, -90, 90):
        motivos.append("latitud inválida")

    #Validar longitud
    lon = fila.get("decimalLongitude", "").strip()
    if lon and not es_coordenada_valida(lon, -180, 180):
        motivos.append("longitud inválida")

    #Validar que no haya coordenada incompleta
    if (lat and not lon) or (lon and not lat):
        motivos.append("coordenada incompleta")

    #Validar fecha
    fecha_str = fila.get("eventDate", "").strip()[:10]
    if fecha_str:
        es_valida, fecha = es_fecha_valida(fecha_str, formato_fecha)
        if not es_valida:
            motivos.append("fecha inválida")
        elif fecha and fecha > datetime.now():
            motivos.append("fecha futura")

    #Validar countryCode
    country_code = fila.get("countryCode", "").strip().upper()
    if country_code and country_code not in codigos_pais_validos:
        motivos.append(f"countryCode inválido: {country_code}")

    #Validar incertidumbre de coordenada
    incertidumbre = fila.get("coordinateUncertaintyInMeters", "").strip()
    if incertidumbre and not es_incertidumbre_valida(incertidumbre):
        motivos.append("coordinateUncertaintyInMeters inválida")

    #Validar nombre científico
    if not fila.get("scientificName", "").strip():
        motivos.append("scientificName vacío")

    return motivos


def sanitizar_dataset(ruta_original, ruta_nueva, separador="\t"):
    """
    Recorre el dataset, elimina las filas inválidas y guarda el resultado en un nuevo archivo.
    Retorna un resumen con el total de registros, los eliminados y los motivos.
    """
    eliminados = 0
    total = 0
    motivos_conteo = {}

    Path(ruta_nueva).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
 
        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)
 
        escritor.writeheader()

        for fila in lector:
            total += 1
            motivos = validar_fila(fila)

            if motivos:
                eliminados += 1
                for motivo in motivos:
                    motivos_conteo[motivo] = motivos_conteo.get(motivo, 0) + 1
                continue

            escritor.writerow(fila)

    return {
        "total": total,
        "eliminados": eliminados,
        "motivos": motivos_conteo,
    }


def sanitizar_dataset_evolucionada(ruta_original, ruta_nueva, separador="\t"):
    """
    Igual que sanitizar_dataset pero además muestra un reporte detallado por pantalla
    e incluye el ID de cada registro eliminado y sus motivos en el resultado.
    """
    eliminados = 0
    total = 0
    reporte_detallado = []
    motivos_conteo = {}

    Path(ruta_nueva).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_original, "r", encoding="utf-8", newline="") as archivo_original, \
         open(ruta_nueva, "w", encoding="utf-8", newline="") as archivo_nuevo:
 
        lector = csv.DictReader(archivo_original, delimiter=separador)
        escritor = csv.DictWriter(archivo_nuevo, fieldnames=lector.fieldnames, delimiter=separador)
 
        escritor.writeheader()

        for fila in lector:
            total += 1
            motivos = validar_fila(fila)

            if motivos:
                eliminados += 1
                for motivo in motivos:
                    motivos_conteo[motivo] = motivos_conteo.get(motivo, 0) + 1
                reporte_detallado.append({
                    "occurrenceID": fila.get("occurrenceID", ""),
                    "motivos": motivos,
                })
                continue

            escritor.writerow(fila)

    porcentaje = (eliminados / total * 100) if total > 0 else 0

    print(f"\n----Reporte de sanitización----")
    print(f"Total de registros: {total}")
    print(f"Registros eliminados: {eliminados}")
    print(f"Porcentaje eliminado: {porcentaje:.2f}%") #porcentaje:.2f solo muestra dos decimales
    print(f"\nMotivos de eliminación:")
    for motivo, cantidad in motivos_conteo.items():
        print(f"  - {motivo}: {cantidad} registros")

    return {
        "total": total,
        "eliminados": eliminados,
        "porcentaje": round(porcentaje, 2),
        "motivos_conteo": motivos_conteo,
        "detalle": reporte_detallado,
    }
