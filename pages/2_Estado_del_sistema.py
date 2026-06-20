import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from estado_sistema import leer_logs, limpiar_logs

st.title("Estado del sistema")
st.write("""
En esta sección se muestran los registros de operaciones realizadas por el sistema.
Esto permite visualizar el historial de acciones sobre los datasets de biodiversidad.
""")

ruta_log = Path(__file__).parent.parent / "logs" / "operations.log"
logs = leer_logs(ruta_log)

if logs is None:
    st.error("No encuentra el archivo logs/operations.log")
elif len(logs) == 0:
    st.warning("El log está vacío o no se ha creado todavía el archivo operations.log")
else:
    df_logs, cant_corruptos = limpiar_logs(logs)

    if cant_corruptos > 0:
        st.warning(f" Se omitieron {cant_corruptos} línea(s) del log por formato de fecha corrupto")

    # -- 4.E - Métricas resumidas --
    st.subheader("Resumen de operaciones")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Inserciones", len(df_logs[df_logs["Operación"] == "INSERT"]))
    col2.metric("Total Actualizaciones", len(df_logs[df_logs["Operación"] == "UPDATE"]))
    col3.metric("Total Eliminaciones", len(df_logs[df_logs["Operación"] == "DELETE"]))
    col4.metric("Total Errores", len(df_logs[df_logs["Estado"] == "ERROR"]))

    st.markdown("---")
    st.subheader("Filtrar Registros")

    col_filtros1, col_filtros2 = st.columns(2)

    with col_filtros1:
        opciones_op = ["INSERT", "UPDATE", "DELETE", "ERROR"]
        filtro_op = st.multiselect("Tipo de Operación", opciones_op, default=opciones_op)

    with col_filtros2:
        rango_fechas = st.date_input("Rango de fechas", [])

    df_filtrado = df_logs[
        (df_logs["Operación"].isin(filtro_op)) |
        ((df_logs["Estado"] == "ERROR") & ("ERROR" in filtro_op))
    ]

    if len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
        mascara_fechas = df_filtrado["Fecha_parsed"].dt.date.between(fecha_inicio, fecha_fin)
        df_filtrado = df_filtrado[mascara_fechas]

    st.markdown(f"**{len(df_filtrado)} registro(s)**")

    if df_filtrado.empty:
        st.info("No hay registros que coincidan con los filtros aplicados.")
    else:
        st.table(df_filtrado.drop(columns=["Fecha_parsed"]))