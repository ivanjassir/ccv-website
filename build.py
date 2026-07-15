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
current_region = next(
    (r for r in site["regions"] if r.get("current")), site["regions"][0]
)

GLOBAL = {
    "site": site,
    "divisions": divisions,
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
write("index.html", env.get_template("home.html").render(**GLOBAL, meta=home_meta, page="home"))
for d in divisions:
    write(
        f"{d['slug']}.html",
        env.get_template("division.html").render(**GLOBAL, division=d, meta=d["meta"], page="division"),
    )

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
(ROOT / "preview.html").write_text(html, encoding="utf-8")
leftover = re.findall(r'(?:src|href)="(assets/[^"]+)"', html)
size_mb = (ROOT / "preview.html").stat().st_size / (1024 * 1024)
print(f"  preview.html ({size_mb:.2f} MB) — leftover local refs: {leftover or 'none'}")

print(f"\nDone: 1 home + {len(divisions)} division pages + preview.html")
