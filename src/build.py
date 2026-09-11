#!/usr/bin/env python3
"""Assemble les pages de la maquette à partir de partials (≈ header.php / footer.php
d'un thème WordPress). Usage : python3 src/build.py"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

ICONS = {
  "arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
  "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>',
  "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
  "folder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
  "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
  "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.5-4 3-6 6.5-6s6 2 6.5 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.5c3 0 5.5 1.5 6 5.5"/></svg>',
  "message": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/></svg>',
  "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
  "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
  "bell": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/></svg>',
  "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6.2 6.8.8-5 4.6 1.3 6.7L12 17.5l-6 3.3 1.3-6.7-5-4.6 6.8-.8z"/></svg>',
  "award": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9" r="6"/><path d="M8.5 14.5L7 22l5-3 5 3-1.5-7.5"/></svg>',
  "france": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-6-5.3-6-11a6 6 0 0 1 12 0c0 5.7-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/></svg>',
  "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/></svg>',
  "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg>',
  "help": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01"/></svg>',
  "history": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5M12 7v5l3 2"/></svg>',
  "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>',
  "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
  "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/></svg>',
  "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.5 8.5v11h-3v-11zm-1.5-5a1.8 1.8 0 1 1 0 3.6 1.8 1.8 0 0 1 0-3.6zM20.5 13.2v6.3h-3v-5.6c0-1.4-.5-2.4-1.8-2.4-1 0-1.6.7-1.8 1.3-.1.2-.1.6-.1.9v5.8h-3v-11h3V10c.4-.6 1.1-1.5 2.8-1.5 2 0 3.9 1.3 3.9 4.7z"/></svg>',
  "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.3-1.5 1.5-1.5h1.5V5.1c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.6v7z"/></svg>',
  "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor"/></svg>',
  "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3z"/></svg>',
  "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
  "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
  "logo": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4c6 0 9 9 11.5 17 3.8 11-2.9 21-11.5 21S8.7 32 12.5 21C15 13 18 4 24 4z" fill="#5B7A1F"/><path d="M24 4c6 0 9 9 11.5 17L24 24z" fill="#DCCB4F"/><path d="M12.5 21C15 13 18 4 24 4v20z" fill="#3D5516"/><path d="M24 24l11.5-3c3.8 11-2.9 21-11.5 21z" fill="#A9C24A"/><ellipse cx="24" cy="30" rx="5.5" ry="6.4" fill="#A4492F"/></svg>',
}

import hashlib
def _v(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:8]
ASSET_V = {"css": _v("assets/css/main.css"), "js": _v("assets/js/main.js")}

def render(name, out, root):
    tpl = (SRC / "pages" / name).read_text(encoding="utf-8")
    parts = {p.stem: (SRC / "partials" / p.name).read_text(encoding="utf-8") for p in (SRC / "partials").glob("*.html")}
    def sub(s):
        s = re.sub(r"\{\{partial:(\w+)\}\}", lambda m: parts[m.group(1)], s)
        s = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], s)
        s = s.replace("{{v:css}}", ASSET_V["css"]).replace("{{v:js}}", ASSET_V["js"])
        return s.replace("{{root}}", root)
    html = sub(sub(tpl))
    (ROOT / out).write_text(html, encoding="utf-8")
    print("→", out, len(html), "octets")

render("index.html", "index.html", "")
render("fonctionnalites.html", "fonctionnalites.html", "")
render("tarifs.html", "tarifs.html", "")
render("article.html", "blog/article.html", "../")
