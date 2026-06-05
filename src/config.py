from pathlib import Path

ruta_raiz = Path(__file__).parent.parent
ruta_de_datasets = ruta_raiz / "raw_datasets"
ruta_procesados = ruta_raiz / "processed_datasets"

CONFIGURACION_DATASETS = {
    "iadiza": {
        "ruta": ruta_de_datasets / "Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI" / "occurrence.txt",
        "ruta_procesado": ruta_procesados / "Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI" / "ocurrence.txt",
        "separador": "\t",
        "col_lat": "decimalLatitude",
        "col_lon": "decimalLongitude",
        "ruta_multimedia": None,
    },
    "xeno_canto": {
        "ruta": ruta_de_datasets / "xeno-canto-bird-sounds-filtered" / "Occurrence.txt",
        "ruta_procesado": ruta_procesados / "xeno_canto" / "occurrence.txt",
        "separador": ",",
        "col_lat": "latitudeDecimal",
        "col_lon": "longitudeDecimal",
        "ruta_multimedia": ruta_de_datasets / "xeno-canto-bird-sounds-filtered" / "Multimedia.txt",
    },
    "inaturalist": {
        "ruta": ruta_de_datasets / "inaturalist-filtered" / "observations.csv",
        "ruta_procesado": ruta_procesados / "inaturalist" / "observations.csv",
        "separador": ",",
        "col_lat": "decimalLatitude",
        "col_lon": "decimalLongitude",
        "ruta_multimedia": ruta_de_datasets / "inaturalist-filtered" / "media.csv",
    }
}