import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataset_loader import cargar_dataset
from config import CONFIGURACION_DATASETS
from dataset_reader import porcentaje_nulos_por_columna
from validador import es_coordenada_valida, validar_y_convertir_fecha

# EJERCICIO 5.4
def obtener_info_archivo(nombre, cfg):
    """
    Retorna diccionario con nombre del archivo (o ruta si no existe),
            tamaño en MB redondeado a 4 decimales, o "N/D",
            fecha formateada, o "N/D", "✅" si existe en disco, "❌" si no.
    """
    ruta = Path(cfg["ruta"])
 
    if ruta.exists():
        tamanio_mb = round(ruta.stat().st_size / (1024 * 1024), 4)
        fecha_mod = datetime.fromtimestamp(ruta.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "Nombre del archivo": ruta.name,
            "Tamaño (MB)": tamanio_mb,
            "Última modificación": fecha_mod,
            "Disponible": "✅"
        }
    else:
        return {
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

def mostrar_tabla_datasets():
    """
        Muestra una tabla con todos los datasets registrados en el sistema.
    """
    st.header("Datasets disponibles")
    st.markdown("Listado de todos los datasets registrados en el sistema con información básica de cada archivo.")
 
    df_tabla = construir_tabla_datasets()
    st.dataframe(df_tabla, use_container_width=True)
 
    st.markdown("---")


# EJERCICIO 5.B
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

def mostrar_detalle_dataset(datasets_disponibles):
    """
    Muestra un selector con los datasets disponibles. Al elegir uno,
    muestra la cantidad de registros, cantidad de columnas y una tabla
    con el porcentaje de valores nulos por columna (de mayor a menor).
    """
    st.header("Información detallada")
    st.markdown("Seleccioná un dataset para ver sus columnas, cantidad de registros y valores nulos.")
 
    if not datasets_disponibles:
        st.warning("No hay datasets disponibles en el sistema.")
        st.markdown("---")
        return
 
    dataset_elegido = st.selectbox(
        "Elegí un dataset para explorar",
        datasets_disponibles,
        key="selector_detalle"
    )
 
    with st.spinner(f"Cargando {dataset_elegido}..."):
        df_detalle = cargar_dataset(dataset_elegido)
 
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.metric("Total de registros", len(df_detalle))
    with col_der:
        st.metric("Total de columnas", len(df_detalle.columns))
 
    st.subheader("Columnas y valores nulos")
    st.markdown("Porcentaje de valores nulos por columna, ordenado de mayor a menor.")
 
    df_nulos = calcular_nulos_por_columna(df_detalle)
    st.dataframe(df_nulos, use_container_width=True)
 
    st.markdown("---")

# Ejercicio 5.C
def calcular_pct_coordenadas_validas(df, nombre):
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

def calcular_metricas_dataset(nombre):
    """
    Carga un dataset y calcula sus métricas de calidad de datos.
    """
    ruta = Path(CONFIGURACION_DATASETS[nombre]["ruta"])
    if not ruta.exists():
        return None

    df = cargar_dataset(nombre)
    total = len(df)

    if total == 0:
        return {"Dataset": nombre, "Registros": 0,
                "% Coords válidas": 0.0, "% Fechas válidas": 0.0,
                "% Campos completos (prom.)": 0.0}

    return {
        "Dataset": nombre,
        "Registros": total,
        "% Coords válidas": calcular_pct_coordenadas_validas(df, nombre),  # ← pasa nombre
        "% Fechas válidas": calcular_pct_fechas_validas(df),
        "% Campos completos (prom.)": round(df.notnull().mean().mean() * 100, 2),
    }
 
def construir_tabla_comparativa(datasets_disponibles):
    """
    Genera un DataFrame comparativo con métricas de calidad para todos
    los datasets disponibles.
    """
    filas = []
    for nombre in datasets_disponibles:
        metricas = calcular_metricas_dataset(nombre)
        if metricas:
            filas.append(metricas)
 
    if not filas:
        return None
 
    return pd.DataFrame(filas).set_index("Dataset")
 
def mostrar_tabla_comparativa(datasets_disponibles):
    """
    Muestra una tabla comparativa de todos los datasets disponibles con
        la cantidad de registros, % de registros con coordenadas válidas,
        % de registros con fecha válida,
        % de campos completados en promedio.
    """
    st.header("Tabla comparativa")
    st.markdown("Comparación de calidad de datos entre todos los datasets disponibles.")
 
    if not datasets_disponibles:
        st.info("No hay datasets disponibles para comparar.")
        st.markdown("---")
        return
 
    with st.spinner("Calculando métricas de calidad..."):
        df_comp = construir_tabla_comparativa(datasets_disponibles)
 
    if df_comp is not None:
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.warning("No se pudieron calcular métricas para los datasets disponibles.")
 
    st.markdown("---")
 
 # Ejercicio 5.D
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


def mostrar_documentacion():
    """
    Busca archivos .md en la carpeta documentation/ y muestra un selector.
    Al elegir uno renderiza su contenido con st.markdown.
    Si no hay archivos informa al usuario.
    """
    st.header("Documentación del proyecto")
    st.markdown("Documentos generados durante la primera etapa del trabajo.")

    archivos = obtener_archivos_documentacion()

    if not archivos:
        st.info("No se encontraron archivos en la carpeta `documentation/`.")
        return

    nombres = [f.name for f in archivos]
    doc_elegida = st.selectbox("Elegí un documento para visualizar", nombres, key="selector_doc")

    ruta_doc = next(f for f in archivos if f.name == doc_elegida)
    contenido = leer_archivo_markdown(ruta_doc)
    st.markdown(contenido)
 
def main():
    """
    Función principal de la página P6 — Datasets.
    Llama al sidebar y luego a cada sección en orden.
    """

    st.title("Datasets")
    st.markdown("""
    Esta página ofrece una vista general de todos los datasets disponibles en el sistema.
    """)
    st.markdown("---")

    datasets_disponibles = obtener_datasets_disponibles()
    
    mostrar_tabla_datasets()    # Ejercicio 5.A
    mostrar_detalle_dataset(datasets_disponibles)   # Ejercicio 5.B
    mostrar_tabla_comparativa(datasets_disponibles) # Ejercicio 5.C
    mostrar_documentacion() # Ejercicio 5.D

main()

