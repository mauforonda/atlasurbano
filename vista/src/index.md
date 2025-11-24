---
theme: dashboard
title: Atlas urbano
toc: false
sidebar: false
---

<link 
  rel="stylesheet" 
  type="text/css" 
  href="https://unpkg.com/maplibre-gl@4.0.2/dist/maplibre-gl.css"
>

<link 
  rel="stylesheet" 
  type="text/css" 
  href="index.css"
>

<header>
  <header_titulo>
    <titulo>Atlas urbano</titulo>
    <subtitulo>con datos del Censo 2024</subtitulo>
  </header_titulo>
  <menu>
    ${ciudadInput}
    ${seleccionInput}
  </menu>
  <leyenda>
    ${leyendaLineal(
      indice[seleccion].colormap, 
      indice[seleccion].ayuda,
      indice[seleccion].format
    )}
    ${leyendaCategorias([["sin datos", invalido]])}
  </leyenda>
</header>

<div id="mapa"></div>

```js
// Dependencias para el mapa
import maplibregl from "npm:maplibre-gl";
import { PMTiles, Protocol } from "npm:pmtiles";
const protocol = new Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);
```

```js
// Cargar el pmtiles
import { PMTILES_URL } from "./components/pmtiles-url.js";
const pm = new PMTiles(PMTILES_URL);
protocol.add(pm);
```

```js
// Definiciones de campos y ciudades
const campos = await FileAttachment("./campos.json").json();
const ciudades = await FileAttachment("./ciudades.json").json();
```

```js
// Cargar componentes en otros js y definir constantes
const invalido = "rgba(180, 180, 199, 0.36)";
import { indice } from "./components/capas.js";
import { autoSelect } from "./components/inputs.js";
```

```js
// Qué ciudad mostrar al cargar el mapa
const idCiudad = (d) => `${d.departamento}|${d.municipio}|${d.nombre}`;
const ciudad_key = "atlasurbano_ciudad";
const ciudad_default = ciudades[0];
const storedId = localStorage.getItem(ciudad_key);
const ciudad_inicial =
  ciudades.find((d) => idCiudad(d) === storedId) ?? ciudad_default;
```

```js
// Menú de ciudades
const ciudadInput = autoSelect(ciudades, (d) => d.nombre, ciudad_inicial);
const ciudad = Generators.input(ciudadInput);
```

```js
// Desde qué coordenadas cargar el mapa
const posicion_key = "atlasurbano_posicion";
const posicion_stored = localStorage.getItem(posicion_key);
const posicion_inicial = posicion_stored
  ? (() => {
      const p = JSON.parse(posicion_stored);
      return [p.x, p.y];
    })()
  : [ciudad_inicial.x, ciudad_inicial.y];
const tiene_posicion_stored = !!posicion_stored;
```

```js
// Luego cada movimiento, guardar las coordenadas localmente para futuras sesiones
map.on("moveend", () => {
  const centro = map.getCenter();
  localStorage.setItem(
    posicion_key,
    JSON.stringify({ x: centro.lng, y: centro.lat })
  );
});
```

```js
map.__skipInitialFly = tiene_posicion_stored;
```

```js
// Volar a la ciudad seleccionada y guardarla localmente
{
  await ciudad;
  if (map.__skipInitialFly) {
    map.__skipInitialFly = false;
  } else {
    map.flyTo({ center: [ciudad.x, ciudad.y], minZoom: 10, zoom: 11 });
    localStorage.setItem(ciudad_key, idCiudad(ciudad));
  }
}
```

```js
// Leyendas

function leyendaLineal(colormap, ayuda, format) {
  const valores = colormap.map((c) => c[0]);
  const domain = [Math.min(...valores), Math.max(...valores)];
  return Plot.legend({
    margin: 0,
    height: 50,
    label: ayuda,
    className: "leyenda",
    color: {
      type: "linear",
      domain: domain,
      range: colormap.map((c) => c[1]),
      tickFormat: d3.format(format),
    },
  });
}

function leyendaCategorias(colormap) {
  const valores = colormap.map((c) => c[0]);
  return Plot.legend({
    margin: 0,
    className: "leyenda",
    swatchHeight: 10,
    color: {
      domain: valores,
      range: colormap.map((c) => c[1]),
    },
  });
}
```

```js
// Qué variable cargar al inicio
const seleccion_key = "atlasurbano_variable";
const seleccion_default = "personas_por_hectarea";
const seleccion_stored = localStorage.getItem(seleccion_key);
const seleccion_inicial = seleccion_stored ?? seleccion_default;
```

```js
// Menú de variables
const seleccionInput = Inputs.select(Object.keys(indice), {
  required: true,
  format: (d) => indice[d].nombre,
  value: seleccion_inicial,
});
const seleccion = Generators.input(seleccionInput);
```

```js
// Tras seleccionar una variable, guardarla localmente para futuras sesiones
localStorage.setItem(seleccion_key, seleccion);
```

```js
// Crear capas para maplibre

function capaLineal(campo, colormap) {
  return {
    id: campo,
    type: "fill",
    source: "atlas",
    "source-layer": "manzanos",
    paint: {
      "fill-color": [
        "let",
        "campo",
        ["to-number", ["get", campos[campo]]],
        [
          "case",
          [
            "any",
            ["!", ["has", campos[campo]]],
            ["!=", ["var", "campo"], ["var", "campo"]],
          ],
          invalido,
          ["interpolate", ["linear"], ["var", "campo"], ...colormap.flat()],
        ],
      ],
      "fill-opacity": ["interpolate", ["linear"], ["zoom"], 6, 0.2, 12, 0.8],
    },
    minzoom: 8,
  };
}
```

```js
// Inicializar el mapa

const container = document.querySelector("#mapa");
const map = new maplibregl.Map({
  container: container,
  center: posicion_inicial,
  zoom: 11,
  minZoom: 10,
  maxZoom: 14,
  scrollZoom: true,
  style:
    "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json",
  attributionControl: {
    compact: true,
    customAttribution:
      "<a href='https://mauforonda.github.io/'>Mauricio Foronda</a>",
  },
});
// Popup
const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false });

// Controles
map.addControl(new maplibregl.NavigationControl(), "bottom-left");
map.addControl(
  new maplibregl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true,
    },
    showAccuracyCircle: false,
    showUserLocation: true,
  }),
  "bottom-left"
);

invalidation.then(() => {
  popup.remove();
  map.remove();
});
```

```js
// Capa de etiquetas

const capaEtiquetas = {
  source: {
    type: "raster",
    tiles: [
      "https://a.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png",
    ],
    tileSize: 256,
  },
  layer: {
    id: "etiquetas",
    type: "raster",
    source: "etiquetas",
    paint: {
      "raster-opacity": 0.8,
    },
  },
};
```

```js
// Tras cargar el mapa, definir las fuentes y capas
const ready = new Promise((resolve) => {
  map.on("load", () => {
    map.addSource("etiquetas", capaEtiquetas.source);
    map.addLayer(capaEtiquetas.layer);
    if (!map.getSource("atlas")) {
      map.addSource("atlas", {
        type: "vector",
        url: `pmtiles://${PMTILES_URL}`,
        minzoom: 8,
        maxzoom: 14,
      });
    }
    resolve();
  });
});
```

```js
// Cómo mostrar el popup
let locked = false;
function bindHoverFor(campo) {
  if (map.__hoverHandlers) {
    const { layer, enter, leave, clickIn, clickAny } = map.__hoverHandlers;
    map.off("mouseenter", layer, enter);
    map.off("mouseleave", layer, leave);
    map.off("click", layer, clickIn);
    map.off("click", clickAny);
  }

  const enter = (e) => {
    map.getCanvas().style.cursor = "pointer";
    const f = e.features && e.features[0];
    if (!f) return;

    const key = campos[campo];
    const raw = f.properties?.[key];

    const n = typeof raw === "number" ? raw : raw == null ? NaN : +raw;
    if (!Number.isFinite(n)) {
      map.getCanvas().style.cursor = "";
      popup.remove();
      return;
    }

    const fmt = d3.format(indice[campo].format);
    popup
      .setHTML(
        `<div class="popup"><div class="descripcion">${
          indice[campo].ayuda
        }</div><div class="valor">${fmt(n)}</div></div>`
      )
      .setLngLat(e.lngLat)
      .addTo(map);
  };

  const leave = () => {
    map.getCanvas().style.cursor = "";
    if (!locked) popup.remove();
  };

  const clickIn = () => {
    locked = true;
  };

  const clickAny = (e) => {
    const hit = map.queryRenderedFeatures(e.point, { layers: [campo] }).length;
    if (!hit) {
      locked = false;
      popup.remove();
    }
  };

  map.on("mouseenter", campo, enter);
  map.on("mouseleave", campo, leave);
  map.on("click", campo, clickIn);
  map.on("click", clickAny);

  map.__hoverHandlers = { layer: campo, enter, leave, clickIn, clickAny };
}
```

```js
// Cambiar la capa
let active = null;
const apply = (campo) => {
  if (active && map.getLayer(active)) map.removeLayer(active);
  map.addLayer(capaLineal(campo, indice[campo].colormap), "etiquetas");
  active = campo;
  map.__activeId = campo;

  bindHoverFor(campo);
};
```

```js
// Cambiar la capa cuando el usuario seleccione una variable
{
  await ready;
  apply(seleccion);
}
```
