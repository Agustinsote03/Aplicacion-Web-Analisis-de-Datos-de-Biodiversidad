import streamlit as st 
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from dataset_loader import cargar_dataset, seleccionar_dataset
from config import CONFIGURACION_DATASETS

st.set_page_config(page_title="App Biodiversidad", layout="wide")

seleccionar_dataset()

st.title("Aplicacion de Biodiversidad")
st.write("Selecciona una pagina desde el menu lateral")

