# BioAR 

Aplicación de análisis y visualización de datos de biodiversidad basada en el estándar Darwin Core, desarrollada como la primera parte del Trabajo Integrador 2026 para la materia "Taller de Lenguajes".

## Grupo 56 - Integrantes

- Martina Buiras
- Catalina Victoria Flores
- Santiago Pastor
- Fabricio Agustín Ghizzo

---

## Estructura del proyecto

```
/
├── src/                        # Código fuente Python
│   ├── config.py               # Configuración de datasets
│   ├── dataset_reader.py       # Funciones de lectura (Ejercicio 2)
│   ├── validador.py            # Funciones de validación (Ejercicio 3)
│   ├── insercion_registros.py  # Funciones de inserción (Ejercicio 4)
│   ├── actualizacion_registros.py  # Funciones de actualización (Ejercicio 5)
│   ├── eliminacion_registros.py    # Funciones de eliminación (Ejercicio 6)
│   ├── logger.py               # Registro de operaciones (Ejercicio 7)
│   └── utils.py                # Funciones utilitarias
├── notebooks/                  # Jupyter Notebooks por ejercicio
│   ├── ejercicio_2.ipynb
│   ├── ejercicio_3.ipynb
│   ├── ejercicio_4.ipynb
│   ├── ejercicio_5.ipynb
│   ├── ejercicio_6.ipynb
│   └── ejercicio_7.ipynb
├── documentation/              # Documentación de los datasets
│   ├── dataset_iadiza.md
│   ├── dataset_xenocanto.md
│   └── dataset_inaturalist.md
├── raw_datasets/               # Datasets originales (no subir al repositorio)
│   ├── Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI/
│   ├── xeno-canto-bird-sounds-filtered/
│   └── inaturalist-filtered/
├── processed_datasets/         # Datasets procesados (no subir al repositorio)
│   ├── IADIZA/
│   ├── xeno_canto/
│   └── inaturalist/
├── logs/                       # Archivo de log de operaciones
│   └── operations.log
├── pages/                      # Páginas de la app Streamlit
├── app.py                      # Archivo principal de Streamlit
├── requirements.txt            # Dependencias del proyecto
└── README.md
```

---

## Requisitos previos

- Python 3.10 o superior
- pip

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <https://gitlab.catedras.linti.unlp.edu.ar/python-2026/proyectos/grupo56/code.git>
cd <nombre-del-repositorio>
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows:
```bash
venv\Scripts\activate
```

En Linux/Mac:
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración de datasets

Los datasets **no se incluyen en el repositorio**. Deben descargarse manualmente y ubicarse en la carpeta `raw_datasets/` con la siguiente estructura:

```
raw_datasets/
├── Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI/
│   ├── occurrence.txt
│   ├── meta.xml
│   └── metadata.xml
├── xeno-canto-bird-sounds-filtered/
│   ├── Occurrence.txt
│   ├── Multimedia.txt
│   ├── meta.xml
│   └── eml.xml
└── inaturalist-filtered/
    ├── observations.csv
    ├── media.csv
    ├── meta.xml
    └── eml.xml
```

También deben crearse manualmente las carpetas de datasets procesados:

```bash
mkdir -p processed_datasets/IADIZA
mkdir -p processed_datasets/Xeno_canto
mkdir -p processed_datasets/iNaturalist
mkdir -p logs
```

---

## Ejecución de los notebooks

Asegurate de tener el entorno virtual activado y Jupyter instalado.

Para abrir Jupyter:

```bash
jupyter notebook
```

Luego abrí el notebook correspondiente al ejercicio desde la interfaz. Por ejemplo, para ejecutar el ejercicio 2:

```
notebooks/ejercicio_2.ipynb
```

> **Importante:** los notebooks deben ejecutarse desde la carpeta `notebooks/` para que las rutas relativas funcionen correctamente.

---

## Ejecución de la aplicación Streamlit

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en el navegador en `http://localhost:8501`.

---

## Dependencias principales

Las dependencias se encuentran en `requirements.txt`. Las principales son:

- `streamlit` — interfaz gráfica
- `jupyter` — ejecución de notebooks

> Este proyecto **no utiliza pandas** ni otras librerías de análisis de datos en los ejercicios 2 a 7, tal como indica la consigna. El procesamiento se realiza con las librerías estándar de Python (`csv`, `pathlib`, `datetime`).

-------

## Notas de implementación

### Ejercicio 3 — Validación

- **Validación de fechas (3.C):** el formato de fecha esperado por la función es `"%d/%m/%y"`. Los tres datasets utilizan formatos distintos (por ejemplo `"2025-05-03"` o `"2018-03-31T08:09:00-03:00"`), por lo que la mayoría de los registros son marcados como inválidos. Esto es un comportamiento esperado dado el formato configurado.

- **Validación de country code (3.F):** Xeno-canto no utiliza el campo `countryCode` sino `country` con el nombre completo del país (por ejemplo `"Argentina"`). Por este motivo todos sus registros son marcados como inválidos en esta validación.

### Ejercicio 4 — Inserción de registros

Las funciones de inserción están implementadas principalmente para el dataset IADIZA, ya que cada dataset tiene una estructura y un formato de IDs distinto:

- **IADIZA:** `catalogNumber` autoincremental con formato `XXXXXX` (6 dígitos) y `occurrenceID` con formato `IADIZA:COI:XXXXXX`.
- **Xeno-canto:** `id` con formato `XXXXXX@XC` y `catalogNumber` con formato `XCXXXXXX`.
- **iNaturalist:** `id` autoincremental numérico y `occurrenceID` como URL (`https://www.inaturalist.org/observations/XXXXXX`).

Para extender la inserción a los otros datasets se deberán implementar funciones específicas para cada uno respetando sus formatos de ID.