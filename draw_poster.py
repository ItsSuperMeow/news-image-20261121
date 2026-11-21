#!/usr/bin/env python3
"""Draw the 1024x1024 world-news poster for Saturday 21 November 2026.

Entry for make.fun competition news-image-20261121.
Run: python3 draw_poster.py  ->  writes entry.png next to this script.
All art is drawn with code (Pillow shapes and text); no photos, no copied images.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (20, 33, 61)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (24, 24, 28)
MUTED = (82, 82, 90)
RED = (178, 34, 34)
GOLD = (198, 142, 30)
GOLD_L = (232, 182, 76)
BLUE = (38, 84, 160)
LINE = (205, 200, 188)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def burst(d, cx, cy, r_out, r_in, spikes, color):
    """Starburst / explosion shape centred at (cx, cy)."""
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def jet(d, cx, cy, s, color):
    """Small delta-wing jet silhouette pointing right."""
    d.polygon([(cx - s, cy + s * 0.35), (cx + s, cy), (cx - s, cy - s * 0.35),
               (cx - s * 0.55, cy)], fill=color)


def flag_pl(d, x, y, w, h):
    """Small Polish flag (white over red) on a pole; pole ends at y + h + 26."""
    d.line([(x, y), (x, y + h + 26)], fill=INK, width=3)
    d.rectangle([x, y, x + w, y + h // 2], fill=(255, 255, 255))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(220, 20, 60))


def lead_scene(d, x0, y0, x1, y1):
    """Dusk sky over south-eastern Poland: missile trails, blasts, jets, flag."""
    top = (44, 62, 108)
    bot = (226, 138, 76)
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, (y1 - y0))
        col = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(x0, yy), (x1, yy)], fill=col)
    # low sun
    d.ellipse([x1 - 96, y0 + 52, x1 - 36, y0 + 112], fill=(255, 214, 140))
    # ground silhouette
    gy = y1 - 46
    d.rectangle([x0, gy, x1, y1], fill=(26, 28, 36))
    # pine silhouettes on the horizon
    for px in (x0 + 84, x0 + 436):
        d.polygon([(px, gy), (px + 15, gy - 28), (px + 30, gy)], fill=(26, 28, 36))
    # missile trails streaking down from the upper sky
    d.line([(x0 + 60, y0 + 14), (x0 + 190, gy - 30)], fill=(255, 240, 200), width=4)
    d.line([(x0 + 268, y0 + 4), (x0 + 330, gy - 44)], fill=(255, 240, 200), width=4)
    # smoke puffs along the trails
    for (sx, sy, sr) in [(x0 + 120, y0 + 56, 10), (x0 + 150, y0 + 84, 13),
                         (x0 + 292, y0 + 38, 9), (x0 + 310, y0 + 64, 12)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(205, 205, 210))
    # explosion bursts where the missiles came down
    burst(d, x0 + 190, gy - 16, 46, 20, 9, (255, 120, 30))
    burst(d, x0 + 190, gy - 16, 28, 12, 9, (255, 210, 80))
    burst(d, x0 + 330, gy - 24, 38, 17, 9, (255, 120, 30))
    burst(d, x0 + 330, gy - 24, 22, 10, 9, (255, 210, 80))
    # NATO jets scrambled in the upper sky
    jet(d, x0 + 380, y0 + 40, 22, (20, 20, 26))
    jet(d, x0 + 420, y0 + 150, 17, (20, 20, 26))
    # Polish flag planted on the ground, left
    flag_pl(d, x0 + 26, gy - 46, 34, 20)


def icon_scales(d, cx, cy, s, color):
    """Scales of justice, centred at (cx, cy)."""
    d.line([(cx, cy - s), (cx, cy + s)], fill=color, width=5)
    d.line([(cx - s, cy - s * 0.55), (cx + s, cy - s * 0.55)], fill=color, width=5)
    d.line([(cx, cy + s), (cx - s * 0.55, cy + s)], fill=color, width=5)
    d.line([(cx, cy + s), (cx + s * 0.55, cy + s)], fill=color, width=5)
    for sx in (cx - s, cx + s):
        d.line([(sx, cy - s * 0.55), (sx - s * 0.32, cy - s * 0.05)],
               fill=color, width=3)
        d.line([(sx, cy - s * 0.55), (sx + s * 0.32, cy - s * 0.05)],
               fill=color, width=3)
        d.arc([sx - s * 0.32, cy - s * 0.18, sx + s * 0.32, cy + s * 0.14],
              0, 180, fill=color, width=4)
    d.ellipse([cx - 6, cy - s - 8, cx + 6, cy - s + 4], fill=color)


def icon_flags(d, cx, cy, s, color):
    """Three flag poles with blue, red and gold flags."""
    cols = [(38, 84, 160), (178, 34, 34), (198, 142, 30)]
    for i, c in enumerate(cols):
        px = cx - s + i * s
        d.line([(px, cy - s), (px, cy + s)], fill=color, width=4)
        d.polygon([(px, cy - s), (px + s * 0.85, cy - s * 0.62),
                   (px, cy - s * 0.24)], fill=c)


def icon_chart(d, cx, cy, s, color):
    """Falling market line with an arrowhead, on axes."""
    d.line([(cx - s, cy + s * 0.7), (cx + s, cy + s * 0.7)], fill=color, width=4)
    d.line([(cx - s, cy + s * 0.7), (cx - s, cy - s * 0.8)], fill=color, width=4)
    pts = [(cx - s + 4, cy - s * 0.55), (cx - s * 0.3, cy - s * 0.2),
           (cx + s * 0.2, cy + s * 0.1), (cx + s - 4, cy + s * 0.55)]
    d.line(pts, fill=(178, 34, 34), width=6, joint="curve")
    d.polygon([(cx + s - 4, cy + s * 0.55), (cx + s - 22, cy + s * 0.42),
               (cx + s - 14, cy + s * 0.72)], fill=(178, 34, 34))


def icon_building(d, cx, cy, s, color):
    """Government building: pediment, columns and steps."""
    d.polygon([(cx - s, cy - s * 0.35), (cx, cy - s * 0.85),
               (cx + s, cy - s * 0.35)], fill=color)
    d.rectangle([cx - s, cy - s * 0.3, cx + s, cy - s * 0.15], fill=color)
    for i in range(4):
        colx = cx - s * 0.72 + i * s * 0.48
        d.rectangle([colx, cy - s * 0.15, colx + s * 0.16, cy + s * 0.6],
                    fill=color)
    d.rectangle([cx - s, cy + s * 0.6, cx + s, cy + s * 0.75], fill=color)
    d.rectangle([cx - s * 1.1, cy + s * 0.75, cx + s * 1.1, cy + s * 0.9],
                fill=color)


def icon_eu_uk(d, cx, cy, s, color):
    """EU circle of gold stars with a small Union Jack overlapping."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=(38, 84, 160))
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx = cx + (s * 0.68) * math.cos(a)
        sy = cy + (s * 0.68) * math.sin(a)
        burst(d, sx, sy, 5, 2, 5, (255, 215, 0))
    fx, fy = cx + s * 0.3, cy + s * 0.5
    fw, fh = 38, 26
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(30, 60, 140),
                outline=(20, 20, 26), width=2)
    d.line([(fx + 2, fy + 2), (fx + fw - 2, fy + fh - 2)],
           fill=(255, 255, 255), width=5)
    d.line([(fx + fw - 2, fy + 2), (fx + 2, fy + fh - 2)],
           fill=(255, 255, 255), width=5)
    d.line([(fx + fw // 2, fy + 2), (fx + fw // 2, fy + fh - 2)],
           fill=(255, 255, 255), width=7)
    d.line([(fx + 2, fy + fh // 2), (fx + fw - 2, fy + fh // 2)],
           fill=(255, 255, 255), width=7)
    d.line([(fx + fw // 2, fy + 2), (fx + fw // 2, fy + fh - 2)],
           fill=(200, 30, 40), width=3)
    d.line([(fx + 2, fy + fh // 2), (fx + fw - 2, fy + fh // 2)],
           fill=(200, 30, 40), width=3)


def draw_card_a(d, box, title, body, icon, accent, title_size=26):
    """Narrow story card (row A): icon on top, centred title and body."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=LINE, width=2)
    d.rectangle([x0 + 10, y0, x1 - 10, y0 + 7], fill=accent)
    cx = (x0 + x1) // 2
    icon(d, cx, y0 + 52, 30, NAVY)
    f_t = F(SERIF_B, title_size)
    lines = wrap(d, title, f_t, (x1 - x0) - 28)
    ty = y0 + 92
    for ln in lines[:2]:
        tw = d.textlength(ln, font=f_t)
        d.text(((x0 + x1 - tw) / 2, ty), ln, font=f_t, fill=INK)
        ty += 31
    f_b = F(SANS, 19)
    blines = wrap(d, body, f_b, (x1 - x0) - 28)
    ty += 6
    for ln in blines[:3]:
        tw = d.textlength(ln, font=f_b)
        d.text(((x0 + x1 - tw) / 2, ty), ln, font=f_b, fill=MUTED)
        ty += 24


def draw_card_b(d, box, title, body, icon, accent):
    """Wide story card (row B): icon on the left, text on the right."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=LINE, width=2)
    d.rectangle([x0 + 10, y0, x1 - 10, y0 + 7], fill=accent)
    icon(d, x0 + 72, y0 + 122, 42, NAVY)
    tx = x0 + 136
    tw_max = x1 - tx - 18
    f_t = F(SERIF_B, 24)
    lines = wrap(d, title, f_t, tw_max)
    ty = y0 + 34
    for ln in lines[:2]:
        d.text((tx, ty), ln, font=f_t, fill=INK)
        ty += 30
    f_b = F(SANS, 20)
    blines = wrap(d, body, f_b, tw_max)
    ty += 8
    for ln in blines[:3]:
        d.text((tx, ty), ln, font=f_b, fill=MUTED)
        ty += 26


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header: navy band, title, date ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    f_title = F(SERIF_B, 72)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 18), title, font=f_title, fill=(255, 255, 255))
    f_date = F(SANS_B, 30)
    date = "SATURDAY, 21 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 100), date, font=f_date, fill=GOLD_L)
    d.rectangle([0, 148, W, 152], fill=GOLD)

    # ---- lead story panel ----
    d.rounded_rectangle([16, 164, 1008, 480], radius=10, fill=CARD,
                        outline=LINE, width=2)
    # TOP STORY tag
    tag = "TOP STORY"
    f_tag = F(SANS_B, 18)
    tag_w = d.textlength(tag, font=f_tag) + 24
    d.rounded_rectangle([32, 176, 32 + tag_w, 176 + 30], radius=6, fill=RED)
    d.text((32 + 12, 176 + 5), tag, font=f_tag, fill=(255, 255, 255))
    # scene on the left
    lead_scene(d, 32, 214, 540, 464)
    # headline + text on the right
    tx = 560
    tw_max = 992 - tx
    f_h = F(SERIF_B, 54)
    for i, ln in enumerate(["MISSILES HIT", "POLAND"]):
        d.text((tx, 214 + i * 60), ln, font=f_h, fill=INK)
    f_sub = F(SANS, 23)
    sub = ("Tusk calls it a \u2018deliberate provocation\u2019 \u2014 NATO jets "
           "scrambled as missiles land near allied drills.")
    ty = 214 + 2 * 60 + 12
    for ln in wrap(d, sub, f_sub, tw_max):
        d.text((tx, ty), ln, font=f_sub, fill=INK)
        ty += 29
    f_small = F(SANS, 19)
    small = "No injuries in Poland; 8 killed in Ukraine."
    ty += 10
    for ln in wrap(d, small, f_small, tw_max):
        d.text((tx, ty), ln, font=f_small, fill=MUTED)
        ty += 24

    # ---- row A: three story cards ----
    draw_card_a(d, (16, 496, 334, 740),
                "MYANMAR GUILTY OF GENOCIDE",
                "World Court\u2019s first genocide verdict against a state "
                "\u2014 9\u20136 on the 2017 crackdown.",
                icon_scales, BLUE)
    draw_card_a(d, (353, 496, 671, 740),
                "TRUMP, XI, PUTIN WRAP UP TALKS",
                "Trilateral talks in Shenzhen agree UN reform, oil supplies "
                "and nuclear-risk dialogue.",
                icon_flags, RED)
    draw_card_a(d, (690, 496, 1008, 740),
                "S&P 500 SLIDES INTO CORRECTION",
                "US stocks fall ~3.7% as AI shares sell off; Dow also in "
                "correction territory.",
                icon_chart, GOLD, title_size=24)

    # ---- row B: two wide story cards ----
    draw_card_b(d, (16, 756, 500, 1000),
                "HERZOG TAPS EISENKOT",
                "Israel\u2019s president picks the ex-army chief over "
                "Netanyahu to form the next government.",
                icon_building, NAVY)
    draw_card_b(d, (524, 756, 1008, 1000),
                "UK AND EU SIGN THREE DEALS",
                "Food trade, carbon markets and youth mobility agreed at a "
                "Brussels summit.",
                icon_eu_uk, BLUE)

    # ---- footer ----
    f_f = F(SANS, 15)
    foot = "Six stories from Saturday, 21 November 2026"
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, 1006), foot, font=f_f, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    build()
