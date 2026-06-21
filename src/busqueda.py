import pandas as pd
from utils import buscar_registros_logica

def obtener_columna_pais(columnas):
    """
    Detecta y retorna el nombre de la columna de país disponible en el dataset.
    """
    if "countryCode" in columnas:
        return "countryCode"
    elif "country" in columnas:
        return "country"
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

    if observador_sel and "recordedBy" in resultados.columns:
        resultados = resultados[
            resultados["recordedBy"].astype(str).str.contains(observador_sel.strip(), case=False, na=False)
        ]

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

def paginar_resultados(df, pagina, registros_por_pagina=20):
    """
    Retorna el slice del DataFrame correspondiente a la página solicitada.
    """
    inicio = (pagina - 1) * registros_por_pagina
    fin = inicio + registros_por_pagina
    return df.iloc[inicio:fin]

def calcular_resumen(resultados, col_pais, col_provincia):
    """
    Calcula el resumen estadístico del subconjunto de registros encontrados.
    """
    return {
        "especies_unicas": resultados["scientificName"].nunique() if "scientificName" in resultados.columns else 0,
        "paises_repr": resultados[col_pais].nunique() if col_pais and col_pais in resultados.columns else 0,
        "provincias_repr": resultados[col_provincia].nunique() if col_provincia and col_provincia in resultados.columns else 0,
        "observadores": resultados["recordedBy"].nunique() if "recordedBy" in resultados.columns else 0
    }