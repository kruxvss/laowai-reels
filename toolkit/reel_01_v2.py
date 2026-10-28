"""Reel 01 - talent day - 'Don't reply.' (paradox + fake notification/chat UI -> brutalist slam -> app-card UI -> end card)."""
import sys
sys.path.insert(0, "/home/claude/reels")
from reel_lib import *

BEAT = 60 / 128
BAR = BEAT * 4
DUR = 15.0
INK, BRAND, RLIGHT, CREAM = (11, 11, 10), (196, 28, 28), (220, 45, 45), (243, 240, 232)
YEL = CREAM; RED = RLIGHT; WHITE = CREAM
CHAT_BG = (18, 18, 16)
GRAY = (140, 140, 158)

MSGS = [(2.00, "Hi! You're foreign, right?", "你好！你是外国人吧？"),
        (2.85, "Casting tomorrow. 3000 RMB.", "明天试镜，3000元。"),
        (3.85, "Send a photo of your passport to confirm.", "发一张护照照片确认一下。"),
        (4.95, "Hurry, only 1 spot left!", "快点，只剩一个名额！")]
PAD = 24


def build_bubble(en, cn):
    lines = wrap(en, 44, "semibold", 690)
    w = int(max(max(text_w(l, 44, "semibold") for l in lines), text_w(cn, 36, "regular")) + 76)
    h = 154 + (len(lines) - 1) * 56
    lay = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((PAD, PAD, PAD + w, PAD + h), 40, fill=(44, 43, 38))
    for k, l in enumerate(lines):
        draw_text(d, PAD + 38, PAD + 74 + k * 56, l, 44, "semibold", WHITE)
    draw_text(d, PAD + 38, PAD + 74 + (len(lines) - 1) * 56 + 54, cn, 36, "regular", (165, 165, 182))
    return lay, w, h


BUBBLES, y = [], 480
for tb, en, cn in MSGS:
    lay, w, h = build_bubble(en, cn)
    BUBBLES.append(dict(t=tb, lay=lay, w=w, h=h, x=70, y=y))
    y += h + 30
B3 = BUBBLES[2]
B3C = (B3["x"] + B3["w"] / 2, B3["y"] + B3["h"] / 2)

# banner (bar 1)
def build_banner():
    w, h = 960, 158
    lay = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((PAD, PAD, PAD + w, PAD + h), 42, fill=(40, 39, 35))
    d.ellipse((PAD + 26, PAD + 32, PAD + 120, PAD + 126), fill=(80, 80, 98))
    draw_text(d, PAD + 73, PAD + 98, "?", 52, "black", (210, 210, 225), "m")
    draw_text(d, PAD + 148, PAD + 66, "Unknown number", 36, "bold", WHITE)
    draw_text(d, PAD + w - 28, PAD + 64, "now", 30, "regular", GRAY, "r")
    draw_text(d, PAD + 148, PAD + 118, "Hi! You're foreign, right?", 36, "regular", (200, 200, 214))
    return lay, (PAD + w / 2, PAD + h / 2)


BANNER, BANNER_A = build_banner()


def build_card(icon, en, cn):
    w, h = 940, 230
    lay = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((PAD, PAD, PAD + w, PAD + h), 44, fill=(24, 24, 22), outline=(60, 58, 52), width=3)
    tx, ty = PAD + 40, PAD + 50
    d.rounded_rectangle((tx, ty, tx + 130, ty + 130), 34, fill=BRAND)
    cx, cy = tx + 65, ty + 65
    if icon == "check":
        d.line([(cx - 30, cy + 2), (cx - 8, cy + 26), (cx + 32, cy - 24)], fill=CREAM, width=17, joint="curve")
    elif icon == "star":
        pts = []
        for k in range(10):
            r = 46 if k % 2 == 0 else 19
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=CREAM)
    else:
        d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), outline=CREAM, width=13)
        d.line([(cx - 28, cy + 28), (cx + 28, cy - 28)], fill=CREAM, width=13)
    draw_text(d, PAD + 215, PAD + 108, en, 54, "bold", WHITE)
    draw_text(d, PAD + 215, PAD + 168, cn, 38, "regular", (160, 166, 200))
    return lay, (PAD + w / 2, PAD + h / 2)


CARDS = [build_card("check", "ID verification", "身份认证"),
         build_card("star", "Blind mutual ratings", "双向盲评"),
         build_card("slash", "Report + block", "举报 + 拉黑")]
CARD_T = [11.72, 12.19, 12.66]
CARD_Y = [560, 840, 1120]

SLAMS = [(7.5, 16), (7.97, 16), (8.44, 12), (8.91, 10), (9.375, 18), (9.84, 16), (10.31, 26), (10.78, 10),
         (13.125, 22), (6.55, 14)]
CUTS = {1.875: 0.7, 7.5: 1.0, 9.375: 0.8, 11.25: 0.7, 13.125: 0.9}


def fit(s, maxw, weight, start, lo=40):
    z = start
    while z > lo and text_w(s, z, weight) > maxw:
        z -= 4
    return z


def slam(img, s, size, weight, fill, cx, by, t, t0, rot=0.0, big=0.45):
    p = (t - t0) / 0.17
    if p < 0:
        return
    sc = 1 + big * (1 - out_cubic(p))
    lay, anc = text_layer(s, size, weight, fill)
    paste_scaled(img, lay, anc, cx, by, sc, clamp(p * 4), rot * (1 - 0.3 * out_cubic(p)))


def fade_in(img, s, size, weight, fill, x, by, t, t0, dur=0.3, rise=24, anchor="l"):
    p = out_cubic((t - t0) / dur)
    if p <= 0:
        return
    lay, anc = text_layer(s, size, weight, fill)
    w = text_w(s, size, weight)
    cx = x + (w / 2 if anchor == "l" else 0)
    paste_scaled(img, lay, anc, cx, by + (1 - p) * rise, 1.0, p)


# ---------------- scenes ----------------
def scene_b1(t):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    br = 1 + 0.012 * math.sin(t * 5)
    lay, anc = text_layer("Don't reply.", 132, "black", WHITE)
    paste_scaled(img, lay, anc, W / 2, 960, br)
    d = ImageDraw.Draw(img)
    draw_text(d, W / 2, 1070, "别回复。", 64, "bold", (130, 130, 140), "m")
    if t >= 1.2:
        p = out_expo((t - 1.2) / 0.35)
        paste_scaled(img, BANNER, BANNER_A, W / 2, -120 + (200 + 120) * p + 79)
    return img


def draw_chat(t):
    img = Image.new("RGB", (W, H), CHAT_BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 150, W, 350), fill=(26, 26, 23))
    d.ellipse((60, 190, 180, 310), fill=(72, 72, 90))
    draw_text(d, 120, 272, "?", 64, "black", (205, 205, 220), "m")
    draw_text(d, 212, 246, "Unknown number", 46, "bold", WHITE)
    draw_text(d, 212, 300, "未知号码 · 23:47", 32, "regular", GRAY)
    draw_text(d, W / 2, 430, "Today 23:47", 28, "medium", (100, 100, 120), "m")
    for b in BUBBLES:
        tb = b["t"]
        if tb - 0.55 <= t < tb:
            d.rounded_rectangle((70, b["y"], 70 + 150, b["y"] + 84), 42, fill=(44, 43, 38))
            for k in range(3):
                off = 7 * math.sin((t * 9) - k * 0.9)
                d.ellipse((108 + k * 34 - 9, b["y"] + 42 - 9 + off, 108 + k * 34 + 9, b["y"] + 42 + 9 + off), fill=(170, 170, 188))
        if t >= tb:
            p = clamp((t - tb) / 0.24)
            sc = 0.84 + 0.16 * out_back(p)
            paste_scaled(img, b["lay"], (PAD + b["w"] / 2, PAD + b["h"] / 2), b["x"] + b["w"] / 2,
                         b["y"] + b["h"] / 2 + (1 - p) * 34, sc, clamp(p * 2.2))
    d = ImageDraw.Draw(img)
    # input bar - the thing you're tempted to use
    d.rounded_rectangle((60, 1380, 900, 1480), 50, fill=(34, 33, 30))
    blink = int(t * 2) % 2 == 0
    draw_text(d, 104, 1442, "Reply…", 38, "regular", (95, 95, 112))
    if blink:
        d.rectangle((96, 1410, 99, 1456), fill=(150, 150, 170))
    d.ellipse((920, 1380, 1020, 1480), fill=BRAND)
    d.polygon([(948, 1447), (948, 1413), (994, 1430)], fill=WHITE)
    return img


def scene_b4_ring(img, t):
    if t < 5.85:
        return
    p = clamp((t - 5.85) / 0.18)
    sc = 1.25 - 0.25 * out_cubic(p)
    w, h = B3["w"] + 44, B3["h"] + 44
    lay, anc = rrect_layer(w, h, 52, None, outline=RED, ow=9)
    paste_scaled(img, lay, anc, B3C[0], B3C[1], sc, clamp(p * 2))
    d = ImageDraw.Draw(img)
    if p >= 0.6:
        cx, cy = B3["x"] + B3["w"] + 6, B3["y"] - 8
        d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=RED)
        draw_text(d, cx, cy + 20, "!", 54, "black", WHITE, "m")


def scene_slam1(t):  # 7.5 - 9.375 yellow brutalist
    img = Image.new("RGB", (W, H), BRAND)
    d = ImageDraw.Draw(img)
    tape(d, 210, t, INK, CREAM, "GIGS ARE REAL  •  ")
    tape(d, 1560, t, INK, CREAM, "GIGS ARE REAL  •  ", rev=True)
    s1 = fit("THE GIGS", 920, "black", 200)
    slam(img, "THE GIGS", s1, "black", CREAM, W / 2, 740, t, 7.5)
    s2 = fit("ARE REAL.", 920, "black", 200)
    slam(img, "ARE REAL.", s2, "black", CREAM, W / 2, 740 + int(s2 * 0.95), t, 7.97, rot=-2)
    slam(img, "机会是真的。", 84, "bold", CREAM, W / 2, 1090, t, 8.44, big=0.3)
    if t >= 8.91:
        p = out_expo((t - 8.91) / 0.25)
        d = ImageDraw.Draw(img)
        d.rectangle((90, 1135, 90 + int(900 * p), 1155), fill=CREAM)
    return img


def tape(d, y, t, bg, fg, s, rev=False):
    d.rectangle((0, y, W, y + 84), fill=bg)
    w = text_w(s, 40, "black")
    off = (t * 260) % w
    x = -off if not rev else -w + off
    while x < W:
        draw_text(d, x, y + 58, s, 40, "black", fg)
        x += w


def scene_slam2(t):  # 9.375 - 11.25 inverted
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    tape(d, 210, t, BRAND, CREAM, "THE SEARCH  •  ")
    tape(d, 1560, t, BRAND, CREAM, "THE SEARCH  •  ", rev=True)
    slam(img, "THE SEARCH", fit("THE SEARCH", 920, "black", 170), "black", WHITE, W / 2, 700, t, 9.375)
    slam(img, "IS THE", fit("IS THE", 920, "black", 170), "black", WHITE, W / 2, 870, t, 9.84)
    slam(img, "GAMBLE.", fit("GAMBLE.", 920, "black", 230), "black", RLIGHT, W / 2, 1090, t, 10.31, rot=-4, big=0.6)
    slam(img, "风险在于找的方式。", 70, "bold", CREAM, W / 2, 1230, t, 10.78, big=0.3)
    return img


def scene_cards(t):  # 11.25 - 13.125 app-card UI
    img = Image.new("RGB", (W, H), (11, 11, 10))
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 90):
        d.line([(gx, 0), (gx, H)], fill=(19, 19, 17), width=2)
    for gy in range(0, H, 90):
        d.line([(0, gy), (W, gy)], fill=(19, 19, 17), width=2)
    fade_in(img, "Inside laowai吗:", 78, "black", WHITE, 70, 380, t, 11.3)
    fade_in(img, "laowai吗 里面有：", 40, "regular", (160, 166, 200), 70, 445, t, 11.4)
    for (lay, anc), ts, cy in zip(CARDS, CARD_T, CARD_Y):
        p = (t - ts) / 0.42
        if p < 0:
            continue
        off = (1 - out_expo(p)) * 1150
        paste_scaled(img, lay, anc, W / 2 + off, cy + 115)
    return img


def wordmark_layer(size):
    w1, w2 = text_w("laowai", size, "extrabold"), text_w("吗", size, "extrabold")
    pad = 40; w = int(w1 + w2) + 2 * pad; h = int(size * 1.7) + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ay = pad + int(size * 1.2)
    dd = ImageDraw.Draw(lay)
    draw_text(dd, pad, ay, "laowai", size, "extrabold", INK + (255,))
    draw_text(dd, pad + w1, ay, "吗", size, "extrabold", BRAND + (255,))
    return lay, (w / 2, ay)


def scene_end(t):  # 13.125 - 15 cream end card
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    p = (t - 13.125) / 0.17
    if p >= 0:
        lay, anc = wordmark_layer(210)
        paste_scaled(img, lay, anc, W / 2, 700, 1 + 0.55 * (1 - out_cubic(p)), clamp(p * 4))
    fade_in(img, "Foreign talent. Chinese agents.", 44, "bold", INK, W / 2, 830, t, 13.59, anchor="m")
    fade_in(img, "No WeChat chaos.", 44, "bold", BRAND, W / 2, 890, t, 13.66, anchor="m")
    fade_in(img, "外国人才。中国中介。告别微信群混乱。", 36, "regular", (126, 115, 101), W / 2, 950, t, 13.75, anchor="m")
    slam(img, "So don't reply to strangers.", fit("So don't reply to strangers.", 900, "extrabold", 58), "extrabold", INK, W / 2, 1120, t, 14.06, big=0.2)
    if t >= 14.53:
        p = clamp((t - 14.53) / 0.3)
        pulse = 1 + 0.025 * math.sin((t - 14.53) * 9)
        lay, anc = rrect_layer(760, 150, 75, BRAND)
        paste_scaled(img, lay, anc, W / 2, 1310, (0.7 + 0.3 * out_back(p)) * pulse, clamp(p * 3))
        tl, ta = text_layer("Sign up at laowai.ma", 54, "extrabold", CREAM)
        paste_scaled(img, tl, ta, W / 2, 1310 + 20, (0.7 + 0.3 * out_back(p)) * pulse, clamp(p * 3))
        if t >= 14.65:
            fade_in(img, "来注册吧", 38, "bold", INK, W / 2, 1450, t, 14.65, anchor="m")
    return img


# ---------------- frame ----------------
def frame(i):
    t = i / FPS
    zoom, cx, cy, sx, sy = 1.0, W / 2, H / 2, 0.0, 0.0
    if t < BAR:
        img = scene_b1(t)
        for a, b in ((1.2, 1.45), (1.5, 1.75)):
            if a <= t < b:
                sx += 14 * math.sin(2 * math.pi * 32 * t) * (1 - (t - a) / (b - a) * 0.4)
                sy += 7 * math.sin(2 * math.pi * 41 * t)
    elif t < 7.5:
        img = draw_chat(t)
        if t >= 5.625:
            scene_b4_ring(img, t)
        zoom = 1 + 0.035 * in_out((t - BAR) / 3.8)
        if t >= 5.7:
            p = in_out((t - 5.7) / 0.95)
            zoom = 1.035 + 0.27 * p
            cx, cy = W / 2 + (B3C[0] - W / 2) * p, H / 2 + (B3C[1] - H / 2) * p
        if 3.75 <= t < 7.5:  # heartbeat micro-shake
            step = BEAT * 2 if t < 5.625 else BEAT
            dt = (t - 3.75) % step
            sy += 5 * math.exp(-dt * 22) * (1 if t < 5.625 else 1.6)
    elif t < 9.375:
        img = scene_slam1(t)
    elif t < 11.25:
        img = scene_slam2(t)
    elif t < 13.125:
        img = scene_cards(t)
    else:
        img = scene_end(t)

    for ts, amp in SLAMS:
        dt = t - ts
        if 0 <= dt < 0.4:
            e = math.exp(-dt * 16)
            sx += amp * e * math.sin(2 * math.pi * 23 * dt)
            sy += amp * 0.8 * e * math.sin(2 * math.pi * 29 * dt + 1)
            zoom *= 1 + 0.022 * math.exp(-dt * 9)

    img = camera(img, zoom, cx, cy, sx, sy)

    if 6.5 <= t < 7.5:  # open-loop question over dimmed scene
        k = clamp((t - 6.5) / 0.15)
        img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.86 * k)
        slam(img, "Would you", 132, "black", WHITE, W / 2, 590, t, 6.55)
        slam(img, "send it?", 132, "black", WHITE, W / 2, 735, t, 6.75)
        slam(img, "你会发吗？", 72, "bold", RLIGHT, W / 2, 850, t, 6.95, big=0.3)

    g = 0.0
    for tc, s in CUTS.items():
        dt = t - tc
        if 0 <= dt < 0.22:
            g = max(g, s * math.exp(-dt / 0.06))
    fade = clamp((DUR - t) / 0.2) if t > DUR - 0.2 else 1.0
    light = 7.5 <= t < 9.375 or t >= 13.125
    return post(img, i, glitch=g, grain=0.55, vignette=0.07 if light else 0.28, fade=fade)


# ---------------- audio ----------------
def build_audio(path):
    m = Mix(DUR)
    m.add(0.02, boom(), 0.22)
    m.add(1.2, buzz(0.25), 0.9); m.add(1.5, buzz(0.25), 0.9)
    m.add(BAR - 0.45, whoosh(0.45, 0.8), 0.8)
    m.add(BAR, drone(7.4 - BAR, 55, 0.7), 0.95)
    hh = BAR
    while hh < 5.625:  # quiet pulse so the chat bars never go dead
        m.add(hh, hat(0.5), 0.3); hh += BEAT / 2
    for b in BUBBLES:
        m.add(b["t"], pop(1.0), 0.8)
    # heartbeat builds
    k = 0
    tt = 3.75
    while tt < 5.625:
        m.add(tt, heartbeat(1.0), 0.8); tt += BEAT * 2
    while tt < 7.35:
        m.add(tt, heartbeat(1.0), 0.95); tt += BEAT
    h = 5.625
    while h < 7.35:
        m.add(h, hat(0.6), 0.5 + 0.5 * (h - 5.625) / 1.75); h += BEAT / 2
    m.add(5.625, riser(1.85), 0.7)
    m.add(5.85, tick(1.0), 0.9)
    m.add(6.55, boom(), 0.45); m.add(6.75, kick(), 0.5); m.add(6.95, pop(1.0, 300, 700), 0.6)
    m.add(7.0, whoosh(0.4, 1.0), 0.8)
    # drop
    m.add(7.5, boom(), 0.9)
    m.add(7.5, hat(1.2, True), 0.8)
    start_k, end_k = int(round(7.5 / BEAT)), int(round(14.4 / BEAT))
    bass_pat = [(0, 55.0), (0.75, 55.0), (1.5, 65.41), (2, 55.0), (2.75, 82.41), (3.5, 49.0)]
    arp = [220.0, 261.63, 329.63, 261.63, 392.0, 329.63, 261.63, 329.63]
    for kk in range(start_k, end_k):
        tb = kk * BEAT
        if tb < 13.125 or True:
            m.add(tb, kick(), 0.95)
        if kk % 2 == 1:
            m.add(tb, clap(), 0.8)
        m.add(tb + BEAT / 2, hat(1.0), 0.6)
        if kk % 4 == 3:
            m.add(tb + BEAT * 0.75, hat(1.0, True), 0.5)
        if kk % 4 == 0 and tb < 13.125:
            for off, f in bass_pat:
                m.add(tb + off * BEAT, bass(f, 0.2), 0.9)
        if kk >= 20 and tb < 13.125:
            for q in range(2):
                m.add(tb + q * BEAT / 2, pluck(arp[(kk * 2 + q) % len(arp)]), 0.55)
    for tw in (9.375, 11.25, 13.125):
        m.add(tw - 0.3, whoosh(0.3, 0.9), 0.5)
    for tc in CARD_T:
        m.add(tc, tick(1.0), 0.9); m.add(tc, pop(1.0, 700, 1500), 0.5)
    m.add(11.3, pop(1.0, 400, 900), 0.4)
    m.add(13.125, stab([220.0, 261.63, 329.63, 392.0]), 0.95); m.add(13.125, boom(), 0.6)
    m.add(13.59, pop(1.0, 600, 1100), 0.6); m.add(14.06, pop(1.0, 500, 1000), 0.7)
    m.add(14.53, stab([261.63, 329.63, 392.0, 523.25]), 0.9); m.add(14.53, tick(1.0), 0.8)
    m.add(14.35, whoosh(0.65, 0.9), 0.8)
    x = m.master(fade_out=0.22, ducks=[(7.36, 7.5)])
    write_wav(path, x)


if __name__ == "__main__":
    out_dir = "/home/claude/reels/out"
    os.makedirs(out_dir, exist_ok=True)
    if len(sys.argv) >= 2 and sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            arr = frame(int(round(float(tt) * FPS)))
            Image.fromarray(arr).save(f"{out_dir}/v2still_{tt}.png")
        sys.exit(0)
    build_audio(f"{out_dir}/reel_01v2.wav")
    render(frame, int(DUR * FPS), f"{out_dir}/reel_01v2.wav", f"{out_dir}/laowai_reel_01_v2.mp4")
    Image.fromarray(frame(int(7.25 * FPS))).save(f"{out_dir}/laowai_reel_01_v2_cover.png")
    print("done")
