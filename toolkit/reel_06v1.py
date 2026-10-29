"""Reel 05 v1 (from 04v3 helpers) - WOW fact: 88888888 phone number sold for 2.33M yuan. Inspo motion language, FASTER, no repeating typing/tick sounds, icons centred by bbox."""
import sys, math, random
sys.path.insert(0, "/home/claude/reels")
import reel_07base as P
import reel_04v2 as V
import reel_02 as R
from reel_lib import *
from PIL import ImageFilter

INK, BRAND, RLIGHT, MUTED, GREY, LINE = P.INK, P.BRAND, P.RLIGHT, P.MUTED, P.GREY, P.LINE
DUR, wl, ss, person = P.DUR, P.wl, P.ss, P.person
vo, ENV = P.vo, P.ENV
# ---------- helpers ----------
def tight(lay):
    bb = lay.getchannel("A").getbbox()
    c = lay.crop(bb); return c, (c.size[0] / 2, c.size[1] / 2)
_ct = {}
def ctext(s, size, wt, col):
    k = (s, size, wt, col)
    if k not in _ct: _ct[k] = tight(wl(s, size, wt, col)[0])
    return _ct[k]

def typed(img, t, segs, size, cx, by, t0, cps=30.0, alpha=1.0):
    ws = [text_w(s, int(size * k), wt) for s, wt, c, k in segs]
    total = sum(ws); x = cx - total / 2; n = 0
    for (s, wt, col, k), w in zip(segs, ws):
        fs = int(size * k)
        for i, ch in enumerate(s):
            if ch == " ": n += 1; continue
            age = t - (t0 + n / cps); n += 1
            if age < 0: continue
            p = clamp(age / 0.1); e = out_cubic(p)
            lay, anc = V.char_layer(ch, fs, wt, col, 7 * (1 - e) ** 1.5)
            cw = text_w(ch, fs, wt)
            px = x + text_w(s[:i], fs, wt) + cw / 2
            paste_scaled(img, lay, anc, px, by + 10 * (1 - e), 1.0 + 0.08 * (1 - e), min(1, p * 2) * alpha)
        x += w
    return t0 + n / cps
def bin_(img, lay, anc, cx, cy, t, t0, d=0.26, sc=1.0, alpha=1.0): V.blur_in(img, lay, anc, cx, cy, t, t0, d, sc, alpha)
def zh(img, s, cx, cy, t, t0, size=40, col=MUTED, wt="bold"): bin_(img, *wl(s, size, wt, col), cx, cy, t, t0)

S_ = lambda s, c=INK, k=1.0: (s, "extrabold", c, k)
SE_ = lambda s, c=BRAND, k=1.25: (s, "serif", c, k)
def pop(t, t0, d=0.28): return out_back(clamp((t - t0) / d), 2.2)

def disc_icon(r, glyph, fill=BRAND, k=3, pad=10, ring=None):
    S = (2 * r + 2 * pad) * k; c = S / 2
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), fill=fill)
    if ring: d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), outline=ring, width=5 * k)
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0)); glyph(ImageDraw.Draw(g), k, c)
    bb = g.getchannel("A").getbbox()
    tmp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    tmp.paste(g, (int(round(c - (bb[0] + bb[2]) / 2)), int(round(c - (bb[1] + bb[3]) / 2))))
    im.alpha_composite(tmp)
    im = im.resize((S // k, S // k), Image.LANCZOS)
    return im, (im.size[0] / 2, im.size[1] / 2)
WH = (255, 255, 255)
def g_phone(d, k, c):
    d.rounded_rectangle((c - 30 * k, c - 52 * k, c + 30 * k, c + 52 * k), 10 * k, outline=WH, width=7 * k)
    d.line((c - 10 * k, c - 38 * k, c + 10 * k, c - 38 * k), fill=WH, width=5 * k)
    d.ellipse((c - 5 * k, c + 30 * k, c + 5 * k, c + 40 * k), fill=WH)
def g_plane(d, k, c):
    d.polygon([(c - 60 * k, c - 6 * k), (c + 62 * k, c - 44 * k), (c + 22 * k, c + 44 * k), (c - 2 * k, c + 12 * k)], fill=WH)
def g_pin(d, k, c, hole=BRAND):
    d.ellipse((c - 30 * k, c - 50 * k, c + 30 * k, c + 10 * k), fill=WH)
    d.polygon([(c - 27 * k, c - 8 * k), (c + 27 * k, c - 8 * k), (c, c + 46 * k)], fill=WH)
    d.ellipse((c - 11 * k, c - 30 * k, c + 11 * k, c - 8 * k), fill=hole)
def g_ticket(d, k, c):
    d.rounded_rectangle((c - 50 * k, c - 30 * k, c + 50 * k, c + 30 * k), 10 * k, outline=WH, width=7 * k)
    for y in range(-20, 24, 12): d.line((c + 14 * k, c + y * k, c + 14 * k, c + (y + 6) * k), fill=WH, width=5 * k)
    d.line((c - 34 * k, c - 8 * k, c - 4 * k, c - 8 * k), fill=WH, width=6 * k); d.line((c - 34 * k, c + 10 * k, c - 12 * k, c + 10 * k), fill=WH, width=6 * k)
def g_person(d, k, c): person(d, k, c / k, c / k + 12, 56, WH)
def g_case(d, k, c):
    d.rounded_rectangle((c - 50 * k, c - 24 * k, c + 50 * k, c + 38 * k), 10 * k, fill=WH)
    d.arc((c - 20 * k, c - 50 * k, c + 20 * k, c - 8 * k), 180, 360, fill=WH, width=8 * k)
    d.line((c - 50 * k, c + 4 * k, c + 50 * k, c + 4 * k), fill=BRAND, width=5 * k)
def g_lock(d, k, c):
    d.arc((c - 26 * k, c - 58 * k, c + 26 * k, c + 2 * k), 180, 360, fill=WH, width=9 * k)
    d.line((c - 26 * k, c - 28 * k, c - 26 * k, c - 4 * k), fill=WH, width=9 * k); d.line((c + 26 * k, c - 28 * k, c + 26 * k, c - 4 * k), fill=WH, width=9 * k)
    d.rounded_rectangle((c - 42 * k, c - 6 * k, c + 42 * k, c + 46 * k), 10 * k, fill=WH)
    d.ellipse((c - 8 * k, c + 12 * k, c + 8 * k, c + 28 * k), fill=BRAND); d.rectangle((c - 3 * k, c + 22 * k, c + 3 * k, c + 38 * k), fill=BRAND)
def g_q(d, k, c): d.text((c, c), "?", font=font(100 * k, "extrabold"), fill=WH, anchor="mm")

ICON = {n: disc_icon(64, g, ) for n, g in (("phone", g_phone), ("plane", g_plane), ("pin", g_pin), ("ticket", g_ticket), ("lock", g_lock))}
ICON["lockS"] = disc_icon(48, g_lock)
ICON["person"] = disc_icon(120, g_person, fill=INK)
ICON["case"] = disc_icon(120, g_case)
ICON["q"] = disc_icon(120, g_q, fill=(176, 168, 156))
ICON["youP"] = disc_icon(100, g_person, fill=INK)

def pill(txt, zhs, icon, solid=False, size=44):
    w = int(text_w(txt, size, "bold")) + 190; h = 118; p = 16
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), h // 2, fill=BRAND if solid else (255, 255, 255), outline=None if solid else INK, width=3)
    ic, ia = ICON[icon]; sm = ic.resize((92, 92), Image.LANCZOS)
    lay.alpha_composite(sm, (p + 12, p + 13))
    if solid: d.ellipse((p + 14, p + 15, p + 14 + 88, p + 15 + 88), outline=WH, width=4)
    draw_text(d, p + 118, p + 52, txt, size, "bold", WH if solid else INK)
    draw_text(d, p + 118, p + 94, zhs, 28, "bold", (255, 214, 208) if solid else MUTED)
    return lay, (p + w / 2, p + h / 2)

# ---------- layers ----------
def digit_cell(on=True):
    w, h, p = 100, 150, 40
    lay, d, pp = P.card_shadow(w, h, 24, outline=(LINE if not on else BRAND));
    if on:
        e, ea = ctext("8", 120, "extrabold", BRAND); lay.alpha_composite(e, (int(pp + w / 2 - ea[0]), int(pp + h / 2 - ea[1])))
    return lay, (pp + w / 2, pp + h / 2)
CELL_ON = digit_cell(True)
def ghost_cell():
    w, h, p = 100, 150, 40
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 24, outline=(205, 198, 188), width=3)
    return lay, (p + w / 2, p + h / 2)
CELL_OFF = ghost_cell()
CELL_X = [540 + (i - 3.5) * 110 + (-15 if i < 4 else 15) for i in range(8)]

def circ_char(ch, r=150, col=INK, ring=BRAND, size=200):
    S = (2 * r + 60); im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 255, 255), outline=ring, width=7)
    t, a = ctext(ch, size, "extrabold", col); im.alpha_composite(t, (int(c - a[0]), int(c - a[1])))
    return im, (c, c)
CH8 = circ_char("八"); CHF = circ_char("发", col=BRAND)

def sold_stamp():
    w, h, p = 640, 190, 50
    im = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((p, p, p + w, p + h), 28, fill=(255, 255, 255, 235), outline=BRAND, width=9)
    d.rounded_rectangle((p + 14, p + 14, p + w - 14, p + h - 14), 18, outline=BRAND, width=3)
    t, a = ctext("SOLD  成交", 84, "extrabold", BRAND); im.alpha_composite(t, (int(p + w / 2 - a[0]), int(p + h / 2 - a[1])))
    return im, (p + w / 2, p + h / 2)
SOLD, SOLDA = sold_stamp()

def lot_card():
    w, h = 900, 470
    lay, d, p = P.card_shadow(w, h, 40)
    draw_text(d, p + 48, p + 76, "LOT 001  ·  拍卖", 30, "mono", MUTED)
    draw_text(d, p + w - 48, p + 76, "2003", 30, "mono", MUTED, "r")
    d.line((p + 40, p + 104, p + w - 40, p + 104), fill=LINE, width=3)
    return lay, (p + w / 2, p + h / 2), p
LOT, LOTA, LOTP = lot_card()

def chat_card(w=900, h=520):
    lay, d, p = P.card_shadow(w, h, 44)
    d.rounded_rectangle((p, p, p + w, p + 140), 44, fill=(247, 244, 240)); d.rectangle((p, p + 90, p + w, p + 140), fill=(247, 244, 240))
    d.line((p, p + 140, p + w, p + 140), fill=LINE, width=3)
    ic, ia = ICON["case"]; sm = ic.resize((92, 92), Image.LANCZOS); lay.alpha_composite(sm, (p + 34, p + 24))
    draw_text(d, p + 150, p + 66, "Casting agent", 38, "extrabold", INK); draw_text(d, p + 150, p + 108, "选角经纪人 · WeChat", 26, "bold", MUTED)
    return lay, (p + w / 2, p + h / 2), p
CC, CCA, CCP = chat_card()
def msg_line(txt, w=760, h=84, fill=(240, 236, 230), col=INK, size=36):
    p = 12; lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 26, fill=fill)
    draw_text(d, p + 30, p + h / 2 + size * 0.34, txt, size, "bold", col)
    return lay, (p + w / 2, p + h / 2)
ML = [msg_line("Casting tomorrow, ¥3000"), msg_line("WeChat:  wx_zhang88"), msg_line("Call:  138 0000 0000")]

def num_chip(txt="+86 138 0000 0000", size=40):
    w = int(text_w(txt, size, "mono")) + 80; h = 96; p = 20
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p + 6, p + w, p + h + 6), 48, fill=(0, 0, 0, 40)); lay = lay.filter(ImageFilter.GaussianBlur(8)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 48, fill=BRAND)
    draw_text(d, p + w / 2, p + h / 2 + size * 0.33, txt, size, "mono", WH, "m")
    return lay, (p + w / 2, p + h / 2)
NUM, NUMA = num_chip()

def arrow(img, x0, y0, x1, y1, prog, col=BRAND, w=8, head=26):
    p = clamp(prog)
    if p <= 0: return
    x, y = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    d = ImageDraw.Draw(img); d.line((x0, y0, x, y), fill=col, width=w)
    if p > 0.98:
        a = math.atan2(y1 - y0, x1 - x0)
        d.polygon([(x1, y1), (x1 - head * math.cos(a - 0.5), y1 - head * math.sin(a - 0.5)), (x1 - head * math.cos(a + 0.5), y1 - head * math.sin(a + 0.5))], fill=col)

WMK, WMKA = R.wordmark(150)

def whip(img, t, i):
    s = scene_idx(t); ts, te = SC[s], SC[s + 1]
    pe = clamp((t - (te - 0.14)) / 0.14) if s < NS else 0
    pn = 1 - clamp((t - ts) / 0.16) if s > 0 else 0
    a = max(pe ** 2, pn ** 2)
    if a < 0.02: return img
    dx = int(-190 * pe ** 2 + 190 * pn ** 2)
    arr = np.asarray(img)
    if dx: arr = np.roll(arr, dx, axis=1)
    arr = V.hblur_np(arr.astype(np.float32), 70 * a)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


SMALLP = disc_icon(40, g_person, fill=(196, 188, 176))
HIP = disc_icon(40, g_person, fill=BRAND)

def mkt_card():
    w, h = 920, 800
    lay, d, p = P.card_shadow(w, h, 48)
    wm, wa = R.wordmark(56); lay.alpha_composite(wm, (int(p + 40 - 40), int(p + 18 - 0)))
    d.rounded_rectangle((p + 520, p + 36, p + w - 40, p + 100), 32, fill=(244, 240, 234))
    draw_text(d, p + 548, p + 78, "Search  搜索", 26, "bold", GREY)
    rows = [("Runway casting", "走秀选角 · Shanghai", "case"), ("Brand shoot", "品牌拍摄 · Beijing", "pin"), ("English host", "英语主持 · Chengdu", "plane")]
    for k, (a, b, ic_) in enumerate(rows):
        y = p + 150 + k * 130
        d.rounded_rectangle((p + 36, y, p + w - 36, y + 108), 30, fill=(250, 247, 243), outline=LINE, width=2)
        ic, ia = ICON[ic_]; sm = ic.resize((76, 76), Image.LANCZOS); lay.alpha_composite(sm, (p + 62, y + 16))
        draw_text(d, p + 166, y + 52, a, 36, "extrabold", INK); draw_text(d, p + 166, y + 88, b, 26, "bold", MUTED)
        d.rounded_rectangle((p + w - 250, y + 32, p + w - 62, y + 78), 23, fill=BRAND); draw_text(d, p + w - 156, y + 63, "Apply  申请", 24, "extrabold", WH, "m")
    y = p + 150 + 3 * 130 + 10
    draw_text(d, p + 44, y + 40, "Agents  经纪人", 30, "extrabold", INK)
    for k in range(6):
        sm = (SMALLP if k % 2 else HIP)[0].resize((84, 84), Image.LANCZOS)
        d.ellipse((p + 44 + k * 66 - 3, y + 66 - 3, p + 44 + k * 66 + 87, y + 66 + 87), fill=(255, 255, 255))
        lay.alpha_composite(sm, (p + 44 + k * 66, y + 66))
    return lay, (p + w / 2, p + h / 2), p
MK, MKA, MKP = mkt_card()

def fmt(n): return f"¥{int(n):,}"
import re
def _n(w): return re.sub(r"[^a-z0-9.]", "", w.lower()).strip(".")
def tw(word, after=0.0, end=False):
    for w, s, e, i in P.WN:
        if s >= after - 1e-6 and _n(w) == _n(word): return e if end else s
    raise KeyError(word)
SC = [0, 4.0, 7.9, 11.6, 14.1, 17.8, 22.0, 25.7, 31.1, P.DUR + 1]
NS = len(SC) - 2
P.CAPEND = SC[8]
def scene_idx(t):
    k = 0
    for i, c in enumerate(SC[1:-1], 1):
        if t >= c: k = i
    return k
DUR = P.DUR
WHITE = (255, 255, 255); GOLD = (232, 176, 60); DRED = (150, 18, 18)

# ---------- photos ----------
_ph = {}
def photo(n):
    if n not in _ph: _ph[n] = Image.open(f"/home/claude/photos/p{n}.jpg").convert("RGB")
    return _ph[n]
def cover(n, w, h, zoom=1.0, px=0.5, py=0.5):
    im = photo(n); iw, ih = im.size
    s = max(w / iw, h / ih) * zoom
    cw, ch = w / s, h / s
    x0 = (iw - cw) * px; y0 = (ih - ch) * py
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
_mask = {}
def rmask(w, h, r):
    k = (w, h, r)
    if k not in _mask:
        m = Image.new("L", (w * 2, h * 2), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
        _mask[k] = m.resize((w, h), Image.LANCZOS)
    return _mask[k]
def photo_card(n, w, h, t, t0, zoom0=1.04, zoom1=1.16, px=0.5, py=0.5, r=44, border=14):
    """returns RGBA card with white border, shadow baked, Ken-Burns crop"""
    k = clamp((t - t0) / 3.0)
    ph = cover(n, w, h, zoom0 + (zoom1 - zoom0) * k, px, py).convert("RGBA")
    p = 50; lay = Image.new("RGBA", (w + 2 * border + 2 * p, h + 2 * border + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p + 16, p + w + 2 * border, p + h + 2 * border + 16), r + border, fill=(0, 0, 0, 70))
    lay = lay.filter(ImageFilter.GaussianBlur(16)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w + 2 * border, p + h + 2 * border), r + border, fill=WHITE)
    lay.paste(ph, (p + border, p + border), rmask(w, h, r))
    return lay, (lay.size[0] / 2, lay.size[1] / 2)
def circ_photo(n, d_, t, t0, ring=BRAND, rw=14):
    k = clamp((t - t0) / 3.0)
    ph = cover(n, d_, d_, 1.1 + 0.15 * k, 0.5, 0.55).convert("RGBA")
    m = Image.new("L", (d_ * 2, d_ * 2), 0); ImageDraw.Draw(m).ellipse((0, 0, d_ * 2 - 1, d_ * 2 - 1), fill=255); m = m.resize((d_, d_), Image.LANCZOS)
    lay = Image.new("RGBA", (d_ + 40, d_ + 40), (0, 0, 0, 0)); lay.paste(ph, (20, 20), m)
    return lay, ((d_ + 40) / 2, (d_ + 40) / 2)
def paste_xy(img, lay, anc, cx, cy, sx=1.0, sy=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003 or sx <= 0.01 or sy <= 0.01: return
    if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
        lay = lay.resize((max(1, int(lay.size[0] * sx)), max(1, int(lay.size[1] * sy))), Image.BILINEAR); anc = (anc[0] * sx, anc[1] * sy)
    paste_scaled(img, lay, anc, cx, cy, 1.0, alpha, rot)

# ---------- fun sticker mascot (Santa-hat 吗 bubble) ----------
def hatty(state="happy", k=3):
    W_, H_ = 330, 360; S = (W_ * k, H_ * k)
    body = Image.new("RGBA", S, (0, 0, 0, 0)); d = ImageDraw.Draw(body)
    bx0, by0, bx1, by1 = 40 * k, 100 * k, 290 * k, 290 * k
    d.rounded_rectangle((bx0, by0, bx1, by1), 70 * k, fill=BRAND)
    d.polygon([(70 * k, 270 * k), (60 * k, 340 * k), (140 * k, 285 * k)], fill=BRAND)
    # eyes
    ex = (125 * k, 205 * k); ey = 170 * k
    if state == "happy":
        for x in ex: d.arc((x - 26 * k, ey - 20 * k, x + 26 * k, ey + 24 * k), 200, 340, fill=WHITE, width=9 * k)
        d.pieslice((140 * k, 200 * k, 190 * k, 262 * k), 0, 180, fill=(120, 14, 14)); d.pieslice((152 * k, 232 * k, 178 * k, 262 * k), 0, 180, fill=(255, 140, 140))
    elif state == "wow":
        for x in ex:
            d.ellipse((x - 26 * k, ey - 28 * k, x + 26 * k, ey + 28 * k), fill=WHITE); d.ellipse((x - 11 * k, ey - 12 * k, x + 11 * k, ey + 12 * k), fill=INK)
        d.ellipse((152 * k, 214 * k, 178 * k, 252 * k), fill=(120, 14, 14))
    else:  # wink
        d.ellipse((ex[0] - 26 * k, ey - 28 * k, ex[0] + 26 * k, ey + 28 * k), fill=WHITE); d.ellipse((ex[0] - 11 * k, ey - 10 * k, ex[0] + 11 * k, ey + 14 * k), fill=INK)
        d.arc((ex[1] - 26 * k, ey - 10 * k, ex[1] + 26 * k, ey + 30 * k), 200, 340, fill=WHITE, width=9 * k)
        d.arc((130 * k, 205 * k, 200 * k, 250 * k), 10, 170, fill=WHITE, width=8 * k)
    t_, a_ = ctext("吗", 64, "extrabold", WHITE)
    # glyph tight-centred in lower body
    gl = t_.resize((int(t_.size[0] * k / 1.0 * 0.62), int(t_.size[1] * k * 0.62)), Image.LANCZOS)
    body.alpha_composite(gl, (int(165 * k - gl.size[0] / 2 + (0 if state != "happy" else 0)), int(268 * k - gl.size[1] / 2)))
    # santa hat
    hat = Image.new("RGBA", S, (0, 0, 0, 0)); hd = ImageDraw.Draw(hat)
    hd.polygon([(70 * k, 125 * k), (260 * k, 125 * k), (230 * k, 40 * k), (275 * k, 28 * k), (262 * k, 18 * k), (180 * k, 30 * k)], fill=DRED)
    hd.polygon([(70 * k, 125 * k), (260 * k, 125 * k), (215 * k, 38 * k), (150 * k, 40 * k)], fill=DRED)
    hd.rounded_rectangle((55 * k, 108 * k, 275 * k, 148 * k), 20 * k, fill=WHITE)
    hd.ellipse((240 * k, 4 * k, 292 * k, 56 * k), fill=WHITE)
    body.alpha_composite(hat)
    body = body.resize((W_, H_), Image.LANCZOS)
    a = body.getchannel("A"); out = a.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(1.2))
    lay = Image.new("RGBA", (W_ + 80, H_ + 80), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W_, H_), (0, 0, 0, 90)); sh.putalpha(out.point(lambda v: int(v * 0.35)))
    lay.paste(sh.filter(ImageFilter.GaussianBlur(10)), (40, 52), sh.filter(ImageFilter.GaussianBlur(10)))
    wh = Image.new("RGBA", (W_, H_), (255, 255, 255, 255)); wh.putalpha(out); lay.alpha_composite(wh, (40, 40)); lay.alpha_composite(body, (40, 40))
    return lay, ((W_ + 80) / 2, H_ + 60)
HAT = {s: hatty(s) for s in ("happy", "wow", "wink")}
def mascot(img, state, cx, cy, t, t0, sc=0.9, flip=False):
    if t < t0: return
    k = clamp((t - t0) / 0.45); e = out_back(k, 2.6)
    ph = t * 7.0
    sx = (1 - 0.05 * math.sin(ph)) * e * sc; sy = (1 + 0.06 * math.sin(ph)) * e * sc
    lay, anc = HAT[state]
    if flip: lay = lay.transpose(Image.FLIP_LEFT_RIGHT); anc = (lay.size[0] - anc[0], anc[1])
    paste_xy(img, lay, anc, cx, cy, sx, sy, min(1, k * 3), 5 * math.sin(t * 3.4 + t0))

def factory(col=INK, k=3, s=64):
    S = s * k; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((6 * k, 28 * k, 58 * k, 58 * k), fill=col)
    for i in range(3): d.polygon([(6 * k + i * 17 * k, 28 * k), (6 * k + i * 17 * k, 12 * k + 8 * k), (6 * k + (i + 1) * 17 * k, 28 * k)], fill=col)
    d.rectangle((44 * k, 4 * k, 54 * k, 28 * k), fill=col)
    for x in (14, 28, 42): d.rectangle((x * k, 40 * k, (x + 8) * k, 50 * k), fill=WHITE)
    im = im.resize((s, s), Image.LANCZOS); return im, (s / 2, s / 2)
FAC_D = factory((120, 112, 100)); FAC_R = factory(BRAND); FAC_I = factory(INK)

def stall(col, k=2, s=40):
    S = s * k; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((6 * k, 16 * k, 34 * k, 34 * k), fill=col)
    d.polygon([(2 * k, 16 * k), (38 * k, 16 * k), (32 * k, 6 * k), (8 * k, 6 * k)], fill=col)
    d.rectangle((10 * k, 22 * k, 30 * k, 30 * k), fill=WHITE)
    im = im.resize((s, s), Image.LANCZOS); return im, (s / 2, s / 2)
ST_R = stall(BRAND); ST_G = stall((190, 182, 170))

def confetti(img, t, t0, n=26, seed=5):
    if t < t0: return
    rnd = random.Random(seed); d = ImageDraw.Draw(img, "RGBA")
    for k in range(n):
        x0 = rnd.uniform(0, 1080); sp = rnd.uniform(60, 140); ph = rnd.uniform(0, 1920); r = rnd.uniform(5, 11); col = rnd.choice((BRAND, GOLD, (255, 255, 255), RLIGHT))
        y = (ph + (t - t0) * sp) % 2000 - 40; x = x0 + 30 * math.sin(t * 1.3 + k)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (170,))

def stamp_x(img, cx, cy, p, size=300, w=26):
    p = clamp(p)
    if p <= 0: return
    d = ImageDraw.Draw(img, "RGBA"); h = size / 2
    a = clamp(p * 2); b = clamp(p * 2 - 1)
    d.line((cx - h, cy - h, cx - h + size * a, cy - h + size * a), fill=BRAND + (255,), width=w)
    if b > 0: d.line((cx + h, cy - h, cx + h - size * b, cy - h + size * b), fill=BRAND + (255,), width=w)

def ring_chart(img, cx, cy, r, prog, w=60):
    k = 2; S = int(2 * r + 2 * w + 20)
    lay = Image.new("RGBA", (S * k, S * k), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = S * k / 2
    d.arc((c - r * k, c - r * k, c + r * k, c + r * k), 0, 360, fill=(226, 222, 216, 255), width=w * k)
    if prog > 0: d.arc((c - r * k, c - r * k, c + r * k, c + r * k), -90, -90 + 360 * prog, fill=BRAND + (255,), width=w * k)
    lay = lay.resize((S, S), Image.LANCZOS); img.paste(lay, (int(cx - S / 2), int(cy - S / 2)), lay)

# timeline anchors
T_Q = tw("question"); T_WHERE = tw("Where"); T_NOT = tw("Not"); T_POLE = tw("Pole.", end=True)
T_CITY = tw("city"); T_YIWU = tw("Yiwu."); T_60 = tw("60"); T_DECO = tw("decorations.", end=True)
T_600 = tw("600"); T_FACT = tw("factories,"); T_BUY = tw("buyers"); T_ALL = tw("all."); T_ONE = tw("one", T_ALL); T_MARKET = tw("market.")
T_75 = tw("75000"); T_STALLS = tw("stalls."); T_EVERY = tw("Everything"); T_PLACE = tw("place.")
T_FUNNY = tw("Funny,"); T_FIND = tw("Finding"); T_DIFF = tw("different."); T_NOT2 = tw("Not", T_DIFF); T_10 = tw("10"); T_WE = tw("WeChat"); T_ONE2 = tw("one", T_WE)
T_MP = tw("marketplace."); T_EVERYJ = tw("Every"); T_JOB = tw("job,"); T_AGENT = tw("agent."); T_WELCOME = tw("Welcome"); T_URL = tw("laowai.ma")
CTA3 = P.cta("Welcome to laowai.ma")

def cap_plate(img, Lc, Ac, cy=1630):
    bb = Lc.getchannel("A").getbbox()
    if not bb: return
    d = ImageDraw.Draw(img, "RGBA")
    x0 = 540 - Ac[0] + bb[0] - 34; x1 = 540 - Ac[0] + bb[2] + 34; y0 = cy - Ac[1] + bb[1] - 16; y1 = cy - Ac[1] + bb[3] + 16
    d.rounded_rectangle((x0, y0, x1, y1), 40, fill=(255, 255, 255, 225))

MINI_G = []
def mini_group(name, k):
    w, h = 440, 120; lay, d, p = P.card_shadow(w, h, 32)
    ic, ia = ICON["case"]; sm = ic.resize((68, 68), Image.LANCZOS); lay.alpha_composite(sm, (p + 20, p + 26))
    draw_text(d, p + 108, p + 56, name, 25, "extrabold", INK)
    d.rounded_rectangle((p + 108, p + 72, p + 108 + 170, p + 92), 10, fill=(226, 222, 216))
    d.ellipse((p + w - 62, p + 22, p + w - 22, p + 62), fill=BRAND); draw_text(d, p + w - 42, p + 52, str(k), 24, "extrabold", WHITE, "m")
    return lay, (p + w / 2, p + h / 2)
GN = ["Shanghai Casting", "Beijing Shoots", "Shenzhen Hosts", "Chengdu Models", "Hangzhou Jobs", "Guangzhou Ads", "Expat Work CN", "Teach in China", "Voice Actors", "Event Staff"]
MINI_G = [mini_group(n, 1 + (i * 7) % 12) for i, n in enumerate(GN)]
MG_POS = [(290 + (i % 2) * 500, 470 + (i // 2) * 150) for i in range(10)]

def frame(i):
    t = i / FPS
    s = scene_idx(t); ts = SC[s]
    img = P.BG.copy(); V.bg_motion(img, t)
    if s == 0:
        k = clamp(t / 4.0)
        bg = cover(14632569, W, H, 1.02 + 0.10 * k, 0.5, 0.5).convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for y in range(H):
            a = int(210 * max(0, (y - 700) / 1220) ** 1.2) + 20; od.line((0, y, W, y), fill=(120, 10, 10, min(235, a)))
        bg.alpha_composite(ov); img.paste(bg.convert("RGB"), (0, 0))
        q = clamp((t - 0.05) / 0.25)
        chip = pill_text = None
        if t >= 0.05:
            L, A = wl("QUICK QUESTION  快问快答", 38, "mono", WHITE); d = ImageDraw.Draw(img, "RGBA")
            d.rounded_rectangle((540 - text_w("QUICK QUESTION  快问快答", 38, "mono") / 2 - 36, 300, 540 + text_w("QUICK QUESTION  快问快答", 38, "mono") / 2 + 36, 372), 36, fill=BRAND + (255,))
            paste_scaled(img, L, A, 540, 350, pop(t, 0.05, 0.25), 1)
        typed(img, t, [("Where does", "extrabold", WHITE, 1.0)], 104, 540, 1060, T_WHERE, 32)
        typed(img, t, [("Christmas", "extrabold", WHITE, 1.0)], 124, 540, 1190, tw("Christmas"), 32)
        typed(img, t, [("come from?", "serif", (255, 214, 208), 1.0)], 124, 540, 1320, tw("come"), 32)
        zh(img, "圣诞节，是从哪来的？", 540, 1410, t, T_WHERE + 0.5, 46, (255, 232, 228), "extrabold")
        mascot(img, "wow", 880, 900, t, tw("from?") - 0.3, 0.8)
    elif s == 1:
        V.glow(img, 540, 900, t, ts, 1.8, 0.5); confetti(img, t, ts)
        if t < T_CITY - 0.1:
            k = pop(t, ts + 0.05, 0.35)
            L, A = photo_card(6102434, 620, 780, t, ts, 1.0, 1.1, 0.5, 0.45)
            paste_scaled(img, L, A, 540, 840, k, min(1, (t - ts) / 0.1), rot=-4)
            typed(img, t, [S_("Not the ", INK), SE_("North Pole.", BRAND, 1.2)], 92, 540, 330, T_NOT, 30)
            if t >= T_NOT + 0.25: stamp_x(img, 540, 840, (t - T_NOT - 0.25) / 0.35, 360, 30)
            zh(img, "不是北极", 540, 1330, t, T_NOT + 0.4, 46)
        else:
            q = clamp((t - T_CITY + 0.1) / 0.3)
            L, A = photo_card(15555090, 940, 640, t, T_CITY, 1.0, 1.15, 0.5, 0.5)
            paste_scaled(img, L, A, 540, 700, pop(t, T_CITY - 0.1, 0.35), q, rot=2)
            typed(img, t, [S_("A city in ", INK, 0.85), SE_("China", BRAND, 1.2)], 84, 540, 330, T_CITY, 30)
            if t >= T_YIWU - 0.1:
                V.glow(img, 540, 1190, t, T_YIWU - 0.1, 1.5, 0.9)
                L2, A2 = ctext("YIWU 义乌", 150, "extrabold", BRAND)
                paste_scaled(img, L2, A2, 540, 1220, pop(t, T_YIWU - 0.1, 0.35), 1)
                ic, ia = ICON["pin"]; paste_scaled(img, ic, ia, 840, 960, pop(t, T_YIWU + 0.1, 0.3), 1)
        mascot(img, "happy", 900, 1530, t, T_YIWU + 0.3, 0.7, True) if t > T_YIWU else None
    elif s == 2:
        V.glow(img, 540, 800, t, ts, 1.8, 0.6); confetti(img, t, ts, 30, 9)
        typed(img, t, [S_("It makes ", INK, 0.85), SE_("about", BRAND, 1.2)], 84, 540, 330, T_60 - 0.7, 30)
        pr = out_cubic(clamp((t - T_60) / 0.9)) * 0.6
        ring_chart(img, 540, 860, 270, pr, 70)
        L, A = circ_photo(279128, 440, t, ts)
        paste_scaled(img, L, A, 540, 860, pop(t, ts + 0.1, 0.4), 1)
        val = int(round(60 * out_cubic(clamp((t - T_60) / 0.9))))
        if t >= T_60 - 0.05:
            L2, A2 = ctext(f"{val}%", 200, "extrabold", WHITE)
            Lo, Ao = ctext(f"{val}%", 200, "extrabold", BRAND)
            paste_scaled(img, Lo, Ao, 540, 860, 1.06, 0.55); paste_scaled(img, L2, A2, 540, 860, 1.0 + 0.08 * math.sin(clamp((t - T_60 - 0.9) / 0.3) * math.pi), 1)
        typed(img, t, [S_("of the world's", INK, 0.85)], 72, 540, 1290, tw("world's"), 30)
        typed(img, t, [SE_("Christmas decorations.", BRAND, 1.15)], 78, 540, 1380, tw("Christmas", T_60), 30)
        zh(img, "全球约六成的圣诞装饰", 540, 1465, t, tw("world's") + 0.2, 44)
        mascot(img, "wow", 925, 1235, t, T_60 + 0.2, 0.7, True)
    elif s == 3:
        V.glow(img, 540, 780, t, ts, 1.8, 0.6)
        L, A = photo_card(16765239, 940, 560, t, ts, 1.0, 1.18, 0.5, 0.5)
        paste_scaled(img, L, A, 540, 520, pop(t, ts + 0.05, 0.35), min(1, (t - ts) / 0.1), rot=-2)
        typed(img, t, [S_("Over", INK, 0.8)], 70, 540, 965, tw("Over"), 30)
        val = int(round(600 * out_cubic(clamp((t - T_600) / 0.9)))) if t >= T_600 else 0
        if t >= T_600 - 0.05:
            L2, A2 = ctext(f"{val}+", 230, "extrabold", BRAND); paste_scaled(img, L2, A2, 540, 1120, 1.0 + 0.08 * math.sin(clamp((t - T_600 - 0.9) / 0.3) * math.pi), 1)
        if t >= T_FACT - 0.1:
            typed(img, t, [SE_("factories", INK, 1.2)], 92, 540, 1305, T_FACT - 0.05, 30)
            zh(img, "工厂", 540, 1385, t, T_FACT + 0.1, 46)
        for j in range(12):
            c0 = T_600 + 0.2 + j * 0.06
            if t >= c0:
                x = 150 + (j % 6) * 156; y = 1470 + (j // 6) * 70
                paste_scaled(img, FAC_R[0], FAC_R[1], x, y, pop(t, c0, 0.25), 1)
    elif s == 4:
        V.glow(img, 540, 900, t, ts, 1.6, 0.5)
        typed(img, t, [S_("But buyers ", INK, 0.85), SE_("don't", BRAND, 1.2)], 86, 540, 300, T_BUY - 0.1, 30)
        for j in range(12):
            x = 140 + (j % 6) * 160; y = 480 + (j // 6) * 110
            c0 = ts + 0.15 + j * 0.03
            if t >= c0: paste_scaled(img, FAC_D[0], FAC_D[1], x, y, pop(t, c0, 0.25), 0.9)
        typed(img, t, [S_("visit them all.", INK, 0.85)], 80, 540, 760, tw("visit"), 30)
        if t >= T_ALL - 0.1: stamp_x(img, 540, 545, (t - T_ALL + 0.1) / 0.35, 260, 26)
        if t >= T_ONE - 0.15:
            L, A = photo_card(28699440, 880, 470, t, T_ONE - 0.15, 1.0, 1.15, 0.5, 0.5)
            paste_scaled(img, L, A, 540, 1130, pop(t, T_ONE - 0.15, 0.4), min(1, (t - T_ONE + 0.15) / 0.1), rot=-2)
            V.glow(img, 540, 1130, t, T_ONE - 0.15, 1.2, 0.5)
            L2, A2 = ctext("ONE MARKET  一个市场", 52, "extrabold", WHITE); d = ImageDraw.Draw(img, "RGBA")
            wtxt = text_w("ONE MARKET  一个市场", 52, "extrabold"); pp = pop(t, T_ONE, 0.3)
            d.rounded_rectangle((540 - wtxt / 2 - 36, 1325, 540 + wtxt / 2 + 36, 1405), 40, fill=BRAND + (255,))
            paste_scaled(img, L2, A2, 540, 1365, pp, 1)
        mascot(img, "happy", 930, 935, t, T_ONE, 0.6, True) if t > T_ONE else None
    elif s == 5:
        V.glow(img, 540, 760, t, ts, 1.8, 0.6); confetti(img, t, ts, 22, 3)
        L, A = photo_card(28699440, 940, 500, t, ts, 1.0, 1.15, 0.5, 0.45)
        paste_scaled(img, L, A, 540, 500, pop(t, ts + 0.05, 0.35), min(1, (t - ts) / 0.1), rot=1.5)
        val = int(round(75000 * out_cubic(clamp((t - T_75) / 1.0)))) if t >= T_75 else 0
        if t >= T_75 - 0.05:
            L2, A2 = ctext(f"{val:,}", 200, "extrabold", BRAND); paste_scaled(img, L2, A2, 540, 900, 1.0 + 0.07 * math.sin(clamp((t - T_75 - 1.0) / 0.3) * math.pi), 1)
        if t >= T_STALLS - 0.2:
            typed(img, t, [SE_("stalls", INK, 1.2)], 96, 540, 1075, T_STALLS - 0.15, 30); zh(img, "个摊位", 540, 1145, t, T_STALLS, 44)
        cols = 14
        for j in range(42):
            c0 = T_75 + 0.1 + j * 0.03
            if t >= c0:
                x = 540 + ((j % cols) - (cols - 1) / 2) * 62; y = 1235 + (j // cols) * 56
                paste_scaled(img, (ST_R if j % 4 else ST_G)[0], (ST_R if j % 4 else ST_G)[1], x, y, pop(t, c0, 0.22), 1)
        if t >= T_EVERY - 0.05:
            typed(img, t, [S_("Everything in ", INK, 0.82), SE_("one place.", BRAND, 1.2)], 78, 540, 1455, T_EVERY, 30)
        mascot(img, "wow", 160, 335, t, T_75 + 0.2, 0.65)
    elif s == 6:
        V.glow(img, 540, 800, t, ts, 1.8, 0.5)
        typed(img, t, [S_("Funny, right?", INK, 1.0)], 98, 540, 300, T_FUNNY, 30)
        typed(img, t, [S_("Work in ", INK, 0.9), SE_("China?", BRAND, 1.3)], 108, 540, 430, T_FIND, 30)
        for j, (name, (x, y)) in enumerate(zip(GN, MG_POS[:6])):
            c0 = T_FIND + j * 0.12
            if t >= c0:
                Lg, Ag = MINI_G[j]; bob = 6 * math.sin(t * 2.2 + j)
                paste_scaled(img, Lg, Ag, x + (-1) ** j * 20, y + 420 + bob, pop(t, c0, 0.3), 1, rot=(-1) ** j * 3)
        zh(img, "找工作，也该这样", 540, 1430, t, T_DIFF - 0.3, 46)
        mascot(img, "wink", 900, 1500, t, T_DIFF, 0.65, True)
    elif s == 7:
        V.glow(img, 540, 860, t, ts, 1.8, 0.6)
        if t < T_ONE2 - 0.05:
            typed(img, t, [S_("Not ", INK, 1.0), SE_("10", BRAND, 1.3), S_(" WeChat groups", INK, 1.0)], 76, 540, 300, T_NOT2, 30)
            for j in range(10):
                c0 = ts + 0.1 + j * 0.06
                if t >= c0:
                    x, y = MG_POS[j]; Lg, Ag = MINI_G[j]
                    paste_scaled(img, Lg, Ag, x, y + 300 + 5 * math.sin(t * 2 + j), pop(t, c0, 0.25) * 0.82, 1, rot=(-1) ** j * 2)
            if t >= T_10: stamp_x(img, 540, 760, (t - T_10) / 0.4, 760, 26)
        else:
            q = clamp((t - T_ONE2 + 0.05) / 0.5)
            typed(img, t, [SE_("One ", BRAND, 1.2), S_("marketplace.", INK, 1.0)], 100, 540, 300, T_ONE2, 30)
            # groups fly into the card
            for j in range(10):
                x, y = MG_POS[j]; Lg, Ag = MINI_G[j]; e = out_cubic(clamp(q * 1.4 - j * 0.04))
                if e < 1: paste_scaled(img, Lg, Ag, x + (540 - x) * e, y + 300 + (900 - y - 300) * e, 0.82 * (1 - 0.5 * e), 1 - e)
            k2 = clamp((t - T_ONE2 - 0.25) / 0.4)
            if k2 > 0:
                V.glow(img, 540, 900, t, T_ONE2 + 0.25, 1.8, 0.8)
                paste_scaled(img, MK, MKA, 540, 880, 0.9 * out_back(k2, 2.0) * (1 + 0.008 * math.sin(t * 1.5)), min(1, k2 * 3))
            if t >= T_EVERYJ:
                L, A = pill("Every job", "所有机会", "case", True); V.blur_in(img, L, A, 290, 1400, t, T_EVERYJ, 0.22)
            if t >= tw("every", T_EVERYJ + 0.1) - 0.05:
                L, A = pill("Every agent", "所有经纪人", "person", False); V.blur_in(img, L, A, 790, 1400, t, tw("every", T_EVERYJ + 0.1) - 0.05, 0.22)
            zh(img, "一个平台，全都有", 540, 410, t, T_ONE2 + 0.2, 42)
            mascot(img, "happy", 935, 375, t, T_MP, 0.55, True)
    else:
        V.glow(img, 540, 460, t, ts, 1.5, 0.7)
        V.scramble(img, t, "laowai吗", 150, 540, 470, ts + 0.02, 0.06, cols={6})
        sp = ENV[min(i, len(ENV) - 1)]
        mouth = "big" if sp > 0.12 else ("o" if sp > 0.05 else "smile")
        R.lay_at(img, R.masc(mouth, (0, 0), blink=(t % 2.3) < 0.1), R.MA, 540, 790 - 6 * math.sin(t * 6), t, ts + 0.2, 0.35, sc=0.8)
        typed(img, t, [S_("Foreign talent. Chinese agents.", MUTED, 0.38)], 90, 540, 1060, ts + 0.5, 34)
        zh(img, "外国人才 · 中国经纪人", 540, 1120, t, ts + 0.9, 34, GREY)
        typed(img, t, [S_("laowai.ma", INK, 1.0)], 112, 540, 1300, T_URL, 18)
        if t >= T_URL + 0.7: V.ellipse_draw(img, 540, 1263, 340, 92, (t - T_URL - 0.7) / 0.35)
        if t >= T_WELCOME: R.lay_at(img, CTA3[0], CTA3[1], 540, 1480, t, T_WELCOME, 0.3)
        mascot(img, "happy", 950, 1390, t, T_URL, 0.5, True)
    img = whip(img, t, i)
    te = SC[s + 1]; p = clamp((t - ts) / max(0.5, min(te, P.DUR) - ts))
    img = camera(img, zoom=1.0 + 0.04 * p)
    if t < SC[8] and not (s == 0 and t < 0.35):
        for gi, g in enumerate(P.GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.2:
                ai = 0
                for k, (w, s2, e) in enumerate(g):
                    if t >= s2 - 0.02: ai = k
                Lc, Ac = P.CAPS[(gi, ai)]
                cap_plate(img, Lc, Ac, 1650)
                paste_scaled(img, Lc, Ac, 540, 1650, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06))
                break
    fade = clamp((P.DUR - t) / 0.3) if t > P.DUR - 0.3 else 1.0
    return post(img, i, glitch=0.0, grain=0.22, vignette=0.0, fade=fade)

def jingle(g=1.0):
    out = np.zeros(int(0.7 * SR))
    for k, f in enumerate((2637, 3136, 3951, 3136, 4186)):
        n = int(0.32 * SR); tt = np.arange(n) / SR; o = k * int(0.055 * SR)
        out[o:o + n] += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt / 0.09) * 0.16
    return out * g

def build_audio(path):
    m = Mix(DUR)
    x = vo / (np.max(np.abs(vo)) + 1e-9) * 0.82
    voice = np.zeros(m.n); voice[:min(len(x), m.n)] = x[:m.n]
    bed = Mix(DUR)
    for c in SC[1:-1]:
        bed.add(c - 0.16, V.swoosh(0.34), 0.8); bed.add(c + 0.02, V.thump(), 0.45)
    bed.add(0.0, V.swoosh(0.4), 0.7); bed.add(0.08, V.blip(380, 900), 0.6)
    bed.add(T_WHERE, V.thump(), 0.5)
    bed.add(T_NOT + 0.25, V.swoosh(0.3), 0.7); bed.add(T_NOT + 0.6, buzz(0.18), 0.12)
    bed.add(T_YIWU - 0.1, V.thump(), 0.8); bed.add(T_YIWU - 0.1, jingle(), 0.9)
    bed.add(T_60 - 0.1, riser(1.0), 0.2); bed.add(T_60 + 0.9, V.thump(), 0.7); bed.add(T_60 + 0.9, V.sparkle(), 0.6)
    bed.add(T_600 - 0.05, riser(1.0), 0.2); bed.add(T_600 + 0.9, V.thump(), 0.7)
    bed.add(T_ALL - 0.1, V.thump(), 0.6); bed.add(T_ALL, V.swoosh(0.3), 0.5)
    bed.add(T_ONE - 0.15, V.blip(380, 900), 0.7); bed.add(T_ONE - 0.15, V.thump(), 0.5); bed.add(T_ONE, jingle(), 0.8)
    bed.add(T_75 - 0.05, riser(1.0), 0.2); bed.add(T_75 + 1.0, V.thump(), 0.7); bed.add(T_75 + 1.0, V.sparkle(), 0.55)
    bed.add(T_EVERY, V.blip(420, 980), 0.5)
    for j in range(6): bed.add(T_FIND + j * 0.12, V.blip(300 + 40 * j, 600 + 40 * j), 0.28)
    bed.add(T_10, buzz(0.2), 0.12); bed.add(T_10, V.thump(), 0.5)
    bed.add(T_ONE2, V.swoosh(0.45), 0.8); bed.add(T_ONE2 + 0.3, V.thump(), 0.7); bed.add(T_ONE2 + 0.3, jingle(), 0.9)
    for t0 in (T_EVERYJ, tw("every", T_EVERYJ + 0.1)): bed.add(t0, V.blip(400, 950), 0.6)
    for tt, f in ((SC[8], 330), (SC[8] + 0.4, 392), (SC[8] + 0.8, 494), (SC[8] + 1.2, 659)): bed.add(tt, pluck(f), 0.38)
    bed.add(T_WELCOME, V.blip(400, 1000), 0.6); bed.add(T_URL + 0.7, V.swoosh(0.4), 0.6); bed.add(T_URL + 1.1, V.sparkle(), 0.6)
    b = hp(bed.buf.copy(), 40)
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
    b = b * (1 - 0.45 * np.clip(env / 0.08, 0, 1)) * 0.75
    y = voice + b
    y = np.tanh(y * 1.1) / np.tanh(1.1); y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    n = int(0.3 * SR); y[-n:] *= np.linspace(1, 0, n)
    write_wav(path, y)

if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]: Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/v6still_{tt}.png")
    elif sys.argv[1] == "audio": build_audio("out/reel06.wav")
    else:
        build_audio("out/reel06.wav")
        render(frame, int(DUR * FPS), "out/reel06.wav", "out/laowai_reel_06.mp4")
