"""Reel 8 (file 09) - 'Said yes to one TV job' (Dashan). Rigged characters + cinematic scenes."""
import sys, json, math, os, random
sys.path.insert(0, "/home/claude/reels")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel_lib import *
from premium import mblur, tilt, chroma, letters, type3d, wipe_in, glint
from rig import draw_char

BRAND = (196, 28, 28); INK = (31, 27, 22); WHITE = (252, 250, 246); GOLD = (255, 214, 140)

# ---------------- timeline ----------------
VO_DIR = "/home/claude/vo9"
LINES = [
    (0.20, 2.50, "A Canadian student said yes to one TV job."),
    (2.60, 5.40, "By morning, hundreds of millions of people knew his face."),
    (5.70, 6.50, "It's 1988."),
    (6.60, 8.90, "Mark Rowswell is studying Chinese in Beijing."),
    (9.00, 11.40, "A TV station wants a foreigner who speaks Mandarin."),
    (11.50, 13.20, "His professors give them his name."),
    (13.50, 18.00, "Months later, he's doing a comedy skit, in Mandarin, on China's biggest night of television."),
    (18.20, 19.30, "He wakes up a star."),
    (19.40, 21.60, "China calls him Dashan. Big Mountain."),
    (21.80, 25.60, "He planned to stay a few years. He's still a household name decades later."),
    (25.80, 28.60, "And it all started with one job he happened to hear about."),
    (28.80, 32.40, "Most people never do. The jobs are out there. They're just scattered."),
    (32.60, 35.00, "So we put every job and every agent in one place."),
    (35.20, 36.20, "laowai.ma"),
]
def _n(w): return "".join(ch for ch in w.lower() if ch.isalnum())
if os.path.exists(VO_DIR + "/words.json"):
    WN = json.load(open(VO_DIR + "/words.json"))  # [word, start, end, line]
else:
    WN = []
    for li, (a, b, txt) in enumerate(LINES):
        ws = txt.split(); tot = sum(len(w) + 1 for w in ws); t = a
        for w in ws:
            d = (b - a) * (len(w) + 1) / tot; WN.append([w, t, t + d * 0.92, li]); t += d
LS = [min(w[1] for w in WN if w[3] == i) for i in range(len(LINES))]
LE = [max(w[2] for w in WN if w[3] == i) for i in range(len(LINES))]
def tw(word, line, nth=0):
    c = [w for w in WN if w[3] == line and _n(w[0]) == _n(word)]
    return c[min(nth, len(c) - 1)][1] if c else LS[line]
DUR = round(LE[-1] + 1.6, 2)
SC = [0, LS[1], LS[2], LS[4], LS[5], LS[6], LS[7], LS[9], LS[10], LS[11], LS[12], DUR + 1]
NF = int(DUR * FPS)
# caption groups: split lines into <=5-word chunks
GROUPS = []
for li in range(len(LINES) - 1):
    ws = [(w[0], w[1], w[2]) for w in WN if w[3] == li]
    cur = []
    for w in ws:
        cur.append(w)
        if len(cur) >= 5 or w[0][-1] in ".,?": GROUPS.append(cur); cur = []
    if cur: GROUPS.append(cur)

# ---------------- helpers ----------------
_cache = {}
def C(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]
def fit(txt, size, wt="extrabold", maxw=960):
    while text_w(txt, size, wt) > maxw and size > 20: size -= 4
    return size
def T3(txt, size, kind="white", depth=None, wt="extrabold", maxw=980):
    P_ = {"white": ((255, 255, 255), (255, 214, 206), (140, 16, 16)), "red": ((255, 96, 84), (196, 28, 28), (96, 8, 8)),
          "ink": ((74, 66, 58), (31, 27, 22), (196, 28, 28)), "gold": ((255, 242, 200), (255, 150, 90), (120, 30, 10)),
          "sepia": ((255, 236, 200), (232, 170, 96), (110, 56, 20))}[kind]
    size = fit(txt, size, wt, maxw)
    d = depth if depth is not None else max(8, int(size * 0.07))
    return C(("t3", txt, size, kind, d, wt), lambda: type3d(txt, size, wt, P_[0], P_[1], P_[2], d))
def TL(txt, size, wt, col, pad=40):
    return C(("tl", txt, size, wt, col), lambda: text_layer(txt, size, wt, col, pad=pad))
def slam(img, lay, anc, cx, cy, t, t0, d=0.32, s0=1.6, rot=0.0):
    if t < t0: return 0
    p = clamp((t - t0) / d); sc = s0 + (1 - s0) * out_expo(p)
    paste_scaled(img, lay, anc, cx, cy, sc, min(1, p * 2.5), rot * (1 - out_expo(p)))
    return p
def fly(img, lay, anc, cx, cy, t, t0, frm=(0, -400), d=0.35, alpha=1.0):
    if t < t0: return
    p = out_back(clamp((t - t0) / d), 1.6)
    paste_scaled(img, lay, anc, cx + frm[0] * (1 - p), cy + frm[1] * (1 - p), 1, alpha * min(1, (t - t0) / 0.1))
def zh(img, s, cx, cy, t, t0, size=40, col=(255, 230, 220), wt="extrabold"):
    if t < t0: return
    L, A = TL(s, size, wt, col); p = clamp((t - t0) / 0.3)
    paste_scaled(img, L, A, cx, cy + 20 * (1 - out_cubic(p)), 1, p)
def pill(txt, size, bg, fg):
    def mk():
        w = int(text_w(txt, size, "extrabold")) + size * 1.4; h = int(size * 1.9)
        lay = Image.new("RGBA", (int(w) + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((20, 20, 20 + w, 20 + h), h // 2, fill=bg)
        draw_text(d, 20 + w / 2, 20 + h / 2 + size * 0.36, txt, size, "extrabold", fg, "m")
        return lay, (lay.size[0] / 2, lay.size[1] / 2)
    return C(("pill", txt, size, bg, fg), mk)
def grad_bg(top, bot, key):
    def mk():
        a = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        arr = np.array(top, np.float32) * (1 - a) + np.array(bot, np.float32) * a
        return Image.fromarray(np.broadcast_to(arr, (H, W, 3)).astype(np.uint8), "RGB").convert("RGBA")
    return C(("bg", key), mk).copy()
def glow(img, cx, cy, r, col, a=0.6):
    key = ("glow", r, col)
    def mk():
        yy, xx = np.mgrid[-r:r, -r:r].astype(np.float32); d = np.sqrt(xx ** 2 + yy ** 2) / r
        al = np.clip(1 - d, 0, 1) ** 2.2
        arr = np.zeros((2 * r, 2 * r, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = (al * 255).astype(np.uint8)
        return Image.fromarray(arr, "RGBA")
    g = C(key, mk)
    if a < 0.999:
        g = g.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(g, (int(cx - r), int(cy - r))) if 0 else img.paste(g, (int(cx - r), int(cy - r)), g)
def hblur(img, amt):
    if amt < 1: return img
    arr = np.asarray(img.convert("RGB")).astype(np.float32); k = int(amt)
    cs = np.cumsum(np.pad(arr, ((0, 0), (k, k), (0, 0)), mode="edge"), axis=1)
    out = (cs[:, 2 * k:] - cs[:, :-2 * k]) / (2 * k)
    return Image.fromarray(out[:, :W].clip(0, 255).astype(np.uint8)).convert("RGBA")
def vblur(img, amt):
    if amt < 1: return img
    return hblur(img.transpose(Image.Transpose.TRANSPOSE).resize((W, H)), 0).transpose(Image.Transpose.TRANSPOSE) if 0 else Image.fromarray(
        _vb(np.asarray(img.convert("RGB")).astype(np.float32), int(amt))).convert("RGBA")
def _vb(arr, k):
    cs = np.cumsum(np.pad(arr, ((k, k), (0, 0), (0, 0)), mode="edge"), axis=0)
    return ((cs[2 * k:] - cs[:-2 * k]) / (2 * k))[:H].clip(0, 255).astype(np.uint8)
def cam(img, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0):
    if abs(zoom - 1) < 1e-3 and abs(cx - W / 2) < 0.5 and abs(cy - H / 2) < 0.5 and not rot: return img
    w2, h2 = W / zoom, H / zoom
    if zoom >= 1:
        cx = min(max(cx, w2 / 2), W - w2 / 2); cy = min(max(cy, h2 / 2), H - h2 / 2)
    box = (cx - w2 / 2, cy - h2 / 2, cx + w2 / 2, cy + h2 / 2)
    out = img.transform((W, H), Image.EXTENT, box, Image.BILINEAR)
    if rot: out = out.rotate(rot, Image.BILINEAR)
    return out
def particles(img, t, n=60, seed=3, col=(255, 230, 200), area=(0, 0, W, H), sp=20, a=120, rad=(2, 5)):
    rnd = random.Random(seed); d = ImageDraw.Draw(img, "RGBA")
    for i in range(n):
        x0 = rnd.uniform(area[0], area[2]); y0 = rnd.uniform(area[1], area[3]); r = rnd.uniform(*rad); ph = rnd.uniform(0, 6.28)
        x = x0 + math.sin(t * 0.6 + ph) * 30; y = area[1] + ((y0 - area[1] - t * sp * (0.5 + r / 5)) % (area[3] - area[1]))
        al = int(a * (0.5 + 0.5 * math.sin(t * 2 + ph)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (al,))

# ---------------- karaoke captions ----------------
def karaoke(img, t, y=1660, dark=True):
    for g in GROUPS:
        if not (g[0][1] - 0.05 <= t <= g[-1][2] + 0.18): continue
        size = 50; ws = [(w, s2, e, text_w(w, size, "extrabold") + 20) for (w, s2, e) in g]
        Wd = sum(x[3] for x in ws) + 56; Hh = 92
        a_in = clamp((t - (g[0][1] - 0.05)) / 0.08); a_out = 1 - clamp((t - (g[-1][2] + 0.04)) / 0.14)
        al = a_in * a_out
        if al <= 0: return
        lay = Image.new("RGBA", (int(Wd) + 80, Hh + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((40, 48, 40 + Wd, 48 + Hh), 46, fill=(0, 0, 0, 110)); lay = lay.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((40, 40, 40 + Wd, 40 + Hh), 46, fill=(255, 255, 255, 246))
        x = 40 + 28; by = 40 + Hh / 2 + 18
        for k, (w, s2, e, ww) in enumerate(ws):
            nxt = ws[k + 1][1] if k + 1 < len(ws) else e + 0.2
            active = s2 - 0.02 <= t < nxt; done = t >= nxt
            col = INK if (active or done) else (160, 152, 140)
            if active:
                d.rounded_rectangle((x - 2, by - 50, x + ww - 18 + 12, by + 14), 22, fill=BRAND); col = (255, 255, 255)
            draw_text(d, x + 4, by, w, size, "extrabold", col)
            x += ww
        paste_scaled(img, lay, (lay.size[0] / 2, 40 + Hh / 2), W / 2, y, 0.92 + 0.08 * out_back(a_in, 2.0), al)
        return

# ================= SCENE ART =================
def studio_bg():
    def mk():
        bg = grad_bg((22, 16, 14), (8, 6, 6), "studio")
        d = ImageDraw.Draw(bg, "RGBA")
        d.ellipse((60, 1180, 1020, 1520), fill=(70, 40, 30, 255))
        bg = bg.filter(ImageFilter.GaussianBlur(40))
        d = ImageDraw.Draw(bg, "RGBA")
        for i in range(9):  # back rigging lights
            x = 80 + i * 115; d.ellipse((x - 14, 180 - 14, x + 14, 180 + 14), fill=(255, 210, 160, 60))
        return bg
    return C("studio", mk).copy()
def cone_layer():
    def mk():
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.polygon([(470, -40), (610, -40), (900, 1420), (180, 1420)], fill=(255, 226, 180, 70))
        d.ellipse((150, 1300, 930, 1500), fill=(255, 220, 170, 110))
        return lay.filter(ImageFilter.GaussianBlur(28))
    return C("cone", mk)

def tv_screen_layer(w, h, on, face=True):
    def mk():
        lay = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((6, 6, 6 + w, 6 + h), 14, fill=(40, 36, 34))
        sc = (14, 14, 14) if not on else (255, 196, 150)
        d.rounded_rectangle((13, 13, w - 1, h - 1), 18, fill=sc)
        if on and face:
            cx, cy = 6 + w / 2, 6 + h / 2 + 4; r = h * 0.28
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(244, 205, 178))
            d.chord((cx - r - 2, cy - r - 4, cx + r + 2, cy + r * 0.3), 180, 360, fill=(176, 120, 66))
            for ex in (-0.35, 0.35):
                d.ellipse((cx + ex * r - 3, cy + r * 0.05 - 3, cx + ex * r + 3, cy + r * 0.05 + 3), fill=(30, 26, 24))
            d.arc((cx - r * 0.35, cy + r * 0.1, cx + r * 0.35, cy + r * 0.55), 20, 160, fill=(90, 36, 30), width=2)
            d.rectangle((cx - r * 1.1, cy + r * 0.95, cx + r * 1.1, cy + r * 1.6), fill=(38, 64, 118))
        return lay
    return C(("tvs", w, h, on, face), mk)
SW, SH_, GAPX, GAPY = 120, 96, 14, 14
COLS, ROWS = 11, 22
def tv_wall(t, t0):
    """returns (wall image W x H, centre screen box)"""
    def mk_static():
        bg = Image.new("RGBA", (W, H), (10, 8, 8, 255))
        return bg
    img = C("wallbg", mk_static).copy()
    ox = (W - (COLS * SW + (COLS - 1) * GAPX)) / 2; oy = (H - (ROWS * SH_ + (ROWS - 1) * GAPY)) / 2
    cc, cr = COLS // 2, ROWS // 2
    rad = (t - t0) * 9.0
    for r in range(ROWS):
        for c in range(COLS):
            x = ox + c * (SW + GAPX); y = oy + r * (SH_ + GAPY)
            dist = math.hypot(c - cc, (r - cr) * 0.8)
            on = dist <= rad
            img.alpha_composite(tv_screen_layer(SW, SH_, on), (int(x - 6), int(y - 6)))
    return img, (ox + cc * (SW + GAPX), oy + cr * (SH_ + GAPY), SW, SH_)

def beijing_layers():
    def mk():
        sky = grad_bg((255, 170, 110), (120, 60, 90), "dusk")
        d = ImageDraw.Draw(sky, "RGBA")
        sky_g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sky_g).ellipse((640, 560, 900, 820), fill=(255, 236, 190, 255))
        sky.alpha_composite(sky_g.filter(ImageFilter.GaussianBlur(6)))
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(halo).ellipse((520, 440, 1020, 940), fill=(255, 220, 160, 120))
        sky.alpha_composite(halo.filter(ImageFilter.GaussianBlur(60)))
        # far: gate tower silhouette (2x width for scroll)
        far = Image.new("RGBA", (W * 2, H), (0, 0, 0, 0)); d = ImageDraw.Draw(far)
        fc = (150, 70, 80, 255)
        for gx in (500, 1500):
            d.rectangle((gx - 260, 900, gx + 260, 1150), fill=fc)
            d.rectangle((gx - 180, 820, gx + 180, 900), fill=fc)
            d.polygon([(gx - 330, 900), (gx + 330, 900), (gx + 230, 850), (gx - 230, 850)], fill=fc)
            d.polygon([(gx - 240, 820), (gx + 240, 820), (gx + 150, 760), (gx - 150, 760)], fill=fc)
            d.polygon([(gx - 360, 905), (gx - 330, 880), (gx - 300, 905)], fill=fc); d.polygon([(gx + 300, 905), (gx + 330, 880), (gx + 360, 905)], fill=fc)
            d.polygon([(gx - 270, 825), (gx - 240, 800), (gx - 210, 825)], fill=fc); d.polygon([(gx + 210, 825), (gx + 240, 800), (gx + 270, 825)], fill=fc)
        d.rectangle((0, 1100, W * 2, 1300), fill=fc)
        # mid: hutong wall with roof tiles + red doors
        mid = Image.new("RGBA", (W * 3, H), (0, 0, 0, 0)); d = ImageDraw.Draw(mid)
        d.rectangle((0, 1060, W * 3, 1420), fill=(120, 112, 118, 255))
        d.rectangle((0, 1040, W * 3, 1072), fill=(70, 62, 70, 255))
        for x in range(0, W * 3, 26): d.ellipse((x, 1026, x + 30, 1052), fill=(80, 70, 78, 255))
        for x in range(160, W * 3, 520):
            d.rectangle((x, 1180, x + 130, 1420), fill=(170, 30, 30, 255)); d.rectangle((x - 12, 1166, x + 142, 1186), fill=(90, 60, 50, 255))
            d.ellipse((x + 50, 1290, x + 62, 1302), fill=(230, 190, 90, 255)); d.ellipse((x + 68, 1290, x + 80, 1302), fill=(230, 190, 90, 255))
            d.ellipse((x + 160, 1110, x + 200, 1160), fill=(230, 60, 40, 255))  # lantern
        # ground
        gnd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(gnd)
        d.rectangle((0, 1410, W, H), fill=(70, 50, 56, 255))
        for i in range(8): d.line((0, 1430 + i * 70, W, 1430 + i * 70), fill=(84, 62, 68, 255), width=3)
        # near: lamp posts + tree silhouettes
        near = Image.new("RGBA", (W * 3, H), (0, 0, 0, 0)); d = ImageDraw.Draw(near)
        for x in range(100, W * 3, 700):
            d.rectangle((x, 700, x + 18, 1700), fill=(40, 26, 30, 255)); d.ellipse((x - 26, 670, x + 44, 730), fill=(255, 220, 150, 255))
        for x in range(450, W * 3, 900):
            d.rectangle((x, 900, x + 30, 1700), fill=(40, 26, 30, 255))
            for k in range(7):
                rr = 110 - k * 6; d.ellipse((x - 120 + k * 30 - rr / 2, 760 + (k % 3) * 50 - rr / 2, x - 120 + k * 30 + rr / 2, 760 + (k % 3) * 50 + rr / 2), fill=(52, 30, 40, 255))
        return sky, far, mid, gnd, near
    return C("bj", mk)

def bike(img, x, y, s, a):
    d = ImageDraw.Draw(img, "RGBA"); r = 70 * s; col = (30, 30, 34, 255)
    w1 = (x - 120 * s, y - r); w2 = (x + 120 * s, y - r)
    for (cx, cy) in (w1, w2):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=int(9 * s))
        for k in range(6):
            an = a + k * math.pi / 3
            d.line((cx, cy, cx + math.cos(an) * r, cy + math.sin(an) * r), fill=(70, 70, 76, 255), width=2)
    crank = (x, y - r)
    d.line((*w1, x - 10 * s, y - 175 * s), fill=BRAND + (255,), width=int(10 * s))
    d.line((x - 10 * s, y - 175 * s, crank[0], crank[1]), fill=BRAND + (255,), width=int(10 * s))
    d.line((crank[0], crank[1], *w1), fill=BRAND + (255,), width=int(10 * s))
    d.line((crank[0], crank[1], x + 90 * s, y - 185 * s), fill=BRAND + (255,), width=int(10 * s))
    d.line((x - 10 * s, y - 175 * s, x + 90 * s, y - 185 * s), fill=BRAND + (255,), width=int(10 * s))
    d.line((x + 90 * s, y - 185 * s, *w2), fill=BRAND + (255,), width=int(10 * s))
    d.line((x + 85 * s, y - 190 * s, x + 80 * s, y - 230 * s), fill=col, width=int(8 * s)); d.line((x + 60 * s, y - 232 * s, x + 110 * s, y - 232 * s), fill=col, width=int(8 * s))
    d.rounded_rectangle((x - 50 * s, y - 192 * s, x + 20 * s, y - 176 * s), int(8 * s), fill=col)
    # basket with books
    d.rectangle((x + 100 * s, y - 240 * s, x + 170 * s, y - 196 * s), outline=(120, 90, 50, 255), width=int(5 * s))
    d.rectangle((x + 108 * s, y - 256 * s, x + 160 * s, y - 238 * s), fill=(230, 210, 160, 255))

def station_art():
    def mk():
        bg = grad_bg((70, 110, 110), (36, 60, 64), "station")
        d = ImageDraw.Draw(bg, "RGBA")
        for x in range(0, W, 90): d.line((x, 0, x, 1200), fill=(255, 255, 255, 14), width=2)
        d.rectangle((0, 1200, W, H), fill=(110, 76, 52, 255)); d.rectangle((0, 1200, W, 1230), fill=(140, 100, 70, 255))
        # monitor with colour bars
        d.rounded_rectangle((640, 330, 1000, 620), 24, fill=(50, 46, 44, 255))
        cols = [(230, 230, 230), (230, 230, 40), (40, 220, 230), (40, 220, 40), (230, 40, 230), (230, 40, 40), (40, 40, 230)]
        for i, c in enumerate(cols): d.rectangle((670 + i * 43, 360, 670 + (i + 1) * 43, 590), fill=c + (255,))
        d.rectangle((0, 1050, W, 1210), fill=(150, 104, 70, 255)); d.rectangle((0, 1050, W, 1070), fill=(176, 126, 86, 255))
        return bg
    return C("station", mk).copy()
def phone_art(ring):
    d = None
    lay = Image.new("RGBA", (380, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((40, 120, 340, 280), 40, fill=(200, 30, 30, 255))
    d.ellipse((120, 140, 260, 270), fill=(240, 236, 228, 255)); d.ellipse((165, 185, 215, 225), fill=(200, 30, 30, 255))
    for k in range(10):
        an = math.radians(200 + k * 14); d.ellipse((190 + math.cos(an) * 46 - 8, 205 + math.sin(an) * 46 - 8, 190 + math.cos(an) * 46 + 8, 205 + math.sin(an) * 46 + 8), fill=(40, 30, 30, 255))
    lift = 26 * abs(math.sin(ring * 40)) if ring else 0
    d.rounded_rectangle((20, 70 - lift, 360, 130 - lift), 30, fill=(170, 20, 20, 255))
    d.ellipse((10, 60 - lift, 90, 140 - lift), fill=(170, 20, 20, 255)); d.ellipse((290, 60 - lift, 370, 140 - lift), fill=(170, 20, 20, 255))
    return lay
def casting_card():
    def mk():
        w, h = 760, 520
        lay = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((52, 60, 52 + w, 60 + h), 30, fill=(0, 0, 0, 120)); lay = lay.filter(ImageFilter.GaussianBlur(16)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((40, 40, 40 + w, 40 + h), 30, fill=(250, 244, 230, 255))
        d.rounded_rectangle((40, 40, 40 + w, 150), 30, fill=BRAND + (255,)); d.rectangle((40, 110, 40 + w, 150), fill=BRAND + (255,))
        draw_text(d, 40 + w / 2, 122, "WANTED", 70, "extrabold", (255, 255, 255), "m")
        draw_text(d, 40 + w / 2, 260, "A FOREIGNER WHO", 54, "extrabold", INK, "m")
        draw_text(d, 40 + w / 2, 340, "SPEAKS MANDARIN", 64, "extrabold", BRAND, "m")
        d.line((120, 380, 40 + w - 80, 380), fill=(220, 210, 190), width=3)
        draw_text(d, 40 + w / 2, 450, "招：会说中文的外国人", 46, "extrabold", (110, 100, 90), "m")
        draw_text(d, 40 + w / 2, 520, "TV STATION · BEIJING · 1988", 30, "mono", (150, 140, 128), "m")
        return lay, (lay.size[0] / 2, lay.size[1] / 2)
    return C("ccard", mk)
def classroom_art():
    def mk():
        bg = grad_bg((236, 226, 206), (210, 196, 172), "class")
        d = ImageDraw.Draw(bg, "RGBA")
        d.rounded_rectangle((70, 260, 1010, 820), 16, fill=(110, 80, 50, 255))
        d.rectangle((90, 280, 990, 800), fill=(46, 84, 64, 255))
        for i, (s, x, y, sz) in enumerate((("你好", 200, 420, 110), ("谢谢", 560, 380, 90), ("相声", 360, 640, 120), ("xiàngsheng", 700, 560, 44))):
            draw_text(d, x, y, s, sz, "extrabold", (236, 240, 230, 220))
        d.line((120, 760, 980, 700), fill=(236, 240, 230, 60), width=4)
        d.rectangle((0, 1250, W, H), fill=(150, 116, 84, 255)); d.rectangle((0, 1250, W, 1270), fill=(170, 134, 100, 255))
        return bg
    return C("class", mk).copy()

def gala_bg():
    def mk():
        bg = grad_bg((60, 6, 10), (14, 2, 4), "gala")
        d = ImageDraw.Draw(bg, "RGBA")
        # back screen
        d.rounded_rectangle((90, 300, 990, 900), 30, fill=(120, 14, 18, 255))
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for i in range(14):
            an = i * math.pi / 7; gd.line((540, 600, 540 + math.cos(an) * 700, 600 + math.sin(an) * 700), fill=(255, 190, 90, 40), width=40)
        bg.alpha_composite(g.filter(ImageFilter.GaussianBlur(8)))
        draw_text(d, 540, 560, "春节联欢晚会", 100, "extrabold", (255, 214, 120), "m")
        draw_text(d, 540, 680, "1989", 70, "mono", (255, 214, 120, 200), "m")
        # stage floor
        d.polygon([(0, 1260), (W, 1260), (W, H), (0, H)], fill=(40, 10, 12, 255))
        d.ellipse((120, 1230, 960, 1420), fill=(150, 60, 40, 255))
        bg2 = bg.filter(ImageFilter.GaussianBlur(1))
        return bg2
    return C("gala", mk).copy()
def curtain(side, openp):
    def mk():
        lay = Image.new("RGBA", (W // 2 + 60, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for x in range(0, W // 2 + 60, 40):
            f = 0.6 + 0.4 * math.sin(x / 40 * 1.3)
            d.rectangle((x, 0, x + 40, H), fill=(int(170 * f), int(18 * f), int(24 * f), 255))
        lay = lay.filter(ImageFilter.GaussianBlur(6))
        ImageDraw.Draw(lay).rectangle((0, H - 20, W, H), fill=(200, 160, 60, 255))
        return lay
    lay = C(("curt"), mk)
    return lay
def audience(img, t, beat):
    d = ImageDraw.Draw(img, "RGBA"); rnd = random.Random(9)
    for row in range(2):
        for i in range(9):
            x = -40 + i * 140 + (70 if row else 0) + rnd.uniform(-20, 20); y = 1720 + row * 150
            bounce = abs(math.sin(t * 8 + i)) * 18 * beat
            col = (16, 6, 8, 255) if row else (28, 10, 12, 255)
            d.ellipse((x - 62, y - 150 - bounce, x + 62, y - 26 - bounce), fill=col)
            d.rounded_rectangle((x - 100, y - 40 - bounce * 0.5, x + 100, y + 200), 60, fill=col)
def beams(img, t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k, (x0, ph) in enumerate(((140, 0), (940, 1.6), (540, 3.0))):
        an = math.sin(t * 1.3 + ph) * 0.45
        x1 = x0 + math.sin(an) * 1500; y1 = 1500
        d.polygon([(x0 - 20, 0), (x0 + 20, 0), (x1 + 160, y1), (x1 - 160, y1)], fill=(255, 220, 160, 34))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))

def bedroom_art():
    def mk():
        bg = grad_bg((255, 236, 210), (238, 210, 180), "bed")
        d = ImageDraw.Draw(bg, "RGBA")
        d.rounded_rectangle((560, 260, 960, 760), 16, fill=(255, 250, 236, 255))
        sky = Image.new("RGBA", (380, 480), (0, 0, 0, 0)); sd = ImageDraw.Draw(sky)
        for i in range(480): sd.line((0, i, 380, i), fill=(255, int(190 + 50 * i / 480), int(130 + 90 * i / 480), 255))
        sd.ellipse((150, 300, 270, 420), fill=(255, 245, 210, 255))
        for x in range(0, 380, 60): sd.rectangle((x, 400 - (x * 7) % 90, x + 50, 480), fill=(200, 120, 110, 255))
        bg.alpha_composite(sky, (570, 270))
        d.line((760, 270, 760, 750), fill=(220, 200, 170, 255), width=10); d.line((570, 510, 950, 510), fill=(220, 200, 170, 255), width=10)
        d.rectangle((0, 1300, W, H), fill=(196, 160, 126, 255))
        return bg
    return C("bedroom", mk).copy()
def rays(img, t, cx, cy, a=50):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(9):
        an = math.radians(110 + k * 9 + math.sin(t + k) * 2)
        d.polygon([(cx, cy), (cx + math.cos(an - 0.04) * 2000, cy + math.sin(an - 0.04) * 2000), (cx + math.cos(an + 0.04) * 2000, cy + math.sin(an + 0.04) * 2000)], fill=(255, 240, 200, a))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(20)))
def newspaper():
    def mk():
        w, h = 560, 700
        lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rectangle((40, 44, 40 + w, 44 + h), fill=(0, 0, 0, 90)); lay = lay.filter(ImageFilter.GaussianBlur(12)); d = ImageDraw.Draw(lay)
        d.rectangle((30, 30, 30 + w, 30 + h), fill=(246, 240, 226, 255))
        draw_text(d, 30 + w / 2, 110, "大山!", 96, "extrabold", BRAND, "m")
        d.line((60, 140, w, 140), fill=INK, width=4)
        d.rectangle((60, 170, 330, 470), fill=(220, 210, 190, 255))
        for i in range(10): d.line((350, 180 + i * 28, w, 180 + i * 28), fill=(170, 160, 150, 255), width=8)
        for i in range(7): d.line((60, 500 + i * 28, w, 500 + i * 28), fill=(170, 160, 150, 255), width=8)
        tmp = Image.new("RGBA", (270, 300), (0, 0, 0, 0))
        draw_char(tmp, 135, 470, 0.62, "mark", mouth="grin", armR=(150, 160))
        lay.alpha_composite(tmp, (60, 170))
        return lay, (lay.size[0] / 2, lay.size[1] / 2)
    return C("news", mk)

def mountain_layer(p):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    base = 900
    peaks = [(220, 560), (540, 380), (860, 560)]
    hgt = out_cubic(p)
    pts = [(0, base)]
    for i, (x, y) in enumerate(peaks):
        yy = base - (base - y) * hgt
        pts += [(x - 150, base - (base - y) * hgt * 0.25), (x, yy)]
    pts += [(1010, base - 60 * hgt), (W, base), (W, base + 30), (0, base + 30)]
    d.polygon(pts, fill=(196, 28, 28, 255))
    for (x, y) in peaks:
        yy = base - (base - y) * hgt
        d.polygon([(x - 40 * hgt, yy + 70 * hgt), (x, yy), (x + 40 * hgt, yy + 70 * hgt), (x + 12, yy + 52 * hgt), (x - 10, yy + 64 * hgt)], fill=(255, 250, 246, 255))
    return lay

def phone_ui(p_items, glow_a=0):
    w, h = 600, 1000
    lay = Image.new("RGBA", (w + 100, h + 100), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((60, 66, 60 + w, 66 + h), 80, fill=(0, 0, 0, 120)); lay = lay.filter(ImageFilter.GaussianBlur(18)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((50, 50, 50 + w, 50 + h), 80, fill=(20, 18, 20, 255))
    d.rounded_rectangle((70, 70, 30 + w, 30 + h), 64, fill=(252, 250, 246, 255))
    draw_text(d, 50 + w / 2, 200, "laowai吗", 64, "extrabold", BRAND, "m")
    items = [("CASTING", "Shanghai"), ("TV HOST", "Beijing"), ("LIVESTREAM", "Hangzhou"), ("AGENT", "Shenzhen"), ("SHOOT", "Chengdu")]
    for i, (a, b) in enumerate(items):
        pp = clamp(p_items * 5 - i)
        if pp <= 0: continue
        y = 260 + i * 140; x = 100 + (1 - out_back(pp, 1.6)) * 300
        d.rounded_rectangle((x, y, x + w - 100, y + 112), 28, fill=(244, 238, 228, 255))
        d.ellipse((x + 22, y + 26, x + 82, y + 86), fill=BRAND + (255,))
        draw_text(d, x + 104, y + 52, a, 36, "extrabold", INK)
        draw_text(d, x + 104, y + 92, b, 28, "bold", (140, 130, 120))
    return lay, (lay.size[0] / 2, lay.size[1] / 2)

def city_bg():
    def mk():
        bg = grad_bg((22, 18, 40), (8, 6, 16), "city")
        d = ImageDraw.Draw(bg, "RGBA"); rnd = random.Random(4)
        for i in range(26):
            x = i * 46 - 20 + rnd.uniform(-10, 10); bw = rnd.uniform(60, 120); bh = rnd.uniform(300, 900)
            d.rectangle((x, 1500 - bh, x + bw, 1500), fill=(30, 26, 52, 255))
            for wy in range(int(1500 - bh + 20), 1490, 34):
                for wx in range(int(x + 10), int(x + bw - 10), 22):
                    if rnd.random() < 0.3: d.rectangle((wx, wy, wx + 10, wy + 14), fill=(255, 210, 140, 160))
        d.rectangle((0, 1500, W, H), fill=(14, 12, 24, 255))
        return bg
    return C("city", mk).copy()
def job_bubble(lbl, seed):
    def mk():
        w = int(text_w(lbl, 34, "extrabold")) + 90
        lay = Image.new("RGBA", (w + 30, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((10, 10, 10 + w, 80), 30, fill=(250, 248, 244, 255))
        d.polygon([(40, 78), (70, 78), (36, 102)], fill=(250, 248, 244, 255))
        d.ellipse((24, 26, 60, 62), fill=BRAND + (255,))
        draw_text(d, 74, 58, lbl, 34, "extrabold", INK)
        return lay, (lay.size[0] / 2, 45)
    return C(("jb", lbl), mk)
JOBS = ["Casting", "TV host", "Voice-over", "Livestream", "Model", "Agent", "Shoot", "Extra", "Host", "Brand ad", "Teacher", "Event MC"]
BUB = []
_r = random.Random(11)
for i in range(22):
    BUB.append((JOBS[i % len(JOBS)], _r.uniform(130, 950), _r.uniform(560, 1230), _r.uniform(0, 0.9), _r.uniform(-8, 8), _r.uniform(0.6, 1.0)))

# ================= FRAME =================
def scene_of(t):
    for k in range(len(SC) - 1):
        if SC[k] <= t < SC[k + 1]: return k
    return len(SC) - 2

def s0_studio(t):
    img = studio_bg()
    on = 1.0 if t > 0.1 else (0.5 if t > 0.033 else 0.0)
    if on:
        cone = cone_layer()
        if on < 1: cone = cone.copy(); cone.putalpha(cone.getchannel("A").point(lambda v: int(v * on)))
        img.alpha_composite(cone)
        particles(img, t, 40, 5, (255, 230, 190), (220, 0, 860, 1400), 18, 110)
    # Mark walks in
    t0, t1 = 0.0, 1.0
    p = clamp((t - t0) / (t1 - t0))
    x = 260 + (540 - 260) * in_out(p)
    walking = 0 < p < 1
    wave = t > 1.1
    armR = (140 + 22 * math.sin((t - 1.25) * 12), 160 + 30 * math.sin((t - 1.25) * 12)) if wave else (-10, -10)
    draw_char(img, x, 1430, 1.5, "mark", walk=t * 10, amp=1.0 if walking else 0, armR=armR,
              mouth="grin" if wave else "smile", eyes=1.1 if wave else 1.0, brow=0.5 if wave else 0, look=(0.0, -0.2), rim=(255, 220, 170) if on else None,
              blink=(1.9 < t < 1.98))
    if on: glow(img, 540, 1400, 300, (255, 200, 140), 0.25)
    # kinetic hook text
    Lc, Ac = pill("A CANADIAN STUDENT  加拿大留学生", 34, (255, 255, 255, 235), INK)
    fly(img, Lc, Ac, 540, 200, t, 0.0, (0, -120), 0.25)
    L, A = T3("SAID YES", 190, "white", 16)
    if t > tw("said", 0) - 0.05:
        g = glint(L, clamp((t - tw("yes", 0) - 0.05) / 0.6), 0.16, 0.9)
        slam(img, g, A, 540, 380, t, tw("said", 0) - 0.05, 0.3, 1.7)
    sz = 108; parts = [("TO", "white", (-700, 0)), ("ONE", "red", (0, -500)), ("TV", "white", (700, 0)), ("JOB.", "red", (700, 200))]
    widths = [text_w(p[0], sz, "extrabold") for p in parts]; gap = 34
    x = 540 - (sum(widths) + gap * 3) / 2
    for (wd, col, frm), wdt in zip(parts, widths):
        Lw, Aw = T3(wd, sz, col, 10)
        fly(img, Lw, Aw, x + wdt / 2 + 12, 590, t, tw(wd.lower().strip("."), 0) - 0.06, frm, 0.28)
        x += wdt + gap
    return cam(img, 1.0 + 0.06 * clamp(t / 2.6), 540, 900)

_snap = {}
def snapshot0():
    if "s0" not in _snap: _snap["s0"] = s0_studio(SC[1] - 0.04).copy()
    return _snap["s0"]
def s1_wall(t):
    t0 = SC[1]
    wall, (sx, sy, sw, sh) = tv_wall(t, t0 + 0.15)
    # zoom out from centre screen
    p = clamp((t - t0) / 0.75); e = out_cubic(p)
    zoom_start = W / sw
    z = zoom_start ** (1 - e)
    ccx = sx + sw / 2 + (W / 2 - sx - sw / 2) * e; ccy = sy + sh / 2 + (H / 2 - sy - sh / 2) * e
    img = cam(wall, z, ccx, ccy)
    # sharp snapshot drawn at the screen's on-screen rect (no upscaling blur)
    w2, h2 = W / z, H / z; bx = ccx - w2 / 2; by = ccy - h2 / 2
    rx0 = (sx + 7 - bx) * z; ry0 = (sy + 7 - by) * z; rw = (sw - 14) * z; rh = (sh - 14) * z
    if rw > 4:
        snap = snapshot0().resize((max(1, int(rw)), max(1, int(rh))), Image.LANCZOS)
        img.paste(snap, (int(rx0), int(ry0)))
    # warm bloom
    glow(img, 540, 960, 700, (255, 150, 90), 0.35 * clamp((t - t0 - 0.3) / 1.0))
    # type
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(dark).rounded_rectangle((40, 690, 1040, 1230), 60, fill=(10, 6, 6, 215))
    if t > tw("hundreds", 1) - 0.1: img.alpha_composite(dark.filter(ImageFilter.GaussianBlur(30)))
    L1, A1 = T3("HUNDREDS OF", 104, "white", 10)
    slam(img, L1, A1, 540, 800, t, tw("hundreds", 1) - 0.06, 0.28, 1.5)
    L2, A2 = T3("MILLIONS", 210, "gold", 18)
    if t > tw("millions", 1) - 0.06:
        L2g = glint(L2, clamp((t - tw("millions", 1) - 0.2) / 0.7), 0.16, 0.95)
        p2 = clamp((t - tw("millions", 1) + 0.06) / 0.3); paste_scaled(img, L2g, A2, 540, 990, 1.8 - 0.8 * out_expo(p2), min(1, p2 * 3))
        if p2 < 1: img = chroma(img, 8 * (1 - p2))
    letters(img, "knew his face.", 64, "extrabold", (255, 226, 214), 540, 1160, t, tw("knew", 1) - 0.05, 0.03)
    return img

def s2_beijing(t):
    t0 = SC[2]
    sky, far, mid, gnd, near = beijing_layers()
    img = sky.copy()
    tt = t - t0
    img.alpha_composite(far.crop((int(tt * 30), 0, int(tt * 30) + W, H)))
    img.alpha_composite(mid.crop((int(tt * 120), 0, int(tt * 120) + W, H)))
    img.alpha_composite(gnd)
    # bike + Mark
    ta = tw("mark", 3) - 0.6
    p = clamp((t - ta) / 1.6); bx = -260 + (520 + 260) * out_cubic(p)
    if t > ta:
        a = (t - ta) * 9 * (1.2 - out_cubic(p) * 0.7)
        bike(img, bx, 1560, 1.15, a)
        draw_char(img, bx - 30, 1590, 1.0, "mark", pedal=a, armR=(62, 75), armL=(62, 75), lean=12, mouth="grin", look=(0.4, 0), legs=True)
        if t > tw("chinese", 3) - 0.1:
            Lb, Ab = pill("你好！", 44, (255, 255, 255, 255), INK)
            paste_scaled(img, Lb, Ab, bx + 190, 1000, out_back(clamp((t - tw("chinese", 3) + 0.1) / 0.3), 2), 1)
    img.alpha_composite(near.crop((int(tt * 300) % (W * 2), 0, int(tt * 300) % (W * 2) + W, H)))
    if t > tw("mark", 3):
        Ln, An = pill("MARK ROWSWELL · 加拿大 CANADA", 30, BRAND + (255,), (255, 255, 255))
        fly(img, Ln, An, 540, 820, t, tw("mark", 3), (0, -120), 0.35)
    # year rewind
    ty = tw("1988", 2) - 0.6
    if t >= t0:
        if t < ty + 0.6:
            pr = clamp((t - t0) / max(0.2, ty + 0.6 - t0)); yr = int(round(2026 - 38 * out_cubic(pr)))
            L, A = T3(str(yr), 300, "sepia", 22)
            paste_scaled(img, L, A, 540, 560, 0.95, 1)
        else:
            L, A = T3("1988", 300, "sepia", 22)
            pm = clamp((t - (ty + 0.6)) / 0.25); sc = 1.25 - 0.3 * out_expo(pm)
            mv = clamp((t - (LS[3] - 0.1)) / 0.45); e = out_cubic(mv)
            L = glint(L, clamp((t - ty - 0.7) / 0.6), 0.16, 0.9)
            paste_scaled(img, L, A, 540, 560 - 300 * e, sc * (1 - 0.45 * e), 1)
            if mv > 0:
                Lp, Ap = pill("北京 · BEIJING", 34, (255, 255, 255, 230), INK); paste_scaled(img, Lp, Ap, 540, 420, 1, e)
    if t - t0 < 0.3:
        img = chroma(img, 14 * (1 - (t - t0) / 0.3)); img = hblur(img, 30 * (1 - (t - t0) / 0.3))
        d = ImageDraw.Draw(img, "RGBA")
        for y in range(0, H, 6): d.line((0, y, W, y), fill=(0, 0, 0, 50))
    return img

def s3_station(t):
    t0 = SC[3]
    img = station_art()
    rt = t - t0
    ringing = rt < tw("foreigner", 4) - t0 + 0.2
    ph = phone_art(rt if ringing else 0)
    shake = (math.sin(rt * 60) * 8) if ringing else 0
    paste_scaled(img, ph, (190, 280), 300 + shake, 1060, 1.3, 1, shake * 0.4)
    if ringing:
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(3):
            r = 200 + k * 40 + (rt * 200) % 40
            d.arc((300 - r, 900 - r, 300 + r, 900 + r), 220, 320, fill=(255, 255, 255, 160), width=6)
    Lc, Ac = casting_card()
    tc = tw("foreigner", 4) - 0.1
    if t > tc:
        p = clamp((t - tc) / 0.28); sc = 1.5 - 0.5 * out_expo(p)
        Lt, At = tilt(Lc, -6, 8 * (1 - p) + 3 * math.sin(rt * 1.5))
        paste_scaled(img, Lt, At, 540, 620, sc * 1.05, min(1, p * 3), -4 * (1 - p) - 2)
        if p < 1: img = chroma(img, 8 * (1 - p))
        if t > tw("mandarin", 4):
            d = ImageDraw.Draw(img, "RGBA"); pu = clamp((t - tw("mandarin", 4)) / 0.3)
            d.line((280, 700, 280 + 520 * out_cubic(pu), 700), fill=BRAND + (255,), width=10)
    img = cam(img, 1.0 + 0.04 * rt, 540, 900)
    if rt < 0.18: img = hblur(img, 60 * (1 - rt / 0.18))
    return img

def s4_class(t):
    t0 = SC[4]; rt = t - t0
    img = classroom_art()
    tp = tw("professors", 5) - 0.1
    turn = 1 if t > tp else -1
    point = clamp((t - tp) / 0.25)
    draw_char(img, 270, 1500, 1.25, "prof", face=turn, armR=(-10 + 105 * out_back(point), -10 + 100 * out_back(point)),
              mouth="talk" if t > tp else "flat", mo=abs(math.sin(rt * 14)), brow=0.3, rim=None)
    tn = tw("name", 5) - 0.15
    surprised = t > tn
    draw_char(img, 800, 1520, 1.3, "mark", face=-1, armR=((28, -118) if surprised else (14, 8)), eyes=1.35 if surprised else 1,
              brow=1 if surprised else 0, mouth="o" if surprised else "smile", look=(-0.5, 0), bob=-14 * math.sin(clamp((t - tn) / 0.3) * math.pi))
    if surprised:
        Lb, Ab = pill("我？ Me?", 46, (255, 255, 255, 255), INK)
        paste_scaled(img, Lb, Ab, 930, 800, out_back(clamp((t - tn) / 0.3), 2.2), 1)
        Ln, An = T3("MARK ROWSWELL", 92, "white", 9)
        pn = clamp((t - tn - 0.1) / 0.4)
        paste_scaled(img, Ln, An, 300 + 240 * out_cubic(pn), 760 - 60 * out_cubic(pn), 0.4 + 0.6 * out_back(pn), pn)
    z = 1.0 + 0.18 * in_out(clamp((t - tn) / 0.9)) if surprised else 1.0
    img = cam(img, z, 540 + 200 * (z - 1) / 0.18, 1150)
    if rt < 0.2: img = vblur(img, 50 * (1 - rt / 0.2))
    return img

def s5_gala(t):
    t0 = SC[5]; rt = t - t0
    img = gala_bg()
    beams(img, t)
    # performers: alternate talk
    talkA = math.sin(rt * 3.2) > 0
    g1 = math.sin(rt * 7)
    draw_char(img, 330, 1390, 1.15, "partner", face=1, hand_prop="fan", armR=(70 + 30 * g1, 140 + 20 * g1) if talkA else (40, 100),
              mouth="talk" if talkA else "grin", mo=abs(math.sin(rt * 15)), rim=(255, 210, 150))
    draw_char(img, 760, 1390, 1.2, "mark", face=-1, armR=(80 + 40 * math.sin(rt * 6), 120 + 40 * math.sin(rt * 6 + 1)) if not talkA else (-10, 20),
              mouth="talk" if not talkA else "grin", mo=abs(math.sin(rt * 14)), brow=0.4, rim=(255, 210, 150))
    laugh = clamp((t - tw("skit", 6)) / 0.3)
    audience(img, t, laugh)
    if laugh > 0:
        rnd = random.Random(int(rt * 3))
        for k in range(3):
            tt = (rt * 1.5 + k * 0.33) % 1
            L, A = TL("哈哈", 54, "extrabold", (255, 214, 120))
            paste_scaled(img, L, A, 140 + k * 400, 1300 - tt * 300, 0.8 + tt * 0.4, (1 - tt) * laugh)
    # curtains open
    op = in_out(clamp(rt / 0.8))
    cl = curtain(0, op)
    img.alpha_composite(cl, (int(-W / 2 * op) - 30, 0))
    cr = cl.transpose(Image.Transpose.FLIP_LEFT_RIGHT); img.paste(cr, (int(W / 2 + W / 2 * op) - 30, 0), cr)
    # type
    Lm, Am = pill("IN MANDARIN · 说中文", 36, (255, 255, 255, 240), BRAND)
    fly(img, Lm, Am, 540, 980, t, tw("mandarin", 6), (0, 80), 0.3)
    L1, A1 = T3("CHINA'S BIGGEST", 110, "gold", 10)
    L2, A2 = T3("NIGHT OF TV", 150, "white", 14)
    slam(img, L1, A1, 540, 230, t, tw("biggest", 6) - 0.2, 0.3, 1.5)
    slam(img, L2, A2, 540, 400, t, tw("night", 6) - 0.05, 0.3, 1.6)
    z = 1.12 - 0.12 * out_cubic(clamp(rt / 2.5))
    img = cam(img, z, 540, 900 + 160 * (1 - out_cubic(clamp(rt / 2.5))))
    return img

def s6_star(t):
    t0 = SC[6]; rt = t - t0
    td = tw("dashan", 8) - 0.25
    if t < td:
        img = bedroom_art(); rays(img, t, 760, 360, 40)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((40, 1210, 700, 1420), 40, fill=(230, 226, 240, 255))
        wake = clamp(rt / 0.5)
        draw_char(img, 330, 1560, 1.2, "mark", legs=False, armR=(140 + 30 * math.sin(rt * 5), 175), armL=(140, 175), mouth="o" if rt < 0.6 else "grin", eyes=0.3 + 0.8 * wake, bob=60 * (1 - out_cubic(wake)))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((0, 1300, 760, 1480), 50, fill=(240, 236, 248, 255)); d.rounded_rectangle((0, 1300, 760, 1340), 30, fill=(196, 28, 28, 255))
        tn = tw("star", 7) - 0.1
        if t > tn:
            Ln, An = newspaper(); p = clamp((t - tn) / 0.45)
            paste_scaled(img, Ln, An, 760 - 100 * out_cubic(p), 860, 0.2 + 0.8 * out_back(p, 1.4), 1, 720 * (1 - out_cubic(p)) - 8)
            Ls, As = T3("A STAR.", 150, "red", 12); slam(img, Ls, As, 540, 240, t, tn + 0.15, 0.3, 1.6)
        return img
    img = grad_bg((255, 248, 240), (244, 228, 214), "dash")
    p = clamp((t - td) / 0.5)
    m = clamp((t - td - 0.35) / 0.6)
    L, A = T3("山", 560, "red", 30)
    if m < 1: paste_scaled(img, L, A, 540, 720, 0.6 + 0.4 * out_back(p), (1 - m) * min(1, p * 3))
    if m > 0: img.alpha_composite(mountain_layer(m))
    L2, A2 = T3("大山 DASHAN", 150, "ink", 12)
    wipe_in(img, L2, A2, 540, 1110, clamp((t - td - 0.4) / 0.5), 50)
    tb = tw("big", 8) - 0.05
    if t > tb:
        L3, A3 = TL("Big Mountain.", 110, "serif", BRAND); p3 = clamp((t - tb) / 0.4)
        paste_scaled(img, L3, A3, 540, 1270, 0.8 + 0.2 * out_back(p3), p3)
    if p < 0.3: img = hblur(img, 40 * (1 - p / 0.3))
    particles(img, t, 30, 8, (196, 28, 28), (0, 300, W, 1400), 30, 90, (2, 4))
    return img

def screen_dev(kind):
    def mk():
        if kind == 0:
            return tv_screen_layer(300, 230, True)
        if kind == 1:
            lay = Image.new("RGBA", (440, 280), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.rounded_rectangle((10, 10, 430, 250), 10, fill=(24, 24, 28, 255)); inner = tv_screen_layer(400, 220, True)
            lay.alpha_composite(inner.crop((6, 6, 406, 226)), (20, 20)); d.rectangle((200, 250, 240, 276), fill=(24, 24, 28, 255)); return lay
        lay = Image.new("RGBA", (220, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((10, 10, 210, 410), 34, fill=(24, 24, 28, 255)); inner = tv_screen_layer(180, 370, True)
        lay.alpha_composite(inner.crop((6, 6, 186, 376)), (20, 20)); return lay
    return C(("dev", kind), mk)
def s7_decades(t):
    t0 = SC[7]; rt = t - t0
    img = grad_bg((40, 30, 60), (20, 14, 30), "dec")
    glow(img, 540, 900, 600, (196, 28, 28), 0.4)
    tf = tw("still", 9) - 0.2
    if t < tf:
        draw_char(img, 540, 1400, 1.3, "mark", armR=(30, 10), mouth="smile", look=(0.3, 0), walk=0, rim=(255, 180, 160))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((620, 1240, 860, 1420), 24, fill=(150, 100, 60, 255)); d.rounded_rectangle((700, 1210, 780, 1250), 12, outline=(90, 60, 40, 255), width=8)
        Lt, At = pill("A FEW YEARS?", 38, (255, 255, 255, 255), INK)
        paste_scaled(img, Lt, At, 740, 1150, out_back(clamp((t - tw("few", 9)) / 0.3), 2), 1, 6)
        Ly, Ay = T3("1988", 200, "sepia", 16); paste_scaled(img, Ly, Ay, 540, 300, 1, 1)
        return img
    p = clamp((t - tf) / 1.2)
    yr = int(round(1988 + (2026 - 1988) * out_cubic(p)))
    Ly, Ay = T3(str(yr), 200, "gold", 16); paste_scaled(img, Ly, Ay, 540, 300, 1 + 0.06 * math.sin(p * 30) * (1 - p), 1)
    k = min(2, int(p * 3))
    dev = screen_dev(k)
    for (x, y, s) in ((170, 1080, 0.62), (910, 1080, 0.62), (540, 780, 0.5)):
        paste_scaled(img, dev, (dev.size[0] / 2, dev.size[1] / 2), x, y + 10 * math.sin(t * 2 + x), s, 0.9)
    who = "mark" if p < 0.5 else "mark_old"
    draw_char(img, 540, 1440, 1.3, who, armR=(150 + 20 * math.sin(rt * 10), 170), mouth="grin", rim=(255, 180, 160))
    if p < 0.6:
        fl = Image.new("RGBA", (W, H), (255, 255, 255, int(60 * abs(math.sin(p * 40))))); img.alpha_composite(fl)
    Lh, Ah = T3("STILL A", 110, "white", 10); Lh2, Ah2 = T3("HOUSEHOLD NAME", 120, "red", 11)
    slam(img, Lh, Ah, 540, 500, t, tw("household", 9) - 0.35, 0.3)
    slam(img, Lh2, Ah2, 540, 640, t, tw("household", 9) - 0.1, 0.3)
    return img

def s8_onejob(t):
    t0 = SC[8]; rt = t - t0
    img = Image.new("RGBA", (W, H), (8, 6, 6, 255))
    glow(img, 540, 760, 620, (255, 200, 140), 0.5 + 0.1 * math.sin(rt * 4))
    Lc, Ac = casting_card()
    s = 0.85 + 0.08 * rt
    Lt, At = tilt(Lc, 4 * math.sin(rt * 1.1), 10 * math.sin(rt * 0.8))
    paste_scaled(img, Lt, At, 540, 760, s, clamp(rt / 0.3))
    particles(img, t, 40, 12, (255, 220, 170), (0, 0, W, H), 12, 100)
    L, A = T3("ONE JOB.", 220, "red", 18)
    to = tw("one", 10) - 0.08
    if t > to:
        L = glint(L, clamp((t - to - 0.3) / 0.7), 0.16, 0.9)
        slam(img, L, A, 540, 1240, t, to, 0.3, 1.8)
    letters(img, "he happened to hear about", 52, "extrabold", (255, 226, 214), 540, 1430, t, tw("happened", 10) - 0.1, 0.03)
    return img

def s9_scatter(t):
    t0 = SC[9]; rt = t - t0
    img = city_bg()
    pull = out_cubic(clamp(rt / 0.6))
    for i, (lbl, x, y, d0, rot, sc) in enumerate(BUB):
        ta = t0 + d0 * 0.8
        if t < ta: continue
        p = clamp((t - ta) / 0.3)
        blink = 1.0
        if t > tw("never", 11) and i % 3 == 0: blink = max(0.15, 1 - clamp((t - tw("never", 11) - (i % 5) * 0.1) / 0.3))
        L, A = job_bubble(lbl, i)
        paste_scaled(img, L, A, x, y + 6 * math.sin(t * 2 + i), sc * out_back(p, 2), blink * 0.95, rot)
    # talent scrolling, frowning
    tsh = tw("scattered", 11)
    shrug = clamp((t - tsh) / 0.3)
    draw_char(img, 540, 1560, 1.25, "talent", hand_prop="phone", armR=(40 + 60 * shrug, 150 - 40 * shrug), armL=(10 + 60 * shrug, 10 + 90 * shrug),
              look=(0.3, 0.7) if shrug == 0 else (0, -0.2), mouth="flat" if shrug == 0 else "o", brow=-0.6 if shrug == 0 else 0.8, rim=(140, 170, 255),
              bob=-10 * math.sin(shrug * math.pi))
    glow(img, 600, 1260, 120, (130, 190, 255), 0.4)
    L1, A1 = T3("THE JOBS ARE", 92, "white", 9)
    L2, A2 = T3("OUT THERE.", 130, "white", 12)
    if t < tsh - 0.15:
        slam(img, L1, A1, 540, 230, t, tw("jobs", 11) - 0.15, 0.3)
        slam(img, L2, A2, 540, 370, t, tw("out", 11) - 0.05, 0.3)
    else:
        # SCATTERED letters flung around
        rnd = random.Random(21); word = "SCATTERED"
        p = clamp((t - tsh + 0.15) / 0.5)
        tot = text_w(word, 150, "extrabold"); x = 540 - tot / 2
        for ch in word:
            Lc, Ac = T3(ch, 150, "red", 12)
            cw = text_w(ch, 150, "extrabold")
            dx, dy, rr = rnd.uniform(-260, 260), rnd.uniform(-160, 260), rnd.uniform(-50, 50)
            e = out_back(p, 1.4)
            paste_scaled(img, Lc, Ac, x + cw / 2 + dx * e, 330 + dy * e, 1, 1, rr * e)
            x += cw
    img = cam(img, 1.25 - 0.25 * pull, 540, 900)
    return img

def s10_one(t):
    t0 = SC[10]; rt = t - t0
    tend = LS[13] - 0.15
    if t < tend:
        img = city_bg()
        glow(img, 540, 900, 700, (196, 28, 28), 0.5)
        pc = clamp(rt / 0.7)
        for i, (lbl, x, y, d0, rot, sc) in enumerate(BUB):
            e = in_out(clamp(pc * 1.3 - i * 0.015))
            if e >= 1: continue
            L, A = job_bubble(lbl, i)
            paste_scaled(img, L, A, x + (540 - x) * e, y + (900 - y) * e, sc * (1 - 0.8 * e), 1 - e, rot * (1 - e))
        pu = clamp((rt - 0.35) / 0.5)
        Lp, Ap = phone_ui(clamp((rt - 0.6) / 1.0))
        if pu > 0:
            Lt, At = tilt(Lp, 8 * (1 - pu), -10 + 6 * math.sin(rt * 1.2))
            paste_scaled(img, Lt, At, 540, 640, 0.3 + 0.5 * out_back(pu, 1.4), min(1, pu * 3))
        for k, (wd, y, col, word) in enumerate((("EVERY JOB.", 1200, "white", "job"), ("EVERY AGENT.", 1330, "white", "agent"), ("ONE PLACE.", 1490, "gold", "place"))):
            L, A = T3(wd, 104 if k < 2 else 130, col, 10); slam(img, L, A, 540, y, t, tw(word, 12) - 0.12, 0.28, 1.5)
        draw_char(img, 540, 1900, 0.75, "talent", hand_prop=None, armR=(150, 175), armL=(150, 175), mouth="grin", eyes=1.2, brow=0.7, bob=-26 * abs(math.sin(rt * 6)) if rt > 1.2 else 0, face=1)
        return img
    # end card
    img = grad_bg((214, 38, 36), (150, 14, 18), "endc")
    re = clamp((t - tend) / 0.35)
    particles(img, t, 40, 14, (255, 220, 200), (0, 0, W, H), 20, 90)
    L, A = T3("laowai吗", 210, "white", 18, maxw=900)
    L = glint(L, clamp((t - tend - 0.4) / 0.8), 0.18, 0.9)
    paste_scaled(img, L, A, 540, 820, 0.7 + 0.3 * out_back(re, 1.8), min(1, re * 2))
    Lp, Ap = pill("laowai.ma", 54, (255, 255, 255, 255), BRAND)
    fly(img, Lp, Ap, 540, 1040, t, tend + 0.3, (0, 120), 0.35)
    Ls, As = TL("Every job. Every agent. One place.", 46, "bold", (255, 230, 226))
    paste_scaled(img, Ls, As, 540, 1180, 1, clamp((t - tend - 0.55) / 0.3))
    Lz, Az = TL("外国人才的工作与经纪人，一站汇集", 40, "extrabold", (255, 214, 208))
    paste_scaled(img, Lz, Az, 540, 1250, 1, clamp((t - tend - 0.7) / 0.3))
    pj = clamp((t - tend - 0.5) / 0.4)
    if pj > 0:
        hop = abs(math.sin((t - tend) * 7)) * 30
        draw_char(img, 290, 1900 + 400 * (1 - out_back(pj, 1.6)), 0.8, "mark", armR=(150 + 20 * math.sin(t * 9), 170), mouth="grin", eyes=1.1, brow=0.5, rim=(255, 210, 190))
        draw_char(img, 790, 1900 + 400 * (1 - out_back(clamp(pj * 1.1 - 0.1), 1.6)), 0.75, "talent", face=-1, armR=(150, 175), armL=(150, 175), mouth="grin", eyes=1.2, brow=0.7, bob=-hop, rim=(255, 210, 190))
    if re < 1:
        cut = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(cut).ellipse((540 - 1400 * re, 960 - 1400 * re, 540 + 1400 * re, 960 + 1400 * re), fill=(255, 255, 255, 255))
        prev = s10_one(tend - 0.01); prev.paste(img, (0, 0), cut.getchannel("A")); img = prev
    return img

SCENES = [s0_studio, s1_wall, s2_beijing, s3_station, s4_class, s5_gala, s6_star, s7_decades, s8_onejob, s9_scatter, s10_one]

def frame_f(fi):
    t = fi / FPS
    s = scene_of(t)
    img = SCENES[s](t)
    if t < SC[10] and not (s == 0 and t < 0.25): karaoke(img, t)
    # scene-cut flash/whip on entry
    rt = t - SC[s]
    if s > 0 and rt < 0.1 and s not in (1, 2, 3, 4):
        img = hblur(img, 40 * (1 - rt / 0.1))
    arr = post(img.convert("RGB"), int(fi), grain=1.0, vignette=0.22)
    return np.asarray(arr) if not isinstance(arr, np.ndarray) else arr

KEYS = []
def mb_n(i):
    t = i / FPS
    for k in SC[1:-1]:
        if abs(t - k) < 0.25: return 3
    return 1
def frame(i):
    n = mb_n(i)
    return frame_f(i) if n == 1 else mblur(frame_f, i, n, 0.5)

# ================= AUDIO =================
def build_audio(path):
    m = Mix(DUR)
    bpm = 100; beat = 60 / bpm
    # music bed: pad + soft kick from the wall onward
    chords = [(110, 138.6, 164.8), (98, 123.5, 146.8), (87.3, 110, 130.8), (98, 123.5, 146.8)]
    t = 0.0; i = 0
    while t < DUR:
        m.add(t, stab([f * 2 for f in chords[i % 4]], 0.10, beat * 4), 1.0); t += beat * 4; i += 1
    t = SC[1]
    while t < DUR - 1:
        m.add(t, kick(0.5), 1.0); m.add(t + beat / 2, hat(0.12), 1.0); t += beat
    # SFX
    m.add(0.16, boom(0.8)); m.add(0.18, bass(55, 0.6, 0.6))
    for k in range(6): m.add(0.3 + k * 0.16, tick(0.12))
    m.add(tw("said", 0) - 0.05, kick(0.9)); m.add(tw("one", 0) - 0.06, pop(0.5)); m.add(tw("tv", 0) - 0.06, whoosh(0.3, 0.4))
    m.add(SC[1] - 0.35, whoosh(0.5, 0.6, False))
    for k in range(10): m.add(SC[1] + 0.15 + k * 0.09, pop(0.15, 900 + k * 60, 1500 + k * 60))
    m.add(tw("millions", 1) - 0.4, riser(0.4, 0.4)); m.add(tw("millions", 1) - 0.04, boom(0.9))
    m.add(SC[2] - 0.05, whoosh(0.6, 0.6, False))
    for k in range(12): m.add(SC[2] + k * 0.05, tick(0.25))
    m.add(tw("1988", 2) + 0.0, boom(0.8))
    m.add(tw("chinese", 3) - 0.1, pluck(880, 0.4)); m.add(tw("chinese", 3), pluck(1320, 0.3))
    for k in range(5):
        m.add(SC[3] + k * 0.28, buzz(0.14, 0.18))
    m.add(tw("foreigner", 4) - 0.1, kick(1.0)); m.add(tw("foreigner", 4) - 0.1, clap(0.4))
    m.add(SC[4] - 0.1, whoosh(0.35, 0.5))
    m.add(tw("name", 5) - 0.15, pop(0.6)); m.add(tw("name", 5) - 0.05, whoosh(0.3, 0.3))
    m.add(SC[5], whoosh(0.8, 0.6))
    for k in range(4): m.add(tw("skit", 6) + k * 0.5, clap(0.18))
    m.add(tw("biggest", 6) - 0.2, kick(0.8)); m.add(tw("night", 6) - 0.05, boom(0.7))
    m.add(SC[6], pluck(1046, 0.3)); m.add(SC[6] + 0.12, pluck(1318, 0.3)); m.add(tw("star", 7) - 0.1, whoosh(0.4, 0.5)); m.add(tw("star", 7) + 0.25, kick(0.8))
    m.add(tw("dashan", 8) - 0.3, riser(0.3, 0.4)); m.add(tw("dashan", 8) - 0.05, boom(1.0)); m.add(tw("big", 8), pluck(660, 0.4))
    for k in range(14): m.add(tw("still", 9) - 0.2 + k * 0.085, tick(0.2))
    m.add(tw("household", 9) - 0.35, kick(0.8)); m.add(tw("household", 9) - 0.1, boom(0.6))
    m.add(SC[8], drone(2.6, 55, 0.25)); m.add(tw("one", 10) - 0.08, boom(0.9))
    for k in range(8): m.add(SC[9] + 0.1 + k * 0.1, pop(0.12, 700 + k * 50, 1100 + k * 50))
    m.add(tw("scattered", 11) - 0.15, whoosh(0.5, 0.7))
    m.add(SC[10] + 0.05, riser(0.6, 0.5)); m.add(SC[10] + 0.65, boom(0.9))
    for w_ in ("job", "agent", "place"): m.add(tw(w_, 12) - 0.12, kick(0.9))
    m.add(LS[13] - 0.15, boom(1.0)); m.add(LS[13] + 0.1, stab([523, 659, 784], 0.3, 1.2))
    x = m.master(0.4)
    # VO
    vo = VO_DIR + "/vo_n.wav"
    if os.path.exists(vo):
        import wave
        w = wave.open(vo); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
        if w.getnchannels() == 2: v = v[::2]
        x = x * 0.32
        n = min(len(x), len(v)); x[:n] += v[:n] * 0.95
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    write_wav(path, x)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for a in sys.argv[2:]:
            t = float(a); Image.fromarray(frame_f(int(t * FPS))).save(f"out/v9still_{a}.png")
    elif sys.argv[1] == "render":
        build_audio("out/reel09.wav")
        render(frame, NF, "out/reel09.wav", "out/laowai_reel_08.mp4")
        print("done", DUR)
