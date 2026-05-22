import streamlit as st 
import matplotlib.pyplot as plt

st.title("Visualización")

# Validamos que el dataset haya sido cargado previamente en el sidebar
if "dataset_iadiza" not in st.session_state:
    st.warning("Selecciona un dataset desde la barra lateral para visualizar los datos.")
    st.stop()

# Recuperamos los datos de la memoria 
df_iadiza = st.session_state["dataset_iadiza"]

# Bloque del slider 
num_elementos = st.slider("Cantidad de ubicaciones a mostrar: ", min_value=1, max_value=20, value=5)
conteos = df_iadiza['stateProvince'].value_counts().head(num_elementos)

# Bloque de gráfico de matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(conteos.index, conteos.values, color='#3498db') 

# Etiquetas y título
ax.set_xlabel("País")
ax.set_ylabel("Cantidad de Registros")
ax.set_title(f"Top {num_elementos} países con más observaciones")
plt.xticks(rotation=45) 

# Renderiza Streamlit
st.pyplot(fig)


