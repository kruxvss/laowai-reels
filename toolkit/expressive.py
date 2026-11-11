# Expressive Kokoro pass: each line its own speed and pitch, placed on the reference line slots; a reaction voice + bleep.
import json, os, tempfile, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro, EspeakConfig
import espeakng_loader
data = os.path.join(tempfile.gettempdir(), "kokoro-espeak-ng-data")
if not os.path.exists(os.path.join(data, "phontab")): data = espeakng_loader.get_data_path()
M = "/root/claude-animation-skills/kit/models/"
k = Kokoro(M + "kokoro-v1.0.onnx", M + "voices-v1.0.bin", espeak_config=EspeakConfig(lib_path=espeakng_loader.get_library_path(), data_path=data))
SR = 24000; TMP = "/tmp/claude-0/-home-claude/65f3343c-f749-5619-96c5-39fd1bc2a775/scratchpad/"
ref = json.load(open("audio/lines_ref.json")); plan = json.load(open("expr_plan.json"))
def gen(text, voice, speed, semis):
    s, sr = k.create(text, voice=voice, speed=speed, lang="en-us"); a = np.abs(s); i = np.where(a > 0.01)[0]; s = s[max(0, i[0] - 480): i[-1] + 1200]
    if semis:
        sf.write(TMP + "p_in.wav", s, sr); r = 2 ** (semis / 12)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TMP + "p_in.wav", "-af", f"asetrate={int(sr * r)},aresample={sr},atempo={1 / r:.5f}", TMP + "p_out.wav"], check=True)
        s, _ = sf.read(TMP + "p_out.wav")
    return s
def fit(s, slot):
    if len(s) / SR <= slot: return s, 1.0
    ratio = len(s) / SR / slot; sf.write(TMP + "f_in.wav", s, SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", TMP + "f_in.wav", "-af", f"atempo={ratio:.4f}", TMP + "f_out.wav"], check=True)
    return sf.read(TMP + "f_out.wav")[0], ratio
total = ref[-1]["start"] + ref[-1]["dur"] + 0.8; out = np.zeros(int(total * SR) + SR); meta = []
for i, (r, p) in enumerate(zip(ref, plan["lines"])):
    s = gen(p["text"], plan["voice"], p["speed"], p.get("semis", 0))
    st = p.get("start", r["start"])
    slot = p.get("slot") or ((ref[i + 1]["start"] - st - 0.06) if i + 1 < len(ref) else r["dur"] + 0.6)
    s, ratio = fit(s, slot); a = int(st * SR); out[a:a + len(s)] += s * p.get("gain", 1.0)
    meta.append({"i": i, "start": st, "dur": round(len(s) / SR, 3), "tempo": round(ratio, 3)})
for x in plan.get("reactions", []):
    s = gen(x["text"], x["voice"], x["speed"], x.get("semis", 0)); a = int(x["at"] * SR); out[a:a + len(s)] += s * x.get("gain", 1.0)
    if x.get("bleep"):
        # the censored word is never spoken: a 1 kHz bleep follows "what the"
        d = x["bleep"]; n = int(d * SR); tt = np.arange(n) / SR; e = np.minimum(1, np.minimum(tt / 0.01, (d - tt) / 0.01))
        i0 = a + len(s) + int(0.02 * SR); out[i0:i0 + n] += 0.3 * np.sin(2 * np.pi * 1000 * tt) * e
        x["bleep_at"] = round(i0 / SR, 3)
    meta.append({"reaction": x["text"], "start": x["at"], "dur": round(len(s) / SR, 3), "bleep_at": x.get("bleep_at")}); print(meta[-1])
sf.write("audio/vo.wav", out[: int(total * SR)], SR); json.dump([m for m in meta if "i" in m], open("audio/lines.json", "w"), indent=1)
print([m.get("tempo") for m in meta])
