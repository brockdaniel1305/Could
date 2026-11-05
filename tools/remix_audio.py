#!/usr/bin/env python3
"""Re-mix only the audio of a rendered episode from its index.html clips (voice + sfx + music) and swap it into the MP4.

    python3 tools/remix_audio.py episodes/<ep> <rendered.mp4> <out-final.mp4>

For sound-only changes (e.g. thinner SFX): the picture is copied, the new mix is loudness-normalised (-15 LUFS, TP -1.5).
"""
import re
import subprocess
import sys
from pathlib import Path

ep, src, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]   # add --duck to sidechain the music under the voice
html = (ep / "index.html").read_text()
clips = []
for tag in re.findall(r"<audio\b[^>]*>", html):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
    clips.append((ep / a["src"], float(a.get("data-start", 0)), float(a.get("data-duration", 0)), float(a.get("data-volume", 1))))
args, chains = ["ffmpeg", "-y", "-loglevel", "error", "-i", src], []
for i, (f, start, dur, vol) in enumerate(clips, start=1):
    args += ["-i", str(f)]
    ms = int(round(start * 1000))
    chains.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={vol},adelay={ms}|{ms}[a{i}]")
music = [i for i, c in enumerate(clips, start=1) if "/music/" in str(c[0])]
rest = [i for i in range(1, len(clips) + 1) if i not in music]
if music and "--duck" in sys.argv:
    # the music dips under the narrator (sidechain) so it can be livelier without masking the voice
    m = music[0]
    flt = (";".join(chains) + f";{''.join(f'[a{i}]' for i in rest)}amix=inputs={len(rest)}:normalize=0:dropout_transition=0,asplit=2[fg][sc]"
           f";[a{m}][sc]sidechaincompress=threshold=0.05:ratio=2.5:attack=120:release=1500:makeup=1[mu]"
           f";[fg][mu]amix=inputs=2:normalize=0:dropout_transition=0,apad[out]")
else:
    mix = "".join(f"[a{i}]" for i in range(1, len(clips) + 1))
    flt = ";".join(chains) + f";{mix}amix=inputs={len(clips)}:normalize=0:dropout_transition=0,apad[out]"
args += ["-filter_complex", flt, "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
# static loudness: mix first, measure, then ONE fixed gain + limiter (single-pass loudnorm is dynamic and lifts the music in
# every speech pause after a few seconds)
mixed = Path(out).with_suffix(".mix.mp4")
args[-1] = str(mixed)
subprocess.run(args, check=True)
meas = subprocess.run(["ffmpeg", "-nostdin", "-i", str(mixed), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", meas)[-1])
gain = -15.0 - I
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mixed), "-map", "0:v", "-map", "0:a", "-c:v", "copy",
                "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
mixed.unlink()
print(f"mix {I:.1f} LUFS -> gain {gain:+.1f} dB")
print(out, len(clips), "clips")
