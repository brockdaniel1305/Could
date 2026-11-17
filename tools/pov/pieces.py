"""Cut a TTS take at every silence (>= 0.12 s below -40 dB) into numbered pieces and transcribe each one, so dialogue lines can be
assembled reliably (whisper's word times on a whole take drift). usage: pieces.py <take.mp3>  -> prints  index start end text
Then: pieces.py <take.mp3> --make <out.wav> i0 i1   (pieces i0..i1 joined, trimmed, faded, -24 LUFS)"""
import json, re, subprocess, sys
from pathlib import Path

take = Path(sys.argv[1]).resolve()
r = subprocess.run(["ffmpeg", "-i", str(take), "-af", "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(take)], capture_output=True, text=True).stdout)
edges = [0.0] + [(a + b) / 2 for a, b in zip(st, en) if 0.05 < (a + b) / 2 < dur - 0.05] + [dur]
F = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,afade=t=in:d=0.04,areverse,afade=t=in:d=0.02"
if "--make" in sys.argv:
    k = sys.argv.index("--make"); out, i0, i1 = sys.argv[k + 1], int(sys.argv[k + 2]), int(sys.argv[k + 3])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(take), "-ss", f"{edges[i0]:.3f}", "-to", f"{edges[i1 + 1]:.3f}",
                    "-af", F + ",loudnorm=I=-24:TP=-2:LRA=11", "-ar", "44100", "-ac", "1", out], check=True)
    sys.exit(0)
tmp = take.parent / f".pc_{take.stem}"; tmp.mkdir(exist_ok=True)
for i in range(len(edges) - 1):
    f = tmp / f"p{i:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(take), "-ss", f"{edges[i]:.3f}", "-to", f"{edges[i + 1]:.3f}", "-ar", "16000", "-ac", "1", str(f)])
    subprocess.run(["npx", "--yes", "hyperframes", "transcribe", str(f), "--model", "small.en", "--json"], capture_output=True, cwd=tmp)
    t = tmp / "transcript.json"
    txt = " ".join(w.get("text", "") for w in (lambda d: d if isinstance(d, list) else d.get("words", []))(json.loads(t.read_text()))) if t.exists() else ""
    if t.exists(): t.unlink()
    print(f"{i:2d} {edges[i]:6.2f}-{edges[i + 1]:6.2f}  {txt}")
