#!/usr/bin/env python3
"""Level every narrator segment of an episode to the same loudness (default -24 LUFS), so a long ElevenLabs take that drifts
quieter (or a re-recorded line) does not sound like a different speaker.

    python3 tools/norm_segments.py episodes/<ep> [-24]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
target = float(sys.argv[2]) if len(sys.argv) > 2 else -24.0
d = ep / "assets/voice/el"
for name in json.loads((d / "segments.json").read_text()):
    f = d / name
    out = subprocess.run(["ffmpeg", "-nostdin", "-i", str(f), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    if not m:
        continue
    gain = target - float(m[-1])
    if abs(gain) < 0.5:
        continue
    tmp = f.with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(f), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.95", str(tmp)], check=True)
    tmp.replace(f)
    print(f"{name}: {float(m[-1]):6.1f} LUFS -> {target} ({gain:+.1f} dB)")
