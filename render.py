"""Draws the front page into entry.png. Offline; Pillow + stdlib only.

Each band measures itself and returns its bottom edge; build() asserts the
stack fits, so the page can never silently overflow. Leading is absolute
(multiples of the font size), not the font's own ascent+descent, because
Poppins ships metrics near 1.4em and would waste a third of the page.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

import newsdata as D

W = H = 1024
M = 26
GUT = 10

BG = "#F7F4EB"
INK = "#0E1218"
INK_SOFT = "#333B47"
HAIR = "#B4AC98"
PANEL = "#EBE5D4"
MAP_BG = "#DDD6C2"

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")


def _face(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def head(size):
    return _face("Poppins-Bold.ttf", size)


def body(size, weight="Regular"):
    return _face("Inter-Variable.ttf", size, weight)


def mono(size, weight="Regular"):
    return _face("RobotoMono-Variable.ttf", size, weight)


# Type scale. Floors: giant 90, lead 24, card 18, deck 16, brief 15,
# label 13, stat label 14, absolute minimum 12.
SZ = {
    "giant": 90,
    "lead_head": 24,
    "lead_deck": 16,
    "card_head": 19,
    "card_deck": 17,
    "brief": 16,
    "tag": 13,
    "label": 13,
    "stat_num": 28,
    "stat_label": 15,
    "clock": 16,
    "event": 14,
}


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), BG)
        self.d = ImageDraw.Draw(self.img)
        self.boxes = []
        self.min_size = 99
        self.clipped = []

    # ---------- measurement ----------
    @staticmethod
    def wrap(text, font, width):
        words = text.split()
        if not words:
            return []
        lines, cur = [], words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if font.getlength(trial) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
        return lines

    def _note(self, x, y, text, font, anchor="la"):
        wid = font.getlength(text)
        asc, desc = font.getmetrics()
        if anchor == "la":
            box = (x, y, x + wid, y + asc + desc)
        elif anchor == "ra":
            box = (x - wid, y, x, y + asc + desc)
        elif anchor == "lm":
            box = (x, y - (asc + desc) / 2, x + wid, y + (asc + desc) / 2)
        else:
            box = (x - wid / 2, y, x + wid / 2, y + asc + desc)
        self.boxes.append((box, text))
        self.min_size = min(self.min_size, font.size)

    # ---------- drawing ----------
    def text(self, x, y, s, font, fill=INK, anchor="la", step=None):
        self.d.text((x, y), s, font=font, fill=fill, anchor=anchor)
        self._note(x, y, s, font, anchor)
        return y + (step if step is not None else font.size * 1.35)

    def para(self, x, y, s, font, width, fill=INK, step=None,
             max_lines=None, name=""):
        step = step if step is not None else font.size * 1.28
        lines = self.wrap(s, font, width)
        if max_lines is not None and len(lines) > max_lines:
            self.clipped.append((name or s, len(lines), max_lines, lines[max_lines:]))
            lines = lines[:max_lines]
        for i, ln in enumerate(lines):
            self.d.text((x, y + i * step), ln, font=font, fill=fill)
            self._note(x, y + i * step, ln, font)
        return y + len(lines) * step

    def para_h(self, s, font, width, step=None, max_lines=None):
        step = step if step is not None else font.size * 1.28
        lines = self.wrap(s, font, width)
        if max_lines is not None:
            lines = lines[:max_lines]
        return len(lines) * step

    def rule(self, x0, y, x1, w=1, fill=INK):
        self.d.rectangle([x0, y, x1, y + w - 1], fill=fill)

    def pill(self, x, y, label, font, colour, h=16):
        bw = font.getlength(label) + 12
        self.d.rounded_rectangle([x, y, x + bw, y + h], radius=3, fill=colour)
        self.d.text((x + 6, y + h / 2), label, font=font, fill="#FFFFFF", anchor="lm")
        self._note(x + 6, y + h / 2, label, font, "lm")
        return bw

    def save(self, path):
        self.img.save(path, "PNG", optimize=True)


# ------------------------------------------------------------- masthead
def masthead(p, y, n_stories, n_regions, n_fields):
    f_kick = body(13, "Bold")
    p.text(M, y, D.PAPER, f_kick, INK, step=16)
    p.text(W - M, y, D.WEEKDAY + "  ·  ALL REGIONS", f_kick, INK_SOFT, anchor="ra", step=16)
    y += 17
    p.rule(M, y, W - M, 3)
    y += 5
    p.text(M - 3, y, D.DAY_LONG, head(SZ["giant"]), INK, step=88)
    y += 88
    p.rule(M, y, W - M, 1)
    y += 4
    f_sum = head(18)
    line = "%d STORIES   ·   %d REGIONS   ·   %d FIELDS" % (
        n_stories, n_regions, n_fields)
    p.text(M, y, line, f_sum, INK, step=22)
    p.text(W - M, y + 4, D.WEEKDAY, f_kick, INK_SOFT, anchor="ra", step=16)
    return y + 22


# ----------------------------------------------------------- region bar
def region_bar(p, y, counts):
    h = 22
    p.d.rectangle([M, y, W - M, y + h - 1], fill=INK)
    x = M + 7
    f = body(SZ["label"], "Bold")
    for reg in D.REGIONS:
        n = counts.get(reg, 0)
        if not n:
            continue
        label = "%s %d" % (reg.upper(), n)
        p.d.rectangle([x, y + 6, x + 2, y + h - 7], fill=D.REGION_COLOR[reg])
        p.d.text((x + 6, y + h / 2), label, font=f, fill=BG, anchor="lm")
        p._note(x + 6, y + h / 2, label, f, "lm")
        x += f.getlength(label) + 19
    return y + h


# ------------------------------------------------------------- timeline
def timeline(p, y, items):
    p.text(M, y, "THE DAY IN UTC", body(SZ["label"], "Bold"), INK_SOFT, step=15)
    y += 16
    p.rule(M, y, W - M, 2)
    y += 3
    n = len(items)
    colw = (W - 2 * M - GUT * (n - 1)) / n
    f_t = mono(SZ["clock"], "Bold")
    f_e = body(SZ["event"])
    bottom = y
    for i, (clock, event) in enumerate(items):
        x = M + i * (colw + GUT)
        p.d.rectangle([x, y - 3, x, y - 1], fill=INK)
        p.text(x, y, clock, f_t, INK, step=17)
        bottom = max(bottom, p.para(x, y + 17, event, f_e, colw - 4, INK_SOFT,
                                    step=15, max_lines=2, name=clock))
    return bottom


# ---------------------------------------------------------------- icons
def icon(d, kind, cx, cy, s, colour):
    """Geometric marks only: no bitmaps, no photographs."""
    if kind == "strike":
        for r in (0.34, 0.62, 0.90):
            rr = s * r
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 340, fill=colour, width=3)
        d.polygon([(cx, cy - s * 0.62), (cx - s * 0.20, cy - s * 0.06),
                   (cx + s * 0.20, cy - s * 0.06)], fill=colour)
    elif kind == "talks":
        d.rounded_rectangle([cx - s * 0.95, cy - s * 0.62, cx + s * 0.10, cy + s * 0.10],
                            radius=4, outline=colour, width=3)
        d.rounded_rectangle([cx - s * 0.10, cy - s * 0.10, cx + s * 0.95, cy + s * 0.62],
                            radius=4, outline=colour, width=3)
    elif kind == "handshake":
        d.arc([cx - s * 1.00, cy - s * 0.55, cx + s * 0.10, cy + s * 0.55],
              285, 75, fill=colour, width=3)
        d.arc([cx - s * 0.10, cy - s * 0.55, cx + s * 1.00, cy + s * 0.55],
              105, 255, fill=colour, width=3)
        d.rectangle([cx - s * 0.22, cy - s * 0.05, cx + s * 0.22, cy + s * 0.05],
                    fill=colour)
    elif kind == "chart":
        for i, hh in enumerate((0.34, 0.56, 0.46, 0.80)):
            bx = cx - s * 0.92 + i * s * 0.50
            d.rectangle([bx, cy + s * 0.50 - s * hh, bx + s * 0.34, cy + s * 0.50],
                        fill=colour)
        d.line([cx - s * 1.00, cy + s * 0.66, cx + s * 0.96, cy + s * 0.02],
               fill=colour, width=3)


# ---------------------------------------------------------------- leads
def lead_cell(p, x, y, w, lead):
    colour = D.REGION_COLOR[lead["region"]]
    f_tag = body(SZ["tag"], "Bold")
    f_head = head(SZ["lead_head"])
    f_deck = body(SZ["lead_deck"])

    bw = p.pill(x, y, lead["region"].upper(), f_tag, colour)
    p.text(x + bw + 6, y + 2, D.FIELD_LABEL[lead["field"]], f_tag, INK_SOFT, step=16)
    icon(p.d, lead["icon"], x + w - 20, y + 38, 24, colour)

    yy = y + 19
    yy = p.para(x, yy, lead["headline"], f_head, w - 42, INK, step=25,
                max_lines=2, name="lead:" + lead["headline"][:20])
    yy += 1
    yy = p.para(x, yy, lead["deck"], f_deck, w, INK_SOFT, step=18,
                max_lines=1, name="deck:" + lead["headline"][:20])
    yy += 1
    return p.text(x, yy, "%s · %s" % (lead["sure"], lead["outlets"]), f_tag,
                  colour, step=15)


def leads_band(p, y, leads):
    colw = (W - 2 * M - GUT) / 2
    for r in (0, 1):
        hs = []
        for c in range(2):
            x = M + c * (colw + GUT)
            hs.append(lead_cell(p, x, y, colw, leads[r * 2 + c]))
        y = max(hs) + 6
        if r == 0:
            p.rule(M, y - 3, W - M, 1, HAIR)
    return y - 3


# ---------------------------------------------------------------- cards
def card_cell(p, x, y, w, card, num):
    colour = D.REGION_COLOR[card["region"]]
    f_num = mono(SZ["tag"], "Bold")
    f_head = head(SZ["card_head"])
    f_deck = body(SZ["card_deck"])
    f_tag = body(SZ["tag"], "Bold")

    p.d.rectangle([x, y, x + 2, y + 62], fill=colour)
    x += 8
    w -= 8
    p.text(x, y, "%02d" % num, f_num, colour, step=14)
    yy = p.para(x, y + 14, card["headline"], f_head, w, INK, step=20,
                max_lines=2, name="card:" + card["headline"][:20])
    yy = p.para(x, yy, card["deck"], f_deck, w, INK_SOFT, step=18,
                max_lines=1, name="carddeck:" + card["headline"][:16])
    return p.text(x, yy, "%s · %s" % (card["sure"], card["outlets"]), f_tag,
                  colour, step=15)


def cards_band(p, y, cards):
    cols = 6
    colw = (W - 2 * M - GUT * (cols - 1)) / cols
    for r in range(0, len(cards), cols):
        hs = []
        for c, card in enumerate(cards[r:r + cols]):
            x = M + c * (colw + GUT)
            hs.append(card_cell(p, x, y, colw, card, r + c + 1))
        y = max(hs) + 4
    return y - 4


# ---------------------------------------------------------------- stats
def stats_band(p, y, stats):
    n = len(stats)
    colw = (W - 2 * M - GUT * (n - 1)) / n
    p.rule(M, y, W - M, 2)
    y += 4
    f_num = mono(SZ["stat_num"], "Bold")
    f_lab = body(SZ["stat_label"])
    bottom = y
    for i, (num, label) in enumerate(stats):
        x = M + i * (colw + GUT)
        p.text(x, y, num, f_num, INK, step=29)
        bottom = max(bottom, p.para(x, y + 29, label, f_lab, colw - 2, INK_SOFT,
                                    step=15, max_lines=1, name="stat:" + num))
    return bottom


# ------------------------------------------------------------------ map
CONTINENTS = [
    [(-168, 65), (-158, 71), (-138, 70), (-124, 70), (-110, 68), (-94, 70),
     (-80, 73), (-62, 66), (-56, 52), (-66, 45), (-70, 42), (-75, 35),
     (-81, 25), (-97, 26), (-105, 20), (-115, 30), (-125, 40), (-125, 48),
     (-136, 58), (-152, 60)],
    [(-55, 60), (-44, 60), (-22, 70), (-20, 82), (-45, 84), (-60, 76), (-58, 66)],
    [(-80, 9), (-60, 10), (-50, 0), (-35, -5), (-38, -15), (-48, -25),
     (-58, -35), (-63, -42), (-68, -55), (-75, -52), (-72, -40), (-71, -18),
     (-80, -5)],
    [(-17, 15), (-10, 28), (0, 32), (10, 37), (25, 32), (32, 31), (35, 28),
     (43, 12), (51, 12), (43, -2), (40, -15), (35, -25), (26, -34), (18, -34),
     (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (0, 44), (5, 52), (10, 55), (20, 55), (30, 60), (28, 70),
     (40, 70), (60, 72), (90, 75), (120, 73), (140, 70), (160, 68), (179, 66),
     (179, 60), (160, 58), (140, 45), (130, 35), (122, 30), (110, 20),
     (105, 10), (95, 8), (90, 22), (80, 10), (72, 20), (60, 25), (45, 30),
     (36, 36), (28, 40), (20, 42), (10, 44), (0, 40)],
    [(114, -22), (122, -18), (130, -12), (142, -11), (147, -19), (153, -28),
     (150, -38), (140, -38), (129, -32), (115, -34)],
    [(166, -46), (174, -41), (178, -38), (173, -35), (168, -44)],
    [(95, 5), (110, 2), (120, -8), (105, -8), (95, -2)],
    [(130, 34), (142, 40), (146, 36), (136, 33)],
    [(43, -12), (50, -15), (48, -25), (44, -20)],
]


def _inside(lon, lat, poly):
    hit = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > lat) != (y2 > lat):
            if lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                hit = not hit
    return hit


def map_band(p, x, y, w, h, pins):
    p.text(x, y, "WHERE IT HAPPENED", body(SZ["label"], "Bold"), INK_SOFT, step=15)
    y += 15
    p.d.rectangle([x, y, x + w - 1, y + h - 1], fill=MAP_BG)

    lat_top, lat_bot = 82.0, -56.0

    def px(lon):
        return x + 4 + (lon + 180.0) / 360.0 * (w - 8)

    def py(lat):
        return y + 4 + (lat_top - lat) / (lat_top - lat_bot) * (h - 8)

    step = 3
    for cx in range(0, w - 6, step):
        lon = (cx - 4) / (w - 8) * 360.0 - 180.0
        for cy in range(0, h - 6, step):
            lat = lat_top - (cy - 4) / (h - 8) * (lat_top - lat_bot)
            for poly in CONTINENTS:
                if _inside(lon, lat, poly):
                    p.d.point((x + cx, y + cy), fill="#8B8570")
                    break

    f_pin = body(12, "Bold")
    R = 8
    placed = []
    for lon, lat, colour, label in pins:
        cx, cy = px(lon), py(lat)
        for _ in range(40):
            clash = any(abs(cx - ax) < 2 * R + 1 and abs(cy - ay) < 2 * R + 1
                        for (ax, ay) in placed)
            if not clash:
                break
            cx += 2 * R + 2          # step right past the neighbour
            if cx > x + w - R - 2:
                cx = px(lon)
                cy += 2 * R + 2
        placed.append((cx, cy))
        p.d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=colour,
                    outline=MAP_BG, width=1)
        p.d.text((cx, cy), label, font=f_pin, fill="#FFFFFF", anchor="mm")
        p.boxes.append(((cx - R, cy - R, cx + R, cy + R), label))
        p.min_size = min(p.min_size, f_pin.size)
    return y + h


# ------------------------------------------------------------ date check
def date_check_h(left_out, not_yet):
    """Height this panel needs, so its background can never be too short."""
    return 23 + 15 + 15 * len(left_out) + 4 + 15 + 15 * len(not_yet) + 6


def date_check(p, x, y, w, left_out, not_yet):
    h = date_check_h(left_out, not_yet)
    p.d.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL)
    p.d.rectangle([x, y, x + 3, y + h - 1], fill="#0E1218")
    p.text(x + 10, y + 5, "DATE CHECK", body(14, "Bold"), INK, step=16)
    yy = y + 23
    f_when = mono(13, "Bold")
    f_what = body(13)
    p.text(x + 10, yy, "LEFT OUT ON PURPOSE", body(SZ["label"], "Bold"), "#8A3A10",
           step=15)
    yy += 15
    for when, what in left_out:
        p.text(x + 10, yy, when, f_when, INK_SOFT, step=15)
        p.para(x + 56, yy, what, f_what, w - 64, INK, step=15, max_lines=1,
               name="leftout:" + what[:14])
        yy += 15
    yy += 4
    p.text(x + 10, yy, "NOT YET", body(SZ["label"], "Bold"), "#1B4C9C", step=15)
    yy += 15
    for when, what in not_yet:
        p.text(x + 10, yy, when, f_when, INK_SOFT, step=15)
        p.para(x + 56, yy, what, f_what, w - 64, INK, step=15, max_lines=1,
               name="notyet:" + what[:14])
        yy += 15
    return y + h


# --------------------------------------------------------------- digest
def digest_band(p, y, briefs):
    p.text(M, y, "ALSO ON 20 NOVEMBER", body(SZ["label"], "Bold"), INK_SOFT, step=15)
    y += 15
    cols = 3
    colw = (W - 2 * M - GUT * (cols - 1)) / cols
    per = (len(briefs) + cols - 1) // cols
    f = body(SZ["brief"])
    fn = mono(SZ["tag"], "Bold")
    bottom = y
    for i, b in enumerate(briefs):
        c, r = i // per, i % per
        x = M + c * (colw + GUT)
        yy = y + r * 15
        p.d.rectangle([x, yy + 3, x + 2, yy + 13], fill=D.REGION_COLOR[b["region"]])
        p.text(x + 7, yy + 1, "%02d" % (i + 13), fn, INK_SOFT, step=15)
        p.para(x + 30, yy, b["text"], f, colw - 32, INK, step=17, max_lines=1,
               name="brief:" + b["text"][:16])
        bottom = max(bottom, yy + 15)
    return bottom


# --------------------------------------------------------------- legend
def legend(p, y):
    f_b = body(SZ["label"], "Bold")
    f_n = body(SZ["label"])
    x = M
    p.text(x, y, "HOW SURE:", f_b, INK_SOFT, step=15)
    x += f_b.getlength("HOW SURE:") + 8
    for word, note in (("CONFIRMED", "2+ outlets"), ("OFFICIAL", "a statement"),
                       ("REPORTED", "1 outlet"), ("CLAIM", "one party"),
                       ("FORECAST", "a forecast")):
        p.text(x, y, word, f_b, INK, step=15)
        x += f_b.getlength(word) + 4
        p.text(x, y, note, f_n, INK_SOFT, step=15)
        x += f_n.getlength(note) + 10
    return y + 15


def footer(p, y):
    p.rule(M, y, W - M, 1, HAIR)
    y += 4
    p.text(M, y, "Every story here happened, or was first reported, on 20 November 2026.",
           body(SZ["label"], "Bold"), INK, step=15)
    y += 15
    p.para(M, y, "Sources: " + D.SOURCES_LINE, body(13), W - 2 * M, INK_SOFT,
           step=15, max_lines=1, name="sources")
    return y + 14


# ----------------------------------------------------------------- page
def counts():
    per = {}
    for group in (D.LEADS, D.CARDS, D.BRIEFS):
        for item in group:
            per[item["region"]] = per.get(item["region"], 0) + 1
    return per


def pins():
    out = []
    for i, lead in enumerate(D.LEADS):
        lon, lat = lead["pin"]
        out.append((lon, lat, D.REGION_COLOR[lead["region"]], str(i + 1)))
    for i, card in enumerate(D.CARDS):
        lon, lat = card["pin"]
        out.append((lon, lat, D.REGION_COLOR[card["region"]], str(i + 1)))
    return out


def build(out_path, verbose=True):
    p = Page()
    per = counts()
    n_stories = len(D.LEADS) + len(D.CARDS) + len(D.BRIEFS)
    n_regions = len([r for r in D.REGIONS if per.get(r)])
    fields = {i["field"] for g in (D.LEADS, D.CARDS, D.BRIEFS) for i in g}

    marks = []
    y = 12
    for name, fn, gap in (
        ("masthead", lambda yy: masthead(p, yy, n_stories, n_regions, len(fields)), 6),
        ("regionbar", lambda yy: region_bar(p, yy, per), 6),
        ("timeline", lambda yy: timeline(p, yy, D.TIMELINE), 6),
        ("leads", lambda yy: leads_band(p, yy, D.LEADS), 4),
        ("cards", lambda yy: cards_band(p, yy, D.CARDS), 3),
        ("stats", lambda yy: stats_band(p, yy, D.STATS), 4),
    ):
        top = y
        y = fn(y)
        marks.append((name, top, y))
        y += gap

    map_w = 596
    top = y
    row_h = max(120, date_check_h(D.LEFT_OUT, D.NOT_YET))
    date_check(p, M + map_w + GUT, y, W - 2 * M - map_w - GUT, D.LEFT_OUT, D.NOT_YET)
    map_band(p, M, y, map_w, row_h, pins())
    y = top + row_h
    marks.append(("map", top, y))
    y += 5

    top = y
    y = digest_band(p, y, D.BRIEFS)
    marks.append(("digest", top, y))
    y += 2
    top = y
    y = legend(p, y)
    marks.append(("legend", top, y))
    top = y
    y = footer(p, y)
    marks.append(("footer", top, y))

    if verbose:
        for name, a, b in marks:
            print("%-10s %4d -> %4d  (%3d)" % (name, a, b, b - a))
        print("bottom     %4d / canvas %d   slack %d" % (y, H, H - M - y))
        print("smallest font: %d px" % p.min_size)
        for c in p.clipped:
            print("CLIPPED", c[0], "lines", c[1], ">", c[2], c[3])

    assert y <= H - M + 1, "page overflows by %.1f px" % (y - (H - M))
    assert not p.clipped, "text was truncated: %r" % (p.clipped[:3],)
    off = [t for (b, t) in p.boxes if b[0] < 0 or b[1] < 0 or b[2] > W or b[3] > H]
    assert not off, "text outside canvas: %r" % (off[:3],)
    assert p.min_size >= 12, "text below 12 px: %d" % p.min_size

    p.save(out_path)
    return p


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
