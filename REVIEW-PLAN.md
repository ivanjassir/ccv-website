# CCV.com.ve — Site Review & Rebuild Plan

**Goal:** migrate the remaining ~110 pages of `www.ccv.com.ve` into the new
design system (the rebuilt homepage), rebranded as **CCV Grupo**, with the
**countries served** surfaced. This plan tiers the work, defines a review
rubric, and sequences delivery.

**Status:** Homepage (`index.html`) rebuilt ✅. Everything below is the "rest".

---

## 1. Key insight — it's ~6 templates, not 110 designs

The live site has ~110 URLs, but almost all are content instances of a handful
of repeating layouts. Build the templates once, generate the pages from content.

| # | Archetype | Count | Example URLs |
|---|-----------|------|--------------|
| A | Home | 1 | `/` — **done** |
| B | Division landing | 7 | `division-laboratorio`, `solucionesfarma`, `division-informatica`, `division-mobiliario`, `life-science`, `servicio-tecnico`, `division-filtracion` |
| C | Sector / industry | 8 | `alimentos-y-bebidas`, `petroleo-y-energia`, `medio-ambiente`, `geologia-mineria`, `agroindustria`, `ciencia-materiales`, `industria-quimica`, `farmaceutica-y-cosmetica` |
| D | Sub-sector / application | ~40 | `lacteos-y-derivados`, `bebidas`, `cafe`, `crudo`, `petroquimica`, `microbiologia`, `corrosion`, `metalurgica`, `cemento-y-concreto`, `polimeros`, … |
| E | Product-category (Farma & Proyectos) | ~30 | `ingenieriafarmaceutica`, `sistemadeesterilizacion` (+3 children), `sistemadeliofilizacion` (+2), `aguapwywfiyvaporpuro` (+4), `salasblancasyequiposasociados` (+4), `cabinadeflujolaminar`, `campanasdeextracciondegases`, … |
| F | Product / equipment detail | ~15 | `pcr`, `secuenciadores-de-adn`, `microscopia`, `lectores-de-placas`, `incubadora`, `binder`, `camara-de-clima-constante`, hornos (×3), … |
| G | Brand | 2 | `marcas`, `perkin-elmer` |
| H | Utility / conversion | ~5 | `contactenos`, `seminarios` (`copia-de-contáctenos`), `cursosdecapacitacion`, `consultoria`, `copia-de-seminarios` |
| — | **Retire (Wix duplicates)** | ~5 | `copia-de-*` pages ("copia de" = "copy of") — consolidate & redirect, do not rebuild |

Templates to build (Phase 0): **B** division landing · **C** sector · **E**
product-category · **F** product detail · **G** brand · **H** utility.
The homepage is a one-off. That's it.

---

## 2. New global requirements (this session)

- **CCV Grupo branding.** Treat `ccv.com.ve` as the **Venezuela site under the
  CCV Grupo master brand**. Header shows "CCV Grupo" with a "Venezuela" locator;
  add a lightweight region switcher (Venezuela / Colombia / Perú). Apply to
  logo, footer, `<title>`/meta, and copy.
- **Countries served.** New reusable component: a "Presencia regional" strip/map
  showing **Venezuela, Colombia, Perú** with links to the sister sites
  (`ccvgrupo.com`, `ccvgrupo.com.co`). Place on the homepage (new section) and in
  the global footer. Both are Phase 0 (global, touch every page via the shared
  header/footer).

---

## 3. Per-page review rubric (the "review" itself)

Every page passes an AEGIS-style 8-point check before sign-off:

1. **Content** — copy matches live site, correct Spanish, no placeholder, clean heading hierarchy, action-title style.
2. **Design system** — uses shared tokens/components; spacing, type, color consistent with homepage.
3. **Brand** — CCV Grupo header/footer, correct logo, region locator.
4. **Responsive** — mobile / tablet / desktop; banner-card behavior verified.
5. **Robustness (no-JS)** — content visible without JavaScript; real values seeded, not `0`; all `<img>` have `alt`. *(The lesson from the blank-preview bug.)*
6. **Links & nav** — no broken internal links; nav + breadcrumbs consistent; sister-site links valid.
7. **Assets** — correct images, optimized, `loading="lazy"`, `srcset` for retina.
8. **SEO / a11y** — `<title>`, meta description, `lang`, canonical; contrast, focus states, skip link, aria.

---

## 4. Recommended approach — data-driven generation

Hand-authoring 110 HTML files will drift and rot. Recommendation: **content in
structured data (JSON/Markdown) rendered through the 6 templates by a build
step** (extend the existing `build_preview.py`, or adopt a small SSG like
Astro/Eleventy). One CSS/JS component library, one place to fix bugs, consistent
output. Deliverables: `content/*.json`, `templates/*.html`, `build.py`, and a
generated `dist/`.

Alternative (only if a generator is off the table): a shared partial header/
footer + copy-paste templates, hand-filled per page. Faster to start, expensive
to maintain across 110 pages.

---

## 5. Phasing

- **Phase 0 — Foundations.** Extract shared CSS/JS into a component library;
  build the 6 templates; add CCV Grupo brand + region switcher + "Presencia
  regional" (countries) component; stand up the generator + content schema;
  build the SEO/redirect map (incl. retiring `copia-de-*`). *Unblocks all pages.*
- **Phase 1 — Division landings (B, 7).** Highest nav priority.
- **Phase 2 — Sector pages (C, 8).**
- **Phase 3 — Product-category pages (E, ~30).**
- **Phase 4 — Sub-sector (D, ~40) + product detail (F, ~15).** Bulk, templated.
- **Phase 5 — Brands (G, 2) + utility/conversion (H, ~5).** Contact form, seminars, courses.
- **Phase 6 — Cleanup & launch.** Retire duplicates + 301 redirects; full-site
  QA sweep against the rubric; link crawl; performance/Lighthouse pass.

Cross-cutting (runs through all phases): **content migration** (scrape live copy
per page), **asset collection** (images/logos/brand marks), **QA sign-off** per
the rubric.

---

## 6. Effort (T-shirt)

| Phase | Size | Notes |
|-------|------|-------|
| 0 Foundations | L | Templates + generator + brand/countries; the real investment |
| 1 Divisions | M | 7 pages, first template shake-out |
| 2 Sectors | M | 8 pages |
| 3 Product-category | L | ~30 pages, but templated |
| 4 Sub-sector + detail | L | ~55 pages, mostly content entry |
| 5 Brands + utility | S | Contact form needs a real backend decision |
| 6 Cleanup & launch | M | Redirects + QA crawl |

Once Phase 0 lands, per-page cost is minutes (content entry), not hours.

---

## 7. Decisions — LOCKED (2026-07-14)

1. **Build approach** ✅ **Data-driven generator.** Content in JSON/Markdown
   rendered through the 6 templates by a build step (extend `build_preview.py`).
   One component library; generated `dist/`.
2. **Scope** ✅ **Prioritized subset first** — Phase 0 foundations + division
   landings (7) + sector pages (8) + top product-category pages, then expand.
   Prune `copia-de-*` duplicates.
3. **Branding** ✅ **CCV Grupo + Venezuela locator** — header shows "CCV Grupo"
   with a "Venezuela" locator and a region switcher (VE/CO/PE).
4. **Contact form / seminars backend** — *still open* (Phase 5): static mailto
   (current) vs. a real submission endpoint. Not blocking Phase 0.

### Immediate next step — Phase 0 kickoff

Deliverables when we start: (a) shared component library (extract homepage
CSS/JS), (b) content schema + generator, (c) the 6 templates, (d) CCV Grupo
header/footer + region switcher, (e) "Presencia regional" (countries) component,
(f) SEO/redirect map. Say the word and I'll scaffold it.

---

## 8. Risks

- **Scope** — 110 pages invites creep; the template+generator approach and tiered
  phasing contain it.
- **Content accuracy** — technical Spanish product specs; needs a content source
  of truth and a review pass.
- **Asset availability** — many product images to source; may need client assets.
- **Wix cruft** — duplicate/orphan pages; handle with the redirect map, don't port.
- **Consistency** — mitigated by one component library + the per-page rubric.
