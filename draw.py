#!/usr/bin/env python3
"""news-22 b17 regions-seven: draw the 22 Nov 2026 front page (36 stories)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 244, 230)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARK = (30, 45, 70)
CREAM = (252, 248, 238)

FDIR = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF_R = lambda s: F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def txt(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def chip(x, y, label, color):
    f = SANSB(9)
    w_ = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], 3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w_


CHIP_C = {"CONFIRMED": (34, 139, 34), "REPORTED": (40, 90, 170),
          "CLAIM": (200, 130, 20), "OFFICIAL": (90, 90, 90),
          "FORECAST": (120, 80, 160), "ONGOING": (180, 60, 60)}

# ---------- masthead ----------
d.rectangle([0, 0, W, 6], fill=RED)
txt(14, 12, "THE WORLD IN ONE DAY", SANSB(13), RED)
txt(1010, 12, "36 STORIES  ·  7 REGIONS", SANSB(13), INK, "ra")
txt(14, 28, "Sunday 22 November 2026", SERIF(40), INK)
txt(14, 74, "COP31 fails  ·  186 drones  ·  Bahrain radar claim — the day the world said no",
    SANSB(13), RED)
d.line([14, 94, 1010, 94], fill=INK, width=2)

# ---------- number strip ----------
nums = [("186", "drones fired"), ("161", "shot down"), ("720/9", "India declare"),
        ("98.79%", "HK turnout"), ("$120bn", "adaptation dropped"), ("35%", "2035 power kept"),
        ("44h", "COP31 overtime"), ("258", "Dems seats")]
cw = (1010 - 14) / 8
for i, (n, lab) in enumerate(nums):
    x = 14 + i * cw
    txt(x + cw / 2, 100, n, SANSB(25), RED, "ma")
    txt(x + cw / 2, 128, lab, SANS(10), INK, "ma")
    if i:
        d.line([x, 102, x, 140], fill=(200, 190, 170), width=1)
d.line([14, 146, 1010, 146], fill=INK, width=1)

# ---------- region bar ----------
regs = [("EUROPE 8", (30, 90, 170)), ("MIDDLE EAST 7", (200, 90, 40)),
        ("ASIA-PACIFIC 7", (20, 130, 70)), ("AMERICAS 5", (130, 60, 160)),
        ("AFRICA 3", (170, 130, 40)), ("OCEANIA 3", (20, 140, 150)),
        ("WORLD 3", (90, 90, 90))]
x = 14
tot = sum(len(r[0]) for r in regs)
for name, col in regs:
    w_ = (1010 - 14) * len(name) / tot
    d.rectangle([x, 150, x + w_, 168], fill=col)
    txt(x + w_ / 2, 153, name, SANSB(11), (255, 255, 255), "ma")
    x += w_

# ---------- UTC strip ----------
d.rectangle([14, 172, 1010, 190], fill=DARK)
txt(20, 175, "THE DAY IN UTC", SANSB(11), (255, 210, 90))
txt(140, 175, "01:00 HK polls open  ·  03:00 COP31 objections close  ·  06:00 adoption vote  ·  "
               "~16:00 COP31 fails  ·  18:13 Dems 258  ·  20:43 Alcaraz wins",
    SANS(11), (255, 255, 255))

# ---------- hero scenes ----------
def scene_cop31(x0, y0, w_, h_):
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(245, 180, 90))
    d.rectangle([x0, y0 + h_ - 34, x0 + w_, y0 + h_], fill=(60, 50, 45))
    for i in range(6):
        d.rectangle([x0 + 14 + i * 52, y0 + h_ - 30, x0 + 44 + i * 52, y0 + h_ - 8],
                    fill=(255, 220, 120))
    for i, c in enumerate([(200, 40, 40), (40, 90, 200), (30, 140, 60), (240, 200, 40),
                           (150, 60, 180), (255, 140, 40)]):
        d.polygon([(x0 + 20 + i * 48, y0 + 8), (x0 + 20 + i * 48, y0 + 26),
                   (x0 + 38 + i * 48, y0 + 17)], fill=c)
    d.ellipse([x0 + w_ - 52, y0 + 8, x0 + w_ - 12, y0 + 48], fill=(255, 230, 150))
    d.rectangle([x0 + w_ - 118, y0 + 10, x0 + w_ - 8, y0 + 34], fill=RED)
    txt(x0 + w_ - 63, y0 + 14, "NO DEAL", SANSB(14), (255, 255, 255), "ma")


def scene_drones(x0, y0, w_, h_):
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(18, 24, 48))
    for bx in range(0, 7):
        bw, bh = 34, 26 + (bx % 3) * 12
        d.rectangle([x0 + 8 + bx * 44, y0 + h_ - bh, x0 + 36 + bx * 44, y0 + h_], fill=(40, 44, 70))
        for wy in range(2):
            for wx in range(2):
                d.rectangle([x0 + 13 + bx * 44 + wx * 14, y0 + h_ - bh + 5 + wy * 10,
                             x0 + 19 + bx * 44 + wx * 14, y0 + h_ - bh + 11 + wy * 10],
                            fill=(255, 210, 90))
    d.ellipse([x0 + w_ - 90, y0 + h_ - 34, x0 + w_ - 40, y0 + h_ + 16], fill=(255, 140, 40))
    d.ellipse([x0 + w_ - 78, y0 + h_ - 22, x0 + w_ - 52, y0 + h_ + 4], fill=(255, 200, 80))
    for i, (dx, dy) in enumerate([(40, 14), (90, 26), (150, 10), (210, 30), (260, 16)]):
        d.line([x0 + dx - 14, y0 + dy + 6, x0 + dx + 14, y0 + dy - 6], fill=(255, 90, 90), width=2)
        d.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3], fill=(255, 255, 255))


def scene_radar(x0, y0, w_, h_):
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=(16, 22, 44))
    d.ellipse([x0 + w_ - 60, y0 + 6, x0 + w_ - 16, y0 + 50], fill=(230, 230, 220))
    d.pieslice([x0 + 30, y0 + h_ - 66, x0 + 150, y0 + h_ + 10], 180, 360, fill=(150, 150, 150))
    d.line([x0 + 90, y0 + h_ - 60, x0 + 90, y0 + 12], fill=(200, 200, 200), width=4)
    d.line([x0 + 90, y0 + 12, x0 + 170, y0 + 40], fill=(255, 210, 90), width=3)
    d.ellipse([x0 + 166, y0 + 36, x0 + 174, y0 + 44], fill=(255, 210, 90))
    d.ellipse([x0 + w_ - 70, y0 + h_ - 26, x0 + w_ - 30, y0 + h_ + 14], fill=(255, 140, 40))
    for i in range(5):
        d.ellipse([x0 + 12 + i * 16, y0 + h_ - 10, x0 + 18 + i * 16, y0 + h_ - 4],
                  fill=(255, 210, 90))


heroes = [
    ("ANTALYA · POLITICS", "COP31 collapses — NO DEAL", "CONFIRMED",
     "EU + ~130 parties reject a text with no fossil-fuel language; $120bn target dropped; "
     "35% power kept.",
     "Source: AP · Reuters · Guardian", scene_cop31),
    ("KYIV · WAR", "186 drones fired, 161 shot down", "REPORTED",
     "186 drones fired overnight; 161 shot down or jammed. Dymer block falls: 1 dead, "
     "14 unaccounted for.",
     "Source: Ukrainian Air Force · AP", scene_drones),
    ("BAHRAIN · WAR", "Iran claims 2 Patriot radars hit", "CLAIM",
     "Tehran says Patriot radars at al-Riffa and Awali were hit. Bahrain denies it; "
     "Sitra burns, 2 hurt, no deaths.",
     "Source: IRGC vs Bahrain MoI · Reuters", scene_radar),
]
hy, hh, hw, gap = 196, 148, 322, 8
for i, (kick, title, ch, body, src, scene) in enumerate(heroes):
    x0 = 14 + i * (hw + gap)
    d.rectangle([x0, hy, x0 + hw, hy + hh], outline=(150, 140, 125), width=1, fill=CREAM)
    scene(x0 + 1, hy + 1, hw - 2, 62)
    txt(x0 + 8, hy + 68, kick, SANSB(10), RED)
    chip(x0 + hw - 82, hy + 66, ch, CHIP_C[ch])
    for j, ln in enumerate(wrap(title, SANSB(16), hw - 16)):
        txt(x0 + 8, hy + 84 + j * 19, ln, SANSB(16), INK)
    by = hy + 84 + len(wrap(title, SANSB(16), hw - 16)) * 19 + 2
    for j, ln in enumerate(wrap(body, SANS(10), hw - 16)[:2]):
        txt(x0 + 8, by + j * 12, ln, SANS(10), INK)
    txt(x0 + 8, hy + hh - 13, src, SANS(9), (90, 90, 90))

# ---------- small cards ----------
cards = [
    ("HONG KONG · POLITICS", "#4", "Hong Kong votes: 98.79% turnout",
     "856 candidates, 723 seats; 5,640 of 5,709 voters.", "CONFIRMED", "SCMP · Reuters", (30, 90, 170)),
    ("LAS VEGAS · SPORT", "#5", "Verstappen wins by 0.639s",
     "Beats Norris; Piastri 3rd; 75th win.", "CONFIRMED", "F1 · Reuters", (20, 130, 70)),
    ("TURIN · SPORT", "#6", "Alcaraz takes ATP Finals",
     "Beats Zverev 6–2, 7–6(7); first title.", "CONFIRMED", "ATP · BBC", (130, 60, 160)),
    ("NEW ZEALAND · SPORT", "#7", "India declare 720/9",
     "Highest Test total in NZ; Rahul 136, Pant 128.", "CONFIRMED", "ESPNcricinfo", (20, 140, 150)),
    ("CIKANDE · SOCIETY", "#8", "Candy-factory fire: 3 dead, 36 missing",
     "Fire began Sat. night; 15 survived.", "REPORTED", "Detiknews", (200, 90, 40)),
    ("TEHRAN · SOCIETY", "#9", "Iran starts power rationing",
     "Blackouts ~2h a day; gas output hit.", "REPORTED", "Reuters", (170, 130, 40)),
    ("DR CONGO · HEALTH", "#10", "Ebola cases reach 11,613",
     "WHO count; fighting traps medics.", "OFFICIAL", "WHO · Reuters", (90, 90, 90)),
    ("SEOUL · SOCIETY", "#11", "Minister quits in AI-cheat scandal",
     "111 device cases; Choi resigns.", "CONFIRMED", "Yonhap", (130, 60, 160)),
    ("CAPE CANAVERAL · SCIENCE", "#12", "Falcon 9 launches NROL-136",
     "Record 32h turnaround; booster lands.", "OFFICIAL", "SpaceX", (20, 130, 70)),
    ("LIVERPOOL · SPORT", "#13", "Liverpool rout Man Utd 4–0",
     "Pochettino debut ends in a rout.", "CONFIRMED", "BBC Sport", (200, 40, 40)),
]
cy, chh, cw2 = 352, 84, 195
for idx, (kick, num, title, body, ch, src, col) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = 14 + c * (cw2 + 6)
    y0 = cy + r * (chh + 6)
    d.rectangle([x0, y0, x0 + cw2, y0 + chh], outline=(150, 140, 125), width=1, fill=CREAM)
    d.rectangle([x0, y0, x0 + cw2, y0 + 14], fill=col)
    txt(x0 + 6, y0 + 1, kick, SANSB(8), (255, 255, 255))
    txt(x0 + cw2 - 6, y0 + 1, num, SANSB(9), (255, 255, 255), "ra")
    tl = wrap(title, SANSB(11), cw2 - 12)
    for j, ln in enumerate(tl[:2]):
        txt(x0 + 6, y0 + 18 + j * 13, ln, SANSB(11), INK)
    ty = y0 + 18 + len(tl[:2]) * 13
    for j, ln in enumerate(wrap(body, SANS(9), cw2 - 12)[:2]):
        txt(x0 + 6, ty + j * 11, ln, SANS(9), INK)
    chip(x0 + 6, y0 + chh - 17, ch, CHIP_C[ch])
    txt(x0 + cw2 - 6, y0 + chh - 15, src, SANS(8), (90, 90, 90), "ra")

# ---------- map + ALSO ----------
my0 = 536
txt(14, my0, "THE WORLD — WHERE IT HAPPENED", SANSB(12), RED)
txt(496, my0, "PIN = STORY NUMBER", SANS(9), (90, 90, 90), "ra")
txt(516, my0, "ALSO ON SUNDAY — 23 MORE STORIES", SANSB(12), RED)
d.line([14, my0 + 16, 1010, my0 + 16], fill=INK, width=1)

MX0, MY0, MX1, MY1 = 14, 556, 500, 800
d.rectangle([MX0, MY0, MX1, MY1], fill=(190, 215, 235))
for gx in range(MX0, MX1 + 1, 40):
    d.line([gx, MY0, gx, MY1], fill=(210, 228, 240), width=1)
for gy in range(MY0, MY1 + 1, 40):
    d.line([MX0, gy, MX1, gy], fill=(210, 228, 240), width=1)


def proj(lon, lat):
    return (MX0 + (lon + 170) / 360 * (MX1 - MX0),
            MY0 + (75 - lat) / 130 * (MY1 - MY0))


LAND = (232, 214, 170)
continents = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-85, 66), (-75, 62), (-55, 52),
     (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-158, 58), (-168, 66)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-68, 76), (-58, 64)],
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-80, -5), (-80, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (45, 66), (40, 60), (35, 55),
     (30, 50), (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -18), (30, -26), (20, -35), (15, -30),
     (12, -18), (9, -1), (9, 4), (-8, 5), (-17, 15)],
    [(30, 70), (45, 68), (60, 69), (75, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (142, 50), (140, 40),
     (135, 35), (130, 32), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (85, 20), (80, 10), (77, 8), (72, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (43, 35), (40, 40), (35, 45), (30, 50), (30, 60), (30, 70)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (135, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (150, -25), (146, -19), (142, -11), (137, -12),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
    [(95, 5), (100, 6), (104, 2), (100, -3), (95, -2)],
    [(110, -6), (114, -8), (114, -10), (108, -8)],
    [(120, -2), (125, -4), (128, -2), (122, 1)],
]
for poly in continents:
    d.polygon([proj(lo, la) for lo, la in poly], fill=LAND, outline=(180, 165, 130))

pins = [(1, 31, 49), (2, 30, 37), (3, 50.5, 26), (4, 114, 22), (5, -115, 36),
        (6, 7.7, 45), (7, 174, -41), (8, 106, -6), (9, 51, 35.7), (10, 23, -3),
        (11, 127, 37.5), (12, -80.5, 28.5), (13, -3, 53.4), (14, 25, 59), (15, 10, 56),
        (16, 4.5, 50.5), (17, 31, 44), (18, 20, 32), (19, 34.3, 31.3), (20, 35.3, 32.2),
        (21, 35.0, 31.7), (22, 77, 28.6), (23, 94, 24.5), (24, 112, -8),
        (25, 149, -35), (26, -77, 39), (27, -47.9, -15.8), (28, -98.5, 29.4),
        (29, -72, 41), (30, 32.5, 15.6), (31, 6, 4.9), (32, 145, -37.8),
        (33, 151, -33.9), (34, 133, -25), (35, -30, 0), (36, -122, 37)]
for n, lo, la in pins:
    px, py = proj(lo, la)
    col = (200, 130, 20) if n in (3, 18) else RED
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
    f = SANSB(7)
    tw = d.textlength(str(n), font=f)
    d.text((px - tw / 2, py - 4), str(n), font=f, fill=(255, 255, 255))
txt(16, MY1 - 12, "N ↑", SANSB(9), INK)

# ALSO grouped by region, two columns
also = [
    ("EUROPE", (30, 90, 170), [(14, "Estonia closes 5 Russia crossings"),
                                (15, "Denmark expels Russian attaché"),
                                (16, "Belgium controllers join Monday strike"),
                                (17, "Sparta II still burning, towed home")]),
    ("MIDDLE EAST", (200, 90, 40), [(18, "Merkury corvette hit off Benghazi"),
                                     (19, "Gaza: 4 killed; aid-van strike kills 3"),
                                     (20, "Eisenkot invites Likud to coalition talks"),
                                     (21, "Settlers burn 12 cars in West Bank")]),
    ("ASIA-PACIFIC", (20, 130, 70), [(22, "Nepal PM lands in Delhi, first trip abroad"),
                                      (23, "Manipur liquor toll rises; ~600 treated"),
                                      (24, "EU–Indonesia deal signed (date split)"),
                                      (25, "Marles rejects US AUKUS sub report")]),
    ("AMERICAS", (130, 60, 160), [(26, "Democrats take the House: 258 seats"),
                                   (27, "Bolsonaro in intensive care"),
                                   (28, "Wembanyama scores 50"),
                                   (29, "FBI probes NCIC crime-database hack")]),
    ("AFRICA", (170, 130, 40), [(30, "Drones kill 4 near Khartoum"),
                                 (31, "Mourners' boat capsizes: 24 dead")]),
    ("OCEANIA", (20, 140, 150), [(32, "Melbourne: 70 yrs since 1956 Games"),
                                  (33, "Fred Nile dies, 92"),
                                  (34, "Cummins stays Test captain")]),
    ("WORLD", (90, 90, 90), [(35, "Bitcoin back above $60,000"),
                              (36, "Nvidia faces SEC accounting probe")]),
]
ay = my0 + 22
col_w = 244
for ci, (gname, gcol, items) in enumerate(also):
    cx = 516 + (ci % 2) * (col_w + 6)
    if ci % 2 == 0 and ci > 0:
        ay = ay  # left column continues
    # compute y per column independently
    if ci == 0:
        ly, ry = ay, ay
    if ci % 2 == 0:
        y = ly
    else:
        y = ry
    txt(cx, y, gname, SANSB(10), gcol)
    y += 13
    for n, s in items:
        for j, ln in enumerate(wrap(f"{n}  {s}", SANS(10), col_w - 4)):
            txt(cx, y + j * 12, ln, SANS(10), INK)
        y += 12 * len(wrap(f"{n}  {s}", SANS(10), col_w - 4)) + 1
    y += 4
    if ci % 2 == 0:
        ly = y
    else:
        ry = y

# ---------- DATE CHECK ----------
dy0 = 812
d.rectangle([14, dy0, 1010, 952], outline=RED, width=2, fill=(255, 240, 240))
txt(22, dy0 + 6, "DATE CHECK", SANSB(12), RED)
txt(22, dy0 + 22, "Every story above happened or was first reported on Sunday 22 November 2026.",
    SANSB(11), INK)
txt(700, dy0 + 22, "WIRES READ UP TO 23:00 UTC", SANSB(10), RED, "ra")
yy = dy0 + 42
for ln in wrap("LEFT OUT (not 22 Nov):  400-drone barrage (19–20 Nov)  ·  El Chapo Isidro captured "
               "(20 Nov)  ·  BepiColombo Mercury orbit (21 Nov, burn 18:24 GMT)  ·  Kryvyi Rih "
               "(20 Nov night)  ·  Peru quake (20 Nov)  ·  Hormuz tankers hit (Sat 21 Nov 05:00 GMT, "
               "reported Sun 17:13 UTC)", SANS(10), 972):
    txt(22, yy, ln, SANS(10), INK)
    yy += 13
yy += 4
for ln in wrap("NOT YET:  Dymer final toll  ·  4 House races uncalled  ·  EU–Indonesia deal date split "
               "(Sat 21 vs Sun 22)  ·  Nigeria boat date (Fri 20 vs Sun 22)  ·  FBI hack date split "
               "(Fri 20 / Sat 21)  ·  Sparta II hit Sat 21, still burning Sun  ·  COP32 venue undecided",
               SANS(10), 972):
    txt(22, yy, ln, SANS(10), INK)
    yy += 13

# ---------- footer ----------
txt(14, 960, "SOURCES: AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · Yonhap · Anadolu · "
              "Detiknews · WHO · SpaceX", SANS(9), INK)
txt(14, 974, "CONFIRMED = 2+ outlets  ·  REPORTED = carried by the wires today  ·  CLAIM = one side, unverified  ·  "
              "OFFICIAL = recorded result  ·  FORECAST = not yet decided", SANS(9), INK)
txt(14, 988, "Red pin = reported  ·  Amber pin = claim (unverified)", SANS(9), INK)
txt(1010, 988, "Scenes are drawn illustrations, not photographs.", SANS(9), (90, 90, 90), "ra")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
