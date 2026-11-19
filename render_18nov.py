#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page (1024x1024).

A dense broadsheet front page drawn with PIL and real TTF fonts:
  - Noto Serif Display Black for the masthead
  - Noto Serif Bold / Regular for headlines and body
  - DejaVu Sans for kickers, labels and briefs

Layout (top to bottom): masthead + date line, the TOP 3 lead stories,
9 smaller stories in a 3x3 grid, 24 one-line briefs in 2 columns,
and a footer with a confidence note and sources.

Run once:   python3 render_18nov.py
Writes:      entry.png  (1024x1024, deterministic)
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width: 968

PAPER = (248, 244, 234)
INK = (18, 18, 18)
GRAY = (74, 74, 74)
RED = (178, 28, 28)
RULE = (30, 30, 30)
FAINT = (205, 198, 184)

DISPLAY_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x, y, w, weight=2):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=RULE)


def kicker(draw, x, y, text, size=12):
    fnt = font(SANS_BOLD, size)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + size + 5


def section_head(draw, x, y, text):
    """Small section header with a rule above it; returns y below it."""
    rule(draw, x, y, CW, 2)
    y += 7
    fnt = font(SANS_BOLD, 12)
    draw.text((x, y), text.upper(), font=fnt, fill=INK)
    return y + 12 + 6


# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD"
DATE_LINE = "WEDNESDAY, 18 NOVEMBER 2026"
EDITION = "THE DAY'S WORLD NEWS  •  ONE PAGE  •  No. 323"

LEAD = {
    "kicker": "The lead  •  Gulf war flares",
    "head": "U.S. JETS STRIKE IRAN AS GULF WAR FLARES",
    "body": (
        "American fighter jets hit a Revolutionary Guard missile site on Qeshm "
        "Island in the Strait of Hormuz after Iranian drones targeted a US radar "
        "at Sheikh Isa Air Base in Bahrain. Iran claimed overnight drone strikes "
        "on Ali Al Salem Air Base in Kuwait; Bahrain and Kuwait intercepted "
        "further attacks early on Wednesday."
    ),
    "facts": (
        "BRENT $93.14 (17 NOV)  •  $92.61 (18 NOV)  •  3 TANKERS HIT IN ~36 HRS  "
        "•  CENTCOM: NO US DAMAGE OR INJURIES"
    ),
}

TOP2 = {
    "kicker": "Asia",
    "head": "XI AND PUTIN MEET IN SHENZHEN AS APEC OPENS",
    "body": (
        "Xi Jinping and Vladimir Putin met in Shenzhen on Wednesday, a day "
        "before their planned trilateral summit with Donald Trump (Thu 19 Nov). "
        "The APEC summit opened in Shenzhen. In Manila, the Quad met at leader "
        "level for the first time in over two years; Trump announced a trade "
        "deal with the Philippines."
    ),
}

TOP3 = {
    "kicker": "Tech / Markets",
    "head": "NVIDIA'S $115.8 BILLION QUARTER — BUT NO HUANG COMEBACK",
    "body": (
        "Nvidia revenue hit $115.8 billion for the quarter ended 25 Oct, up 103% "
        "year on year; data-centre sales $107.6 billion; net profit $65.3 "
        "billion. The board unanimously accepted Jensen Huang's resignation "
        "and does not intend to reinstate him as CEO. Nvidia halted shipments "
        "of all licensed Hopper-generation AI chips to China."
    ),
}

SMALL9 = [
    ("Cyclone", "Cyclone Akvan bears down on India",
     "Odisha evacuated 47,000+; landfall ~noon Fri 20 Nov; winds 90–100 kmph, gusts 110."),
    ("Ukraine", "Kerch Bridge road arch collapses",
     "227-m span fell after 16–17 Nov strikes; road shut, 2 killed; rail partly back 18 Nov."),
    ("US politics", "Peltola flips Alaska — Democrats take Senate 56–44",
     "144,302–131,844 (50.12%); 9th flip; first Alaska Native in the Senate."),
    ("Space", "Voyager 1 reaches one light-day from Earth",
     "10:16 UTC, ~25.9bn km away; first human-made object so far; no data since 14 Nov."),
    ("AI", "OpenAI launches GPT-6.2 Astra and Sol",
     "Edu access, Astra API prices cut 20%, tighter cyber safeguards. (Released 17 Nov.)"),
    ("US politics", "Musk: “I’m not MAGA”",
     "Spent $445m+ in midterms; backed Paxton, who lost by 12 pts; wants 51 GOP senators in 2029."),
    ("Cricket", "Dhoni retires from the IPL",
     "Chennai Super Kings confirm a mentoring role ahead of IPL 2027."),
    ("Health", "US loses measles-free status after 26 years",
     "5,412 cases in 2026 (to 12 Nov), most since 1991, 45 states, 10 deaths. Mexico, Bolivia too."),
    ("Health", "Ebola in DR Congo passes 11,000 cases",
     "11,042 cases, 5,387 deaths (11 Nov); 2nd-largest outbreak on record; children ~1/3 of deaths."),
]

BRIEFS = [
    "India wholesale inflation 12.29% in Oct — four-year high (was 11.39% in Sep).",
    "India–Japan 2+2 dialogue in Tokyo, 18–19 Nov.",
    "Quad leaders meet in Manila; Trump announces Philippines trade deal.",
    "Alcaraz beats Medvedev 6–2, 6–4 at ATP Finals — into semis.",
    "Chelsea beat PSG 1–0 in Women's UCL — Buurman's 87th-min winner.",
    "India beat Pakistan 2–1 to win a record 10th SAFF Championship.",
    "Grizzlies beat Cavs 124–121 — 8th straight road win; Spencer 26 pts.",
    "Illinois beat Duke 99–78 — Stojakovic 46 pts at Cameron Indoor.",
    "England win ODI series in Australia — Hobart decider; Duckett century.",
    "Rio Tinto settles PNG mine dispute — pays $250 million.",
    "FIFA presidential election — Infantino seeks a fourth term.",
    "US intel chief: Iranian threats “substantially increased” (DNI Jay Clayton).",
    "Trump's Board of Peace faults Israel and Hamas over Gaza ceasefire.",
    "Israel's parliament elects Matan Kahana as speaker.",
    "WHO: 950,000 displaced Palestinians in flood-prone ground in Gaza.",
    "NATO announces new strategy for next-gen communications networks.",
    "Britain sanctions eight firms tied to West Bank settlement expansion.",
    "CISA warns on Java4Shell — Oracle patched Tue; Java in 90% of Fortune 500.",
    "Hayabusa2 retargeted — JAXA flyby of asteroid 2015 BM510 in Apr 2028.",
    "Quantum microscope reads ten spin states of strontium-87 atoms (ICFO).",
    "Australia: RBA split 6–3 on hike to 4.85%, an 18-year high; jobless 4.7%.",
    "South Korea exam-cheating crackdown — rewards up to $75,000.",
    "42 of world's 50 most polluted cities are in India–Pakistan.",
    "French Greens' Tondelier opens door to Mélenchon coalition for 2027.",
]

FOOTER_NOTE = (
    "HOW SURE ARE WE:  Figures are as reported on 18 November 2026. Where a number was "
    "still moving (oil, the cyclone track) we give the day's reported value. "
    "Sources: Reuters, BBC, AP, PAHO, WHO, NASA, company statements."
)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN
    y = 22

    # ---- masthead ----
    mast = font(DISPLAY_BLACK, 88)
    tw = d.textlength(MASTHEAD, font=mast)
    d.text(((W - tw) / 2, y), MASTHEAD, font=mast, fill=INK)
    y += 88 + 4
    rule(d, x, y, CW, 3)
    y += 7
    rule(d, x, y, CW, 1)
    y += 9
    # date / edition line
    dl = font(SANS_BOLD, 13)
    ed = font(SANS, 13)
    d.text((x, y), DATE_LINE, font=dl, fill=INK)
    ew = d.textlength(EDITION, font=ed)
    d.text((W - MARGIN - ew, y), EDITION, font=ed, fill=GRAY)
    y += 13 + 8
    rule(d, x, y, CW, 2)
    y += 10

    # ---- LEAD story (TOP 3 #1) ----
    y = kicker(d, x, y, LEAD["kicker"], size=13)
    head = font(SERIF_BLACK, 34)
    y = draw_lines(d, x, y, LEAD["head"], head, CW, spacing=2)
    y += 2
    body = font(SERIF_REG, 16)
    y = draw_lines(d, x, y, LEAD["body"], body, CW, spacing=3)
    y += 3
    facts = font(SANS_BOLD, 12)
    y = draw_lines(d, x, y, LEAD["facts"], facts, CW, fill=RED, spacing=2)
    y += 6
    rule(d, x, y, CW, 2)
    y += 10

    # ---- TOP 3 #2 and #3, two columns (both start at the same top) ----
    col_w = (CW - 24) // 2
    start_y = y
    bottom = start_y
    for i, story in enumerate((TOP2, TOP3)):
        cx = x + i * (col_w + 24)
        cy = kicker(d, cx, start_y, story["kicker"], size=12)
        hd = font(SERIF_BOLD, 21)
        cy = draw_lines(d, cx, cy, story["head"], hd, col_w, spacing=1)
        cy += 1
        bd = font(SERIF_REG, 14)
        cy = draw_lines(d, cx, cy, story["body"], bd, col_w, spacing=2)
        bottom = max(bottom, cy)
    col_y = bottom
    # vertical divider between the two columns
    mid = x + col_w + 12
    d.line([mid, y, mid, col_y - 4], fill=FAINT, width=1)
    y = col_y + 4
    rule(d, x, y, CW, 2)
    y += 8

    # ---- SMALL 9 grid (3 cols x 3 rows) ----
    y = section_head(d, x, y, "More of the day")
    gap = 16
    cell_w = (CW - 2 * gap) // 3
    cell_h = 78
    for row in range(3):
        row_y = y + row * cell_h
        for col in range(3):
            s = SMALL9[row * 3 + col]
            cx = x + col * (cell_w + gap)
            cy = kicker(d, cx, row_y, s[0], size=10)
            hd = font(SERIF_BOLD, 15)
            cy = draw_lines(d, cx, cy, s[1], hd, cell_w, spacing=0)
            bd = font(SERIF_REG, 12)
            draw_lines(d, cx, cy, s[2], bd, cell_w, spacing=1)
        # faint row divider (not after the last row)
        if row < 2:
            d.line([x, row_y + cell_h - 8, x + CW, row_y + cell_h - 8],
                   fill=FAINT, width=1)
    y += 3 * cell_h - 4
    rule(d, x, y, CW, 2)
    y += 8

    # ---- BRIEFS 24 (2 cols x 12 rows) ----
    y = section_head(d, x, y, "In brief")
    bcol_w = (CW - 24) // 2
    bf = font(SANS, 11)
    row_h = 17
    for i, b in enumerate(BRIEFS):
        col = 0 if i < 12 else 1
        row = i % 12
        bx = x + col * (bcol_w + 24)
        by = y + row * row_h
        d.rectangle([bx, by + 4, bx + 5, by + 9], fill=RED)
        # keep each brief to one line: shorten only if it would overflow
        txt = b
        while d.textlength(txt, font=bf) > bcol_w - 12 and len(txt) > 20:
            txt = txt.rsplit(" ", 1)[0] + "…"
        d.text((bx + 10, by), txt, font=bf, fill=INK)
    y += 12 * row_h + 2
    rule(d, x, y, CW, 2)
    y += 8

    # ---- footer: confidence note ----
    ff = font(SERIF_ITALIC, 12)
    y = draw_lines(d, x, y, FOOTER_NOTE, ff, CW, fill=GRAY, spacing=2)
    y += 2
    fin = font(SANS_BOLD, 10)
    tag = "THE WORLD  •  18 NOVEMBER 2026  •  ONE DAY, ONE PAGE"
    tw = d.textlength(tag, font=fin)
    d.text(((W - tw) / 2, y), tag, font=fin, fill=GRAY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
