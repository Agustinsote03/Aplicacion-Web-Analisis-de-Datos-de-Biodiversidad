import streamlit as st
import sys
import pandas as pd
from pathlib import Path

ruta_raiz = Path.cwd().parent
print(f"Ruta del directorio raiz: ", ruta_raiz)

ruta_de_src = Path(ruta_raiz / "src")
print(f"Ruta src: ", ruta_de_src)

# Se añade la ruta raíz al sys.path para poder importar módulos
sys.path.append(str(ruta_de_src))
from dataset_loader import seleccionar_dataset, mostrar_info_dataset

ruta_de_datasets = ruta_raiz / "processed_datasets"
#Ruta de los datasets procesados
print(f"Ruta de archivos: ", ruta_de_datasets)

ruta_raiz = Path(__file__).parent.parent
RUTAS_PROCESADOS = {
    "iadiza": ruta_raiz / "processed_datasets" / "IADIZA" / "occurrence.txt",
    "xeno_canto": ruta_raiz / "processed_datasets" / "Xeno-canto" / "occurrence.txt",
    "inaturalist": ruta_raiz / "processed_datasets" / "iNaturalist" / "occurrence.txt",
}

#Sidebar: selector e información de datasets
seleccionar_dataset()
mostrar_info_dataset()

st.title("Búsqueda")
st.markdown("""
Esta página permite buscar registros dentro del dataset seleccionado.
Podés elegir la columna por la que querés buscar e ingresar un texto.
La búsqueda no distingue mayúsculas de minúsculas.
""")

#Verificar que haya un dataset cargado en la sesión
if "nombre_dataset" not in st.session_state:
    st.warning("Seleccioná un dataset desde el menú lateral.")
    st.stop()

#Obtener el dataframe del dataset seleccionado
df = st.session_state["dataset_actual"]
columnas = list(df.columns)

#--------EJERCICIO 2.A: BÚSQUEDA POR TEXTO LIBRE--------#
st.subheader("Búsqueda por texto libre")
st.markdown("Seleccioná una columna e ingresá el texto que querés buscar.")

col_busqueda = st.selectbox("Seleccioná la columna", columnas)
texto_busqueda = st.text_input("Texto a buscar")

if st.button("Buscar"):
    if texto_busqueda.strip():
        # Búsqueda case-insensitive como subcadena en la columna seleccionada
        resultados = df[
            df[col_busqueda].astype(str).str.contains(
                texto_busqueda.strip(), case=False, na=False
            )
        ]
        st.write(f"Resultados encontrados: {len(resultados)}")
        st.dataframe(resultados, use_container_width=True)
    else:
        st.warning("Ingresá un texto para buscar.")
