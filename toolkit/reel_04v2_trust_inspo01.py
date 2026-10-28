"""Reel 04 v2 - inspo-grade motion (divyansh.fx spec): typewriter chars, glow, whip transitions, dial, brackets, hexes with draw-on callouts, pill slide-ins, scramble decode."""
import sys, math, wave, random
sys.path.insert(0, "/home/claude/reels")
import reel_04 as P
import reel_02 as R
from reel_lib import *
from PIL import ImageFilter
from scipy import ndimage

INK, BRAND, RLIGHT, MUTED, GREY, LINE, WHITE = P.INK, P.BRAND, P.RLIGHT, P.MUTED, P.GREY, P.LINE, P.WHITE
T, E, WN, DUR, wl, ss, person, wifi = P.T, P.E, P.WN, P.DUR, P.wl, P.ss, P.person, P.wifi
vo, ENV = P.vo, P.ENV
SC = [0, 2.1, 4.6, 8.6, 12.7, 16.5, 20.3, 22.3, 32.4, DUR + 1]
def scene_idx(t):
    k = 0
    for i, c in enumerate(SC[1:-1], 1):
        if t >= c: k = i
    return k

# ---------------- helpers ----------------
def hblur_np(a, r):
    return ndimage.uniform_filter1d(a, size=int(2 * r + 1), axis=1, mode="nearest") if r >= 1 else a
def hblur_layer(lay, r):
    if r < 1: return lay
    a = np.asarray(lay, dtype=np.float32)
    a = a * (a[..., 3:4] / 255.0)  # premultiply
    a = ndimage.uniform_filter1d(a, size=int(2 * r + 1), axis=1, mode="constant")
    al = a[..., 3:4]
    rgb = np.where(al > 1e-3, a[..., :3] / np.maximum(al / 255.0, 1e-3), 0)
    return Image.fromarray(np.clip(np.concatenate([rgb, al], -1), 0, 255).astype(np.uint8), "RGBA")

_cc = {}
def char_layer(ch, size, wt, col, blur):
    k = (ch, size, wt, col, int(blur))
    if k not in _cc:
        lay, anc = wl(ch, size, wt, col)
        _cc[k] = (lay.filter(ImageFilter.GaussianBlur(int(blur))) if blur >= 1 else lay, anc)
    return _cc[k]

def typed(img, t, segs, size, cx, by, t0, cps=18.0, alpha=1.0):
    """segs: [(text, weight, color, scale)] each text may end with a space. returns end time."""
    ws = [text_w(s, int(size * k), wt) for s, wt, c, k in segs]
    total = sum(ws) - text_w(" ", int(size * segs[-1][3]), segs[-1][1]) * (1 if segs[-1][0].endswith(" ") else 0)
    x = cx - total / 2; n = 0
    for (s, wt, col, k), w in zip(segs, ws):
        fs = int(size * k)
        for i, ch in enumerate(s):
            if ch == " ": n += 1; continue
            age = t - (t0 + n / cps); n += 1
            if age < 0: continue
            p = clamp(age / 0.16); e = out_cubic(p)
            lay, anc = char_layer(ch, fs, wt, col, 9 * (1 - e) ** 1.5)
            cw = text_w(ch, fs, wt)
            px = x + text_w(s[:i], fs, wt) + cw / 2
            paste_scaled(img, lay, anc, px, by + 12 * (1 - e), 1.0 + 0.08 * (1 - e), min(1, p * 1.8) * alpha)
        x += w
    return t0 + n / cps

def blur_in(img, lay, anc, cx, cy, t, t0, d=0.4, sc=1.0, alpha=1.0, key=None):
    if t < t0: return
    p = clamp((t - t0) / d); e = out_expo(p)
    r = 14 * (1 - e) ** 2
    L = lay.filter(ImageFilter.GaussianBlur(r)) if r > 0.8 else lay
    paste_scaled(img, L, anc, cx, cy + 30 * (1 - e), (1.12 - 0.12 * e) * sc, min(1, p * 1.6) * alpha)

# glow blob
def make_glow(w=900, h=620, col=BRAND, amax=120):
    yy, xx = np.mgrid[0:h, 0:w]
    r2 = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    a = np.exp(-r2 * 3.2) * amax
    arr = np.zeros((h, w, 4), np.uint8); arr[..., 0], arr[..., 1], arr[..., 2] = col; arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA"), (w / 2, h / 2)
GLOW, GLOWA = make_glow()
def glow(img, cx, cy, t, t0, sc=1.0, a=1.0):
    if t < t0: return
    k = clamp((t - t0) / 0.5)
    paste_scaled(img, GLOW, GLOWA, cx, cy, sc * (0.7 + 0.3 * out_cubic(k)) * (1 + 0.04 * math.sin(t * 2.6)), k * a)

def particles(img, t, t0, cx, cy, seed=1, n=6):
    if t < t0: return
    rnd = random.Random(seed)
    for k in range(n):
        ox, oy, sp, ph = rnd.uniform(-380, 380), rnd.choice((rnd.uniform(-240, -140), rnd.uniform(130, 250))), rnd.uniform(40, 90), rnd.uniform(0, 3)
        life = ((t - t0) * 0.7 + ph) % 2.0
        a = math.sin(clamp(life / 2.0) * math.pi) * 0.75
        lay, anc = wl("¥", 40 + int(14 * (k % 3)), "bold", BRAND)
        paste_scaled(img, lay, anc, cx + ox + 10 * math.sin(t * 2 + k), cy + oy - life * sp, 1.0, a * min(1, (t - t0) / 0.4))

# background arcs + drifting rings
def bg_motion(img, t):
    d = ImageDraw.Draw(img, "RGBA")
    for cx, cy, r, ph, sp in ((60, 160, 190, 0, 11), (940, 1700, 300, 90, -8), (1020, 560, 150, 40, 13), (200, 1500, 120, 10, -12)):
        a0 = ph + t * sp
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 150, fill=BRAND + (80,), width=3)
        d.arc((cx - r, cy - r, cx + r, cy + r), a0 + 175, a0 + 215, fill=LINE + (255,), width=3)
def make_ring(sz=900, th=170, blur=34):
    im = Image.new("RGBA", (sz + 200, sz + 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((100, 100, 100 + sz, 100 + sz), outline=BRAND + (70,), width=th)
    return im.filter(ImageFilter.GaussianBlur(blur)), ((sz + 200) / 2, (sz + 200) / 2)
RING, RINGA = make_ring()

# ---------------- dial ----------------
DC = (-130, 1150); DR = 1180
def make_dial():
    k = 2; im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = DC[0] * k, DC[1] * k
    d.arc((cx - DR * k, cy - DR * k, cx + DR * k, cy + DR * k), 272, 352, fill=BRAND, width=7 * k)
    for a10 in range(2740, 3440, 12):
        a = math.radians(a10 / 10); big = (a10 // 12) % 5 == 0
        r0, r1 = (DR - (62 if big else 44)) * k, (DR - 18) * k
        d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=(120, 112, 100, 230) if big else (190, 184, 174, 200), width=(3 if big else 2) * k)
    for ang in (281, 303, 330):
        a = math.radians(ang); x, y = cx + DR * k * math.cos(a), cy + DR * k * math.sin(a)
        d.ellipse((x - 11 * k, y - 11 * k, x + 11 * k, y + 11 * k), fill=(255, 255, 255, 255), outline=INK, width=3 * k)
    return im.resize((W, H), Image.LANCZOS)
DIAL = make_dial()
def make_needle(L=1130):
    k = 2; w = 180; im = Image.new("RGBA", (w * k, (L + 80) * k), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = w * k // 2; base = (L + 40) * k
    # shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.polygon([(cx - 26 * k + 20 * k, base), (cx + 26 * k + 20 * k, base), (cx + 6 * k + 20 * k, 0), (cx - 6 * k + 20 * k, 0)], fill=(0, 0, 0, 50))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * k)); im.alpha_composite(sh)
    d.polygon([(cx - 26 * k, base), (cx + 26 * k, base), (cx + 6 * k, 0), (cx - 6 * k, 0)], fill=INK)
    ty = int(base - L * 0.7 * k)  # diamond ornament
    d.polygon([(cx, ty - 78 * k), (cx + 30 * k, ty), (cx, ty + 78 * k), (cx - 30 * k, ty)], fill=(255, 255, 255), outline=INK, width=6 * k)
    d.rectangle((cx - 14 * k, int(base - L * 0.12 * k) - 8 * k, cx + 14 * k, int(base - L * 0.12 * k) + 8 * k), fill=BRAND)
    d.ellipse((cx - 42 * k, base - 42 * k, cx + 42 * k, base + 42 * k), fill=INK)
    d.ellipse((cx - 22 * k, base - 22 * k, cx + 22 * k, base + 22 * k), fill=BRAND)
    return im.resize((w, L + 80), Image.LANCZOS), (w / 2, L + 40)
NEEDLE, NEEDLEA = make_needle()
def dial_scene(img, t, ts):
    p = clamp((t - ts) / 0.5)
    paste_scaled(img, DIAL, (0, 0), 0 - 14 * (1 - out_cubic(p)), 0, 1.0, min(1, p * 2))
    loc = max(0, t - ts); step = int(loc / 0.28); fr = (loc % 0.28) / 0.28
    dl = 8 + 2.3 * (step + out_back(clamp(fr * 2.5), 3.0))
    paste_scaled(img, NEEDLE, NEEDLEA, DC[0], DC[1], 1.0, min(1, p * 2), rot=-dl)
    wm, wa = wl("TRUST METER  信任度", 26, "mono", (190, 184, 174))
    paste_scaled(img, wm, wa, 300, 560, 1.0, 0.8 * p, rot=-18)

# ---------------- brackets / persons / cards ----------------
def brackets(w, h, ln=130, wd=7, col=BRAND):
    p = 20; lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (x, y, sx, sy) in ((p, p, 1, 1), (p + w, p, -1, 1), (p, p + h, 1, -1), (p + w, p + h, -1, -1)):
        d.line((x, y + sy * ln, x, y, x + sx * ln, y), fill=col, width=wd, joint="curve")
    return lay, (p + w / 2, p + h / 2)
BR, BRA = brackets(900, 780)
RET, RETA = brackets(130, 150, 36, 4, INK)
def people_row(img, t, ts, cy):
    xs = [-330, -170, 0, 170, 330]; ss_ = [0.6, 0.82, 1.0, 0.82, 0.6]
    scan = clamp((t - ts - 0.5) / 1.8)
    ret_i = 2 if scan >= 1 else (scan * 5) % 5 if False else None
    # reticle position sweeps left->right->centre
    pos = (-330 + 660 * clamp(scan * 2)) if scan < 0.5 else (330 - 330 * clamp((scan - 0.5) * 2))
    for x, s in zip(xs, ss_):
        near = abs(x - pos) < 80 and scan > 0
        col = INK if (near or (scan >= 1 and x == 0)) else (176, 168, 156)
        lay = ss(220, 240, lambda d, k: person(d, k, 110, 150, 78 * 1.0, col))
        blur_in(img, lay, (110, 120), 540 + x, cy + 6 * math.sin(t * 2 + x), t, ts + 0.25 + abs(x) / 2000, 0.5, s)
    if t > ts + 0.5:
        rx = 540 + pos
        paste_scaled(img, RET, RETA, rx, cy - 10, 1.0 + 0.04 * math.sin(t * 8), 0.95)
    if scan >= 1:
        ql, qa = wl("?", 90, "extrabold", BRAND)
        paste_scaled(img, ql, qa, 540, cy - 120, P.ppop(t, ts + 2.4, 0.3) if False else 1.0, min(1, (t - ts - 2.3) / 0.2))

def chat_card(txt, name="Unknown  陌生人"):
    w, h = 560, 190
    lay, d, p = P.card_shadow(w, h, 34)
    d.ellipse((p + 28, p + 28, p + 100, p + 100), fill=(214, 208, 198)); draw_text(d, p + 64, p + 80, "?", 44, "extrabold", (255, 255, 255), "m")
    draw_text(d, p + 120, p + 56, name, 26, "bold", MUTED)
    draw_text(d, p + 120, p + 108, txt, 42, "extrabold", INK)
    for k in range(3): d.ellipse((p + 120 + k * 22, p + 142, p + 134 + k * 22, p + 156), fill=BRAND if k == 0 else (226, 222, 216))
    return lay, (p + w / 2, p + h / 2)
CD1 = chat_card("Hello handsome"); CD2 = chat_card("Free Saturday?"); CD3 = chat_card("Casting tomorrow, 3000 RMB")

# ---------------- ghost ??? ----------------
def ghost_q():
    sz = 420; im = Image.new("RGBA", (1000, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = font(sz, "extrabold")
    d.text((500, 300), "???", font=f, fill=(0, 0, 0, 0), stroke_width=7, stroke_fill=BRAND + (110,), anchor="mm")
    for k in range(3): d.ellipse((290 + k * 210, 495, 330 + k * 210, 535), outline=BRAND + (110,), width=6)
    return im, (500, 280)
GQ, GQA = ghost_q()

# ---------------- hex ----------------
def hexa(kind, size=260):
    k = 3
    def f(d, k_):
        c = size / 2; Rr = size / 2 - 10
        pts = [(c + Rr * math.cos(math.radians(60 * i - 90)), c + Rr * math.sin(math.radians(60 * i - 90))) for i in range(6)]
        d.polygon([(x * k_, y * k_) for x, y in pts], fill=BRAND)
        # black corner brackets on lower vertices
        for i in (1, 2, 3, 4, 5):
            if i in (2, 3, 4):
                x, y = pts[i]; px, py = pts[(i + 1) % 6]; qx, qy = pts[i - 1]
                for (ox, oy) in ((px, py), (qx, qy)):
                    vx, vy = ox - x, oy - y; ln = math.hypot(vx, vy); vx, vy = vx / ln * 34, vy / ln * 34
                    d.line(((x + vx) * k_, (y + vy) * k_, x * k_, y * k_), fill=INK, width=int(6 * k_))
        w = (255, 255, 255); wd = int(6 * k_); s = size / 260
        d.ellipse(((c - 62 * s) * k_, (c - 62 * s) * k_, (c + 62 * s) * k_, (c + 62 * s) * k_), outline=w, width=wd)
        if kind == "time":
            d.line((c * k_, c * k_, c * k_, (c - 38 * s) * k_), fill=w, width=wd); d.line((c * k_, c * k_, (c + 28 * s) * k_, (c + 16 * s) * k_), fill=w, width=wd)
            for a in range(0, 360, 30):
                r0, r1 = 50 * s, 58 * s; aa = math.radians(a)
                d.line(((c + r0 * math.cos(aa)) * k_, (c + r0 * math.sin(aa)) * k_, (c + r1 * math.cos(aa)) * k_, (c + r1 * math.sin(aa)) * k_), fill=w, width=int(3 * k_))
        elif kind == "gig":
            d.rounded_rectangle(((c - 38 * s) * k_, (c - 16 * s) * k_, (c + 38 * s) * k_, (c + 32 * s) * k_), 8 * k_, outline=w, width=wd)
            d.arc(((c - 18 * s) * k_, (c - 38 * s) * k_, (c + 18 * s) * k_, (c - 2 * s) * k_), 180, 360, fill=w, width=wd)
            d.line(((c - 30 * s) * k_, (c + 26 * s) * k_, (c + 30 * s) * k_, (c - 10 * s) * k_), fill=w, width=wd)
        else:
            d.polygon([((c - 34 * s) * k_, (c - 30 * s) * k_), ((c + 34 * s) * k_, (c - 30 * s) * k_), ((c + 34 * s) * k_, (c + 4 * s) * k_), (c * k_, (c + 40 * s) * k_), ((c - 34 * s) * k_, (c + 4 * s) * k_)], outline=w, width=wd)
            d.text((c * k_, (c - 8 * s) * k_), "?", font=font(int(50 * s * k_), "extrabold"), fill=w, anchor="mm")
    return ss(size, size, f, 3), (size / 2, size / 2)
HXN = {kk: hexa(kk) for kk in ("time", "gig", "trust")}
def draw_poly(img, pts, prog, col=INK, w=4):
    d = ImageDraw.Draw(img)
    lens = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(lens) * clamp(prog); out = [pts[0]]
    for i, ln in enumerate(lens):
        if tot >= ln: out.append(pts[i + 1]); tot -= ln
        else:
            f = tot / ln; out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
    if len(out) > 1: d.line(out, fill=col, width=w, joint="curve")

# ---------------- pills ----------------
def pill_s(txt, solid, size):
    w = int(text_w(txt, size, "bold")) + 76; h = int(size * 2.3); p = 14
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if solid: d.rounded_rectangle((p, p, p + w, p + h), h // 2, fill=BRAND)
    else: d.rounded_rectangle((p, p, p + w, p + h), h // 2, fill=(255, 255, 255), outline=INK, width=3)
    draw_text(d, p + w / 2, p + h / 2 + size * 0.34, txt, size, "bold", (255, 255, 255) if solid else INK, "m")
    return lay, (p + w / 2, p + h / 2), w + 2 * p, h
PILLS_DEF = [("They're clearer.", True, 22.42, 0, 0), ("Passport-verified people", False, P.T(56), 0, 1),
             ("Agents you can check", True, P.T(58), 1, 0), ("Blind ratings, both ways", False, P.T(62), 1, 1),
             ("No contact details in chat", True, P.T(66), 2, 0)]
def build_pills():
    size = 56
    while True:
        items = [pill_s(t, s, size) for t, s, *_ in PILLS_DEF]
        if all(i[2] <= 880 for i in items): break
        size -= 2
    out = []; y0 = 560; rh = 175
    xs = {}
    for ri, it in enumerate(items): xs[id(it)] = (540 + (-70 if ri % 2 == 0 else 70), y0 + ri * rh)
    for it, d in zip(items, PILLS_DEF):
        out.append((d[0], d[1], xs[id(it)], d[2]))
    return out
PILLS = build_pills()

# ---------------- end ----------------
CHARS = "abcdefghijklmnopqrstuvwxyz0123456789#%&@"
def scramble(img, t, final, size, cx, by, t0, per=0.08, wts=("extrabold", INK), cols=None):
    wt = "extrabold"; total = text_w(final, size, wt); x = cx - total / 2; rnd = random.Random(int(t * 30))
    for i, ch in enumerate(final):
        x0 = x + text_w(final[:i], size, wt)
        if t < t0: continue
        done = t0 + i * per
        col = (BRAND if (cols and i in cols) else INK)
        if t >= done + 0.12: c = ch
        else:
            c = rnd.choice(CHARS) if ch.isascii() else rnd.choice("吗你好嘛的")
        lay, anc = wl(c, size, wt, col)
        paste_scaled(img, lay, anc, x0 + text_w(ch, size, wt) / 2, by, 1.0, min(1, (t - t0) / 0.12))

def ellipse_draw(img, cx, cy, rx, ry, prog, col=BRAND):
    k = 2; w = int(2 * rx + 120); h = int(2 * ry + 120)
    lay = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.arc((60 * k, 60 * k, (w - 60) * k, (h - 60) * k), -90, -90 + 360 * clamp(prog), fill=col + (255,), width=7 * k)
    g = lay.filter(ImageFilter.GaussianBlur(18 * k)); g = ImageEnhance_alpha(g, 0.9)
    lay.alpha_composite(g) if False else None
    base = Image.alpha_composite(g, lay).resize((w, h), Image.LANCZOS)
    img.paste(base, (int(cx - w / 2), int(cy - h / 2)), base)
def ImageEnhance_alpha(im, f):
    a = im.getchannel("A").point(lambda v: min(255, int(v * 2.2 * f))); im = im.copy(); im.putalpha(a); return im

WM, WMA = R.wordmark(150)
TY = {  # typed schedule (t0, cps) shared with audio
    "trust": (0.5, 20), "gigA": (2.2, 17), "gigB": (3.5, 17), "strangerA": (4.9, 17), "strangerB": (5.7, 17),
    "cast": (9.3, 17), "cant": (13.0, 17), "neither": (14.5, 17), "wastes": (17.1, 18), "aren": (21.4, 20),
    "tag1": (33.0, 28), "url": (32.95, 12)}
CLICKS = []
def reg(k, text): CLICKS.append((TY[k][0], len(text.replace(" ", "")), TY[k][1]))
for k, tx in (("trust", "Trust is expensive"), ("gigA", "Because"), ("gigB", "every gig starts"), ("strangerA", "A stranger"), ("strangerB", "on WeChat"),
              ("cast", "Casting agent or Kevin?"), ("cant", "You can't tell."), ("neither", "Neither can they."), ("wastes", "Everyone wastes time."),
              ("aren", "aren't louder."), ("tag1", "Foreign talent. Chinese agents."), ("url", "laowai.ma")): reg(k, tx)

S_ = lambda s, c=INK, k=1.0: (s, "extrabold", c, k)
SE_ = lambda s, c=BRAND, k=1.25: (s, "serif", c, k)

def whip(img, t, i):
    s = scene_idx(t); ts, te = SC[s], SC[s + 1]
    pe = clamp((t - (te - 0.2)) / 0.2) if s < 8 else 0
    pn = 1 - clamp((t - ts) / 0.24) if s > 0 else 0
    a = max(pe ** 2, pn ** 2)
    if a < 0.02: return img
    dx = int(-160 * pe ** 2 + 160 * pn ** 2)
    arr = np.asarray(img)
    if dx: arr = np.roll(arr, dx, axis=1)
    arr = hblur_np(arr.astype(np.float32), 60 * a)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def frame(i):
    t = i / FPS
    s = scene_idx(t); ts = SC[s]
    img = P.BG.copy(); bg_motion(img, t)
    if s == 7:
        a = clamp((t - ts) / 0.8)
        paste_scaled(img, RING, RINGA, 130 + 30 * math.sin(t * 0.7), 180, 1.0, a * 0.9, rot=t * 6)
        paste_scaled(img, RING, RINGA, 980, 1560 + 24 * math.cos(t * 0.6), 0.85, a * 0.8, rot=-t * 5)
    if s == 0:
        glow(img, 540, 900, t, 0.9, 1.5)
        particles(img, t, 1.0, 540, 940)
        lay, anc = wl("Trust", 210, "extrabold", INK)
        if t < 0.5:
            p = clamp(t / 0.5); e = out_expo(p)
            L = lay.filter(ImageFilter.GaussianBlur(max(0.1, 30 * (1 - e) ** 2)))
            paste_scaled(img, L, anc, 540, 900, 2.4 - 1.4 * e, min(1, p * 2.5))
        else:
            typed(img, t, [S_("Trust is ", INK, 1.0), SE_("expensive", BRAND, 1.2)], 104, 540, 900, 0.5, 20)
            blur_in(img, *wl("信任，很贵。", 48, "bold", MUTED), 540, 1040, t, 1.9, 0.4)
    elif s == 1:
        glow(img, 700, 1000, t, ts, 1.1, 0.7)
        dial_scene(img, t, ts)
        typed(img, t, [S_("Because", INK, 1.0)], 72, 640, 930, TY["gigA"][0], TY["gigA"][1])
        typed(img, t, [SE_("every gig", BRAND, 1.3), S_(" starts", INK, 0.8)], 80, 640, 1040, TY["gigB"][0], TY["gigB"][1])
        blur_in(img, *wl("the same way.  每个机会，开头都一样。", 34, "bold", MUTED), 640, 1110, t, 4.0, 0.4)
    elif s == 2:
        k = out_cubic(clamp((t - ts) / 0.6))
        paste_scaled(img, BR, BRA, 540, 960, (0.84 + 0.16 * k) * (1 + 0.03 * (t - ts) / 4), k)
        glow(img, 540, 900, t, ts + 0.4, 1.3, 0.6)
        typed(img, t, [S_("A stranger", INK, 1.0)], 96, 540, 480, TY["strangerA"][0], TY["strangerA"][1])
        typed(img, t, [S_("on ", INK, 1.0), SE_("WeChat", BRAND, 1.3)], 96, 540, 600, TY["strangerB"][0], TY["strangerB"][1])
        people_row(img, t, ts, 940)
        blur_in(img, *wl("陌生人 · 微信", 38, "bold", MUTED), 540, 1130, t, 6.4, 0.4)
        for (CD, t0, x, y, rot, ph) in ((CD1, T(14), 330, 1250, -2, 0.0), (CD2, T(16), 760, 1390, 2, 1.7)):
            if t >= t0: R.lay_at(img, CD[0], CD[1], x, y + 9 * math.sin(t * 2 + ph), t, t0, 0.4, rot=rot)
    elif s == 3:
        glow(img, 540, 800, t, ts + 0.1, 1.6, 0.9)
        paste_scaled(img, GQ, GQA, 540, 820 + 10 * math.sin(t * 1.5), 1.0 + 0.02 * math.sin(t), clamp((t - ts) / 0.6) * 0.9)
        typed(img, t, [S_("Casting agent ", INK, 1.0), SE_("or Kevin?", BRAND, 1.25)], 82, 540, 370, TY["cast"][0], TY["cast"][1])
        R.lay_at(img, P.CA, P.CAA, 540 - 255, 840 + 8 * math.sin(t * 1.8), t, T(21) - 0.2, 0.45, rot=-2)
        R.lay_at(img, P.CK, P.CKA, 540 + 255, 840 + 8 * math.sin(t * 1.8 + 1), t, T(24) - 0.1, 0.45, rot=2)
        if t >= T(28) - 0.1:
            paste_scaled(img, P.QM, P.QMA, 540, 330 + 0, R.pop_s(t, T(28) - 0.1, 0.3) * (1 + 0.06 * math.sin(t * 6)), 0.0)
    elif s == 4:
        glow(img, 540, 880, t, ts, 1.5, 0.7)
        typed(img, t, [S_("You can't ", INK, 1.0), SE_("tell.", BRAND, 1.3)], 100, 540, 380, TY["cant"][0], TY["cant"][1])
        R.lay_at(img, P.YOU, P.YOUA, 290, 880, t, T(29) + 0.1, 0.45)
        R.lay_at(img, P.THEM, P.THEMA, 790, 880, t, T(32), 0.45)
        d = ImageDraw.Draw(img)
        for (x, t0) in ((290, T(29) + 0.4), (790, T(32) + 0.3)):
            if t > t0:
                a0 = (t - t0) * 260; paste_a = clamp((t - t0) / 0.2)
                d.arc((x - 140, 785 - 140 + 0, x + 140, 785 + 140), a0, a0 + 70, fill=BRAND, width=8)
        if t >= T(33):
            pr = clamp((t - T(33)) / 0.5)
            ex = 290 + 140 + (790 - 140 - (290 + 140)) * pr
            for xx in range(int(430), int(ex), 22): d.line((xx, 785, xx + 10, 785), fill=BRAND, width=5)
            if pr > 0.9: paste_scaled(img, *wl("?", 80, "extrabold", BRAND), 540, 810, 1 + 0.12 * math.sin(t * 8), 1)
        typed(img, t, [S_("Neither can ", INK, 1.0), SE_("they.", BRAND, 1.3)], 100, 540, 1290, TY["neither"][0], TY["neither"][1])
    elif s == 5:
        glow(img, 540, 760, t, ts, 1.5, 0.5)
        typed(img, t, [S_("Everyone wastes ", INK, 1.0), SE_("time.", BRAND, 1.25)], 80, 540, 310, TY["wastes"][0], TY["wastes"][1])
        spec = [(390, 800, "time", "Wasted time", "浪费时间", T(42) - 0.1, [(0, -135), (0, -185), (-80, -245)], "r"),
                (690, 800, "gig", "Missed gigs", "错过机会", T(47) - 0.2, [(0, -135), (0, -185), (80, -245)], "l"),
                (540, 1150, "trust", "No trust", "信任归零", T(49) - 0.25, [(0, 135), (0, 185), (80, 245)], "l")]
        for (x, y, kk, a, b, t0, poly, side) in spec:
            if t < t0: continue
            lay, anc = HXN[kk]; k = clamp((t - t0) / 0.4)
            glow(img, x, y, t, t0, 0.55, 0.6)
            r = 16 * (1 - out_expo(k)) ** 2
            L = lay.filter(ImageFilter.GaussianBlur(r)) if r > 0.8 else lay
            paste_scaled(img, L, anc, x + 0, y + 14 * math.sin(t * 1.6 + x), 0.35 + 0.65 * out_back(k, 2.2), min(1, k * 2))
            pts = [(x + dx, y + dy + 14 * math.sin(t * 1.6 + x) * 0) for dx, dy in poly]
            draw_poly(img, pts, (t - t0 - 0.2) / 0.4)
            ex, ey = pts[-1]
            ly = ey + (-12 if poly[-1][1] < 0 else 36)
            l1, a1 = wl(a, 38, "extrabold", INK); l2, a2 = wl(b, 30, "bold", MUTED)
            lx = ex + (-6 if side == "r" else 6)
            off1 = -text_w(a, 38, "extrabold") / 2 - 6 if side == "r" else text_w(a, 38, "extrabold") / 2 + 6
            blur_in(img, l1, a1, lx + off1, ly, t, t0 + 0.55, 0.35)
            blur_in(img, l2, a2, lx + (-text_w(b, 30, "bold") / 2 - 6 if side == "r" else text_w(b, 30, "bold") / 2 + 6), ly + 44, t, t0 + 0.62, 0.35)
    elif s == 6:
        glow(img, 540, 800, t, ts, 1.5, 0.8)
        if t < T(52):
            w, tw = (("Great", T(50)) if t < T(51) else ("platforms", T(51)))
            if t >= T(50): blur_in(img, *wl(w, 130, "extrabold", BRAND), 540, 820, t, tw, 0.22)
        else:
            typed(img, t, [SE_("aren't louder.", INK, 1.0)], 150, 540, 840, TY["aren"][0], TY["aren"][1])
    elif s == 7:
        for (txt, solid, (x, y), t0) in PILLS:
            if t < t0 - 0.05: continue
            lay, anc, w, h = pill_s(txt, solid, 44 if False else PILLSIZE)
            p = clamp((t - t0 + 0.05) / 0.42); e = out_expo(p)
            L = hblur_layer(lay, 46 * (1 - e) ** 1.5)
            paste_scaled(img, L, anc, x + 520 * (1 - e), y + 6 * math.sin(t * 1.4 + x), 1.0, min(1, p * 2))
            if p < 1: glow(img, x, y, t, t0, 0.35, 0.5)
        blur_in(img, *wl("实名认证 · 可查证中介 · 双向盲评 · 聊天不露联系方式", 34, "bold", MUTED), 540, 1420, t, T(66) + 0.3, 0.5)
    else:
        glow(img, 540, 440, t, ts, 1.4, 0.7)
        scramble(img, t, "laowai吗", 150, 540, 470, ts + 0.05, 0.09, cols={6})
        sp = ENV[min(i, len(ENV) - 1)]
        mouth = "big" if sp > 0.12 else ("o" if sp > 0.05 else "smile")
        R.lay_at(img, R.masc(mouth, (0, 0), blink=(t % 2.3) < 0.1), R.MA, 540, 780 - 6 * math.sin(t * 6), t, ts + 0.3, 0.45, sc=0.8)
        typed(img, t, [S_("Foreign talent. Chinese agents.", MUTED, 0.38)], 90, 540, 1060, TY["tag1"][0], TY["tag1"][1])
        blur_in(img, *wl("外国人才 · 中国经纪人 · 告别微信混乱", 34, "bold", GREY), 540, 1120, t, 33.8, 0.4)
        typed(img, t, [S_("laowai.ma", INK, 1.0)], 110, 540, 1300, TY["url"][0], TY["url"][1])
        if t >= 33.9: ellipse_draw(img, 540, 1265, 330, 90, (t - 33.9) / 0.5)
        if t >= T(78) - 0.1: R.lay_at(img, P.CT, P.CTA_, 540, 1480, t, T(78) - 0.1, 0.4)
    img = whip(img, t, i)
    # camera push
    te = SC[s + 1]; p = clamp((t - ts) / max(0.5, min(te, DUR) - ts))
    img = camera(img, zoom=1.0 + 0.05 * p)
    # captions
    if t < 32.3 and not (s == 0 and t < 0.5):
        for gi, g in enumerate(P.GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.2:
                ai = 0
                for k, (w, s2, e) in enumerate(g):
                    if t >= s2 - 0.02: ai = k
                Lc, Ac = P.CAPS[(gi, ai)]
                paste_scaled(img, Lc, Ac, 540, 1580, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06))
                break
    fade = clamp((DUR - t) / 0.3) if t > DUR - 0.3 else 1.0
    return post(img, i, glitch=0.0, grain=0.22, vignette=0.0, fade=fade)
PILLSIZE = 44
# recompute pill size consistently
def _ps():
    size = 56
    while True:
        items = [pill_s(t, s, size) for t, s, *_ in PILLS_DEF]
        if all(i[2] <= 880 for i in items): return size
        size -= 2
PILLSIZE = _ps()

# ---------------- audio ----------------
rng2 = np.random.default_rng(7)
def keyclick(g=1.0):
    n = int(0.022 * SR); t = np.arange(n) / SR
    f = rng2.uniform(5200, 8200)
    x = bp(rng2.normal(0, 1, n), f * 0.7, min(f * 1.4, 18000)) * np.exp(-t / 0.004) + np.sin(2 * np.pi * rng2.uniform(1400, 2100) * t) * np.exp(-t / 0.006) * 0.35
    return x * 0.55 * g
def tock(g=1.0):
    n = int(0.09 * SR); t = np.arange(n) / SR
    return (bp(rng2.normal(0, 1, n), 700, 1800) * np.exp(-t / 0.018) * 0.6 + np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.03) * 0.5) * g
def blip(f0=420, f1=980, g=1.0, dur=0.16):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = f0 + (f1 - f0) * (t / dur) ** 0.6
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.07) * 0.55 * g
def thump(g=1.0):
    n = int(0.28 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (58 + 70 * np.exp(-t / 0.05)) * t) * np.exp(-t / 0.09) * g
def sparkle(g=1.0):
    out = np.zeros(int(0.5 * SR))
    for k, f in enumerate((1568, 2093, 2637, 3136)):
        n = int(0.28 * SR); t = np.arange(n) / SR; o = k * int(0.05 * SR)
        out[o:o + n] += np.sin(2 * np.pi * f * t) * np.exp(-t / 0.07) * 0.22
    return out * g
def swoosh(dur=0.42, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6
    nz = bp(rng2.normal(0, 1, n), 400, 6500) * env
    sub = np.sin(2 * np.pi * (180 - 100 * t / dur) * t) * env * 0.25
    return (nz * 0.5 + sub) * g

def build_audio(path):
    m = Mix(DUR)
    x = vo / (np.max(np.abs(vo)) + 1e-9) * 0.82
    voice = np.zeros(m.n); voice[:min(len(x), m.n)] = x[:m.n]
    bed = Mix(DUR)
    for c in SC[1:-1]:
        bed.add(c - 0.22, swoosh(0.42), 0.9); bed.add(c + 0.03, thump(), 0.55)
    for (t0, n, cps) in CLICKS:
        for k in range(n): bed.add(t0 + k / cps, keyclick(), 0.55 + 0.25 * ((k * 7) % 3) / 2)
    # dial tocks
    k = 0
    while 2.1 + k * 0.28 < 4.55: bed.add(2.1 + k * 0.28, tock(), 0.7); k += 1
    bed.add(2.2, blip(300, 600), 0.6)
    # scene 2: reticle sweep ticks + cards
    for k in range(10): bed.add(5.1 + k * 0.18, tick(), 0.35)
    for t0 in (T(14), T(16)): bed.add(t0, blip(), 0.8); bed.add(t0, thump(), 0.3)
    # scene 3
    for t0 in (T(21) - 0.2, T(24) - 0.1): bed.add(t0, blip(380, 880), 0.85); bed.add(t0, thump(), 0.35)
    bed.add(T(24) + 0.1, sparkle(), 0.5)
    # scene 4
    for t0 in (T(29) + 0.1, T(32)): bed.add(t0, blip(330, 700), 0.8)
    for k in range(6): bed.add(T(33) + k * 0.07, tick(), 0.4)
    # scene 5 hexes
    for t0 in (T(42) - 0.1, T(47) - 0.2, T(49) - 0.25):
        bed.add(t0, blip(260, 900), 0.9); bed.add(t0, thump(), 0.5)
        for k in range(5): bed.add(t0 + 0.2 + k * 0.07, tick(), 0.3)
        bed.add(t0 + 0.55, keyclick(), 0.8)
    # scene 6
    for t0 in (T(50), T(51)): bed.add(t0, blip(500, 1200), 0.8); bed.add(t0, thump(), 0.4)
    # pills
    for (_, _, _, t0) in PILLS: bed.add(t0 - 0.12, swoosh(0.3), 0.7); bed.add(t0 + 0.1, blip(500, 1100), 0.7)
    bed.add(PILLS[1][3] + 0.2, sparkle(), 0.5)
    # end
    for k in range(9): bed.add(32.5 + k * 0.08, keyclick(), 0.6)
    bed.add(33.9, swoosh(0.5), 0.7); bed.add(34.4, sparkle(), 0.7); bed.add(T(78) - 0.1, blip(400, 1000), 0.9)
    for tt, f in ((32.4, 330), (32.9, 392), (33.4, 494), (33.9, 392)): bed.add(tt, pluck(f), 0.35)
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
        for tt in sys.argv[2:]: Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/v2still_{tt}.png")
    elif sys.argv[1] == "audio": build_audio("out/reel04v2.wav")
    else:
        build_audio("out/reel04v2.wav")
        render(frame, int(DUR * FPS), "out/reel04v2.wav", "out/laowai_reel_04v2.mp4")
