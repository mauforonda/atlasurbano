#!/usr/bin/env python3

import geopandas as gpd
import pandas as pd
from pyproj import Geod
import re
from shapely.geometry import mapping
import json
import numpy as np
from pathlib import Path

gdf = gpd.read_parquet("datos/manzanos.parquet")
p = pd.read_parquet("datos/poblacion.parquet")
f = pd.read_parquet("datos/fichas.parquet")

OUTPUT = Path("vista/src/")


def filterSum(df, regex):
    return df[[c for c in df.columns if re.search(regex, c)]].sum(axis=1)


def defineCities(manzanos, poblacion, output_path, min_poblacion=5000):
    index_cols = ["departamento", "municipio", "nombre"]
    gdf = manzanos.merge(poblacion, how="left", on="codigo")
    gdf.crs = 4326
    gdf["geometry"] = gdf.geometry.buffer(0)
    geoms = gpd.GeoDataFrame(
        gdf.groupby(index_cols, as_index=False).agg(
            geometry=("geometry", lambda s: s.union_all())
        ),
        geometry="geometry",
        crs=gdf.crs,
    )
    geoms["center"] = geoms.geometry.to_crs("EPSG:32720").centroid.to_crs("EPSG:4326")
    pops = gdf.groupby(index_cols, as_index=False).personas.sum().copy()
    gdf = geoms.merge(pops, on=index_cols, how="left")
    gdf["x"] = gdf.center.x
    gdf["y"] = gdf.center.y
    gdf.nombre = gdf.nombre.str.title()
    with open(OUTPUT / output_path, "w") as f:
        json.dump(
            gdf[gdf.personas >= min_poblacion][
                ["departamento", "municipio", "nombre", "personas", "x", "y"]
            ]
            .sort_values("personas", ascending=False)
            .to_dict(orient="records"),
            f,
        )


def save_geojson(gdf, out_path, indice_path, as_int):
    g = gdf.drop(columns=["codigo"]).copy()
    g = g.replace([np.inf, -np.inf], np.nan)
    geom_col = g.geometry.name
    columnas = [c for c in g.columns if c != geom_col]
    abreviaciones = [f"{chr(97 + i % 26)}{i // 26 + 1}" for i in range(len(columnas))]
    indice_columnas = {col: i for i, col in zip(abreviaciones, columnas)}
    como_enteros = [indice_columnas[i] for i in as_int]
    g = g.rename(columns=indice_columnas)

    features = []
    for row in g.itertuples(index=False):
        rowd = row._asdict()
        geom = rowd.pop(geom_col)
        props = {}
        for c in abreviaciones:
            v = rowd[c]
            if v == v:
                props[c] = round(float(v), 0 if c in como_enteros else 2)
        features.append(
            {"type": "Feature", "geometry": mapping(geom), "properties": props}
        )
    fc = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False, separators=(",", ":"))
    with open(OUTPUT / indice_path, "w") as f:
        json.dump(indice_columnas, f)


# Densidad poblacional
# Número de habitantes por hectárea

geod = Geod(ellps="WGS84")
gdf["area_ha"] = gdf.geometry.apply(
    lambda g: abs(geod.geometry_area_perimeter(g)[0]) / 1e4
)
p["personas_por_hectarea"] = p.personas / p.codigo.map(gdf.set_index("codigo").area_ha)

# Dependencia económica
# Número de personas inactivas entre la población ocupada, entre residentes dentro del país.

f["poblacion_ocupada"] = filterSum(f, "^ocupacion_.*")
f["poblacion_residente_pais"] = f[
    [c for c in f.columns if "residencia_" in c and "residencia_otropais" not in c]
].sum(axis=1)
f["dependencia_economica"] = (
    (f.poblacion_residente_pais - f.poblacion_ocupada) / f.poblacion_ocupada
) * 100

# Población en rangos de edad

f["poblacion_total"] = filterSum(f, "^edad")
f["porcentaje_menor20"] = filterSum(f, "^edad_0a19.*") / f.poblacion_total
f["porcentaje_60omas"] = filterSum(f, "^edad_60omas.*") / f.poblacion_total

# Masculinidad
# Número de hombres por mujer

f["hombres"] = filterSum(f, "^edad_.*_hombre$")
f["mujeres"] = filterSum(f, "^edad_.*_mujer$")
f["masculinidad"] = (f.hombres / f.mujeres) * 100

# Educación
# Porcentaje de residentes en el país mayores a 19 años que culminaron la educación superior

f["poblacion_residente_mayor"] = filterSum(f, "^educacion_.*")
f["educacion_superior"] = (
    filterSum(f, "^educacion_superior_.*") / f.poblacion_residente_mayor
)

# Brecha de género en educación superior
# Diferencia entre el porcentaje de residentes mayores a 19 años que culminaron la educación secundaria entre mujeres y hombres.

f["brecha_genero_educacion"] = (
    filterSum(f, "educacion_(secundaria|superior)_mujer")
    / filterSum(f, "^educacion_.*_mujer$")
) - (
    filterSum(f, "educacion_(secundaria|superior)_hombre")
    / filterSum(f, "^educacion_.*_hombre$")
)


# Brecha de género en acceso a seguro de salud
# Diferencia entre el porcentaje de personas afiliadas a algún seguro entre mujeres y hombres.

f["brecha_genero_seguro"] = (
    filterSum(f, "^saludafiliacion_((?!ninguno).)*_mujer$")
    / filterSum(f, "^saludafiliacion_.*_mujer$")
) - (
    filterSum(f, "^saludafiliacion_((?!ninguno).)*_hombre$")
    / filterSum(f, "^saludafiliacion_.*_hombre$")
)

# Inmigrantes
# Porcentaje de personas que nacieron en otro municipio o país

f["poblacion_migrante"] = filterSum(f, "^nacimiento_otro.*") / f.poblacion_total

# Ocupación
# Porcentaje de la población que es empleada u obrera, y trabajadora por cuenta propia

f["ocupados_empleados"] = filterSum(f, "^ocupacion_empleado.*") / f.poblacion_ocupada
f["ocupados_cuentapropistas"] = (
    filterSum(f, "^ocupacion_cuentapropia.*") / f.poblacion_ocupada
)

# Seguro privado
# Porcentaje de residentes con seguro privado

f["seguro_privado"] = (
    filterSum(f, "^saludafiliacion_seguroprivado.*") / f.poblacion_residente_pais
)

# Actividades económicas
# Porcentaje de personas dedicadas a cada actividad económica entre el total de personas ocupadas


for actividad in [
    "agricultura",
    "comercio",
    "manufactura",
    "construccion",
    "transporte",
    "alojamientoycomida",
    "enseñanza",
    "saludyasistencia",
]:
    f[f"poblacion_{actividad}"] = (
        filterSum(f, f"^actividad_{actividad}_.*") / f.poblacion_ocupada
    )

# Viviendas desocupadas
# Porcentaje de viviendas particulares con personas temporalmente ausentes o desocupadas

f["viviendas_desocupadas"] = (
    filterSum(f, "^viviendatipo_.*desocupada$") / f.viviendatipo_particular
)

# Viviendas alquiladas o en anticrético
# Porcentaje de viviendas particulares ocupadas que están en alquiler o anticrético

f["viviendas_alquiladas_anticretico"] = (
    filterSum(f, "^viviendatenencia_alquilada$|^viviendatenencia_anticretico$")
    / f.viviendatipo_personaspresentes
)

# Acceso a servicios básicos
# Porcentaje de viviendas particulares ocupadas que cuentan con servicio público de energía eléctrica

for servicio in [
    "energiaelectrica_serviciopublico",
    "agua_cañería",
    "desague_alcantarillado",
    "combustible_gascañería",
    "tics_internet",
]:
    f[f"viviendas_{servicio}"] = (
        filterSum(f, f"^{servicio}$") / f.viviendatipo_personaspresentes
    )

# Consolidar

consolidado = (
    gdf[["codigo", "geometry"]]
    .merge(p[["codigo", "personas", "personas_por_hectarea"]], how="left", on="codigo")
    .merge(
        f[
            [
                "codigo",
                "dependencia_economica",
                "porcentaje_menor20",
                "porcentaje_60omas",
                "masculinidad",
                "educacion_superior",
                "poblacion_migrante",
                "seguro_privado",
                "ocupados_empleados",
                "ocupados_cuentapropistas",
                "poblacion_agricultura",
                "poblacion_comercio",
                "poblacion_manufactura",
                "poblacion_construccion",
                "poblacion_transporte",
                "poblacion_alojamientoycomida",
                "poblacion_enseñanza",
                "poblacion_saludyasistencia",
                "brecha_genero_educacion",
                "brecha_genero_seguro",
                "viviendas_desocupadas",
                "viviendas_alquiladas_anticretico",
                "viviendas_energiaelectrica_serviciopublico",
                "viviendas_agua_cañería",
                "viviendas_desague_alcantarillado",
                "viviendas_combustible_gascañería",
                "viviendas_tics_internet",
            ]
        ],
        how="left",
        on="codigo",
    )
    .copy()
)

save_geojson(
    consolidado,
    "temporal/manzanos.geojson",
    "campos.json",
    ["personas", "personas_por_hectarea", "masculinidad", "dependencia_economica"],
)
defineCities(gdf, p, "ciudades.json", 5000)
