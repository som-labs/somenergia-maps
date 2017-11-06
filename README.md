# Mapa de contratos de Som Energia por municipio

**Demo: https://som-labs.github.io/somenergia-maps/**

> Nota: **Los datos son estáticos, a 1 de Octubre de 2017.**


## Cómo se generaron los datos para el mapa

### Paso 1. Preparación de la base municipal

La base municipal pertenece al Atlas Nacional de España (Base cartográfica SIANE), obtenida del [Centro de Descargas del CNIG](http://centrodedescargas.cnig.es/CentroDescargas/index.jsp).
A partir de dos ficheros shapefile (uno para Península y Balerares, otro para las Islas Canarias), se descartaron todos
los atributos excepto el código INE y el nombre de municipio, y se convirtió el resultado a formato [GeoJSON](https://tools.ietf.org/html/rfc7946).
Esto se hizo mediante la aplicación de software libre [QGIS](http://www.qgis.org).

Se parte pues del fichero `data/municipios.geojson` con la geometría para cada municipio y sus atributos:
   * **id_ine**: String de 5 caracteres numéricos (para consevar los 0 a la izquierda),
   * **rotulo**: String con el nombre del municipio.


### Paso 2. Generación de series temporales a partir de hojas de cálculo

Se dispone de una serie de hojas de cálculo proporcionadas por [David García Garzón](https://github.com/vokimon) de Som Energia en formato CSV, cuyos nombres de fichero son
`data/distribution-summaries/distribucion-contratos-YYYY-MM-DD-detalle.tsv`, y que contiene las siguientes columnas:
   * **codi_pais** y **pais**: De momento, el mismo para todos los registros.
   * **codi_ccaa** y **comunitat_autonoma**: Identificador y nombre de la comunidad autónoma a la que pertenece el municipio.
   * **codi_provincia** y **provincia**: Identificador y nombre de la provincia a la que pertenece el municipio.
   * **codi_ine** y **municipi**: Identificador y nombre del municipio.
   * **quants**: Número de contratos en el municipio a la fecha indicada en el nombre del fichero (formato YYYY-MM-DD).

Existe un fichero para cada mes, desde el día 1 de Enero de 2015 hasta el día 1 de Octubre de 2017.
Los ficheros a partir de Octubre de 2017 hasta Diciembre de 2018 pueden ser ignorados (son fechas futuras al día de la generación
de los datos, y contienen la misma información que la de Octubre de 2017).  

> Nota: También se dispone de otra serie igual para número de socias, pero se han detectado errores en los datos que la hacen inusable,
> al menos en los datos de ejemplo proporcionados. 

Mediante el script en python `scripts/prepare_data.py`, es posible leer las hojas de cálculo y generar
un fichero JSON el número de contratos para cada municipio a lo largo del tiempo. El formato de salida
sería un diccionario cuya clave es el código INE del municipio, y el valor es un nuevo objeto con las
fechas y el número de contratos por cada fecha, así:

```json
{
  "08019": {
    "2015-01-01": 3295,
    "2015-02-01": 5555
  },
  "08015": {
    "2015-01-01": 164,
    "2015-02-01": 222
  }
}
```

Mediante este script se ha generado el fichero `data/contratos.json`, pero sólo para la fecha "2017-10-01".


### Paso 3. Mezcla de base municipal y series temporales de datos

Mediante el script en ES6 para node `scripts/merge_data_into_map.js`, se genera un nuevo mapa municipal
en formato GeoJSON que contiene las geometrías de los municipios, y las series temporales de contratos
por fecha.


### Paso 4. Generación de teselas vectoriales

Finalmente, el mapa en GeoJSON tiene que convertirse a [*vector tiles*](https://www.mapbox.com/vector-tiles/), un
formato que permite visualizar mapas complejos en un navegador de forma eficiente.

Para ello se usa el script bash `scripts/geojson2tiles.sh`, que a su vez requiere tener instalado
[mapbox/tippecanoe](https://github.com/mapbox/tippecanoe).

El resultado final se encuentra en los ficheros `data/tiles/{z}/{x}/{y}.pbf`, que son los que finalmente
se sirven a través de la red para componer el mapa.
