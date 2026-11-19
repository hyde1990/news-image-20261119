#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: THE WORLD IN ONE DAY.

Pillow only, deterministic (fixed seed, no clock, no network, no date
reading). Running `python3 generate.py` writes entry.png beside it.
All facts are the verified stories for Thursday 19 November 2026.
"""
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(42)

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 21, 19)
RED = (166, 25, 46)
BLUE = (29, 78, 121)
GOLD = (180, 138, 44)
GREY = (90, 86, 78)
LIGHT_GREY = (232, 227, 216)
SKY_TOP = (46, 58, 96)
SKY_BOT = (214, 132, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
SERIF = lambda s: font("DejaVuSerif", s)
SANS_B = lambda s: font("DejaVuSans-Bold", s)
SANS = lambda s: font("DejaVuSans", s)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centred(draw, y, text, f, fill, x0=0, x1=W):
    draw.text(((x0 + x1 - text_w(draw, text, f)) / 2, y), text, font=f, fill=fill)


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def draw_lead_art(draw, x0, y0, x1, y1):
    # Dusk sky: horizontal bands, deterministic.
    bands = 24
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * t) for c in range(3))
        yy0 = y0 + int((y1 - y0) * i / bands)
        yy1 = y0 + int((y1 - y0) * (i + 1) / bands)
        draw.rectangle([x0, yy0, x1, yy1], fill=col)
    # Sun removed: the three flags fill the top of the panel.
    # Shenzhen skyline silhouettes.
    heights = [58, 96, 70, 128, 84, 112, 64, 142, 90, 76, 120, 66]
    bw = (x1 - x0) // len(heights)
    for i, hgt in enumerate(heights):
        bx0 = x0 + i * bw
        draw.rectangle([bx0 + 2, y1 - hgt, bx0 + bw - 2, y1], fill=(28, 30, 52))
        for wy in range(y1 - hgt + 10, y1 - 8, 16):
            draw.rectangle([bx0 + 6, wy, bx0 + 10, wy + 6], fill=(240, 196, 110))
    # Three flags on poles above the skyline.
    pole_y = y0 + 8
    flag_w, flag_h = 78, 48
    starts = [x0 + 12, x0 + 122, x0 + 232]
    # China: red field, yellow stars.
    fx, fy = starts[0], pole_y + 34
    draw.rectangle([fx, fy, fx + flag_w, fy + flag_h], fill=(222, 41, 16))
    draw.polygon([(fx + 14, fy + 8), (fx + 17, fy + 15), (fx + 24, fy + 15),
                  (fx + 18, fy + 19), (fx + 20, fy + 26), (fx + 14, fy + 22),
                  (fx + 8, fy + 26), (fx + 10, fy + 19), (fx + 4, fy + 15),
                  (fx + 11, fy + 15)], fill=(255, 222, 0))
    for sx, sy in [(38, 12), (48, 20), (38, 28)]:
        draw.ellipse([fx + sx, fy + sy, fx + sx + 7, fy + sy + 7], fill=(255, 222, 0))
    # Russia: white / blue / red horizontal bands.
    fx, fy = starts[1], pole_y + 34
    for j, col in enumerate([(245, 245, 245), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx, fy + j * 16, fx + flag_w, fy + (j + 1) * 16], fill=col)
    # USA: red/white stripes, blue canton.
    fx, fy = starts[2], pole_y + 34
    for j in range(6):
        col = (178, 34, 52) if j % 2 == 0 else (245, 245, 245)
        draw.rectangle([fx, fy + j * 8, fx + flag_w, fy + (j + 1) * 8], fill=col)
    draw.rectangle([fx, fy, fx + 32, fy + 24], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([fx + 4 + c * 7, fy + 4 + r * 7, fx + 7 + c * 7, fy + 7 + r * 7],
                         fill=(255, 255, 255))
    for fx in starts:
        draw.line([(fx + flag_w + 4, pole_y), (fx + flag_w + 4, pole_y + 34 + flag_h)],
                  fill=INK, width=3)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- icons
def icon_justice(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.line([(cx, cy - 22), (cx, cy + 20)], fill=BLUE, width=4)
    draw.line([(cx - 26, cy - 18), (cx + 26, cy - 18)], fill=BLUE, width=4)
    for sx in (-22, 22):
        draw.line([(cx + sx, cy - 18), (cx + sx, cy - 2)], fill=BLUE, width=3)
        draw.polygon([(cx + sx - 11, cy - 2), (cx + sx + 11, cy - 2),
                      (cx + sx, cy + 8)], fill=GOLD)
    draw.rectangle([cx - 14, cy + 20, cx + 14, cy + 24], fill=BLUE)


def icon_bridge(draw, x0, y0, x1, y1):
    # Water.
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(120, 170, 205))
    draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=(255, 255, 255), width=2)
    # Deck: left span, collapsed middle, right span.
    mid = (y0 + y1) // 2 - 6
    draw.rectangle([x0 + 10, mid, x0 + 118, mid + 7], fill=INK)
    draw.rectangle([x0 + 188, mid, x1 - 10, mid + 7], fill=INK)
    draw.polygon([(x0 + 118, mid + 7), (x0 + 138, mid + 26),
                  (x0 + 168, mid + 26), (x0 + 188, mid + 7)], fill=RED)
    for px in (x0 + 30, x0 + 88, x0 + 218, x0 + 272):
        draw.line([(px, mid), (px, y1 - 16)], fill=INK, width=3)


def icon_gulf(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(120, 170, 205))
    # Ship hull.
    draw.polygon([(x0 + 30, y1 - 30), (x0 + 150, y1 - 30), (x0 + 138, y1 - 14),
                  (x0 + 44, y1 - 14)], fill=INK)
    draw.rectangle([x0 + 78, y1 - 46, x0 + 108, y1 - 30], fill=BLUE)
    # Explosion burst above.
    cx, cy = x0 + 210, y0 + 26
    for ang in range(0, 360, 30):
        import math
        r = 20
        x2 = cx + int(r * math.cos(math.radians(ang)))
        y2 = cy + int(r * math.sin(math.radians(ang)))
        draw.line([(cx, cy), (x2, y2)], fill=RED, width=4)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)


def icon_fire(draw, x0, y0, x1, y1):
    # House.
    draw.polygon([(x0 + 60, y0 + 18), (x0 + 150, y0 + 18), (x0 + 105, y0 - 2)],
                 fill=RED)
    draw.rectangle([x0 + 68, y0 + 18, x0 + 142, y1 - 8], fill=(150, 110, 70))
    draw.rectangle([x0 + 96, y1 - 26, x0 + 114, y1 - 8], fill=INK)
    # Flames sitting on the roof, centred over the house.
    draw.polygon([(x0 + 88, y0 + 20), (x0 + 98, y0 + 2), (x0 + 106, y0 + 14),
                  (x0 + 114, y0 + 0), (x0 + 124, y0 + 20)], fill=(230, 110, 20))
    draw.polygon([(x0 + 98, y0 + 20), (x0 + 106, y0 + 10), (x0 + 114, y0 + 20)],
                 fill=GOLD)


def icon_chip(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2 - 40, (y0 + y1) // 2
    draw.rectangle([cx - 26, cy - 22, cx + 26, cy + 22], fill=INK)
    draw.rectangle([cx - 12, cy - 10, cx + 12, cy + 10], fill=GOLD)
    for dx in (-18, 0, 18):
        draw.line([(cx + dx, cy - 22), (cx + dx, cy - 32)], fill=INK, width=3)
        draw.line([(cx + dx, cy + 22), (cx + dx, cy + 32)], fill=INK, width=3)
    # Rising chart arrow.
    ax0, ay0 = x0 + 176, y1 - 12
    draw.line([(ax0, ay0), (ax0 + 26, ay0 - 18), (ax0 + 52, ay0 - 30),
               (ax0 + 78, ay0 - 48)], fill=RED, width=5)
    draw.polygon([(ax0 + 78, ay0 - 48), (ax0 + 62, ay0 - 48), (ax0 + 78, ay0 - 32)],
                 fill=RED)


def icon_game(draw, x0, y0, x1, y1):
    # Neon sunset bands.
    for i, col in enumerate([(255, 140, 90), (255, 90, 120), (150, 60, 160)]):
        draw.rectangle([x0, y0 + i * 18, x1, y0 + (i + 1) * 18], fill=col)
    # Controller.
    cx, cy = (x0 + x1) // 2, y0 + 38
    draw.rounded_rectangle([cx - 52, cy - 14, cx + 52, cy + 14], radius=12,
                           fill=INK)
    draw.ellipse([cx - 38, cy - 6, cx - 26, cy + 6], fill=(255, 255, 255))
    draw.ellipse([cx + 26, cy - 6, cx + 38, cy + 6], fill=GOLD)
    draw.ellipse([cx - 6, cy - 4, cx + 6, cy + 4], fill=RED)


ICONS = {"justice": icon_justice, "bridge": icon_bridge, "gulf": icon_gulf,
         "fire": icon_fire, "chip": icon_chip, "game": icon_game}

CARDS = [
    ("justice", "JUSTICE — THE HAGUE",
     "ICJ: Myanmar guilty of Rohingya genocide",
     ["Genocidal intent found in 2017.",
      "About 10,000 killed; 730,000 fled."]),
    ("bridge", "WAR IN UKRAINE",
     "Ukraine hits Kerch Bridge a third time",
     ["Road and rail traffic suspended.",
      "Road span collapsed earlier in week."]),
    ("gulf", "CONFLICT — THE GULF",
     "Iran strikes Gulf states; Kuwait repels attack",
     ["Kuwait repels its first Iranian attack.",
      "Houthi rocket damages PIF Tower."]),
    ("fire", "BANGLADESH",
     "Bangladesh shuts down ahead of Hasina return",
     ["Lockdown shuts parts of the country.",
      "Yunus home torched; 37 Grameen branches hit."]),
    ("chip", "TECH — MARKETS",
     "Anthropic IPO: the largest ever at $81.3bn",
     ["Priced at $83; debuts on Nasdaq as ANT.",
      "Valued at about $1.5tn fully diluted."]),
    ("game", "CULTURE — GAMES",
     "GTA VI launches after 13-year wait",
     ["Out at midnight on PS5 and Xbox X|S.",
      "Presales top $1.6bn; reviews ~99/100."]),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, mx1 = 36, W - 36

    # Masthead.
    centred(d, 26, "THE WORLD IN ONE DAY", SERIF_B(60), INK)
    rule(d, 108, mx, mx1, 5)
    centred(d, 122, "THURSDAY \u2022 19 NOVEMBER 2026", SANS_B(27), RED)
    centred(d, 156, "Seven stories that defined the day, as reported",
            SANS(20), GREY)
    rule(d, 186, mx, mx1, 2)

    # Lead story.
    ly = 200
    d.text((mx, ly), "DIPLOMACY \u2014 SHENZHEN, CHINA", font=SANS_B(20), fill=RED)
    head = wrap(d, "Three leaders, one summit in Shenzhen", SERIF_B(43), 560)
    y = ly + 30
    for line in head:
        d.text((mx, y), line, font=SERIF_B(43), fill=INK)
        y += 50
    dek = ["Trump, Xi and Putin meet for the first time as a trio \u2014",
           "90 minutes, no breakthrough. They pledge talks on",
           "nuclear risks, UN reform and more oil output.",
           "Ukraine was not the main topic; Zelensky warned",
           "of a \u201cnew Yalta\u201d."]
    y += 4
    for line in dek:
        d.text((mx, y), line, font=SANS(20), fill=INK)
        y += 25
    draw_lead_art(d, 632, ly, mx1, ly + 228)

    rule(d, 472, mx, mx1, 2)

    # Cards: 3 x 2 grid.
    cw = (mx1 - mx - 2 * 12) // 3
    ch, gap = 182, 12
    top = 488
    for i, (icon, kicker, headline, deks) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x0 = mx + c * (cw + gap)
        y0 = top + r * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rectangle([x0, y0, x1, y1], outline=GREY, width=1)
        # Icon panel.
        d.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 56], fill=LIGHT_GREY)
        ICONS[icon](d, x0 + 1, y0 + 1, x1 - 1, y0 + 56)
        ty = y0 + 63
        d.text((x0 + 10, ty), kicker, font=SANS_B(14), fill=RED)
        hlines = wrap(d, headline, SERIF_B(20), cw - 20)
        ty += 20
        for line in hlines[:2]:
            d.text((x0 + 10, ty), line, font=SERIF_B(20), fill=INK)
            ty += 22
        # Dek: wrap each statement to the card width; shrink if it
        # would need more than 3 lines, so nothing crosses the border.
        dek_lines = []
        for s in deks:
            dek_lines.extend(wrap(d, s, SANS(14), cw - 20))
        dek_font = SANS(14)
        if len(dek_lines) > 3:
            dek_font = SANS(13)
            dek_lines = []
            for s in deks:
                dek_lines.extend(wrap(d, s, dek_font, cw - 20))
        ty = y0 + 128
        for line in dek_lines[:3]:
            d.text((x0 + 10, ty), line, font=dek_font, fill=INK)
            ty += 16

    # Ticker.
    ty = 878
    rule(d, ty, mx, mx1, 2)
    prefix = "ALSO TODAY:  "
    rest = ("COP31 deadlocked on fossil-fuel phaseout in Antalya; "
            "IEA calls the Hormuz crisis the greatest threat to energy security "
            "in history \u2022 Van Gogh sells for a record $190.4m at Sotheby's "
            "in New York \u2022 Cyclone Akvan nears India's east coast; landfall "
            "expected Friday")
    pw = text_w(d, prefix, SANS_B(17))
    lines = wrap(d, rest, SANS(17), mx1 - mx - pw)
    ty += 12
    d.text((mx, ty), prefix, font=SANS_B(17), fill=INK)
    d.text((mx + pw, ty), lines[0], font=SANS(17), fill=INK)
    ty += 21
    for line in lines[1:]:
        d.text((mx, ty), line, font=SANS(17), fill=INK)
        ty += 21

    centred(d, 976, "Thursday 19 November 2026 \u2022 All stories as reported on the day "
                     "\u2022 Sources: Reuters, AP, AFP, BBC, United Nations, IEA",
            SANS(14), GREY)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
