# CCV Grupo Venezuela — QA, UX/UI & Conversion Audit + Improvement Plan

**Date:** 2026-07-15 · **Scope:** the rebuilt static site (92 pages, generated
via `build.py`). **Method:** automated technical QA (links, assets, meta, a11y),
heuristic UX/UI review (Nielsen), user-journey walkthroughs, and a conversion /
A-B backlog. Findings are grounded in measured data, not assumptions.

Severity: **[H]** high · **[M]** medium · **[L]** low.

---

## 1. Technical QA — findings

**Strengths (verified):** every page has exactly one `<h1>`; all `<img>` have
`alt`; no broken internal links; no emoji; content is visible without JS
(reveal gated behind `.js`); `prefers-reduced-motion` respected; semantic
landmarks + skip link; external links use `rel="noopener"`.

**Gaps:**
- **[H] No SEO metadata** — missing `canonical`, Open Graph, Twitter cards, and
  JSON-LD structured data (Organization, BreadcrumbList, Product/Service). Weak
  search ranking and poor link previews when shared.
- **[H] No `sitemap.xml` / `robots.txt`** — 92 pages with no crawl guidance.
- **[M] No favicon / `apple-touch-icon` / `theme-color`.**
- **[M] No custom `404` page.**
- **[M] Image weight** — client logo `cvg.png` is 476 KB; division card `@2x`
  PNGs are ~300–380 KB each. Converting to WebP/AVIF + correct sizing saves
  roughly 2–3 MB site-wide (10.6 MB today, excl. the catalog PDF).
- **[M] Catalog PDF weight** — `lacteos-y-derivados.pdf` is 5 MB, loaded in an
  iframe; large on mobile data.
- **[L] No analytics / instrumentation** — no way to measure any of the below.

---

## 2. Accessibility (WCAG 2.1 AA)

- **[M] Dropdowns** (Divisiones, Región) open on hover/`:focus-within` but
  `aria-expanded` is static `"false"` and there's no Esc-to-close. Works with a
  keyboard but doesn't announce state. Manage `aria-expanded` + add Esc.
- **[L] Contrast** — brand teal `#0e7d8e` on white ≈ 4.5:1 (borderline AA for
  normal text); muted `#5b6b83` on white ≈ 5.7:1 (pass). Verify small text on
  the `--soft` background and lighten/darken where borderline.
- **[L] Focus-visible** — ensure a consistent visible focus ring on all
  interactive elements (links, cards-as-links, buttons).
- Positives: form labels present, `role="status"` on form note, `lang="es"`.

---

## 3. UX/UI heuristic review

- **IA / navigation [strong]** — clear 3-level hierarchy (división → sector →
  aplicación) with working breadcrumbs on inner pages and a Divisiones dropdown.
- **[H] No site search** — with 92 pages, users can't jump straight to
  "petroquímica" or "esterilización". Add search or a single **"Todas las
  soluciones"** index page (cheap, big findability win).
- **[H] Contact / quote friction** — the only contact path is the homepage
  `#contacto` anchor with a `mailto:` fallback that opens the user's mail
  client. For Venezuelan B2B, add **WhatsApp** + click-to-call and a real form
  backend; consider a standalone `/contacto` page.
- **[M] No persistent conversion CTA** — add a sticky "Solicitar asesoría /
  WhatsApp" bar so contact is always one tap away on long solution pages.
- **[M] Catalog inconsistency** — only one page (lácteos) has an embedded
  catalog; others don't. Set expectations or resolve the catalog strategy.
- **[M] Trust assets** — good clients strip + stats; add representation/brand
  certifications and 1–2 case references or testimonials for credibility.
- **[L] Locale** — Spanish only; the region switcher hints at a group. An EN
  toggle could help multinational procurement (later).
- **Positives:** consistent design system, strong hero, the animated process
  band, real content + brands per page post-enrichment.

---

## 4. User-journey tests

**A — QC lab manager (food), needs a milk-fat analyzer.**
Home → Divisiones → Equipos → Alimentos y Bebidas → Lácteos → sees analyses +
Gerber catalog + "Solicitar asesoría". *Works well once in the tree; 4 clicks
from home and no search to shortcut it.*

**B — Pharma project engineer, needs a sterilizer.**
Home → Soluciones Farma → Sistema de Esterilización → Telstar SteriDelta +
process + CTA. *Good; friction: no spec sheet/catalog on Farma pages, and the
CTA is generic rather than "request a quote".*

**C — Procurement, wants to get a quote fast.**
Nav "Contáctenos" → home `#contacto` → `mailto:` compose. *Highest friction:
no dedicated contact page, no WhatsApp, mailto may deter. This is the top
conversion leak.*

**Cross-cutting friction:** (1) no search, (2) contact/quote friction, (3)
catalog inconsistent. Breadcrumbs and back-navigation are fine.

---

## 5. A/B test backlog (needs analytics first)

| # | Hypothesis | Variant vs control | Primary metric |
|---|------------|--------------------|----------------|
| 1 | A quote-oriented hero CTA lifts contacts | "Solicitar asesoría" primary vs "Explorar divisiones" | CTA CTR → contact starts |
| 2 | A sticky WhatsApp/phone bar lifts contacts | sticky bar vs none | contact conversions |
| 3 | Solution-page CTA wording | "Solicitar cotización" vs "Solicitar asesoría" | contact submit rate |
| 4 | Shorter form converts better | 3 fields vs 4 (drop empresa) | form completion |
| 5 | Catalog label | "Descargar catálogo (PDF)" vs "Ver catálogo" | catalog opens |
| 6 | Process band position | near top vs mid page | scroll depth + contact |

Each needs a defined sample size / minimum runtime and adequate traffic.

---

## 6. Prioritized roadmap (impact × effort)

**Quick wins — high impact, low effort (do first; the generator can emit most):**
- SEO essentials: `canonical` + Open Graph/Twitter + JSON-LD (Organization +
  per-page Breadcrumb/Service) + `sitemap.xml` + `robots.txt` + favicon set.
- WhatsApp + click-to-call **sticky contact** bar.
- Image optimization → WebP/AVIF + responsive `sizes` (cut ~2–3 MB).
- Custom `404.html`.

**Medium:**
- Site search or a **"Todas las soluciones"** index page.
- Standalone `/contacto` page + real form backend (e.g. Formspree/Web3Forms).
- Manage `aria-expanded` + Esc on dropdowns; audit focus-visible.
- Analytics (GA4 or Plausible) + event instrumentation + Core Web Vitals.

**Larger:**
- A/B testing harness (after analytics + sufficient traffic).
- Catalog strategy resolution (host key PDFs natively / a Recursos page).
- EN language option.

---

## 7. Instrumentation to add first (unblocks §5)

Analytics with events: `division_view`, `solution_view`, `catalog_open`,
`contact_start`, `contact_submit`, `whatsapp_click`; plus Core Web Vitals
(LCP/CLS/INP) monitoring.

---

## 8. Recommendation

Ship the **Quick wins** as one batch — they're mostly generator-emitted
(SEO/sitemap/favicon/404), plus the WhatsApp sticky bar and image optimization —
for an immediate SEO + conversion + performance lift. Then add analytics so the
A/B backlog (§5) can actually be measured. I can implement the entire Quick-wins
batch now on request.
