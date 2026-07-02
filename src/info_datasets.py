import pandas as pd
from pathlib import Path
from datetime import datetime
from config import CONFIGURACION_DATASETS


def obtener_info_archivo(nombre, cfg):
    ruta = Path(cfg["ruta"])

    if ruta.exists():
        tamanio_mb = round(ruta.stat().st_size / (1024 * 1024), 4)
        fecha_mod = datetime.fromtimestamp(ruta.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "Dataset": nombre,        
            "Nombre del archivo": ruta.name,
            "Tamaño (MB)": tamanio_mb,
            "Última modificación": fecha_mod,
            "Disponible": "✅"
        }
    else:
        return {
            "Dataset": nombre,       
            "Nombre del archivo": cfg["ruta"],
            "Tamaño (MB)": "N/D",
            "Última modificación": "N/D",
            "Disponible": "❌"
        }


def construir_tabla_datasets():
    """
    Construye un DataFrame con información de todos los datasets registrados
    en CONFIGURACION_DATASETS, sin importar si existen o no en disco.
    """
    filas = [
        obtener_info_archivo(nombre, cfg)
        for nombre, cfg in CONFIGURACION_DATASETS.items()
    ]
    return pd.DataFrame(filas)


def calcular_nulos_por_columna(df):
    """
    Calcula el porcentaje y cantidad de valores nulos por columna de un DataFrame.
    Considera como nulo tanto NaN como strings vacíos.
    """
    nulos_abs = df.apply(lambda col: col.isna() | (col.astype(str).str.strip() == "")).sum()
    validos = len(df) - nulos_abs
    nulos_pct = (nulos_abs / len(df)) * 100

    df_nulos = pd.DataFrame({
        "Columna": df.columns,
        "% Nulos": nulos_pct.round(2).values,
        "Registros nulos": nulos_abs.values,
        "Registros válidos": validos.values
    })
    return df_nulos.sort_values("% Nulos", ascending=False).reset_index(drop=True)


def obtener_datasets_disponibles():
    """
    Recorre CONFIGURACION_DATASETS y devuelve una lista con los nombres
    de los datasets cuyos archivos existen físicamente en disco.
    """
    return [
        nombre
        for nombre, cfg in CONFIGURACION_DATASETS.items()
        if Path(cfg["ruta"]).exists()
    ]


def calcular_pct_coordenadas_validas(df, nombre):
    """
    Calcula el porcentaje de registros con coordenadas válidas para un dataset.
    """
    cfg = CONFIGURACION_DATASETS[nombre]
    col_lat = cfg.get("col_lat", "decimalLatitude")
    col_lon = cfg.get("col_lon", "decimalLongitude")

    if col_lat not in df.columns or col_lon not in df.columns:
        return 0.0

    lat = pd.to_numeric(df[col_lat], errors="coerce")
    lon = pd.to_numeric(df[col_lon], errors="coerce")

    validas = (
        lat.notna() & lon.notna() &
        lat.between(-90, 90) &
        lon.between(-180, 180)
    ).sum()

    return round(validas / len(df) * 100, 2)


def calcular_pct_fechas_validas(df):
    """
    Calcula el porcentaje de registros con fecha válida (no nula y no futura).
    """
    if "eventDate" not in df.columns:
        return 0.0

    fechas = pd.to_datetime(
        df["eventDate"].astype(str).str[:10],
        format="%Y-%m-%d",
        errors="coerce"
    )
    hoy = pd.Timestamp(datetime.now().date())
    validas = (fechas.notna() & (fechas <= hoy)).sum()

    return round(validas / len(df) * 100, 2)


def calcular_metricas_dataset(nombre, df):
    """
    Calcula las métricas de calidad de datos para un dataset ya cargado.
    Recibe el nombre y el DataFrame para no releer el archivo desde disco.
    """
    total = len(df)
    if total == 0:
        return {"Dataset": nombre, "Registros": 0,
                "% Coords válidas": 0.0, "% Fechas válidas": 0.0,
                "% Campos completos (prom.)": 0.0}

    return {
        "Dataset": nombre,
        "Registros": total,
        "% Coords válidas": calcular_pct_coordenadas_validas(df, nombre),
        "% Fechas válidas": calcular_pct_fechas_validas(df),
        "% Campos completos (prom.)": round(df.notnull().mean().mean() * 100, 2),
    }


def construir_tabla_comparativa(datasets_disponibles, cargar_fn):
    """
    Genera un DataFrame comparativo con métricas de calidad para todos
    los datasets disponibles. Recibe cargar_fn para no depender de imports
    de otras páginas directamente.
    """
    filas = []
    for nombre in datasets_disponibles:
        df = cargar_fn(nombre)
        metricas = calcular_metricas_dataset(nombre, df)
        if metricas:
            filas.append(metricas)

    if not filas:
        return None

    return pd.DataFrame(filas).set_index("Dataset")


def obtener_archivos_documentacion():
    """
    Busca archivos Markdown (.md) dentro de la carpeta 'documentation/'.
    Retorna lista de objetos Path ordenados alfabéticamente,
    o lista vacía si la carpeta no existe o no tiene archivos .md.
    """
    carpeta = Path("documentation")
    if not carpeta.exists():
        return []
    return sorted(carpeta.glob("*.md"))


def leer_archivo_markdown(ruta_archivo):
    """
    Lee y retorna el contenido de un archivo Markdown como string.
    """
    return Path(ruta_archivo).read_text(encoding="utf-8")