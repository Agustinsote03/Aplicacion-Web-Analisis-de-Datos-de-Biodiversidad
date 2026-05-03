from datetime import datetime
from pathlib import Path

# Importación de las funciones a utilizar
from insercion_registros import insertar_registro, insertar_multiples_registros
from actualizacion_registros import actualizar_un_campo_validando, actualizar_multiples_campos_validando
from eliminacion_registros import eliminar_por_id, eliminar_por_lista, eliminar_por_condicion, sanitizar_dataset_evolucionada

#Ruta del nuevo archivo log
ruta_log = Path(__file__).resolve().parent.parent / "logs" / "operations.log"

def obtener_fecha_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

