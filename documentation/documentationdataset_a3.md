# Dataset: iNaturalist

## Información general
- Nombre del dataset: iNaturalist Research-grade Observations    
- Institución proveedora: iNaturalist (California Academy of Sciences / National Geographic Society). Contacto: help@inaturalist.org
- Cantidad de registros: 1.229.610
- Cobertura geográfica: Global. Bounding box: latitud entre -84.41° y 90°, longitud prácticamente global (0° a ~0°). |
- Cobertura temporal: Desde 1768-09-17 hasta 2026-02-16.                                                        
- Separador de campos: Coma (`,`) 
- Codificación de caracteres: UTF-8 
- Tipo de licencia: CCC BY-NC 4.0 para el archivo en su conjunto. Registros individuales pueden estar bajo CC0 o CC BY 4.0. |
- Frecuencia temporal: Semanal. Las observaciones son dinámicas: las identificaciones y la calidad de los datos pueden cambiar en cualquier momento por curación colaborativa. 

--------

## Archivos del dataset

### `observations.csv`
Archivo principal del dataset. Contiene las observaciones de biodiversidad registradas por la comunidad de iNaturalist que alcanzaron el grado "Research Grade". Cada fila representa una observación individual de un organismo (animal, planta, hongo, etc.) con información sobre quién lo observó, cuándo, dónde y qué especie es. Separador: coma. Campos encerrados entre comillas dobles. Encoding: UTF-8.

### `media.csv` *(extensión Multimedia)*
Archivo de extensión que contiene referencias a archivos multimedia (fotos, sonidos) asociados a cada observación. Se vincula con `observations.csv` a través del campo `id`. Incluye tipo de medio, formato, URL del archivo, fecha de creación, autor, licencia y titular de derechos.

### `dna_derived_data.csv` *(extensión DNADerivedData)*
Archivo de extensión que contiene datos derivados de secuencias de ADN asociados a algunas observaciones. Incluye el identificador, la secuencia de ADN y metadatos asociados. **Nota:** según el EML, estos datos no están sujetos a control de calidad por parte de iNaturalist.

### `meta.xml`
Archivo de metadatos estructurales del Darwin Core Archive. Describe el separador de campos (`,`), la codificación (UTF-8), el archivo principal (`observations.csv`) y las extensiones (`media.csv`, `dna_derived_data.csv`), junto con el término DwC correspondiente a cada columna y su índice.

### `eml.xml`
Archivo EML (Ecological Metadata Language) que describe el dataset en detalle: título, institución proveedora, cobertura geográfica y temporal, licencias, metodología de calidad de datos (Research Grade), frecuencia de actualización y propósito del proyecto.

----------

## Atributos del dataset

| Atributo | Descripción | Ejemplo de valor |

| `id` | Identificador interno del registro (índice 0, usado como clave) | `123456789` |
| `occurrenceID` | Identificador único de la ocurrencia | `https://www.inaturalist.org/observations/123456789` |
| `basisOfRecord` | Base del registro (valor por defecto) | `HumanObservation` |
| `modified` | Fecha de última modificación del registro | `2024-03-15T10:22:00Z` |
| `institutionCode` | Código de la institución (valor por defecto) | `iNaturalist` |
| `recordedBy` | Nombre del usuario que registró la observación | `@nombreusuario` |
| `identifiedBy` | Nombre del usuario que identificó la especie | `@identificador` |
| `eventDate` | Fecha de la observación | `2023-11-05` |
| `eventTime` | Hora de la observación | `14:30:00` |
| `decimalLatitude` | Latitud en grados decimales | `-34.5897` |
| `decimalLongitude` | Longitud en grados decimales | `-58.3974` |
| `coordinateUncertaintyInMeters` | Incertidumbre de la coordenada en metros | `10` |
| `countryCode` | Código de país ISO 3166-1 alpha-2 | `AR` |
| `stateProvince` | Provincia o estado | `Buenos Aires` |

| `identificationRemarks` | Comentarios sobre la identificación taxonómica | *(texto libre)* |
| `taxonID` | Identificador del taxón en iNaturalist | `12704` |
| `scientificName` | Nombre científico de la especie | `Ara chloropterus` |
| `taxonRank` | Rango taxonómico | `species` |
| `kingdom` | Reino | `Animalia` |
| `family` | Familia | `Psittacidae` |
| `genus` | Género | `Ara` |
| `license` | Licencia del registro individual | `CC_BY_NC_4_0` |

-------

## Descripcion
Este dataset contiene registros de ocurrencias de especies del reino animal y vegetal, cada registro representa una observación validada por la comunidad de iNaturalist que alcanzó el grado "Research Grade" e incluye información taxonómica (como reino, clase, orden, familia y género), datos geográficos (país, provincia, coordenadas y localidad descriptiva), y detalles del evento de observación (fecha, hora y observador). Además, incorpora información sobre el estado biológico del organismo (sexo, etapa de vida y condición reproductiva), referencias multimedia asociadas a cada observación y datos sobre la identificación taxonómica (quién identificó la especie y cuándo).

