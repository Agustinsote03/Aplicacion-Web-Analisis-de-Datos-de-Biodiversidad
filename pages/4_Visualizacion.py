#-------------------------------------------------------Importaciones----------------------------------------------------------#

#Importación de librerías
import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys

#Importación de funciones
sys.path.append(str(Path(__file__).parent.parent / "src"))
from utils import calcular_porcentaje_nulos_logica
from validador import validar_coordenadas, validar_fechas


#--------------------------------------------------Funciones Auxiliares-------------------------------------------------------#
def generar_grafico_generico(datos_x, datos_y, tipo_grafico="bar", titulo="", x_etiqueta="", y_etiqueta="", **kwargs):

    """
     Crea un gráfico de Matplotlib según los argumentos recibidos y lo renderiza en Streamlit
    """
    fig, ax = plt.subplots(figsize=kwargs.get('figsize',(10, 6)))
    if tipo_grafico == 'bar':
        ax.bar(datos_x, datos_y, color=kwargs.get('color', '#4db6ac'))
        plt.xticks(rotation=45)

    elif tipo_grafico == 'line':
        ax.plot(datos_x, datos_y, marker='o', color=kwargs.get('color', '#e74c3c'))
        plt.xticks(rotation=45)

    elif tipo_grafico == 'pie':
        ax.pie(datos_y, labels=datos_x, autopct='%1.1f%%', shadow=True)
    
    ax.set_title(titulo)
    if tipo_grafico != "pie":
        ax.set_xlabel(x_etiqueta)
        ax.set_ylabel(y_etiqueta)
    

    fig.tight_layout()
    st.pyplot(fig)



#--------------------------------Control: se verifica que haya un dataset cargado en la sesión--------------------------------#

if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()
df_actual = st.session_state["dataset_actual"]

st.title("Visualización de Datos de Biodiversidad")


#--------------------------------------------------Funciones Principales-------------------------------------------------------#

#Ejericio 3.A: Cantidad de observaciones por ubicación
def cantidad_registros(df_actual):
    st.header("Observaciones por ubicacion")
    num_elementos = st.slider("Cantidad de ubicaciones a mostrar: ", min_value=1, max_value=10, value=5)

    if 'country' in df_actual.columns and df_actual['country'].nunique() > 1:
        columna_agrupacion = 'country'
        etiqueta_eje = 'País'
    elif 'stateProvince' in df_actual.columns:
        columna_agrupacion = 'stateProvince'
        etiqueta_eje = 'Provincia'
    else:
        columna_agrupacion = 'locality' 
        etiqueta_eje = 'Localidad'
    conteos = df_actual[columna_agrupacion].value_counts().head(num_elementos)
    generar_grafico_generico(
        conteos.index,
        conteos.values,
        tipo_grafico="bar",
        titulo=f"Top {num_elementos} {etiqueta_eje.lower()}s con más observaciones",
        x_etiqueta=etiqueta_eje,
        y_etiqueta="Cantidad de Registros",
        color="#4ddb34",
        figsize=(12, 6))




#Ejercicio 3.B, se va a crear un nuevo dataframe para manipular las fechas
def cantidad_registros_por_anio(df_actual):
    nombre_id = df_actual.columns[0]
    df_fechas = df_actual[['eventDate', nombre_id]].rename(columns={'eventDate': 'fecha', nombre_id: 'codigo'})
    df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'], errors='coerce', utc=True)
    df_fechas['anio_calculado'] = df_fechas['fecha'].dt.year
    contador_nulos = df_fechas['anio_calculado'].isnull().sum()

    #Se limpia el dataframe
    df_fechas = df_fechas.dropna(subset=['anio_calculado'])

    #Se cambia el formato de las fechas a uno más simple
    df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'], errors='coerce', utc=True)
    df_fechas['anio_calculado'] = df_fechas['fecha'].dt.year

    #Se aplica un filtrado de fechas, para quedarnos solo con las fechas coherentes
    mascara_validos = df_fechas['anio_calculado'].between(1900, 2026)
    df_fechas = df_fechas[mascara_validos]

    #Se agrupan los datos por año y se cuentan la cantidad de registros únicos que hay para cada año, descartando duplicados
    conteos_por_anio = df_fechas.groupby('anio_calculado')['codigo'].nunique()
    contador_nulos = df_fechas['anio_calculado'].isnull().sum()

    #Se muestra en una advertencia la cantidad de registros con fechas nulas o inválidas
    st.warning(f"Se encontraron {contador_nulos} registros con fechas nulas o inválidas")

    generar_grafico_generico(conteos_por_anio.index,
                            conteos_por_anio.values,
                            tipo_grafico="line",
                            titulo="Cantidad de registros por año",
                            x_etiqueta="Año",
                            y_etiqueta="Cantidad de observaciones únicas",
                            color="#e74c3c"
                            )


#Ejercicio 3.C

def distribucion_registros_taxonomia(df_actual):
    st.header("Distribución de registros según taxonomía")
    opciones_taxonomia = {'Clase': 'class', 'Orden': 'order', 'Familia': 'family'}

    # Se filtran solo las opciones cuya columna existe en el dataset
    opciones_disponibles = {k: v for k, v in opciones_taxonomia.items() if v in df_actual.columns}

    if not opciones_disponibles:
        st.warning("Este dataset no contiene columnas taxonómicas (class, order, family).")
        return

    eleccion_usuario = st.radio(
        'Selecciona un nivel taxonómico para visualizar en el gráfico',
        list(opciones_disponibles.keys())
    )
    columna_seleccionada = opciones_taxonomia[eleccion_usuario]
    columna_taxonomia = df_actual[columna_seleccionada]
    
    #Se cuentan los registros por cada valor único de la columna taxonomica seleccionada
    conteo_taxonomia = columna_taxonomia.value_counts().head(10)

    #Se crea gráfico de torta
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

    #Puente entre DataFrame y el iterador que espera la función 'calcular_porcentaje_nulos_logica'
    filas = df_actual.fillna("").astype(str).to_dict(orient="records")

    #se reutiliza la función lógica del ejercicio 2.F de la primera parte
    porcentaje_nulos = calcular_porcentaje_nulos_logica(filas, df.columns)

    #Se calcula el porcentaje de completitud a partir del porcentaje de nulos
    completitud = {col: 100 - pct for col, pct in porcentaje_nulos.items()}

    #See filtra y ordena el resultado 
    ordenado = sorted([(col, val) for col, val in completitud.items() if val > 0],key=lambda x: x[1])

    columnas = [item[0] for item in ordenado]
    valores  = [item[1] for item in ordenado]

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


cantidad_registros(df_actual)
cantidad_registros_por_anio(df_actual)
distribucion_registros_taxonomia(df_actual)
mostrar_grafico_completitud(df_actual)