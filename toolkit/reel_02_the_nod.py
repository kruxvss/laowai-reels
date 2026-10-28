"""Reel 02 - humor - 'The Nod' (cream sticker editorial + original mascot). Captions-only."""
import sys, math
sys.path.insert(0, "/home/claude/reels")
from reel_lib import *

BPM = 112; BEAT = 60 / BPM
DUR = 16.0
INK, BRAND, RLIGHT, CREAM = (31, 27, 22), (196, 28, 28), (220, 45, 45), (243, 240, 232)
NIGHT = (11, 11, 10); MUTED = (126, 115, 101); GREEN = (46, 125, 70); BLUSH = (251, 236, 233)

def rich(segs, size, shadow=True, pad=40, off=5, maxw=960):
    """segs: [(text, weight, fill, scale)] -> layer, anchor(center, baseline)."""
    while sum(text_w(t, int(size * sc), wt) for t, wt, fl, sc in segs) > maxw: size -= 2
    ws = []
    for t, wt, fl, sc in segs:
        ws.append(text_w(t, int(size * sc), wt))
    w = int(sum(ws)) + 2 * pad + off; h = int(size * 1.7) + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ay = pad + int(size * 1.2)
    for layer_i in ((0, 1) if shadow else (1,)):
        x = pad
        for (t, wt, fl, sc), tw in zip(segs, ws):
            if layer_i == 0: draw_text(d, x + off, ay + off, t, int(size * sc), wt, INK)
            else: draw_text(d, x, ay, t, int(size * sc), wt, fl)
            x += tw
    return lay, (pad + (w - 2 * pad - off) / 2, ay)

def plain(s, size, wt, fill):
    return text_layer(s, size, wt, fill)

def halftone(bg, dot, rmax=8, sp=30):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    for gy in range(-1, H // sp + 2):
        for gx in range(-1, W // sp + 2):
            x = gx * sp + (sp // 2 if gy % 2 else 0); y = gy * sp
            dd = math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2))
            r = rmax * clamp((dd - 0.35) / 0.9) ** 1.3
            if r > 0.6: d.ellipse((x - r, y - r, x + r, y + r), fill=dot)
    return im

BG_C = halftone(CREAM, (226, 221, 208)); BG_N = halftone(NIGHT, (26, 26, 23), 9)

# ---------------- mascot ----------------
def mascot(mouth="smile", look=(0, 0), blink=False, sweat=False, S=2):
    w, h = 520, 540
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    k = lambda *a: tuple(v * S for v in a)
    # tail + body (ink outline = bigger shape)
    for off, col in ((10, INK), (0, BRAND)):
        d.polygon([k(110 - off, 390 + off // 2), k(78 - off, 512 + off), k(236 + off, 410)], fill=col)
        d.rounded_rectangle(k(50 - off, 50 - off, 470 + off, 430 + off), 130 * S, fill=col)
    d.polygon([k(112, 380), k(86, 494), k(228, 400)], fill=BRAND)
    d.rounded_rectangle(k(50, 50, 470, 430), 130 * S, fill=BRAND)
    # eyes
    for ex in (190, 330):
        if blink:
            d.line(k(ex - 38, 170, ex + 38, 170), fill=INK, width=9 * S)
        else:
            d.ellipse(k(ex - 52, 118, ex + 52, 222), fill=CREAM, outline=INK, width=7 * S)
            px, py = ex + look[0] * 16, 170 + look[1] * 16
            d.ellipse(k(px - 22, py - 22, px + 22, py + 22), fill=INK)
            d.ellipse(k(px - 8, py - 14, px + 2, py - 4), fill=CREAM)
    # brows for sweat
    if sweat:
        d.line(k(150, 100, 225, 86), fill=INK, width=9 * S); d.line(k(295, 86, 370, 100), fill=INK, width=9 * S)
    # mouth
    if mouth == "smile":
        d.arc(k(210, 220, 310, 290), 15, 165, fill=INK, width=9 * S)
    elif mouth == "big":
        d.pieslice(k(200, 215, 320, 300), 0, 180, fill=INK); d.pieslice(k(222, 262, 298, 300), 0, 180, fill=(220, 110, 110))
    elif mouth == "o":
        d.ellipse(k(236, 225, 284, 285), fill=INK)
    elif mouth == "flat":
        d.line(k(215, 255, 305, 255), fill=INK, width=9 * S)
    elif mouth == "wob":
        d.line(k(212, 258, 240, 246, 268, 262, 308, 248), fill=INK, width=9 * S, joint="curve")
    if sweat:
        d.polygon([k(410, 120), k(392, 160), k(428, 160)], fill=(150, 200, 235)); d.ellipse(k(392, 148, 428, 178), fill=(150, 200, 235))
    # glyph
    f = font(118 * S, "black", True)
    d.text((260 * S, 400 * S), "吗", font=f, fill=CREAM, anchor="ms")
    return im.resize((w, h), Image.LANCZOS)

MASC = {}
for m in ("smile", "big", "o", "flat", "wob"):
    for bl in (False, True):
        for lk in ((0, 0), (1, 0), (-1, 0), (0, -1)):
            for sw in (False, True):
                MASC[(m, bl, lk, sw)] = mascot(m, lk, bl, sw)
MA = (260, 270)

def masc(m="smile", look=(0, 0), blink=False, sweat=False):
    return MASC[(m, blink, look, sweat)]

# ---------------- layers ----------------
EYE, EYEA = plain("// LAOWAI LOG 01 - THE NOD", 30, "mono", MUTED)
H1a, H1aA = rich([("Someone just", "extrabold", INK, 1.0)], 112)
H1b, H1bA = rich([("spoke ", "extrabold", INK, 1.0), ("Mandarin", "serif", BRAND, 1.25), (" to you.", "extrabold", INK, 1.0)], 98)
Z1, Z1A = plain("有人刚用中文跟你说话。", 54, "bold", MUTED)
H2a, H2aA = rich([("How much", "extrabold", INK, 1.0)], 112)
H2b, H2bA = rich([("did you ", "extrabold", INK, 1.0), ("get", "serif", BRAND, 1.25), ("?", "extrabold", INK, 1.0)], 112)
Z2, Z2A = plain("你听懂了多少？", 54, "bold", MUTED)
VIBES, VIBESA = rich([("the other 60% is ", "extrabold", INK, 0.62), ("vibes", "serif", BRAND, 0.95)], 74, shadow=False)
VZ, VZA = plain("剩下60%靠感觉", 44, "bold", MUTED)
H3a, H3aA = rich([("Your ", "extrabold", INK, 1.0), ("move", "serif", BRAND, 1.25), (".", "extrabold", INK, 1.0)], 124)
Z3, Z3A = plain("你怎么办？", 54, "bold", MUTED)

def card(letter, line, sub, sel=False):
    w, h, p = 920, 200, 30
    lay = Image.new("RGBA", (w + 2 * p + 12, h + 2 * p + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p + 12, p + 12, p + w + 12, p + h + 12), 36, fill=INK)
    d.rounded_rectangle((p, p, p + w, p + h), 36, fill=BRAND if sel else (255, 252, 244), outline=INK, width=6)
    d.ellipse((p + 28, p + 50, p + 128, p + 150), fill=INK if not sel else CREAM)
    draw_text(d, p + 78, p + 118, letter, 56, "extrabold", CREAM if not sel else BRAND, "m")
    draw_text(d, p + 160, p + 96, line, 50, "extrabold", CREAM if sel else INK)
    draw_text(d, p + 160, p + 150, sub, 36, "bold", (255, 225, 220) if sel else MUTED)
    return lay, (p + w / 2, p + h / 2)

CA, CAA = card("A", "Say 听不懂", "\"I don't understand\"")
CB, CBA = card("B", "Ask them to repeat", "请再说一遍")
CC, CCA = card("C", "Nod. Smile. 好的。", "\"Sure.\"")
CCs, CCsA = card("C", "Nod. Smile. 好的。", "\"Sure.\"", True)
STAMP, STAMPA = rich([("works 100%*", "extrabold", BRAND, 1.0)], 64, shadow=False)
FOOT, FOOTA = plain("*results may vary", 32, "bold", MUTED)

N1, N1A = rich([("Nods given: ", "extrabold", CREAM, 1.0), ("14", "extrabold", RLIGHT, 1.0)], 100, shadow=False)
N2, N2A = rich([("Things agreed to: ", "extrabold", CREAM, 1.0)], 70, shadow=False)
N3, N3A = rich([("???", "extrabold", RLIGHT, 1.0)], 220, shadow=False)
NZ, NZA = plain("点头14次。答应了什么？不知道。", 44, "bold", (170, 164, 150))

def wordmark(size):
    a = text_w("laowai", size, "extrabold"); b = text_w("吗", size, "extrabold")
    lay = Image.new("RGBA", (int(a + b) + 80, int(size * 1.7) + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ay = 40 + int(size * 1.2)
    draw_text(d, 40, ay, "laowai", size, "extrabold", INK); draw_text(d, 40 + a, ay, "吗", size, "extrabold", BRAND)
    return lay, ((a + b) / 2 + 40, ay)

WM, WMA = wordmark(150)
E1, E1A = rich([("Say it ", "extrabold", INK, 1.0), ("clearly", "serif", BRAND, 1.25), (".", "extrabold", INK, 1.0)], 92)
E2, E2A = plain("Verified people. Clear messages.", 40, "bold", MUTED)
E2b, E2bA = plain("No nodding required.", 40, "bold", MUTED)
E3, E3A = plain("沟通清晰，实名认证，不用再点头装懂。", 40, "bold", MUTED)
def pill(txt):
    w, h, p = 760, 130, 30
    lay = Image.new("RGBA", (w + 2 * p + 10, h + 2 * p + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p + 10, p + 10, p + w + 10, p + h + 10), h // 2, fill=INK)
    d.rounded_rectangle((p, p, p + w, p + h), h // 2, fill=BRAND, outline=INK, width=6)
    draw_text(d, p + w / 2, p + 84, txt, 50, "extrabold", CREAM, "m")
    return lay, (p + w / 2, p + h / 2)
CTA, CTAA = pill("Sign up at laowai.ma")

def check_layer(sz=120):
    lay = Image.new("RGBA", (sz + 20, sz + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pts = [(14, sz * .55), (sz * .38, sz * .86), (sz * .92, sz * .16)]
    d.line(pts, fill=INK, width=30, joint="curve"); d.line(pts, fill=(60, 190, 100), width=18, joint="curve")
    return lay, ((sz + 20) / 2, (sz + 20) / 2)
CHK, CHKA = check_layer()

# ---------------- timeline ----------------
CUTS = [2.7, 6.4, 10.6, 13.0]
NODS = [4.9 + k * 0.45 for k in range(5)] + [8.9 + k * 0.4 for k in range(3)]
BAR_T0, BAR_T1 = 3.0, 4.7

def pop_s(t, t0, d=0.35):
    return out_back((t - t0) / d)

def lay_at(base, L, A, cx, cy, t, t0, d=0.35, rot=0.0, alpha=1.0, sc=1.0):
    if t < t0: return
    s = pop_s(t, t0, d) * sc
    paste_scaled(base, L, A, cx, cy, s, min(1, (t - t0) / 0.08) * alpha, rot)

def nod_bob(t):
    b = 0
    for n in NODS:
        dt = t - n
        if 0 <= dt < 0.36: b = max(b, math.sin(dt / 0.36 * math.pi))
    return b

def frame(i):
    t = i / FPS
    punch = 0.0
    for c in CUTS + [11.4]:
        if 0 <= t - c < 0.35: punch = max(punch, (1 - (t - c) / 0.35))
    glitch = max([max(0, 1 - (t - c) / 0.14) for c in CUTS if 0 <= t - c < 0.14] or [0])
    night = 10.6 <= t < 13.0
    img = (BG_N if night else BG_C).copy()
    # screen shake on slam
    sx = sy = 0
    if 11.4 <= t < 11.8:
        r = np.random.default_rng(i); sx, sy = r.integers(-14, 14), r.integers(-14, 14)
    if t < 2.7:
        paste_scaled(img, EYE, EYEA, 540, 190, 1, min(1, t / 0.1))
        lay_at(img, H1a, H1aA, 540, 450, t, 0.0, 0.01); lay_at(img, H1b, H1bA, 540, 590, t, 0.0, 0.01)
        lay_at(img, Z1, Z1A, 540, 730, t, 0.35, 0.3)
        b = 0.5 + 0.5 * math.sin(t * 5)
        lay_at(img, masc("o" if t > 0.9 else "smile", (1, 0) if t < 1.6 else (-1, 0), blink=(int(t * 3) % 5 == 4 and t % 0.33 < 0.12)), MA, 540, 1210 - 6 * b, t, 0.25, 0.4, sc=1.15)
    elif t < 6.4:
        u = t - 2.7
        paste_scaled(img, EYE, EYEA, 540, 190, 1)
        lay_at(img, H2a, H2aA, 540, 340, t, 2.7, 0.3); lay_at(img, H2b, H2bA, 540, 480, t, 2.8, 0.3); lay_at(img, Z2, Z2A, 540, 580, t, 3.0, 0.3)
        # bar
        bx0, by, bw, bh = 120, 820, 840, 110
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((bx0 + 8, by + 8, bx0 + bw + 8, by + bh + 8), 55, fill=INK)
        d.rounded_rectangle((bx0, by, bx0 + bw, by + bh), 55, fill=(255, 252, 244), outline=INK, width=6)
        p = 0.40 * out_cubic((t - BAR_T0) / (BAR_T1 - BAR_T0)) if t >= BAR_T0 else 0
        if p > 0.01:
            d.rounded_rectangle((bx0 + 8, by + 8, bx0 + 8 + (bw - 16) * p / 1.0, by + bh - 8), 47, fill=BRAND)
        pct = int(round(p * 100))
        lay, A = plain(f"{pct}%", 190, "extrabold", BRAND)
        paste_scaled(img, lay, A, 540, 740, 1.0 + (0.08 * max(0, 1 - (t - BAR_T1) / 0.3) if t > BAR_T1 else 0))
        # tail marks
        for q in (0.25, 0.5, 0.75):
            d.line((bx0 + bw * q, by + bh + 4, bx0 + bw * q, by + bh + 22), fill=MUTED, width=4)
        lay_at(img, VIBES, VIBESA, 540, 1050, t, 5.2, 0.3); lay_at(img, VZ, VZA, 540, 1120, t, 5.5, 0.3)
        sweat = t > 4.7
        mouth = "wob" if t > 4.7 else "o"
        bob = nod_bob(t)
        lay_at(img, masc(mouth, (0, 0), blink=False, sweat=sweat), MA, 540, 1330 + 22 * bob, t, 3.2, 0.4, sc=0.7)
    elif t < 10.6:
        paste_scaled(img, EYE, EYEA, 540, 190, 1)
        lay_at(img, H3a, H3aA, 540, 380, t, 6.4, 0.3); lay_at(img, Z3, Z3A, 540, 470, t, 6.6, 0.3)
        sel = t >= 8.6
        lay_at(img, CA, CAA, 540, 650, t, 6.9, 0.35, rot=-1.2)
        lay_at(img, CB, CBA, 540, 880, t, 7.35, 0.35, rot=1.0)
        lay_at(img, CCs if sel else CC, CCsA, 540, 1110, t, 7.8, 0.35, rot=-0.8 if not sel else 0)
        if sel:
            kk = pop_s(t, 8.6, 0.3)
            paste_scaled(img, CHK, CHKA, 905, 1040, kk, 1, 8)
            lay_at(img, STAMP, STAMPA, 660, 1370, t, 9.2, 0.3, rot=-6); lay_at(img, FOOT, FOOTA, 660, 1430, t, 9.8, 0.3)
        bob = nod_bob(t)
        lay_at(img, masc("big" if sel else "flat", (0, 0)), MA, 200, 1380 + 14 * bob, t, 7.9, 0.4, sc=0.5)
    elif t < 13.0:
        # NIGHT punchline
        if t >= 10.6:
            pass
        lay_at(img, N1, N1A, 540, 560, t, 10.65, 0.01 + 0.0)
        if t >= 11.4:
            lay_at(img, N2, N2A, 540, 900, t, 11.4, 0.25)
            lay_at(img, N3, N3A, 540 + sx, 1170 + sy, t, 11.55, 0.3)
            lay_at(img, NZ, NZA, 540, 1380, t, 12.0, 0.3)
    else:
        u = t - 13.0
        lay_at(img, WM, WMA, 540, 470, t, 13.0, 0.4)
        lay_at(img, E1, E1A, 540, 700, t, 13.25, 0.35)
        lay_at(img, E2, E2A, 540, 810, t, 13.5, 0.3); lay_at(img, E2b, E2bA, 540, 870, t, 13.6, 0.3); lay_at(img, E3, E3A, 540, 945, t, 13.7, 0.3)
        lay_at(img, CTA, CTAA, 540, 1100, t, 13.9, 0.35)
        bob = nod_bob(t + 0.0) if False else 0.5 + 0.5 * math.sin(t * 7)
        lay_at(img, masc("big", (0, 0), blink=(t % 1.3 < 0.1)), MA, 540, 1380 - 8 * bob, t, 14.1, 0.4, sc=0.68)
    zoom = 1.0 + 0.06 * punch * out_cubic(punch)
    img = camera(img, zoom=zoom)
    fade = clamp((DUR - t) / 0.25) if t > DUR - 0.25 else 1.0
    return post(img, i, glitch=glitch, grain=0.45 if not night else 0.7, vignette=0.12 if not night else 0.3, fade=fade)

# ---------------- audio ----------------
def build_audio(path):
    m = Mix(DUR)
    bt = lambda n: n * BEAT
    for k in range(int(10.6 / BEAT)):
        t = bt(k)
        if t < 10.4 and t > 0.2:
            if k % 2 == 0: m.add(t, kick(), 0.5)
            if k % 4 == 2: m.add(t, clap(), 0.3)
            m.add(t + BEAT / 2, hat(), 0.18)
    for k, f in enumerate([110, 110, 130.8, 98] * 6):
        t = bt(k * 2)
        if 2.7 < t < 10.4: m.add(t, bass(f, 0.4), 0.35)
    for c in CUTS:
        m.add(c - 0.35, whoosh(0.35, 0.5), 0.6)
        m.add(c, boom(), 0.35)
    m.add(0.0, pop(), 0.8); m.add(0.35, pop(0.7, 700, 1500), 0.6)
    for k in range(18):
        tt = BAR_T0 + k * (BAR_T1 - BAR_T0) / 17
        m.add(tt, tick(), 0.5)
    m.add(BAR_T1, stab([220, 277, 330], dur=0.5), 0.35)
    for n in NODS: m.add(n + 0.08, pop(0.6, 400, 800), 0.55)
    for tc in (6.9, 7.35, 7.8): m.add(tc, pop(), 0.6)
    m.add(8.6, pluck(660), 0.7); m.add(8.6, pluck(990), 0.5); m.add(9.2, boom(), 0.5)
    m.add(10.65, pop(), 0.5)
    m.add(11.4, boom(), 1.0); m.add(11.4, buzz(0.3), 0.5); m.add(11.55, boom(), 0.8)
    m.add(13.0, riser(0.0001), 0.0)
    for t0, f in ((13.0, 262), (13.25, 330), (13.5, 392), (13.9, 523)):
        m.add(t0, pluck(f), 0.6)
    m.add(13.9, stab([262, 330, 392], dur=0.9), 0.4)
    x = m.master(0.2, ducks=[(10.45, 11.35)])
    write_wav(path, x)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/r2still_{tt}.png")
    elif sys.argv[1] == "audio":
        build_audio("out/reel02.wav")
    else:
        build_audio("out/reel02.wav")
        render(frame, int(DUR * FPS), "out/reel02.wav", "out/laowai_reel_02.mp4")
