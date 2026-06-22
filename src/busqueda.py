import pandas as pd
from utils import buscar_registros_logica, cumple_alguno, cumple_filtro
from config import CONFIGURACION_DATASETS
from ficha_mapa import detectar_columnas_coordenadas

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


def buscar_por_filtros(df, especies_sel, observador_texto, col_pais, paises_sel, col_provincia, provincias_sel, fechas_sel):
    """
    Filtra el dataset aplicando múltiples condiciones combinadas.

    Reutiliza las funciones de comparación de la etapa 1 (utils.py) en
    TODOS los filtros de igualdad/texto del modo "Filtros avanzados".

    El filtro de fechas es la única excepción y se mantiene con
    operaciones de pandas (>=, <=) porque es un rango continuo, una
    comparación de naturaleza distinta a la igualdad/contención que
    resuelven cumple_filtro y cumple_alguno: no tiene sentido forzarlo
    a esa capa de lógica solo por uniformidad.
    """
    resultados = df.copy()

    if especies_sel:
        mascara_especie = resultados["scientificName"].fillna("").apply(
            lambda valor: cumple_alguno(valor, especies_sel, modo="exacto")
        )
        resultados = resultados[mascara_especie]

    if observador_texto and observador_texto.strip():
        mascara_observador = resultados["recordedBy"].fillna("").apply(
            lambda valor: cumple_filtro(valor, observador_texto, modo="contiene")
        )
        resultados = resultados[mascara_observador]

    if paises_sel and col_pais:
        mascara_pais = resultados[col_pais].fillna("").apply(
            lambda valor: cumple_alguno(valor, paises_sel, modo="exacto")
        )
        resultados = resultados[mascara_pais]

    if provincias_sel and col_provincia:
        mascara_provincia = resultados[col_provincia].fillna("").apply(
            lambda valor: cumple_alguno(valor, provincias_sel, modo="exacto")
        )
        resultados = resultados[mascara_provincia]

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
    Usa detectar_columnas_coordenadas para resolver las variantes de lat/lon
    """
    col_lat, col_lon = detectar_columnas_coordenadas(df)

    columnas_candidatas = [
        "occurrenceID", "scientificName", "recordedBy",
        col_pais, col_provincia, "locality", "eventDate",
        col_lat, col_lon
    ]
    return [c for c in columnas_candidatas if c is not None and c in df.columns]

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