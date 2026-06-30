import pandas as pd
from config import CONFIGURACION_DATASETS
import streamlit as st 
from datetime import datetime
from pathlib import Path 

def cargar_dataset(nombre_dataset):
    """
    Recibe el nombre de un dataset y lo carga como DataFrame de pandas
    desde processed_datasets (los datos ya sanitizados en la primera etapa).
    Si el archivo procesado todavía no existe, lo genera a partir del dataset crudo (raw_datasets) para que la app no se rompa.
    """
    cfg = CONFIGURACION_DATASETS[nombre_dataset]
    ruta_procesado = Path(cfg["ruta_procesado"])

    try:
        df = pd.read_csv(ruta_procesado, sep=cfg["separador"], encoding="utf-8", low_memory=False)
    except FileNotFoundError:
        ruta_procesado.parent.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(cfg["ruta"], sep=cfg["separador"], encoding="utf-8", low_memory=False)
        df.to_csv(ruta_procesado, sep=cfg["separador"], index=False, encoding="utf-8")

    return df

def seleccionar_dataset():
    """
    Muestra un selector en el sidebar para elegir el dataset.
    Guarda la seleccion en session_state para que persista entre paginas
    """

    opciones = list(CONFIGURACION_DATASETS.keys())

    indice = 0
    if "nombre_dataset" in st.session_state:
        if st.session_state["nombre_dataset"] in opciones:
            indice = opciones.index(st.session_state["nombre_dataset"])

    seleccion = st.sidebar.selectbox("Selecciona un dataset", opciones, index=indice)

    if st.session_state.get("nombre_dataset") != seleccion:
        st.session_state["nombre_dataset"] = seleccion
        st.session_state["dataset_actual"] = cargar_dataset(seleccion)
        st.session_state["fecha_seleccion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def mostrar_info_dataset():
    """
    Muestra en el sidebar el nombre del dataset seleccionado, 
    la cantidad de registros y la fecha y hora de seleccion.
    """
    if "dataset_actual" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.write(f" **Dataset:** {st.session_state['nombre_dataset']}")
        st.sidebar.write(f" **Registros:** {len(st.session_state['dataset_actual'])}")
        st.sidebar.write(f" **Cargado:** {st.session_state['fecha_seleccion']}")
        
