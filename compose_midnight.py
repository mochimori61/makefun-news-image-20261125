#!/usr/bin/env python3
"""THE MIDNIGHT GAZETTE — News Image 20261125, Akun 20.

Tuesday 25 November 2026 in black and fire orange: the night
edition, set after dark, when the day can finally be read
whole — 37 stories, 9 regions, every story dated.
Stdlib (PIL) only. Deterministic.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MX = 26

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(n, bold=False, disp=False):
    return ImageFont.truetype(SERIF if disp else (SANSB if bold else SANS), n)


def T(d, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# palette — black & fire orange
PAPER = (238, 233, 226)
PAPER_D = (215, 205, 191)
WHITE = (250, 248, 244)
BLACK = (14, 13, 12)
BLACK_L = (40, 36, 33)
FIRE = (240, 110, 40)
FIRE_D = (188, 70, 16)
INK = (26, 22, 20)
MUTE = (120, 108, 98)

# ------------------------------------------------------------- the day
# num: (region, headline, deck, source, tag, chip)
# Stacked lead headlines fit one line; grid decks fit two.
CARDS = {
    6: ("6 · WORLD — UKRAINE",
        "700,000 Russian dead, new count finds",
        "New analysis counts 700,000+ Russian soldiers killed "
        "in the nearly five-year war on Ukraine.",
        "RFE/RL", "REPORTED", "700,000+ KILLED"),
    3: ("3 · MIDDLE EAST — IRAQ",
        "Baghdad orders oilfields seized",
        "Federal units ordered to seize the Kurdish oilfields.",
        "Starlit / wires", "REPORTED", "OILFIELDS ORDER"),
    4: ("4 · MIDDLE EAST — GAZA",
        "Drone strikes kill security chief",
        "7 killed in Gaza: a security chief, 3 policemen, 3 siblings.",
        "Al Jazeera", "REPORTED", "7 KILLED IN STRIKES"),
    1: ("1 · EUROPE — POLAND",
        "NATO sends jets to Poland",
        "AWACS to Poland after missiles landed; Merz vows support.",
        "wire reports", "REPORTED", "AWACS TO POLAND"),
    2: ("2 · MIDDLE EAST — HORMUZ",
        "Iran says 3 tankers hit by mines",
        "The IRGC Navy claims 3 tankers hit by mines at Hormuz.",
        "Iranian claim", "CLAIMED", "TANKERS HIT — IRAN SAYS"),
    36: ("36 · WORLD — NVIDIA",
         "Nvidia's $1 trillion Monday",
         "Monday close: shares +31.5%, $1tn clawed back.",
         "Forbes via wires", "REPORTED", "+31.5% MONDAY CLOSE"),
    13: ("13 · OCEANIA — AUSTRALIA",
         "12 coral species brought back",
         "Reef genetics resurrect 12 Acropora coral species.",
         "science wires", "REPORTED", "12 SPECIES BACK"),
    5: ("5 · EUROPE — BRUSSELS",
        "EU unveils new Russia sanctions",
        "New restrictive measures on Russia amid the Ukraine war.",
        "wire roundups", "REPORTED", "NEW EU SANCTIONS"),
    33: ("33 · WORLD — WASHINGTON",
         "PCE inflation report due today",
         "Due Tuesday 25 November; no figure had landed at close.",
         "scheduled", "SCHEDULED", "PCE DUE TODAY"),
    10: ("10 · ASIA — CHINA",
         "Xiamen Airlines orders 50 Boeing jets",
         "China Southern unit agrees to acquire 50 Boeing 737-8 jets.",
         "wire reports", "REPORTED", "50 JETS ORDERED"),
    37: ("37 · AMERICAS — USA",
         "Storms target Thanksgiving travel",
         "Storms on both coasts threaten Thanksgiving travel.",
         "wire reports", "REPORTED", "STORMS BOTH COASTS"),
    34: ("34 · AMERICAS · TECH",
         "US targets 7 firms over chips",
         "Washington targets 7 firms — one Alibaba-owned — "
         "over chip diversion.",
         "wires", "REPORTED", "7 FIRMS TARGETED"),
    11: ("11 · EUROPE — MADRID",
         "Madrid rout PSV 5-1 in comeback",
         "5-1 from behind: Bellingham stunner, Mbappé brace.",
         "wire reports", "REPORTED", "MADRID 5-1 PSV"),
}
LEADS = [6, 3, 4]
GRID = [1, 2, 36, 13, 5, 33, 10, 37, 34, 11]

BRIEFS = [
    (7, "First 5 Lynx KF41 IFVs enter Ukrainian service"),
    (8, "Colombia car bomb injures at least 23"),
    (9, "Gunmen hold dozens in a Cartagena supermarket"),
    (12, "England level T20 series, chasing 185"),
    (14, "Fiji declares disaster in El Niño dry spell"),
    (15, "Iran pharmacies run dry in medicine shortage"),
    (16, "Iran braces for winter gas shortages"),
    (17, "Britain sanctions the Houthis' top leaders"),
    (18, "Senegal AFCON title restored by CAS ruling"),
    (19, "Rebels pull back in DR Congo after clashes"),
    (20, "Nigerian emir suspended after allegation"),
    (21, "Sudan RSF commander defects"),
    (22, "Cameroon separatist in Norway court"),
    (23, "Punjab: BJP and Akali Dal reunite as allies"),
    (24, "Bangladesh opens Guangzhou investment office"),
    (25, "Indonesia's vice-president resigns"),
    (26, "Solomons eye Australia treaty switch"),
    (27, "North Korea touts China ties in Pyongyang"),
    (28, "Denmark court upholds ghetto evictions law"),
    (29, "Sarkozy headed for Libya-case trial"),
    (30, "Black Sea clash at the UN"),
    (31, "Shortwave school for Afghan girls"),
    (32, "Dimorphos casts its shadow on Didymos"),
    (35, "Moscow buys inflatable decoys from China"),
]

NUMBERS = [
    ("700,000+", "RUSSIAN DEAD", "#6"),
    ("3", "TANKERS, HORMUZ", "#2"),
    ("50", "BOEING JETS", "#10"),
    ("23", "INJURED, COLOMBIA", "#8"),
    ("12", "CORAL SPECIES", "#13"),
    ("5–1", "MADRID v PSV", "#11"),
    ("+31.5%", "NVIDIA MONDAY", "#36"),
    ("7", "FIRMS TARGETED", "#34"),
]

REGIONS = [("EUROPE", 8), ("MIDDLE EAST", 6), ("WORLD", 6), ("AFRICA", 5),
           ("AMERICAS", 4), ("ASIA", 2), ("SOUTH ASIA", 2),
           ("ASIA-PACIFIC", 2), ("OCEANIA", 2)]

DATESTRIP = [
    ("22 NOV", "Iran rationing began"),
    ("MON CLOSE", "Nvidia +31.5%"),
    ("TUE 25 NOV", "PCE report due"),
    ("TODAY", "AWACS plan for Poland"),
    ("2027", "Punjab alliance vote"),
]

TIMELINE = [
    ("MON CLOSE", "Nvidia +31.5% — Monday close"),
    ("DUSK", "NATO AWACS plan reported"),
    ("EVENING", "Iran says 3 tankers mined"),
    ("NIGHT", "Baghdad oilfield order"),
    ("TODAY", "US PCE report due — none yet"),
    ("MIDNIGHT", "Storms target travel"),
]

DATECHECK = [
    "Mercury story — dated 23 Nov, not tonight",
    "COP31 talks — earlier in Nov, not tonight",
    "Liverpool 4–0 — earlier round, not tonight",
    "GTA VI hype — no release today, not tonight",
]

PINS = [(6, 0.625, 0.22), (3, 0.635, 0.38), (4, 0.645, 0.62),
        (1, 0.575, 0.13), (2, 0.66, 0.50), (36, 0.145, 0.46),
        (13, 0.915, 0.82), (5, 0.56, 0.30), (33, 0.185, 0.33),
        (10, 0.845, 0.30), (37, 0.195, 0.58), (34, 0.155, 0.20),
        (11, 0.55, 0.46)]

MAP_ROWS = [
    "..........",
    ".####.....",
    "########..",
    ".######...",
    "..####....",
    "...##..#..",
    "......####",
    ".....######",
    "......####",
    ".......##.",
]


# ------------------------------------------------------------- scenes
def _sky(d, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(h - 1, 1)
        d.line([x, y + i, x + w, y + i],
               fill=tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3)))


def sc_crosses(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 28, 26))
    for r in range(4):
        for c in range(9):
            cx = x + w * (0.08 + c * 0.105) + (r % 2) * 5
            cy = y + h * (0.18 + r * 0.22)
            d.line([cx, cy - 6, cx, cy + 6], fill=(214, 206, 192), width=2)
            d.line([cx - 4, cy - 2, cx + 4, cy - 2], fill=(214, 206, 192), width=2)
    d.ellipse([x + w * 0.86, y + h * 0.1, x + w * 0.93, y + h * 0.24], fill=(238, 230, 210))


def sc_derricks(d, x, y, w, h):
    _sky(d, x, y, w, h, (96, 74, 60), (150, 116, 84))
    d.rectangle([x, y + h * 0.8, x + w, y + h], fill=(110, 88, 58))
    for fx in (0.3, 0.68):
        bx, by = x + w * fx, y + h * 0.8
        d.line([bx - 16, by, bx, by - h * 0.52], fill=(16, 14, 12), width=3)
        d.line([bx + 16, by, bx, by - h * 0.52], fill=(16, 14, 12), width=3)
        d.line([bx - 10, by - h * 0.2, bx + 10, by - h * 0.2], fill=(16, 14, 12), width=2)
        d.polygon([(bx, by - h * 0.62), (bx + 8, by - h * 0.46), (bx - 2, by - h * 0.46)],
                  fill=FIRE)


def sc_gaza(d, x, y, w, h):
    _sky(d, x, y, w, h, (52, 46, 54), (110, 92, 84))
    gy = y + h * 0.78
    for bx, bw, bh in [(0.04, 0.13, 0.34), (0.20, 0.10, 0.24), (0.33, 0.15, 0.44),
                       (0.51, 0.11, 0.30), (0.65, 0.14, 0.38), (0.82, 0.12, 0.26)]:
        d.rectangle([x + w * bx, gy - h * bh, x + w * (bx + bw), gy], fill=(22, 20, 22))
        d.rectangle([x + w * (bx + 0.03), gy - h * (bh - 0.08),
                     x + w * (bx + 0.06), gy - h * (bh - 0.16)], fill=(246, 190, 100))
    d.line([x + w * 0.58, y + h * 0.16, x + w * 0.86, y + h * 0.16], fill=(14, 12, 14), width=3)
    d.rectangle([x + w * 0.68, y + h * 0.10, x + w * 0.76, y + h * 0.16], fill=(14, 12, 14))
    d.rectangle([x, gy, x + w, y + h], fill=(34, 30, 28))


def sc_awacs(d, x, y, w, h):
    _sky(d, x, y, w, h, (70, 80, 96), (120, 128, 138))
    cx, cy = x + w * 0.5, y + h * 0.52
    d.ellipse([cx - 34, cy - 26, cx + 34, cy + 26], outline=(230, 226, 218), width=2)
    d.line([x + w * 0.1, cy, x + w * 0.9, cy], fill=(16, 15, 14), width=3)
    d.polygon([(x + w * 0.1, cy), (x + w * 0.2, cy - 7), (x + w * 0.2, cy + 7)],
              fill=FIRE)
    d.rectangle([cx - 4, cy - 12, cx + 4, cy - 4], fill=(16, 15, 14))


def sc_tankers(d, x, y, w, h):
    _sky(d, x, y, w, h, (60, 70, 84), (104, 116, 122))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 52, 66))
    for fx in (0.16, 0.5, 0.84):
        cx = x + w * fx
        d.polygon([(cx - 26, y + h * 0.55), (cx + 26, y + h * 0.55),
                   (cx + 18, y + h * 0.68), (cx - 18, y + h * 0.68)], fill=(14, 13, 12))
        d.rectangle([cx - 16, y + h * 0.44, cx + 16, y + h * 0.55], fill=(150, 52, 36))
    d.ellipse([x + w * 0.3, y + h * 0.8, x + w * 0.36, y + h * 0.9],
              outline=(8, 8, 8), width=2)


def sc_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 15, 14))
    pts = [(0.06, 0.72), (0.3, 0.66), (0.52, 0.7), (0.74, 0.4), (0.94, 0.2)]
    for i in range(len(pts) - 1):
        d.line([x + w * pts[i][0], y + h * pts[i][1],
                x + w * pts[i + 1][0], y + h * pts[i + 1][1]], fill=(96, 204, 124), width=3)
    d.rectangle([x + w * 0.55, y + h * 0.08, x + w * 0.97, y + h * 0.34],
                outline=(96, 204, 124), width=1)
    T(d, (x + w * 0.6, y + h * 0.12), "+31.5%", F(13, True), (96, 204, 124))


def sc_coral(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 198))
    d.rectangle([x, y + h * 0.8, x + w, y + h], fill=(196, 182, 148))
    for fx, s in [(0.24, 1.0), (0.5, 1.25), (0.76, 0.9)]:
        bx, by = x + w * fx, y + h * 0.82
        col = (206, 96, 80)
        d.line([bx, by, bx, by - h * 0.3 * s], fill=col, width=3)
        d.line([bx, by - h * 0.18 * s, bx - w * 0.07, by - h * 0.36 * s], fill=col, width=2)
        d.line([bx, by - h * 0.2 * s, bx + w * 0.07, by - h * 0.4 * s], fill=col, width=2)
        d.ellipse([bx - w * 0.085, by - h * 0.42 * s, bx - w * 0.055, by - h * 0.36 * s], fill=col)
        d.ellipse([bx + w * 0.055, by - h * 0.46 * s, bx + w * 0.085, by - h * 0.4 * s], fill=col)


def sc_arc(d, x, y, w, h):
    _sky(d, x, y, w, h, (120, 116, 110), (168, 160, 148))
    for i in range(9):
        t = i / 8
        px = x + w * (0.12 + t * 0.76)
        py = y + h * (0.62 - 0.4 * (1 - (2 * t - 1) ** 2))
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=FIRE_D)
    d.line([x + w * 0.08, y + h * 0.66, x + w * 0.92, y + h * 0.66], fill=INK, width=2)


def sc_report(d, x, y, w, h):
    _sky(d, x, y, w, h, (140, 134, 126), (180, 172, 160))
    pw, ph = w * 0.4, h * 0.78
    px, py = x + (w - pw) / 2, y + h * 0.1
    d.rectangle([px, py, px + pw, py + ph], fill=(250, 248, 240), outline=INK, width=1)
    for i in range(4):
        d.line([px + 8, py + 12 + i * 11, px + pw - 8, py + 12 + i * 11],
               fill=(172, 164, 152), width=2)
    ccx, ccy = px + pw * 0.72, py + ph * 0.68
    d.ellipse([ccx - 11, ccy - 11, ccx + 11, ccy + 11], outline=FIRE_D, width=2)
    T(d, (ccx, ccy - 1), "?", F(14, True), FIRE_D, anchor="mm")


def sc_jets(d, x, y, w, h):
    _sky(d, x, y, w, h, (88, 102, 120), (140, 154, 168))
    for fy, fx, s in [(0.34, 0.3, 1.0), (0.58, 0.62, 0.8)]:
        cx, cy = x + w * fx, y + h * fy
        d.line([cx - 26 * s, cy, cx + 26 * s, cy], fill=(18, 17, 16), width=3)
        d.polygon([(cx + 26 * s, cy), (cx + 14 * s, cy - 5 * s), (cx + 14 * s, cy + 5 * s)],
                  fill=(18, 17, 16))
        d.line([cx - 6 * s, cy, cx - 16 * s, cy - 9 * s], fill=(18, 17, 16), width=2)


def sc_storm(d, x, y, w, h):
    _sky(d, x, y, w, h, (44, 48, 60), (88, 96, 108))
    for cx, cy, r in [(0.3, 0.42, 0.16), (0.68, 0.5, 0.2)]:
        for k in range(3):
            d.arc([x + w * (cx - r - k * 0.03), y + h * (cy - r - k * 0.03),
                   x + w * (cx + r + k * 0.03), y + h * (cy + r + k * 0.03)],
                  start=20 + k * 40, end=240 + k * 40, fill=(232, 234, 236), width=2)
    d.polygon([(x + w * 0.14, y + h * 0.14), (x + w * 0.2, y + h * 0.14),
               (x + w * 0.16, y + h * 0.3), (x + w * 0.22, y + h * 0.3),
               (x + w * 0.13, y + h * 0.46), (x + w * 0.11, y + h * 0.3),
               (x + w * 0.15, y + h * 0.3)], fill=(250, 204, 92))


def sc_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 16, 15))
    cw2, ch2 = w * 0.42, h * 0.62
    cx, cy = x + (w - cw2) / 2, y + (h - ch2) / 2
    d.rectangle([cx, cy, cx + cw2, cy + ch2], fill=(40, 34, 30), outline=FIRE, width=2)
    for i in range(4):
        px = cx + 8 + i * (cw2 - 16) / 3
        d.line([px, cy - 5, px, cy], fill=FIRE, width=2)
        d.line([px, cy + ch2, px, cy + ch2 + 5], fill=FIRE, width=2)
    for i in range(3):
        py = cy + 8 + i * (ch2 - 16) / 2
        d.line([cx - 5, py, cx, py], fill=FIRE, width=2)
        d.line([cx + cw2, py, cx + cw2 + 5, py], fill=FIRE, width=2)
    ccx, ccy = cx + cw2 / 2, cy + ch2 / 2
    d.ellipse([ccx - 13, ccy - 13, ccx + 13, ccy + 13], outline=(250, 220, 160), width=2)
    d.line([ccx - 18, ccy, ccx + 18, ccy], fill=(250, 220, 160), width=2)
    d.line([ccx, ccy - 18, ccx, ccy + 18], fill=(250, 220, 160), width=2)


def sc_stadium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 24, 30))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(36, 96, 54))
    d.line([x, y + h * 0.55, x + w, y + h * 0.55], fill=(240, 240, 234), width=1)
    d.ellipse([x + w * 0.4, y + h * 0.62, x + w * 0.6, y + h * 0.92],
              outline=(240, 240, 234), width=1)
    T(d, (x + w * 0.5, y + h * 0.3), "5–1", F(24, True), (250, 248, 244), anchor="mm")


SCENES = {6: sc_crosses, 3: sc_derricks, 4: sc_gaza, 1: sc_awacs,
          2: sc_tankers, 36: sc_chart, 13: sc_coral, 5: sc_arc,
          33: sc_report, 10: sc_jets, 37: sc_storm, 34: sc_chip,
          11: sc_stadium}


def draw_map(d, x, y, w, h, pins):
    rows = MAP_ROWS
    cw = w / 46
    ch = h / 34
    land = (150, 138, 124)
    for ri, row in enumerate(rows):
        for ci, chrc in enumerate(row):
            if chrc == "#":
                for yy in range(3):
                    for xx in range(4):
                        px = x + (ci * 4 + xx) * cw
                        py = y + (ri * 3 + yy) * ch
                        if (xx * 7 + yy * 13 + ci + ri) % 3:
                            d.point((px, py), fill=land)
    for num, fx, fy in pins:
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=FIRE, outline=BLACK, width=1)
        T(d, (px, py - 1), str(num), F(8, True), (255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- cards
def draw_card(d, num, x, y, w, h, lead=False):
    region, head, deck, source, tag, chip = CARDS[num]
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BLACK, width=1)
    d.rectangle([x, y, x + w, y + 15], fill=BLACK if lead else BLACK_L)
    T(d, (x + 5, y + 3), region, F(8, True), (250, 248, 244))
    T(d, (x + w - 5, y + 3), tag, F(8, True), FIRE, anchor="ra")
    frac = 0.40 if h > 130 else 0.34
    scene_h = int(h * (frac if lead else 0.34))
    SCENES[num](d, x + 3, y + 18, w - 6, scene_h)
    ty = y + 22 + scene_h
    hf = F(19, disp=True) if lead else F(12, True)
    for line in wrap(d, head, hf, w - 12):
        if ty + 14 > y + h - 18:
            break
        T(d, (x + 6, ty), line, hf, INK)
        ty += (23 if lead else 15)
    df = F(11) if lead else F(9)
    for line in wrap(d, deck, df, w - 12):
        if ty + (13 if lead else 11) > y + h - 18:
            break
        T(d, (x + 6, ty), line, df, (82, 72, 64))
        ty += (14 if lead else 11)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=PAPER_D, outline=BLACK)
    T(d, (x + 5, y + h - 12), chip, F(8, True), FIRE_D)
    T(d, (x + w - 5, y + h - 12), source, F(7), MUTE, anchor="ra")


def number_strip(d, y):
    cw = (W - 2 * MX) / 8
    d.line([MX, y, W - MX, y], fill=BLACK, width=2)
    for i, (big, lab, ref) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            d.line([x, y + 4, x, y + 34], fill=(198, 188, 172), width=1)
        T(d, (x + cw / 2, y + 3), big, F(19, True), BLACK, anchor="ma")
        T(d, (x + cw / 2, y + 24), lab, F(7, True), MUTE, anchor="ma")
        T(d, (x + cw / 2, y + 33), ref, F(8, True), FIRE_D, anchor="ma")
    d.line([MX, y + 44, W - MX, y + 44], fill=BLACK, width=1)
    return y + 50


def region_strip(d, y):
    x = MX
    T(d, (x, y + 2), "REGIONS:", F(10, True), INK)
    x += d.textlength("REGIONS: ", font=F(10, True))
    fills = [(14, 13, 12), (188, 70, 16), (40, 36, 33), (96, 130, 96),
             (150, 96, 60), (110, 70, 130), (52, 130, 140), (160, 120, 60),
             (90, 140, 110)]
    for i, (name, n) in enumerate(REGIONS):
        label = f"{name} {n}"
        tw = d.textlength(label, font=F(9, True)) + 12
        d.rectangle([x, y, x + tw, y + 16], fill=fills[i % len(fills)])
        T(d, (x + 6, y + 3), label, F(9, True), (250, 248, 244))
        x += tw + 5
    return y + 22


def date_strip(d, y):
    d.rectangle([MX, y, W - MX, y + 22], fill=BLACK)
    cw = (W - 2 * MX) / 5
    for i, (when, what) in enumerate(DATESTRIP):
        x = MX + i * cw
        T(d, (x + 8, y + 5), when, F(10, True), FIRE)
        T(d, (x + 8 + d.textlength(when + " ", font=F(10, True)), y + 5), what,
          F(10), (250, 248, 244))
    return y + 28


def briefs_block(d, y, h):
    d.rectangle([MX, y, W - MX, y + 17], fill=BLACK)
    T(d, (MX + 6, y + 3), "ALSO BEFORE MIDNIGHT — IN BRIEF, NUMBERED", F(10, True),
      (250, 248, 244))
    cols = 4
    cw = (W - 2 * MX) / cols
    rows = (len(BRIEFS) + cols - 1) // cols
    rh = (h - 22) / rows
    for idx, (num, text) in enumerate(BRIEFS):
        cx = MX + (idx // rows) * cw
        cy = y + 21 + (idx % rows) * rh
        T(d, (cx + 2, cy), f"{num}. {text}", F(9), INK)
    return y + h


def bottom_row(d, y, h, order):
    widths = {"map": 0.44, "time": 0.28, "date": 0.28}
    x = MX
    total = W - 2 * MX
    for i, kind in enumerate(order):
        w = total * widths[kind] - (6 if i < 2 else 0)
        if kind == "map":
            d.rectangle([x, y, x + w, y + h], fill=BLACK)
            T(d, (x + 5, y + 4), "THE NIGHT MAP — PINS = CARD NUMBERS",
              F(9, True), (250, 248, 244))
            draw_map(d, x + 4, y + 20, w - 8, h - 40, PINS)
            T(d, (x + 5, y + h - 13),
              "EUROPE 8 · MIDDLE EAST 6 · WORLD 6 · AFRICA 5 · AMERICAS 4 · ASIA 2",
              F(7, True), (196, 182, 168))
            T(d, (x + 5, y + h - 5), "SOUTH ASIA 2 · ASIA-PACIFIC 2 · OCEANIA 2",
              F(7, True), (196, 182, 168))
        elif kind == "time":
            d.rectangle([x, y, x + w, y + 15], fill=BLACK)
            T(d, (x + 5, y + 3), "THE NIGHT WATCH", F(9, True), (250, 248, 244))
            ty = y + 21
            for when, what in TIMELINE:
                T(d, (x + 5, ty), when, F(8, True), FIRE_D)
                for line in wrap(d, what, F(9), w - 66):
                    T(d, (x + 64, ty), line, F(9), INK)
                    ty += 11
                ty += 3
        else:
            d.rectangle([x, y, x + w, y + 15], fill=FIRE_D)
            T(d, (x + 5, y + 3), "YESTERDAY'S NEWS — NOT TONIGHT'S", F(9, True),
              (250, 248, 244))
            ty = y + 21
            for item in DATECHECK:
                T(d, (x + 5, ty), "×", F(10, True), FIRE_D)
                for line in wrap(d, item, F(9), w - 22):
                    T(d, (x + 17, ty), line, F(9), INK)
                    ty += 11
                ty += 3
        x += w + 6
    return y + h


def footer(d):
    T(d, (MX, 1002),
      "Sources: wire reports · RFE/RL · Al Jazeera · DW · Starlit Daily · Forbes via wires. Claims labelled as claims.",
      F(8), MUTE)
    T(d, (W - MX, 1002), "Original drawings.", F(8), MUTE, anchor="ra")
    T(d, (W / 2, 1013), "THE MIDNIGHT GAZETTE · NIGHT EDITION · TUESDAY 25 NOVEMBER 2026",
      F(8, True), INK, anchor="ma")


def strips(d, y):
    y = number_strip(d, y)
    y = region_strip(d, y + 2)
    y = date_strip(d, y + 4)
    return y + 6


def grid_block(d, y):
    cw = (W - 2 * MX - 4 * 6) / 5
    for r in range(2):
        for c in range(5):
            draw_card(d, GRID[r * 5 + c], MX + c * (cw + 6), y, cw, 138)
        y += 144
    return y


# ---------------------------------------------------------------- layouts
def layout_c():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    T(d, (MX, 8), "THE NIGHT EDITION · 37 STORIES · 9 REGIONS · SET AFTER DARK",
      F(11, True), INK)
    T(d, (W - MX, 8), "READ BY LAMPLIGHT", F(11, True), FIRE_D, anchor="ra")
    d.line([MX, 28, W - MX, 28], fill=FIRE, width=3)
    T(d, (MX, 34), "THE MIDNIGHT GAZETTE", F(48, disp=True), BLACK)
    T(d, (W - MX, 52), "TUESDAY", F(27, disp=True), FIRE_D, anchor="ra")
    T(d, (W - MX, 82), "25 NOVEMBER 2026", F(19, True), BLACK, anchor="ra")
    d.line([MX, 122, W - MX, 122], fill=BLACK, width=2)
    y = strips(d, 128)
    lw = (W - 2 * MX) * 0.585
    draw_card(d, 6, MX, y, lw, 252, lead=True)
    rx = MX + lw + 8
    rw = W - MX - rx
    draw_card(d, 3, rx, y, rw, 122, lead=True)
    draw_card(d, 4, rx, y + 130, rw, 122, lead=True)
    y += 258
    y = grid_block(d, y + 4)
    y = briefs_block(d, y + 2, 84)
    bottom_row(d, y + 6, 990 - (y + 6), ["map", "time", "date"])
    footer(d)
    return img


def layout_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 22], fill=FIRE)
    T(d, (MX, 5), "37 STORIES · 9 REGIONS · EVERY STORY DATED TUESDAY · NIGHT EDITION",
      F(11, True), BLACK)
    T(d, (W - MX, 5), "READ BY LAMPLIGHT", F(11, True), BLACK, anchor="ra")
    d.rectangle([MX, 28, W - MX, 150], fill=BLACK)
    T(d, (MX + 12, 36), "SET AFTER DARK", F(9, True), (196, 182, 168))
    T(d, (W - MX - 12, 36), "No. 25-11", F(9, True), (196, 182, 168), anchor="ra")
    T(d, (W / 2, 48), "THE MIDNIGHT GAZETTE", F(48, disp=True), (250, 248, 244), anchor="ma")
    T(d, (W / 2, 108), "TUESDAY 25 NOVEMBER 2026", F(27, disp=True), FIRE, anchor="ma")
    y = strips(d, 158)
    lw = (W - 2 * MX - 2 * 8) / 3
    for i, num in enumerate(LEADS):
        draw_card(d, num, MX + i * (lw + 8), y, lw, 180, lead=True)
    y += 186
    y = grid_block(d, y)
    y = briefs_block(d, y + 2, 84)
    bottom_row(d, y + 6, 990 - (y + 6), ["date", "map", "time"])
    footer(d)
    return img


def render(variant):
    return layout_c() if variant == "C" else layout_b()


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "C"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, f"entry_{variant.lower()}.png")
    render(variant).save(out, optimize=True)
    print("saved", out)
