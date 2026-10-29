"""Reel 04 - WHITE-MINIMAL KINETIC EXPLAINER (inspo: divyansh.fx). VO: Elena. Trust is expensive -> laowai."""
import sys, json, math, wave
sys.path.insert(0, "/home/claude/reels")
import reel_02 as R
from reel_lib import *
from PIL import ImageFilter
INK, BRAND, RLIGHT, MUTED = R.INK, R.BRAND, R.RLIGHT, R.MUTED
WHITE = (252, 252, 250); LINE = (226, 222, 216); GREY = (150, 144, 134)
CAPEND = 999.0
DUR = round(__import__("wave").open("/home/claude/vo7/vo_n.wav").getnframes() / 44100 + 1.3, 1)
WN = json.load(open("/home/claude/vo7/words.json"))
def T(i): return WN[i][1]
def E(i): return WN[i][2]

# ---------- background ----------
def make_bg():
    bg = Image.new("RGB", (W, H), WHITE)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for cx, cy, r, a in ((200, 520, 360, 70), (900, 1380, 420, 55), (780, 300, 240, 40)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BRAND + (a,))
    g = g.filter(ImageFilter.GaussianBlur(150))
    bg.paste(g, (0, 0), g)
    return bg
BG = make_bg()
def arcs(img, t):
    d = ImageDraw.Draw(img, "RGBA")
    for cx, cy, r, ph, sp in ((60, 150, 190, 0, 4), (940, 1700, 300, 90, -3), (1020, 560, 150, 40, 5)):
        a0 = ph + t * sp
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 150, fill=BRAND + (70,), width=3)
        d.arc((cx - r, cy - r, cx + r, cy + r), a0 + 180, a0 + 200, fill=LINE + (255,), width=3)

# ---------- text helpers ----------
_wc = {}
def wl(s, size, wt, col):
    k = (s, size, wt, col)
    if k not in _wc: _wc[k] = text_layer(s, size, wt, col)
    return _wc[k]
def blur_in(img, lay, anc, cx, cy, t, t0, d=0.38, sc=1.0):
    if t < t0: return
    p = clamp((t - t0) / d); e = out_expo(p)
    L = lay
    r = 16 * (1 - e) ** 2
    if r > 0.6: L = lay.filter(ImageFilter.GaussianBlur(r))
    paste_scaled(img, L, anc, cx, cy + 36 * (1 - e), (1.12 - 0.12 * e) * sc, min(1, p * 1.6))
def line(img, t, segs, size, cx, by, times, sp=0.26):
    ws = [text_w(s, int(size * k), wt) for s, wt, c, k in segs]
    gap = size * sp
    tot = sum(ws) + gap * (len(segs) - 1); x = cx - tot / 2
    for (s, wt, c, k), w, t0 in zip(segs, ws, times):
        lay, anc = wl(s, int(size * k), wt, c)
        blur_in(img, lay, anc, x + w / 2, by, t, t0)
        x += w + gap
def sub(img, t, s, t0, cy, size=44, col=MUTED, cx=540):
    lay, anc = wl(s, size, "bold", col)
    blur_in(img, lay, anc, cx, cy, t, t0, 0.4)
S = lambda s, c=INK, k=1.0: (s, "extrabold", c, k)
SE = lambda s, c=BRAND, k=1.25: (s, "serif", c, k)

def ss(w, h, fn, k=2):
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn(d, k)
    return im.resize((w, h), Image.LANCZOS)

def card_shadow(w, h, r=36, fill=(255, 255, 255), outline=LINE, p=60):
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p + 14, p + w, p + h + 14), r, fill=(0, 0, 0, 40))
    lay = lay.filter(ImageFilter.GaussianBlur(18))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), r, fill=fill, outline=outline, width=3)
    return lay, d, p

def person(d, k, cx, cy, s, col):
    d.ellipse(((cx - 0.30 * s) * k, (cy - 0.95 * s) * k, (cx + 0.30 * s) * k, (cy - 0.35 * s) * k), fill=col)
    d.pieslice(((cx - 0.62 * s) * k, (cy - 0.22 * s) * k, (cx + 0.62 * s) * k, (cy + 0.9 * s) * k), 180, 360, fill=col)
    d.rectangle(((cx - 0.62 * s) * k, (cy + 0.34 * s) * k, (cx + 0.62 * s) * k, (cy + 0.38 * s) * k), fill=col)

def wifi(d, k, cx, cy, s, col, w=8):
    for i, r in enumerate((0.9, 0.6, 0.3)):
        d.arc(((cx - r * s) * k, (cy - r * s) * k, (cx + r * s) * k, (cy + r * s) * k), 225, 315, fill=col, width=int(w * k))
    d.ellipse(((cx - 0.08 * s) * k, (cy - 0.08 * s) * k, (cx + 0.08 * s) * k, (cy + 0.08 * s) * k), fill=col)

# ---------- scene 1 elements ----------
def coin(sz=70):
    def f(d, k):
        d.ellipse((4 * k, 4 * k, (sz - 4) * k, (sz - 4) * k), outline=BRAND, width=5 * k)
        d.text((sz / 2 * k, sz / 2 * k), "¥", font=font(int(sz * 0.55) * k, "extrabold"), fill=BRAND, anchor="mm")
    return ss(sz, sz, f), (sz / 2, sz / 2)
COIN, COINA = coin(90)

# ---------- chat scene ----------
def chat_phone():
    w, h = 880, 600
    lay, d, p = card_shadow(w, h, 46)
    d.rounded_rectangle((p, p, p + w, p + 150), 46, fill=(247, 244, 240)); d.rectangle((p, p + 100, p + w, p + 150), fill=(247, 244, 240))
    d.line((p, p + 150, p + w, p + 150), fill=LINE, width=3)
    d.ellipse((p + 40, p + 34, p + 120, p + 114), fill=(214, 208, 198)); draw_text(d, p + 80, p + 92, "?", 52, "extrabold", (255, 255, 255), "m")
    draw_text(d, p + 150, p + 74, "Unknown", 44, "extrabold", INK); draw_text(d, p + 150, p + 118, "陌生人 · WeChat", 30, "bold", MUTED)
    return lay, (p + w / 2, p + h / 2), p
PH, PHA, PHP = chat_phone()
def bubble(txt, size=54, w=None):
    tw = text_w(txt, size, "extrabold"); bw = int(tw + 90); bh = int(size * 1.9)
    lay = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((20, 20, 20 + bw, 20 + bh), 40, fill=(240, 236, 230))
    draw_text(d, 20 + bw / 2, 20 + bh / 2 + size * 0.34, txt, size, "extrabold", INK, "m")
    return lay, (20, 20 + bh / 2), bw
B1 = bubble("Hello handsome"); B2 = bubble("Free Saturday?")

# ---------- two cards: agent vs Kevin ----------
def prof(name, role, kind):
    w, h = 470, 600
    lay, d, p = card_shadow(w, h, 40)
    im = ss(w, h, lambda dd, k: (dd.ellipse((150 * k, 70 * k, 320 * k, 240 * k), fill=(232, 226, 218)),
                                person(dd, k, 235, 205, 105, (190, 182, 170))), 2)
    lay.paste(im, (p, p), im)
    draw_text(d, p + w / 2, p + 340, name, 50 if len(name) > 8 else 60, "extrabold", INK, "m")
    draw_text(d, p + w / 2, p + 400, role, 36, "bold", MUTED, "m")
    d.line((p + 60, p + 450, p + w - 60, p + 450), fill=LINE, width=3)
    if kind == "agent":
        draw_text(d, p + w / 2, p + 520, "Verified?  ???", 38, "mono", MUTED, "m")
    else:
        ic = ss(110, 90, lambda dd, k: wifi(dd, k, 55, 80, 70, BRAND, 9), 2)
        lay.paste(ic, (p + w // 2 - 55, p + 462), ic)
        draw_text(d, p + w - 40, p + 520, "", 10, "bold", MUTED, "r")
    return lay, (p + w / 2, p + h / 2)
CA, CAA = prof("Casting agent", "选角经纪人", "agent")
CK, CKA = prof("Kevin", "Wi-Fi connection", "kevin")
QM, QMA = wl("?", 150, "extrabold", BRAND)
OR, ORA = wl("or", 54, "serif", MUTED)

# ---------- you / they ----------
def duo(col, lbl, zh, dashed):
    w, h = 400, 560
    def f(d, k):
        cx = w / 2
        person(d, k, cx, 280, 150, col)
        if dashed:
            for a in range(0, 360, 20):
                d.arc((20 * k, 20 * k, (w - 20) * k, (w - 20) * k + 0), a, a + 10, fill=GREY + (255,), width=5 * k) if False else None
    im = ss(w, h, f)
    d = ImageDraw.Draw(im)
    draw_text(d, w / 2, 470, lbl, 54, "extrabold", INK, "m"); draw_text(d, w / 2, 525, zh, 34, "bold", MUTED, "m")
    return im, (w / 2, h / 2)
def person_card(col, lbl, zh, q):
    w, h = 400, 600
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pi = ss(w, 360, lambda d, k: person(d, k, 200, 290, 130, col))
    im.paste(pi, (0, 0), pi)
    d = ImageDraw.Draw(im)
    for a in range(0, 360, 18):
        d.arc((60, 70, 340, 350), a, a + 9, fill=GREY, width=5)
    draw_text(d, w / 2, 450, lbl, 54, "extrabold", INK, "m"); draw_text(d, w / 2, 510, zh, 34, "bold", MUTED, "m")
    draw_text(d, w / 2, 90, "?", 110, "extrabold", BRAND, "m")
    return im, (w / 2, h / 2)
YOU, YOUA = person_card((60, 56, 50), "You", "你", True)
THEM, THEMA = person_card((176, 168, 156), "Them", "对方", True)

# ---------- hexagons ----------
def hexagon(kind, size=210):
    def f(d, k):
        c = size / 2
        pts = [(c + (size / 2 - 6) * math.cos(math.radians(60 * i - 90)), c + (size / 2 - 6) * math.sin(math.radians(60 * i - 90))) for i in range(6)]
        d.polygon([(x * k, y * k) for x, y in pts], fill=BRAND)
        wcol = (255, 255, 255); wd = 7 * k
        if kind == "time":
            d.ellipse(((c - 52) * k, (c - 52) * k, (c + 52) * k, (c + 52) * k), outline=wcol, width=wd)
            d.line((c * k, c * k, c * k, (c - 34) * k), fill=wcol, width=wd); d.line((c * k, c * k, (c + 26) * k, (c + 14) * k), fill=wcol, width=wd)
        elif kind == "gig":
            d.rounded_rectangle(((c - 52) * k, (c - 26) * k, (c + 52) * k, (c + 44) * k), 10 * k, outline=wcol, width=wd)
            d.arc(((c - 24) * k, (c - 54) * k, (c + 24) * k, (c - 2) * k), 180, 360, fill=wcol, width=wd)
            d.line(((c - 40) * k, (c + 40) * k, (c + 40) * k, (c - 22) * k), fill=wcol, width=wd)
        else:
            d.polygon([((c - 44) * k, (c - 40) * k), ((c + 44) * k, (c - 40) * k), ((c + 44) * k, (c + 6) * k), (c * k, (c + 52) * k), ((c - 44) * k, (c + 6) * k)], outline=wcol, width=wd)
            d.text((c * k, (c - 6) * k), "?", font=font(60 * k, "extrabold"), fill=wcol, anchor="mm")
    return ss(size, size, f, 3), (size / 2, size / 2)
HX = {k: hexagon(k) for k in ("time", "gig", "trust")}

# ---------- pills ----------
def pill_l(txt, zh, solid, w=900):
    h = 150; p = 24
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if solid: d.rounded_rectangle((p, p, p + w, p + h), 75, fill=BRAND)
    else: d.rounded_rectangle((p, p, p + w, p + h), 75, fill=(255, 255, 255), outline=INK, width=5)
    tc = (255, 255, 255) if solid else INK; zc = (255, 214, 208) if solid else MUTED
    cx0 = p + 90
    d.ellipse((p + 34, p + 45, p + 114, p + 105), fill=None) if False else None
    d.ellipse((p + 30, p + 35, p + 100, p + 105), fill=(255, 255, 255) if solid else BRAND)
    d.line((p + 48, p + 72, p + 62, p + 86), fill=BRAND if solid else (255, 255, 255), width=7); d.line((p + 62, p + 86, p + 84, p + 54), fill=BRAND if solid else (255, 255, 255), width=7)
    draw_text(d, p + 130, p + 78, txt, 52, "extrabold", tc); draw_text(d, p + 130, p + 124, zh, 34, "bold", zc)
    return lay, (p + w / 2, p + h / 2)
PL = [pill_l("Passport-verified people", "护照实名认证", True), pill_l("Agents you can check", "可查证的中介", False),
      pill_l("Blind ratings, both ways", "双向盲评", False), pill_l("No contact details in chat", "聊天中不显示电话和微信号", True)]

# ---------- end ----------
WM, WMA = R.wordmark(160)
def cta(txt):
    w, h, p = 800, 130, 30
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 65, fill=BRAND)
    draw_text(d, p + w / 2, p + 84, txt, 52, "extrabold", (255, 255, 255), "m")
    return lay, (p + w / 2, p + h / 2)
CT, CTA_ = cta("Sign up at laowai.ma")
TAG, TAGA = wl("Foreign talent. Chinese agents. No WeChat chaos.", 36, "bold", MUTED)
TAGZ, TAGZA = wl("外国人才 · 中国经纪人 · 告别微信混乱", 36, "bold", GREY)

# ---------- captions ----------
def groups():
    gs, cur = [], []
    for w, s, e, i in WN:
        if s < CAPEND:
            cur.append((w, s, e))
            if w[-1] in ".,?\"" or len(cur) >= 5: gs.append(cur); cur = []
    if cur: gs.append(cur)
    return gs
GROUPS = groups(); CAPS = {}
def cap_layer(g, active):
    size = 56; maxw = 940
    words = [w for w, s, e in g]; lines, cur = [], []
    for w in words:
        if text_w(" ".join(cur + [w]), size, "extrabold") <= maxw: cur.append(w)
        else: lines.append(cur); cur = [w]
    lines.append(cur)
    lay = Image.new("RGBA", (1000, 80 * len(lines) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k = 0
    for li, ln in enumerate(lines):
        x = 500 - text_w(" ".join(ln), size, "extrabold") / 2; y = 66 + li * 80
        for w in ln:
            draw_text(d, x, y, w, size, "extrabold", BRAND if k == active else INK)
            x += text_w(w + " ", size, "extrabold"); k += 1
    return lay, (500, 66)
for gi, g in enumerate(GROUPS):
    for ai in range(len(g)): CAPS[(gi, ai)] = cap_layer(g, ai)

vo = np.frombuffer(wave.open("/home/claude/vo7/vo_n.wav").readframes(10**9), dtype=np.int16).astype(np.float64) / 32768
ENV = np.array([np.sqrt(np.mean(vo[int(i / FPS * 44100): int((i + 1) / FPS * 44100)] ** 2) + 1e-12) if int(i / FPS * 44100) < len(vo) - 100 else 0.0 for i in range(int(DUR * FPS))])

CUTS = [2.1, 4.6, 8.6, 12.7, 16.5, 20.3, 23.5, 32.4]
def lay_at(*a, **k): return R.lay_at(*a, **k)
def ppop(t, t0, d=0.3): return R.pop_s(t, t0, d)

def scene_of(t):
    k = 0
    for c in CUTS:
        if t >= c: k += 1
    return k
def draw_line_prog(img, p0, p1, p, col=INK, w=4):
    d = ImageDraw.Draw(img)
    x = p0[0] + (p1[0] - p0[0]) * clamp(p); y = p0[1] + (p1[1] - p0[1]) * clamp(p)
    d.line((p0[0], p0[1], x, y), fill=col, width=w)

def frame(i):
    t = i / FPS
    sc = scene_of(t); starts = [0] + CUTS; ts = starts[sc]
    glitch = 0.0
    img = BG.copy(); arcs(img, t)
    # ---- scene 0: Trust is expensive
    if sc == 0:
        for k, (x, y, ph) in enumerate(((820, 420, 0.0), (160, 1130, 1.3), (900, 1250, 2.4), (250, 520, 3.1))):
            if t > T(2) - 0.1:
                yy = y - ((t - T(2)) * 60 + ph * 40) % 120
                paste_scaled(img, COIN, COINA, x, yy, 0.7 + 0.15 * k % 0.3, min(1, (t - T(2) + 0.1) / 0.3) * 0.7)
        # 'Trust' motion-blur zoom
        lay, anc = wl("Trust", 190, "extrabold", INK)
        if t < T(2):
            p = clamp(t / 0.5); e = out_expo(p)
            L = lay.filter(ImageFilter.GaussianBlur(26 * (1 - e) ** 2)) if (1 - e) > 0.05 else lay
            paste_scaled(img, L, anc, 540, 860, 2.2 - 1.2 * e if t < 0.5 else 1.0, min(1, p * 2))
        else:
            line(img, t, [S("Trust"), S("is"), SE("expensive")], 100, 540, 900, [0, T(1), T(2)])
            sub(img, t, "信任，很贵。", T(2) + 0.2, 1040)
    elif sc == 1:
        line(img, t, [S("Every gig")], 120, 540, 760, [T(3)])
        line(img, t, [S("starts the"), SE("same way", BRAND, 1.2)], 88, 540, 920, [T(6), T(8)])
        sub(img, t, "每个机会，开头都一样。", T(8) + 0.2, 1040)
    elif sc == 2:
        lay_at(img, PH, PHA, 540, 820, t, ts, 0.4, rot=0)
        ox, oy = 540 - 880 / 2 - 60, 820 - 760 / 2 - 60 + 60
        paste_scaled(img, wl("WeChat", 34, "bold", GREY)[0], wl("WeChat", 34, "bold", GREY)[1], 540, 1260, 1, min(1, (t - ts) / 0.3)) if False else None
        if t >= T(14): paste_scaled(img, B1[0], B1[1], 540 - 880 / 2 + 60, 820 - 300 + 250, ppop(t, T(14), 0.3), min(1, (t - T(14)) / 0.1))
        if t >= T(16): paste_scaled(img, B2[0], B2[1], 540 - 880 / 2 + 60, 820 - 300 + 390, ppop(t, T(16), 0.3), min(1, (t - T(16)) / 0.1))
        line(img, t, [S("A "), S("stranger")], 96, 540, 330, [T(10), T(11)], 0.2) if False else line(img, t, [S("A stranger"), SE("on WeChat", BRAND, 1.2)], 92, 540, 330, [T(10), T(12)])
    elif sc == 3:
        lay_at(img, CA, CAA, 540 - 255, 800, t, T(21) - 0.2, 0.4, rot=-2)
        lay_at(img, CK, CKA, 540 + 255, 800, t, T(24) - 0.1, 0.4, rot=2)
        if t >= T(28) - 0.1: paste_scaled(img, QM, QMA, 540, 330, ppop(t, T(28) - 0.1, 0.3), 1)
        line(img, t, [S("Casting agent"), SE("or", GREY, 1.1), S("Kevin?")], 78, 540, 410, [T(21), T(23), T(24)], 0.2)
    elif sc == 4:
        lay_at(img, YOU, YOUA, 540 - 250, 880, t, T(29), 0.4)
        lay_at(img, THEM, THEMA, 540 + 250, 880, t, T(32), 0.4)
        line(img, t, [S("You can't"), SE("tell.", BRAND)], 104, 540, 360, [T(29), T(31)])
        line(img, t, [S("Neither can"), SE("they.", BRAND)], 104, 540, 1330 if False else 1320, [T(33), T(34)])
    elif sc == 5:
        line(img, t, [S("Everyone wastes"), SE("time.")], 76, 540, 360, [T(41), T(43)], 0.22)
        line(img, t, [SE("time.")], 130, 540, 480, [T(43)]) if False else None
        pos = [(300, 860, "time", "Wasted time", "浪费时间", T(42)), (780, 860, "gig", "Gigs gone", "机会溜走", T(47)), (540, 1140, "trust", "No trust", "信任归零", T(49) - 0.15)]
        for (x, y, k, a, b, t0) in pos:
            if t >= t0:
                lay, anc = HX[k]
                paste_scaled(img, lay, anc, x, y, ppop(t, t0, 0.35), min(1, (t - t0) / 0.1))
                l1, a1 = wl(a, 40, "extrabold", INK); l2, a2 = wl(b, 30, "bold", MUTED)
                ly = y + 160
                blur_in(img, l1, a1, x, ly, t, t0 + 0.2, 0.3); blur_in(img, l2, a2, x, ly + 46, t, t0 + 0.28, 0.3)
        line(img, t, [S("and good"), SE("gigs", BRAND)], 90, 540, 600 if False else 520, [T(44), T(47)], 0.2) if False else None
    elif sc == 6:
        line(img, t, [S("Great platforms")], 100, 540, 640, [T(50)])
        lay, anc = wl("louder", int(112 * 1.25), "serif", GREY)
        line(img, t, [S("aren't"), SE("louder.", GREY, 1.25)], 112, 540, 800, [T(52), T(53)])
        if t >= T(53) + 0.15:
            wL = text_w("louder.", int(112 * 1.25), "serif"); wA = text_w("aren't", 112, "extrabold"); gap = 112 * 0.26
            tot = wA + gap + wL; x0 = 540 - tot / 2 + wA + gap
            draw_line_prog(img, (x0, 770), (x0 + wL - 20, 770), (t - T(53) - 0.15) / 0.25, BRAND, 8)
        if t >= T(54):
            line(img, t, [S("They're"), SE("clearer.", BRAND, 1.25)], 112, 540, 1050, [T(54), T(55)], 0.4)
    elif sc == 7:
        # pills
        ys = [560, 760, 960, 1160]; ts_ = [T(56), T(58), T(62), T(66)]
        for L, y, t0, r in zip(PL, ys, ts_, (-1, 1, -1, 1)):
            lay_at(img, L[0], L[1], 540, y, t, t0 - 0.05, 0.35, rot=r * 0.6)
        line(img, t, [S("Not louder."), SE("Clearer.", BRAND)], 84, 540, 340, [T(56) - 0.3, T(56) - 0.1])
    else:
        sp = ENV[min(i, len(ENV) - 1)]
        mouth = "big" if sp > 0.12 else ("o" if sp > 0.05 else "smile")
        lay_at(img, WM, WMA, 540, 420, t, 32.4, 0.4)
        lay_at(img, R.masc(mouth, (0, 0), blink=(t % 2.3) < 0.1), R.MA, 540, 800 - 6 * math.sin(t * 6), t, 32.7, 0.4, sc=0.88)
        blur_in(img, TAG, TAGA, 540, 1100, t, 33.0, 0.4); blur_in(img, TAGZ, TAGZA, 540, 1155, t, 33.1, 0.4)
        lay_at(img, CT, CTA_, 540, 1330, t, T(78) - 0.1, 0.35)
    # ---- captions
    if t < 32.3:
        for gi, g in enumerate(GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.2:
                ai = 0
                for k, (w, s, e) in enumerate(g):
                    if t >= s - 0.02: ai = k
                Lc, Ac = CAPS[(gi, ai)]
                paste_scaled(img, Lc, Ac, 540, 1560, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06))
                break
    # camera: slow push per scene + hard glitch-free
    p = clamp((t - ts) / max(0.5, (CUTS[sc] if sc < len(CUTS) else DUR) - ts))
    zoom = 1.0 + 0.035 * p
    img = camera(img, zoom=zoom)
    fade = clamp((DUR - t) / 0.3) if t > DUR - 0.3 else 1.0
    return post(img, i, glitch=0.0, grain=0.25, vignette=0.0, fade=fade)

def build_audio(path):
    m = Mix(DUR)
    x = vo / (np.max(np.abs(vo)) + 1e-9) * 0.82
    voice = np.zeros(m.n); voice[:min(len(x), m.n)] = x[:m.n]
    bed = Mix(DUR)
    for c in CUTS: bed.add(c - 0.28, whoosh(0.3, 0.5), 0.9); bed.add(c, boom(), 0.25)
    for k in (0, 1, 2): bed.add(T(k), tick(), 0.8)
    for k in (3, 6, 10, 12, 21, 24, 29, 31, 33, 34, 42, 50, 52, 53, 54, 55, 62, 66): bed.add(T(k), tick(), 0.5)
    for k in (14, 16): bed.add(T(k), pop(), 0.8)
    bed.add(T(28) - 0.1, pop(), 0.9); bed.add(T(42), pop(), 0.7); bed.add(T(47), pop(), 0.7); bed.add(T(49) - 0.15, pop(), 0.7)
    for k in (56, 58, 62, 66): bed.add(T(k) - 0.05, pop(), 0.9); bed.add(T(k), pluck(660), 0.35)
    bed.add(T(53) + 0.15, whoosh(0.25, 0.4), 0.8)
    for tt, f in ((32.4, 330), (32.9, 392), (33.4, 494), (33.9, 392)): bed.add(tt, pluck(f), 0.5)
    for k in range(int(32 / 0.6)):
        if k % 2 == 0: bed.add(k * 0.6, kick(), 0.18)
        bed.add(k * 0.6 + 0.3, hat(), 0.12)
    b = hp(bed.buf.copy(), 40)
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
    b = b * (1 - 0.6 * np.clip(env / 0.08, 0, 1)) * 0.6
    y = voice + b
    y = np.tanh(y * 1.1) / np.tanh(1.1); y = y / (np.max(np.abs(y)) + 1e-9) * 0.88
    n = int(0.3 * SR); y[-n:] *= np.linspace(1, 0, n)
    write_wav(path, y)

if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]: Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/r4still_{tt}.png")
    elif sys.argv[1] == "audio": build_audio("out/reel04.wav")
    else:
        build_audio("out/reel04.wav")
        render(frame, int(DUR * FPS), "out/reel04.wav", "out/laowai_reel_04.mp4")
