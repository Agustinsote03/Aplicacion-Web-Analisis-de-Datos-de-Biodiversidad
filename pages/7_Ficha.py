import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
from dataset_loader import seleccionar_dataset, mostrar_info_dataset
from ficha_mapa import (
    detectar_columnas_coordenadas,
    detectar_columna_pais,
    separar_por_coordenadas,
    obtener_opciones_coloreo,
    construir_mapa_colores,
    construir_mapa,
)

try:
    from streamlit_folium import st_folium
except ImportError:
    st.error("Instalá las dependencias: `pip install folium streamlit-folium`")
    st.stop()


def verificar_resultados():
    """
    Verifica que haya resultados de búsqueda en la sesión.
    Detiene la página si no hay o están vacíos.
    """
    if "resultados_busqueda" not in st.session_state:
        st.warning("No hay resultados de búsqueda. Realizá una búsqueda en la página de Búsqueda primero.")
        st.stop()

    resultados = st.session_state["resultados_busqueda"]
    st.write("DEBUG - Registros recibidos:", len(resultados))  # DEBUG

    if resultados.empty:
        st.info("No hay registros para mostrar en el mapa.")
        st.stop()

    return resultados


def mostrar_metricas(df_validos, df_invalidos, total):
    """
    Muestra las métricas de registros incluidos, excluidos y total.
    Si hay excluidos, muestra un aviso al usuario.
    """
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros en el mapa", len(df_validos))
    col2.metric("Registros excluidos", len(df_invalidos), help="Coordenadas nulas o inválidas")
    col3.metric("Total de resultados", total)

    if not df_invalidos.empty:
        st.warning(f"Se excluyeron **{len(df_invalidos)}** registro(s) del mapa por coordenadas nulas o inválidas.")


def mostrar_selector_coloreo(df_validos, col_pais):
    """
    Muestra el selector de criterio de coloreo y retorna
    la columna elegida y el mapa de colores correspondiente.
    """
    st.subheader("Configuración del mapa")
    opciones_color = obtener_opciones_coloreo(df_validos, col_pais)
    criterio_label = st.selectbox("Colorear puntos por:", list(opciones_color.keys()))
    col_color = opciones_color[criterio_label]
    mapa_colores = construir_mapa_colores(df_validos, col_color)
    return criterio_label, col_color, mapa_colores


def mostrar_leyenda(criterio_label, col_color, mapa_colores):
    """
    Muestra la leyenda de colores debajo del selector.
    Si hay más de 20 valores distintos, informa al usuario y la omite.
    """
    if not col_color:
        return

    css_map = {
        "red": "#e74c3c", "blue": "#3498db", "green": "#2ecc71",
        "purple": "#9b59b6", "orange": "#e67e22", "darkred": "#c0392b",
        "darkblue": "#1a5276", "darkgreen": "#1e8449", "cadetblue": "#5dade2",
        "darkpurple": "#76448a", "pink": "#f1948a", "lightblue": "#85c1e9",
        "lightgreen": "#a9dfbf", "gray": "#7f8c8d", "black": "#2c3e50",
        "lightgray": "#bdc3c7", "beige": "#f0e68c", "lightred": "#f1948a",
    }

    if len(mapa_colores) > 20:
        st.info(f"Hay {len(mapa_colores)} valores distintos en '{criterio_label}'. La leyenda se omite por extensión.")
        return

    st.markdown(f"**Leyenda — {criterio_label}:**")
    cols = st.columns(min(4, len(mapa_colores)))
    for i, (valor, color) in enumerate(sorted(mapa_colores.items())):
        css_color = css_map.get(color, "#3498db")
        cols[i % 4].markdown(
            f"<span style='background:{css_color}; color:white; padding:2px 8px; "
            f"border-radius:4px; font-size:12px;'>⬤ {valor}</span>",
            unsafe_allow_html=True
        )
    st.markdown("")


def mostrar_mapa(df_validos, col_lat, col_lon, col_color, mapa_colores, col_pais):
    """
    Construye y renderiza el mapa interactivo con folium.
    """
    st.subheader("Mapa de ocurrencias")
    mapa = construir_mapa(df_validos, col_lat, col_lon, col_color, mapa_colores, col_pais)
    st_folium(mapa, width="100%", height=550, returned_objects=[])


def main():
    seleccionar_dataset()
    mostrar_info_dataset()

    st.title("Ficha de datos")
    st.markdown("Esta página muestra el detalle de los registros seleccionados en la búsqueda.")

    resultados = verificar_resultados()

    col_lat, col_lon = detectar_columnas_coordenadas(resultados)
    col_pais = detectar_columna_pais(resultados)

    
    df_validos, df_invalidos = separar_por_coordenadas(resultados, col_lat, col_lon)

    mostrar_metricas(df_validos, df_invalidos, len(resultados))

    if df_validos.empty:
        st.error("Ningún registro tiene coordenadas válidas para mostrar en el mapa.")
        st.stop()

    criterio_label, col_color, mapa_colores = mostrar_selector_coloreo(df_validos, col_pais)
    mostrar_leyenda(criterio_label, col_color, mapa_colores)
    mostrar_mapa(df_validos, col_lat, col_lon, col_color, mapa_colores, col_pais)


main()