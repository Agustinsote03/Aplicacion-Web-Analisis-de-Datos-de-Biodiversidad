import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from dataset_loader import seleccionar_dataset, mostrar_info_dataset, cargar_dataset
from config import CONFIGURACION_DATASETS

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
    A diferencia del resto de las páginas, **no depende del dataset seleccionado** en el sidebar.
    """)
    st.markdown("---")

    mostrar_tabla_datasets()

main()