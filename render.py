"""Draws one front page for 21 November 2026 into a 1024x1024 PNG.

The page is a vertical stack of bands. Each band draws itself and returns the
y it finished at, so build() can measure the whole page before saving it and
refuse to write anything that is clipped, overflows, or sets type under 12 px.

Vertical space is the binding constraint: a giant date plus 30 stories does
not fit at 1024 px unless the gutters are tight. So build() sweeps a few
density levels - looser first - and keeps the first one where every band
still passes. The chosen level is printed, and slack is reported, so the
layout can never silently squeeze.

Leading is absolute (a multiple of the font size), never the font's own
ascent plus descent: Poppins ships line metrics near 1.4 em, and trusting
them is what pushed the previous cycle's page 425 px past the canvas.

Pillow and the standard library only. No network. No external images: every
mark on the page is drawn from code.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

import newsdata as D

CANVAS = 1024
MARGIN = 26
GUTTER = 9

BG = "#F7F4EB"
INK = "#0E1218"
INK_SOFT = "#333B47"
HAIR = "#B4AC98"
PANEL = "#EBE5D4"
MAP_BG = "#DDD6C2"
LAND = "#C3BBA4"
COAST = "#9E9581"

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# Type scale. The floor is 12 px and build() enforces it.
SIZE = {
    "weekday": 28,
    "giant": 100,
    "lead_head": 28,
    "lead_deck": 14,
    "card_head": 18,
    "card_deck": 13,
    "brief": 13,
    "tag": 12,
    "label": 12,
    "stat_num": 31,
    "stat_label": 12,
    "clock": 14,
    "event": 12,
    "counts": 15,
    "foot": 12,
}

# One deliberate setting rather than a ladder: the page fits with 6 px to spare,
# the map gets 144 px of height, and nothing is squeezed to make it work.
DENSITIES = [
    {"gap": 2, "card_pad": 1, "lead_pad": 2, "digest_step": 13, "map": 130},
]


def _font(filename, size, variation=None):
    face = ImageFont.truetype(os.path.join(FONT_DIR, filename), size)
    if variation:
        try:
            face.set_variation_by_name(variation)
        except Exception:
            pass
    return face


def bold(size):
    return _font("Poppins-Bold.ttf", size)


def text_face(size, variation="Regular"):
    return _font("Inter-Variable.ttf", size, variation)


def mono(size, variation="Medium"):
    return _font("RobotoMono-Variable.ttf", size, variation)


class Sheet:
    """A canvas that remembers every string it drew, so the fit can be proved."""

    def __init__(self):
        self.image = Image.new("RGB", (CANVAS, CANVAS), BG)
        self.draw = ImageDraw.Draw(self.image)
        self.boxes = []
        self.clipped = []
        self.smallest = 999

    @staticmethod
    def split(text, face, width):
        words = text.split()
        if not words:
            return []
        out, line = [], words[0]
        for word in words[1:]:
            probe = line + " " + word
            if face.getlength(probe) <= width:
                line = probe
            else:
                out.append(line)
                line = word
        out.append(line)
        return out

    def record(self, x, y, s, face, anchor="la"):
        """Store the ink box of the string, not the font's em box.

        getmetrics() returns ascent plus descent, which for Poppins is about
        1.4 em - far taller than the letters. Using that would report overlaps
        that a reader never sees, so the audit would cry wolf. getmask() gives
        the actual painted pixels, which is what can collide on the page.
        """
        wide = face.getlength(s)
        up, down = face.getmetrics()
        mask_box = face.getmask(s).getbbox()
        if mask_box is None:          # a space, or nothing at all
            return
        mx0, my0, mx1, my1 = mask_box
        if anchor == "ra":
            dx, dy = x - wide, y
        elif anchor == "lm":
            dx, dy = x, y - (up + down) / 2.0
        elif anchor == "mm":
            dx, dy = x - wide / 2.0, y - (up + down) / 2.0
        else:
            dx, dy = x, y
        box = (dx + mx0, dy + my0, dx + mx1, dy + my1)
        self.boxes.append((box, s))
        self.smallest = min(self.smallest, face.size)

    def line_of(self, x, y, s, face, fill=INK, anchor="la", step=None):
        self.draw.text((x, y), s, font=face, fill=fill, anchor=anchor)
        self.record(x, y, s, face, anchor)
        return y + (step if step is not None else face.size * 1.3)

    def block(self, x, y, s, face, width, fill=INK, step=None, cap=None, name=""):
        step = step if step is not None else face.size * 1.28
        rows = self.split(s, face, width)
        if cap is not None and len(rows) > cap:
            self.clipped.append((name or s, len(rows), cap, rows[cap:]))
            rows = rows[:cap]
        for i, row in enumerate(rows):
            self.draw.text((x, y + i * step), row, font=face, fill=fill)
            self.record(x, y + i * step, row, face)
        return y + len(rows) * step

    def rule(self, x0, y, x1, weight=1, fill=INK):
        self.draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)

    def chip(self, x, y, label, face, colour, height=15):
        wide = face.getlength(label) + 10
        self.draw.rounded_rectangle([x, y, x + wide, y + height], radius=2, fill=colour)
        self.draw.text((x + 5, y + height / 2.0), label, font=face, fill="#FFFFFF", anchor="lm")
        self.record(x + 5, y + height / 2.0, label, face, "lm")
        return wide

    def save(self, path):
        self.image.save(path, "PNG", optimize=True)


def giant_size(phrase, width):
    """Largest Poppins Bold size in the brief's 96-104 band that fits the width."""
    for size in range(SIZE["giant"], 95, -1):
        if bold(size).getlength(phrase) <= width:
            return size
    return 96


# ---------------------------------------------------------------- masthead
def masthead(s, y, stories, regions, fields, cap_out):
    kicker = text_face(SIZE["label"], "Bold")
    s.line_of(MARGIN, y, D.PAPER, kicker, INK, step=13)
    s.line_of(CANVAS - MARGIN, y, "ONE PAGE  ·  ONE DAY", kicker, INK_SOFT, anchor="ra", step=13)
    y += 14
    s.rule(MARGIN, y, CANVAS - MARGIN, 3)
    y += 4

    # Weekday above, numerals below: the numerals then own the full measure and
    # stay the largest element on the page without shrinking the weekday to a
    # speck.
    s.line_of(MARGIN, y, D.DAY_WORDS, bold(SIZE["weekday"]), INK, step=29)
    y += 29

    phrase = D.DAY_REST
    size = giant_size(phrase, CANVAS - 2 * MARGIN)
    face = bold(size)
    cap_out.append(face.getbbox("H")[3] - face.getbbox("H")[1])
    step = int(size * 0.93)
    s.line_of(MARGIN - 3, y, phrase, face, INK, step=step)
    y += step + 2
    s.rule(MARGIN, y, CANVAS - MARGIN, 1)
    y += 3

    tally = "%d STORIES  ·  %d REGIONS  ·  %d FIELDS  ·  ALL FROM THIS SATURDAY" % (
        stories, regions, fields)
    s.line_of(MARGIN, y, tally, bold(SIZE["counts"]), INK, step=17)
    return y + 17


# -------------------------------------------------------------- region bar
def region_bar(s, y, tally):
    height = 20
    s.draw.rectangle([MARGIN, y, CANVAS - MARGIN, y + height - 1], fill=INK)
    face = text_face(SIZE["label"], "Bold")
    x = MARGIN + 6
    for region in D.REGIONS:
        n = tally.get(region, 0)
        if not n:
            continue
        label = "%s %d" % (region.upper(), n)
        s.draw.rectangle([x, y + 5, x + 2, y + height - 6], fill=D.REGION_COLOR[region])
        s.draw.text((x + 6, y + height / 2.0), label, font=face, fill=BG, anchor="lm")
        s.record(x + 6, y + height / 2.0, label, face, "lm")
        x += face.getlength(label) + 17
    return y + height


# ---------------------------------------------------------------- timeline
def timeline(s, y, stamps):
    s.line_of(MARGIN, y, "THE DAY IN UTC", text_face(SIZE["label"], "Bold"), INK_SOFT, step=13)
    y += 14
    s.rule(MARGIN, y, CANVAS - MARGIN, 2)
    y += 4
    n = len(stamps)
    span = (CANVAS - 2 * MARGIN - GUTTER * (n - 1)) / float(n)
    clock = mono(SIZE["clock"], "Bold")
    event = text_face(SIZE["event"])
    bottom = y
    for i, (when, what) in enumerate(stamps):
        x = MARGIN + i * (span + GUTTER)
        s.draw.rectangle([x, y - 3, x, y - 1], fill=INK)
        s.line_of(x, y, when, clock, INK, step=15)
        bottom = max(bottom, s.block(x, y + 15, what, event, span - 2, INK_SOFT,
                                     step=14, cap=2, name="stamp:" + when))
    return bottom


# ------------------------------------------------------------------- marks
def glyph(d, kind, cx, cy, scale, colour):
    """Flat geometric marks only - nothing here is a photo or a bitmap."""
    if kind == "dome":
        d.arc([cx - scale, cy - scale * 0.85, cx + scale, cy + scale * 0.85],
              180, 360, fill=colour, width=3)
        d.line([cx - scale, cy + scale * 0.2, cx + scale, cy + scale * 0.2], fill=colour, width=3)
        for k in (-0.5, 0.0, 0.5):
            d.line([cx + k * scale, cy - scale * 0.3, cx + k * scale, cy + scale * 0.2],
                   fill=colour, width=2)
    elif kind == "badge":
        d.polygon([(cx, cy - scale), (cx + scale * 0.75, cy - scale * 0.4),
                   (cx + scale * 0.75, cy + scale * 0.35), (cx, cy + scale),
                   (cx - scale * 0.75, cy + scale * 0.35), (cx - scale * 0.75, cy - scale * 0.4)],
                  outline=colour, width=3)
        d.line([cx - scale * 0.28, cy, cx - scale * 0.05, cy + scale * 0.3], fill=colour, width=3)
        d.line([cx - scale * 0.05, cy + scale * 0.3, cx + scale * 0.35, cy - scale * 0.28],
               fill=colour, width=3)
    elif kind == "tanker":
        d.polygon([(cx - scale, cy + scale * 0.2), (cx + scale * 0.5, cy + scale * 0.2),
                   (cx + scale * 0.8, cy - scale * 0.1), (cx + scale * 0.8, cy + scale * 0.5),
                   (cx - scale, cy + scale * 0.5)], fill=colour)
        d.rectangle([cx + scale * 0.1, cy - scale * 0.5, cx + scale * 0.45, cy + scale * 0.05],
                    fill=colour)
    elif kind == "boat":
        d.arc([cx - scale, cy - scale * 0.15, cx + scale, cy + scale * 0.7], 0, 180,
              fill=colour, width=3)
        d.line([cx, cy - scale * 0.7, cx, cy + scale * 0.2], fill=colour, width=3)
        d.polygon([(cx, cy - scale * 0.65), (cx + scale * 0.55, cy + scale * 0.1),
                   (cx, cy + scale * 0.1)], fill=colour)


# ------------------------------------------------------------------- leads
def lead_cell(s, x, y, width, lead):
    colour = D.REGION_COLOR[lead["region"]]
    tag = text_face(SIZE["tag"], "Bold")
    wide = s.chip(x, y, lead["region"].upper(), tag, colour)
    s.line_of(x + wide + 5, y + 1, D.FIELD_LABEL[lead["field"]], tag, INK_SOFT, step=13)
    glyph(s.draw, lead["icon"], x + width - 15, y + 30, 16, colour)

    yy = s.block(x, y + 17, lead["headline"], bold(SIZE["lead_head"]), width - 36,
                 INK, step=30, cap=2, name="lead:" + lead["headline"][:16])
    yy = s.block(x, yy + 1, lead["deck"], text_face(SIZE["lead_deck"]), width,
                 INK_SOFT, step=16, cap=2, name="deck:" + lead["headline"][:16])
    return s.line_of(x, yy + 1, "%s · %s" % (lead["sure"], lead["outlets"]), tag, colour, step=13)


def leads_band(s, y, leads, pad):
    width = (CANVAS - 2 * MARGIN - GUTTER) / 2.0
    for row in (0, 1):
        edges = [lead_cell(s, MARGIN + col * (width + GUTTER), y, width,
                           leads[row * 2 + col]) for col in range(2)]
        y = max(edges) + pad
        if row == 0:
            s.rule(MARGIN, y - pad + 1, CANVAS - MARGIN, 1, HAIR)
    return y - pad


# ------------------------------------------------------------------- cards
def card_cell(s, x, y, width, card, number):
    colour = D.REGION_COLOR[card["region"]]
    tag = text_face(SIZE["tag"], "Bold")
    s.draw.rectangle([x, y, x + 2, y + 70], fill=colour)
    x += 7
    width -= 7
    s.line_of(x, y, "%02d" % number, mono(SIZE["tag"], "Bold"), colour, step=12)
    yy = s.block(x, y + 12, card["headline"], bold(SIZE["card_head"]), width, INK,
                 step=20, cap=2, name="card:" + card["headline"][:16])
    yy = s.block(x, yy, card["deck"], text_face(SIZE["card_deck"]), width, INK_SOFT,
                 step=15, cap=2, name="carddeck:" + card["headline"][:12])
    # A card column is 147 px wide; "CONFIRMED · Reuters, Al Jazeera" is not.
    # Drop the outlets before letting the tag cross into the next column.
    label = "%s · %s" % (card["sure"], card["outlets"])
    if tag.getlength(label) > width:
        label = card["sure"]
    return s.line_of(x, yy, label, tag, colour, step=12)


def cards_band(s, y, cards, pad):
    columns = 6
    width = (CANVAS - 2 * MARGIN - GUTTER * (columns - 1)) / float(columns)
    for start in range(0, len(cards), columns):
        edges = [card_cell(s, MARGIN + col * (width + GUTTER), y, width,
                           card, start + col + 1)
                 for col, card in enumerate(cards[start:start + columns])]
        y = max(edges) + pad
    return y - pad


# ------------------------------------------------------------------- stats
def stats_band(s, y, figures):
    n = len(figures)
    width = (CANVAS - 2 * MARGIN - GUTTER * (n - 1)) / float(n)
    s.rule(MARGIN, y, CANVAS - MARGIN, 2)
    y += 4
    num = mono(SIZE["stat_num"], "Bold")
    bottom = y
    for i, (value, caption) in enumerate(figures):
        x = MARGIN + i * (width + GUTTER)
        s.line_of(x, y, value, num, INK, step=30)
        bottom = max(bottom, s.block(x, y + 30, caption, text_face(SIZE["stat_label"]),
                                     width - 2, INK_SOFT, step=14, cap=2,
                                     name="stat:" + value))
    return bottom


# --------------------------------------------------------------------- map
# Coarse coastlines, drawn by hand at this scale: enough to place a pin, and
# plainly a diagram rather than a survey.
COASTS = {
    "north_america": [(-168, 66), (-156, 71), (-140, 70), (-125, 70), (-110, 69), (-95, 72),
                      (-80, 73), (-62, 67), (-55, 52), (-66, 45), (-71, 41), (-76, 35),
                      (-81, 25), (-90, 29), (-97, 26), (-105, 22), (-113, 29), (-124, 40),
                      (-124, 48), (-136, 58), (-152, 59)],
    "greenland": [(-55, 60), (-42, 60), (-20, 70), (-19, 82), (-45, 84), (-61, 76), (-58, 66)],
    "south_america": [(-79, 9), (-60, 11), (-50, 0), (-35, -6), (-38, -16), (-48, -25),
                      (-58, -35), (-63, -43), (-69, -55), (-75, -51), (-72, -40),
                      (-71, -18), (-80, -5)],
    "africa": [(-17, 15), (-10, 28), (0, 32), (10, 37), (25, 32), (33, 31), (36, 27),
               (43, 12), (51, 12), (43, -1), (40, -15), (35, -25), (26, -34), (18, -34),
               (12, -18), (9, 4), (-8, 5)],
    "eurasia": [(-10, 36), (0, 44), (5, 52), (10, 55), (20, 55), (30, 60), (28, 70),
                (42, 70), (60, 72), (90, 75), (120, 73), (140, 70), (162, 68), (179, 66),
                (179, 60), (160, 58), (140, 45), (130, 35), (122, 30), (110, 20),
                (105, 10), (95, 8), (90, 22), (80, 10), (72, 20), (60, 25), (45, 30),
                (36, 36), (28, 40), (20, 42), (10, 44), (0, 40)],
    "australia": [(114, -22), (122, -18), (130, -12), (142, -11), (147, -19), (153, -28),
                  (150, -38), (140, -38), (129, -32), (115, -34)],
    "new_zealand": [(166, -46), (174, -41), (178, -38), (173, -35), (168, -44)],
    "indonesia": [(95, 5), (110, 2), (120, -8), (105, -8), (95, -2)],
    "japan": [(130, 34), (142, 40), (146, 36), (136, 33)],
    "madagascar": [(43, -12), (50, -15), (48, -25), (44, -20)],
}


def map_band(s, x, y, width, height, pins):
    s.line_of(x, y, "WHERE IT HAPPENED", text_face(SIZE["label"], "Bold"), INK_SOFT, step=13)
    y += 14
    s.draw.rectangle([x, y, x + width - 1, y + height - 1], fill=MAP_BG)

    top_lat, bottom_lat = 84.0, -58.0

    def to_x(lon):
        return x + 6 + (lon + 180.0) / 360.0 * (width - 12)

    def to_y(lat):
        return y + 4 + (top_lat - lat) / (top_lat - bottom_lat) * (height - 8)

    for points in COASTS.values():
        s.draw.polygon([(to_x(lon), to_y(lat)) for lon, lat in points], fill=LAND)
    for lon in range(-150, 180, 30):
        s.draw.line([(to_x(lon), y + 4), (to_x(lon), y + height - 5)], fill=MAP_BG, width=1)
    for lat in range(-45, 75, 15):
        s.draw.line([(x + 6, to_y(lat)), (x + width - 7, to_y(lat))], fill=MAP_BG, width=1)
    for points in COASTS.values():
        s.draw.polygon([(to_x(lon), to_y(lat)) for lon, lat in points], outline=COAST)

    digits = text_face(12, "Bold")
    placed = []
    for number, lon, lat, colour in pins:
        cx, cy = to_x(lon), to_y(lat)
        # Several stories share a city or a strait. A pin that lands on top of
        # another pin hides a number, so nudge it along a small spiral until it
        # has room. The dot still sits close enough to read as that place.
        for attempt in range(24):
            if all((cx - px) ** 2 + (cy - py) ** 2 > 15 ** 2 for px, py in placed):
                break
            step = 5 + 3 * attempt
            cx += (1 if attempt % 2 else -1) * step * 0.7
            cy += (1 if attempt % 3 else -1) * step * 0.5
        placed.append((cx, cy))
        radius = 7
        s.draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                       fill=colour, outline=BG, width=1)
        s.draw.text((cx, cy), str(number), font=digits, fill="#FFFFFF", anchor="mm")
        s.smallest = min(s.smallest, 12)
    return y + height


# -------------------------------------------------------------- date check
def date_check_height(left_out, not_yet, width=366):
    """Two labelled flows of inline items, plus whatever rows they wrap onto."""
    inner = width - 22
    rows_left = _flow_rows(left_out, inner)
    rows_next = _flow_rows(not_yet, inner)
    return 24 + 15 * (1 + rows_left) + 15 * (1 + rows_next) + 4


def _flow_rows(items, width):
    """How many rows a list of dated items takes when flowed inline."""
    when_face = mono(SIZE["label"], "Bold")
    what_face = text_face(SIZE["label"])
    x, rows = 0.0, 1
    for when, what in items:
        need = when_face.getlength(when) + 5 + what_face.getlength(what) + 14
        if x + need > width and x > 0:
            rows += 1
            x = 0.0
        x += need
    return rows


def date_check(s, x, y, width, left_out, not_yet):
    """Left-out and upcoming items flowed inline, so the box stays shallow.

    Stacking one item per row made this box the tallest thing on the page and
    forced the map to shrink. Flowing each list across the full width keeps
    every word at 12 px while cutting the box to a few rows.
    """
    height = date_check_height(left_out, not_yet, width)
    s.draw.rectangle([x, y, x + width - 1, y + height - 1], fill=PANEL)
    s.draw.rectangle([x, y, x + 3, y + height - 1], fill=INK)
    head = text_face(SIZE["label"], "Bold")
    when_face = mono(SIZE["label"], "Bold")
    what_face = text_face(SIZE["label"])
    s.line_of(x + 10, y + 4, "DATE CHECK", head, INK, step=14)

    yy = y + 24
    for title, colour, items in (("LEFT OUT ON PURPOSE", "#8A3A10", left_out),
                                 ("NOT YET", "#1B4C9C", not_yet)):
        s.line_of(x + 10, yy, title, head, colour, step=15)
        cx = x + 10 + head.getlength(title) + 12
        limit = x + width - 12
        for when, what in items:
            need = when_face.getlength(when) + 5 + what_face.getlength(what) + 14
            if cx + need > limit and cx > x + 10 + head.getlength(title) + 12:
                yy += 15
                cx = x + 10
            s.line_of(cx, yy, when, when_face, INK_SOFT, step=15)
            cx += when_face.getlength(when) + 5
            s.line_of(cx, yy, what, what_face, INK, step=15)
            cx += what_face.getlength(what) + 14
        yy += 15
    return y + height


# ------------------------------------------------------------------ digest
def digest_band(s, y, briefs, first_number, step, columns=3, width=None):
    """Briefs in N columns inside the given width.

    With 20 briefs and two columns the block is tall and narrow, which is what
    lets DATE CHECK sit beside it instead of underneath.
    """
    s.line_of(MARGIN, y, "ALSO ON 21 NOVEMBER", text_face(SIZE["label"], "Bold"), INK_SOFT, step=13)
    y += 14
    total = width if width is not None else CANVAS - 2 * MARGIN
    col_w = (total - GUTTER * (columns - 1)) / float(columns)
    per_column = (len(briefs) + columns - 1) // columns
    body = text_face(SIZE["brief"])
    num = mono(SIZE["tag"], "Bold")
    bottom = y
    for i, brief in enumerate(briefs):
        col, row = i // per_column, i % per_column
        x = MARGIN + col * (col_w + GUTTER)
        yy = y + row * step
        s.draw.rectangle([x, yy + 2, x + 2, yy + 11], fill=D.REGION_COLOR[brief["region"]])
        s.line_of(x + 6, yy, "%02d" % (i + first_number), num, INK_SOFT, step=13)
        s.block(x + 27, yy, brief["text"], body, col_w - 29, INK, step=step, cap=1,
                name="brief:" + brief["text"][:14])
        bottom = max(bottom, yy + step)
    return bottom


# ------------------------------------------------------------------ legend
def legend(s, y):
    """Five confidence tags, flowed onto as many rows as they need."""
    bold_face = text_face(SIZE["label"], "Bold")
    plain = text_face(SIZE["label"])
    limit = CANVAS - MARGIN
    x = MARGIN
    s.line_of(x, y, "HOW SURE:", bold_face, INK_SOFT, step=13)
    x += bold_face.getlength("HOW SURE:") + 6
    for word, note in D.SURE_LEGEND:
        need = bold_face.getlength(word) + 4 + plain.getlength(note) + 14
        if x + need > limit:
            x = MARGIN
            y += 13
        s.line_of(x, y, word, bold_face, INK, step=13)
        x += bold_face.getlength(word) + 4
        s.line_of(x, y, note, plain, INK_SOFT, step=13)
        x += plain.getlength(note) + 14
    return y + 13


def footer(s, y):
    s.rule(MARGIN, y, CANVAS - MARGIN, 1, HAIR)
    y += 3
    s.line_of(MARGIN, y, D.FOOTER, text_face(SIZE["foot"], "Bold"), INK, step=13)
    y += 13
    s.block(MARGIN, y, D.SOURCES_LINE, text_face(SIZE["foot"]), CANVAS - 2 * MARGIN,
            INK_SOFT, step=13, cap=2, name="sources")
    return y + 24


# -------------------------------------------------------------------- page
def tally_by_region():
    counts = {}
    for group in (D.LEADS, D.CARDS, D.BRIEFS):
        for item in group:
            counts[item["region"]] = counts.get(item["region"], 0) + 1
    return counts


def pin_list():
    """Every lead and card gets a pin, numbered as it is numbered on the page."""
    pins = []
    for i, lead in enumerate(D.LEADS):
        lon, lat = lead["pin"]
        pins.append((i + 1, lon, lat, D.REGION_COLOR[lead["region"]]))
    for j, card in enumerate(D.CARDS):
        lon, lat = card["pin"]
        pins.append((len(D.LEADS) + j + 1, lon, lat, D.REGION_COLOR[card["region"]]))
    return pins


def compose(density, verbose=False):
    s = Sheet()
    counts = tally_by_region()
    stories = len(D.LEADS) + len(D.CARDS) + len(D.BRIEFS)
    regions = len([r for r in D.REGIONS if counts.get(r)])
    fields = {item["field"] for group in (D.LEADS, D.CARDS, D.BRIEFS) for item in group}
    caps = []
    gap = density["gap"]
    bands = []

    y = 6
    start = y
    y = masthead(s, y, stories, regions, len(fields), caps)
    bands.append(("masthead", start, y))
    y += gap

    start = y
    y = region_bar(s, y, counts)
    bands.append(("regionbar", start, y))
    y += gap

    start = y
    y = timeline(s, y, D.TIMELINE)
    bands.append(("timeline", start, y))
    y += gap

    start = y
    y = leads_band(s, y, D.LEADS, density["lead_pad"])
    bands.append(("leads", start, y))
    y += gap

    start = y
    y = cards_band(s, y, D.CARDS, density["card_pad"])
    bands.append(("cards", start, y))
    y += gap

    start = y
    y = stats_band(s, y, D.STATS)
    bands.append(("stats", start, y))
    y += gap

    # Full-width map: a world this crowded cannot be read in a half-column, and
    # the previous cycle's small map was called out for exactly that.
    start = y
    y = map_band(s, MARGIN, y, CANVAS - 2 * MARGIN, density["map"], pin_list())
    bands.append(("map", start, y))
    y += gap

    # Digest on the left, DATE CHECK on the right: both are small type, and
    # pairing them keeps the map at full width instead of stealing its height.
    check_width = 372
    digest_width = CANVAS - 2 * MARGIN - check_width - GUTTER
    start = y
    digest_bottom = digest_band(s, y, D.BRIEFS, len(D.LEADS) + len(D.CARDS) + 1,
                                density["digest_step"], columns=2, width=digest_width)
    check_bottom = date_check(s, MARGIN + digest_width + GUTTER, y, check_width,
                              D.LEFT_OUT, D.NOT_YET)
    y = max(digest_bottom, check_bottom)
    bands.append(("digest+check", start, y))
    y += gap

    start = y
    y = legend(s, y)
    bands.append(("legend", start, y))
    y += 2

    start = y
    y = footer(s, y)
    bands.append(("footer", start, y))

    if verbose:
        print("density        %r" % (density,))
        for name, a, b in bands:
            print("  %-11s %4d -> %4d  %3d px" % (name, a, b, b - a))
        print("giant date     %d px font, cap %d px" % (
            giant_size(D.DAY_REST, CANVAS - 2 * MARGIN), caps[0]))
        print("bottom         %4d of %d, slack %d px" % (y, CANVAS, CANVAS - MARGIN - y))
        print("smallest font  %d px, %d strings" % (s.smallest, len(s.boxes)))

    problems = []
    if s.clipped:
        problems.append("clipped: %r" % (s.clipped[:3],))
    if y > CANVAS - MARGIN:
        problems.append("overflows by %d px" % (y - (CANVAS - MARGIN)))
    outside = [t for (box, t) in s.boxes
               if box[0] < 0 or box[1] < 0 or box[2] > CANVAS or box[3] > CANVAS]
    if outside:
        problems.append("outside canvas: %r" % (outside[:3],))
    if s.smallest < 12:
        problems.append("type under 12 px: %d" % s.smallest)
    if caps[0] < 48:
        problems.append("date letter height %d px under 48" % caps[0])
    clashes = overlaps(s.boxes)
    if clashes:
        problems.append("%d overlapping strings, e.g. %r" % (len(clashes), clashes[:2]))
    return s, y, problems, stories


def overlaps(boxes, tolerance=1.0):
    """Pairs of strings whose painted pixels intersect.

    Sorted sweep on the left edge, so this stays cheap with 200 strings.
    A one-pixel tolerance keeps letters that merely touch from counting.
    """
    ordered = sorted(boxes, key=lambda item: item[0][0])
    found = []
    for i, (a, ta) in enumerate(ordered):
        for b, tb in ordered[i + 1:]:
            if b[0] >= a[2] - tolerance:
                break
            if (b[1] < a[3] - tolerance and b[3] > a[1] + tolerance):
                found.append((ta[:22], tb[:22]))
                if len(found) >= 40:
                    return found
    return found


def build(path, verbose=True):
    for density in DENSITIES:
        s, bottom, problems, stories = compose(density, verbose=False)
        if not problems:
            if verbose:
                compose(density, verbose=True)
                words = count_words()
                print("stories %d, words on page %d" % (stories, words))
            s.save(path)
            return s
        if verbose:
            print("density %r rejected: %s" % (density["gap"], "; ".join(problems)))
    raise SystemExit("no density level fits: " + "; ".join(problems))


def count_words():
    chunks = []
    for lead in D.LEADS:
        chunks += [lead["headline"], lead["deck"], lead["outlets"]]
    for card in D.CARDS:
        chunks += [card["headline"], card["deck"], card["outlets"]]
    for brief in D.BRIEFS:
        chunks.append(brief["text"])
    for when, what in D.TIMELINE:
        chunks.append(what)
    for value, caption in D.STATS:
        chunks += [value, caption]
    for when, what in D.LEFT_OUT + D.NOT_YET:
        chunks.append(what)
    for word, note in D.SURE_LEGEND:
        chunks.append(note)
    chunks += [D.FOOTER, D.SOURCES_LINE]
    return sum(len(c.split()) for c in chunks)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
