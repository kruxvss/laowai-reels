"""Premium motion helpers: motion blur, 3D tilt, chromatic aberration, light sweep, per-letter kinetic type, spotlight."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel_lib import *

def mblur(frame_fn, i, n=4, shutter=0.55):
    """average n subframes across shutter*1 frame; frame_fn(float_i)->uint8 HxWx3"""
    if n <= 1: return frame_fn(float(i))
    acc = None
    for k in range(n):
        f = frame_fn(i - shutter * (k / (n - 1)) + shutter / 2).astype(np.float32)
        acc = f if acc is None else acc + f
    return (acc / n).astype(np.uint8)

def persp_coeffs(src, dst):
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float))

def tilt(lay, ax_deg=0.0, ay_deg=0.0, depth=1400):
    """fake 3D rotation of an RGBA layer about its centre; returns new layer (same size w/ padding), anchor offset kept centred"""
    w, h = lay.size; pad = int(max(w, h) * 0.35)
    big = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); big.paste(lay, (pad, pad))
    W2, H2 = big.size; cx, cy = W2 / 2, H2 / 2
    pts = [(-W2 / 2, -H2 / 2), (W2 / 2, -H2 / 2), (W2 / 2, H2 / 2), (-W2 / 2, H2 / 2)]
    ax, ay = math.radians(ax_deg), math.radians(ay_deg); out = []
    for x, y in pts:
        z = 0.0
        y1 = y * math.cos(ax) - z * math.sin(ax); z1 = y * math.sin(ax) + z * math.cos(ax)
        x2 = x * math.cos(ay) + z1 * math.sin(ay); z2 = -x * math.sin(ay) + z1 * math.cos(ay)
        s = depth / (depth + z2); out.append((cx + x2 * s, cy + y1 * s))
    coeffs = persp_coeffs([(0, 0), (W2, 0), (W2, H2), (0, H2)], out)
    res = big.transform((W2, H2), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    return res, (cx, cy)

def chroma(img, amt=3.0):
    if amt < 0.4: return img
    a = np.asarray(img).copy(); s = int(round(amt))
    a[..., 0] = np.roll(a[..., 0], s, axis=1); a[..., 2] = np.roll(a[..., 2], -s, axis=1)
    return Image.fromarray(a)

def spotlight(img, cx, cy, r, col, strength=0.5):
    w, h = img.size; k = 6
    ys, xs = np.mgrid[0:h // k, 0:w // k]; d = np.sqrt((xs * k - cx) ** 2 + (ys * k - cy) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** 2 * strength
    a = np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    a += (np.random.RandomState(3).rand(h, w).astype(np.float32) - 0.5) / 120
    arr = np.asarray(img).astype(np.float32); c = np.array(col, np.float32)
    arr = arr * (1 - a[..., None]) + c * a[..., None]
    img.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), (0, 0))

def sweep(img, t, t0, dur=0.7, y0=0, y1=None, col=(255, 255, 255), a=90, ang=0.35):
    p = (t - t0) / dur
    if p < 0 or p > 1: return
    w, h = img.size; x = -300 + (w + 600) * (1 - (1 - p) ** 3)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.polygon([(x, 0), (x + 160, 0), (x + 160 - h * ang, h), (x - h * ang, h)], fill=col + (a,))
    ov = ov.filter(ImageFilter.GaussianBlur(30)); img.paste(ov, (0, 0), ov)

def letters(img, txt, size, weight, col, cx, by, t, t0, stagger=0.035, dur=0.35, rise=60, blur=True):
    """per-letter kinetic: fade/rise/overshoot"""
    from reel_lib import out_back, clamp
    wtot = text_w(txt, size, weight); x = cx - wtot / 2; d = img
    for k, ch in enumerate(txt):
        wch = text_w(ch, size, weight)
        if ch != " ":
            p = clamp((t - t0 - k * stagger) / dur)
            if p > 0:
                e = out_back(p, 2.2); L, A = text_layer(ch, size, weight, col, pad=20)
                lay = L
                if blur and p < 0.7: lay = L.filter(ImageFilter.GaussianBlur((0.7 - p) * 10))
                paste_scaled(img, lay, A, x + wch / 2, by + rise * (1 - e), 0.8 + 0.2 * e, min(1, p * 2.5))
        x += wch
