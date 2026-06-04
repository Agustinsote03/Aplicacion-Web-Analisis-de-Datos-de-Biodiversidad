import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys

#Importación de funciones
sys.path.append(str(Path(__file__).parent.parent / "src"))
from utils import calcular_porcentaje_nulos_logica

st.title("Visualización de Datos de Biodiversidad")

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

#Control: se verifica que haya un dataset cargado en la sesión
if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()
df_actual = st.session_state["dataset_actual"]




#Ejericio 3.A: Cantidad de observaciones por ubicación
def cantidad_registros():
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
    generar_grafico_generico(conteos.index, conteos.values, tipo_grafico="bar", titulo=f"Top {num_elementos} {etiqueta_eje.lower()}s con más observaciones", x_etiqueta=etiqueta_eje, y_etiqueta="Cantidad de Registros", color="#4ddb34", figsize=(12, 6))




#Ejercicio 3.B, se va a crear un nuevo dataframe para manipular las fechas
def cantidad_registros_por_anio():
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

    generar_grafico_generico(conteos_por_anio.index, conteos_por_anio.values, tipo_grafico="line", titulo="Cantidad de registros por año", x_etiqueta="Año", y_etiqueta="Cantidad de observaciones únicas", color="#e74c3c")


#Ejercicio 3.C #Preguntar

opciones_taxonomia = {'Clase': 'class', 'Orden': 'order', 'Familia': 'family'}

st.header("Distribución de registros según taxonomía")
df_actual = st.session_state["dataset_actual"]

eleccion_usuario = st.radio('Selecciona un nivel taxónomico para visualizar en el gráfico', ('Clase', 'Orden', 'Familia'))

columna_seleccionada = opciones_taxonomia[eleccion_usuario]
columna_taxonomia = df_actual[columna_seleccionada]

#Contamos los registros

conteo_taxonomia = columna_taxonomia.value_counts().head(10)

#Se crea gráfico de torta
fig, ax = plt.subplots(figsize=(20, 20))
ax.pie(conteo_taxonomia.values, labels=conteo_taxonomia.index, autopct='%1.1f%%', shadow=True)
ax.set_title(f"Distribución de registros por {eleccion_usuario}")
st.pyplot(fig)

#Ejercicio 3.D

def mostrar_grafico_completitud(nombre_archivo_dataset, separador="\t"):
    st.subheader("Completitud de datos por columna")
    
    ruta_str = "processed_datasets/" + nombre_archivo_dataset
    
    #Se reutiliza la función del ejercicio 3.F
    porcentaje_nulos_dict = calcular_porcentaje_nulos_logica(ruta_str, separador)
    
    #Se pasa a pandas para procesar el grafico 
    porcentaje_nulos = pd.Series(porcentaje_nulos_dict)
    
    #Se calculan los porcentajes de registros no nulos
    porcentaje_no_nulos = 100 - porcentaje_nulos
    porcentaje_ordenado = porcentaje_no_nulos.sort_values(ascending=True)
    
    #Se grafica con Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(porcentaje_ordenado.index, porcentaje_ordenado.values, color='#4db6ac')
    
    ax.set_title("Porcentaje de completitud por columna")
    ax.set_xlabel("Porcentaje de registros NO nulos (%)")
    ax.set_ylabel("Columnas")
    fig.tight_layout()
    
    st.pyplot(fig)

nombre_dataset = st.session_state["nombre_dataset"]
mostrar_grafico_completitud(nombre_dataset)
#Ejercicio 3.E