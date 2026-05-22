import streamlit as st 
import matplotlib.pyplot as plt

st.title("Visualización de Datos de Biodiversidad")


if "dataset_actual" not in st.session_state or st.session_state["dataset_actual"] is None:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()

# tomamos el dataframe de la memoria de la memoria
df = st.session_state["dataset_actual"]

st.header("Observaciones por Ubicación")

# Control deslizante requerido por el Ejercicio 3.A
num_elementos = st.slider("Cantidad de ubicaciones a mostrar: ", min_value=1, max_value=50, value=5)

#Validación automática: Si hay 1 solo país único, graficamos por provincia. Si hay más, por país.
# 3. Validación automática mejorada (Ejercicio 3.A)
# Primero verificamos si la columna 'country' existe Y si tiene más de 1 país
if 'country' in df.columns and df['country'].nunique() > 1:
    columna_agrupacion = 'country'
    etiqueta_eje = 'País'
# Si no hay 'country' o es un solo país, verificamos si existe 'stateProvince'
elif 'stateProvince' in df.columns:
    columna_agrupacion = 'stateProvince'
    etiqueta_eje = 'Provincia'
# Si tampoco existe (algunos datasets son muy básicos), usamos 'locality'
else:
    columna_agrupacion = 'locality' 
    etiqueta_eje = 'Localidad'

# Usamos la variable 'columna_agrupacion' de forma dinámica para contar

# Usamos la variable 'columna_agrupacion' de forma dinámica para contar
conteos = df[columna_agrupacion].value_counts().head(num_elementos)

# 4. Bloque de gráfico de Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(conteos.index, conteos.values, color="#4ddb34") 

# Etiquetas y título dinámicos
ax.set_xlabel(etiqueta_eje)
ax.set_ylabel("Cantidad de Registros")
ax.set_title(f"Top {num_elementos} {etiqueta_eje.lower()}s con más observaciones")
plt.xticks(rotation=45) 

# Renderiza Streamlit
st.pyplot(fig)


