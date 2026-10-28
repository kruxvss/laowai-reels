"""Reel 03 - knowledge (VO: jimmy) - China's new exit/entry rules (Order 841): false statements -> 1-5yr entry ban."""
import sys, json, math, wave
sys.path.insert(0, "/home/claude/reels")
import reel_02 as R
from reel_lib import *
INK, BRAND, RLIGHT, CREAM, MUTED = R.INK, R.BRAND, R.RLIGHT, R.CREAM, R.MUTED
PAPER = (245, 239, 230); NIGHT = (11, 11, 10); GREEN = (46, 160, 90); GREENL = (60, 190, 100); DIM = (150, 144, 132)
DUR = 41.6
WN = json.load(open("/home/claude/vo/words_new.json"))   # [word, start, end, idx]
def T(idx, k=1):  # start time of original word idx
    for w, s, e, i in WN:
        if i == idx: return s
    raise KeyError(idx)
def E(idx):
    for w, s, e, i in WN:
        if i == idx: return e

def paper_card(w, h, fill=PAPER, off=14, r=34, outline=INK, p=40):
    lay = Image.new("RGBA", (w + 2 * p + off, h + 2 * p + off), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p + off, p + off, p + w + off, p + h + off), r, fill=INK)
    d.rounded_rectangle((p, p, p + w, p + h), r, fill=fill, outline=outline, width=6)
    return lay, d, p

def stamp(txt, sub, col, size=120, w=900, rot=0):
    h = int(size * 1.7) + (70 if sub else 0)
    p = 30
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p, p, p + w, p + h), 26, fill=PAPER, outline=col, width=14)
    d.rounded_rectangle((p + 18, p + 18, p + w - 18, p + h - 18), 16, outline=col, width=5)
    draw_text(d, p + w / 2, p + 18 + int(size * 1.15), txt, size, "extrabold", col, "m")
    if sub: draw_text(d, p + w / 2, p + h - 40, sub, 46, "bold", col, "m")
    return lay, (p + w / 2, p + h / 2)

# ---- hotpot ----
def hotpot(S=2):
    n = 640
    im = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c, Rr = n // 2 * S, 250 * S
    k = lambda v: v * S
    d.rounded_rectangle((c - Rr - k(70), c - k(26), c - Rr + k(10), c + k(26)), k(24), fill=INK)
    d.rounded_rectangle((c + Rr - k(10), c - k(26), c + Rr + k(70), c + k(26)), k(24), fill=INK)
    d.ellipse((c - Rr - k(22), c - Rr - k(22), c + Rr + k(22), c + Rr + k(22)), fill=INK)
    d.ellipse((c - Rr, c - Rr, c + Rr, c + Rr), fill=(250, 244, 232))
    d.pieslice((c - Rr, c - Rr, c + Rr, c + Rr), 90, 270, fill=BRAND)
    h = Rr // 2
    d.ellipse((c - h, c - Rr, c + h, c), fill=BRAND)
    d.ellipse((c - h, c, c + h, c + Rr), fill=(250, 244, 232))
    d.ellipse((c - k(26), c - Rr // 2 - k(26), c + k(26), c - Rr // 2 + k(26)), fill=(250, 244, 232))
    d.ellipse((c - k(26), c + Rr // 2 - k(26), c + k(26), c + Rr // 2 + k(26)), fill=BRAND)
    for bx, by, br in ((-150, -90, 22), (-90, 100, 16), (150, 90, 20), (110, -120, 14), (170, -30, 12)):
        d.ellipse((c + k(bx - br), c + k(by - br), c + k(bx + br), c + k(by + br)), fill=(255, 255, 255, 200), outline=INK, width=k(4))
    return im.resize((n, n), Image.LANCZOS)
POT = hotpot()
POTL, POTA = POT, (320, 320)

# ---- layers ----
EYEB, EYEBA = R.plain("// LAOWAI LOG 02 - NEW RULE", 30, "mono", DIM)
H_A1, H_A1A = R.rich([("China's entry rules", "extrabold", CREAM, 1.0)], 96, shadow=False)
H_A2, H_A2A = R.rich([("just ", "extrabold", CREAM, 1.0), ("changed", "serif", RLIGHT, 1.3), (".", "extrabold", CREAM, 1.0)], 110, shadow=False)
Z_A, Z_AA = R.plain("中国出入境新规，已生效", 52, "bold", DIM)
def date_card():
    lay, d, p = paper_card(640, 560)
    draw_text(d, p + 320, p + 130, "SEP", 100, "extrabold", BRAND, "m")
    draw_text(d, p + 320, p + 360, "15", 270, "extrabold", INK, "m")
    draw_text(d, p + 320, p + 450, "2026", 80, "extrabold", MUTED, "m")
    draw_text(d, p + 320, p + 520, "2026年9月15日起", 40, "bold", MUTED, "m")
    return lay, (p + 320, p + 280)
DATE, DATEA = date_card()

def art_card():
    lay, d, p = paper_card(900, 520)
    draw_text(d, p + 450, p + 90, "STATE COUNCIL ORDER NO. 841", 34, "mono", MUTED, "m")
    draw_text(d, p + 450, p + 330, "ARTICLE 5", 150, "extrabold", INK, "m")
    draw_text(d, p + 450, p + 440, "第五条 · 国务院令第841号", 52, "bold", BRAND, "m")
    return lay, (p + 450, p + 260)
ART, ARTA = art_card()

def form_card():
    lay, d, p = paper_card(920, 640)
    d.rounded_rectangle((p + 6, p + 6, p + 914, p + 110), 30, fill=INK)
    draw_text(d, p + 40, p + 78, "VISA APPLICATION", 44, "extrabold", CREAM)
    draw_text(d, p + 880, p + 76, "签证申请", 40, "bold", (200, 194, 180), "r")
    for yy in (190, 300, 410):
        d.line((p + 60, p + yy + 40, p + 860, p + yy + 40), fill=(205, 196, 180), width=4)
    draw_text(d, p + 60, p + 175, "Name", 34, "bold", MUTED); draw_text(d, p + 60, p + 285, "Purpose of visit  目的", 34, "bold", MUTED); draw_text(d, p + 60, p + 395, "Documents  材料", 34, "bold", MUTED)
    # scribbles
    d.line([(p + 220, p + 215), (p + 260, p + 200), (p + 320, p + 222), (p + 380, p + 205)], fill=(120, 110, 96), width=5, joint="curve")
    d.rounded_rectangle((p + 60, p + 450, p + 330, p + 520), 12, outline=(205, 196, 180), width=4)
    d.rounded_rectangle((p + 360, p + 450, p + 630, p + 520), 12, outline=(205, 196, 180), width=4)
    return lay, (p + 460, p + 320)
FORM, FORMA = form_card()

def pill_l(txt, zh, col=BRAND, w=880):
    h = 140; p = 26
    lay = Image.new("RGBA", (w + 2 * p + 10, h + 2 * p + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((p + 10, p + 10, p + w + 10, p + h + 10), 40, fill=PAPER)
    d.rounded_rectangle((p, p, p + w, p + h), 40, fill=col, outline=PAPER, width=5)
    draw_text(d, p + w / 2, p + 70, txt, 52, "extrabold", CREAM, "m")
    draw_text(d, p + w / 2, p + 118, zh, 36, "bold", (255, 226, 220), "m")
    return lay, (p + w / 2, p + h / 2)
P1, P1A = pill_l("FALSE MATERIALS", "虚假材料"); P2, P2A = pill_l("FALSE STATEMENT", "虚假陈述")
P3, P3A = pill_l("AT THE VISA APPLICATION", "申请签证时", (60, 56, 50)); P4, P4A = pill_l("OR AT THE BORDER", "或入境口岸", (60, 56, 50))

ST1, ST1A = stamp("ENTRY BAN", None, RLIGHT, 118, 760)
ST2, ST2A = stamp("1 TO 5 YEARS", "禁止入境 1至5年", RLIGHT, 88, 800)
SLAP, SLAPA = R.rich([("Not a ", "extrabold", CREAM, 1.0), ("slap", "serif", RLIGHT, 1.3)], 120, shadow=False)
SLAP2, SLAP2A = R.rich([("on the wrist.", "extrabold", CREAM, 1.0)], 120, shadow=False)
SLZ, SLZA = R.plain("这可不是轻描淡写", 52, "bold", DIM)
HP0, HP0A = R.rich([("Hotpot: ", "extrabold", CREAM, 1.0), ("0", "extrabold", RLIGHT, 1.0)], 150, shadow=False)
HPZ, HPZA = R.plain("火锅：0。（最多5年）", 50, "bold", DIM)

def mini_card(label, val, zh, fill=PAPER, ink=INK):
    lay, d, p = paper_card(900, 250, fill=fill)
    draw_text(d, p + 50, p + 76, label, 36, "mono", MUTED if fill == PAPER else (255, 220, 214))
    draw_text(d, p + 50, p + 170, val, 84, "extrabold", ink)
    draw_text(d, p + 850, p + 170, zh, 62, "bold", ink if fill == PAPER else CREAM, "r")
    return lay, (p + 450, p + 125)
C_FT, C_FTA = mini_card("FORM  申请表", "Tourist", "旅游")
C_FW, C_FWA = mini_card("FORM  申请表", "Work", "工作")
C_PW, C_PWA = mini_card("REAL PLAN  实际计划", "Working", "工作", BRAND, CREAM)
ST_MIS, ST_MISA = stamp("MISMATCH", None, RLIGHT, 110, 700)
ST_MAT, ST_MATA = stamp("MATCH", None, GREEN, 120, 600)

def agent_card():
    lay, d, p = paper_card(900, 520)
    d.ellipse((p + 50, p + 50, p + 190, p + 190), fill=INK)
    draw_text(d, p + 120, p + 150, "?", 100, "extrabold", CREAM, "m")
    draw_text(d, p + 230, p + 100, "VISA AGENT", 62, "extrabold", INK); draw_text(d, p + 230, p + 160, "签证中介", 46, "bold", MUTED)
    d.line((p + 50, p + 240, p + 850, p + 240), fill=(205, 196, 180), width=4)
    draw_text(d, p + 130, p + 345, "Record-filing  备案", 52, "bold", INK)
    d.rounded_rectangle((p + 50, p + 295, p + 110, p + 355), 12, fill=(255, 252, 244), outline=INK, width=6)
    return lay, (p + 450, p + 260)
AG, AGA = agent_card()
def bubble(txt, zh, w=820):
    h = 200; p = 30
    lay = Image.new("RGBA", (w + 2 * p, h + 2 * p + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(p + 120, p + h - 4), (p + 90, p + h + 44), (p + 190, p + h - 4)], fill=INK)
    d.rounded_rectangle((p + 8, p + 8, p + w + 8, p + h + 8), 44, fill=INK)
    d.rounded_rectangle((p, p, p + w, p + h), 44, fill=BRAND, outline=INK, width=6)
    draw_text(d, p + w / 2, p + 96, txt, 58, "extrabold", CREAM, "m"); draw_text(d, p + w / 2, p + 156, zh, 40, "bold", (255, 226, 220), "m")
    return lay, (p + w / 2, p + h / 2)
BUB, BUBA = bubble("Show me your record-filing.", "请出示你的备案。")
CHK, CHKA = R.check_layer(110)
DISC, DISCA = R.plain("Not legal advice. Check the National Immigration Administration.", 30, "bold", DIM)
DISC2, DISC2A = R.plain("Not legal advice. Check the National Immigration Administration.", 30, "bold", MUTED)

# end card
WM, WMA = R.wordmark(150)
EL1, EL1A = R.rich([("Passport-verified ", "extrabold", INK, 1.0), ("people", "serif", BRAND, 1.25), (".", "extrabold", INK, 1.0)], 76)
EL2, EL2A = R.rich([("Agents you can ", "extrabold", INK, 1.0), ("check", "serif", BRAND, 1.25), (".", "extrabold", INK, 1.0)], 76)
EL3, EL3A = R.plain("Paperwork starts with knowing who you're dealing with.", 34, "bold", MUTED)
EZ, EZA = R.plain("实名认证的人，可查证的中介。", 44, "bold", MUTED)
CTA, CTAA = R.pill("Sign up at laowai.ma")

# captions
def groups():
    gs, cur = [], []
    for w, s, e, i in WN:
        if s < 30.85:
            cur.append((w, s, e))
            if w[-1] in ".,?" or len(cur) >= 6:
                gs.append(cur); cur = []
    if cur: gs.append(cur)
    return gs
GROUPS = groups()
CAPS = {}
def cap_layer(g, active):
    size = 56; maxw = 940
    words = [w for w, s, e in g]
    lines, cur = [], []
    for w in words:
        t = " ".join(cur + [w])
        if text_w(t, size, "extrabold") <= maxw: cur.append(w)
        else: lines.append(cur); cur = [w]
    lines.append(cur)
    lay = Image.new("RGBA", (1000, 80 * len(lines) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k = 0
    for li, ln in enumerate(lines):
        txt = " ".join(ln); x = 500 - text_w(txt, size, "extrabold") / 2; y = 66 + li * 80
        for w in ln:
            col = RLIGHT if k == active else CREAM
            draw_text(d, x + 3, y + 3, w, size, "extrabold", (0, 0, 0)); draw_text(d, x, y, w, size, "extrabold", col)
            x += text_w(w + " ", size, "extrabold"); k += 1
    return lay, (500, 66)
for gi, g in enumerate(GROUPS):
    for ai in range(len(g)):
        CAPS[(gi, ai)] = cap_layer(g, ai)

# mouth envelope
vo = np.frombuffer(wave.open("/home/claude/vo/vo2c.wav").readframes(10**9), dtype=np.int16).astype(np.float64) / 32768
ENV = np.array([np.sqrt(np.mean(vo[int(i / FPS * 44100): int((i + 1) / FPS * 44100)] ** 2) + 1e-12) if int(i / FPS * 44100) < len(vo) - 100 else 0.0 for i in range(int(DUR * FPS))])

CUTS = [3.29, 6.66, 12.21, 15.59, 17.49, 20.18, 25.58, 30.88]
def lay_at(*a, **k): return R.lay_at(*a, **k)
def ppop(t, t0, d=0.3): return R.pop_s(t, t0, d)

def frame(i):
    t = i / FPS
    glitch = max([max(0, 1 - (t - c) / 0.12) for c in CUTS if 0 <= t - c < 0.12] or [0])
    punch = 0.0
    for c in (T(39), T(44)) :
        if 0 <= t - c < 0.35: punch = max(punch, 1 - (t - c) / 0.35)
    end = t >= 30.88
    img = (R.BG_C if end else R.BG_N).copy()
    sx = sy = 0
    for c in (T(39), T(44), 23.1):
        if 0 <= t - c < 0.25:
            r = np.random.default_rng(i); sx, sy = int(r.integers(-12, 12)), int(r.integers(-12, 12))
    if not end: paste_scaled(img, EYEB, EYEBA, 540, 190, 1, min(1, t / 0.1))
    if t < 3.29:
        lay_at(img, H_A1, H_A1A, 540, 360, t, 0, 0.01); lay_at(img, H_A2, H_A2A, 540, 500, t, 0, 0.01); lay_at(img, Z_A, Z_AA, 540, 590, t, 0.3, 0.3)
        lay_at(img, DATE, DATEA, 540, 930, t, 0.0, 0.01, rot=-3, sc=1.2)
    elif t < 6.66:
        lay_at(img, ART, ARTA, 540, 760, t, 3.29, 0.35, rot=2)
    elif t < 12.21:
        lay_at(img, FORM, FORMA, 540, 560, t, 6.66, 0.35, sc=0.78)
        tk = T(21)
        lay_at(img, P1, P1A, 540, 895, t, T(20), 0.3, rot=-1.5); lay_at(img, P2, P2A, 540, 895 + 135, t, T(24), 0.3, rot=1.2)
        if t >= T(26): lay_at(img, P3, P3A, 540, 895 + 270, t, T(26), 0.3, rot=-0.8)
        if t >= T(32): lay_at(img, P4, P4A, 540, 895 + 405, t, T(32), 0.3, rot=0.8)
    elif t < 15.59:
        lay_at(img, ST1, ST1A, 540, 700 + sy, t, T(39), 0.22, rot=-7, sc=1.0)
        lay_at(img, ST2, ST2A, 540 + sx, 1040 + sy, t, T(44), 0.22, rot=5)
        if t < T(39): lay_at(img, FORM, FORMA, 540, 700, t, 0, 0.01, sc=0.8, alpha=0.5)
    elif t < 17.49:
        lay_at(img, SLAP, SLAPA, 540, 620, t, 15.59, 0.3); lay_at(img, SLAP2, SLAP2A, 540, 790, t, 16.2, 0.3); lay_at(img, SLZ, SLZA, 540, 900, t, 16.5, 0.3)
    elif t < 20.18:
        lay_at(img, POTL, POTA, 540, 760, t, 17.49, 0.4, rot=0 + 6 * math.sin(t * 3))
        if t >= T(59):
            kk = ppop(t, T(59), 0.2)
            d = ImageDraw.Draw(img)
            a = int(255 * min(1, kk))
            d.line((300, 520, 780, 1000), fill=RLIGHT, width=44); d.line((780, 520, 300, 1000), fill=RLIGHT, width=44)
        if t >= T(60): lay_at(img, HP0, HP0A, 540, 1220, t, T(60), 0.25)
    elif t < 25.58:
        lay_at(img, C_FW if t >= T(74) else C_FT, C_FWA, 540, 520, t, 20.4, 0.3, rot=-1.0)
        lay_at(img, C_PW, C_PWA, 540, 840, t, T(67), 0.3, rot=1.0)
        if T(69) <= t < T(74): lay_at(img, ST_MIS, ST_MISA, 540 + sx, 1130 + sy, t, T(69) + 0.05, 0.2, rot=-6)
        if t >= T(74): lay_at(img, ST_MAT, ST_MATA, 540, 1130, t, T(74), 0.25, rot=-4)
        if t >= T(74) + 0.2: paste_scaled(img, CHK, CHKA, 640, 520, ppop(t, T(74) + 0.2, 0.3), 1, 8)
    elif t < 30.88:
        lay_at(img, AG, AGA, 540, 690, t, 25.58, 0.35, rot=-1.0)
        if t >= T(88): lay_at(img, BUB, BUBA, 540, 1090, t, T(88), 0.3, rot=1)
        if t >= T(92): paste_scaled(img, CHK, CHKA, 200 + 0, 640 + 0, ppop(t, T(92) + 0.4, 0.3), 1, 6) if False else None
        if t >= T(93) + 0.1:
            d = ImageDraw.Draw(img)
            kk = ppop(t, T(93) + 0.1, 0.3)
            paste_scaled(img, CHK, CHKA, 215, 692, kk, 1, 0)
        paste_scaled(img, DISC, DISCA, 540, 1295, 1, min(1, (t - 27.0) / 0.4))
    else:
        lay_at(img, WM, WMA, 540, 380, t, 30.88, 0.4)
        sp = ENV[min(i, len(ENV) - 1)]
        mouth = "big" if sp > 0.12 else ("o" if sp > 0.05 else "smile")
        blink = (t % 2.3) < 0.1
        lay_at(img, R.masc(mouth, (0, 0), blink=blink), R.MA, 540, 740 - 6 * math.sin(t * 6), t, 31.2, 0.4, sc=0.88)
        lay_at(img, EL1, EL1A, 540, 1120, t, T(108) - 0.05, 0.3)
        if t >= T(111): lay_at(img, EL2, EL2A, 540, 1225, t, T(111), 0.3)
        if t >= T(116): lay_at(img, CTA, CTAA, 540, 1390, t, T(116), 0.35)
        paste_scaled(img, DISC2, DISC2A, 540, 1520, 1, 1)
    # captions
    if t < 30.85:
        for gi, g in enumerate(GROUPS):
            if g[0][1] - 0.06 <= t <= g[-1][2] + 0.18:
                ai = 0
                for k, (w, s, e) in enumerate(g):
                    if t >= s - 0.02: ai = k
                L, A = CAPS[(gi, ai)]
                paste_scaled(img, L, A, 540, 1440, 1, min(1, (t - (g[0][1] - 0.06)) / 0.06))
                break
    zoom = 1.0 + 0.06 * punch * out_cubic(punch)
    img = camera(img, zoom=zoom)
    fade = clamp((DUR - t) / 0.3) if t > DUR - 0.3 else 1.0
    return post(img, i, glitch=glitch, grain=0.5 if not end else 0.4, vignette=0.28 if not end else 0.12, fade=fade)

def build_audio(path):
    m = Mix(DUR)
    x = vo / (np.max(np.abs(vo)) + 1e-9) * 0.80
    voice = np.zeros(m.n); voice[:min(len(x), m.n)] = x[:m.n]
    bed = Mix(DUR)
    for k in range(int(30.5 / (60 / 100))):
        tt = k * 0.6
        if k % 2 == 0: bed.add(tt, kick(), 0.5)
        bed.add(tt + 0.3, hat(), 0.25)
    for c in CUTS:
        bed.add(c - 0.3, whoosh(0.3, 0.5), 0.8); bed.add(c, boom(), 0.35)
    for tt in (T(39), T(44), 23.1 + 0.0):
        bed.add(tt, boom(), 1.0); bed.add(tt, clap(), 0.8)
    for tt in (T(20), T(24), T(26), T(32), T(67), T(88)): bed.add(tt, pop(), 0.8)
    bed.add(T(59), buzz(0.3), 0.7); bed.add(T(74), pluck(660), 0.9); bed.add(T(74), pluck(990), 0.6)
    bed.add(T(93) + 0.1, pluck(880), 0.8)
    for tt, f in ((30.88, 262), (31.4, 330), (33.63, 392), (35.34, 330), (37.25, 262)): bed.add(tt, pluck(f), 0.5)
    b = bed.buf.copy(); b = hp(b, 40)
    # duck bed under voice (envelope)
    env = np.convolve(np.abs(voice), np.ones(2205) / 2205, mode="same")
    duck = 1 - 0.78 * np.clip(env / 0.08, 0, 1)
    b = b * duck * 0.55
    y = voice + b
    y = np.tanh(y * 1.1) / np.tanh(1.1)
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.88
    n = int(0.3 * SR); y[-n:] *= np.linspace(1, 0, n)
    write_wav(path, y)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            Image.fromarray(frame(int(float(tt) * FPS))).save(f"out/r3still_{tt}.png")
    elif sys.argv[1] == "audio":
        build_audio("out/reel03.wav")
    else:
        build_audio("out/reel03.wav")
        render(frame, int(DUR * FPS), "out/reel03.wav", "out/laowai_reel_03.mp4")
