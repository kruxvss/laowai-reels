"""Silence-based alignment: compress pauses, map punctuation phrases to the largest gaps, distribute words by length.
usage: python3 align.py VO_DIR reel_module"""
import sys, json, wave, re, importlib
import numpy as np
sys.path.insert(0, "/home/claude/reels")
D = sys.argv[1]; mod = importlib.import_module(sys.argv[2])
w = wave.open(D + "/vo_raw.wav"); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = int(sr * 0.01); n = len(x) // hop
rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, 1)); thr = max(0.004, 0.04 * rms.max())
v = rms > thr
segs = []; i = 0
while i < n:
    if v[i]:
        j = i
        while j < n and (v[j] or (j + 16 < n and v[j:j + 16].any())): j += 1
        segs.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
# phrases
words = []; phrases = []
for li, (_, _, txt) in enumerate(mod.LINES):
    for ph in re.split(r"(?<=[.,?!])\s+", txt):
        ws = ph.split()
        if ws: phrases.append((li, ws))
P = len(phrases)
# DP: split the segment list into P contiguous groups matching expected phrase durations
S = len(segs); chars = [sum(len(w) + 1 for w in ws) for _, ws in phrases]; Ctot = sum(chars)
voiced = sum(b - a for a, b in segs); exp = [voiced * c / Ctot for c in chars]
def gdur(i, j): return sum(segs[k][1] - segs[k][0] for k in range(i, j))
def gapb(k): return segs[k][0] - segs[k - 1][1] if k > 0 else 1.0
INF = 1e9; dp = [[INF] * (S + 1) for _ in range(P + 1)]; bk = [[0] * (S + 1) for _ in range(P + 1)]; dp[0][0] = 0
for p in range(1, P + 1):
    for j in range(p, S + 1):
        for i in range(p - 1, j):
            if dp[p - 1][i] >= INF: continue
            c = dp[p - 1][i] + ((gdur(i, j) - exp[p - 1]) / max(0.4, exp[p - 1])) ** 2 - 2.0 * min(0.6, gapb(i)) * (p > 1)
            if c < dp[p][j]: dp[p][j] = c; bk[p][j] = i
if S < P: raise SystemExit("fewer segments than phrases")
groups = []; j = S
for p in range(P, 0, -1):
    i = bk[p][j]; groups.insert(0, segs[i:j]); j = i
print("segments", len(segs), "phrases", P, "groups", len(groups))
# rebuild audio with compressed gaps
out = []; t = 0.0; newt = []; GAP_IN, GAP_PH, GAP_LINE = 0.10, 0.16, 0.24
prev_line = None
for gi, (g, (li, ws)) in enumerate(zip(groups, phrases)):
    if gi: t += GAP_LINE if li != prev_line else GAP_PH; out.append(np.zeros(int((GAP_LINE if li != prev_line else GAP_PH) * sr), np.float32))
    spans = []
    for si, (a, b) in enumerate(g):
        if si: out.append(np.zeros(int(GAP_IN * sr), np.float32)); t += GAP_IN
        a2, b2 = max(0, a - 0.03), b + 0.05
        seg = x[int(a2 * sr):int(b2 * sr)]; spans.append((t, t + len(seg) / sr)); out.append(seg); t += len(seg) / sr
    # words by char length across voiced spans
    tot_v = sum(b - a for a, b in spans); chars = [len(wd) + 1 for wd in ws]; C = sum(chars); acc = 0
    def at(f):
        rem = f * tot_v
        for a, b in spans:
            if rem <= b - a: return a + rem
            rem -= b - a
        return spans[-1][1]
    for wd, c in zip(ws, chars):
        words.append([wd, round(at(acc / C), 3), round(at((acc + c) / C) - 0.02, 3), li]); acc += c
    prev_line = li
y = np.concatenate([np.zeros(int(0.15 * sr), np.float32)] + out)
for wd in words: wd[1] += 0.15; wd[2] += 0.15
pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
o = wave.open(D + "/vo_n.wav", "wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(pcm.tobytes()); o.close()
json.dump(words, open(D + "/words.json", "w"))
print("dur", round(len(y) / sr, 2), "words", len(words))
