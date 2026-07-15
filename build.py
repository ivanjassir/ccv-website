#!/usr/bin/env python3
"""CCV Grupo static site generator.

Renders the homepage + division landing pages from `content/` through the
Jinja2 templates in `templates/`, then regenerates the self-contained
`preview.html` (homepage with CSS/JS inlined and images embedded as base64).

Usage:  python3 build.py
"""
import base64
import json
import mimetypes
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
YEAR = 2026

env = Environment(
    loader=FileSystemLoader(str(ROOT / "templates")),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# ---- load content ----
site = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
divisions = [
    json.loads(p.read_text(encoding="utf-8"))
    for p in sorted((ROOT / "content/divisions").glob("*.json"))
]
divisions.sort(key=lambda d: d.get("order", 99))

categories_dir = ROOT / "content/categories"
categories = [
    json.loads(p.read_text(encoding="utf-8"))
    for p in sorted(categories_dir.glob("*.json"))
] if categories_dir.exists() else []
categories.sort(key=lambda c: (c.get("parent", {}).get("slug", ""), c.get("order", 99)))
cat_by_slug = {c["slug"]: c for c in categories}


def crumbs_for(c):
    """Ancestor chain (division -> ... -> parent) for breadcrumbs, top-first."""
    chain, par, seen = [], c.get("parent"), set()
    while par and par.get("slug") not in seen:
        seen.add(par["slug"])
        chain.append({"slug": par["slug"], "name": par["name"]})
        nxt = cat_by_slug.get(par["slug"])
        par = nxt.get("parent") if nxt else None
    chain.reverse()
    return chain


pages_dir = ROOT / "content/pages"
pages = [
    json.loads(p.read_text(encoding="utf-8"))
    for p in sorted(pages_dir.glob("*.json"))
] if pages_dir.exists() else []

current_region = next(
    (r for r in site["regions"] if r.get("current")), site["regions"][0]
)

GLOBAL = {
    "site": site,
    "divisions": divisions,
    "categories": categories,
    "current_region": current_region,
    "year": YEAR,
}


def write(rel_path: str, html: str) -> None:
    (ROOT / rel_path).write_text(html, encoding="utf-8")
    print(f"  {rel_path}")


# ---- render pages ----
print("Rendering pages…")
home_meta = {
    "title": "CCV Grupo — Corporación Científica Venezolana | Venezuela",
    "description": "CCV Grupo Venezuela: equipos, servicios y proyectos para su laboratorio. Más de 40 años de experiencia con soporte técnico local.",
}
urls = []  # for sitemap
write("index.html", env.get_template("home.html").render(**GLOBAL, meta=home_meta, page="home", canonical_path="index.html"))
urls.append("index.html")
for d in divisions:
    path = f"{d['slug']}.html"
    write(path, env.get_template("division.html").render(**GLOBAL, division=d, meta=d["meta"], page="division", canonical_path=path))
    urls.append(path)
for c in categories:
    path = f"{c['slug']}.html"
    write(path, env.get_template("category.html").render(**GLOBAL, cat=c, crumbs=crumbs_for(c), meta=c["meta"], page="category", canonical_path=path))
    urls.append(path)
for pg in pages:
    path = f"{pg['slug']}.html"
    write(path, env.get_template("page.html").render(**GLOBAL, pg=pg, meta=pg["meta"], page="page", canonical_path=path))
    urls.append(path)

# ---- custom 404 (not in sitemap) ----
write("404.html", env.get_template("404.html").render(
    **GLOBAL, meta={"title": "Página no encontrada | CCV Grupo Venezuela",
                    "description": "La página que busca no existe o fue movida."},
    page="404", canonical_path="404.html"))

# ---- sitemap.xml + robots.txt ----
base = site["base_url"].rstrip("/")
today = "2026-07-15"
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = "1.0" if u == "index.html" else "0.7"
    sm.append(f"  <url><loc>{base}/{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
write("sitemap.xml", "\n".join(sm) + "\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

# ---- self-contained preview.html (homepage, fully inlined) ----
print("Building self-contained preview.html…")
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "assets/css/styles.css").read_text(encoding="utf-8")
js = (ROOT / "assets/js/script.js").read_text(encoding="utf-8")
html = html.replace(
    '<link rel="stylesheet" href="assets/css/styles.css" />', f"<style>\n{css}\n</style>"
)
html = html.replace(
    '<script src="assets/js/script.js"></script>', f"<script>\n{js}\n</script>"
)
# 1x only in the shareable file — keeps it lean
html = re.sub(r'\s+srcset="assets/images/[^"]*"', "", html)


def data_uri(rel: str) -> str:
    p = ROOT / rel
    mime, _ = mimetypes.guess_type(str(p))
    if mime is None:
        mime = "image/svg+xml" if p.suffix == ".svg" else "application/octet-stream"
    return "data:" + mime + ";base64," + base64.b64encode(p.read_bytes()).decode("ascii")


html = re.sub(r'src="(assets/images/[^"]+)"', lambda m: f'src="{data_uri(m.group(1))}"', html)
html = re.sub(r'href="(assets/images/[^"]+)"', lambda m: f'href="{data_uri(m.group(1))}"', html)
(ROOT / "preview.html").write_text(html, encoding="utf-8")
leftover = re.findall(r'(?:src|href)="(assets/[^"]+)"', html)
size_mb = (ROOT / "preview.html").stat().st_size / (1024 * 1024)
print(f"  preview.html ({size_mb:.2f} MB) — leftover local refs: {leftover or 'none'}")

print(f"\nDone: 1 home + {len(divisions)} divisions + {len(categories)} categories + {len(pages)} pages + preview.html")
