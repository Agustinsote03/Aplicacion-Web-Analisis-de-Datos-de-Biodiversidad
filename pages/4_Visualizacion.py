import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
from src.dataset_reader import porcentaje_nulos_por_columna
st.title("Visualización de Datos de Biodiversidad")


if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()


df_actual = st.session_state["dataset_actual"]

st.header("Observaciones por ubicación")

num_elementos = st.slider("Cantidad de ubicaciones a mostrar: ", min_value=1, max_value=10, value=5)

#Validación automática: Si hay 1 solo país único, graficamos por provincia. Si hay más, por país.
if 'country' in df_actual.columns and df_actual['country'].nunique() > 1:
    columna_agrupacion = 'country'
    etiqueta_eje = 'País'
# Si no hay 'country' o es un solo país, verificamos si existe 'stateProvince'
elif 'stateProvince' in df_actual.columns:
    columna_agrupacion = 'stateProvince'
    etiqueta_eje = 'Provincia'
# Si tampoco existe (algunos datasets son muy básicos), usamos 'locality'
else:
    columna_agrupacion = 'locality' 
    etiqueta_eje = 'Localidad'

conteos = df_actual[columna_agrupacion].value_counts().head(num_elementos)

#Bloque de gráfico de Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(conteos.index, conteos.values, color="#4ddb34") 

# Etiquetas y título 
ax.set_xlabel(etiqueta_eje)
ax.set_ylabel("Cantidad de Registros")
ax.set_title(f"Top {num_elementos} {etiqueta_eje.lower()}s con más observaciones")
plt.xticks(rotation=45) 

# Renderiza Streamlit
st.pyplot(fig)


#Ejercicio 3.B, se va a crear un nuevo dataframe para manipular las fechas

#Control: se verifica que encabezado le corresponde a la columna que contiene los IDs

nombre_id = df_actual.columns[0] #Preguntar si es segura esta forma de obtener el nombre de la columna ID
df_fechas = df_actual[['eventDate', nombre_id]].rename(columns={'eventDate': 'fecha', nombre_id: 'codigo'}) 

df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'], errors='coerce', utc= True)
df_fechas['anio_calculado'] = df_fechas['fecha'].dt.year
contador_nulos = df_fechas['anio_calculado'].isnull().sum()
st.warning(f"Se encontraron {contador_nulos} registros con fechas nulas o inválidas")

#Se limpia el dataframe
df_fechas = df_fechas.dropna(subset=['anio_calculado'])

#Se cambia el formato de las fechas a uno más simple

df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'], errors='coerce', utc=True)
df_fechas['anio_calculado'] = df_fechas['fecha'].dt.year

#Se aplica un filtrado de fechas, para quedarnos solo con las fechas coherentes
mascara_validos = df_fechas['anio_calculado'].between(1900, 2026)
df_fechas = df_fechas[mascara_validos]
#Por control, se imprimen las primeras filas del nuevo dataset
st.subheader("Primeras filas del dataset de fechas")
st.dataframe(df_fechas[['anio_calculado', 'codigo']].head(3))


#Se agrupan los datos por año y se cuentan la cantidad de registros únicos que hay para cada año, descartando duplicados
conteos_por_anio = df_fechas.groupby('anio_calculado')['codigo'].nunique()
contador_nulos = df_fechas['anio_calculado'].isnull().sum()

st.warning(f"Se encontraron {contador_nulos} registros con fechas nulas o inválidas")


#En este bloque se grafican las lineas con matplotlib
fig, ax = plt.subplots(figsize=(10, 6))


ax.plot(conteos_por_anio.index, conteos_por_anio.values, marker='o', color='#e74c3c')

ax.set_title('Cantidad de registros por año')
ax.set_xlabel('Año')
ax.set_ylabel('Cantidad de observaciones únicas') 
plt.xticks(rotation=45) 
st.pyplot(fig)

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

st.subheader("Porcentaje de registros nulos por columna")
ruta_archivo = st.session_state["dataset_actual"]
diccionario_nulos = porcentaje_nulos_por_columna(ruta_archivo)
series_nulos = pd.Sereis(diccionario_nulos)

#Calculamos el porcentaje de registros no nulos
serie_completitud = 100 - series_nulos
serie_completitud = serie_completitud.sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 10))

ax.barh(serie_completitud.index, serie_completitud.values, color="#3498db")
ax.set_title("Porcentaje de registro no nulos por columna")
ax.set_xlabel("Porcentaje %")
ax.set_xlim(0, 100)

st.ptplot(fig)