#!/usr/bin/env python3
"""Cut one long narrator take (e.g. ElevenLabs, generated in a single call to save credits) into the script's segments.

    python3 tools/split_master.py episodes/<ep> <take.mp3>

Segments = every scene's text split at ||pause|| markers (same as build_episode.py). The take is transcribed with whisper,
each segment's words are found in order, and the audio from its first to last word is written to
<ep>/assets/voice/el/segNN.wav. narration.json then uses "provider": "prerecorded" and build_episode.py picks the files
up in order instead of calling a TTS engine; our own ||pauses|| still decide the gaps.
"""
import difflib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("be", ROOT / "tools/build_episode.py")
be = importlib.util.module_from_spec(spec)
spec.loader.exec_module(be)

ep, take = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out = ep / "assets/voice/el"
out.mkdir(parents=True, exist_ok=True)
cfg = json.loads((ep / "narration.json").read_text())
segs = []
for sc in cfg["scenes"]:
    parts = be.PAUSE.split(sc["text"])
    for i in range(0, len(parts), 2):
        u, _ = be.parse(parts[i])
        segs.append([be.norm(w) for x in u for w in x["shown"].split() if be.norm(w)])

wav = out / "take.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(take), "-ac", "1", "-ar", "24000", "-sample_fmt", "s16", str(wav)], check=True)
# speech chunks between pauses in the take
sd = subprocess.run(["ffmpeg", "-nostdin", "-i", str(wav), "-af", "silencedetect=n=-38dB:d=0.32", "-f", "null", "-"], capture_output=True, text=True).stderr
import re
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", sd)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", sd)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout)
edges = [0.0] + [x for pair in zip(st, en) for x in pair] + [dur]
chunks = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2) if edges[i + 1] - edges[i] > 0.08]
# transcribe every chunk on its own, then assign chunks to segments in order by text similarity (dynamic programming)
NUM = {"0": "nil", "1": "one", "2": "two", "11": "eleven", "70": "seventy", "90": "ninety", "92": "ninetytwo", "28": "twentyeight", "twentyeight": "twentyeight", "195": "oneninetyfive",
       "1m": "onemetre"}
def toks(text):
    out = []
    for t in text.split():
        n = be.norm(t)
        out.append(NUM.get(n, n))
    return "".join(out)
heard = []
for a, b in chunks:
    f = out / "chunk.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ss", f"{max(0, a - 0.12):.3f}", "-to", f"{b + 0.12:.3f}", str(f)], check=True)
    r = subprocess.run(["npx", "--yes", "hyperframes", "transcribe", str(f), "--model", "small.en", "--json"], capture_output=True, text=True, cwd=out)
    words = []
    for line in (r.stdout + "\n" + r.stderr).splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "words":
            words += ev["words"]
    heard.append(toks(" ".join(w["text"] for w in words)))
(out / "chunk.wav").unlink(missing_ok=True)
(out / "transcript.json").unlink(missing_ok=True)
want = ["".join(sgm) for sgm in segs]
N, M = len(segs), len(chunks)
if M < N:
    # fast talkers barely pause: cut at word starts from one transcript of the whole take instead
    print(f"only {M} speech chunks for {N} segments - cutting at word starts", flush=True)
    r = subprocess.run(["npx", "--yes", "hyperframes", "transcribe", str(wav), "--model", "small.en", "--json"], capture_output=True, text=True, cwd=out)
    words = []
    for line in (r.stdout + "\n" + r.stderr).splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "words":
            words += ev["words"]
    (out / "transcript.json").unlink(missing_ok=True)
    heardw = [toks(w["text"]) for w in words]
    flat = [(k, w) for k, sgm in enumerate(segs) for w in sgm]
    first = {}
    sm = difflib.SequenceMatcher(None, [w for _, w in flat], heardw, autojunk=False)
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            k = flat[blk.a + j][0]
            if k not in first:
                first[k] = (blk.a + j, words[blk.b + j]["start"])
    # a segment whose first word was not matched: take its first matched word minus the words before it (~0.3 s each)
    starts = []
    for k in range(N):
        if k in first:
            idx, t = first[k]
            lead = idx - next(i for i, (kk, _) in enumerate(flat) if kk == k)
            starts.append(t - 0.3 * lead)
        else:
            starts.append(None)
    for k in range(N):
        if starts[k] is None:
            prv = next((starts[j] for j in range(k - 1, -1, -1) if starts[j] is not None), 0.0)
            nxt = next((starts[j] for j in range(k + 1, N) if starts[j] is not None), dur)
            starts[k] = (prv + nxt) / 2
            print(f"  seg {k:02d} start interpolated", flush=True)
    starts = [max(0.0, min(dur, x)) for x in starts]
    starts[0] = 0.0
    bounds = [(starts[k] - (0.04 if k else 0), (starts[k + 1] - 0.03) if k + 1 < N else dur) for k in range(N)]
    for k in range(N):
        print(f"  seg {k:02d}: {bounds[k][0]:6.2f}-{bounds[k][1]:6.2f} {want[k]!r}" if False else f"  seg {k:02d}: {bounds[k][0]:6.2f}-{bounds[k][1]:6.2f}")
    M = 0
if M:
    INF = float("inf")

    best = [[INF] * (M + 1) for _ in range(N + 1)]
    back = [[0] * (M + 1) for _ in range(N + 1)]
    best[0][0] = 0.0
    for k in range(1, N + 1):
        for m in range(k, M - (N - k) + 1):
            for p in range(max(k - 1, m - 4), m):
                if best[k - 1][p] == INF:
                    continue
                got = "".join(heard[p:m])
                cost = best[k - 1][p] + (1 - difflib.SequenceMatcher(None, got, want[k - 1]).ratio()) * max(len(got), len(want[k - 1]))
                if cost < best[k][m]:
                    best[k][m], back[k][m] = cost, p
    bounds, m = [], M
    for k in range(N, 0, -1):
        p = back[k][m]
        bounds.append((chunks[p][0], chunks[m - 1][1]))
        print(f"  seg {k - 1:02d}: {want[k - 1]!r} <- {''.join(heard[p:m])!r}")
        m = p
    bounds.reverse()
files = []
for k, (a, b) in enumerate(bounds):
    lo = max(0.0, a - 0.06) if k == 0 else max(bounds[k - 1][1] + 0.02, a - 0.06)
    hi = b + 0.12 if k == len(segs) - 1 else min(bounds[k + 1][0] - 0.02, b + 0.12)
    f = out / f"seg{k:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ss", f"{lo:.3f}", "-to", f"{hi:.3f}",
                    "-af", "afade=t=in:d=0.01,areverse,afade=t=in:d=0.03,areverse", str(f)], check=True)
    files.append(f.name)
(out / "segments.json").write_text(json.dumps(files, indent=1))
print(f"{len(files)} segments written to {out}")
