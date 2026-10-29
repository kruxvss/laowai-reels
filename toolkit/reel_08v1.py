"""Reel 05 v1 (from 04v3 helpers) - WOW fact: 88888888 phone number sold for 2.33M yuan. Inspo motion language, FASTER, no repeating typing/tick sounds, icons centred by bbox."""
import sys, math, random
sys.path.insert(0, "/home/claude/reels")
import reel_08base as P
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

import re
from premium import *
def pop(t, t0, d=0.28): return out_back(clamp((t - t0) / d), 2.2)
def _n(w): return re.sub(r"[^a-z0-9]", "", w.lower())
def tw(word, after=0.0, end=False):
    for w, s, e, i in P.WN:
        if s >= after - 1e-6 and _n(w) == _n(word): return e if end else s
    raise KeyError(word)
WHITE = (255, 255, 255); INKD = (16, 13, 11); DRED = (150, 18, 18)

# ---- anchors (spoken words) ----
T_JOKE = tw("joke"); T_ONE = tw("One"); T_TRILL = tw("trillion"); T_YUAN = tw("yuan"); T_HOW = tw("How")
T_NINE = tw("nineties"); T_NAN = tw("Nanjing"); T_ELEV = tw("Eleven"); T_4ONES = tw("ones"); T_LONELY = tw("lonely")
T_2009 = tw("thousand"); T_27 = tw("twentyseven"); T_50 = tw("fifty"); T_LAST = tw("Last", T_50)
T_TRILL2 = tw("trillion", T_LAST); T_FACES = tw("faces"); T_HOSTS = tw("Hosts"); T_MODELS = tw("Models"); T_ADS = tw("Ads")
T_IF = tw("If"); T_WORK = tw("work"); T_HARD = tw("hard"); T_FIND = tw("finding")
T_SO = tw("So"); T_EVJOB = tw("every"); T_EVAG = tw("every", T_EVJOB + 0.2); T_PLACE = tw("place"); T_ONEM = tw("One", T_PLACE); T_MARKET = tw("marketplace"); T_WELCOME = tw("Welcome"); T_URL = tw("laowaima")
SC = [0, T_NINE - 0.15, T_2009 - 0.3, T_LAST - 0.2, T_FACES - 0.3, T_IF - 0.2, T_SO - 0.15, T_WELCOME - 0.1, P.DUR + 1]
NS = len(SC) - 2
P.CAPEND = SC[7]
def scene_idx(t):
    k = 0
    for i, c in enumerate(SC[1:-1], 1):
        if t >= c: k = i
    return k
DUR = P.DUR
DARK = {0, 3}

def stage(s): return s

# ---------- backgrounds ----------
def dark_bg(t, seed=0, hot=(540, 820)):
    img = Image.new("RGB", (W, H), INKD)
    spotlight(img, hot[0] + 60 * math.sin(t * 0.7 + seed), hot[1] + 50 * math.cos(t * 0.5), 1100, (214, 34, 30), 0.85)
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(34):
        r = random.Random(k + seed * 50); x = r.uniform(0, W); y = (r.uniform(0, H) - t * r.uniform(8, 30)) % H; rr = r.uniform(1.5, 4.5)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 255, 255, int(r.uniform(25, 80))))
    return img

# ---------- characters: the lonely "1" ----------
def one_char(look=0.0, mood="flat", blink=False, col=BRAND, k=3):
    w, h = 220, 400; S = (w * k, h * k)
    im = Image.new("RGBA", S, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((70 * k, 40 * k, 160 * k, 340 * k), 45 * k, fill=col)
    d.polygon([(70 * k, 100 * k), (70 * k, 52 * k), (28 * k, 128 * k), (28 * k, 170 * k)], fill=col)
    d.rounded_rectangle((26 * k, 120 * k, 95 * k, 175 * k), 22 * k, fill=col)
    # feet
    d.rounded_rectangle((72 * k, 332 * k, 112 * k, 358 * k), 13 * k, fill=INK); d.rounded_rectangle((118 * k, 332 * k, 158 * k, 358 * k), 13 * k, fill=INK)
    ex = (97 * k, 135 * k); ey = 120 * k; ox = look * 8 * k
    for x in ex:
        if blink: d.rounded_rectangle((x - 17 * k, ey - 2 * k, x + 17 * k, ey + 3 * k), 3 * k, fill=WHITE)
        else:
            d.ellipse((x - 18 * k, ey - 20 * k, x + 18 * k, ey + 20 * k), fill=WHITE); d.ellipse((x - 7 * k + ox, ey - 9 * k, x + 9 * k + ox, ey + 9 * k), fill=INK)
    my = 175 * k
    if mood == "sad": d.arc((100 * k, my, 134 * k, my + 24 * k), 200, 340, fill=WHITE, width=5 * k)
    else: d.line((104 * k, my + 8 * k, 130 * k, my + 8 * k), fill=WHITE, width=5 * k)
    im = im.resize((w, h), Image.LANCZOS)
    lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.25)))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (30, 40)); lay.alpha_composite(im, (30, 30))
    return lay, (30 + 112, 30 + 358)
CHARS = {(m, b): one_char(0, m, b) for m in ("flat", "sad") for b in (False, True)}
CH_LOOK = {}
def char(look, mood, blink):
    key = (round(look, 1), mood, blink)
    if key not in CH_LOOK: CH_LOOK[key] = one_char(look, mood, blink)
    return CH_LOOK[key]

def shop(col, s=64, k=3):
    S = s * k; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10 * k, 30 * k, 54 * k, 58 * k), 5 * k, fill=(250, 244, 238), outline=col, width=3 * k)
    for j in range(5): d.rectangle((6 * k + j * 10.4 * k, 12 * k, 6 * k + (j + 1) * 10.4 * k, 32 * k), fill=col if j % 2 == 0 else WHITE)
    d.rectangle((6 * k, 12 * k, 58 * k, 32 * k), outline=col, width=2 * k)
    d.rounded_rectangle((26 * k, 40 * k, 38 * k, 58 * k), 3 * k, fill=col)
    return im.resize((s, s), Image.LANCZOS), (s / 2, s / 2)
SHOP = shop(BRAND)

# ---------- dorm illustration ----------
def dorm_card(w=940, h=620):
    lay, d, p = P.card_shadow(w, h, 48)
    d.rounded_rectangle((p + 14, p + 14, p + w - 14, p + h - 14), 38, fill=(247, 240, 230))
    d.rectangle((p + 14, p + h - 170, p + w - 14, p + h - 14), fill=(226, 208, 184))
    d.rounded_rectangle((p + w / 2 - 150, p + 60, p + w / 2 + 150, p + 250), 18, fill=(255, 255, 255), outline=(196, 188, 176), width=8)
    d.rectangle((p + w / 2 - 146, p + 64, p + w / 2 + 146, p + 150), fill=(160, 196, 226)); d.rectangle((p + w / 2 - 146, p + 150, p + w / 2 + 146, p + 246), fill=(26, 38, 70))
    d.line((p + w / 2, p + 60, p + w / 2, p + 250), fill=(196, 188, 176), width=8)
    for (x, y) in ((-110, 190), (-30, 215), (70, 180), (115, 220)): d.ellipse((p + w / 2 + x - 4, p + y - 4, p + w / 2 + x + 4, p + y + 4), fill=(255, 238, 190))
    d.ellipse((p + w / 2 + 60, p + 150 - 60, p + w / 2 + 110, p + 150 - 10), fill=(255, 236, 170))
    for bx in (p + 50, p + w - 50 - 130):
        d.rounded_rectangle((bx, p + 130, bx + 130, p + h - 40), 14, outline=(150, 112, 80), width=10)
        d.rectangle((bx, p + 250, bx + 130, p + 280), fill=(196, 28, 28) if bx < p + 100 else (90, 120, 170)); d.rectangle((bx, p + 410, bx + 130, p + 440), fill=(250, 250, 250))
    return lay, (p + w / 2, p + h / 2), p
DORM, DORMA, DORMP = dorm_card()

# ---------- phone (live commerce) ----------
def phone_layer(t, w=520, h=980):
    lay, d, p = P.card_shadow(w, h, 74)
    d.rounded_rectangle((p + 14, p + 14, p + w - 14, p + h - 14), 62, fill=(40, 28, 32))
    sx0, sy0, sx1, sy1 = p + 34, p + 34, p + w - 34, p + h - 34
    scr = Image.new("RGBA", (sx1 - sx0, sy1 - sy0), (0, 0, 0, 0)); sd = ImageDraw.Draw(scr); sw, sh_ = scr.size
    for y in range(sh_):
        k = y / sh_; sd.line((0, y, sw, y), fill=(int(250 - 24 * k), int(214 - 70 * k), int(206 - 70 * k), 255))
    # host
    cx = sw / 2; sd.ellipse((cx - 150, sh_ * 0.48, cx + 150, sh_ * 0.48 + 520), fill=(52, 38, 52))
    sd.ellipse((cx - 62, sh_ * 0.27, cx + 62, sh_ * 0.27 + 150), fill=(246, 206, 174))
    sd.pieslice((cx - 78, sh_ * 0.245, cx + 78, sh_ * 0.245 + 150), 180, 360, fill=(54, 36, 30)); sd.rectangle((cx - 78, sh_ * 0.245 + 74, cx - 58, sh_ * 0.245 + 190), fill=(54, 36, 30)); sd.rectangle((cx + 58, sh_ * 0.245 + 74, cx + 78, sh_ * 0.245 + 190), fill=(54, 36, 30))
    sd.ellipse((cx - 36, sh_ * 0.27 + 62, cx - 22, sh_ * 0.27 + 76), fill=INK); sd.ellipse((cx + 22, sh_ * 0.27 + 62, cx + 36, sh_ * 0.27 + 76), fill=INK)
    sd.arc((cx - 24, sh_ * 0.27 + 86, cx + 24, sh_ * 0.27 + 120), 20, 160, fill=(196, 60, 60), width=6)
    sd.rounded_rectangle((16, 22, 120, 66), 22, fill=BRAND); draw_text(sd, 68, 55, "LIVE", 28, "extrabold", WHITE, "m")
    sd.rounded_rectangle((sw - 190, 22, sw - 16, 66), 22, fill=(0, 0, 0, 120)); draw_text(sd, sw - 103, 54, f"{12400 + int(t * 37):,}", 26, "bold", WHITE, "m")
    sd.rounded_rectangle((16, sh_ - 190, sw - 16, sh_ - 20), 30, fill=(255, 255, 255, 245))
    sd.rounded_rectangle((34, sh_ - 172, 34 + 134, sh_ - 38), 22, fill=(238, 224, 214)); sd.ellipse((70, sh_ - 140, 134, sh_ - 76), fill=BRAND)
    draw_text(sd, 186, sh_ - 112, "11.11 deal", 28, "extrabold", INK); draw_text(sd, 186, sh_ - 66, "¥99", 40, "extrabold", BRAND)
    sd.rounded_rectangle((sw - 150, sh_ - 124, sw - 30, sh_ - 56), 34, fill=BRAND); draw_text(sd, sw - 90, sh_ - 80, "Buy", 30, "extrabold", WHITE, "m")
    m = Image.new("L", scr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh_ - 1), 48, fill=255)
    lay.paste(scr, (sx0, sy0), m)
    return lay, (p + w / 2, p + h / 2)

def heart(img, x, y, sc, a, col=BRAND):
    d = ImageDraw.Draw(img, "RGBA"); r = 16 * sc
    d.ellipse((x - 2 * r, y - r * 1.6, x, y + r * 0.4), fill=col + (a,)); d.ellipse((x, y - r * 1.6, x + 2 * r, y + r * 0.4), fill=col + (a,))
    d.polygon([(x - 1.9 * r, y - r * 0.2), (x + 1.9 * r, y - r * 0.2), (x, y + 2.0 * r)], fill=col + (a,))

# ---------- misc cards ----------
def cap_plate(img, Lc, Ac, cy=1650, dark=False):
    bb = Lc.getchannel("A").getbbox()
    if not bb: return
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((540 - Ac[0] + bb[0] - 34, cy - Ac[1] + bb[1] - 16, 540 - Ac[0] + bb[2] + 34, cy - Ac[1] + bb[3] + 16), 40, fill=(255, 255, 255, 235))
def mini_group(name, k):
    w, h = 440, 120; lay, d, p = P.card_shadow(w, h, 32)
    ic, ia = ICON["case"]; lay.alpha_composite(ic.resize((68, 68), Image.LANCZOS), (p + 20, p + 26))
    draw_text(d, p + 108, p + 56, name, 25, "extrabold", INK); d.rounded_rectangle((p + 108, p + 72, p + 278, p + 92), 10, fill=(226, 222, 216))
    d.ellipse((p + w - 62, p + 22, p + w - 22, p + 62), fill=BRAND); draw_text(d, p + w - 42, p + 52, str(k), 24, "extrabold", WHITE, "m")
    return lay, (p + w / 2, p + h / 2)
GN = ["Shanghai Casting", "Beijing Shoots", "Shenzhen Hosts", "Chengdu Models", "Hangzhou Jobs", "Guangzhou Ads", "Expat Work CN", "Teach in China", "Voice Actors", "Event Staff", "Live Hosts", "Extras Call"]
MG = [mini_group(n, 1 + (i * 7) % 12) for i, n in enumerate(GN)]
CTA3 = P.cta("Welcome to laowai.ma")

def glass_pill(img, txt, cx, cy, t, t0, col=BRAND, size=44, tc=WHITE):
    k = pop(t, t0, 0.3)
    if k <= 0: return
    wd = text_w(txt, size, "extrabold") + 80
    lay = Image.new("RGBA", (int(wd) + 80, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((40, 40, 40 + wd, 120), 40, fill=col); draw_text(d, 40 + wd / 2, 93, txt, size, "extrabold", tc, "m")
    sh = lay.filter(ImageFilter.GaussianBlur(14)); sh2 = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh2.putalpha(sh.getchannel("A").point(lambda v: int(v * 0.3)))
    base = Image.new("RGBA", lay.size, (0, 0, 0, 0)); base.alpha_composite(sh2, (0, 10)); base.alpha_composite(lay)
    paste_scaled(img, base, (lay.size[0] / 2, 80), cx, cy, k, min(1, k * 2.5))

def frame_f(fi):
    t = fi / FPS; i = int(round(fi))
    s = scene_idx(t); ts = SC[s]
    if s in DARK: img = dark_bg(t, s, (540, 820 if s == 0 else 1000))
    else:
        img = P.BG.copy(); V.bg_motion(img, t)
    cam_z = 1.0; shake = 0.0
    if s == 0:
        # 11.11 big, then counter, then HOW?
        pin = clamp((t - 0.05) / 0.5)
        if t < T_ONE:
            Lb, Ab = text_layer("11.11", 400, "extrabold", WHITE, pad=60)
            Lt, At = tilt(Lb, -5 + 3 * math.sin(t * 1.3), 14 * math.sin(t * 1.1 + 0.3))
            out_k = clamp((t - (T_ONE - 0.25)) / 0.25)
            paste_scaled(img, Lt, At, 540, 780 - 80 * out_k, out_back(pin, 2.0) * (1 - 0.4 * out_k), min(1, pin * 3) * (1 - out_k))
            for k, ch in enumerate("1111"): pass
            letters(img, "A joke about being single.", 62, "extrabold", WHITE, 540, 1130, t, T_JOKE - 0.05, 0.028)
            zh(img, "一个关于单身的玩笑", 540, 1230, t, T_JOKE + 0.5, 42, (255, 214, 208), "extrabold")
        else:
            v = 1.7 * out_cubic(clamp((t - T_ONE) / max(0.3, T_TRILL - T_ONE)))
            Ln, An = text_layer(f"¥{v:.1f}", 330, "extrabold", WHITE, pad=40)
            slam = clamp((t - T_TRILL) / 0.35)
            paste_scaled(img, Ln, An, 540, 780 + (0 if t > T_TRILL else 20), 1.0 + 0.1 * math.sin(slam * math.pi) * (t > T_TRILL), 1)
            if t >= T_TRILL:
                letters(img, "TRILLION", 128, "extrabold", (255, 86, 78), 540, 985, t, T_TRILL - 0.05, 0.03, 0.3, 40, False)
                if t < T_TRILL + 0.3: img = chroma(img, 9 * (1 - (t - T_TRILL) / 0.3))
            if t >= T_YUAN:
                wd = text_w("IN SALES · LAST YEAR   去年销售额", 34, "mono")
                L, A = wl("IN SALES · LAST YEAR   去年销售额", 34, "mono", (255, 226, 220)); bin_(img, L, A, 540, 1100, t, T_YUAN, 0.25)
                zh(img, "一个单身玩笑，卖出1.7万亿元", 540, 1180, t, T_YUAN + 0.3, 40, (255, 214, 208), "extrabold")
            if t >= T_HOW - 0.05:
                p = clamp((t - T_HOW + 0.05) / 0.3); sc = 1.5 - 0.5 * out_expo(p)
                L, A = text_layer("HOW?", 230, "extrabold", BRAND, pad=50); Lw, Aw = text_layer("HOW?", 230, "extrabold", WHITE, pad=50)
                paste_scaled(img, L, A, 548, 1488, sc * 1.0, min(1, p * 3)); paste_scaled(img, Lw, Aw, 540, 1480, sc, min(1, p * 3))
                shake = 14 * (1 - p) ** 2
    elif s == 1:
        V.glow(img, 540, 760, t, ts, 1.8, 0.4)
        glass_pill(img, "1990s · NANJING  南京", 540, 250, t, T_NINE, BRAND, 40)
        k = pop(t, ts + 0.05, 0.4)
        paste_scaled(img, DORM, DORMA, 540, 880, 1.0 * k, min(1, k * 2), rot=-1.2)
        if T_ELEV - 0.1 <= t < T_4ONES + 0.1:
            e = pop(t, T_ELEV - 0.1, 0.35); Lb, Ab = text_layer("11.11", 260, "extrabold", BRAND, pad=50); Lt, At = tilt(Lb, -8, 12 * math.sin(t * 2))
            paste_scaled(img, Lt, At, 540, 820, e * 1.15, 1)
        if t >= T_4ONES - 0.05:
            for j in range(4):
                c0 = T_4ONES + j * 0.12 - 0.05
                if t < c0: continue
                p = clamp((t - c0) / 0.4); drop = (1 - out_back(p, 1.8)) * -420
                lonely = clamp((t - T_LONELY) / 0.6)
                x = 540 + (j - 1.5) * (165 + 30 * lonely)
                look = (-1 if j < 2 else 1) * lonely
                blink = ((t * 0.9 + j * 0.37) % 2.1) < 0.1
                L, A = char(look, "sad" if lonely > 0.3 else "flat", blink)
                paste_scaled(img, L, A, x, 1150 + drop + 4 * math.sin(t * 2 + j), 1.15, min(1, p * 3), rot=2 * math.sin(t * 1.5 + j))
        zh(img, "1990年代 · 南京宿舍里的一个笑话", 540, 1360, t, T_NINE + 0.4, 42)
        if t >= T_LONELY:
            for j in range(4):
                x = 540 + (j - 1.5) * 195; tt = (t - T_LONELY - j * 0.15)
                if tt > 0:
                    L, A = text_layer("…", 70, "extrabold", MUTED); paste_scaled(img, L, A, x + 60, 800 - 14 * (tt % 1.6) , 0.7, 0.7 * min(1, tt * 3) * (1 - clamp((tt % 1.6 - 1.0) / 0.6)))
    elif s == 2:
        V.glow(img, 540, 700, t, ts, 1.8, 0.4)
        letters(img, "2009", 280, "serif", BRAND, 540, 520, t, ts + 0.1, 0.09, 0.45, 80, True)
        glass_pill(img, "27 SHOPS  27家店", 540, 640, t, T_27 - 0.05, INK, 40)
        cols = 9
        for j in range(27):
            c0 = T_27 + j * 0.03
            if t >= c0:
                x = 540 + ((j % cols) - (cols - 1) / 2) * 104; y = 800 + (j // cols) * 112
                paste_scaled(img, SHOP[0], SHOP[1], x, y + 4 * math.sin(t * 2 + j * 0.7), pop(t, c0, 0.25) * 1.25, 1)
        if t >= T_50 - 0.1:
            v = int(round(50 * out_cubic(clamp((t - T_50 + 0.1) / 0.9)))); L, A = ctext(f"≈ ¥{v} MILLION", 112, "extrabold", BRAND)
            paste_scaled(img, L, A, 540, 1250, pop(t, T_50 - 0.1, 0.3), 1)
            zh(img, "约5000万元", 540, 1330, t, T_50 + 0.3, 44)
    elif s == 3:
        # bars
        glass_pill(img, "LAST YEAR  去年", 540, 250, t, T_LAST, BRAND, 40)
        h0 = 16; p = out_expo(clamp((t - (T_TRILL2 - 0.45)) / 1.5)); hb = 14 + 1500 * p
        base_y = 1500
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((210, base_y - h0, 330, base_y), 8, fill=(255, 255, 255, 220)); draw_text(d, 270, base_y + 50, "2009", 34, "mono", (255, 226, 220), "m")
        pp = pop(t, ts + 0.2, 0.3)
        if t < T_TRILL2 - 0.45: draw_text(d, 270, base_y - 40, "¥50M", 32, "extrabold", WHITE, "m")
        d.rounded_rectangle((540, base_y - hb, 900, base_y), 16, fill=BRAND + (255,))
        d.rectangle((540, base_y - hb, 900, base_y - hb + 18), fill=(255, 120, 110, 255)) if hb > 60 else None
        draw_text(d, 720, base_y + 50, "2025", 34, "mono", (255, 226, 220), "m")
        for k in range(14):
            r = random.Random(k); x = 560 + r.uniform(0, 320); y = (base_y - hb + (t * 900 + r.uniform(0, 1500)) % max(40, hb)); d.line((x, y, x, y + r.uniform(40, 120)), fill=(255, 255, 255, 60), width=3) if hb > 100 else None
        if t >= T_TRILL2 - 0.15:
            val = 1.7 * out_cubic(clamp((t - T_TRILL2 + 0.15) / 0.9)); L, A = text_layer(f"¥{val:.1f} TRILLION", 120, "extrabold", WHITE, pad=40)
            paste_scaled(img, L, A, 540, 520, 1.0 + 0.06 * math.sin(clamp((t - T_TRILL2 - 0.75) / 0.3) * math.pi), 1)
            if t < T_TRILL2 + 0.3: img = chroma(img, 8 * (1 - (t - T_TRILL2 + 0.15) / 0.45))
            zh(img, "1.7万亿元", 540, 640, t, T_TRILL2 + 0.2, 44, (255, 214, 208), "extrabold")
        sweep(img, t, T_TRILL2 - 0.1, 0.9, a=70)
    elif s == 4:
        V.glow(img, 540, 800, t, ts, 1.8, 0.4)
        tt = t - ts; L, A = phone_layer(t); ay = -16 + 22 * clamp(tt / 3.5); ax = -4 + 3 * math.sin(t)
        Lt, At = tilt(L, ax, ay); k = pop(t, ts + 0.05, 0.45)
        paste_scaled(img, Lt, At, 360, 930, 0.9 * k, min(1, k * 2.5))
        for j, (txt, t0, y) in enumerate((("Hosts  主播", T_HOSTS, 640), ("Models  模特", T_MODELS, 820), ("Ads  广告", T_ADS, 1000))):
            glass_pill(img, txt, 790, y, t, t0 - 0.05, BRAND if j != 1 else INK, 44)
        for j in range(9):
            r = random.Random(j * 7); ph = (t * 0.55 + r.uniform(0, 1)) % 1.0; x = 330 + r.uniform(-60, 80) + 30 * math.sin(ph * 6 + j); y = 1250 - ph * 700
            heart(img, x, y, 0.8 + 0.4 * r.random(), int(220 * math.sin(ph * math.pi)))
        zh(img, "镜头前的面孔", 540, 1520, t, T_FACES, 44)
    elif s == 5:
        V.glow(img, 540, 760, t, ts, 1.8, 0.5)
        letters(img, "That's work.", 120, "extrabold", INK, 540, 480, t, T_WORK - 0.35, 0.04, 0.35, 60, True)
        zh(img, "你是在中国的外国人，这就是工作", 540, 570, t, T_IF + 0.5, 42)
        mx = clamp((t - T_HARD) / 1.0)
        for j in range(8):
            c0 = T_HARD - 0.05 + j * 0.09
            if t < c0: continue
            r = random.Random(j * 3); bx = 150 + (j % 2) * 780 + r.uniform(-60, 60); by = 760 + (j // 2) * 210 + r.uniform(-30, 30)
            Lg, Ag = MG[j]; paste_scaled(img, Lg, Ag, bx, by + 7 * math.sin(t * 1.7 + j), pop(t, c0, 0.3) * 0.78, 1, rot=(-1) ** j * (4 + 3 * r.random()))
        if t >= T_HARD:
            L, A = text_layer("?", 260, "serif", BRAND, pad=40); paste_scaled(img, L, A, 540, 1130 + 10 * math.sin(t * 3), pop(t, T_HARD + 0.2, 0.4), 1, rot=6 * math.sin(t * 2))
            zh(img, "难的是，找到它", 540, 1420, t, T_HARD + 0.3, 46)
    elif s == 6:
        V.glow(img, 540, 840, t, ts, 1.8, 0.6)
        q = clamp((t - T_SO) / 1.0)
        if t < T_ONEM + 0.2:
            for j in range(12):
                r = random.Random(j); x0 = 150 + (j % 2) * 780 + r.uniform(-40, 40); y0 = 400 + (j // 2) * 170; e = out_cubic(clamp((t - T_SO - 0.1 - j * 0.04) / 0.8))
                x = x0 + (540 - x0) * e; y = y0 + (940 - y0) * e - 160 * math.sin(e * math.pi)
                Lg, Ag = MG[j]; paste_scaled(img, Lg, Ag, x, y, 0.8 * (1 - 0.55 * e), 1 - clamp((e - 0.7) / 0.3), rot=(-1) ** j * 5 * (1 - e))
        k2 = clamp((t - T_SO - 0.8) / 0.55)
        if k2 > 0:
            Lm, Am = MK, MKA; Lt, At = tilt(Lm, -8 * (1 - out_cubic(k2)) + 2 * math.sin(t), 14 * (1 - out_cubic(k2)) * (-1))
            V.glow(img, 540, 940, t, T_SO + 0.8, 1.8, 0.8)
            paste_scaled(img, Lt, At, 540, 940, 0.92 * out_back(k2, 1.8), min(1, k2 * 3))
        typed(img, t, [S_("One ", INK, 1.0), SE_("marketplace.", BRAND, 1.2)], 96, 540, 300, T_ONEM, 28)
        zh(img, "一个平台，所有机会、所有经纪人", 540, 400, t, T_ONEM + 0.3, 40)
        if t >= T_EVJOB: L, A = pill("Every job", "所有机会", "case", True); V.blur_in(img, L, A, 290, 1480, t, T_EVJOB, 0.22)
        if t >= T_EVAG: L, A = pill("Every agent", "所有经纪人", "person", False); V.blur_in(img, L, A, 790, 1480, t, T_EVAG, 0.22)
    else:
        V.glow(img, 540, 460, t, ts, 1.5, 0.7)
        V.scramble(img, t, "laowai吗", 150, 540, 470, ts + 0.02, 0.06, cols={6})
        sp = ENV[min(i, len(ENV) - 1)]; mouth = "big" if sp > 0.12 else ("o" if sp > 0.05 else "smile")
        R.lay_at(img, R.masc(mouth, (0, 0), blink=(t % 2.3) < 0.1), R.MA, 540, 790 - 6 * math.sin(t * 6), t, ts + 0.2, 0.35, sc=0.8)
        typed(img, t, [S_("Foreign talent. Chinese agents.", MUTED, 0.38)], 90, 540, 1060, ts + 0.5, 34)
        zh(img, "外国人才 · 中国经纪人", 540, 1120, t, ts + 0.9, 34, GREY)
        typed(img, t, [S_("laowai.ma", INK, 1.0)], 112, 540, 1300, T_URL, 18)
        if t >= T_URL + 0.7: V.ellipse_draw(img, 540, 1263, 340, 92, (t - T_URL - 0.7) / 0.35)
        if t >= T_WELCOME: R.lay_at(img, CTA3[0], CTA3[1], 540, 1480, t, T_WELCOME, 0.3)
    if shake: img = img.transform(img.size, Image.AFFINE, (1, 0, random.uniform(-shake, shake), 0, 1, random.uniform(-shake, shake)))
    img = whip(img, t, i)
    te = SC[s + 1]; p = clamp((t - ts) / max(0.5, min(te, P.DUR) - ts))
    img = camera(img, zoom=1.0 + 0.05 * p)
    if t < SC[7] and not (s == 0 and t < 0.3):
        for gi, g in enumerate(P.GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.2:
                ai = 0
                for k, (w, s2, e) in enumerate(g):
                    if t >= s2 - 0.02: ai = k
                Lc, Ac = P.CAPS[(gi, ai)]; cap_plate(img, Lc, Ac, 1700); paste_scaled(img, Lc, Ac, 540, 1700, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06)); break
    fade = clamp((P.DUR - t) / 0.3) if t > P.DUR - 0.3 else 1.0
    return post(img, i, glitch=0.0, grain=0.22, vignette=0.12 if s in DARK else 0.0, fade=fade)

MB_EV = None
def mb_n(i):
    t = i / FPS
    ev = [T_TRILL, T_HOW, T_4ONES, T_ELEV, T_TRILL2, T_SO + 0.8, T_ONEM] + SC[1:7]
    return 4 if any(abs(t - e) < 0.28 for e in ev) else 1
def frame(i):
    return mblur(lambda fi: np.asarray(frame_f(fi)), i, mb_n(i), 0.6)
def frame_img(i): return Image.fromarray(frame(i))

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
    for c in SC[1:7]: bed.add(c - 0.16, V.swoosh(0.34), 0.8); bed.add(c + 0.02, V.thump(), 0.5)
    bed.add(0.0, V.swoosh(0.4), 0.7); bed.add(0.1, V.thump(), 0.7)
    bed.add(T_ONE - 0.1, riser(1.2), 0.22); bed.add(T_TRILL, V.thump(), 0.9); bed.add(T_TRILL, V.sparkle(), 0.6)
    bed.add(T_HOW, V.thump(), 0.9); bed.add(T_HOW, boom(), 0.35)
    bed.add(T_NINE, V.blip(380, 900), 0.6)
    bed.add(T_ELEV - 0.1, V.thump(), 0.7)
    for j in range(4): bed.add(T_4ONES + j * 0.12 - 0.05, V.blip(300 + 70 * j, 620 + 70 * j), 0.45); bed.add(T_4ONES + j * 0.12 + 0.2, V.thump(), 0.3)
    for j in range(27): bed.add(T_27 + j * 0.03, V.blip(500 + 12 * j, 900 + 14 * j), 0.1)
    bed.add(T_50, riser(0.9), 0.2); bed.add(T_50 + 0.9, V.thump(), 0.6)
    bed.add(T_TRILL2 - 0.5, riser(1.0), 0.3); bed.add(T_TRILL2 - 0.1, boom(), 0.5); bed.add(T_TRILL2, V.sparkle(), 0.5)
    for t0 in (T_HOSTS, T_MODELS, T_ADS): bed.add(t0 - 0.05, V.blip(420, 980), 0.55)
    bed.add(T_HARD, buzz(0.2), 0.12)
    bed.add(T_SO + 0.8, V.swoosh(0.45), 0.8); bed.add(T_SO + 1.0, V.thump(), 0.7); bed.add(T_SO + 1.0, jingle(), 0.9)
    for t0 in (T_EVJOB, T_EVAG): bed.add(t0, V.blip(400, 950), 0.6)
    for tt, f in ((SC[7], 330), (SC[7] + 0.4, 392), (SC[7] + 0.8, 494), (SC[7] + 1.2, 659)): bed.add(tt, pluck(f), 0.38)
    bed.add(T_WELCOME, V.blip(400, 1000), 0.6); bed.add(T_URL + 0.7, V.swoosh(0.4), 0.6); bed.add(T_URL + 1.1, V.sparkle(), 0.6)
    b = hp(bed.buf.copy(), 40)
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
    b = b * (1 - 0.45 * np.clip(env / 0.08, 0, 1)) * 0.75
    y = voice + b; y = np.tanh(y * 1.1) / np.tanh(1.1); y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    n = int(0.3 * SR); y[-n:] *= np.linspace(1, 0, n); write_wav(path, y)

if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]: frame_img(int(float(tt) * FPS)).save(f"out/v8still_{tt}.png")
    elif sys.argv[1] == "audio": build_audio("out/reel08.wav")
    else:
        build_audio("out/reel08.wav"); render(frame, int(DUR * FPS), "out/reel08.wav", "out/laowai_reel_07.mp4")
