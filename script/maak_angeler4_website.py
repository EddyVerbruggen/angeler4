#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║        Angeler 4 — Website Generator                ║
╠══════════════════════════════════════════════════════╣
║  Gebruik vanuit Terminal:                            ║
║      python3 ~/Desktop/maak_angeler4_website.py      ║
║                                                      ║
║  De website verschijnt op:                           ║
║      ~/Desktop/Angeler4-website/index.html           ║
╚══════════════════════════════════════════════════════╝
"""

import os, sys, shutil
from pathlib import Path

# ── Pillow voor afbeeldingsoptimalisatie (optioneel) ─────────────────────────
try:
    from PIL import Image, ImageOps
    HAS_PIL = True
    print("✓ Pillow gevonden — foto's worden geoptimaliseerd voor web")
except ImportError:
    HAS_PIL = False
    print("ℹ  Pillow niet gevonden — foto's worden 1:1 gekopieerd (grotere bestanden)")
    print("   Tip: pip3 install Pillow")
print()

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATIE
# ═════════════════════════════════════════════════════════════════════════════

BRON  = Path("/Users/eddy/Desktop/Huizen/Angeler 4")
DOEL  = Path("/Users/eddy/sandboxes/angeler4")
IMG   = DOEL / "img"

MAX_W = 1800   # breedte voor volledig scherm in lichtbak
THB_W = 900    # breedte voor thumbnail in grid (optioneel kleinere versie)

# ── Indeling vorige eigenaar foto's op ruimte ─────────────────────────────
# Gebaseerd op steekproef van de nummers (839-916)
VORIGE_SECTIES = [
    {"id": "v-buiten",    "naam": "Exterieur",               "nums": range(839, 842)},
    {"id": "v-woonkamer", "naam": "Woonkamer",               "nums": range(842, 854)},
    {"id": "v-kantoor",   "naam": "Kantoor",                 "nums": range(854, 856)},
    {"id": "v-hal",       "naam": "Hal",                     "nums": range(1856, 1875)},
    {"id": "v-keuken",    "naam": "Keuken",                  "nums": range(858, 863)},
    {"id": "v-slaap",     "naam": "Master bedroom",          "nums": range(864, 873)},
    {"id": "v-verdiep",   "naam": "Verdieping",              "nums": range(875, 889)},
    {"id": "v-tuin",      "naam": "Tuin",                    "nums": range(889, 917)},
    {"id": "v-tuinhuis",  "naam": "Tuinhuis",                "nums": range(1902, 1908)},
]

# ── Plattegronden ─────────────────────────────────────────────────────────
PLATTEGRONDEN = [
    ("Begane grond.png",     "Begane grond"),
    ("Eerste verdieping.png","Eerste verdieping"),
    ("Garage.png",           "Garage"),
    ("Overkapping.png",      "Overkapping"),
    ("Perceel.png",          "Perceel"),
    ("Tuinhuis.png",         "Tuinhuis"),
]

# ── AI-renders / inspiratie ───────────────────────────────────────────────
# Elk plan heeft een id, naam, is_plan-vlag en een lijst van (submap, bestand) tuples.
RENDERS = [
    {
        "id": "r-woonkamer", "naam": "Woonkamer", "is_plan": False,
        "fotos": [
            ("woonkamer", "ChatGPT Image 19 apr 2026, 08_31_09.png"),
            ("woonkamer", "ChatGPT Image 19 apr 2026, 08_33_17.png"),
            ("woonkamer", "ChatGPT Image 19 apr 2026, 08_35_24.png"),
            ("woonkamer", "ChatGPT Image 16 mei 2026, 07_54_05.png"),
            ("woonkamer", "ChatGPT Image 16 mei 2026, 07_59_04.png"),
            ("woonkamer", "ChatGPT Image 16 mei 2026, 08_02_23.png"),
            ("woonkamer", "01 - Gemini  - maar dan de haard op de grond en een sonos arc tussen haard en tv.png"),
            ("woonkamer", "02 - Gemini met meubel maar daar moet nog een haard in en de tv lager.png"),
            ("woonkamer", "Woonkamer - bovenaanzicht (render).png"),
            ("woonkamer", "Gezellige_woonkamer_voor_7_personen_met_grote_TV,_elektrische_haard_en_golden_hoekbank.png"),
            ("woonkamer", "Woonkamer_ontwerp_voor_monumentale_boerderij_met_elektrische_haard_onder_ramen.png"),
        ]
    },
    {
        "id": "r-keuken", "naam": "Keuken & Eetkamer", "is_plan": False,
        "fotos": [
            ("keuken & eetkamer", "Eethoekontwerp_met_VIERKANTE_tafel_225x225_cm,_banken_aan_beide_zijden_en_TV.png"),
            ("keuken & eetkamer", "Vernieuwd_eethoekontwerp_met_vierkante_tafel,_banken_aan_2_zijden,_eetkamerstoelen_en_geïntegreerde_TV.png"),
            ("keuken & eetkamer", "ChatGPT Image 17 jan 2026, 21_05_10.png"),
            ("keuken & eetkamer", "Gemini_Generated_Image_cjvxywcjvxywcjvx.png"),
            ("keuken & eetkamer", "generated-image-keuken.png"),
        ]
    },
    {
        "id": "r-kantoor", "naam": "Kantoor", "is_plan": False,
        "fotos": [
            ("kantoor", "tegenover - render 1.png"),
            ("kantoor", "tegenover - render 2.png"),
            ("kantoor", "Kantoor - nieuwe deur - wit.png"),
            ("kantoor", "Kantoor - nieuwe deur - zwart.png"),
            ("kantoor", "tegenover - ikea design.jpeg"),
        ]
    },
    {
        "id": "r-overkapping", "naam": "Overkapping", "is_plan": False,
        "fotos": [
            ("overkapping", "Luxurious_covered_patio_redesign_with_cozy_seating,_full_bar,_ambient_lighting,_and_entertainment_setup_for_warm_summer_evenings.png"),
            ("overkapping", "Gemini_Generated_Image_bg6tiqbg6tiqbg6t.png"),
            ("overkapping", "Gemini_Generated_Image_y4mnry4mnry4mnry.png"),
        ]
    },
    {
        "id": "r-jacuzzi", "naam": "Jacuzzi & Achtertuin", "is_plan": True,
        "fotos": [
            ("jacuzzi", "achtertuin-links.jpg"),
            ("jacuzzi", "achteruin-boven.jpg"),
            ("jacuzzi", "achteruin-rechts.jpg"),
            ("jacuzzi", "ChatGPT Image 10 jan 2026, 14_35_43.png"),
            ("jacuzzi", "ChatGPT Image 11 jan 2026, 12_47_41.png"),
            ("jacuzzi", "Gemini_Generated_Image_4m2ggl4m2ggl4m2g.png"),
            ("jacuzzi", "Gemini_Generated_Image_lcci6flcci6flcci.png"),
            ("jacuzzi", "generated-image-jacuzzi.png"),
            ("jacuzzi", "jacuzzi.png"),
        ]
    },
    {
        "id": "r-carport", "naam": "Carport", "is_plan": True,
        "fotos": [
            ("carport", "carport locatie.png"),
            ("carport", "carport stijl.png"),
            ("carport", "Gemini_Generated_Image_diraridiraridira.png"),
            ("carport", "grappig bovenaanzicht.png"),
        ]
    },
    {
        "id": "r-tuinhuis", "naam": "Tuinhuis", "is_plan": False,
        "fotos": [
            ("tuinhuis", "Design Fleur.jpeg"),
            ("tuinhuis", "buitenkant-andere-kleur.png"),
            ("tuinhuis", "interieur-ontwerp.png"),
            ("tuinhuis", "interieur-render-ongeveer.png"),
        ]
    },
    {
        "id": "r-slaapkamers", "naam": "Slaapkamer en Overloop boven", "is_plan": False,
        "fotos": [
            ("slaapkamer boven, 1-naar-kleinste", "render.png"),
            ("overloop", "ChatGPT Image 17 jan 2026, 21_37_30 - die loper is leuk.png"),
        ]
    },
]

# ═════════════════════════════════════════════════════════════════════════════
# HULPFUNCTIES
# ═════════════════════════════════════════════════════════════════════════════

def verwerk_foto(src: Path, dst: Path, max_breedte: int) -> bool:
    """Kopieer (en optimaliseer) één afbeelding naar de doelmap."""
    if dst.exists():
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        if HAS_PIL:
            img = Image.open(src)
            img = ImageOps.exif_transpose(img)          # EXIF-rotatie corrigeren
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            w, h = img.size
            if w > max_breedte:
                schaal = max_breedte / w
                img = img.resize((max_breedte, int(h * schaal)), Image.LANCZOS)
            ext = dst.suffix.lower()
            if ext in (".jpg", ".jpeg"):
                img.save(dst, "JPEG", quality=85, optimize=True)
            elif ext == ".png":
                img.save(dst, "PNG", optimize=True)
            elif ext == ".webp":
                img.save(dst, "WEBP", quality=85)
            else:
                img.save(dst)
        else:
            shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"    ⚠  {src.name}: {e}")
        return False


def rel(pad: Path) -> str:
    """Geeft het pad relatief aan DOEL terug als web-pad."""
    return str(pad.relative_to(DOEL)).replace("\\", "/")


# ═════════════════════════════════════════════════════════════════════════════
# STAP 1 — DIRECTORIES
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 1: Mappen aanmaken ─────────────────────────────")
for d in [IMG / "funda-v", IMG / "funda-e", IMG / "renders", IMG / "plattegronden"]:
    d.mkdir(parents=True, exist_ok=True)
print(f"   Doelmap: {DOEL}\n")


# ═════════════════════════════════════════════════════════════════════════════
# STAP 2 — FOTO'S VORIGE EIGENAAR
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 2: Foto's vorige eigenaar ──────────────────────")
vorige_data = []
bronmap_v = BRON / "foto's funda vorige eigenaar"

for sectie in VORIGE_SECTIES:
    fotos = []
    for num in sectie["nums"]:
        src = bronmap_v / f"{num}.jpg"
        if not src.exists():
            continue
        dst = IMG / "funda-v" / f"{num}.jpg"
        print(f"   {num}.jpg", end="  ")
        sys.stdout.flush()
        if verwerk_foto(src, dst, MAX_W):
            fotos.append(rel(dst))
            print("✓")
        else:
            print("✗")
    if fotos:
        vorige_data.append({**sectie, "fotos": fotos})

print(f"   → {sum(len(s['fotos']) for s in vorige_data)} foto's verwerkt\n")


# ═════════════════════════════════════════════════════════════════════════════
# STAP 3 — FOTO'S EERVORIGE EIGENAAR
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 3: Foto's eervorige eigenaar ───────────────────")
bronmap_e  = BRON / "foto's funda eervorige eigenaar"
ee_buiten  = []
ee_interieur = []

for f in sorted(bronmap_e.iterdir()):
    if f.name.startswith("_") or f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue
    dst = IMG / "funda-e" / f.name
    print(f"   {f.name[:55]}", end="  ")
    sys.stdout.flush()
    if verwerk_foto(f, dst, MAX_W):
        pad = rel(dst)
        if "Buiten" in f.name:
            ee_buiten.append(pad)
        else:
            ee_interieur.append(pad)
        print("✓")
    else:
        print("✗")

print(f"   → {len(ee_buiten)} buitenfoto's, {len(ee_interieur)} interieur\n")


# ═════════════════════════════════════════════════════════════════════════════
# STAP 4 — PLATTEGRONDEN
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 4: Plattegronden ───────────────────────────────")
platte_data = []
for bestand, label in PLATTEGRONDEN:
    src = BRON / "plattegronden" / bestand
    if not src.exists():
        continue
    dst = IMG / "plattegronden" / bestand
    if verwerk_foto(src, dst, 2400):
        platte_data.append((rel(dst), label))
        print(f"   {label} ✓")
print()


# ═════════════════════════════════════════════════════════════════════════════
# STAP 5 — RENDERS
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 5: Inspiratie & renders ────────────────────────")
render_data = []
for plan in RENDERS:
    fotos = []
    for submap, bestand in plan["fotos"]:
        src = BRON / submap / bestand
        if not src.exists():
            print(f"   Niet gevonden: {submap}/{bestand}")
            continue
        dst = IMG / "renders" / src.name
        if verwerk_foto(src, dst, MAX_W):
            fotos.append(rel(dst))
    if fotos:
        render_data.append({**plan, "fotos": fotos})
        print(f"   {plan['naam']}: {len(fotos)} foto's ✓")
    else:
        print(f"   {plan['naam']}: geen foto's gevonden")
print()


# ═════════════════════════════════════════════════════════════════════════════
# STAP 6 — HTML GENEREREN
# ═════════════════════════════════════════════════════════════════════════════

print("── Stap 6: HTML genereren ──────────────────────────────")

def gallery_html(fotos, sectie_id):
    """Genereer een fotogrid met lichtbak-koppeling."""
    lines = [f'<div class="grid" id="{sectie_id}">']
    for i, pad in enumerate(fotos):
        lines.append(
            f'  <img src="{pad}" loading="lazy" '
            f'data-group="{sectie_id}" data-index="{i}" '
            f'onclick="openLightbox(this)" alt="">'
        )
    lines.append('</div>')
    return "\n".join(lines)


# ── Hero afbeelding bepalen ───────────────────────────────────────────────
hero_img = "img/funda-e/Buiten - Angeler 4 - Nijkerk-1.jpg"
if vorige_data:
    for s in vorige_data:
        if "buiten" in s["id"]:
            hero_img = s["fotos"][0]
            break

# ── Navigatie links ───────────────────────────────────────────────────────
nav_links = ""
for s in vorige_data:
    nav_links += f'<li><a href="#{s["id"]}">{s["naam"]}</a></li>\n'
if ee_buiten or ee_interieur:
    nav_links += '<li><a href="#eervorige">Eervorige eigenaar</a></li>\n'
if render_data:
    nav_links += '<li><a href="#inspiratie">Inspiratie</a></li>\n'
if platte_data:
    nav_links += '<li><a href="#plattegronden">Plattegronden</a></li>\n'

# ── Vorige eigenaar secties ───────────────────────────────────────────────
vorige_html = ""
for s in vorige_data:
    grid = gallery_html(s["fotos"], s["id"])
    vorige_html += f"""
<div class="ruimte-sectie" id="{s['id']}">
  <h3 class="ruimte-naam">{s['naam']}</h3>
  {grid}
</div>
"""

# ── Eervorige eigenaar ────────────────────────────────────────────────────
eervorige_html = ""
if ee_buiten:
    eervorige_html += f"""
<div class="ruimte-sectie" id="ee-buiten">
  <h3 class="ruimte-naam">Exterieur</h3>
  {gallery_html(ee_buiten, "ee-buiten")}
</div>
"""
if ee_interieur:
    eervorige_html += f"""
<div class="ruimte-sectie" id="ee-interieur">
  <h3 class="ruimte-naam">Interieur</h3>
  {gallery_html(ee_interieur, "ee-interieur")}
</div>
"""

# ── Inspiratie / renders ──────────────────────────────────────────────────
render_secties_html = ""
for r in render_data:
    badge_txt = "Toekomstplan" if r["is_plan"] else "Idee"
    badge_cls = "plan" if r["is_plan"] else "render"
    grid = gallery_html(r["fotos"], r["id"])
    render_secties_html += f"""
<div class="ruimte-sectie" id="{r['id']}">
  <h3 class="ruimte-naam">{r['naam']} <span class="badge {badge_cls}">{badge_txt}</span></h3>
  {grid}
</div>
"""

# ── Plattegronden ─────────────────────────────────────────────────────────
platte_cards = ""
for pad, label in platte_data:
    platte_cards += f"""
<div class="platte-card" onclick="openLightbox(this.querySelector('img'))" style="cursor:pointer">
  <div class="platte-img"><img src="{pad}" loading="lazy" data-group="plattegronden" data-index="{platte_data.index((pad,label))}" alt="{label}"></div>
  <div class="platte-label">{label}</div>
</div>
"""

platte_paden_js = ", ".join(f'"{p}"' for p, _ in platte_data)

# ═════════════════════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═════════════════════════════════════════════════════════════════════════════

HTML = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Angeler 4 — Nijkerk</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --groen:#2C4A2E;--groen-l:#3D6641;--creme:#FAF8F2;--warm:#F3EFE6;
  --zand:#D9C9A8;--roest:#9E5A3A;--tekst:#1E1C17;--gedempd:#6B6455;
  --rand:rgba(44,74,46,0.15);
}}
html{{scroll-behavior:smooth}}
body{{font-family:'Jost',sans-serif;background:var(--creme);color:var(--tekst);font-size:16px;line-height:1.7}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:200;background:rgba(250,248,242,0.94);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--rand);
  display:flex;align-items:center;justify-content:space-between;padding:0 3rem;height:64px}}
.nav-logo{{font-family:'Playfair Display',serif;font-size:1.2rem;color:var(--groen);text-decoration:none;letter-spacing:.04em}}
.nav-links{{display:flex;gap:0;list-style:none;overflow-x:auto}}
.nav-links a{{display:block;padding:.5rem .9rem;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--gedempd);text-decoration:none;white-space:nowrap;transition:color .2s}}
.nav-links a:hover{{color:var(--groen)}}

/* HERO */
.hero{{margin-top:64px;height:calc(100vh - 64px);min-height:520px;position:relative;overflow:hidden;display:flex;align-items:flex-end}}
.hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 55%}}
.hero-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,20,10,.7) 0%,rgba(10,20,10,.1) 55%,transparent 100%)}}
.hero-content{{position:relative;z-index:2;padding:3rem 4rem}}
.hero-oog{{font-size:.72rem;letter-spacing:.28em;text-transform:uppercase;color:var(--zand);margin-bottom:.9rem;font-weight:300}}
.hero-titel{{font-family:'Playfair Display',serif;font-size:clamp(2.8rem,6.5vw,5rem);font-weight:400;color:#fff;line-height:1.05;margin-bottom:1.4rem}}
.hero-titel em{{font-style:italic}}
.hero-sub{{font-size:1rem;color:rgba(255,255,255,.65);font-weight:300;max-width:440px;margin-bottom:2rem}}
.btn-ghost{{display:inline-block;padding:.7rem 1.8rem;border:1px solid rgba(255,255,255,.5);color:#fff;
  font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:all .25s}}
.btn-ghost:hover{{background:#fff;color:var(--groen);border-color:#fff}}

/* SECTIES */
.sectie{{padding:5rem 4rem}}
.sectie-oog{{font-size:.7rem;letter-spacing:.24em;text-transform:uppercase;color:var(--roest);margin-bottom:.7rem;font-weight:500}}
.sectie-titel{{font-family:'Playfair Display',serif;font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:400;
  line-height:1.15;color:var(--groen)}}
.sectie-titel em{{font-style:italic}}
.streep{{width:44px;height:2px;background:var(--roest);margin:1.1rem 0}}
.sectie-tekst{{font-size:.95rem;color:var(--gedempd);line-height:1.8;max-width:580px}}
.inner{{max-width:1260px;margin:0 auto}}

/* RUIMTE-SECTIE */
.ruimte-sectie{{margin-bottom:3.5rem}}
.ruimte-naam{{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:400;
  color:var(--groen);margin-bottom:1rem;padding-bottom:.5rem;border-bottom:1px solid var(--rand)}}

/* FOTO-GRID */
.grid{{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  gap:8px;margin-bottom:.5rem
}}
.grid img{{width:100%;height:220px;object-fit:cover;display:block;cursor:pointer;
  transition:opacity .2s,transform .3s}}
.grid img:hover{{opacity:.88;transform:scale(1.01)}}

/* KLEUREN */
.bg-warm{{background:var(--warm)}}
.bg-creme{{background:var(--creme)}}

/* BADGE — inline in ruimte-naam */
.badge{{display:inline-block;font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;
  padding:.2rem .55rem;vertical-align:middle;margin-left:.5rem;position:relative;top:-2px}}
.badge.render{{background:var(--groen);color:#fff}}
.badge.plan{{background:var(--roest);color:#fff}}

/* PLATTEGRONDEN GRID */
.platte-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.5rem;margin-top:2rem}}
.platte-card{{border:1px solid var(--rand);overflow:hidden;background:#fff}}
.platte-img{{padding:1.5rem;display:flex;align-items:center;justify-content:center;background:#fff;aspect-ratio:4/3}}
.platte-img img{{width:100%;height:100%;object-fit:contain}}
.platte-label{{padding:.7rem 1rem;border-top:1px solid var(--rand);font-size:.84rem;font-weight:500;color:var(--groen)}}

/* FOOTER */
footer{{background:var(--tekst);color:rgba(255,255,255,.45);padding:2.5rem 4rem;
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem}}
.footer-logo{{font-family:'Playfair Display',serif;font-size:1.2rem;color:rgba(255,255,255,.85)}}
.footer-sub{{font-size:.76rem}}

/* LICHTBAK */
#lb{{display:none;position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.92);
  align-items:center;justify-content:center}}
#lb.open{{display:flex}}
#lb img{{max-width:92vw;max-height:88vh;object-fit:contain;display:block;user-select:none}}
#lb-close{{position:absolute;top:1.2rem;right:1.5rem;font-size:2rem;color:rgba(255,255,255,.7);
  cursor:pointer;line-height:1;background:none;border:none;font-family:sans-serif}}
#lb-close:hover{{color:#fff}}
#lb-prev,#lb-next{{position:absolute;top:50%;transform:translateY(-50%);
  background:none;border:none;color:rgba(255,255,255,.6);font-size:2.5rem;
  cursor:pointer;padding:.5rem 1rem;line-height:1;user-select:none}}
#lb-prev{{left:.5rem}} #lb-next{{right:.5rem}}
#lb-prev:hover,#lb-next:hover{{color:#fff}}
#lb-teller{{position:absolute;bottom:1rem;left:50%;transform:translateX(-50%);
  color:rgba(255,255,255,.45);font-size:.8rem;letter-spacing:.1em}}

/* RESPONSIVE */
@media(max-width:900px){{
  nav{{padding:0 1rem}} .nav-links a{{padding:.5rem .6rem;font-size:.65rem}}
  .sectie{{padding:3.5rem 1.2rem}}
  .hero-content{{padding:2rem 1.5rem}}
  footer{{padding:2rem 1.5rem}}
  .grid{{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}}
  .grid img{{height:160px}}
}}
</style>
</head>
<body>

<!-- NAVIGATIE -->
<nav>
  <a href="#" class="nav-logo">Angeler&nbsp;4</a>
  <ul class="nav-links">
    {nav_links}
  </ul>
</nav>

<!-- HERO -->
<div class="hero">
  <img src="{hero_img}" alt="Angeler 4">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <p class="hero-oog">Gemeentelijk monument · Nijkerk</p>
    <h1 class="hero-titel">Een <em>monumentale</em><br>boerderij</h1>
    <p class="hero-sub">Ons nieuwe thuis — van aankoop tot droomhuis, stap voor stap vastgelegd.</p>
    <a href="#{vorige_data[0]['id'] if vorige_data else 'inspiratie'}" class="btn-ghost">Bekijk de foto's</a>
  </div>
</div>

<!-- VORIGE EIGENAAR -->
<section class="sectie bg-warm" id="vorige">
  <div class="inner">
    <p class="sectie-oog">Funda · Vorige eigenaar</p>
    <h2 class="sectie-titel">Hoe het <em>was</em></h2>
    <div class="streep"></div>
    <p class="sectie-tekst">De professionele Funda-foto's van de vorige eigenaar — per ruimte gegroepeerd.</p>
    <div style="margin-top:3rem">
      {vorige_html}
    </div>
  </div>
</section>

<!-- EERVORIGE EIGENAAR -->
{"" if not eervorige_html else f'''
<section class="sectie bg-creme" id="eervorige">
  <div class="inner">
    <p class="sectie-oog">Funda · Eervorige eigenaar</p>
    <h2 class="sectie-titel">Nog <em>verder</em> terug</h2>
    <div class="streep"></div>
    <p class="sectie-tekst">De foto\'s uit de nog eerdere verkoop — het huis in een andere tijdsgeest.</p>
    <div style="margin-top:3rem">
      {eervorige_html}
    </div>
  </div>
</section>
'''}

<!-- INSPIRATIE -->
{"" if not render_data else f'''
<section class="sectie bg-warm" id="inspiratie">
  <div class="inner">
    <p class="sectie-oog">Ideeën & renders</p>
    <h2 class="sectie-titel"><em>Inspiratie</em></h2>
    <div class="streep"></div>
    <p class="sectie-tekst">Met AI-renders (ChatGPT, Gemini) zijn de ideeën voor elke ruimte al concreet gemaakt. Slechts ideeën — maar wat voor ideeën.</p>
    <div style="margin-top:3rem">
      {render_secties_html}
    </div>
  </div>
</section>
'''}

<!-- PLATTEGRONDEN -->
{"" if not platte_data else f'''
<section class="sectie bg-creme" id="plattegronden">
  <div class="inner">
    <p class="sectie-oog">Indeling</p>
    <h2 class="sectie-titel"><em>Plattegronden</em></h2>
    <div class="streep"></div>
    <p class="sectie-tekst">Alle lagen van het perceel — van begane grond tot tuinhuis en garage.</p>
    <div class="platte-grid">
      {platte_cards}
    </div>
  </div>
</section>
'''}

<!-- FOOTER -->
<footer>
  <div class="footer-logo">Angeler 4</div>
  <div class="footer-sub">Gemeentelijk monument · Nijkerk · Onze verbouwing in beeld</div>
</footer>

<!-- LICHTBAK -->
<div id="lb">
  <button id="lb-close" onclick="closeLightbox()">×</button>
  <button id="lb-prev" onclick="navLightbox(-1)">&#8249;</button>
  <img id="lb-img" src="" alt="">
  <button id="lb-next" onclick="navLightbox(1)">&#8250;</button>
  <div id="lb-teller"></div>
</div>

<script>
// ── Lichtbak ──────────────────────────────────────────────────────────────
const lb       = document.getElementById('lb');
const lbImg    = document.getElementById('lb-img');
const lbTeller = document.getElementById('lb-teller');

const groepen = {{}};

document.querySelectorAll('.grid img').forEach(img => {{
  const g = img.dataset.group;
  if (!groepen[g]) groepen[g] = [];
  groepen[g].push(img.src);
}});

groepen['plattegronden'] = [{platte_paden_js}];

let huidigGroep = null;
let huidigIndex = 0;

function openLightbox(img) {{
  const g = img.dataset.group;
  const i = parseInt(img.dataset.index) || 0;
  huidigGroep = g;
  huidigIndex = i;
  toonFoto();
  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function toonFoto() {{
  const fotos = groepen[huidigGroep] || [];
  if (!fotos.length) return;
  lbImg.src = fotos[huidigIndex];
  lbTeller.textContent = (huidigIndex + 1) + ' / ' + fotos.length;
}}

function navLightbox(richting) {{
  const fotos = groepen[huidigGroep] || [];
  huidigIndex = (huidigIndex + richting + fotos.length) % fotos.length;
  toonFoto();
}}

function closeLightbox() {{
  lb.classList.remove('open');
  document.body.style.overflow = '';
  lbImg.src = '';
}}

lb.addEventListener('click', e => {{ if (e.target === lb) closeLightbox(); }});

document.addEventListener('keydown', e => {{
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape')      closeLightbox();
  if (e.key === 'ArrowRight')  navLightbox(1);
  if (e.key === 'ArrowLeft')   navLightbox(-1);
}});

let touchStart = 0;
lb.addEventListener('touchstart', e => touchStart = e.changedTouches[0].clientX);
lb.addEventListener('touchend',   e => {{
  const delta = e.changedTouches[0].clientX - touchStart;
  if (Math.abs(delta) > 50) navLightbox(delta < 0 ? 1 : -1);
}});
</script>

</body>
</html>
"""

html_pad = DOEL / "index.html"
html_pad.write_text(HTML, encoding="utf-8")
print(f"   index.html geschreven ✓\n")


# ═════════════════════════════════════════════════════════════════════════════
# KLAAR
# ═════════════════════════════════════════════════════════════════════════════

totaal_fotos = (
    sum(len(s["fotos"]) for s in vorige_data)
    + len(ee_buiten) + len(ee_interieur)
    + sum(len(r["fotos"]) for r in render_data)
    + len(platte_data)
)

print("═" * 55)
print(f"  ✓  Website klaar! {totaal_fotos} foto's verwerkt.")
print(f"     Open: {DOEL / 'index.html'}")
print("═" * 55)

import subprocess
subprocess.run(["open", str(DOEL / "index.html")])
