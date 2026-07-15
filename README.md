# CCV Grupo — Venezuela (ccv.com.ve rebuild)

Sitio web de **CCV Grupo · Venezuela** (Corporación Científica Venezolana, C.A.) —
equipos, servicios y proyectos para laboratorio e industria. Sitio estático
generado a partir de datos (contenido en JSON → plantillas Jinja2 → HTML), en
español, con diseño premium de marca teal y animaciones activadas por scroll.

Es la reconstrucción, en un sistema de diseño propio, del sitio Wix
`www.ccv.com.ve`. Ver [REVIEW-PLAN.md](REVIEW-PLAN.md) (plan por fases) y
[SITE-MAP.md](SITE-MAP.md) (arquitectura de información visual).

## Arquitectura

```
ccv-website/
├── build.py                 # Generador (Jinja2): content/ + templates/ -> HTML
├── content/
│   ├── site.json            # Global: marca, regiones (VE/CO/PE), contacto
│   └── divisions/*.json     # Una división por archivo (contenido de página)
├── templates/
│   ├── base.html            # Esqueleto: <head>, header, footer, scripts
│   ├── home.html            # Cuerpo de la portada
│   ├── division.html        # Plantilla de página de división
│   └── partials/            # header · footer · regiones (Presencia regional)
├── assets/
│   ├── css/styles.css       # Estilos y tokens de diseño (:root)
│   ├── js/script.js         # Nav móvil, reveals, count-up, tilt/parallax
│   └── images/              # logo, cards/ (banners @1x + @2x), clients/
├── index.html               # GENERADO (portada)
├── <slug>.html              # GENERADO (una por división)
└── preview.html             # GENERADO — portada autocontenida (CSS/JS/imágenes en línea)
```

> Los archivos `*.html` de la raíz y `preview.html` son **generados**. No los
> edites a mano: modifica `content/` o `templates/` y ejecuta el build.

## Build

Requiere Python 3 con Jinja2 (`pip install jinja2`).

```bash
python3 build.py     # regenera portada + 7 divisiones + preview.html
```

## Ejecutar en local

```bash
python3 -m http.server 8031     # abrir http://localhost:8031
```

O con la extensión **Live Server** de VS Code sobre `index.html`.

## Añadir una división

1. Crea `content/divisions/N-slug.json` (usa uno existente como plantilla:
   `order`, `slug`, `name`, `card_image`, `tagline`, `hero`, `intro`,
   `children[]`, `meta`).
2. Añade su imagen de tarjeta en `assets/images/cards/<card_image>.png` (+ `@2x`).
3. `python3 build.py`. La división aparece automáticamente en el menú
   *Divisiones*, en las tarjetas de la portada, en el pie y en "otras divisiones".

## Marca — CCV Grupo

- Cabecera con lockup **CCV Grupo · Venezuela** y selector de región
  (Venezuela / Colombia / Perú) que enlaza a los sitios hermanos
  (`ccvgrupo.com`, `ccvgrupo.com.co`). Configurable en `content/site.json`.
- Sección **Presencia regional** (países atendidos) en la portada y en el pie.

## Diseño

- **Tipografía:** Sora (títulos) + Plus Jakarta Sans (texto), vía Google Fonts.
- **Paleta teal:** variables CSS en `:root` (`--brand`, `--brand-d`, `--brand-deep`, `--hero`, `--line`).
- **Animaciones:** reveals con `IntersectionObserver`, contadores, timeline, tilt 3D y parallax. Respeta `prefers-reduced-motion`.
- **Robustez sin JS:** el contenido es visible aunque no se ejecute JavaScript
  (las animaciones de reveal están condicionadas a la clase `.js`), para que
  `preview.html` se vea bien en previsualizaciones (p. ej. iOS Quick Look).
- **Responsive:** breakpoints en 900px y 640px; menú móvil hamburguesa.

## Notas

- Los logos de clientes y marcas de terceros son propiedad de sus titulares y se muestran a título de referencia comercial.
- El formulario de contacto solo confirma en el cliente; falta conectarlo a un backend/servicio de envío (decisión pendiente, Fase 5).
- Contenido de las divisiones redactado para el rebuild; debe validarse contra el sitio vigente durante la migración.
