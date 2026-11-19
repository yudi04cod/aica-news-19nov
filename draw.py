"""Draw the 19 November 2026 front page for make.fun news-image-20261119.

Flat vector-style newspaper front page, drawn programmatically with PIL.
Run:  python3 draw.py        # writes entry.png (1024x1024) next to this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color=(178, 34, 34)):
    f = font(SANS_BOLD, 15)
    draw.text((x, y), label, font=f, fill=color)
    return y + 21


def headline(draw, x, y, text, size, max_w, color=(20, 20, 20)):
    f = font(SERIF, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, (x, y), lines, f, color, leading=int(size * 1.08))


def body(draw, x, y, text, size, max_w, color=(40, 40, 40)):
    f = font(SANS, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, (x, y), lines, f, color, leading=int(size * 1.35))


def panel(draw, x, y, w, h, border=(30, 30, 30)):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255),
                   outline=border, width=2)
    draw.line([x + 2, y + 2, x + w - 3, y + 2], fill=(178, 34, 34), width=3)
    return x + 16, y + 12


# ---------------------------------------------------------------- scenes
def scene_gta(draw, x, y, w, h):
    # Sunset sky over a Vice City skyline with palm silhouettes.
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(255 - 60 * t)
        g = int(120 + 60 * t)
        b = int(60 + 110 * t)
        draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # sun
    cx, cy, r = x + w - 110, y + 78, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 90))
    # skyline
    base = y + h
    buildings = [(0, 150, 90), (80, 190, 60), (150, 130, 110), (260, 175, 70),
                 (340, 145, 95), (430, 185, 55), (500, 120, 55)]
    for bx, bh, bw in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(38, 22, 52))
        for wy in range(base - bh + 12, base - 10, 18):
            for wx in range(x + bx + 8, x + bx + bw - 8, 16):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 6, wy + 8],
                                   fill=(255, 214, 90))
    # sea strip
    draw.rectangle([x, base - 26, x + w, base], fill=(24, 90, 130))
    draw.line([x, base - 26, x + w, base - 26], fill=(255, 255, 255), width=2)
    # big VI
    f = font(SERIF, 92)
    draw.text((x + 26, y + 8), "VI", font=f, fill=(255, 255, 255),
              stroke_width=3, stroke_fill=(120, 20, 40))


def scene_shenzhen(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    # three flags on poles across the top half
    flags = ["stripes", "stars", "tricolour"]
    fw, fh = 54, 30
    gap = (w - 3 * fw) // 4
    for i, kind in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        fy = y + 8
        draw.line([(fx, fy), (fx, fy + fh + 8)], fill=(40, 40, 40), width=3)
        if kind == "stripes":
            for s in range(6):
                col = (178, 34, 34) if s % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx + 3, fy + s * 5, fx + 3 + fw, fy + (s + 1) * 5],
                               fill=col)
            draw.rectangle([fx + 3, fy, fx + 23, fy + 14], fill=(30, 60, 120))
        elif kind == "stars":
            draw.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh],
                       fill=(178, 34, 34), outline=(40, 40, 40), width=1)
            draw.ellipse([fx + 9, fy + 6, fx + 21, fy + 18],
                         fill=(255, 214, 90))
        else:
            for s, col in enumerate([(255, 255, 255), (30, 60, 160),
                                     (178, 34, 34)]):
                draw.rectangle([fx + 3, fy + s * 10, fx + 3 + fw,
                                fy + (s + 1) * 10], fill=col)
            draw.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh],
                           outline=(40, 40, 40), width=1)
    # skyline of Shenzhen towers along the bottom
    base = y + h
    fracs = [0.42, 0.58, 0.36, 0.66, 0.46, 0.60, 0.38]
    tw = w // 7
    for i, fr in enumerate(fracs):
        bh = int(h * fr)
        bx = x + i * tw + 2
        draw.rectangle([bx, base - bh, bx + tw - 4, base], fill=(52, 84, 120))
        for wy in range(base - bh + 6, base - 4, 10):
            draw.rectangle([bx + 4, wy, bx + tw - 8, wy + 3],
                           fill=(180, 210, 235))


def scene_icj(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    base = y + h
    roof_y = y + int(h * 0.52)
    # scales of justice above the roof
    sx, sy = x + w // 2, y + 6
    bar_y = sy + 16
    draw.line([(sx, sy), (sx, bar_y + 14)], fill=(90, 70, 20), width=3)
    draw.line([(sx - 30, bar_y), (sx + 30, bar_y)], fill=(90, 70, 20),
              width=3)
    for sgn in (-1, 1):
        px = sx + sgn * 30
        draw.line([(px, bar_y), (px, bar_y + 14)], fill=(90, 70, 20), width=2)
        draw.polygon([(px - 13, bar_y + 14), (px + 13, bar_y + 14),
                      (px, bar_y + 26)], fill=(200, 160, 40),
                     outline=(90, 70, 20))
    draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(200, 160, 40),
                 outline=(90, 70, 20))
    # courthouse: pediment + columns
    draw.rectangle([x + 16, roof_y, x + w - 16, roof_y + 8],
                   fill=(120, 110, 90))
    draw.polygon([(x + 16, roof_y), (x + w // 2, roof_y - 14),
                  (x + w - 16, roof_y)], fill=(150, 140, 118))
    col_w = 18
    n = 4
    span = w - 60
    for i in range(n):
        cx = x + 30 + i * span // (n - 1) - col_w // 2
        draw.rectangle([cx, roof_y + 8, cx + col_w, base - 6],
                       fill=(210, 200, 175), outline=(120, 110, 90), width=2)
    draw.rectangle([x + 16, base - 6, x + w - 16, base - 2],
                   fill=(120, 110, 90))


def scene_voyager(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(8, 12, 34))
    import random
    rng = random.Random(19112026)
    for _ in range(70):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        if sy < y + 30 and sx < x + 250:
            continue  # keep the label area clear
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r],
                     fill=(255, 255, 255))
    # sun, far away, bottom left
    draw.ellipse([x + 10, y + h - 34, x + 38, y + h - 6], fill=(255, 214, 90))
    # trajectory
    draw.line([(x + 28, y + h - 20), (x + w - 70, y + int(h * 0.55))],
              fill=(120, 180, 255), width=2)
    for t in range(0, 8):
        px = x + 28 + (w - 98) * t / 7
        py = y + h - 20 - (h - 20 - int(h * 0.55)) * t / 7
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(120, 180, 255))
    # spacecraft: golden dish + body
    cx, cy = x + w - 62, y + int(h * 0.55)
    draw.polygon([(cx - 26, cy - 6), (cx + 26, cy - 6), (cx, cy + 20)],
                 fill=(212, 175, 55), outline=(140, 110, 20))
    draw.rectangle([cx - 20, cy - 20, cx + 20, cy - 6], fill=(190, 190, 200),
                   outline=(90, 90, 100), width=2)
    draw.line([(cx - 20, cy - 20), (cx - 36, cy - 34)], fill=(190, 190, 200),
              width=3)
    draw.line([(cx + 20, cy - 20), (cx + 36, cy - 34)], fill=(190, 190, 200),
              width=3)
    f = font(SANS_BOLD, 15)
    draw.text((x + 14, y + 12), "1 LIGHT-DAY FROM HOME", font=f,
              fill=(255, 214, 90))


def scene_onkalo(draw, x, y, w, h):
    # cross-section of bedrock with a tunnel and a copper canister
    layers = [(238, 228, 205), (205, 190, 160), (170, 150, 125),
              (140, 120, 95)]
    lh = h // 4
    for i, col in enumerate(layers):
        draw.rectangle([x, y + i * lh, x + w, y + (i + 1) * lh], fill=col)
    for i in range(1, 4):
        draw.line([(x, y + i * lh), (x + w, y + i * lh)],
                  fill=(110, 95, 75), width=2)
    # tunnel
    th = int(h * 0.42)
    ty = y + h - th - 4
    tx, tw = x + 30, w - 60
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=th // 2,
                           fill=(40, 32, 24))
    # copper canister
    cw = min(64, tw - 24)
    cx = x + w // 2 - cw // 2
    draw.rounded_rectangle([cx, ty + 6, cx + cw, ty + th - 6], radius=6,
                           fill=(184, 115, 51), outline=(120, 70, 20), width=2)
    draw.line([(cx + cw // 3, ty + 6), (cx + cw // 3, ty + th - 6)],
              fill=(120, 70, 20), width=2)
    draw.line([(cx + 2 * cw // 3, ty + 6), (cx + 2 * cw // 3, ty + th - 6)],
              fill=(120, 70, 20), width=2)
    # depth marker (pill hides the layer line behind the text)
    f = font(SANS_BOLD, 14)
    label = "450 m DOWN IN FINNISH BEDROCK"
    lw = draw.textlength(label, font=f)
    draw.rectangle([x + 8, y + 4, x + 16 + lw, y + 26], fill=(238, 228, 205))
    draw.text((x + 12, y + 8), label, font=f, fill=(60, 45, 25))


def scene_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(52, 120, 170))
    # coastline on the left
    coast = w // 3
    draw.polygon([(x, y + h), (x + coast - 20, y + int(h * 0.25)),
                  (x + coast + 18, y + int(h * 0.55)), (x + coast, y + h)],
                 fill=(222, 205, 160))
    # cyclone spiral on the right
    cx, cy = x + coast + (w - coast) // 2, y + h // 2
    for k in range(4):
        r = 8 + k * 8
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 start=40 + k * 55, end=300 + k * 55,
                 fill=(255, 255, 255), width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))
    # rain bands over land
    for i in range(3):
        rx = x + 12 + i * 18
        draw.line([(rx, y + 12 + (i % 2) * 10), (rx - 6, y + 38 + (i % 2) * 10)],
                  fill=(200, 225, 245), width=3)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), (250, 246, 236))
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 118], fill=(20, 33, 61))
    d.rectangle([0, 118, W, 122], fill=(200, 162, 60))
    f_title = font(SERIF, 46)
    d.text((MARGIN, 14), "THE WORLD IN ONE PICTURE", font=f_title,
           fill=(255, 255, 255))
    f_sub = font(SANS_BOLD, 17)
    d.text((MARGIN, 86),
           "THURSDAY 19 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE PAGE",
           font=f_sub, fill=(200, 162, 60))

    # ---- lead story: GTA VI
    lx, ly, lw, lh = MARGIN, 136, CONTENT_W, 322
    panel(d, lx, ly, lw, lh)
    scene_gta(d, lx + 2, ly + 2, 560, lh - 4)
    tx = lx + 578
    y = kicker(d, tx, ly + 14, "GAMING  •  AFTER 13 YEARS")
    y = headline(d, tx, y, "VICE CITY AT LAST: GTA VI ROLLS OUT WORLDWIDE",
                 30, lw - 594)
    body(d, tx, y + 8,
         "Grand Theft Auto VI unlocks at midnight around the globe, "
         "starting in New Zealand. Pre-orders top $1.5bn and early "
         "reviews give it 99 on Metacritic — the biggest launch in "
         "gaming history.", 16, lw - 594)

    # ---- row 2: Shenzhen summit + ICJ verdict
    ry, rh = 472, 218
    pw = (CONTENT_W - 16) // 2
    # Shenzhen
    px = MARGIN
    panel(d, px, ry, pw, rh)
    scene_shenzhen(d, px + 2, ry + 2, pw - 4, 92)
    y = kicker(d, px + 16, ry + 106, "DIPLOMACY  •  SHENZHEN")
    y = headline(d, px + 16, y, "TRUMP, XI AND PUTIN MEET IN CHINA",
                 21, pw - 32)
    body(d, px + 16, y + 4,
         "The three leaders gather for a rare trilateral summit, "
         "with Xi greeting Trump on the tarmac.", 14, pw - 32)
    # ICJ
    px = MARGIN + pw + 16
    panel(d, px, ry, pw, rh)
    scene_icj(d, px + 2, ry + 2, pw - 4, 92)
    y = kicker(d, px + 16, ry + 106, "JUSTICE  •  THE HAGUE")
    y = headline(d, px + 16, y, "WORLD COURT RULES ON ROHINGYA CASE",
                 21, pw - 32)
    body(d, px + 16, y + 4,
         "Judges deliver their verdict today in The Gambia's case "
         "over Myanmar's 2017 crackdown.", 14, pw - 32)

    # ---- row 3: Voyager 1 + Finland Onkalo
    ry, rh = 704, 180
    px = MARGIN
    panel(d, px, ry, pw, rh)
    scene_voyager(d, px + 2, ry + 2, pw - 4, 70)
    y = kicker(d, px + 16, ry + 82, "SPACE  •  NASA")
    y = headline(d, px + 16, y, "VOYAGER 1 PASSES ONE LIGHT-DAY FROM EARTH",
                 19, pw - 32)
    body(d, px + 16, y + 4,
         "After nearly 50 years in flight, the probe likely crossed "
         "the mark this morning; NASA confirms it today.", 13, pw - 32)
    px = MARGIN + pw + 16
    panel(d, px, ry, pw, rh)
    scene_onkalo(d, px + 2, ry + 2, pw - 4, 70)
    y = kicker(d, px + 16, ry + 82, "ENERGY  •  FINLAND")
    y = headline(d, px + 16, y, "FINLAND APPROVES FIRST NUCLEAR WASTE TOMB",
                 19, pw - 32)
    body(d, px + 16, y + 4,
         "Regulators give the go-ahead to Onkalo, the first permanent "
         "repository for spent nuclear fuel, deep in bedrock.", 13,
         pw - 32)

    # ---- bottom row: cyclone panel + "also today" briefs
    ry, rh = 898, 102
    bw = (CONTENT_W - 16) // 2
    # cyclone
    px = MARGIN
    panel(d, px, ry, bw, rh)
    scene_cyclone(d, px + 2, ry + 2, 168, rh - 4)
    tx = px + 186
    y = kicker(d, tx, ry + 10, "WEATHER  •  INDIA")
    y = headline(d, tx, y, "CYCLONE AKVAN NEARS INDIA'S EAST COAST",
                 16, bw - 202)
    body(d, tx, y + 3,
         "Akvan is set to cross between Machilipatnam and Puri.",
         12, bw - 202)
    # briefs
    px = MARGIN + bw + 16
    panel(d, px, ry, bw, rh)
    y = kicker(d, px + 16, ry + 10, "ALSO TODAY")
    briefs = [
        "Van Gogh sells for a record $190.4m.",
        "EU proposes a €45bn loan for Ukraine.",
        "Crimean Bridge attacked again.",
        "Anthropic poised for a $1.4tn debut.",
    ]
    f_brief = font(SANS, 13)
    for b in briefs:
        d.text((px + 16, y), "•  " + b, font=f_brief, fill=(40, 40, 40))
        y += 18

    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
