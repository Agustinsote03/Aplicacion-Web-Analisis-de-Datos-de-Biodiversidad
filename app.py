import streamlit as st 
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from dataset_loader import cargar_dataset, seleccionar_dataset, mostrar_info_dataset
from config import CONFIGURACION_DATASETS

st.set_page_config(page_title="App Biodiversidad", layout="wide")

# Definir todas las páginas
inicio = st.Page("pages/1_Inicio.py", title="Inicio")
estado = st.Page("pages/2_Estado_del_sistema.py", title="Estado del sistema")
busqueda = st.Page("pages/3_Busqueda.py", title="Búsqueda")
visualizacion = st.Page("pages/4_Visualizacion.py", title="Visualización")
gestion = st.Page("pages/5_Gestion_de_registros.py", title="Gestión de registros")
datasets = st.Page("pages/6_Datasets.py", title="Datasets")
ficha = st.Page("pages/7_Ficha.py", title="Ficha de datos")

# Registrar todas las páginas incluyendo ficha para que st.switch_page funcione
pg = st.navigation([inicio, estado, busqueda, visualizacion, gestion, datasets, ficha])

# Guardar la página de ficha en session_state para usarla desde P3
st.session_state["pagina_ficha"] = ficha

# Sidebar manual - sin la ficha
with st.sidebar:
    st.page_link(inicio, label="Inicio")
    st.page_link(estado, label="Estado del sistema")
    st.page_link(busqueda, label="Búsqueda")
    st.page_link(visualizacion, label="Visualización")
    st.page_link(gestion, label="Gestión de registros")
    st.page_link(datasets, label="Datasets")
    st.markdown("---")
    seleccionar_dataset()
    mostrar_info_dataset()

pg.run()