# Dataset: IADIZA

## Información general
- Nombre del dataset: Colección Ornitológica del IADIZA-CCT CONICET Mendoza: IADIZA-COI 
- Institucion proveedora: IADIZA — Instituto Argentino de Investigaciones de las Zonas Áridas (CCT CONICET Mendoza) 
- Cantidad de registros: 2.370
- Tipo de datos: biodiversidad (avistamientos de especies)
- Cobertura geográfica: Argentina (principalmente provincias de Río Negro, Neuquén y Mendoza). Continente: América del Sur
- Cobertura temporal: Registros históricos de colección; fechas de modificación desde 2015. Última interpretación por GBIF: noviembre 2025. Descarga generada: 17 de febrero de 2026.
- Separador de campos: Tabulación (`\t`)
- Codificación de caracteres: UTF-8 
- Tipo de licencia: CC VY-NC 4.0 (Creative Commons Atribución-NoComercial 4.0 Internacional) 
- Frecuencia temporal: No especificada. Última actualización registrada: noviembre 2025. 

---------

## Archivos del dataset

### `occurrence.txt`
Archivo principal del dataset. Contiene los registros de ocurrencia de especies bajo el estándar Darwin Core. Cada fila representa un espécimen preservado de la colección ornitológica, con información taxonómica, geográfica, temporal e institucional. Separador: tabulación. Encoding: UTF-8.

### `meta.xml`
Archivo de metadatos estructurales del Darwin Core Archive. Describe cómo interpretar los archivos del dataset: indica el separador de campos (`\t`), la codificación (UTF-8), el archivo principal (`occurrence.txt`) y las extensiones disponibles (`verbatim.txt`, `multimedia.txt`), junto con el término DwC correspondiente a cada columna y su índice.

### `metadata.xml`
Archivo EML (Ecological Metadata Language) generado por GBIF al momento de la descarga. Contiene información general del paquete: nombre del dataset, fecha de publicación (2026-02-17), identificador único de la descarga (`0025550-260208012135463`), codificación y formato (Darwin Core Archive).

### `multimedia.txt` *(extensión)*
Archivo de extensión multimedia. Contiene referencias a imágenes u otros archivos multimedia asociados a los registros de ocurrencia. Se vincula con `occurrence.txt` a través del `gbifID`.

### `verbatim.txt` *(extensión)*
Archivo de extensión que contiene los valores originales tal como fueron provistos por la institución, antes de ser interpretados y normalizados por GBIF.

--------

## Atributos del dataset

| Atributo | Descripción | Ejemplo de valor |
|----------|-------------|------------------|
| `gbifID` | Identificador único asignado por GBIF al registro | `1660908055` |
| `license` | Licencia de uso del dato | `CC_BY_NC_4_0` |
| `modified` | Fecha de última modificación del registro original | `2015-05-19T00:00:00Z` |
| `institutionCode` | Código de la institución proveedora | `IADIZA` |
| `collectionCode` | Código de la colección dentro de la institución | `COI` |
| `basisOfRecord` | Base del registro (cómo fue obtenido) | `PRESERVED_SPECIMEN` |
| `occurrenceID` | Identificador único de la ocurrencia dentro del dataset | `IADIZA:COI:006861` |
| `catalogNumber` | Número de catálogo de la colección | `006861` |
| `recordedBy` | Persona que realizó el registro/colecta | `R.G. Spurr` |
| `occurrenceStatus` | Estado de la ocurrencia | `PRESENT` |
| `eventDate` | Fecha del evento de colecta | (vacío en muchos registros) |
| `year` / `month` / `day` | Año, mes y día del evento desagregados | (vacío en muchos registros) |
| `countryCode` | Código de país ISO 3166-1 alpha-2 | `AR` |
| `stateProvince` | Provincia o estado | `Río Negro` |
| `county` | Departamento o partido | `Pilcaniyeu` |
| `locality` | Descripción textual de la localidad | `Lago Los Juncos, Est. Perito Moreno 900m` |
| `decimalLatitude` | Latitud en grados decimales | (vacío en la mayoría de los registros) |
| `decimalLongitude` | Longitud en grados decimales | (vacío en la mayoría de los registros) |
| `coordinateUncertaintyInMeters` | Incertidumbre de la coordenada en metros | (vacío) |
| `scientificName` | Nombre científico completo de la especie (con autor) | `Chloephaga picta (J.F.Gmelin, 1789)` |
| `kingdom` | Reino | `Animalia` |
| `family` | Familia | `Anatidae` |
| `genus` | Género | `Chloephaga` |
| `specificEpithet` | Epíteto específico | `picta` |
| `taxonRank` | Rango taxonómico del registro | `SPECIES` |
| `species` | Nombre de la especie sin autor | `Chloephaga picta` |
--------

## Descripción
El dataset contiene registros de observaciones de especies, incluyendo información sobre ubicación, fecha, clasificación taxonómica y otros datos asociados al evento de observacion. Estos datos permiten analizar la distribucion de especies y su presencia en distintas regiones.

