from datetime import datetime
from pathlib import Path

#Ruta del nuevo archivo log
ruta_log = Path(__file__).resolve().parent.parent / "logs" / "operations.log"

def obtener_fecha_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#Escribe una entrada en el archivo operations.log, si no existe el archivo y la carpeta los crea
def registrar_operacion(nombre_dataset, tipo_operacion, cantidad_registros, error=False):
    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    fecha_hora = obtener_fecha_hora()
    linea = f"{fecha_hora} | {nombre_dataset} | {tipo_operacion} | {cantidad_registros} registros"

    if error:
        linea += " | ERROR"

    with open(ruta_log, "a", encoding="utf-8") as log:
        log.write(linea + "\n")