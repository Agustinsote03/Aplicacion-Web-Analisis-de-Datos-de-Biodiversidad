import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, date
sys.path.append(str(Path(__file__).parent.parent / "src"))

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

if len(logs) == 0:
    st.warning("El log está vacío o no se ha creado todavía el archivo operations.log")
else:
    df_logs = pd.DataFrame(logs)
    
    # Limpieza de datos (fechas inválidas)
    df_logs["Fecha_parsed"] = pd.to_datetime(df_logs["Fecha"], errors="coerce")
    logs_corruptos = df_logs[df_logs["Fecha_parsed"].isna()]
    
    if not logs_corruptos.empty:
        st.warning(f" Se omitieron {len(logs_corruptos)} línea(s) del log por formato de fecha corrupto")
        
    df_logs = df_logs.dropna(subset=["Fecha_parsed"])

    # -- 4.E - Métricas resumidas --
    st.subheader("Resumen de operaciones")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Inserciones", len(df_logs[df_logs["Operación"] == "INSERT"]))
    col2.metric("Total Actualizaciones", len(df_logs[df_logs["Operación"] == "UPDATE"]))
    col3.metric("Total Eliminaciones", len(df_logs[df_logs["Operación"] == "DELETE"]))
    col4.metric("Total Errores", len(df_logs[df_logs["Estado"] == "ERROR"]))

    st.markdown("---")
    st.subheader("Filtrar Registros")

    # Widgets de filtrado
    col_filtros1, col_filtros2 = st.columns(2)
    
    with col_filtros1:
        opciones_op = ["INSERT", "UPDATE", "DELETE", "ERROR"]
        filtro_op = st.multiselect("Tipo de Operación", opciones_op, default=opciones_op)
        
    with col_filtros2:
        rango_fechas = st.date_input("Rango de fechas", [])

    # Aplicación de filtros
    df_filtrado = df_logs[
        (df_logs["Operación"].isin(filtro_op)) | 
        ((df_logs["Estado"] == "ERROR") & ("ERROR" in filtro_op))
    ]

    # Verificamos si el usuario seleccionó ambas fechas (inicio y fin)
    if len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
        mascara_fechas = df_filtrado["Fecha_parsed"].dt.date.between(fecha_inicio, fecha_fin)
        df_filtrado = df_filtrado[mascara_fechas]

    # Mostrar resultados
    st.markdown(f"**{len(df_filtrado)} registro(s)**")
    
    if df_filtrado.empty:
        st.info("No hay registros que coincidan con los filtros aplicados.")
    else:
        st.table(df_filtrado.drop(columns=["Fecha_parsed"]))