import pandas as pd

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