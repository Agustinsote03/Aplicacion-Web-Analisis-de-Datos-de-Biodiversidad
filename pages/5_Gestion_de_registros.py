import streamlit as st
import sys
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

# Importamos lo necesario para el sidebar
from dataset_loader import seleccionar_dataset, mostrar_info_dataset

# Acá se van a importar las funciones de la etapa 1 para insertar, modificar, eliminar y loguear

# Sidebar: selector e información de datasets
seleccionar_dataset()
mostrar_info_dataset()

st.title("Gestión de Registros")
st.markdown("""
En esta sección podés **Insertar**, **Actualizar** o **Eliminar** registros 
del dataset que tengas seleccionado.
""")

# Verificar que haya un dataset cargado en la sesión
if "nombre_dataset" not in st.session_state:
    st.warning("Seleccioná un dataset desde el menú lateral.")
    st.stop()

# Obtener el dataframe y el nombre del dataset seleccionado
df = st.session_state["dataset_actual"]
nombre_dataset = st.session_state["nombre_dataset"]

# Separamos las operaciones en 3 pestañas limpias
tab_insertar, tab_actualizar, tab_eliminar = st.tabs(["Insertar", "Actualizar", "Eliminar"])