import streamlit as st
import sys
import pandas as pd
from pathlib import Path
 
sys.path.append(str(Path(__file__).parent.parent / "src"))
 
from dataset_loader import seleccionar_dataset, mostrar_info_dataset, cargar_dataset
from insercion_registros import (
    crear_estructura_registro_iadiza,
    crear_estructura_registro_xeno_canto,
    crear_estructura_registro_inaturalist,
    validar_registro_iadiza,
    validar_registro_xeno_canto,
    validar_registro_inaturalist,
    preparar_estructura_iadiza,
    preparar_estructura_xeno_canto,
    preparar_estructura_inaturalist,
    insertar_registro,
)
from config import CONFIGURACION_DATASETS
 
# Mapeo de funciones por dataset
funciones_por_dataset = {
    "iadiza": {
        "crear": crear_estructura_registro_iadiza,
        "validar": validar_registro_iadiza,
        "preparar": preparar_estructura_iadiza,
    },
    "xeno_canto": {
        "crear": crear_estructura_registro_xeno_canto,
        "validar": validar_registro_xeno_canto,
        "preparar": preparar_estructura_xeno_canto,
    },
    "inaturalist": {
        "crear": crear_estructura_registro_inaturalist,
        "validar": validar_registro_inaturalist,
        "preparar": preparar_estructura_inaturalist,
    },
}
 
# Campos del formulario por dataset
campos_por_dataset = {
    "iadiza": [
        ("license", "Licencia", "ej: CC_BY_NC_4_0"),
        ("institutionCode", "Código de institución", "ej: IADIZA"),
        ("collectionCode", "Código de colección", "ej: COI"),
        ("basisOfRecord", "Base del registro", "ej: PRESERVED_SPECIMEN"),
        ("occurrenceStatus", "Estado de ocurrencia", "PRESENT/ABSENT"),
        ("recordedBy", "Registrado por", ""),
        ("eventDate", "Fecha del evento", ""),
        ("year", "Año", ""),
        ("month", "Mes", ""),
        ("day", "Día", ""),
        ("countryCode", "Código de país", "ej: AR"),
        ("stateProvince", "Provincia", ""),
        ("locality", "Localidad", ""),
        ("decimalLatitude", "Latitud decimal", ""),
        ("decimalLongitude", "Longitud decimal", ""),
        ("coordinateUncertaintyInMeters", "Incertidumbre (metros)", ""),
        ("scientificName", "Nombre científico", ""),
        ("kingdom", "Reino", ""),
        ("phylum", "Filo", ""),
        ("taxonClass", "Clase", ""),
        ("order", "Orden", ""),
        ("family", "Familia", ""),
        ("genus", "Género", ""),
        ("specificEpithet", "Epíteto específico", ""),
        ("taxonRank", "Rango taxonómico", ""),
    ],
    "xeno_canto": [
        ("basisOfRecord", "Base del registro", "ej: HUMAN_OBSERVATION"),
        ("collectionCode", "Código de colección", ""),
        ("genus", "Género", ""),
        ("scientificName", "Nombre científico", ""),
        ("taxonRank", "Rango taxonómico", ""),
        ("kingdom", "Reino", ""),
        ("family", "Familia", ""),
        ("longitudeDecimal", "Longitud decimal", ""),
        ("latitudeDecimal", "Latitud decimal", ""),
        ("country", "País", "ej: Argentina"),
        ("locality", "Localidad", ""),
        ("recordedBy", "Registrado por", ""),
        ("eventDate", "Fecha del evento", ""),
        ("license", "Licencia", ""),
    ],
    "inaturalist": [
        ("basisOfRecord", "Base del registro", "ej: HUMAN_OBSERVATION"),
        ("institutionCode", "Código de institución", ""),
        ("recordedBy", "Registrado por", ""),
        ("eventDate", "Fecha del evento", ""),
        ("decimalLatitude", "Latitud decimal", ""),
        ("decimalLongitude", "Longitud decimal", ""),
        ("coordinateUncertaintyInMeters", "Incertidumbre (metros)", ""),
        ("countryCode", "Código de país", ""),
        ("stateProvince", "Provincia", ""),
        ("scientificName", "Nombre científico", ""),
        ("taxonRank", "Rango taxonómico", ""),
        ("kingdom", "Reino", ""),
        ("family", "Familia", ""),
        ("genus", "Género", ""),
        ("license", "Licencia", ""),
    ],
}
 
# Campos obligatorios por dataset
campos_obligatorios = {
    "iadiza": ["scientificName", "decimalLatitude", "decimalLongitude", "eventDate", "countryCode"],
    "xeno_canto": ["scientificName", "latitudeDecimal", "longitudeDecimal", "eventDate"],
    "inaturalist": ["scientificName", "decimalLatitude", "decimalLongitude", "eventDate", "countryCode"],
}
 
# Sidebar
seleccionar_dataset()
mostrar_info_dataset()
 
st.title("Gestión de Registros")
st.markdown("""
En esta sección podés **Insertar**, **Actualizar** o **Eliminar** registros 
del dataset que tengas seleccionado.
""")
 
# Verificar que haya un dataset cargado en la sesión
if "nombre_dataset" not in st.session_state:
    st.warning("Seleccioná un dataset desde el menú lateral.")
    st.stop()
 
df = st.session_state["dataset_actual"]
nombre_dataset = st.session_state["nombre_dataset"]
cfg = CONFIGURACION_DATASETS[nombre_dataset]
ruta_origen = cfg["ruta"]
ruta_destino = cfg["ruta_procesado"]
 
# Pestañas
tab_insertar, tab_actualizar, tab_eliminar = st.tabs(["Insertar", "Actualizar", "Eliminar"])
 
# ── 4.A — Formulario de inserción ───────────────────────
with tab_insertar:
    st.subheader("Insertar nuevo registro")
    st.markdown("Completá los campos del nuevo registro. Los campos marcados con * son obligatorios.")
 
    campos = campos_por_dataset[nombre_dataset]
    obligatorios = campos_obligatorios[nombre_dataset]
    funciones = funciones_por_dataset[nombre_dataset]
 
    valores = {}
    with st.form("form_insercion"):
        col1, col2 = st.columns(2)
        mitad = len(campos) // 2
 
        for i, (campo, etiqueta, placeholder) in enumerate(campos):
            label = f"{etiqueta} *" if campo in obligatorios else etiqueta
            with col1 if i < mitad else col2:
                valores[campo] = st.text_input(label, placeholder=placeholder)
 
        submitted = st.form_submit_button("Insertar registro")
 
    if submitted:
        # Validar campos obligatorios
        faltantes = [
            etiqueta for campo, etiqueta, _ in campos
            if campo in obligatorios and not valores[campo].strip()
        ]
 
        if faltantes:
            st.error("Los siguientes campos son obligatorios:")
            for campo in faltantes:
                st.warning(f" {campo}")
        else:
            # Crear registro según el dataset
            registro = funciones["crear"](**{k: v for k, v in valores.items()})
 
            # Validar registro
            es_valido, errores = funciones["validar"](registro)
 
            if not es_valido:
                st.error("El registro tiene errores. Corregí los siguientes campos:")
                for error in errores:
                    st.warning(f" {error}")
            else:
                if nombre_dataset == "iadiza":
                    preparar = lambda r, ruta, cols: funciones["preparar"](r, ruta, cols, nombre_dataset.upper())
                else:
                    preparar = lambda r, ruta, cols: funciones["preparar"](r, ruta, cols)
 
                insertar_registro(
                    ruta_origen,
                    ruta_destino,
                    registro,
                    nombre_dataset.upper(),
                    preparar_fn=preparar,
                    validar_fn=funciones["validar"],
                )
                st.success("Registro insertado correctamente.")
                # Recargamos el dataset en session_state para reflejar el cambio
                st.session_state["dataset_actual"] = cargar_dataset(nombre_dataset)
