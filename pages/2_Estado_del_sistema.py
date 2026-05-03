import streamlit as st

st.title("Estado del sistema")
st.write("""
En esta sección se muestran los registros de operaciones realizadas por el sistema.
Esto permite visualizar el historial de acciones sobre los datasets de biodiversidad.
""")

def leer_logs():
    registros = []

    try:
        with open("logs/operations.log", "r", encoding="utf-8") as f:
            for linea in f:
                partes = [p.strip() for p in linea.split("|")]

                estado = "OK"
                if "ERROR" in linea:
                    estado = "ERROR"

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


st.title("📊 Estado del sistema")

logs = leer_logs()

if len(logs) == 0:
    st.warning("El log está vacío")
else:
    st.table(logs)