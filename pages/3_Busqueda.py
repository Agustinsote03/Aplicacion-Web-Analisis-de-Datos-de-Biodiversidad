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


#-------EJERICIO 2.B: FILTROS ADICIONALES-------#
st.subheader("Filtros adicionales")
st.markdown("Podés combinar uno o más filtros. El resultado mostrará solo los registros que cumplan todas las condiciones activas.")

# Nombre científico
especies_sel = []
if "scientificName" in df.columns:
    especies = sorted(df["scientificName"].dropna().unique().tolist())
    especies_sel = st.multiselect("Nombre científico", especies)

# Observador
observador = ""
if "recordedBy" in df.columns:
    observador = st.text_input("Observador")

# País (puede llamarse countryCode o country según el dataset)
col_pais = None
paises_sel = []
if "countryCode" in df.columns:
    col_pais = "countryCode"
elif "country" in df.columns:
    col_pais = "country"
if col_pais:
    paises = sorted(df[col_pais].dropna().unique().tolist())
    paises_sel = st.multiselect("País", paises)

# Provincia
col_provincia = None
provincias_sel = []
if "stateProvince" in df.columns:
    col_provincia = "stateProvince"
if col_provincia:
    provincias = sorted(df[col_provincia].dropna().unique().tolist())
    provincias_sel = st.multiselect("Provincia", provincias)

# Rango de fechas
fechas_sel = None
if "eventDate" in df.columns:
    fechas_validas = pd.to_datetime(df["eventDate"], errors="coerce").dropna()
    if not fechas_validas.empty:
        fecha_min = fechas_validas.min().date()
        fecha_max = fechas_validas.max().date()
        usar_fechas = st.checkbox("Filtrar por rango de fechas")
        if usar_fechas:
            fechas_sel = st.date_input("Rango de fechas", value=(fecha_min, fecha_max))

st.markdown("---")

# --- Botón de búsqueda ---
if st.button("Buscar", key="buscar_btn"):
    resultados = df.copy()

    if texto_busqueda.strip():
        resultados = resultados[
            resultados[col_busqueda].astype(str).str.contains(
                texto_busqueda.strip(), case=False, na=False
            )
        ]

    if especies_sel:
        resultados = resultados[resultados["scientificName"].isin(especies_sel)]

    if observador.strip():
        resultados = resultados[
            resultados["recordedBy"].astype(str).str.contains(
                observador.strip(), case=False, na=False
            )
        ]

    if paises_sel and col_pais:
        resultados = resultados[resultados[col_pais].isin(paises_sel)]

    if provincias_sel and col_provincia:
        resultados = resultados[resultados[col_provincia].isin(provincias_sel)]

    if fechas_sel and len(fechas_sel) == 2:
        resultados["eventDate_parsed"] = pd.to_datetime(resultados["eventDate"], errors="coerce")
        resultados = resultados[
            (resultados["eventDate_parsed"] >= pd.Timestamp(fechas_sel[0])) &
            (resultados["eventDate_parsed"] <= pd.Timestamp(fechas_sel[1]))
        ]
        resultados = resultados.drop(columns=["eventDate_parsed"])

    # Guardar en session_state
    st.session_state["resultados_busqueda"] = resultados

#--------EJERCICIO 2.C: MOSTRAR RESULTADOS--------#
if "resultados_busqueda" in st.session_state:
    resultados = st.session_state["resultados_busqueda"]

    st.markdown("---")
    st.subheader(f"Resultados encontrados: {len(resultados)}")

    if resultados.empty:
        st.info("No se encontraron registros.")
    else:
        # Columnas relevantes
        columnas_relevantes = [c for c in [
            "occurrenceID", "scientificName", "recordedBy",
            col_pais, col_provincia, "locality", "eventDate",
            "decimalLatitude", "decimalLongitude"
        ] if c is not None and c in resultados.columns]

        # Ordenamiento
        col_orden = st.selectbox("Ordenar por columna", columnas_relevantes, key="orden_col")
        orden_asc = st.radio("Orden", ["Ascendente", "Descendente"], horizontal=True, key="orden_dir")
        resultados_ordenados = resultados.sort_values(by=col_orden, ascending=(orden_asc == "Ascendente"))

        # Paginación
        registros_por_pagina = 20
        total_paginas = max(1, (len(resultados_ordenados) - 1) // registros_por_pagina + 1)
        pagina = st.number_input("Página", min_value=1, max_value=total_paginas, value=1, step=1, key="pagina")
        inicio = (pagina - 1) * registros_por_pagina
        fin = inicio + registros_por_pagina

        df_pagina = resultados_ordenados[columnas_relevantes].iloc[inicio:fin]
        st.dataframe(df_pagina, use_container_width=True)

        # Detalle de un registro
        st.markdown("#### Ver detalle de un registro")
        indice = st.number_input("Número de fila", min_value=0, max_value=len(resultados_ordenados)-1, value=0, step=1, key="detalle_idx")
        st.dataframe(resultados_ordenados.iloc[[indice]][columnas_relevantes], use_container_width=True)