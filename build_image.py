#!/usr/bin/env python3
"""Build the news-image-20261124 entry: a one-page newspaper front page
summing up Tuesday 24 November 2026. Draws everything in code with PIL:
masthead, three illustrated lead panels, a figures strip, a world map with
15 labelled pins, and a 40-story grid. Output: entry.png, 1024x1024."""

import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = "/tmp/news24-panels"
LAND_GEOJSON = "/tmp/ne_land.geojson"
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 250, 246)
INK = (17, 24, 39)
NAVY = (20, 38, 74)
NAVY_LIGHT = (30, 58, 95)
RED = (185, 28, 28)
GOLD = (217, 164, 65)
GRAY = (100, 116, 139)
LIGHT_LINE = (203, 213, 225)
OCEAN = (221, 232, 241)
LAND = (174, 191, 169)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 34)
F_MAST = font("DejaVuSans-Bold.ttf", 19)
F_KICK = font("DejaVuSans-Bold.ttf", 11)
F_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_SUB = font("DejaVuSans.ttf", 11)
F_FIG = font("DejaVuSans-Bold.ttf", 24)
F_FIG_LBL = font("DejaVuSans.ttf", 10)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_GRID = font("DejaVuSans.ttf", 12)
F_MAP = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 9)


def wrap(text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    tw = fnt.getlength(text)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- figures
FIGURES = [
    ("700,000+", "Russian soldiers\nkilled in Ukraine"),
    ("+31%", "Nvidia shares\nin a single day"),
    ("+6.5%", "Nasdaq rally\non the day"),
    ("26", "dead in the Indonesia\nfactory fire"),
    ("40", "wounded in the\nZaporizhzhia strike"),
    ("2.82m", "rials per US dollar\non the black market"),
]

# ------------------------------------------------------------------- map
# (lon, lat, label, dx, dy) — label offset in px from the pin.
PINS = [
    (114.06, 22.55, "Shenzhen", 8, -6),
    (13.40, 52.52, "Berlin", -52, 4),
    (34.47, 31.50, "Gaza", 8, 4),
    (35.14, 47.84, "Zaporizhzhia", 8, -16),
    (20.07, 32.12, "Benghazi", -52, 4),
    (46.68, 24.71, "Riyadh", 8, -6),
    (106.16, -6.12, "Serang", 8, -6),
    (126.98, 37.57, "Seoul", 8, -6),
    (51.39, 35.69, "Tehran", -16, -16),
    (30.52, 50.45, "Kyiv", -30, -16),
    (30.25, 1.57, "Bunia, DR Congo", 8, 4),
    (-3.70, 40.42, "Madrid", -52, -6),
    (-77.04, 38.90, "Washington", -34, 4),
    (-0.13, 51.51, "London", -20, -24),
    (28.98, 41.01, "Istanbul", 8, 4),
]

# ------------------------------------------------------------------ grid
# (category, headline) — 40 stories, two columns of 20.
CAT_COLORS = {
    "WAR": (185, 28, 28),
    "MARKETS": (21, 128, 61),
    "TECH": (29, 78, 216),
    "SPORT": (194, 65, 12),
    "WORLD": (51, 65, 85),
}
GRID = [
    ("WAR", "Zaporizhzhia apartment strike kills 2, wounds 40"),
    ("WAR", "700,000+ Russian soldiers killed, analysis finds"),
    ("WAR", "Ukraine drones sink Russian ships off Libya"),
    ("WAR", "NATO vows to defend space after nuclear-satellite reports"),
    ("WAR", "Vance and Rubio meet Qatari PM as Iranian rial plunges"),
    ("WAR", "Houthi attack on Riyadh tower wounds 11"),
    ("WORLD", "Indonesia factory fire death toll hits 26, 8 missing"),
    ("TECH", "BepiColombo enters Mercury orbit despite glitch"),
    ("WAR", "Russian jets enter South Korea's air defence zone"),
    ("WAR", "Germany first to get Ukraine's Delta battle system"),
    ("TECH", "UN chief calls for a global AI safety framework"),
    ("SPORT", "Champions League: Real Madrid 5-1 PSV, stay perfect"),
    ("WORLD", "UK sanctions Myanmar generals after ICJ ruling"),
    ("WORLD", "UK sanctions the Houthis as an entity"),
    ("TECH", "US blacklists Singapore cloud firm Megaspeed"),
    ("WORLD", "South Korea offers $375,000 to catch AI exam cheats"),
    ("WORLD", "Pentagon: Canada falls short as defence partner"),
    ("TECH", "FBI probes possible breach of police NCIC database"),
    ("TECH", "Europol disrupts 57 illegal IPTV services"),
    ("WORLD", "Iraq orders oil ministry to run Kurdish oilfields"),
    ("WORLD", "Ebola responders trapped in DR Congo hospital"),
    ("WORLD", "Amnesty: Ethiopia Tigray strikes may be war crimes"),
    ("WORLD", "Ex-PM Hasina plans return to Bangladesh on 16 Dec"),
    ("WORLD", "Trump to expedite federal death sentences"),
    ("WAR", "Hegseth yet to approve 60 Patriot interceptors"),
    ("WAR", "UK warns firms backing Ukraine of Russian sabotage"),
    ("TECH", "China launches coordinated 6G pilot testing"),
    ("TECH", "Chinese LLMs beat US models in cyber test"),
    ("TECH", "Meta brings Muse AI into Instagram DMs"),
    ("TECH", "Uber and Nuro test driverless Lucid robotaxis"),
    ("TECH", "LaLiga data breach steals fans' personal data"),
    ("TECH", "Cleverbridge confirms payment card data copied"),
    ("TECH", "US states challenge Character.AI chat sale"),
    ("TECH", "US probes cyberattacks on up to 50 oil vessels"),
    ("WORLD", "Gaza issues meningitis epidemic alert"),
    ("WORLD", "Oxfam: Gaza now a 'toxic wasteland'"),
    ("WAR", "300+ Russians killed backing Mali's junta"),
    ("WAR", "Russian drone briefly crosses into Polish airspace"),
    ("WAR", "Seven EU states push to limit Russian visas"),
    ("WAR", "Zelensky calls for NATO to admit Ukraine"),
]

# ------------------------------------------------------------------ leads
LEADS = [
    ("nvidia", "MARKETS",
     "Nvidia soars 31% as Huang returns as CEO",
     "Trump says he \u201cmade the deal\u201d; Nasdaq +6.5%, S&P 500 +4.75%"),
    ("ukraine", "UKRAINE",
     "Europe demands a seat at the Ukraine peace talks",
     "After Trump\u2019s call from Air Force One, Berlin insists on a place at the table"),
    ("gaza", "GAZA",
     "Israeli strike kills Hamas security chief in Gaza",
     "Naeem Abu Nahel killed in Gaza City; six others dead"),
]


def draw_map(draw, box):
    """Equirectangular world map from Natural Earth land polygons."""
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0
    draw.rectangle(box, fill=OCEAN)
    with open(LAND_GEOJSON) as f:
        land = json.load(f)
    for feat in land["features"]:
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]
        for poly in polys:
            for ring in poly:
                pts = []
                for lon, lat in ring:
                    if lat < -60:
                        lat = -60
                    px = x0 + (lon + 180.0) / 360.0 * mw
                    py = y0 + (90.0 - lat) / 150.0 * mh
                    pts.append((px, py))
                if len(pts) > 2:
                    draw.polygon(pts, fill=LAND)
    draw.rectangle(box, outline=LIGHT_LINE, width=1)
    for lon, lat, label, dx, dy in PINS:
        px = x0 + (lon + 180.0) / 360.0 * mw
        py = y0 + (90.0 - lat) / 150.0 * mh
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((px + dx, py + dy), label, font=F_MAP, fill=NAVY,
                  stroke_width=3, stroke_fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 86], fill=NAVY)
    d.text((0, 0), "", font=F_MAST, fill=GOLD)  # keep fonts warm
    center(d, 12, "THE WORLD IN ONE IMAGE", F_MAST, GOLD)
    center(d, 38, "TUESDAY 24 NOVEMBER 2026", F_TITLE, (255, 255, 255))
    d.rectangle([0, 86, W, 89], fill=RED)

    # ------------------------------------------------------- lead panels
    pxs = [12, 349, 686]
    for i, (panel, kicker, head, sub) in enumerate(LEADS):
        x = pxs[i]
        im = Image.open(os.path.join(PANELS_DIR, panel + ".png")).convert("RGB")
        # centre-crop to 326x158
        tw, th = 326, 158
        scale = max(tw / im.width, th / im.height)
        nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
        im = im.resize((nw, nh), Image.LANCZOS)
        left, top = (nw - tw) // 2, (nh - th) // 2
        img.paste(im.crop((left, top, left + tw, top + th)), (x, 96))
        d.rectangle([x, 96, x + tw, 96 + th], outline=LIGHT_LINE, width=1)
        d.text((x, 260), kicker, font=F_KICK, fill=RED)
        y = 276
        for line in wrap(head, F_HEAD, 326):
            d.text((x, y), line, font=F_HEAD, fill=INK)
            y += 19
        y += 2
        for line in wrap(sub, F_SUB, 326):
            d.text((x, y), line, font=F_SUB, fill=GRAY)
            y += 14

    # ------------------------------------------------------- figures strip
    d.text((12, 360), "THE DAY IN FIGURES", font=F_SEC, fill=NAVY)
    bx = 12
    for num, lbl in FIGURES:
        d.rectangle([bx, 378, bx + 163, 438], fill=(255, 255, 255),
                    outline=LIGHT_LINE, width=1)
        d.rectangle([bx, 378, bx + 163, 381], fill=NAVY)
        center(d, 384, num, F_FIG, INK, bx, bx + 163)
        lines = lbl.split("\n")
        ly = 410
        for line in lines:
            center(d, ly, line, F_FIG_LBL, GRAY, bx, bx + 163)
            ly += 11
        bx += 167

    # -------------------------------------------------------------- map
    d.text((12, 446), "THE DAY ON THE MAP", font=F_SEC, fill=NAVY)
    draw_map(d, (12, 464, 1012, 664))

    # -------------------------------------------------------------- grid
    d.text((12, 672), "MORE OF THE DAY \u2014 40 STORIES", font=F_SEC, fill=NAVY)
    for i, (cat, head) in enumerate(GRID):
        col = i // 20
        row = i % 20
        x = 12 + col * 510
        y = 692 + row * 16
        d.ellipse([x, y + 3, x + 7, y + 10], fill=CAT_COLORS[cat])
        d.text((x + 13, y), head, font=F_GRID, fill=INK)

    # ------------------------------------------------------------- footer
    center(d, 1013,
           "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 ESA \u00b7 UEFA \u00b7 UN News \u2014 "
           "All stories happened or were first reported on Tuesday 24 November 2026",
           F_FOOT, GRAY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
