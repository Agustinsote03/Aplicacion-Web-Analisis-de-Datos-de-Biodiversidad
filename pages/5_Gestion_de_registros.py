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
from actualizacion_registros import buscar_registros_generica, actualizar_multiples_campos_validando
from eliminacion_registros import (
        eliminar_por_id_generica,
        eliminar_por_lista_generica,
        eliminar_por_condicion_generica,
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
 
#-------- 4.A - Formulario de inserción ---------#
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


#-------- 4.B y 4.C - Actualizar --------#
with tab_actualizar:
    st.subheader("Actualizar registro")

    # 4.B - Buscar registro por ID
    st.markdown("#### Buscar registro por ID")
    placeholders_id = {
        "iadiza": "ej: IADIZA:COI:006861",
        "xeno_canto": "ej: https://data.biodiversitydata.nl/xeno-canto/observation/XC999540",
        "inaturalist": "ej: https://www.inaturalist.org/observations/12345",
    }

    id_busqueda = st.text_input(
        "Ingresá el occurrenceID del registro a modificar",
        placeholder=placeholders_id[nombre_dataset],
        key="id_actualizar"
    )

    if st.button("Buscar", key="btn_buscar_actualizar"):
        if not id_busqueda.strip():
            st.warning("Ingresá un occurrenceID para buscar")
        else:
            resultados = buscar_registros_generica(
                ruta_origen,
                {"occurrenceID": id_busqueda.strip()},
                separador=cfg["separador"]
            )
            if not resultados:
                st.error(f"No se encontró ningún registro con occurrenceID: '{id_busqueda}'")
                st.session_state.pop("registro_a_editar", None)
            else:
                st.session_state["registro_a_editar"] = resultados[0]
                st.session_state["id_a_actualizar"] = id_busqueda.strip() 
                st.success("Registro encontrado")
            
    # 4.C - Formulario editable
    if "registro_a_editar" in st.session_state:
        registro_actual = st.session_state["registro_a_editar"]
 
        st.markdown("#### Editá los campos del registro")
        st.markdown("Los valores actuales aparecen precargados. Modificá solo los que necesitás")
 
        campos_editar = campos_por_dataset[nombre_dataset]
 
        nuevos_valores = {}
        with st.form("form_actualizar"):
            col1, col2 = st.columns(2)
            mitad = len(campos_editar) // 2
 
            for i, (campo, etiqueta, _) in enumerate(campos_editar):
                valor_actual = registro_actual.get(campo, "")
                with col1 if i < mitad else col2:
                    nuevos_valores[campo] = st.text_input(etiqueta, value=valor_actual, key=f"edit_{campo}")
 
            submitted_actualizar = st.form_submit_button("Guardar cambios")
 
        if submitted_actualizar:
            # Detectar campos modificados
            modificaciones = {
                campo: nuevo
                for campo, nuevo in nuevos_valores.items()
                if nuevo != registro_actual.get(campo, "")
            }
 
            if not modificaciones:
                st.warning("No se realizaron cambios")
            else:
                resultado = actualizar_multiples_campos_validando(
                    ruta_origen,
                    ruta_destino,
                    st.session_state.get("id_a_actualizar", ""),  # ← CORREGIDO
                    modificaciones,
                    nombre_dataset.upper(),
                    separador=cfg["separador"]
                )
 
                if resultado:
                    st.success("Registro actualizado correctamente")
                    st.markdown("**Campos modificados:**")
                    for campo, nuevo in modificaciones.items():
                        st.write(f" **{campo}**: {registro_actual.get(campo, '')} → {nuevo}")
                    # Actualizamos el dataset en session_state
                    st.session_state["dataset_actual"] = cargar_dataset(nombre_dataset)
                    st.session_state.pop("registro_a_editar", None)
                else:
                    st.error("No se pudo actualizar el registro. Revisá los valores ingresados")


#-------- 4.D - Eliminar --------#
with tab_eliminar:
    st.subheader("Eliminar registro")

    modalidad = st.radio(
        "Seleccioná la modalidad de eliminación",
        ["Por identificador único", "Por valor de columna", "Por condición"],
        horizontal=True
    )

    st.markdown("---")

    columnas_dataset = list(st.session_state["dataset_actual"].columns)

    #-- Modalidad 1: por ID --
    if modalidad == "Por identificador único":
        st.markdown("#### Eliminar por occurrenceID")
        placeholders_id = {
            "iadiza": "ej: IADIZA:COI:006861",
            "xeno_canto": "ej: https://data.biodiversitydata.nl/xeno-canto/observation/XC999540",
            "inaturalist": "ej: https://www.inaturalist.org/observations/12345",
        }

        id_eliminar = st.text_input(
            "Ingresá el occurrenceID a eliminar",
            placeholder=placeholders_id[nombre_dataset],
            key="id_eliminar"
        )

        if st.button("Previsualizar", key="btn_preview_id"):
            if not id_eliminar.strip():
                st.warning("Ingresá un occurrenceID")
            else:
                preview = buscar_registros_generica(
                    ruta_origen,
                    {"occurrenceID": id_eliminar.strip()},
                    separador=cfg["separador"]
                )
                if not preview:
                    st.error(f"No se encontró ningún registro con occurrenceID: '{id_eliminar}'")
                    st.session_state.pop("preview_eliminar", None)
                else:
                    st.session_state["preview_eliminar"] = preview
                    st.session_state["modalidad_eliminar"] = "id"

        if st.session_state.get("modalidad_eliminar") == "id" and "preview_eliminar" in st.session_state:
            st.warning(f"Se eliminará {len(st.session_state['preview_eliminar'])} registro(s):")
            st.dataframe(st.session_state["preview_eliminar"], use_container_width=True)

            if st.button("Confirmar eliminación", key="btn_confirmar_id"):
                resultado = eliminar_por_id_generica(
                    ruta_origen, ruta_destino,
                    "occurrenceID", id_eliminar.strip(),
                    nombre_dataset=nombre_dataset.upper(),
                    separador=cfg["separador"]
                )
                if resultado:
                    st.success(f"Se eliminó {resultado} registro(s) correctamente")
                    st.session_state["dataset_actual"] = cargar_dataset(nombre_dataset)
                    st.session_state.pop("preview_eliminar", None)
                    st.session_state.pop("modalidad_eliminar", None)
                else:
                    st.error("No se pudo eliminar el registro")

    #-- Modalidad 2: Por valor de columna --
    elif modalidad == "Por valor de columna":
        st.markdown("#### Eliminar por valor de columna")
        col_eliminar = st.selectbox("Seleccioná la columna", columnas_dataset, key="col_lista")
        valores_texto = st.text_input("Ingresá los valores a eliminar separados por coma", key="valores_lista")

        if st.button("Previsualizar", key="btn_preview_lista"):
            if not valores_texto.strip():
                st.warning("Ingresá al menos un valor")
            else:
                valores = [v.strip() for v in valores_texto.split(",")]
                df = st.session_state["dataset_actual"]
                preview = df[df[col_eliminar].astype(str).isin(valores)]
                if preview.empty:
                    st.error("No se encontraron registros con esos valores")
                    st.session_state.pop("preview_eliminar", None)
                else:
                    st.session_state["preview_eliminar"] = preview
                    st.session_state["modalidad_eliminar"] = "lista"
                    st.session_state["valores_eliminar"] = valores

        if st.session_state.get("modalidad_eliminar") == "lista" and "preview_eliminar" in st.session_state:
            st.warning(f"Se eliminarán {len(st.session_state['preview_eliminar'])} registro(s):")
            st.dataframe(st.session_state["preview_eliminar"], use_container_width=True)

            if st.button("Confirmar eliminación", key="btn_confirmar_lista"):
                resultado = eliminar_por_lista_generica(
                    ruta_origen, ruta_destino,
                    col_eliminar,
                    st.session_state["valores_eliminar"],
                    nombre_dataset=nombre_dataset.upper(),
                    separador=cfg["separador"]
                )
                if resultado:
                    st.success(f"Se eliminaron {resultado} registro(s) correctamente")
                    st.session_state["dataset_actual"] = cargar_dataset(nombre_dataset)
                    st.session_state.pop("preview_eliminar", None)
                    st.session_state.pop("modalidad_eliminar", None)
                else:
                    st.error("No se eliminó ningún registro")
    
    #-- Modalidad 3: Por condición --
    elif modalidad == "Por condición":
        st.markdown("#### Eliminar por condición")
        col_condicion = st.selectbox("Seleccioná la columna", columnas_dataset, key="col_condicion")
        operador = st.selectbox("Operador", ["==", "!=", ">", ">=", "<", "<="], key="operador")
        valor_condicion = st.text_input("Valor de referencia", key="valor_condicion")

        if st.button("Previsualizar", key="btn_preview_condicion"):
            if not valor_condicion.strip():
                st.warning("Ingresá un valor de referencia")
            else:
                df = st.session_state["dataset_actual"]
                try:
                    col_num = pd.to_numeric(df[col_condicion], errors="coerce")
                    val_num = float(valor_condicion)
                    if operador == "==":
                        preview = df [col_num == val_num]
                    elif operador == "!=":
                        preview = df[col_num != val_num]
                    elif operador == ">":
                        preview = df[col_num > val_num]
                    elif operador == ">=":
                        preview = df[col_num >= val_num]
                    elif operador == "<":
                        preview = df[col_num < val_num]
                    elif operador == "<=":
                        preview = df[col_num <= val_num]
                except ValueError:
                    if operador == "==":
                        preview = df[df[col_condicion].astype(str) == valor_condicion]
                    elif operador == "!=":
                        preview = df[df[col_condicion].astype(str) != valor_condicion]
                    else:
                        st.error("Para comparaciones numéricas el valor debe ser un número")
                        preview = pd.DataFrame()

                if preview.empty:
                    st.error("No se encontraron registros que cumplan la condición")
                    st.session_state.pop("preview_eliminar", None)
                else:
                    st.session_state["preview_eliminar"] = preview
                    st.session_state["modalidad_eliminar"] = "condicion"

        if st.session_state.get("modalidad_eliminar") == "condicion" and "preview_eliminar" in st.session_state:
            st.warning(f"Se eliminarán {len(st.session_state['preview_eliminar'])} registro(s):")
            st.dataframe(st.session_state["preview_eliminar"], use_container_width=True)

            if st.button("Confirmar eliminación", key="btn_confirmar_condicion"):
                resultado = eliminar_por_condicion_generica(
                    ruta_origen, ruta_destino,
                    col_condicion, operador, valor_condicion,
                    nombre_dataset=nombre_dataset.upper(),
                    separador=cfg["separador"]
                )
                if resultado:
                    st.success(f"Se eliminaron {resultado} registro(s) correctamente")
                    st.session_state["dataset_actual"] = cargar_dataset(nombre_dataset)
                    st.session_state.pop("preview_eliminar", None)
                    st.session_state.pop("modalidad_eliminar", None)
                else:
                    st.error("No se eliminó ningún registro")