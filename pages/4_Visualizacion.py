#-------------------------------------------------------Importaciones----------------------------------------------------------#

#Importación de librerías
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys

#Importación de funciones
sys.path.append(str(Path(__file__).parent.parent / "src"))
from visualizacion import (
    calcular_metricas_dataset,
    determinar_columna_agrupacion,
    calcular_conteos_por_ubicacion,
    calcular_registros_por_anio,
    calcular_distribucion_taxonomia,
    calcular_completitud_columnas,
)
from config import CONFIGURACION_DATASETS

#--------------------------------------------------Funciones Auxiliares-------------------------------------------------------#
def generar_grafico_generico(datos_x, datos_y, tipo_grafico="bar", titulo="", x_etiqueta="", y_etiqueta="", **kwargs):
    """
    Crea un gráfico de Matplotlib según los argumentos recibidos y lo renderiza en Streamlit
    """
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
    if tipo_grafico == 'bar':
        ax.bar(datos_x, datos_y, color=kwargs.get('color', '#4db6ac'))
        plt.xticks(rotation=45)
    elif tipo_grafico == 'line':
        ax.plot(datos_x, datos_y, marker='o', color=kwargs.get('color', '#e74c3c'))
        plt.xticks(rotation=45)
    elif tipo_grafico == 'pie':
        ax.pie(datos_y, labels=datos_x, autopct='%1.1f%%', shadow=True)
    elif tipo_grafico == 'barh':
        ax.barh(datos_x, datos_y, color=kwargs.get('color', '#4db6ac'))
        labelsize = kwargs.get('labelsize', None)
        if labelsize:
            ax.tick_params(axis='y', labelsize=labelsize)

    ax.set_title(titulo)
    if tipo_grafico != "pie":
        ax.set_xlabel(x_etiqueta)
        ax.set_ylabel(y_etiqueta)

    fig.tight_layout()
    st.pyplot(fig)

if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()
df_actual = st.session_state["dataset_actual"]

st.title("Visualización de Datos de Biodiversidad")


#--------------------------------Control: se verifica que haya un dataset cargado en la sesión--------------------------------#

if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()
df_actual = st.session_state["dataset_actual"]

st.title("Visualización de Datos de Biodiversidad")


#--------------------------------------------------Funciones Principales-------------------------------------------------------#

#Ejercicio 3.A
def mostrar_observaciones_por_ubicacion(df_actual):
    st.header("Observaciones por ubicacion")

    columna_agrupacion, etiqueta_eje = determinar_columna_agrupacion(df_actual)

    cantidad_valores_unicos = df_actual[columna_agrupacion].nunique()
    maximo_slider = max(1, cantidad_valores_unicos)
    valor_default = min(5, maximo_slider)

    num_elementos = st.slider(
        "Cantidad de ubicaciones a mostrar: ",
        min_value=1,
        max_value=maximo_slider,
        value=valor_default
    )

    conteos = calcular_conteos_por_ubicacion(df_actual, columna_agrupacion, num_elementos)

    generar_grafico_generico(
        conteos.index,
        conteos.values,
        tipo_grafico="bar",
        titulo=f"Top {num_elementos} {etiqueta_eje.lower()}s con más observaciones",
        x_etiqueta=etiqueta_eje,
        y_etiqueta="Cantidad de Registros",
        color="#4ddb34",
        figsize=(12, 6))


#Ejercicio 3.B
def mostrar_registros_por_anio(df_actual):
    conteos_por_anio, contador_nulos = calcular_registros_por_anio(df_actual)

    if conteos_por_anio.empty:
        st.warning(f"No hay registros con fechas válidas para mostrar. {contador_nulos} registros tienen fecha nula o inválida.")
        return

    st.warning(f"Se encontraron {contador_nulos} registros con fechas nulas o inválidas")

    generar_grafico_generico(
        conteos_por_anio.index,
        conteos_por_anio.values,
        tipo_grafico="line",
        titulo="Cantidad de registros por año",
        x_etiqueta="Año",
        y_etiqueta="Cantidad de observaciones únicas",
        color="#e74c3c"
    )

#Ejercicio 3.C
def mostrar_distribucion_taxonomia(df_actual):
    st.header("Distribución de registros según taxonomía")
    opciones_taxonomia = {'Clase': 'class', 'Orden': 'order', 'Familia': 'family'}

    opciones_disponibles = {k: v for k, v in opciones_taxonomia.items() if v in df_actual.columns}

    if not opciones_disponibles:
        st.warning("Este dataset no contiene columnas taxonómicas (class, order, family).")
        return

    eleccion_usuario = st.radio(
        'Selecciona un nivel taxonómico para visualizar en el gráfico',
        list(opciones_disponibles.keys())
    )
    columna_seleccionada = opciones_taxonomia[eleccion_usuario]

    conteo_taxonomia = calcular_distribucion_taxonomia(df_actual, columna_seleccionada)

    generar_grafico_generico(
        conteo_taxonomia.index,
        conteo_taxonomia.values,
        tipo_grafico="pie",
        titulo=f"Distribución de registros por {eleccion_usuario}",
        figsize=(20, 17)
    )


#Ejercicio 3.D
def mostrar_grafico_completitud(df_actual):
    st.subheader("Completitud de datos por columna")

    columnas, valores = calcular_completitud_columnas(df_actual)

    generar_grafico_generico(
        columnas,
        valores,
        tipo_grafico="barh",
        titulo="Porcentaje de completitud por columna",
        x_etiqueta="% de registros NO nulos",
        y_etiqueta="Columnas",
        figsize=(10, max(8, len(columnas) * 0.3)),
        labelsize=7
    )


#Ejercicio 3.E
def mostrar_tabla_comparativa(datasets):
    st.header("Comparativa de datasets")

    filas = []
    for nombre, cfg in datasets.items():
        fila = calcular_metricas_dataset(cfg["ruta"], nombre, cfg.get("separador", "\t"))
        if fila:
            filas.append(fila)

    if not filas:
        st.warning("No hay datasets disponibles.")
        return

    df_comp = pd.DataFrame(filas).set_index("Dataset")
    st.dataframe(df_comp, use_container_width=True)


mostrar_observaciones_por_ubicacion(df_actual)
mostrar_registros_por_anio(df_actual)
mostrar_distribucion_taxonomia(df_actual)
mostrar_grafico_completitud(df_actual)
mostrar_tabla_comparativa(CONFIGURACION_DATASETS)