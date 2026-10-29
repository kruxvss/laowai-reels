"""Reel 05 v1 (from 04v3 helpers) - WOW fact: 88888888 phone number sold for 2.33M yuan. Inspo motion language, FASTER, no repeating typing/tick sounds, icons centred by bbox."""
import sys, math, random
sys.path.insert(0, "/home/claude/reels")
import reel_06base as P
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


def fmt(n): return f"¥{int(n):,}"
# ================= Reel 05 timeline (from VO word timestamps) =================
import re
def _n(w): return re.sub(r"[^a-z0-9.]", "", w.lower()).strip(".")
def tw(word, after=0.0, end=False):
    for w, s, e, i in P.WN:
        if s >= after - 1e-6 and _n(w) == _n(word): return e if end else s
    raise KeyError(word)
T_MIL = tw("million", end=True)
T_JUST = tw("Just"); T_EIGHTS = tw("eights.", end=True)
T_BEC = tw("Because"); T_EIGHT2 = tw("eight", T_BEC)
T_GET = tw("getting", T_BEC); T_SICH = tw("Sichuan"); T_WON = tw("won", T_SICH)
T_CHENG = tw("Chengdu", T_SICH); T_WHY = tw("Why"); T_ROOM = tw("room.", T_WHY)
T_FUN = tw("Funny"); T_RIGHT = tw("Right"); T_HEAR = tw("hear", T_RIGHT); T_WRONG = tw("Wrong")
T_NEVER = tw("never", T_WRONG); T_SO = tw("So"); T_ONE = tw("one", T_SO); T_JOB = tw("job.", T_SO) if False else tw("Every", T_SO)
T_AGENT = tw("agent.", T_JOB + 0.1) if False else tw("Every", T_JOB + 0.2)
T_MKT = tw("One", T_AGENT); T_FIND = tw("Find"); T_URL = tw("laowai.ma.")
SC = [0, T_JUST - 0.12, T_BEC - 0.18, T_SICH - 0.18, T_WHY - 0.12, T_RIGHT - 0.14, T_SO - 0.12, T_FIND - 0.1, P.DUR + 1]
NS = len(SC) - 2
P.CAPEND = SC[7]
def scene_idx(t):
    k = 0
    for i, c in enumerate(SC[1:-1], 1):
        if t >= c: k = i
    return k

# ---------- new layers ----------
SMALLP = disc_icon(40, g_person, fill=(196, 188, 176))
HIP = disc_icon(40, g_person, fill=BRAND)
def group_card(name, zh_name, msg, zh_msg, w=900, h=330):
    lay, d, p = P.card_shadow(w, h, 40)
    ic, ia = ICON["case"]; sm = ic.resize((92, 92), Image.LANCZOS); lay.alpha_composite(sm, (p + 30, p + 26))
    draw_text(d, p + 142, p + 66, name, 38, "extrabold", INK); draw_text(d, p + 142, p + 108, zh_name, 26, "bold", MUTED)
    d.line((p, p + 140, p + w, p + 140), fill=LINE, width=3)
    bw = int(min(w - 80, text_w(msg, 40, "bold") + 80)); d.rounded_rectangle((p + 40, p + 170, p + 40 + bw, p + 250), 30, fill=(240, 236, 230))
    draw_text(d, p + 40 + bw / 2, p + 222, msg, 40, "bold", INK, "m")
    draw_text(d, p + 44, p + 292, zh_msg, 26, "bold", MUTED)
    return lay, (p + w / 2, p + h / 2), p
GA, GAA, GAP = group_card("Shanghai Casting Group", "上海选角群", "Runway casting · Friday", "周五 · 走秀选角")
GB, GBA, GBP = group_card("Beijing Shoots Group", "北京拍摄群", "Brand shoot · Saturday", "周六 · 品牌拍摄")
def tag(txt, zhs, ok=True):
    w, h, p = 520, 100, 14
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 50, fill=BRAND if ok else (255, 255, 255), outline=None if ok else INK, width=4)
    col = WH if ok else INK
    c = (p + 60, p + h / 2)
    if ok:
        d.line((c[0] - 18, c[1], c[0] - 4, c[1] + 14, c[0] + 20, c[1] - 14), fill=WH, width=9, joint="curve")
    else:
        d.line((c[0] - 16, c[1] - 16, c[0] + 16, c[1] + 16), fill=INK, width=9); d.line((c[0] + 16, c[1] - 16, c[0] - 16, c[1] + 16), fill=INK, width=9)
    draw_text(d, p + 110, p + 48, txt, 36, "extrabold", col); draw_text(d, p + 110, p + 84, zhs, 26, "bold", (255, 214, 208) if ok else MUTED)
    return lay, (p + w / 2, p + h / 2)
TAG_IN = tag("You're in this group", "你在群里", True); TAG_OUT = tag("Not in this group", "你不在这个群", False)

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

# room grid positions
GRID = [(540 + (c - 2) * 160, 760 + (r - 1.5) * 150) for r in range(4) for c in range(5)]
HI = 8   # highlighted seat

def frame(i):
    t = i / FPS
    s = scene_idx(t); ts = SC[s]
    img = P.BG.copy(); V.bg_motion(img, t)
    if s in (4, 6):
        a = clamp((t - ts) / 0.6)
        paste_scaled(img, V.RING, V.RINGA, 130 + 30 * math.sin(t * 0.7), 200, 1.0, a * 0.8, rot=t * 6)
    if s == 0:
        V.glow(img, 540, 840, t, 0.0, 1.8, 0.9)
        V.particles(img, t, 0.4, 540, 880, 3, 7)
        typed(img, t, [S_("In ", INK), SE_("2003,", BRAND, 1.25)], 96, 540, 330, 0.36, 30)
        ic, ia = ICON["phone"]
        t_ph = tw("phone")
        if t >= t_ph - 0.2: paste_scaled(img, ic, ia, 540, 580, pop(t, t_ph - 0.2) * (1 + 0.02 * math.sin(t * 3)), 1)
        p = clamp((t - 0.12) / (T_MIL - 0.12)); val = 2330000 * (p ** 2.2)
        if t < 0.35:
            q = clamp(t / 0.35); e = out_expo(q)
            L, A = ctext("¥", 260, "extrabold", BRAND)
            paste_scaled(img, L.filter(ImageFilter.GaussianBlur(max(0.1, 24 * (1 - e) ** 2))), A, 540, 900, 2.4 - 1.4 * e, min(1, q * 2.5))
        else:
            L, A = ctext(fmt(val), 128, "extrabold", BRAND if p >= 1 else INK)
            sc = 1.0 + (0.12 * math.sin(clamp((t - T_MIL) / 0.3) * math.pi) if t > T_MIL else 0)
            paste_scaled(img, L, A, 540, 900, sc, 1.0)
        typed(img, t, [S_("for a phone number.", MUTED, 0.62)], 90, 540, 1100, tw("phone"), 32)
        zh(img, "2003年，一个手机号，233万元", 540, 1190, t, T_MIL, 38)
    elif s == 1:
        V.glow(img, 540, 900, t, ts, 1.8, 0.8)
        typed(img, t, [S_("Not a ", INK), SE_("special", GREY, 1.25), S_(" one.", INK)], 92, 540, 420, ts + 0.1, 32)
        for k in range(8):
            c0 = T_JUST + 0.15 + k * (T_EIGHTS - T_JUST - 0.1) / 8
            if t < ts + 0.15: continue
            paste_scaled(img, CELL_OFF[0], CELL_OFF[1], CELL_X[k], 880, 1.0, min(1, (t - ts) / 0.3) * 0.9)
            if t >= c0:
                V.glow(img, CELL_X[k], 880, t, c0, 0.4, 0.5)
                paste_scaled(img, CELL_ON[0], CELL_ON[1], CELL_X[k], 880, pop(t, c0, 0.22), min(1, (t - c0) / 0.05))
        typed(img, t, [S_("Just ", INK), SE_("eight eights.", BRAND, 1.2)], 80, 540, 1140, T_JUST, 32)
        zh(img, "全是8 · 八个八", 540, 1230, t, T_EIGHTS - 0.2, 40)
    elif s == 2:
        V.glow(img, 540, 880, t, ts, 1.8, 0.8)
        typed(img, t, [S_("In ", INK), SE_("Chinese,", BRAND, 1.25)], 96, 540, 360, T_BEC + 0.1, 30)
        if t >= T_EIGHT2: paste_scaled(img, CH8[0], CH8[1], 235, 820, pop(t, T_EIGHT2, 0.3), 1)
        if t >= T_GET:
            V.glow(img, 845, 820, t, T_GET, 0.9, 0.7)
            paste_scaled(img, CHF[0], CHF[1], 845, 820, pop(t, T_GET, 0.3), 1)
        if t >= T_EIGHT2: zh(img, "bā · eight", 235, 1030, t, T_EIGHT2 + 0.1, 40, INK, "mono")
        if t >= T_GET: zh(img, "fā · get rich", 845, 1030, t, T_GET + 0.1, 40, BRAND, "mono")
        ts2 = tw("sounds", T_BEC)
        if t >= ts2:
            arrow(img, 405, 820, 665, 820, (t - ts2) / 0.3, INK, 6, 24)
            bin_(img, *wl("sounds like", 30, "mono", MUTED), 535, 770, t, ts2 + 0.1)
        if t >= T_GET + 0.2:
            typed(img, t, [SE_("= get rich.", BRAND, 1.0)], 120, 540, 1300, T_GET + 0.2, 28)
            zh(img, "发财 · 谐音", 540, 1380, t, T_GET + 0.5, 44)
    elif s == 3:
        V.glow(img, 540, 800, t, ts, 1.6, 0.6)
        typed(img, t, [S_("Sichuan ", INK), SE_("Airlines", BRAND, 1.25)], 90, 540, 320, T_SICH, 32)
        k = pop(t, ts + 0.1, 0.3)
        paste_scaled(img, LOT, LOTA, 540, 760, k * (1 + 0.012 * math.sin(t * 1.6)), min(1, (t - ts) / 0.08))
        if t >= ts + 0.35:
            ic, ia = ICON["plane"]
            paste_scaled(img, ic, ia, 250, 740, pop(t, ts + 0.35), 1)
            bin_(img, *wl("四川航空", 44, "bold", MUTED), 600, 770, t, ts + 0.5)
            bin_(img, *wl("Sichuan Airlines", 46, "extrabold", INK), 600, 722, t, ts + 0.45)
            for q in range(8):
                c0 = ts + 0.7 + q * 0.04
                if t >= c0:
                    L, A = ctext("8", 150, "extrabold", BRAND)
                    paste_scaled(img, L, A, 540 + (q - 3.5) * 92 + (-12 if q < 4 else 12), 890, 1.0, min(1, (t - c0) / 0.1))
        if t >= T_WON:
            V.glow(img, 620, 1030, t, T_WON, 1.0, 0.8)
            paste_scaled(img, SOLD, SOLDA, 620, 1030, 0.8 * (1.0 + 0.9 * (1 - out_cubic(clamp((t - T_WON) / 0.14)))) * (1 + 0.01 * math.sin(t * 5)), min(1, (t - T_WON) / 0.06), rot=-8)
        if t >= T_CHENG - 0.05:
            L, A = pill("Chengdu", "成都", "pin"); V.blur_in(img, L, A, 540, 1270, t, T_CHENG - 0.05, 0.26)
    elif s == 4:
        V.glow(img, 540, 900, t, ts, 1.6, 0.6)
        typed(img, t, [S_("Why ", INK), SE_("them?", BRAND, 1.3)], 100, 540, 330, T_WHY, 30)
        for k, (x, y) in enumerate(GRID):
            c0 = ts + 0.12 + 0.015 * k
            if t < c0 or k == HI: continue
            paste_scaled(img, SMALLP[0], SMALLP[1], x, y, pop(t, c0, 0.25), 0.9 if True else 1)
        hx, hy = GRID[HI]
        if t >= T_ROOM - 0.5:
            V.glow(img, hx, hy, t, T_ROOM - 0.5, 0.9, 0.9)
            paste_scaled(img, HIP[0], HIP[1], hx, hy, pop(t, T_ROOM - 0.5, 0.3) * 1.5, 1)
        else:
            paste_scaled(img, SMALLP[0], SMALLP[1], hx, hy, pop(t, ts + 0.2, 0.25), 0.9)
        typed(img, t, [S_("They were in the ", INK, 0.85), SE_("room.", BRAND, 1.2)], 84, 540, 1230, tw("They", T_WHY), 30)
        zh(img, "因为，他们在现场", 540, 1305, t, T_ROOM - 0.2, 38)
        typed(img, t, [SE_("Work works the same.", GREY, 1.0)], 96, 540, 1430, T_FUN, 30)
        zh(img, "机会，也是这样", 540, 1500, t, T_FUN + 0.5, 38)
    elif s == 5:
        V.glow(img, 540, 860, t, ts, 1.6, 0.6)
        if t < T_WRONG - 0.05: typed(img, t, [S_("Right ", INK, 1.0), SE_("group?", BRAND, 1.25)], 96, 540, 300, T_RIGHT, 30)
        else: typed(img, t, [S_("Wrong ", INK, 1.0), SE_("group?", BRAND, 1.25)], 96, 540, 300, T_WRONG, 30)
        dim = 1.0 if t < T_WRONG else 1 - 0.65 * clamp((t - T_WRONG) / 0.3)
        paste_scaled(img, GA, GAA, 540, 600, pop(t, ts + 0.1, 0.3), min(1, (t - ts) / 0.08) * dim)
        if t >= T_HEAR - 0.3: paste_scaled(img, *TAG_IN, 540, 810, pop(t, T_HEAR - 0.3, 0.3), dim)
        if t >= T_WRONG:
            fade = 1 - 0.7 * clamp((t - T_NEVER) / 0.5)
            L = GB.filter(ImageFilter.GaussianBlur(10 * clamp((t - T_NEVER) / 0.5))) if t > T_NEVER else GB
            paste_scaled(img, L, GBA, 540, 1060, pop(t, T_WRONG, 0.3), min(1, (t - T_WRONG) / 0.08) * fade)
            if t < T_NEVER - 0.1: paste_scaled(img, *TAG_OUT, 540, 1290, pop(t, T_WRONG + 0.2, 0.3), 1)
        if t >= T_NEVER:
            L, A = ctext("?", 300, "extrabold", BRAND)
            paste_scaled(img, L, A, 540, 1075, pop(t, T_NEVER, 0.3) * (1 + 0.03 * math.sin(t * 5)), 1)
            zh(img, "你根本不知道它存在", 540, 1330, t, T_NEVER + 0.1, 40)
    elif s == 6:
        V.glow(img, 540, 860, t, ts, 1.8, 0.7)
        if t < T_MKT - 0.05: typed(img, t, [S_("So we built ", INK, 0.95), SE_("one room.", BRAND, 1.25)], 92, 540, 300, T_SO, 30)
        else:
            typed(img, t, [S_("One ", INK, 1.0), SE_("marketplace.", BRAND, 1.25)], 100, 540, 300, T_MKT, 30)
        k = clamp((t - ts) / 0.4)
        if k < 1:
            paste_scaled(img, GA, GAA, 540, 600 + 300 * out_cubic(k), 1 - 0.5 * k, 1 - k)
            paste_scaled(img, GB, GBA, 540, 1060 - 160 * out_cubic(k), 1 - 0.5 * k, (1 - k) * 0.4)
        if t >= ts + 0.25:
            V.glow(img, 540, 900, t, ts + 0.25, 1.8, 0.8)
            paste_scaled(img, MK, MKA, 540, 900, 0.92 * pop(t, ts + 0.25, 0.35) * (1 + 0.01 * math.sin(t * 1.5)), min(1, (t - ts - 0.25) / 0.08))
        if t >= T_JOB:
            L, A = pill("Jobs", "工作", "case", True); V.blur_in(img, L, A, 290, 1400, t, T_JOB, 0.26)
        if t >= T_AGENT:
            L, A = pill("Agents", "经纪人", "person", False); V.blur_in(img, L, A, 790, 1400, t, T_AGENT, 0.26)
        if t >= T_MKT: zh(img, "一个平台，全都有", 540, 385, t, T_MKT + 0.1, 40)
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
        if t >= T_FIND + 0.1: R.lay_at(img, CTA2[0], CTA2[1], 540, 1480, t, T_FIND + 0.1, 0.3)
    img = whip(img, t, i)
    te = SC[s + 1]; p = clamp((t - ts) / max(0.5, min(te, P.DUR) - ts))
    img = camera(img, zoom=1.0 + 0.05 * p)
    if t < SC[7] and not (s == 0 and t < 0.35):
        for gi, g in enumerate(P.GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.2:
                ai = 0
                for k, (w, s2, e) in enumerate(g):
                    if t >= s2 - 0.02: ai = k
                Lc, Ac = P.CAPS[(gi, ai)]
                paste_scaled(img, Lc, Ac, 540, 1620, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06))
                break
    fade = clamp((P.DUR - t) / 0.3) if t > P.DUR - 0.3 else 1.0
    return post(img, i, glitch=0.0, grain=0.22, vignette=0.0, fade=fade)
CTA2 = P.cta("Find it at laowai.ma")
DUR = P.DUR

def build_audio(path):
    m = Mix(DUR)
    x = vo / (np.max(np.abs(vo)) + 1e-9) * 0.82
    voice = np.zeros(m.n); voice[:min(len(x), m.n)] = x[:m.n]
    bed = Mix(DUR)
    for c in SC[1:-1]:
        bed.add(c - 0.16, V.swoosh(0.34), 0.8); bed.add(c + 0.02, V.thump(), 0.45)
    bed.add(0.0, V.swoosh(0.4), 0.7); bed.add(0.2, riser(max(1.0, T_MIL - 0.3)), 0.22)
    bed.add(T_MIL, V.thump(), 0.7); bed.add(T_MIL, V.sparkle(), 0.55)
    bed.add(tw("phone") - 0.2, V.blip(420, 980), 0.55)
    for k, f in enumerate((523, 587, 659, 784, 880, 1047, 1175, 1319)):
        bed.add(T_JUST + 0.15 + k * (T_EIGHTS - T_JUST - 0.1) / 8, pluck(f), 0.3)
    for t0 in (T_EIGHT2, T_GET): bed.add(t0, V.blip(380, 900), 0.7); bed.add(t0, V.thump(), 0.35)
    bed.add(T_GET + 0.3, V.sparkle(), 0.55)
    bed.add(T_SICH + 0.1, V.blip(300, 700), 0.5)
    bed.add(T_WON, V.thump(), 0.9); bed.add(T_WON, clap(), 0.35); bed.add(T_WON + 0.1, V.sparkle(), 0.5)
    bed.add(T_CHENG - 0.05, V.blip(420, 1000), 0.6)
    bed.add(T_ROOM - 0.5, V.blip(330, 900), 0.7); bed.add(T_ROOM - 0.5, V.thump(), 0.4); bed.add(T_ROOM - 0.4, V.sparkle(), 0.5)
    bed.add(T_HEAR - 0.3, V.blip(500, 900), 0.5)
    bed.add(T_WRONG, V.blip(260, 200), 0.6); bed.add(T_NEVER, buzz(0.18), 0.12); bed.add(T_NEVER, V.thump(), 0.6)
    bed.add(SC[6] + 0.25, V.thump(), 0.7); bed.add(SC[6] + 0.25, V.sparkle(), 0.6)
    for t0 in (T_JOB, T_AGENT): bed.add(t0, V.blip(400, 950), 0.6)
    bed.add(T_MKT, V.sparkle(), 0.5)
    for tt, f in ((SC[7], 330), (SC[7] + 0.4, 392), (SC[7] + 0.8, 494), (SC[7] + 1.2, 659)): bed.add(tt, pluck(f), 0.38)
    bed.add(T_FIND + 0.1, V.blip(400, 1000), 0.6); bed.add(T_URL + 0.7, V.swoosh(0.4), 0.6); bed.add(T_URL + 1.1, V.sparkle(), 0.6)
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
        for tt in sys.argv[2:]: Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/v5still_{tt}.png")
    elif sys.argv[1] == "audio": build_audio("out/reel05.wav")
    else:
        build_audio("out/reel05.wav")
        render(frame, int(DUR * FPS), "out/reel05.wav", "out/laowai_reel_05.mp4")
