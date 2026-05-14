import pandas as pd
from config import CONFIGURACION_DATASETS

def cargar_dataset(nombre_dataset):
    """
    Recibe el nombre de un dataset, lo carga como DataFrame de pandas.
    y retorna el DataFrame resultante
    """
    cfg = CONFIGURACION_DATASETS[nombre_dataset]
    df = pd.read_csv(cfg["ruta"], sep=cfg["separador"], encoding="utf-8", low_memory=False)
    return df