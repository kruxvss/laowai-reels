"""Body-rigged flat character for laowai reels.
draw_char(img, x, y, s, look, pose) -> pastes an anti-aliased character with feet at (x, y)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2  # supersample

LOOKS = {
    "mark": dict(skin=(244, 205, 178), hair=(176, 120, 66), hair2=(140, 92, 50), shirt=(38, 64, 118), shirt2=(28, 46, 88),
                 pants=(196, 176, 140), shoe=(52, 40, 34), tall=1.08, hairstyle="part", collar=(240, 236, 228)),
    "mark_old": dict(skin=(240, 200, 175), hair=(196, 192, 186), hair2=(160, 156, 150), shirt=(150, 26, 30), shirt2=(110, 18, 22),
                     pants=(46, 44, 52), shoe=(30, 28, 30), tall=1.08, hairstyle="part", collar=(240, 236, 228)),
    "prof": dict(skin=(232, 190, 150), hair=(168, 166, 162), hair2=(110, 108, 106), shirt=(118, 92, 66), shirt2=(92, 70, 50),
                 pants=(70, 64, 60), shoe=(30, 26, 24), tall=0.96, hairstyle="short", glasses=True, collar=(220, 214, 200)),
    "partner": dict(skin=(234, 192, 152), hair=(28, 26, 30), hair2=(20, 18, 22), shirt=(32, 52, 104), shirt2=(22, 36, 76),
                    pants=(32, 52, 104), shoe=(20, 20, 22), tall=0.98, hairstyle="short", gown=True, collar=(32, 52, 104)),
    "zhao": dict(skin=(226, 182, 140), hair=(26, 24, 26), hair2=(16, 14, 16), shirt=(70, 110, 160), shirt2=(52, 84, 126),
                 pants=(60, 56, 54), shoe=(28, 26, 26), tall=1.0, hairstyle="short", collar=(220, 220, 214), apron=(214, 196, 160)),
    "farmer": dict(skin=(222, 178, 136), hair=(26, 24, 26), hair2=(16, 14, 16), shirt=(150, 140, 110), shirt2=(120, 112, 88),
                   pants=(70, 80, 90), shoe=(60, 50, 40), tall=1.0, hairstyle="short", collar=(200, 190, 160), hat=True),
    "painter2": dict(skin=(230, 186, 146), hair=(40, 30, 28), hair2=(30, 22, 20), shirt=(190, 90, 60), shirt2=(150, 66, 44),
                     pants=(50, 50, 60), shoe=(30, 30, 30), tall=0.96, hairstyle="curly", collar=(240, 230, 220), apron=(200, 200, 196)),
    "talent": dict(skin=(160, 110, 80), hair=(36, 26, 22), hair2=(24, 18, 16), shirt=(196, 28, 28), shirt2=(150, 18, 18),
                   pants=(40, 44, 56), shoe=(245, 245, 245), tall=0.95, hairstyle="curly", collar=(250, 250, 250), hood=True),
}

DEF = dict(walk=0.0, amp=0.0, bob=0.0, lean=0.0, face=1, tilt=0.0,
           armL=(-14, -8), armR=(14, 8), eyes=1.0, look=(0.0, 0.0), brow=0.0, mouth="smile", mo=0.5,
           legs=True, pedal=None, prop=None, hand_prop=None, blink=False)


def _lerp(a, b, t): return a + (b - a) * t


def _limb(d, p0, a1, l1, a2, l2, w, col, k):
    """two-segment limb. angles in deg from straight down (+ = towards +x)."""
    x0, y0 = p0
    r1 = math.radians(a1); x1 = x0 + math.sin(r1) * l1; y1 = y0 + math.cos(r1) * l1
    r2 = math.radians(a2); x2 = x1 + math.sin(r2) * l2; y2 = y1 + math.cos(r2) * l2
    for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)), ((x1, y1), (x2, y2))):
        d.line((ax * k, ay * k, bx * k, by * k), fill=col, width=int(w * k))
    for (ax, ay) in ((x0, y0), (x1, y1), (x2, y2)):
        r = w * k / 2; d.ellipse((ax * k - r, ay * k - r, ax * k + r, ay * k + r), fill=col)
    return (x2, y2), (x1, y1)


def _dark(c, f=0.78): return tuple(int(v * f) for v in c[:3])


def draw_char(img, x, y, s, who="mark", **pose):
    P = dict(DEF); P.update(pose); L = LOOKS[who] if isinstance(who, str) else who
    k = s * SS * L.get("tall", 1.0)
    Wl, Hl = int(420 * k), int(640 * k)
    lay = Image.new("RGBA", (Wl, Hl), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ox, oy = 210, 600  # local origin (feet) in unscaled units
    f = P["face"]
    ph, amp = P["walk"], P["amp"]
    bob = -abs(math.sin(ph)) * 10 * amp + P["bob"]
    hipx, hipy = ox, oy - 196 + bob
    lean = math.radians(P["lean"])
    shx, shy = hipx + math.sin(lean) * 148, hipy - math.cos(lean) * 148

    def T(px, py): return px, py
    # ground shadow
    d.ellipse(((ox - 95) * k, (oy - 14) * k, (ox + 95) * k, (oy + 14) * k), fill=(0, 0, 0, 55))

    sw = math.sin(ph) * amp
    # ---- legs
    if P["legs"] and not L.get("gown"):
        if P["pedal"] is not None:
            a = P["pedal"]
            legs = []
            for sgn in (1, -1):
                th = 40 + 28 * math.sin(a + (0 if sgn > 0 else math.pi)); kn = th - 70 - 22 * math.sin(a + (0 if sgn > 0 else math.pi))
                legs.append((f * th, f * kn))
        else:
            legs = [(f * (24 * sw), f * (24 * sw) - f * max(0, -math.sin(ph + 0.6)) * 28 * amp),
                    (f * (-24 * sw), f * (-24 * sw) - f * max(0, math.sin(ph + 0.6)) * 28 * amp)]
        for i, (a1, a2) in enumerate(legs[::-1]):
            col = L["pants"] if i == 1 else _dark(L["pants"], 0.8)
            end, _ = _limb(d, (hipx + (6 if i else -6), hipy), a1, 98, a2, 92, 46, col, k)
            ex, ey = end
            d.rounded_rectangle(((ex - 22 + f * 2) * k, (ey - 12) * k, (ex + 22 + f * 22) * k, (ey + 16) * k), int(13 * k), fill=L["shoe"])
    if L.get("gown") and P["legs"]:
        d.polygon([((hipx - 62) * k, (hipy - 40) * k), ((hipx + 62) * k, (hipy - 40) * k), ((hipx + 80) * k, (oy - 30) * k), ((hipx - 80) * k, (oy - 30) * k)], fill=L["shirt2"])
        for sx in (-30, 30):
            d.rounded_rectangle(((hipx + sx - 20) * k, (oy - 34) * k, (hipx + sx + 20 + f * 12) * k, (oy + 10) * k), int(10 * k), fill=L["shoe"])
    # ---- back arm
    sL = P["armL"]; sR = P["armR"]
    swing = 28 * sw
    backA = (sL[0] - f * swing, sL[1] - f * swing)
    frontA = (sR[0] + f * swing, sR[1] + f * swing)
    shoulder_b = (shx - f * 46, shy + 18); shoulder_f = (shx + f * 46, shy + 18)
    hb, _ = _limb(d, shoulder_b, f * backA[0], 86, f * backA[1], 80, 36, L["shirt2"], k)
    d.ellipse(((hb[0] - 16) * k, (hb[1] - 16) * k, (hb[0] + 16) * k, (hb[1] + 16) * k), fill=_dark(L["skin"], 0.9))
    # ---- torso
    if not L.get("gown"): d.rounded_rectangle(((hipx - 52) * k, (hipy - 30) * k, (hipx + 52) * k, (hipy + 26) * k), int(20 * k), fill=L["pants"])
    tw0, tw1 = 64, 56
    poly = [(shx - tw0, shy - 4), (shx + tw0, shy - 4), (hipx + tw1, hipy + 10), (hipx - tw1, hipy + 10)]
    d.rounded_rectangle(((min(p[0] for p in poly)) * k, (shy - 10) * k, (max(p[0] for p in poly)) * k, (hipy + 14) * k), int(34 * k), fill=L["shirt"])
    # side shade
    d.rounded_rectangle(((shx + 22 if f > 0 else shx - 64) * k, (shy - 6) * k, (shx + 64 if f > 0 else shx - 22) * k, (hipy + 12) * k), int(30 * k), fill=L["shirt2"])
    if L.get("hood"):
        d.ellipse(((shx - 58) * k, (shy - 30) * k, (shx + 58) * k, (shy + 24) * k), fill=L["shirt2"])
        d.line(((shx - 12) * k, (shy + 10) * k, (shx - 14) * k, (shy + 70) * k), fill=(250, 250, 250), width=int(4 * k))
        d.line(((shx + 12) * k, (shy + 10) * k, (shx + 14) * k, (shy + 70) * k), fill=(250, 250, 250), width=int(4 * k))
    elif L.get("gown"):
        d.line(((shx + f * 10) * k, (shy) * k, (shx + f * 40) * k, (shy + 60) * k), fill=(200, 180, 120), width=int(5 * k))
    else:
        d.polygon([((shx - 26) * k, (shy - 6) * k), ((shx + 26) * k, (shy - 6) * k), (shx * k, (shy + 34) * k)], fill=L["collar"])
    if L.get("apron"):
        ap = L["apron"]
        d.rounded_rectangle(((shx - 46) * k, (shy + 30) * k, (shx + 46) * k, (hipy + 70) * k), int(16 * k), fill=ap)
        for (px, py, pc) in ((-20, 70, (40, 90, 200)), (18, 110, (240, 190, 40)), (-6, 150, (200, 60, 40)), (24, 40, (60, 150, 90))):
            d.ellipse(((shx + px - 7) * k, (shy + py - 6) * k, (shx + px + 7) * k, (shy + py + 6) * k), fill=pc)
    # ---- head
    hx, hy = shx + math.sin(lean) * 24, shy - 92
    tilt = P["tilt"]
    head = Image.new("RGBA", (int(240 * k), int(240 * k)), (0, 0, 0, 0)); hd = ImageDraw.Draw(head)
    c = 120; R = 80
    def H(px, py): return (c + px) * k, (c + py) * k
    # neck under head
    d.rounded_rectangle(((hx - 22) * k, (hy + 50) * k, (hx + 22) * k, (shy + 6) * k), int(10 * k), fill=_dark(L["skin"], 0.88))
    # hair back
    hs = L["hairstyle"]
    if hs == "curly":
        for ang in range(0, 360, 30):
            r = math.radians(ang); px, py = math.cos(r) * 66, math.sin(r) * 62 - 6
            if py < 30: hd.ellipse((*H(px - 30, py - 30), *H(px + 30, py + 30)), fill=L["hair"])
    hd.ellipse((*H(-R, -R), *H(R, R)), fill=L["skin"])
    # ears
    hd.ellipse((*H(-f * 80 - 13, -6), *H(-f * 80 + 13, 24)), fill=_dark(L["skin"], 0.92))
    # hair front
    if hs == "part":
        hd.chord((*H(-R - 6, -R - 10), *H(R + 6, R + 2)), 172, 368, fill=L["hair"])
        hd.ellipse((*H(-f * 18 - 66, -R - 18), *H(-f * 18 + 66, -R + 40)), fill=L["hair"])
        hd.ellipse((*H(f * 40 - 34, -R - 6), *H(f * 40 + 30, -R + 26)), fill=L["hair"])
        hd.arc((*H(-f * 18 - 50, -R - 8), *H(-f * 18 + 50, -R + 30)), 200, 320, fill=L["hair2"], width=int(5 * k))
    elif hs == "short":
        hd.chord((*H(-R - 2, -R - 4), *H(R + 2, R - 22)), 180, 360, fill=L["hair"])
    elif hs == "curly":
        for ang in range(190, 352, 22):
            r = math.radians(ang); px, py = math.cos(r) * 58, math.sin(r) * 56 - 4
            hd.ellipse((*H(px - 22, py - 22), *H(px + 22, py + 22)), fill=L["hair"])
    if L.get("hat"):
        hd.polygon([H(-R - 40, -R + 18), H(R + 40, -R + 18), H(0, -R - 50)], fill=(222, 190, 110))
        hd.line((*H(-R - 40, -R + 18), *H(R + 40, -R + 18)), fill=(170, 136, 70), width=int(5 * k))
    # face
    fx = f * 14 + P["look"][0] * 12; fy = 10 + P["look"][1] * 8
    eo = P["eyes"] if not P["blink"] else 0.08
    for ex in (-28, 28):
        cx, cy = fx + ex, fy - 4
        ew, eh = 15, 17 * max(0.08, eo) + (4 if eo > 1 else 0)
        hd.ellipse((*H(cx - ew, cy - eh), *H(cx + ew, cy + eh)), fill=(255, 255, 255))
        if eo > 0.2:
            px, py = cx + P["look"][0] * 4 + f * 2, cy + P["look"][1] * 4
            pr = 8.5
            hd.ellipse((*H(px - pr, py - pr), *H(px + pr, py + pr)), fill=(30, 26, 24))
            hd.ellipse((*H(px - 2 - 2, py - 4 - 2), *H(px - 2 + 2, py - 4 + 2)), fill=(255, 255, 255))
        # brow
        b = P["brow"]; by = cy - 24 - b * 8
        tilt_b = (b * 4) * (1 if ex < 0 else -1)
        hd.line((*H(cx - 12, by + tilt_b), *H(cx + 12, by - tilt_b)), fill=L["hair2"] if hs != "part" else _dark(L["hair"], 0.7), width=int(5 * k))
    if L.get("glasses"):
        for ex in (-28, 28):
            cx, cy = fx + ex, fy - 4
            hd.ellipse((*H(cx - 21, cy - 19), *H(cx + 21, cy + 19)), outline=(40, 36, 34), width=int(3.5 * k))
        hd.line((*H(fx - 6, fy - 6), *H(fx + 6, fy - 6)), fill=(40, 36, 34), width=int(3 * k))
    # nose
    hd.line((*H(fx + f * 4, fy + 4), *H(fx + f * 10, fy + 16)), fill=_dark(L["skin"], 0.8), width=int(4 * k))
    # cheeks
    for ex in (-40, 40):
        hd.ellipse((*H(fx + ex - 10, fy + 20), *H(fx + ex + 10, fy + 31)), fill=tuple(int(a * 0.72 + b * 0.28) for a, b in zip(L["skin"], (240, 120, 120))))
    # mouth
    m, mo = P["mouth"], P["mo"]; mx, my = fx + f * 2, fy + 40
    if m == "smile":
        hd.arc((*H(mx - 16, my - 12), *H(mx + 16, my + 8 + 6 * mo)), 15, 165, fill=(90, 36, 30), width=int(5 * k))
    elif m == "grin":
        hd.chord((*H(mx - 20, my - 12), *H(mx + 20, my + 14 + 6 * mo)), 0, 180, fill=(90, 30, 28))
        hd.chord((*H(mx - 15, my - 8), *H(mx + 15, my + 2)), 0, 180, fill=(255, 255, 255))
    elif m in ("open", "talk"):
        hgt = 4 + 16 * mo
        hd.ellipse((*H(mx - 12 - 2 * mo, my - hgt / 2), *H(mx + 12 + 2 * mo, my + hgt / 2)), fill=(90, 30, 28))
        if mo > 0.4: hd.ellipse((*H(mx - 7, my + hgt / 2 - 6), *H(mx + 7, my + hgt / 2)), fill=(220, 100, 100))
    elif m == "o":
        hd.ellipse((*H(mx - 8, my - 10), *H(mx + 8, my + 10)), fill=(90, 30, 28))
    else:
        hd.line((*H(mx - 12, my), *H(mx + 12, my)), fill=(90, 36, 30), width=int(5 * k))
    if tilt: head = head.rotate(-tilt * f, resample=Image.BICUBIC, center=(c * k, (c + 60) * k))
    lay.alpha_composite(head, (int((hx - c) * k), int((hy - c) * k)))
    # ---- front arm
    hf, elb = _limb(d, shoulder_f, f * frontA[0], 86, f * frontA[1], 80, 38, L["shirt"], k)
    d.ellipse(((hf[0] - 17) * k, (hf[1] - 17) * k, (hf[0] + 17) * k, (hf[1] + 17) * k), fill=L["skin"])
    if P["hand_prop"] == "phone":
        d.rounded_rectangle(((hf[0] - 16) * k, (hf[1] - 44) * k, (hf[0] + 16) * k, (hf[1] + 4) * k), int(6 * k), fill=(20, 20, 24))
        d.rounded_rectangle(((hf[0] - 12) * k, (hf[1] - 40) * k, (hf[0] + 12) * k, (hf[1]) * k), int(4 * k), fill=(130, 190, 255))
    elif P["hand_prop"] == "brush":
        ang = math.radians(P.get("brush_ang", -40))
        bx2, by2 = hf[0] + math.sin(ang) * 70, hf[1] - math.cos(ang) * 70
        d.line((hf[0] * k, hf[1] * k, bx2 * k, by2 * k), fill=(150, 100, 50), width=int(7 * k))
        d.ellipse(((bx2 - 8) * k, (by2 - 8) * k, (bx2 + 8) * k, (by2 + 8) * k), fill=P.get("brush_col", (240, 190, 40)))
    elif P["hand_prop"] == "fan":
        d.pieslice(((hf[0] - 60) * k, (hf[1] - 70) * k, (hf[0] + 60) * k, (hf[1] + 50) * k), 200, 340, fill=(240, 228, 196), outline=(150, 110, 60), width=int(2 * k))
    # ---- shading pass
    arr = np.asarray(lay).astype(np.float32)
    hgt = arr.shape[0]
    g = np.linspace(1.04, 0.86, hgt, dtype=np.float32)[:, None, None]
    arr[..., :3] = np.clip(arr[..., :3] * g, 0, 255)
    lay = Image.fromarray(arr.astype(np.uint8), "RGBA")
    rim = P.get("rim")
    if rim:
        a = lay.getchannel("A"); sh = Image.new("L", a.size, 0); sh.paste(a, (int(-f * 3 * k), 0))
        rm = np.clip(np.asarray(a).astype(np.int16) - np.asarray(sh).astype(np.int16), 0, 255).astype(np.uint8)
        rl = Image.new("RGBA", lay.size, rim + (0,)); rl.putalpha(Image.fromarray(rm).point(lambda v: int(v * 0.8)))
        lay.alpha_composite(rl)
    lay = lay.resize((max(1, Wl // SS), max(1, Hl // SS)), Image.LANCZOS)
    kk = k / SS
    img.alpha_composite(lay, (int(round(x - ox * kk)), int(round(y - oy * kk)))) if img.mode == "RGBA" else img.paste(lay, (int(round(x - ox * kk)), int(round(y - oy * kk))), lay)
