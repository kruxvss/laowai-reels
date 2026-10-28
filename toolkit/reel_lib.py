"""Shared toolkit for the laowai reels: fonts, text, easing, camera/post FX, audio synth, encoder."""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import signal

W, H, FPS = 1080, 1920, 30
SR = 44100

INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
CJK = {
    "regular": "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "bold": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "black": "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
}
_cache = {}


def _cjk_index(path):
    for i in range(0, 6):
        try:
            f = ImageFont.truetype(path, 20, index=i)
            if "SC" in " ".join(f.getname()):
                return i
        except Exception:
            break
    return 2


def font(size, weight="bold", cjk=False):
    key = (size, weight, cjk)
    if key not in _cache:
        if cjk:
            w = "black" if weight in ("black", "extrabold") else ("regular" if weight in ("regular", "medium") else "bold")
            p = CJK[w]
            _cache[key] = ImageFont.truetype(p, size, index=_cjk_index(p))
        else:
            BF = "/home/claude/fonts/ttf/"
            p = {"regular": "manrope-400", "medium": "manrope-500", "semibold": "manrope-600",
                 "serif": "instrument-serif-400-italic", "mono": "jetbrains-mono-700", "bold": "montserrat-700", "extrabold": "montserrat-800", "black": "montserrat-800"}[weight]
            _cache[key] = ImageFont.truetype(BF + p + ".ttf", size)
    return _cache[key]


def is_cjk(ch):
    o = ord(ch)
    return o >= 0x2E80 and not (0xFF00 <= o <= 0xFFEF and False)


def runs(s):
    out, cur, cur_c = [], "", None
    for ch in s:
        c = is_cjk(ch)
        if cur_c is None or c == cur_c:
            cur += ch
        else:
            out.append((cur_c, cur)); cur = ch
        cur_c = c
    if cur:
        out.append((cur_c, cur))
    return out


def text_w(s, size, weight="bold"):
    return sum(font(size, weight, c).getlength(t) for c, t in runs(s))


def draw_text(d, x, y, s, size, weight, fill, anchor="l"):
    """Baseline-aligned mixed Latin/CJK text. y = baseline."""
    w = text_w(s, size, weight)
    if anchor == "m":
        x -= w / 2
    elif anchor == "r":
        x -= w
    for c, t in runs(s):
        f = font(size, weight, c)
        d.text((x, y), t, font=f, fill=fill, anchor="ls")
        x += f.getlength(t)
    return w


def wrap(text, size, weight, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, size, weight) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def text_layer(s, size, weight, fill, pad=40):
    """RGBA layer with text drawn so baseline anchor = (w/2+pad, pad+1.2*size). Returns layer, anchor."""
    w = int(text_w(s, size, weight)) + 2 * pad
    h = int(size * 1.7) + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ay = pad + int(size * 1.2)
    draw_text(ImageDraw.Draw(lay), w / 2, ay, s, size, weight, fill + (255,) if len(fill) == 3 else fill, "m")
    return lay, (w / 2, ay)


def paste_scaled(base, lay, anchor, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.003 or scale <= 0.01:
        return
    ax, ay = anchor
    if rot:
        # rotate about anchor
        pad = int(max(lay.size) * 0.5)
        big = Image.new("RGBA", (lay.size[0] + 2 * pad, lay.size[1] + 2 * pad), (0, 0, 0, 0))
        big.paste(lay, (pad, pad))
        big = big.rotate(rot, resample=Image.BICUBIC, center=(ax + pad, ay + pad))
        lay, ax, ay = big, ax + pad, ay + pad
    if abs(scale - 1) > 1e-3:
        lay = lay.resize((max(1, int(lay.size[0] * scale)), max(1, int(lay.size[1] * scale))), Image.BILINEAR)
        ax, ay = ax * scale, ay * scale
    if alpha < 0.999:
        lay = lay.copy()
        a = lay.getchannel("A").point(lambda v: int(v * alpha))
        lay.putalpha(a)
    base.paste(lay, (int(round(cx - ax)), int(round(cy - ay))), lay)


def rrect_layer(w, h, r, fill, outline=None, ow=0, pad=30):
    lay = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((pad, pad, pad + w, pad + h), r, fill=fill, outline=outline, width=ow)
    return lay, (pad + w / 2, pad + h / 2)


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def out_cubic(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def out_expo(x):
    x = clamp(x); return 1 - 2 ** (-10 * x) if x < 1 else 1


def out_back(x, s=1.9):
    x = clamp(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def in_out(x):
    x = clamp(x); return 3 * x * x - 2 * x ** 3


def mix(c1, c2, a):
    return tuple(int(c1[i] * a + c2[i] * (1 - a)) for i in range(3))


# ---------- post FX ----------
_rng = np.random.default_rng(7)
_noise = (_rng.normal(0, 1, (H + 64, W + 64)) * 6).astype(np.float32)
_yy, _xx = np.mgrid[0:H, 0:W]
_vq = ((((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) ** 1.2).astype(np.float32)[..., None]


def camera(img, zoom=1.0, cx=W / 2, cy=H / 2, sx=0.0, sy=0.0):
    if zoom == 1.0 and not sx and not sy and cx == W / 2 and cy == H / 2:
        return img
    zoom = max(zoom, 1.0)
    cx = clamp(cx, W / (2 * zoom), W - W / (2 * zoom))
    cy = clamp(cy, H / (2 * zoom), H - H / (2 * zoom))
    a = 1.0 / zoom
    return img.transform((W, H), Image.AFFINE, (a, 0, cx + sx - W / (2 * zoom), 0, a, cy + sy - H / (2 * zoom)),
                         resample=Image.BILINEAR)


def post(img, frame, glitch=0.0, grain=1.0, vignette=0.28, fade=1.0):
    arr = np.asarray(img, dtype=np.float32)
    if glitch > 0.02:
        r = np.random.default_rng(frame + 99)
        sh = int(26 * glitch)
        arr[..., 0] = np.roll(arr[..., 0], sh, axis=1)
        arr[..., 2] = np.roll(arr[..., 2], -sh, axis=1)
        for _ in range(int(3 + 7 * glitch)):
            y0 = int(r.integers(0, H - 80)); hh = int(r.integers(14, 90))
            dx = int(r.integers(-90, 90) * glitch)
            arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], dx, axis=1)
    if vignette:
        arr *= 1 - vignette * _vq
    if grain:
        r = np.random.default_rng(frame)
        oy, ox = int(r.integers(0, 64)), int(r.integers(0, 64))
        arr += (_noise[oy:oy + H, ox:ox + W] * grain)[..., None]
    if fade < 1.0:
        arr *= fade
    return np.clip(arr, 0, 255).astype(np.uint8)


# ---------- audio ----------
rng = np.random.default_rng(3)


def _t(n):
    return np.arange(n) / SR


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, f1, f2, order=2):
    return signal.sosfilt(signal.butter(order, [f1, f2], "band", fs=SR, output="sos"), x)


def kick(g=1.0):
    n = int(0.42 * SR); t = _t(n)
    f = 46 + 120 * np.exp(-t / 0.04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15)
    s += 0.35 * hp(rng.normal(0, 1, n), 2500) * np.exp(-t / 0.006)
    return s * g


def clap(g=1.0):
    n = int(0.22 * SR); t = _t(n)
    nz = bp(rng.normal(0, 1, n), 900, 3800)
    e = np.exp(-t / 0.07) + 0.8 * np.exp(-((t - 0.012) % 0.02) / 0.004) * (t < 0.05)
    return nz * e * 0.9 * g


def hat(g=1.0, open_=False):
    n = int((0.16 if open_ else 0.05) * SR); t = _t(n)
    return hp(rng.normal(0, 1, n), 7000) * np.exp(-t / (0.06 if open_ else 0.014)) * 0.5 * g


def pop(g=1.0, f0=520, f1=1250):
    n = int(0.14 * SR); t = _t(n)
    f = f0 + (f1 - f0) * np.minimum(t / 0.07, 1)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03)) * 0.6 * g


def tick(g=1.0):
    n = int(0.05 * SR); t = _t(n)
    return (bp(rng.normal(0, 1, n), 2500, 6000) * np.exp(-t / 0.006) * 0.7 + np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.012) * 0.5) * g


def buzz(dur=0.25, g=1.0):
    n = int(dur * SR); t = _t(n)
    s = lp(np.sign(np.sin(2 * np.pi * 88 * t)) * 0.7 + 0.3 * np.sin(2 * np.pi * 176 * t), 700)
    return s * np.minimum(t / 0.01, 1) * np.minimum((dur - t) / 0.02, 1) * (0.7 + 0.3 * np.sign(np.sin(2 * np.pi * 38 * t))) * g


def heartbeat(g=1.0):
    n = int(0.45 * SR); t = _t(n)
    s = np.sin(2 * np.pi * 58 * t) * np.exp(-t / 0.09)
    t2 = np.clip(t - 0.17, 0, None)
    s += 0.7 * np.sin(2 * np.pi * 52 * t2) * np.exp(-t2 / 0.09) * (t > 0.17)
    return s * g


def whoosh(dur=0.7, g=1.0, up=True):
    n = int(dur * SR); t = _t(n)
    nz = hp(rng.normal(0, 1, n), 900)
    e = (t / dur) ** 2.2 if up else (1 - t / dur) ** 2.2
    s = nz * e
    return s * 0.55 * g


def riser(dur, g=1.0):
    n = int(dur * SR); t = _t(n)
    f = 220 * (8 ** (t / dur))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / dur) ** 1.6 * 0.35
    nz = hp(rng.normal(0, 1, n), 1500) * (t / dur) ** 2.4 * 0.5
    return (s + nz) * g


def boom(g=1.0):
    n = int(1.4 * SR); t = _t(n)
    s = np.sin(2 * np.pi * 42 * t * (1 + 0.5 * np.exp(-t / 0.1))) * np.exp(-t / 0.5)
    s += 0.5 * lp(rng.normal(0, 1, n), 400) * np.exp(-t / 0.35)
    s += 0.25 * hp(rng.normal(0, 1, n), 3000) * np.exp(-t / 0.25)
    return s * g


def bass(freq, dur=0.22, g=1.0):
    n = int(dur * SR); t = _t(n)
    saw = 2 * ((t * freq) % 1) - 1
    s = lp(saw, 260) * 1.8 + np.sin(2 * np.pi * freq * t)
    return s * np.minimum(t / 0.004, 1) * np.exp(-t / (dur * 0.9)) * 0.55 * g


def pluck(freq, g=1.0):
    n = int(0.3 * SR); t = _t(n)
    s = 2 * ((t * freq) % 1) - 1
    s = lp(s, 2600) * np.exp(-t / 0.1)
    return s * 0.35 * g


def stab(freqs, g=1.0, dur=0.7):
    n = int(dur * SR); t = _t(n)
    s = sum(2 * ((t * f) % 1) - 1 for f in freqs) / len(freqs)
    return lp(s, 3200) * np.exp(-t / 0.28) * 0.7 * g


def drone(dur, f=55.0, g=1.0):
    n = int(dur * SR); t = _t(n)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.003 * t) + 0.25 * np.sin(2 * np.pi * f * 3 * t)
    return s * (0.3 + 0.7 * t / dur) * g * 0.5


class Mix:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.buf = np.zeros(self.n, dtype=np.float64)

    def add(self, t, sig, g=1.0):
        i = int(round(t * SR))
        if i >= self.n or i + len(sig) <= 0:
            return
        j = min(self.n, i + len(sig))
        self.buf[i:j] += sig[: j - i] * g

    def duck(self, t0, t1, ramp=0.006):
        e = np.ones(self.n)
        a, b = int(t0 * SR), int(t1 * SR)
        r = int(ramp * SR)
        e[a:b] = 0
        e[a - r:a] = np.linspace(1, 0, r)
        e[b:b + r] = np.linspace(0, 1, r)
        return e

    def master(self, fade_out=0.2, ducks=()):
        x = self.buf.copy()
        for d0, d1 in ducks:
            x *= self.duck(d0, d1)
        x = hp(x, 28)
        x = np.tanh(x * 1.25) / np.tanh(1.25)
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.72
        n = int(fade_out * SR)
        x[-n:] *= np.linspace(1, 0, n)
        return x


def write_wav(path, x):
    import wave
    st = np.stack([x, x], 1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


# ---------- encode ----------
def render(frame_fn, nframes, wav, out, procs=None):
    """frame_fn(i) -> HxWx3 uint8. Frames rendered in parallel, piped to ffmpeg with the wav track."""
    import multiprocessing as mp
    procs = procs or max(1, min(8, os.cpu_count() or 2))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-maxrate", "12M", "-bufsize", "24M", "-r", str(FPS),
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
           "-shortest", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.get_context("fork").Pool(procs) as pool:
        for k, arr in enumerate(pool.imap(frame_fn, range(nframes), chunksize=4)):
            p.stdin.write(arr.tobytes())
    p.stdin.close(); p.wait()
