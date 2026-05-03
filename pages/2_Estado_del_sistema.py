import streamlit as st

st.title("Estado del sistema")
st.write("""
En esta sección se muestran los registros de operaciones realizadas por el sistema.
Esto permite visualizar el historial de acciones sobre los datasets de biodiversidad.
""")

# Ruta del archivo de logs
log_path = "logs/operations.log"

try:
    # Abrimos el archivo en modo lectura
    with open(log_path, "r", encoding="utf-8") as file:
        # Leemos todas las líneas del archivo y las guardamos en una lista
        lines = file.readlines()

    # Lista donde vamos a guardar los datos ya ordenados
    datos = []

    # Recorremos cada línea del archivo
    for line in lines:

        # Eliminamos espacios/saltos de línea y separamos por comas
        partes = line.strip().split(",")

        # Verificamos que la línea tenga al menos 5 campos
        if len(partes) >= 5:

            # Asignamos cada parte a una variable con significado
            fecha = partes[0]        
            dataset = partes[1]      
            operacion = partes[2]    
            registros = partes[3]    
            estado = partes[4]       

            # Agregamos la fila completa a la lista de datos
            datos.append([fecha, dataset, operacion, registros, estado])

    # Título de la tabla
    st.subheader("Logs de operaciones")

    # Mostramos los datos como tabla en Streamlit
    st.table(datos)

# Si el archivo no existe, mostramos un error en pantalla
except FileNotFoundError:
    st.error("No se encontró el archivo logs/operations.log")