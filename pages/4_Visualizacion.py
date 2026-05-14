import streamlit as st 
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from dataset_loader import seleccionar_dataset

seleccionar_dataset()

st.title("Visualizacion")
st.write("Funcionalidad en desarrollo...") # Placeholder
