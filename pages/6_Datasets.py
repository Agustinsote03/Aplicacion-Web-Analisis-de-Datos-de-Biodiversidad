import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataset_loader import seleccionar_dataset, mostrar_info_dataset, cargar_dataset
from config import CONFIGURACION_DATASETS

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
    """
    nulos_pct = df.isnull().mean() * 100
    nulos_abs = df.isnull().sum()
    validos = df.notnull().sum()
 
    df_nulos = pd.DataFrame({
        "Columna": nulos_pct.index,
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
 
 
def main():
    """
    Función principal de la página P6 — Datasets.
    Llama al sidebar y luego a cada sección en orden.
    """
    seleccionar_dataset()
    mostrar_info_dataset()

    st.title("Datasets")
    st.markdown("""
    Esta página ofrece una vista general de todos los datasets disponibles en el sistema.
    """)
    st.markdown("---")

    datasets_disponibles = obtener_datasets_disponibles()
    
    mostrar_tabla_datasets()    # Ejercicio 5.A
    mostrar_detalle_dataset(datasets_disponibles)   # Ejercicio 5.B


main()

