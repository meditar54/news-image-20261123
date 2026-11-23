#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page to entry.png (1024x1024).

Code-drawn infographic (Pillow): every headline and summary was verified
against reporting published on 23 November 2026 (Anadolu, BBC, Bloomberg,
CNN, Fox News, NYT, Washington Post, 10 Things Global News).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 240)
INK = (20, 20, 20)
GRAY = (107, 114, 128)
RED = (180, 35, 24)
GREEN = (27, 122, 77)
NAVY = (31, 58, 95)
BLUE = (29, 78, 216)
ORANGE = (194, 65, 12)
DARKRED = (156, 43, 46)
OCEAN = (46, 111, 183)
LAND = (62, 155, 79)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, bg, fnt):
    """Small caps tag chip; returns (width, height)."""
    pad_x, pad_y = 12, 6
    tw = draw.textlength(text, font=fnt)
    h = fnt.size + pad_y * 2
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + h], radius=4, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=(255, 255, 255))
    return tw + pad_x * 2, h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    right = W - M

    # ---------- Masthead ----------
    y = 30
    d.text((M, y), "THE WORLD IN ONE DAY", font=font(SANS_B, 26), fill=RED)
    y = 62
    date_font = font(SERIF_B, 56)
    date = "MONDAY, 23 NOVEMBER 2026"
    # shrink if needed so the date never overflows the margins
    while d.textlength(date, font=date_font) > right - M and date_font.size > 40:
        date_font = font(SERIF_B, date_font.size - 2)
    d.text((M, y), date, font=date_font, fill=INK)
    y = 140
    d.line([(M, y), (right, y)], fill=INK, width=4)
    d.line([(M, y + 8), (right, y + 8)], fill=INK, width=1)

    # ---------- Lead story: COP31 ----------
    ly = 172
    d.rectangle([M, ly, M + 10, ly + 268], fill=RED)
    tx = M + 28
    tag_font = font(SANS_B, 21)
    chip(d, tx, ly + 6, "CLIMATE  ·  ANTALYA, TURKEY", GREEN, tag_font)
    hy = ly + 48
    head_font = font(SANS_B, 54)
    head = ["COP31 talks collapse", "with no deal"]
    y = draw_lines(d, head, tx, hy, head_font, INK, 60)
    sum_font = font(SANS, 25)
    summary = ("More than 190 nations fail to agree at the UN summit — "
               "the first climate talks to end without a deal since 2009.")
    y = draw_lines(d, wrap(d, summary, sum_font, 620), tx, y + 12, sum_font, (60, 60, 60), 33)

    # Globe with a crack, right of the lead text
    cx, cy, r = 838, 306, 82
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN)
    for rx in (28, 58):
        d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=(255, 255, 255), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    for dy, half in ((-38, 62), (0, 82), (38, 62)):
        d.line([(cx - half, cy + dy), (cx + half, cy + dy)], fill=(255, 255, 255), width=2)
    for (ex, ey, ew, eh) in ((-52, -42, 46, 24), (8, -58, 30, 16),
                             (-18, 8, 40, 24), (18, 34, 30, 18)):
        d.ellipse([cx + ex, cy + ey, cx + ex + ew, cy + ey + eh], fill=LAND)
    crack = [(cx - 58, cy - 74), (cx - 18, cy - 32), (cx - 44, cy + 2),
             (cx + 6, cy + 34), (cx - 8, cy + 72)]
    # white halo first so the crack reads as a cut through the globe,
    # then the red stroke on top; a thin navy rim defines the disc
    d.line(crack, fill=(255, 255, 255), width=11, joint="curve")
    d.line(crack, fill=RED, width=6, joint="curve")
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)

    # ---------- 2x2 grid ----------
    gy = 470
    cell_w, cell_h = 462, 196
    gap = 20
    stories = [
        ("MIDDLE EAST", DARKRED, "Trump: Iran strikes may resume",
         "Says he is inclined to order new strikes after the New Year "
         "if no deal is reached."),
        ("CONFLICT", NAVY, "Russian warship sunk in Libya",
         "Corvette Merkury capsizes in Benghazi after a suspected drone "
         "attack; Libya files a UN complaint."),
        ("U.S. POLITICS", BLUE, "Democrats' biggest House win since 1992",
         "At least 258 seats called so far, with four races still to be called."),
        ("SPORT", ORANGE, "Alcaraz wins first ATP Finals title",
         "Beats world No. 1 Zverev 6–2, 7–6(9–7) — his 14th straight win."),
    ]
    h_font = font(SANS_B, 29)
    s_font = font(SANS, 22)
    for i, (tag, color, headline, summ) in enumerate(stories):
        cx0 = M + (i % 2) * (cell_w + gap)
        cy0 = gy + (i // 2) * (cell_h + gap)
        chip(d, cx0, cy0, tag, color, tag_font)
        hl = wrap(d, headline, h_font, cell_w)
        y = draw_lines(d, hl, cx0, cy0 + 38, h_font, INK, 35)
        draw_lines(d, wrap(d, summ, s_font, cell_w), cx0, y + 6, s_font, (60, 60, 60), 28)
    # hairline dividers between grid cells
    mid_x = M + cell_w + gap // 2
    d.line([(mid_x, gy), (mid_x, gy + 2 * cell_h + gap)], fill=(200, 196, 186), width=1)
    mid_y = gy + cell_h + gap // 2
    d.line([(M, mid_y), (right, mid_y)], fill=(200, 196, 186), width=1)

    # ---------- Also today strip ----------
    by = 892
    d.rectangle([M, by, right, by + 96], fill=INK)
    d.text((M + 16, by + 10), "ALSO TODAY", font=font(SANS_B, 21), fill=(255, 120, 100))
    also = ("Márquez equals Agostini's record with an 8th MotoGP title   ·   "
            "EU and Indonesia sign a trade deal after a decade of talks   ·   "
            "US lead over China in Asia narrows to its smallest since 2018")
    a_font = font(SANS, 21)
    draw_lines(d, wrap(d, also, a_font, right - M - 32), M + 16, by + 38, a_font,
               (245, 245, 245), 27)

    # ---------- Footer ----------
    d.text((M, 998), "Sources: Anadolu, BBC, Bloomberg, CNN, Fox News, NYT, Washington Post  ·  "
                     "All events of 23 November 2026",
           font=font(SANS, 16), fill=GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}  {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
