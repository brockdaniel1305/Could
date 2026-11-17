"""Prepare a POV episode: per dialogue line, word timings (whisper) and a 30 fps loudness envelope (drives the lip sync).
Writes <ep>/pov_timing.json. usage: prep.py episodes/<ep>"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

ep = Path(sys.argv[1]).resolve(); cfg = json.loads((ep / "pov.json").read_text())
cache = ep / "assets/voice/.words"; cache.mkdir(exist_ok=True)
out = {"lines": []}
for name, who, t0 in cfg["lines"]:
    wav = ep / f"assets/voice/{name}.wav"
    cj = cache / f"{name}.json"
    if not cj.exists():
        subprocess.run(["npx", "--yes", "hyperframes", "transcribe", str(wav), "--model", "small.en", "--json"], cwd=cache, capture_output=True)
        (wav.parent / "transcript.json").rename(cj)
    d = json.loads(cj.read_text()); ws = d if isinstance(d, list) else d["words"]
    with wave.open(str(wav)) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = sr // 30
    env = [float(np.sqrt(np.mean(x[i:i + hop] ** 2))) for i in range(0, len(x), hop)]
    m = max(env) or 1
    out["lines"].append({"id": name, "who": who, "t0": t0, "dur": len(x) / sr,
                         "words": [[w.get("text", w.get("word", "")).strip(), round(t0 + w["start"], 3), round(t0 + w["end"], 3)] for w in ws],
                         "env": [round(min(1, e / m * 1.3), 2) for e in env]})
(ep / "pov_timing.json").write_text(json.dumps(out))
for l in out["lines"]: print(f'{l["t0"]:6.2f}-{l["t0"] + l["dur"]:6.2f} {l["who"]:8s} ' + " ".join(w[0] for w in l["words"]))
