# CCV — Corporación Científica Venezolana

Sitio web corporativo de Corporación Científica Venezolana, C.A. — equipos, servicios y proyectos para laboratorio e industria en Venezuela. Sitio estático (HTML + CSS + JavaScript), en español, con diseño premium de marca teal y animaciones activadas por scroll.

## Estructura del proyecto

```
ccv-website/
├── index.html          # Página única (hero, divisiones, nosotros, servicio, marcas, clientes, contacto)
├── styles.css          # Estilos y tokens de diseño de marca
├── script.js           # Navegación móvil, reveals, count-up, tilt/parallax
├── logo.png            # Logo CCV (navbar / footer)
├── banner-home.png     # Banner alternativo para el hero (opcional)
├── div-*.png           # Banners de las divisiones
└── clientes/           # Logos de clientes (strip animado)
```

## Ejecutar en local

No requiere build. Cualquier servidor estático sirve el sitio:

```bash
python3 -m http.server 8031
# abrir http://localhost:8031
```

O con la extensión **Live Server** de VS Code: clic derecho en `index.html` → *Open with Live Server*.

## Diseño

- **Tipografía:** Sora (títulos) + Plus Jakarta Sans (texto), vía Google Fonts.
- **Paleta teal:** definida como variables CSS en `:root` (`--brand`, `--brand-d`, `--brand-deep`, `--hero`, `--line`).
- **Animaciones:** reveals con `IntersectionObserver`, contadores animados, timeline del servicio técnico, tilt 3D y parallax en el hero. Todo respeta `prefers-reduced-motion`.
- **Responsive:** breakpoints en 900px y 640px; navegación móvil con menú hamburguesa.

## Secciones

1. **Hero** — propuesta de valor y llamados a la acción.
2. **Divisiones** — 7 banners (Equipos, Farma, LIMS, Proyectos, Life Science, Servicio Técnico, Reactivos).
3. **Nosotros** — trayectoria desde 1982, valores y credenciales.
4. **Servicio Técnico** — timeline de 3 pasos del ciclo de vida.
5. **Marcas** — tecnología de referencia mundial.
6. **Clientes** — strip animado con logos de clientes.
7. **Contacto** — datos y formulario de consulta.

## Notas

- Los logos de clientes y marcas de terceros son propiedad de sus respectivos titulares y se muestran a título de referencia comercial.
- El formulario de contacto actualmente solo muestra un mensaje de confirmación en el cliente; falta conectarlo a un backend/servicio de envío.
