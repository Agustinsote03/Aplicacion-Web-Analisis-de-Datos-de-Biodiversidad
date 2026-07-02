import streamlit as st
import pandas as pd
from pathlib import Path
from dataset_loader import seleccionar_dataset, mostrar_info_dataset, cargar_dataset
from info_datasets import (
    construir_tabla_datasets,
    calcular_nulos_por_columna,
    obtener_datasets_disponibles,
    construir_tabla_comparativa,
    obtener_archivos_documentacion,
    leer_archivo_markdown,
)


def mostrar_tabla_datasets():
    """Muestra una tabla con todos los datasets registrados en el sistema."""
    st.header("Datasets disponibles")
    st.markdown("Listado de todos los datasets registrados en el sistema con información básica de cada archivo.")
    st.dataframe(construir_tabla_datasets(), use_container_width=True)
    st.markdown("---")


def mostrar_detalle_dataset(datasets_disponibles):
    """Muestra información detallada del dataset elegido por el usuario."""
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
    st.dataframe(calcular_nulos_por_columna(df_detalle), use_container_width=True)
    st.markdown("---")


def mostrar_tabla_comparativa(datasets_disponibles):
    """Muestra una tabla comparativa de calidad entre todos los datasets disponibles."""
    st.header("Tabla comparativa")
    st.markdown("Comparación de calidad de datos entre todos los datasets disponibles.")

    if not datasets_disponibles:
        st.info("No hay datasets disponibles para comparar.")
        st.markdown("---")
        return

    with st.spinner("Calculando métricas de calidad..."):
        df_comp = construir_tabla_comparativa(datasets_disponibles, cargar_dataset)

    if df_comp is not None:
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.warning("No se pudieron calcular métricas para los datasets disponibles.")

    st.markdown("---")


def mostrar_documentacion():
    """Muestra los archivos Markdown de la carpeta documentation/."""
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
    seleccionar_dataset()
    mostrar_info_dataset()

    st.title("Datasets")
    st.markdown("Esta página ofrece una vista general de todos los datasets disponibles en el sistema.")
    st.markdown("---")

    datasets_disponibles = obtener_datasets_disponibles()

    mostrar_tabla_datasets()
    mostrar_detalle_dataset(datasets_disponibles)
    mostrar_tabla_comparativa(datasets_disponibles)
    mostrar_documentacion()


main()