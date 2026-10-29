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
        glass_pill(img, "LAST YEAR  去年", 540, 250, t, T_LAST, BRAND, 40)
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
