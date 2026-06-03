import streamlit as st 
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from dataset_loader import cargar_dataset, seleccionar_dataset, mostrar_info_dataset
from config import CONFIGURACION_DATASETS

st.set_page_config(page_title="App Biodiversidad", layout="wide")

# Páginas que aparecen en el sidebar
paginas = [
    st.Page("pages/1_Inicio.py", title="Inicio"),
    st.Page("pages/2_Estado_del_sistema.py", title="Estado del sistema"),
    st.Page("pages/3_Busqueda.py", title="Búsqueda"),
    st.Page("pages/4_Visualizacion.py", title="Visualización"),
    st.Page("pages/5_Gestion_de_registros.py", title="Gestión de registros"),
    st.Page("pages/6_Datasets.py", title="Datasets"),
]

# Página oculta
pagina_ficha = st.Page("pages/7_Ficha.py", title="Ficha de datos")

pg = st.navigation(paginas + [pagina_ficha], position="sidebar")

seleccionar_dataset()
mostrar_info_dataset()

st.title("Aplicacion de Biodiversidad")
st.write("Selecciona una pagina desde el menu lateral")

pg.run()
