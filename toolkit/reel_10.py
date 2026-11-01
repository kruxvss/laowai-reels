"""Reel 9 (file 10) - 'More Van Goghs than Van Gogh' (Dafen). Rigged characters, procedural swirl sky."""
import sys, json, math, os, random
sys.path.insert(0, "/home/claude/reels")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel_lib import *
from premium import mblur, tilt, chroma, letters, type3d, wipe_in, glint
from rig import draw_char
import reel_09 as B
from reel09_shim import *  # noqa (helpers re-exported)

VO_DIR = "/home/claude/vo10"
from reel10_lines import LINES
WN = json.load(open(VO_DIR + "/words.json"))
def _n(w): return "".join(ch for ch in w.lower() if ch.isalnum())
LS = [min(w[1] for w in WN if w[3] == i) for i in range(len(LINES))]
LE = [max(w[2] for w in WN if w[3] == i) for i in range(len(LINES))]
def tw(word, line, nth=0):
    c = [w for w in WN if w[3] == line and _n(w[0]) == _n(word)]
    return c[min(nth, len(c) - 1)][1] if c else LS[line]
DUR = round(LE[-1] + 1.8, 2)
NF = int(DUR * FPS)
SC = [0, LS[1], LS[3], LS[6], LS[9], LS[11], LS[12], LS[14] - 0.15, DUR + 1]
GROUPS = []
for li in range(len(LINES) - 1):
    ws = [(w[0], w[1], w[2]) for w in WN if w[3] == li]; cur = []
    for w in ws:
        cur.append(w)
        if len(cur) >= 5 or w[0][-1] in ".,?:": GROUPS.append(cur); cur = []
    if cur: GROUPS.append(cur)
B.GROUPS = GROUPS

NAVY = (14, 26, 58); COB = (38, 74, 150); OCHRE = (242, 179, 61); PALE = (170, 200, 240)

# ---------- procedural swirl sky (original motif) ----------
_r = random.Random(7)
CENTERS = [(300, 520, 260, 1), (780, 380, 200, -1), (620, 820, 300, 1), (180, 1050, 180, -1), (920, 1000, 220, 1)]
STROKES = []
for i in range(1500):
    x, y = _r.uniform(-40, W + 40), _r.uniform(0, 1500)
    STROKES.append((x, y, _r.uniform(14, 34), _r.choice([COB, COB, PALE, (90, 130, 200), (230, 230, 200), OCHRE if _r.random() < 0.12 else COB]), _r.uniform(0, 6.28)))
def flow(x, y):
    vx, vy = 1.0, 0.15
    for cx, cy, r, s in CENTERS:
        dx, dy = x - cx, y - cy; d2 = dx * dx + dy * dy + 1; w_ = math.exp(-d2 / (2 * r * r)) * 2.4
        vx += -dy / math.sqrt(d2) * w_ * s; vy += dx / math.sqrt(d2) * w_ * s
    n = math.hypot(vx, vy) + 1e-6
    return vx / n, vy / n
def sky(t, key="sky"):
    def base():
        img = grad_bg((10, 20, 50), (24, 46, 100), "skyb")
        return img
    img = base()
    d = ImageDraw.Draw(img, "RGBA")
    ph = t * 0.6
    for (x, y, L, col, p) in STROKES:
        # advect start point along the flow over time (loops)
        xx, yy = x, y
        steps = int((ph * 30 + p * 5) % 6)
        for _ in range(steps):
            vx, vy = flow(xx, yy); xx += vx * 6; yy += vy * 6
        pts = [(xx, yy)]
        for _ in range(3):
            vx, vy = flow(xx, yy); xx += vx * L / 3; yy += vy * L / 3; pts.append((xx, yy))
        d.line(pts, fill=col + (220,), width=7, joint="curve")
    # stars + moon with halos
    for (sx, sy, r) in ((180, 300, 30), (520, 220, 22), (880, 260, 26), (420, 640, 18), (960, 700, 20)):
        for k in range(4, 0, -1):
            rr = r + k * 16 + 4 * math.sin(t * 2 + sx)
            d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), outline=(250, 220, 120, 70 + 30 * (4 - k)), width=6)
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 230, 140, 255))
    d.ellipse((860, 120, 1000, 260), fill=(255, 214, 90, 255)); d.ellipse((890, 110, 1020, 240), fill=(10, 20, 50, 255))
    return img
def sky_cached(t):
    k = int(t * 12)  # sky animates at 12 fps (painterly)
    return C(("sky", k), lambda: sky(k / 12)).copy()

def hill(img, y0=1350, col=(20, 34, 40)):
    d = ImageDraw.Draw(img, "RGBA")
    pts = [(0, y0)] + [(x, y0 - 60 * math.sin(x / 260) - 30) for x in range(0, W + 40, 40)] + [(W, H), (0, H)]
    d.polygon(pts, fill=col + (255,))

def easel(img, x, y, s, canvas=None, prog=1.0):
    d = ImageDraw.Draw(img, "RGBA"); wood = (120, 80, 44, 255)
    d.line((x - 120 * s, y, x, y - 560 * s), fill=wood, width=int(12 * s)); d.line((x + 120 * s, y, x, y - 560 * s), fill=wood, width=int(12 * s))
    d.line((x, y - 300 * s, x + 30 * s, y), fill=wood, width=int(10 * s))
    cw, ch = int(300 * s), int(240 * s)
    d.rectangle((x - cw / 2 - 8, y - 520 * s - 8, x + cw / 2 + 8, y - 520 * s + ch + 8), fill=(80, 50, 30, 255))
    if canvas is not None:
        c = canvas.resize((cw, ch))
        if prog < 1:
            m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rectangle((0, 0, int(cw * prog), ch), fill=255)
            bg = Image.new("RGBA", (cw, ch), (246, 240, 226, 255)); bg.paste(c, (0, 0), m); c = bg
        img.paste(c, (int(x - cw / 2), int(y - 520 * s)))
    d.rectangle((x - cw / 2 - 20, y - 520 * s + ch + 6, x + cw / 2 + 20, y - 520 * s + ch + 20), fill=wood)
def mini_painting(seed=0):
    def mk():
        im = sky(seed * 0.7).resize((300, 533)).crop((0, 140, 300, 380))
        return im
    return C(("minip", seed), mk)

def stack(img, x, ybase, n_px, w=170, col_seed=0):
    d = ImageDraw.Draw(img, "RGBA"); rnd = random.Random(col_seed)
    y = ybase; k = 0
    while y > ybase - n_px and y > -40:
        sh = 18; c = rnd.choice([(46, 80, 160), (240, 190, 70), (70, 110, 190), (220, 220, 200)])
        off = rnd.uniform(-10, 10)
        d.rounded_rectangle((x - w / 2 + off, y - sh, x + w / 2 + off, y), 4, fill=(84, 56, 34, 255))
        d.rectangle((x - w / 2 + off + 6, y - sh + 3, x + w / 2 + off - 6, y - 3), fill=c + (255,))
        y -= sh + 2; k += 1

def alley_bg():
    def mk():
        bg = grad_bg((255, 214, 170), (240, 180, 140), "alley")
        d = ImageDraw.Draw(bg, "RGBA"); rnd = random.Random(3)
        # two walls in perspective covered in canvases
        d.polygon([(0, 200), (380, 700), (380, 1400), (0, 1800)], fill=(200, 170, 140, 255))
        d.polygon([(W, 200), (700, 700), (700, 1400), (W, 1800)], fill=(188, 158, 128, 255))
        d.polygon([(380, 1400), (700, 1400), (W, 1920), (0, 1920)], fill=(150, 120, 100, 255))
        for side in (0, 1):
            for r in range(9):
                for cidx in range(4):
                    u = (cidx + 0.5) / 4; v = (r + 0.5) / 9
                    if side == 0:
                        x0 = u * 380; ytop = 200 + (700 - 200) * u; ybot = 1800 + (1400 - 1800) * u
                    else:
                        x0 = W - u * 380; ytop = 200 + (700 - 200) * u; ybot = 1800 + (1400 - 1800) * u
                    yy = ytop + (ybot - ytop) * v; sz = 60 * (1 - u * 0.55)
                    c = rnd.choice([(40, 70, 150), (240, 190, 70), (200, 70, 50), (60, 140, 90), (230, 220, 200)])
                    d.rectangle((x0 - sz * 0.8, yy - sz * 0.6, x0 + sz * 0.8, yy + sz * 0.6), fill=(90, 60, 40, 255))
                    d.rectangle((x0 - sz * 0.8 + 5, yy - sz * 0.6 + 5, x0 + sz * 0.8 - 5, yy + sz * 0.6 - 5), fill=c + (255,))
        # far opening
        d.rectangle((380, 700, 700, 1400), fill=(255, 236, 200, 255))
        return bg
    return C("alley", mk).copy()
def field_bg():
    def mk():
        bg = grad_bg((250, 220, 160), (200, 220, 140), "field")
        d = ImageDraw.Draw(bg, "RGBA")
        d.ellipse((700, 260, 900, 460), fill=(255, 240, 190, 255))
        for i in range(12):
            y = 1000 + i * 80
            d.rectangle((0, y, W, y + 50), fill=(90 + i * 4, 150 + i * 3, 70, 255))
            for x in range(10, W, 44): d.line((x, y + 50, x + 6, y + 10), fill=(60, 120, 50, 255), width=5)
        return bg
    return C("field", mk).copy()

def workshop_bg():
    def mk():
        bg = grad_bg((44, 30, 26), (20, 14, 12), "work")
        d = ImageDraw.Draw(bg, "RGBA")
        d.rectangle((0, 1380, W, H), fill=(60, 40, 30, 255))
        for x in range(80, W, 180): d.ellipse((x - 40, 80, x + 40, 160), fill=(255, 220, 160, 50))
        return bg
    return C("workbg", mk).copy()
def order_slip():
    def mk():
        w, h = 700, 460
        lay = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rectangle((50, 56, 50 + w, 56 + h), fill=(0, 0, 0, 110)); lay = lay.filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(lay)
        d.rectangle((40, 40, 40 + w, 40 + h), fill=(250, 248, 240, 255))
        for y in range(120, h, 46): d.line((70, 40 + y, w + 10, 40 + y), fill=(200, 210, 230), width=2)
        draw_text(d, 80, 120, "PURCHASE ORDER", 40, "mono", (60, 60, 70))
        draw_text(d, 40 + w / 2, 270, "50,000", 150, "extrabold", BRAND, "m")
        draw_text(d, 40 + w / 2, 340, "OIL PAINTINGS", 44, "extrabold", INK, "m")
        draw_text(d, 40 + w / 2, 430, "DEADLINE: 14 DAYS", 46, "mono", (60, 60, 70), "m")
        return lay, (lay.size[0] / 2, lay.size[1] / 2)
    return C("slip", mk)
def calendar(n):
    def mk():
        lay = Image.new("RGBA", (300, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((10, 30, 290, 330), 24, fill=(250, 248, 244, 255)); d.rounded_rectangle((10, 30, 290, 110), 24, fill=BRAND); d.rectangle((10, 80, 290, 110), fill=BRAND)
        draw_text(d, 150, 90, "DAYS LEFT", 30, "extrabold", (255, 255, 255), "m")
        draw_text(d, 150, 260, str(n), 140, "extrabold", INK, "m")
        for x in (80, 220): d.rounded_rectangle((x - 10, 10, x + 10, 60), 8, fill=(60, 60, 60))
        return lay, (150, 180)
    return C(("cal", n), mk)
def plane(img, x, y, s, ang):
    lay = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((40, 135, 260, 165), 15, fill=(250, 250, 250)); d.polygon([(130, 150), (190, 150), (120, 60), (100, 60)], fill=(230, 230, 236))
    d.polygon([(130, 150), (190, 150), (120, 240), (100, 240)], fill=(230, 230, 236)); d.polygon([(40, 150), (70, 150), (50, 100), (36, 100)], fill=BRAND)
    lay = lay.rotate(-ang, Image.BICUBIC)
    paste_scaled(img, lay, (150, 150), x, y, s, 1)
def museum_bg():
    def mk():
        bg = grad_bg((236, 230, 220), (214, 206, 194), "mus")
        d = ImageDraw.Draw(bg, "RGBA")
        d.rectangle((0, 1300, W, H), fill=(150, 110, 80, 255))
        for i, (x, y, w, h) in enumerate(((120, 380, 330, 260), (600, 330, 380, 300), (300, 800, 260, 340), (700, 820, 280, 220))):
            d.rectangle((x - 18, y - 18, x + w + 18, y + h + 18), fill=(176, 140, 60, 255))
            p = mini_painting(i + 1).resize((w, h)); bg.paste(p, (x, y))
            d.ellipse((x + w / 2 - 120, y - 120, x + w / 2 + 120, y - 20), fill=(255, 250, 220, 40))
        return bg
    return C("museum", mk).copy()
def stall_bg():
    def mk():
        bg = grad_bg((120, 170, 210), (190, 210, 230), "stall")
        d = ImageDraw.Draw(bg, "RGBA")
        for x in range(0, W, 200):
            d.rectangle((x, 300, x + 180, 1300), fill=(150, 90, 60, 255)); d.polygon([(x - 10, 300), (x + 190, 300), (x + 90, 200)], fill=(120, 60, 40, 255))
        d.rectangle((0, 1300, W, H), fill=(120, 110, 100, 255))
        d.rectangle((60, 620, 1020, 1320), fill=(230, 210, 170, 255))
        for i, (x, y) in enumerate(((120, 680), (420, 680), (720, 680), (120, 980), (720, 980))):
            p = mini_painting(i + 3).resize((240, 190)); d.rectangle((x - 8, y - 8, x + 248, y + 198), fill=(70, 50, 30, 255)); bg.paste(p, (x, y))
        return bg
    return C("stall", mk).copy()
def tag(txt, col):
    def mk():
        w = int(text_w(txt, 44, "extrabold")) + 80
        lay = Image.new("RGBA", (w + 40, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.polygon([(20, 70), (60, 20), (w + 20, 20), (w + 20, 120), (60, 120)], fill=col)
        d.ellipse((50, 60, 70, 80), fill=(255, 255, 255))
        draw_text(d, 70 + (w - 50) / 2, 88, txt, 44, "extrabold", (255, 255, 255), "m")
        return lay, (lay.size[0] / 2, 70)
    return C(("tag", txt, col), mk)
def tickmark(img, x, y, s, good, p):
    d = ImageDraw.Draw(img, "RGBA"); col = (60, 200, 120, 255) if good else (230, 60, 50, 255)
    d.ellipse((x - 40 * s, y - 40 * s, x + 40 * s, y + 40 * s), fill=col)
    if good:
        pts = [(x - 18 * s, y), (x - 4 * s, y + 14 * s), (x + 20 * s, y - 14 * s)]
        d.line(pts[:2] if p < 0.5 else pts, fill=(255, 255, 255, 255), width=int(9 * s), joint="curve")
    else:
        d.line((x - 15 * s, y - 15 * s, x + 15 * s, y + 15 * s), fill=(255, 255, 255, 255), width=int(9 * s))
        if p > 0.5: d.line((x + 15 * s, y - 15 * s, x - 15 * s, y + 15 * s), fill=(255, 255, 255, 255), width=int(9 * s))

# ================= SCENES =================
def zhao_paint(img, x, y, s, t, face=1, mood="focus"):
    st = math.sin(t * 9)
    draw_char(img, x, y, s, "zhao", face=face, hand_prop="brush", brush_ang=-30 + 30 * st, armR=(60 + 25 * st, 110 + 30 * st),
              mouth="smile" if mood == "focus" else mood, look=(0.6 * face, -0.2), brow=0.2, rim=(255, 210, 140))

def s0_hook(t):
    img = sky_cached(t); hill(img)
    canvas = mini_painting(0)
    easel(img, 700, 1500, 1.3, canvas, clamp(0.35 + t / 2.5))
    zhao_paint(img, 330, 1560, 1.3, t)
    L, A = T3("MORE VAN GOGHS", 120, "gold", 12)
    if t > tw("more", 0) - 0.1:
        g = glint(L, clamp((t - tw("van", 0) - 0.1) / 0.7), 0.16, 0.9)
        slam(img, g, A, 540, 300, t, tw("more", 0) - 0.1, 0.3, 1.7)
    Ls, As = TL("than Van Gogh.", 96, "serif", (255, 236, 190))
    if t > tw("than", 0) - 0.05:
        p = clamp((t - tw("than", 0) + 0.05) / 0.35); paste_scaled(img, Ls, As, 540, 430 + 30 * (1 - out_cubic(p)), 1, p)
    z = 1.18 - 0.18 * out_cubic(clamp(t / SC[1]))
    return cam(img, z, 540, 1000)

def s1_count(t):
    t0 = SC[1]; rt = t - t0
    img = grad_bg((18, 24, 50), (8, 10, 24), "cnt")
    glow(img, 760, 900, 600, (242, 179, 61), 0.25)
    # left: Van Gogh 860
    pv = clamp((t - tw("860", 1) + 0.2) / 0.8)
    stack(img, 280, 1500, 120 * out_cubic(pv), 160, 1)
    v = int(860 * out_cubic(pv))
    L, A = T3(f"{v}", 150, "white", 12); paste_scaled(img, L, A, 280, 1150, 1, min(1, pv * 3))
    Ln, An = TL("VAN GOGH", 40, "extrabold", (200, 210, 240)); paste_scaled(img, Ln, An, 280, 1570, 1, 1)
    if t < tw("hundred", 2) - 0.4:
        Lq, Aq = T3("?", 420, "gold", 24); paste_scaled(img, Lq, Aq, 780, 900 + 12 * math.sin(t * 3), 1, clamp(rt / 0.4))
        Lz0, Az0 = TL("ZHAO?", 48, "extrabold", (255, 214, 140)); paste_scaled(img, Lz0, Az0, 780, 1250, 1, clamp(rt / 0.4))
    # right: Zhao 100,000+
    pz = clamp((t - tw("hundred", 2) + 0.4) / 1.2)
    stack(img, 780, 1500, 2200 * out_cubic(pz), 200, 2)
    z_ = int(100000 * out_cubic(pz))
    Lz, Az = T3(f"{z_:,}" + ("+" if pz >= 1 else ""), 150, "gold", 12)
    if pz > 0:
        paste_scaled(img, Lz, Az, 780, 520 if pz < 1 else 520, 0.85 + 0.15 * out_back(pz), 1)
    if t > tw("zhao", 2) - 0.1:
        Lp, Ap = pill("ZHAO XIAOYONG · 赵小勇", 34, (255, 255, 255, 240), INK); fly(img, Lp, Ap, 780, 1570, t, tw("zhao", 2) - 0.1, (300, 0), 0.3)
        draw_char(img, 960, 1500, 0.55, "zhao", face=-1, mouth="grin", armR=(150, 170), eyes=1.1)
    tilt_up = out_cubic(clamp((t - tw("hundred", 2)) / 1.0))
    img = cam(img, 1.0 + 0.1 * tilt_up, 640, 960 - 200 * tilt_up)
    if rt < 0.15: img = hblur(img, 50 * (1 - rt / 0.15))
    return img

def s2_dafen(t):
    t0 = SC[2]; rt = t - t0
    ta = tw("dafen", 4) - 0.2
    if t < ta:
        img = field_bg()
        p = clamp((t - t0) / max(0.5, ta - t0))
        draw_char(img, 200 + 500 * p, 1500, 1.25, "farmer", walk=t * 9, amp=1, mouth="smile", look=(0.4, 0))
        Lf, Af = T3("A FARMER.", 150, "ink", 12); slam(img, Lf, Af, 540, 420, t, tw("farmer", 3) - 0.1, 0.3)
        if rt < 0.15: img = hblur(img, 50 * (1 - rt / 0.15))
        return img
    img = alley_bg()
    pz = clamp((t - ta) / 0.5)
    # painters in doorways (background loop animation)
    for (x, s, f, ph) in ((170, 0.75, 1, 0), (900, 0.75, -1, 1.3), (330, 0.5, 1, 2.1), (760, 0.5, -1, 0.7)):
        st = math.sin(t * 8 + ph)
        draw_char(img, x, 1300 + (1 - s) * 400, s, "painter2" if ph else "zhao", face=f, hand_prop="brush", armR=(70 + 25 * st, 120 + 25 * st), brush_ang=-20 + 30 * st, mouth="smile")
    draw_char(img, 540, 1640, 1.15, "zhao", walk=t * 9, amp=1 if t < LS[5] else 0, mouth="grin", look=(0, -0.3), armR=(14, 8) if t < LS[5] else (140, 160))
    Lp, Ap = pill("DAFEN · 大芬村 · SHENZHEN", 38, BRAND + (255,), (255, 255, 255))
    fly(img, Lp, Ap, 540, 240, t, tw("dafen", 4) - 0.1, (0, -200), 0.3)
    Lt, At = T3("THOUSANDS", 130, "white", 12); slam(img, Lt, At, 540, 420, t, tw("thousands", 4) - 0.1, 0.3)
    Lc, Ac = TL("of painters copying masterpieces", 48, "extrabold", INK)
    paste_scaled(img, Lc, Ac, 540, 520, 1, clamp((t - tw("painters", 4)) / 0.3))
    if t > LS[5] - 0.1:
        Lb, Ab = T3("BY HAND.", 170, "red", 16)
        slam(img, Lb, Ab, 540, 1000, t, LS[5] - 0.1, 0.25, 2.0, -8)
    img = cam(img, 1.15 - 0.15 * out_cubic(pz), 540, 1000)
    if pz < 0.3: img = hblur(img, 40 * (1 - pz / 0.3))
    return img

def s3_order(t):
    t0 = SC[3]; rt = t - t0
    img = workshop_bg()
    # 1989 and multiplying easels
    tm = tw("one", 6) - 0.1
    n = 1 if t < tm else min(24, 1 + int((t - tm) * 18))
    for i in range(n):
        col, row = i % 6, i // 6
        x = 540 if n == 1 else 110 + col * 172; y = 1500 if n == 1 else 900 + row * 170
        s = 0.9 if n == 1 else 0.32
        easel(img, x, y, s, mini_painting(i % 5), 1.0)
    Ly, Ay = T3("1989", 220, "gold", 18); slam(img, Ly, Ay, 540, 330, t, tw("1989", 6) - 0.1, 0.3)
    ts = tw("ordered", 7) - 0.2
    if t > ts:
        dark = Image.new("RGBA", (W, H), (0, 0, 0, int(160 * clamp((t - ts) / 0.2)))); img.alpha_composite(dark)
        Lo, Ao = order_slip(); p = clamp((t - ts) / 0.28)
        paste_scaled(img, Lo, Ao, 540, 820, 1.6 - 0.6 * out_expo(p), min(1, p * 3), 8 * (1 - p) - 3)
        if p < 1: img = chroma(img, 10 * (1 - p))
        Lw, Aw = pill("REPORTEDLY · 据报道", 30, (255, 255, 255, 230), INK); paste_scaled(img, Lw, Aw, 540, 520, 1, clamp((t - ts - 0.3) / 0.3))
    td = tw("fourteen", 8) - 0.15
    if t > td:
        k = clamp((t - td) / max(0.4, LE[8] - td + 0.3)); nday = max(0, 14 - int(k * 14))
        Lc, Ac = calendar(nday); paste_scaled(img, Lc, Ac, 540, 1360, 1 + 0.05 * math.sin(t * 30), 1, 3 * math.sin(t * 20))
    if rt < 0.15: img = vblur(img, 50 * (1 - rt / 0.15))
    return img

def s4_amsterdam(t):
    t0 = SC[4]; rt = t - t0
    tm = tw("real", 9) - 0.1
    tf = tw("finds", 10) - 0.15
    if t < tm:
        img = sky_cached(t)
        d = ImageDraw.Draw(img, "RGBA")
        p = clamp((t - t0) / max(0.5, tm - t0))
        ax, ay, bx, by = 820, 1250, 260, 520
        pts = []
        for k in range(40):
            u = k / 39; x = ax + (bx - ax) * u; y = ay + (by - ay) * u - math.sin(u * math.pi) * 240
            pts.append((x, y))
        for k in range(0, int(40 * p) - 1, 2): d.line((pts[k], pts[k + 1]), fill=(255, 255, 255, 220), width=6)
        for (x, y, lbl) in ((ax, ay, "SHENZHEN 深圳"), (bx, by, "AMSTERDAM")):
            d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=BRAND + (255,), outline=(255, 255, 255, 255), width=4)
            L, A = pill(lbl, 30, (255, 255, 255, 235), INK); paste_scaled(img, L, A, x, y + 60, 1, 1)
        k = min(39, int(39 * p)); k2 = min(39, k + 1)
        ang = math.degrees(math.atan2(pts[k2][1] - pts[k][1], pts[k2][0] - pts[k][0])) if k2 != k else 200
        plane(img, pts[k][0], pts[k][1], 0.6, ang)
        return img
    if t < tf:
        img = museum_bg()
        p = clamp((t - tm) / 0.6)
        draw_char(img, 540, 1640, 1.3, "zhao", face=1, look=(0, -1), eyes=1.3, brow=0.9, mouth="o", bob=0, rim=(255, 240, 200))
        glow(img, 540, 600, 500, (255, 250, 220), 0.3)
        Lf, Af = T3("THE REAL ONES.", 110, "ink", 10); slam(img, Lf, Af, 540, 200, t, tm + 0.1, 0.3)
        img = cam(img, 1.0 + 0.08 * out_cubic(p), 540, 900)
        if p < 0.2: img = hblur(img, 50 * (1 - p / 0.2))
        return img
    img = stall_bg()
    p = clamp((t - tf) / 0.5)
    draw_char(img, 860, 1700, 1.2, "zhao", face=-1, look=(-0.6, -0.2), eyes=1.3 if t < tw("paid", 10) else 0.9, brow=0.9 if t < tw("paid", 10) else -0.5,
              mouth="o" if t < tw("paid", 10) else "flat", rim=(255, 230, 200))
    Ls, As = tag("SOUVENIR", BRAND + (255,)); fly(img, Ls, As, 300, 600, t, tw("souvenirs", 10) - 0.1, (-300, 0), 0.3)
    Lb, Ab = tag("SOLD FOR: A LOT", (40, 120, 70, 255)); fly(img, Lb, Ab, 380, 1420, t, tw("far", 10) - 0.1, (-400, 0), 0.3)
    Lp, Ap = tag("PAID: A LITTLE", (90, 90, 90, 255)); fly(img, Lp, Ap, 380, 1540, t, tw("paid", 10) - 0.1, (-400, 0), 0.3)
    Lh, Ah = T3("HIS OWN PAINTINGS.", 96, "white", 9); slam(img, Lh, Ah, 540, 220, t, tw("own", 10) - 0.1, 0.3)
    img = cam(img, 1.12 - 0.12 * out_cubic(p), 600, 1000)
    if p < 0.25: img = hblur(img, 40 * (1 - p / 0.25))
    return img

def s5_connection(t):
    t0 = SC[5]; rt = t - t0
    img = grad_bg((12, 14, 30), (4, 4, 10), "conn")
    particles(img, t, 50, 31, (200, 210, 255), (0, 0, W, H), 10, 80)
    for (x, lbl, wd, good) in ((250, "THE TALENT", "talent", True), (830, "THE CONNECTION", "connection", False)):
        ta = tw(wd, 11) - 0.1
        if t < ta: continue
        p = clamp((t - ta) / 0.35)
        glow(img, x, 900, 220, (255, 220, 160) if good else (255, 120, 110), 0.6 * p)
        d = ImageDraw.Draw(img, "RGBA"); d.ellipse((x - 26, 874, x + 26, 926), fill=(255, 245, 220, 255))
        L, A = T3(lbl, 64 if good else 56, "white", 6, maxw=480); paste_scaled(img, L, A, x, 700, out_back(p, 1.8), 1)
        tickmark(img, x, 1080, 1.2, good, clamp((t - ta - 0.2) / 0.4))
    # brush stroke connecting
    tc = tw("connection", 11) + 0.3
    if t > tc:
        p = out_cubic(clamp((t - tc) / 0.6)); d = ImageDraw.Draw(img, "RGBA")
        x1 = 250 + (830 - 250) * p
        pts = [(250 + (x1 - 250) * u, 900 - 60 * math.sin(u * math.pi)) for u in np.linspace(0, 1, 30)]
        d.line(pts, fill=OCHRE + (255,), width=16, joint="curve")
    Lh, Ah = TL("was never the problem.", 56, "extrabold", (220, 226, 255))
    paste_scaled(img, Lh, Ah, 540, 420, 1, clamp((t - tw("never", 11)) / 0.3))
    if rt < 0.15: img = hblur(img, 50 * (1 - rt / 0.15))
    return img

def s6_laowai(t):
    t0 = SC[6]; rt = t - t0
    img = B.city_bg(); glow(img, 540, 800, 700, BRAND, 0.45)
    pc = clamp(rt / 0.9)
    for i, (lbl, x, y, d0, rot, sc) in enumerate(B.BUB[:16]):
        e = in_out(clamp(pc * 1.4 - i * 0.03))
        if e >= 1: continue
        L, A = B.job_bubble(lbl, i)
        paste_scaled(img, L, A, x + (540 - x) * e, y + (760 - y) * e, sc * (1 - 0.8 * e), 1 - e, rot * (1 - e))
    pu = clamp((rt - 0.4) / 0.5)
    Lp, Ap = B.phone_ui(clamp((rt - 0.7) / 1.0))
    if pu > 0:
        Lt, At = tilt(Lp, 8 * (1 - pu), -10 + 6 * math.sin(rt * 1.2))
        paste_scaled(img, Lt, At, 540, 640, 0.3 + 0.5 * out_back(pu, 1.4), min(1, pu * 3))
    for k, (wd, y, col, word) in enumerate((("EVERY JOB.", 1200, "white", "job"), ("EVERY AGENT.", 1330, "white", "agent"), ("ONE PLACE.", 1490, "gold", "place"))):
        L, A = T3(wd, 104 if k < 2 else 130, col, 10); slam(img, L, A, 540, y, t, tw(word, 13) - 0.12, 0.28, 1.5)
    Lf, Af = TL("for foreigners in China", 52, "extrabold", (255, 226, 214))
    if t < LS[13] - 0.1: paste_scaled(img, Lf, Af, 540, 1250, 1, clamp((t - tw("foreigners", 12)) / 0.3))
    if rt < 0.15: img = hblur(img, 50 * (1 - rt / 0.15))
    return img

def s7_end(t):
    t0 = SC[7]; rt = t - t0
    img = sky_cached(t); hill(img, 1500)
    tint = Image.new("RGBA", (W, H), (120, 10, 14, 120)); img.alpha_composite(tint)
    re = clamp(rt / 0.35)
    L, A = T3("laowai吗", 200, "white", 18, maxw=900); L = glint(L, clamp((rt - 0.3) / 0.8), 0.18, 0.9)
    paste_scaled(img, L, A, 540, 520, 0.7 + 0.3 * out_back(re, 1.8), min(1, re * 2))
    Lp, Ap = pill("laowai.ma", 54, (255, 255, 255, 255), BRAND); fly(img, Lp, Ap, 540, 720, t, t0 + 0.25, (0, 120), 0.35)
    Ls, As = TL("The talent was never the problem.", 44, "bold", (255, 236, 220)); paste_scaled(img, Ls, As, 540, 840, 1, clamp((rt - 0.5) / 0.3))
    # replay loop: Zhao lifts brush to a fresh canvas
    easel(img, 700, 1800, 1.0, mini_painting(0), clamp((rt - 0.6) / 2.0))
    zhao_paint(img, 380, 1840, 1.0, t)
    if re < 1: img = chroma(img, 8 * (1 - re))
    return img

SCENES = [s0_hook, s1_count, s2_dafen, s3_order, s4_amsterdam, s5_connection, s6_laowai, s7_end]
def scene_of(t):
    for k in range(len(SC) - 1):
        if SC[k] <= t < SC[k + 1]: return k
    return len(SC) - 2
def frame_f(fi):
    t = fi / FPS; s = scene_of(t)
    img = SCENES[s](t)
    if s < 6: B.karaoke(img, t)
    return post(img.convert("RGB"), int(fi), grain=1.0, vignette=0.22)
def frame(i):
    t = i / FPS
    n = 3 if any(abs(t - k) < 0.25 for k in SC[1:-1]) else 1
    return frame_f(i) if n == 1 else mblur(frame_f, i, n, 0.5)

def build_audio(path):
    m = Mix(DUR); beat = 60 / 96
    chords = [(130.8, 164.8, 196), (110, 138.6, 164.8), (98, 123.5, 146.8), (116.5, 146.8, 174.6)]
    t = 0; i = 0
    while t < DUR:
        m.add(t, stab([f * 2 for f in chords[i % 4]], 0.09, beat * 4)); t += beat * 4; i += 1
    t = 0.0
    while t < DUR - 1:
        if not (SC[4] + 1.0 < t < SC[5] + 0.4): m.add(t, kick(0.45)); m.add(t + beat / 2, hat(0.1))
        t += beat
    m.add(tw("more", 0) - 0.1, boom(0.8)); m.add(tw("than", 0), whoosh(0.3, 0.4))
    m.add(SC[1] - 0.2, whoosh(0.5, 0.6, False))
    for k in range(10): m.add(tw("860", 1) - 0.2 + k * 0.08, tick(0.18))
    m.add(tw("hundred", 2) - 0.4, riser(0.6, 0.5)); m.add(tw("thousand", 2), boom(0.9))
    m.add(SC[2], whoosh(0.4, 0.5)); m.add(tw("farmer", 3) - 0.1, kick(0.8))
    m.add(tw("dafen", 4) - 0.25, whoosh(0.5, 0.6)); m.add(tw("thousands", 4) - 0.1, kick(0.7)); m.add(LS[5] - 0.1, boom(0.9)); m.add(LS[5] - 0.1, clap(0.5))
    m.add(SC[3], whoosh(0.4, 0.5, False)); m.add(tw("1989", 6) - 0.1, boom(0.7))
    for k in range(10): m.add(tw("one", 6) + k * 0.06, pop(0.15, 600 + k * 40, 1000 + k * 40))
    m.add(tw("ordered", 7) - 0.2, kick(1.0)); m.add(tw("ordered", 7) - 0.2, clap(0.5))
    m.add(tw("fourteen", 8) - 0.15, bass(55, 0.4, 0.6))
    m.add(SC[4], whoosh(0.9, 0.6)); m.add(tw("real", 9) - 0.1, stab([523, 659, 784], 0.25, 1.5))
    m.add(tw("finds", 10) - 0.15, whoosh(0.3, 0.4)); m.add(tw("souvenirs", 10) - 0.1, pop(0.4))
    m.add(tw("paid", 10) - 0.1, bass(45, 0.6, 0.5))
    m.add(tw("talent", 11) - 0.1, pluck(660, 0.4)); m.add(tw("connection", 11) - 0.1, pluck(440, 0.4)); m.add(tw("connection", 11) + 0.3, whoosh(0.6, 0.4))
    m.add(SC[6], riser(0.5, 0.4)); m.add(SC[6] + 0.5, boom(0.8))
    for w_ in ("job", "agent", "place"): m.add(tw(w_, 13) - 0.12, kick(0.9))
    m.add(SC[7], boom(1.0)); m.add(SC[7] + 0.2, stab([523, 659, 784], 0.3, 1.2))
    x = m.master(0.4)
    import wave
    w = wave.open(VO_DIR + "/vo_n.wav"); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    x = x * 0.3; n = min(len(x), len(v)); x[:n] += v[:n] * 0.95
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    write_wav(path, x)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for a in sys.argv[2:]:
            Image.fromarray(frame_f(int(float(a) * FPS))).save(f"out/v10still_{a}.png")
    elif sys.argv[1] == "render":
        build_audio("out/reel10.wav"); render(frame, NF, "out/reel10.wav", "out/laowai_reel_09.mp4"); print("done", DUR)
