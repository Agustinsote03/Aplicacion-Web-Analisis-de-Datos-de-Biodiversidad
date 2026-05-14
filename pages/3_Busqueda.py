import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from dataset_loader import seleccionar_dataset, mostrar_info_dataset

seleccionar_dataset()
mostrar_info_dataset()

st.title("Busqueda")
st.write("Funcionalidad en desarrollo...") # Placeholder