import pandas as pd
from utils import buscar_registros_logica

def obtener_columna_pais(df):
    """
    Detecta y retorna el nombre de la columna de país disponible en el dataset.
    """
    if "countryCode" in df.columns:
        return "countryCode"
    elif "country" in df.columns:
        return "country"
    return None

def obtener_columna_provincia(df):
    """
    Detecta y retorna el nombre de la columna de provincia disponible en el dataset.
    """
    if "stateProvince" in df.columns:
        return "stateProvince"
    return None

def buscar_por_texto(df, col_busqueda, texto):
    """
    Busca registros donde la columna contenga el texto ingresado (case-insensitive).
    Reutiliza buscar_registros_logica del ejercicio 5.A con modo contiene.
    """
    if texto.strip():
        filas = df.fillna("").astype(str).to_dict(orient="records")
        filtros = {col_busqueda: texto.strip()}
        lista_valores = buscar_registros_logica(filas, list(df.columns), filtros, modo="contiene")
        return pd.DataFrame(lista_valores)
    return df.copy()


def buscar_por_filtros(df, especies_sel, observador_sel, col_pais, paises_sel, col_provincia, provincias_sel, fechas_sel):
    """
    Filtra el dataset aplicando múltiples condiciones combinadas.
    """
    resultados = df.copy()

    if especies_sel:
        resultados = resultados[resultados["scientificName"].isin(especies_sel)]

    if observador_sel:
        resultados = resultados[resultados["recordedBy"].isin(observador_sel)]

    if paises_sel and col_pais:
        resultados = resultados[resultados[col_pais].isin(paises_sel)]

    if provincias_sel and col_provincia:
        resultados = resultados[resultados[col_provincia].isin(provincias_sel)]

    if fechas_sel and len(fechas_sel) == 2:
        resultados["eventDate_parsed"] = pd.to_datetime(resultados["eventDate"], errors="coerce", utc=True)
        resultados = resultados[
            (resultados["eventDate_parsed"] >= pd.Timestamp(fechas_sel[0], tz="UTC")) &
            (resultados["eventDate_parsed"] <= pd.Timestamp(fechas_sel[1], tz="UTC"))
        ]
        resultados = resultados.drop(columns=["eventDate_parsed"])

    return resultados

def obtener_columnas_relevantes(df, col_pais, col_provincia):
    """
    Retorna la lista de columnas relevantes disponibles en el dataset.
    """
    return [c for c in [
        "occurrenceID", "scientificName", "recordedBy",
        col_pais, col_provincia, "locality", "eventDate",
        "decimalLatitude", "decimalLongitude"
    ] if c is not None and c in df.columns]