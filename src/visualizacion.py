import pandas as pd
from validador import validar_coordenadas, validar_fechas
from utils import calcular_porcentaje_nulos_logica


def calcular_metricas_dataset(ruta_archivo, nombre_dataset, separador="\t"):
    """
    Calcula las métricas de calidad de un dataset: total de registros,
    % de coordenadas válidas, % de fechas válidas y % de completitud promedio.
    """
    df = pd.read_csv(ruta_archivo, sep=separador, low_memory=False)
    total_registros = len(df)

    if total_registros == 0:
        return None

    cant_coord_inv, _ = validar_coordenadas(ruta_archivo, separador)
    pct_coord = round((total_registros - cant_coord_inv) / total_registros * 100, 2)

    cant_fechas_inv, _ = validar_fechas(ruta_archivo, "eventDate", separador)
    pct_fechas = round((total_registros - cant_fechas_inv) / total_registros * 100, 2)

    pct_completitud = round(df.notnull().mean().mean() * 100, 2)

    return {
        "Dataset": nombre_dataset,
        "Total Registros": total_registros,
        "% Coordenadas Válidas": pct_coord,
        "% Fechas Válidas": pct_fechas,
        "% Completitud Promedio": pct_completitud
    }


def determinar_columna_agrupacion(df_actual):
    """
    Determina sobre qué columna agrupar el gráfico de observaciones por
    ubicación, según las columnas disponibles en el dataset.
    Retorna (columna_agrupacion, etiqueta_eje).
    """
    if 'country' in df_actual.columns and df_actual['country'].nunique() > 1:
        return 'country', 'País'
    elif 'stateProvince' in df_actual.columns:
        return 'stateProvince', 'Provincia'
    else:
        return 'locality', 'Localidad'


def calcular_conteos_por_ubicacion(df_actual, columna_agrupacion, num_elementos):
    """
    Retorna la cantidad de registros para los N valores más frecuentes
    de la columna de agrupación.
    """
    return df_actual[columna_agrupacion].value_counts().head(num_elementos)


def calcular_registros_por_anio(df_actual):
    """
    Calcula la cantidad de registros únicos por año a partir de eventDate.
    Retorna (conteos_por_anio, cantidad_de_fechas_invalidas).
    """
    nombre_id = df_actual.columns[0]
    df_fechas = df_actual[['eventDate', nombre_id]].rename(columns={'eventDate': 'fecha', nombre_id: 'codigo'})
    df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'], errors='coerce', utc=True)
    df_fechas['anio_calculado'] = df_fechas['fecha'].dt.year

    contador_nulos = df_fechas['anio_calculado'].isnull().sum()
    df_fechas = df_fechas.dropna(subset=['anio_calculado'])

    mascara_validos = df_fechas['anio_calculado'].between(1900, 2026)
    df_fechas = df_fechas[mascara_validos]

    conteos_por_anio = df_fechas.groupby('anio_calculado')['codigo'].nunique()

    return conteos_por_anio, contador_nulos


def calcular_distribucion_taxonomia(df_actual, columna_seleccionada):
    """
    Retorna la cantidad de registros para los 10 valores más frecuentes
    de la columna taxonómica seleccionada.
    """
    return df_actual[columna_seleccionada].value_counts().head(10)


def calcular_completitud_columnas(df_actual):
    """
    Calcula el porcentaje de completitud por columna, ordenado de menor a mayor.
    Retorna (columnas, valores) listos para graficar.
    """
    filas = df_actual.fillna("").astype(str).to_dict(orient="records")
    porcentaje_nulos = calcular_porcentaje_nulos_logica(filas, df_actual.columns)
    completitud = {col: 100 - pct for col, pct in porcentaje_nulos.items()}

    ordenado = sorted(
        [(col, val) for col, val in completitud.items() if val > 0],
        key=lambda x: x[1]
    )

    columnas = [item[0] for item in ordenado]
    valores = [item[1] for item in ordenado]
    return columnas, valores