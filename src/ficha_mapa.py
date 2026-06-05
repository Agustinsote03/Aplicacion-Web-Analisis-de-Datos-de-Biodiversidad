import pandas as pd
import folium

# Paleta de colores disponibles en folium
COLORES = [
    "red", "blue", "green", "purple", "orange", "darkred",
    "lightred", "beige", "darkblue", "darkgreen", "cadetblue",
    "darkpurple", "pink", "lightblue", "lightgreen",
    "gray", "black", "lightgray"
]

# Mapeo de colores folium a CSS para la leyenda
CSS_COLORES = {
    "red": "#e74c3c", "blue": "#3498db", "green": "#2ecc71",
    "purple": "#9b59b6", "orange": "#e67e22", "darkred": "#c0392b",
    "darkblue": "#1a5276", "darkgreen": "#1e8449", "cadetblue": "#5dade2",
    "darkpurple": "#76448a", "pink": "#f1948a", "lightblue": "#85c1e9",
    "lightgreen": "#a9dfbf", "gray": "#7f8c8d", "black": "#2c3e50",
    "lightgray": "#bdc3c7", "beige": "#f0e68c", "lightred": "#f1948a",
}


def detectar_columnas_coordenadas(df):
    """
    Detecta los nombres de las columnas de latitud y longitud según el dataset.
    xeno-canto usa latitudeDecimal/longitudeDecimal,
    los demás usan decimalLatitude/decimalLongitude.
    Retorna una tupla (col_lat, col_lon).
    """
    if "latitudeDecimal" in df.columns and "longitudeDecimal" in df.columns:
        return "latitudeDecimal", "longitudeDecimal"
    return "decimalLatitude", "decimalLongitude"


def detectar_columna_pais(df):
    """
    Detecta si la columna de país se llama 'countryCode' o 'country'.
    Retorna el nombre de la columna o None si no existe ninguna.
    """
    if "countryCode" in df.columns:
        return "countryCode"
    if "country" in df.columns:
        return "country"
    return None


def es_coordenada_valida(lat, lon):
    """
    Verifica que lat y lon sean números dentro de los rangos geográficos válidos.
    Retorna True si ambas coordenadas son válidas, False en caso contrario.
    """
    try:
        lat_f = float(lat)
        lon_f = float(lon)
        return -90 <= lat_f <= 90 and -180 <= lon_f <= 180
    except (ValueError, TypeError):
        return False


def separar_por_coordenadas(df, col_lat, col_lon):
    """
    Divide el DataFrame en dos: registros con coordenadas válidas e inválidas.
    Retorna una tupla (df_validos, df_invalidos).
    """
    mascara = df.apply(
        lambda fila: es_coordenada_valida(fila.get(col_lat), fila.get(col_lon)),
        axis=1
    )
    return df[mascara].copy(), df[~mascara].copy()


def obtener_opciones_coloreo(df, col_pais):
    """
    Construye un diccionario con los criterios de coloreo disponibles
    según las columnas presentes en el DataFrame.
    Las claves son etiquetas legibles y los valores son nombres de columna.
    """
    opciones = {}
    if col_pais and col_pais in df.columns:
        opciones["País"] = col_pais
    if "scientificName" in df.columns:
        opciones["Especie (scientificName)"] = "scientificName"
    if "institutionCode" in df.columns:
        opciones["Institución (institutionCode)"] = "institutionCode"
    if "stateProvince" in df.columns:
        opciones["Provincia (stateProvince)"] = "stateProvince"
    if "family" in df.columns:
        opciones["Familia"] = "family"
    if not opciones:
        opciones["(Sin criterio)"] = None
    return opciones


def construir_mapa_colores(df, col_color):
    """
    Asigna un color de la paleta a cada valor único de la columna col_color.
    Retorna un diccionario {valor: color_folium}.
    """
    if not col_color:
        return {}
    valores = df[col_color].fillna("(sin dato)").astype(str).unique()
    return {
        valor: COLORES[i % len(COLORES)]
        for i, valor in enumerate(sorted(valores))
    }


def construir_popup(fila, col_pais):
    """
    Genera el HTML del popup para un marcador del mapa.
    Incluye nombre científico, fecha, observador, localidad, país e ID.
    """
    nombre_cientifico = fila.get("scientificName", "—")
    fecha = fila.get("eventDate", "—")
    observador = fila.get("recordedBy", "—")
    localidad = fila.get("locality", "—")
    occurrence_id = fila.get("occurrenceID", "—")
    pais_val = fila.get(col_pais, "—") if col_pais else "—"

    return f"""
    <div style="font-family: sans-serif; min-width: 180px;">
        <b style="font-size:13px;">{nombre_cientifico}</b><br>
        <hr style="margin:4px 0">
        <b>Fecha:</b> {fecha}<br>
        <b>Observador:</b> {observador}<br>
        <b>Localidad:</b> {localidad}<br>
        <b>País:</b> {pais_val}<br>
        <b>ID:</b> <small>{occurrence_id}</small>
    </div>
    """


def construir_mapa(df_validos, col_lat, col_lon, col_color, mapa_colores, col_pais):
    """
    Construye y retorna un objeto folium.Map con un marcador por cada registro.
    El mapa se centra en el promedio de las coordenadas válidas.
    """
    lat_centro = df_validos[col_lat].astype(float).mean()
    lon_centro = df_validos[col_lon].astype(float).mean()

    mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=5)

    for _, fila in df_validos.iterrows():
        lat = float(fila[col_lat])
        lon = float(fila[col_lon])

        if col_color:
            valor_color = str(fila.get(col_color) or "(sin dato)")
            color = mapa_colores.get(valor_color, "blue")
        else:
            color = "blue"

        popup_html = construir_popup(fila, col_pais)
        nombre_cientifico = fila.get("scientificName", "")

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=nombre_cientifico,
            icon=folium.Icon(color=color, icon="leaf", prefix="fa"),
        ).add_to(mapa)

    return mapa