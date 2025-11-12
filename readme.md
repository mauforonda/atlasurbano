## Datos del Censo 2024 en Bolivia a nivel de manzano

El [geoportal oficial](https://geoportal.ine.gob.bo/) de resultados censales permite consultar datos para cada manzano. En este repositorio descargo estos datos y construyo un mapa para observar patrones espaciales desde ellos.

Podemos consultar el número de personas y viviendas para cada manzano, pero el INE sólo nos permite descargar más información en casos donde hayan suficientes personas, por razones de privacidad. Existen 247,346 manzanos a nivel nacional. De éstos, podemos descargar fichas completas para 131,788 (53.28%), donde viven 7,901,688 personas (89.5% de la población nacional) y donde se encuentran 2,920,339 viviendas(87.16% de la viviendas a nivel nacional).

## Datos

Ofrezco 3 conjuntos de datos:

[manzanos.parquet](datos/manzanos.parquet): un geoparquet con los polígonos para todos los manzanos, que tiene esta forma:

| departamento | municipio    | nombre  | codigo        | geometry                                    |
| :----------- | :----------- | :------ | :------------ | :------------------------------------------ |
| Cochabamba   | Villa Rivero | ARAMASI | 05096108787-A | MULTIPOLYGON (((-65.87576 -17.60269, ...))) |

[poblacion.parquet](datos/poblacion.parquet): un parquet con el número de personas y viviendas reportadas en cada manzano y un indicador si existe una ficha disponible (`validado`), con esta forma:

| codigo        | validado | personas | viviendas |
| :------------ | :------- | -------: | --------: |
| 00599713523-A | False    |       14 |        10 |

[fichas.parquet](datos/fichas.parquet): un parquet con la ficha completa para manzanos donde es posible descargarla, con los siguientes campos:

| campo                                 | ejemplo         |
| :------------------------------------ | :------------ |
| codigo                                | 00417298575-A |
| edad_0a19_hombre                      | 13.0          |
| edad_20a39_hombre                     | 31.0          |
| edad_40a59_hombre                     | 15.0          |
| edad_60omas_hombre                    | 7.0           |
| edad_0a19_mujer                       | 14.0          |
| edad_20a39_mujer                      | 28.0          |
| edad_40a59_mujer                      | 12.0          |
| edad_60omas_mujer                     | 13.0          |
| educacion_ninguno_hombre              | 1.0           |
| educacion_primaria_hombre             | 2.0           |
| educacion_secundaria_hombre           | 7.0           |
| educacion_superior_hombre             | 42.0          |
| educacion_sinespecificar_hombre       | 0.0           |
| educacion_ninguno_mujer               | 3.0           |
| educacion_primaria_mujer              | 3.0           |
| educacion_secundaria_mujer            | 4.0           |
| educacion_superior_mujer              | 43.0          |
| educacion_sinespecificar_mujer        | 0.0           |
| salud_centropublico_hombre            | 46.0          |
| salud_cajadesalud_hombre              | 19.0          |
| salud_centroprivado_hombre            | 37.0          |
| salud_atenciondomicilio_hombre        | 12.0          |
| salud_medicinatradicional_hombre      | 20.0          |
| salud_farmaciasinreceta_hombre        | 42.0          |
| salud_remedioscaseros_hombre          | 47.0          |
| salud_centropublico_mujer             | 37.0          |
| salud_cajadesalud_mujer               | 26.0          |
| salud_centroprivado_mujer             | 36.0          |
| salud_atenciondomicilio_mujer         | 4.0           |
| salud_medicinatradicional_mujer       | 17.0          |
| salud_farmaciasinreceta_mujer         | 44.0          |
| salud_remedioscaseros_mujer           | 56.0          |
| saludafiliacion_sus_hombre            | 29.0          |
| saludafiliacion_cajadesalud_hombre    | 21.0          |
| saludafiliacion_seguroprivado_hombre  | 1.0           |
| saludafiliacion_ninguno_hombre        | 13.0          |
| saludafiliacion_sinespecificar_hombre | 0.0           |
| saludafiliacion_sus_mujer             | 28.0          |
| saludafiliacion_cajadesalud_mujer     | 26.0          |
| saludafiliacion_seguroprivado_mujer   | 1.0           |
| saludafiliacion_ninguno_mujer         | 12.0          |
| saludafiliacion_sinespecificar_mujer  | 0.0           |
| nacimiento_aqui_hombre                | 40.0          |
| nacimiento_otromunicipio_hombre       | 23.0          |
| nacimiento_otropais_hombre            | 1.0           |
| nacimiento_sinespecificar_hombre      | 2.0           |
| nacimiento_aqui_mujer                 | 38.0          |
| nacimiento_otromunicipio_mujer        | 28.0          |
| nacimiento_otropais_mujer             | 1.0           |
| nacimiento_sinespecificar_mujer       | 0.0           |
| residencia_aqui_hombre                | 62.0          |
| residencia_otromunicipio_hombre       | 2.0           |
| residencia_otropais_hombre            | 1.0           |
| residencia_sinespecificar_hombre      | 1.0           |
| residencia_aqui_mujer                 | 65.0          |
| residencia_otromunicipio_mujer        | 2.0           |
| residencia_otropais_mujer             | 0.0           |
| residencia_sinespecificar_mujer       | 0.0           |
| ocupacion_empleado_hombre             | 21.0          |
| ocupacion_cuentapropia_hombre         | 12.0          |
| ocupacion_otros_hombre                | 3.0           |
| ocupacion_sinespecificar_hombre       | 3.0           |
| ocupacion_empleado_mujer              | 13.0          |
| ocupacion_cuentapropia_mujer          | 14.0          |
| ocupacion_otros_mujer                 | 4.0           |
| ocupacion_sinespecificar_mujer        | 2.0           |
| actividad_agricultura_hombre          | 0.0           |
| actividad_comercio_hombre             | 4.0           |
| actividad_manufactura_hombre          | 4.0           |
| actividad_construccion_hombre         | 4.0           |
| actividad_transporte_hombre           | 1.0           |
| actividad_alojamientoycomida_hombre   | 0.0           |
| actividad_enseñanza_hombre            | 3.0           |
| actividad_saludyasistencia_hombre     | 2.0           |
| actividad_otras_hombre                | 19.0          |
| actividad_sinespecificar_hombre       | 2.0           |
| actividad_agricultura_mujer           | 0.0           |
| actividad_comercio_mujer              | 8.0           |
| actividad_manufactura_mujer           | 2.0           |
| actividad_construccion_mujer          | 1.0           |
| actividad_transporte_mujer            | 0.0           |
| actividad_alojamientoycomida_mujer    | 0.0           |
| actividad_enseñanza_mujer             | 3.0           |
| actividad_saludyasistencia_mujer      | 1.0           |
| actividad_otras_mujer                 | 14.0          |
| actividad_sinespecificar_mujer        | 4.0           |
| viviendatipo_particular               | 51.0          |
| viviendatipo_personaspresentes        | 43.0          |
| viviendatipo_personasausentes         | 7.0           |
| viviendatipo_particulardesocupada     | 1.0           |
| viviendatipo_colectiva                | 0.0           |
| viviendatenencia_propia               | 25.0          |
| viviendatenencia_alquilada            | 9.0           |
| viviendatenencia_anticretico          | 7.0           |
| viviendatenencia_prestada             | 2.0           |
| viviendatenencia_otra                 | 0.0           |
| energiaelectrica_serviciopublico      | 43.0          |
| energiaelectrica_motorpropio          | 0.0           |
| energiaelectrica_panelsolar           | 0.0           |
| energiaelectrica_otra                 | 0.0           |
| energiaelectrica_notiene              | 0.0           |
| agua_cañería                          | 38.0          |
| agua_piletapública                    | 5.0           |
| agua_carrorepartidor                  | 0.0           |
| agua_pozoconbomba                     | 0.0           |
| agua_pozosinbomba                     | 0.0           |
| agua_vertientenoprotegida             | 0.0           |
| agua_vertienteprotegida               | 0.0           |
| agua_cosechadelluvia                  | 0.0           |
| agua_otra                             | 0.0           |
| desague_alcantarillado                | 42.0          |
| desague_camaraséptica                 | 1.0           |
| desague_pozociego                     | 0.0           |
| desague_superficie                    | 0.0           |
| desague_pozodeabsorción               | 0.0           |
| desague_bañoecológico                 | 0.0           |
| desague_notiene                       | 0.0           |
| combustible_gasgarrafa                | 16.0          |
| combustible_gascañería                | 26.0          |
| combustible_leña                      | 0.0           |
| combustible_guano                     | 0.0           |
| combustible_electricidad              | 0.0           |
| combustible_energíasolar              | 0.0           |
| combustible_otro                      | 0.0           |
| combustible_nococina                  | 1.0           |
| basura_basureropúblico                | 36.0          |
| basura_carrobasurero                  | 7.0           |
| basura_calle                          | 0.0           |
| basura_río                            | 0.0           |
| basura_quema                          | 0.0           |
| basura_entierra                       | 0.0           |
| basura_otro                           | 0.0           |
| tics_radio                            | 30.0          |
| tics_televisor                        | 37.0          |
| tics_celular                          | 39.0          |
| tics_internet                         | 39.0          |

Puedes consultar [el pdf de esta ficha](recursos/ficha_ejemplo.pdf) para comprender qué representa cada valor.

## Descarga

Para construir estos datos, escribí 2 cuadernos:

- [Descarga de polígonos](descarga_poligonos.ipynb)
- [Descarga de datos](armando_manzanero.ipynb)

Estos cuadernos dependen de [un listado de municipios](recursos/municipios.csv) y [un diccionario de los campos en cada ficha](recursos/campos.json).

Mientras el geoportal no cambie mucho, debería ser posible volver a correr este código para reproducir los valores en este repositorio (sin embargo, la descarga de datos podría tomar varios días).

## Mapa

Construyo un mapa que muestra indicadores por manzano que me parecieron básicos e interesantes. En [preparar_mapa.py](preparar_mapa.py) describo cómo se construye cada indicador a partir de los datos mencionados. Guardo estos indicadores en un documento `geojson` temporal que, tras aplicar varias tácticas para ahorrar espacio, convierto en un documento `pmtiles`, que es la fuente desde la que se muestra el mapa. El mapa consume segmentos de este `pmtiles` para mostrar la fracción necesaria de polígonos y datos de manzanos, además de un listado de ciudades y un diccionario de campos, ambos también producidos en [preparar_mapa.py](preparar_mapa.py). Para ésto, utiliza `maplibre-gl` sobre `observable-framework` (ver [index.md](vista/src/index.md)).

Para agregar o cambiar indicadores bastaría con:

Editar [preparar_mapa.py](preparar_mapa.py) para procesar los datos y crear el `geojson`.

Convertir ese `geojson` en un `pmtiles` con `tippecanoe`.

```sh
tippecanoe -Z8 -z14 \
  --no-line-simplification \
  --no-simplification-of-shared-nodes \
  --no-tiny-polygon-reduction \
  --detect-shared-borders \
  --maximum-tile-bytes=1500000 \
  -f -o tiles/atlas.pmtiles \
  temporal/manzanos.geojson
```

Editar [capas.js](vista/src/components/capas.js) para definir cómo debería mostrarse.

🌱
