import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, date
sys.path.append(str(Path(__file__).parent.parent / "src"))
from dataset_loader import seleccionar_dataset, mostrar_info_dataset

seleccionar_dataset()
mostrar_info_dataset()

st.title("Estado del sistema")
st.write("""
En esta sección se muestran los registros de operaciones realizadas por el sistema.
Esto permite visualizar el historial de acciones sobre los datasets de biodiversidad.
""")

def leer_logs():
    registros = []
    ruta_log = Path(__file__).parent.parent / "logs" / "operations.log"

    try:
        with open(ruta_log, "r", encoding="utf-8") as f:
            for linea in f:
                partes = [p.strip() for p in linea.split("|")]
                if len(partes) < 4:
                    continue

                estado = "ERROR" if "ERROR" in linea else "OK"

                registros.append({
                    "Fecha": partes[0],
                    "Dataset": partes[1],
                    "Operación": partes[2],
                    "Registros": partes[3],
                    "Estado": estado
                })

    except FileNotFoundError:
        st.error("No encuentra el archivo logs/operations.log")

    return registros


logs = leer_logs()

if not logs:
    st.warning("El log está vacío")
else:
    df_logs = pd.DataFrame(logs)

    # -- 4.E - Métricas resumidas --
    st.subheader("Resumen de operaciones")

    total_insert = len(df_logs[df_logs["Operación"] == "INSERT"])
    total_update = len(df_logs[df_logs["Operación"] == "UPDATE"])
    total_delete = len(df_logs[df_logs["Operación"] == "DELETE"])
    total_error = len(df_logs[df_logs["Estado"] == "ERROR"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inserciones", total_insert)
    col2.metric("Actualizaciones", total_update)
    col3.metric("Eliminaciones", total_delete)
    col4.metric("Errores", total_error)

    st.markdown("---")

    # -- 4.E - Filtros --
    st.subheader("Filtrar operaciones")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        tipos = ["Todos"] + sorted(df_logs["Operación"].unique().tolist())
        tipo_seleccionado = st.selectbox("Filtrar por tipo de operación", tipos)

    with col_f2:
        try:
            fechas = pd.to_datetime(df_logs["Fecha"], errors="coerce").dropna()
            fecha_min = fechas.min().date()
            fecha_max = fechas.max().date()
            rango_fechas = st.date_input(
                "Fitrar por rango de fechas",
                value=(fecha_min, fecha_max)
            )
        except Exception:
            rango_fechas = None

    # Aplicar filtros
    df_filtrado = df_logs.copy()

    if tipo_seleccionado != "Todos":
        # Incluir también los ERROR del tipo seleccionado
        if tipo_seleccionado == "ERROR":
            df_filtrado = df_filtrado[df_filtrado["Estado"] == "ERROR"]
        else:
            df_filtrado = df_filtrado[df_filtrado["Operación"] == tipo_seleccionado]

    if rango_fechas and len(rango_fechas) == 2:
        df_filtrado["Fecha_parsed"] = pd.to_datetime(df_filtrado["Fecha"], errors="coerce")
        df_filtrado = df_filtrado[
            (df_filtrado["Fecha_parsed"].isna()) |  # mantiene los registros que no se pudieron parsear
            (
                (df_filtrado["Fecha_parsed"].dt.date >= rango_fechas[0]) &
                (df_filtrado["Fecha_parsed"].dt.date <= rango_fechas[1])
            )
        ]
        df_filtrado = df_filtrado.drop(columns=["Fecha_parsed"])

    st.markdown("---")
    st.subheader(f"Operaciones registradas: {len(df_filtrado)}")
    st.dataframe(df_filtrado, use_container_width=True)