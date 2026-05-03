# Dataset: Xeno-canto

## Información general
- Nombre del dataset: Xeno-canto - Bird sounds from around the world   
- Institución proveedora: Xeno-canto Foundation for Nature Sounds (Países Bajos), con soporte de Naturalis Biodiversity Center y NLBIF. Contacto: wp@xeno-canto.org 
- Cantidad de registros: 13.470 (sin contar encabezados)
- Tipo de datos: biodiversidad (avistamientos de especies)
- Cobertura geográfica: Global (bounding box: -180° a 180° longitud, -90° a 90° latitud). El archivo disponible contiene principalmente registros de Argentina. 
- Cobertura temporal: Desde 1900 hasta el presente. Fecha de publicación de esta versión: 2026-02-17.
- Separador de campos: Coma (`,`) 
- Codificación de caracteres: UTF-8 
- Tipo de licencia: CC BY-NC 4.0 (Creative Commons Atribución-NoComercial 4.0 Internacional)
- Frecuencia temporal: Continua. Solo se comparten en GBIF los registros de grabadores que han dado permiso explícito. Las identificaciones cuestionadas no se publican.

--------

## Archivos del dataset

### `Occurrence.txt`
Archivo principal del dataset. Contiene los registros de ocurrencia de aves basados en grabaciones de sonido. Cada fila representa una grabación individual, con información sobre la especie identificada, el lugar y fecha de grabación, el grabador, notas de campo y el comportamiento observado. Separador: coma. Campos encerrados entre comillas dobles. Encoding: UTF-8.

### `Multimedia.txt` *(extensión Multimedia)*
Archivo de extensión que contiene referencias a los archivos de audio (grabaciones) asociados a cada registro. Incluye la URL de acceso al sonido, el formato del archivo, el tipo de medio, el creador, la calificación de la grabación, la técnica de captura, el dispositivo utilizado y la licencia. Se vincula con `Occurrence.txt` a través del campo `id`.

### `meta.xml`
Archivo de metadatos estructurales del Darwin Core Archive. Describe el separador de campos (`,`), la codificación (UTF-8), el archivo principal (`Occurrence.txt`) y la extensión multimedia (`Multimedia.txt`), junto con el término DwC correspondiente a cada columna y su índice.

### `eml.xml`
Archivo EML (Ecological Metadata Language) que describe el dataset en detalle: título, institución proveedora, cobertura geográfica (global) y taxonómica (clase Aves, taxonomía basada en IOC World Bird List), licencia, metodología de control de calidad y referencias bibliográficas.

----------

## Atributos del dataset

### `Occurrence.txt`

| Atributo | Descripción | Ejemplo de valor |

| `id` | Identificador interno del registro (clave) | `999540@XC` |
| `occurrenceID` | URL única de la observación en el sistema | `https://data.biodiversitydata.nl/xeno-canto/observation/XC999540` |
| `catalogNumber` | Número de catálogo de Xeno-canto | `XC999540` |
| `basisOfRecord` | Base del registro | `HumanObservation` |
| `genus` | Género de la especie | `Elaenia` |
| `scientificName` | Nombre científico completo | `Elaenia chilensis` |
| `taxonRank` | Rango taxonómico | `species` |
| `kingdom` | Reino | `Animalia` |
| `family` | Familia | `Tyrannidae` |
| `longitudeDecimal` | Longitud en grados decimales | `-60.6486` |
| `latitudeDecimal` | Latitud en grados decimales | `-32.8606` |
| `country` | País donde se realizó la grabación | `Argentina` |
| `locality` | Descripción textual de la localidad | `Victoria, Entre Ríos` |
| `recordedBy` | Nombre del grabador | `Franco Vushurovich` |
| `eventDate` | Fecha de la grabación | `2025-05-03` |
| `eventTime` | Hora de la grabación | `11:22` |
| `behavior` | Tipo de vocalización o comportamiento registrado | `call` / `alarm call, flight call` |
| `associatedTaxa` | Especies de fondo presentes en la grabación | `has background sounds: Vanellus chilensis\|Phacellodomus ruber` |
| `license` | Licencia del registro individual | `CC BY-NC` |


### `Multimedia.txt` (atributos principales)

| Atributo | Descripción | Ejemplo de valor |

| `coreid` | ID del registro de ocurrencia asociado | `999540@XC` |
| `associatedObservationReference` | URL de la observación asociada | `https://xeno-canto.org/999540` |
| `identifier` | URL directa al archivo de audio | `https://xeno-canto.org/999540/download` |
| `type` | Tipo de medio | `Sound` |
| `Rating` | Calificación de la grabación (escala de Xeno-canto) | `A` / `B` / `C` |
| `creator` | Autor de la grabación | `Franco Vushurovich` |
| `accessURI` | URI de acceso al recurso multimedia | URL al archivo de audio |
| `format` | Formato del archivo de audio | `audio/mpeg` |
| `resourceCreationTechnique` | Técnica de grabación utilizada | *(descripción del equipo/método)* |
| `captureDevice` | Dispositivo de captura | *(nombre del micrófono/grabadora)* |
| `physicalSetting` | Entorno físico de la grabación | `field recording` |
| `rights` | Derechos sobre el archivo multimedia | `CC BY-NC` |

---------

## Descripción
Este dataset contiene registros de aocurrenciass de especies, principalmente aves, cada registro representa una observación individual e incluye información taxonómica (como género, especie y familia), datos geográficos (país, coordenadas y localidad), y detalles del evento de observación (fecha, hora y observador), ademas incorpora información adicional sobre el comportamiento del organismo, su estado biológico (sexo, etapa de vida).

