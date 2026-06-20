import pandas as pd

def leer_logs(ruta_log):
    """
    Lee el archivo de logs de operaciones y retorna una lista de diccionarios,
    uno por línea válida del log. Retorna None si el archivo no existe.
    """
    registros = []
    try:
        with open(ruta_log, "r", encoding="utf-8") as f:
            for linea in f:
                partes = [p.strip() for p in linea.split("|")]
                if len(partes) < 4:
                    continue

                estado = "ERROR" if "ERROR" in linea else "OK"

                registros.append({
                    "Fecha": partes[0],
                    "Dataset": partes[1],
                    "Operación": partes[2],
                    "Registros": partes[3],
                    "Estado": estado
                })
    except FileNotFoundError:
        return None

    return registros


def limpiar_logs(logs):
    """
    Convierte la lista de logs en DataFrame, parsea las fechas y separa
    las filas con formato de fecha corrupto.
    Retorna una tupla (df_logs_limpio, cantidad_de_filas_corruptas).
    """
    df_logs = pd.DataFrame(logs)
    df_logs["Fecha_parsed"] = pd.to_datetime(df_logs["Fecha"], errors="coerce")

    cantidad_corruptos = df_logs["Fecha_parsed"].isna().sum()
    df_logs = df_logs.dropna(subset=["Fecha_parsed"])

    return df_logs, cantidad_corruptos