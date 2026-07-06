import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
from busqueda import buscar_por_texto, buscar_por_filtros, obtener_columna_pais, obtener_columnas_relevantes, paginar_resultados, calcular_resumen

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

#--------EJERCICIO 2.A y 2.B: MODO DE BÚSQUEDA--------#
modo = st.radio("Modo de búsqueda", ["Búsqueda por texto libre", "Filtros avanzados"], horizontal=True)

st.markdown("---")

# Variables con valores por defecto
col_busqueda = columnas[0]
texto_busqueda = ""
especies_sel = []
observador_sel = []
col_pais = None
paises_sel = []
col_provincia = None
provincias_sel = []
fechas_sel = None

if modo == "Búsqueda por texto libre":
    st.subheader("Búsqueda por texto libre")
    st.markdown("Seleccioná una columna e ingresá el texto que querés buscar.")
    col_busqueda = st.selectbox("Seleccioná la columna", columnas)
    texto_busqueda = st.text_input("Texto a buscar")

    st.markdown("---")

    if st.button("Buscar por texto", key="buscar_texto_btn"):
        resultados = buscar_por_texto(df, col_busqueda, texto_busqueda)
        st.session_state["resultados_busqueda"] = resultados

elif modo == "Filtros avanzados":
    st.subheader("Filtros avanzados")
    st.markdown("Podés combinar uno o más filtros. El resultado mostrará solo los registros que cumplan todas las condiciones activas.")

    if "scientificName" in columnas:
        especies = sorted(df["scientificName"].dropna().unique().tolist())
        especies_sel = st.multiselect("Nombre científico", especies)

    if "recordedBy" in columnas:
        observador_sel = st.text_input("Observador")

    col_pais = obtener_columna_pais(columnas)
    if col_pais:
        paises = sorted(df[col_pais].dropna().unique().tolist())
        paises_sel = st.multiselect("País", paises)

    if "stateProvince" in columnas:
        col_provincia = "stateProvince"
        provincias = sorted(df[col_provincia].dropna().unique().tolist())
        provincias_sel = st.multiselect("Provincia", provincias)

    if "eventDate" in columnas:
        fechas_validas = pd.to_datetime(df["eventDate"], errors="coerce", utc=True).dropna()
        if not fechas_validas.empty:
            fecha_min = fechas_validas.min().date()
            fecha_max = fechas_validas.max().date()
            fechas_sel = st.date_input("Rango de fechas", value=(fecha_min, fecha_max))

    st.markdown("---")

    if st.button("Buscar por filtros", key="buscar_filtros_btn"):
        resultados = buscar_por_filtros(df, especies_sel, observador_sel, col_pais, paises_sel, col_provincia, provincias_sel, fechas_sel)
        st.session_state["resultados_busqueda"] = resultados

st.markdown("---")

#--------EJERCICIO 2.C: MOSTRAR RESULTADOS--------#
if "resultados_busqueda" in st.session_state:
    resultados = st.session_state["resultados_busqueda"]

    st.markdown("---")
    st.subheader(f"Resultados encontrados: {len(resultados)}")

    if resultados.empty:
        st.info("No se encontraron registros.")
    else:
        # Columnas relevantes
        columnas_relevantes = obtener_columnas_relevantes(resultados, col_pais, col_provincia)

        # Ordenamiento
        col_orden = st.selectbox("Ordenar por columna", columnas_relevantes, key="orden_col")
        orden_asc = st.radio("Orden", ["Ascendente", "Descendente"], horizontal=True, key="orden_dir")
        resultados_ordenados = resultados.sort_values(by=col_orden, ascending=(orden_asc == "Ascendente"))

        # Paginación
        registros_por_pagina = 20
        total_paginas = max(1, (len(resultados_ordenados) - 1) // registros_por_pagina + 1)
        pagina = st.number_input("Página", min_value=1, max_value=total_paginas, value=1, step=1, key="pagina")
        df_pagina = paginar_resultados(resultados_ordenados[columnas_relevantes], pagina, registros_por_pagina)
        st.dataframe(df_pagina, use_container_width=True)

        # Detalle de un registro
        st.markdown("#### Ver detalle de un registro")
        indice = st.number_input("Número de fila", min_value=0, max_value=len(resultados_ordenados)-1, value=0, step=1, key="detalle_idx")
        st.dataframe(resultados_ordenados.iloc[[indice]], use_container_width=True)

        #--------EJERCICIO 2.D: EXPORTAR CSV--------#
        st.markdown("---")
        
        nombre_archivo = f"{st.session_state['nombre_dataset']}_{datetime.now().strftime('%Y%m%d')}.csv"
        csv = resultados_ordenados[columnas_relevantes].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Exportar resultados",
            data=csv,
            file_name=nombre_archivo,
            mime="text/csv",
            key="exportar_btn"
        )
    
        #--------EJERCICIO 2.E: RESUMEN ESTADÍSTICO--------#
        st.markdown("---")
        st.subheader("Resumen estadístico")
        st.markdown("Información sobre el subconjunto de registros encontrados.")

        resumen = calcular_resumen(resultados, col_pais, col_provincia)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Especies únicas", resumen["especies_unicas"])
        with col2:
            st.metric("Países representados", resumen["paises_repr"])
        with col3:
            st.metric("Provincias representadas", resumen["provincias_repr"])
        with col4:
            st.metric("Observadores", resumen["observadores"])

    #------------EJERCICIO 6.A: BOTÓN VER FICHA------------#
        st.markdown("---")
        if st.button("Ver ficha", key="ver_ficha_btn"):
            st.session_state["resultados_busqueda"] = resultados  
            st.switch_page("pages/7_Ficha.py")