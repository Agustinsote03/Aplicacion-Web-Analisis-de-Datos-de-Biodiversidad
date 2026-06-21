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
├── LICENSE                     # Licencia del código
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
├── LICENSE                     # Licencia del código
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
## Documentación adicional

# Columnas mostradas en resultados de búsqueda (Ejercicio 2.C)

Se decidió mostrar las siguientes columnas en los resultados de búsqueda:

- **occurrenceID**: identificador único del registro, necesario para localizarlo.
- **scientificName**: nombre científico de la especie observada, dato central del registro.
- **recordedBy**: observador que reportó el avistamiento.
- **country / stateProvince**: ubicación geográfica del registro.
- **locality**: descripción textual del lugar.
- **eventDate**: fecha de la observación.
- **decimalLatitude / decimalLongitude**: coordenadas para ubicación en mapa.

Se excluyeron columnas con muy alto porcentaje de valores nulos (identificadas en el 
Ejercicio 2.F de la Etapa 1) o que no aportan información relevante para el análisis 
de biodiversidad, como metadatos técnicos del dataset (ej: `institutionID`, `datasetID`).

## Dependencias principales

Las dependencias se encuentran en `requirements.txt`. Las principales son:

- `streamlit` — interfaz gráfica
- `jupyter` — ejecución de notebooks
- `pandas` — manipulación de datasets
- `streamlit folium` — visualización de mapas
- `matplotlib` — gráficos


## Dependencias principales

Las dependencias se encuentran en `requirements.txt`. Las principales son:

- `streamlit` — interfaz gráfica
- `jupyter` — ejecución de notebooks
- `pandas` — manipulación de datasets
- `streamlit folium` — visualización de mapas
- `matplotlib` — gráficos