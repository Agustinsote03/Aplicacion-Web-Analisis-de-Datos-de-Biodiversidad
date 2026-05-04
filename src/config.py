from pathlib import Path

ruta_raiz = Path(__file__).parent.parent.parent

ruta_de_datasets = ruta_raiz / "raw_datasets"

CONFIGURACION_DATASETS = {
    "iadiza": {
        "ruta": ruta_de_datasets / "Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI" / "occurrence.txt",
        "separador": "\t",
        "col_lat": "decimalLatitude",
        "col_lon": "decimalLongitude"
    },
    "xeno_canto": {
        "ruta": ruta_de_datasets / "xeno-canto-bird-sounds-filtered" / "Occurrence.txt",
        "separador": ",",
        "col_lat": "latitudeDecimal",
        "col_lon": "longitudeDecimal"
    },
    "inaturalist": {
        "ruta": ruta_de_datasets / "inaturalist-filtered" / "observations.csv",
        "separador": ",",
        "col_lat": "decimalLatitude",
        "col_lon": "decimalLongitude"
    }
}