"""Split one TTS take per speaker into single dialogue lines.
usage: split_lines.py <raw.wav> <words.json> <out_dir> name:firstWord,lastWord ...  (word indices into the whisper transcript)
Each cut sits at the quietest 20 ms between the two lines; lines are trimmed, faded and levelled to -24 LUFS."""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

raw, words, out = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
ws = words if isinstance(words, list) else words["words"]
with wave.open(str(raw)) as w:
    sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
win = int(0.02 * sr)
rms = np.sqrt(np.convolve(x * x, np.ones(win) / win, "same"))

# silent stretches (rms < -40 dBFS for >= 80 ms); a cut goes into the middle of the silence nearest the line boundary
lo = rms < 10 ** (-40 / 20)
sil, i = [], 0
while i < len(lo):
    if lo[i]:
        j = i
        while j < len(lo) and lo[j]: j += 1
        if (j - i) / sr >= 0.08: sil.append(((i + j) / 2 / sr, (j - i) / sr))
        i = j
    else: i += 1

def quiet(a, b):
    m = (a + b) / 2
    c = [s for s in sil if a - 0.3 <= s[0] <= b + 0.3]
    if c: return min(c, key=lambda s: abs(s[0] - m) - s[1] * 0.5)[0]
    a, b = int(max(0, a) * sr), int(min(len(x) / sr, b) * sr)
    return (a + int(np.argmin(rms[a:b]))) / sr if b > a else a / sr

specs = [(s.split(":")[0], *map(int, s.split(":")[1].split(","))) for s in sys.argv[4:]]
bounds = []
for k, (name, i0, i1) in enumerate(specs):
    st = 0.0 if i0 == 0 else quiet(ws[i0 - 1]["end"] - 0.25, ws[i0]["start"] + 0.12)
    en = len(x) / sr if i1 == len(ws) - 1 else quiet(ws[i1]["end"] - 0.12, ws[i1 + 1]["start"] + 0.25)
    bounds.append((name, st, en))
out.mkdir(parents=True, exist_ok=True)
for name, st, en in bounds:
    f = out / f"{name}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw).replace(".wav", ".mp3"), "-ss", f"{st:.3f}", "-to", f"{en:.3f}",
                    "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,"
                           "afade=t=in:d=0.04,areverse,afade=t=in:d=0.02,loudnorm=I=-24:TP=-2:LRA=11",
                    "-ar", "44100", "-ac", "1", str(f)], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)
    print(f"{name}: {st:.2f}-{en:.2f} -> {d:.2f}s")
