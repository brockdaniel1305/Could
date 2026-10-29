#!/usr/bin/env python3
"""Synthesize the COULD? cartoon sound-effect library into channel/kit/sfx/ (WAV, 44.1 kHz mono) + manifest.json.

Procedural, licence-free (no downloads: Openverse is not reachable from the cloud sandbox). Every effect has its
peak in the first ~0.1 s unless noted, so a cue lands on the picture. Rebuild with:  python3 tools/make_sfx.py
"""
import json
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "channel/kit/sfx"
rng = np.random.default_rng(7)


def t(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.005, r=0.2, shape=4.0):
    """Attack/exponential release envelope over n samples."""
    x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) * shape / max(r, 1e-3))
    return e


def band(x, lo, hi):
    """FFT band-pass (cheap, fine for effects)."""
    f = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def sweep(f0, f1, d, curve=1.0):
    tt = t(d)
    f = f0 + (f1 - f0) * (tt / d) ** curve
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def noise(d):
    return rng.standard_normal(int(SR * d))


def mix(d, *parts):
    out = np.zeros(int(SR * d))
    for at, sig in parts:
        i = int(at * SR)
        n = min(len(sig), len(out) - i)
        if n > 0:
            out[i:i + n] += sig[:n]
    return out


def stomp():
    d = 0.6
    body = sweep(110, 45, d, 0.4) * env(int(SR * d), 0.003, 0.18, 5)
    grit = band(noise(d), 80, 900) * env(int(SR * d), 0.002, 0.06, 6) * 0.6
    return body + grit


def boing():
    d = 0.7
    tt = t(d)
    f = 220 + 160 * np.sin(2 * np.pi * 9 * tt) * np.exp(-tt * 3) + 60 * tt
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.004, 0.5, 4)


def dizzy():
    d = 0.9
    tt = t(d)
    f = 1500 * np.exp(-tt * 1.6) + 350 + 40 * np.sin(2 * np.pi * 7 * tt)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (s + 0.3 * np.sin(2 * 2 * np.pi * np.cumsum(f) / SR)) * env(len(tt), 0.01, 0.8, 3)


def tweet():
    d = 1.1
    parts = []
    for k in range(5):
        c = sweep(2600 + 300 * (k % 2), 4200, 0.07, 0.6) * env(int(SR * 0.07), 0.002, 0.06, 3)
        parts.append((0.04 + k * 0.2 + (0.05 if k % 2 else 0), c * 0.6))
    return mix(d, *parts)


def kick():
    d = 0.35
    thump = sweep(160, 50, d, 0.3) * env(int(SR * d), 0.001, 0.12, 6)
    click = band(noise(d), 1500, 6000) * env(int(SR * d), 0.0005, 0.01, 8) * 0.5
    return thump + click


def whistle():
    d = 0.8
    tt = t(d)
    trill = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 28 * tt))
    s = np.sin(2 * np.pi * 2900 * tt) + 0.2 * np.sin(2 * np.pi * 5800 * tt)
    e = np.minimum(1, tt / 0.02) * np.minimum(1, (d - tt) / 0.08)
    return s * trill * e * 0.7 + band(noise(d), 2500, 4000) * e * 0.15


def wind():
    d = 4.0
    tt = t(d)
    n = band(noise(d), 200, 1200)
    swell = 0.35 + 0.65 * np.sin(np.pi * tt / d) ** 2 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * tt))
    howl = sweep(380, 520, d, 1) * 0.08 * np.sin(np.pi * tt / d)
    return n * swell / np.abs(n).max() + howl


def domino():
    d = 2.6
    parts, at, gap = [], 0.0, 0.16
    while at < d - 0.1:
        c = band(noise(0.05), 800, 5000) * env(int(SR * 0.05), 0.0005, 0.02, 6)
        tone = np.sin(2 * np.pi * rng.uniform(900, 1400) * t(0.05)) * env(int(SR * 0.05), 0.0005, 0.03, 6) * 0.5
        parts.append((at, (c + tone) * rng.uniform(0.6, 1.0)))
        at += gap
        gap = max(0.035, gap * 0.9)
    return mix(d, *parts)


def tick():
    d = 0.08
    return (np.sin(2 * np.pi * 2200 * t(d)) + band(noise(d), 3000, 8000) * 0.5) * env(int(SR * d), 0.0005, 0.02, 6)


def drumroll():
    d = 2.5
    tt = t(d)
    roll = band(noise(d), 150, 6000) * (0.55 + 0.45 * np.sin(2 * np.pi * 22 * tt) ** 2)
    cres = (tt / d) ** 1.5
    return roll * (0.2 + 0.8 * cres)


def heartbeat():
    d = 1.0
    beat = lambda: sweep(70, 40, 0.18, 0.5) * env(int(SR * 0.18), 0.004, 0.08, 4)
    return mix(d, (0.0, beat()), (0.22, beat() * 0.7))


def clang():
    d = 1.0
    tt = t(d)
    s = sum(a * np.sin(2 * np.pi * f * tt) for f, a in [(520, 1), (1310, 0.6), (2240, 0.4), (3170, 0.25)])
    return s * env(len(tt), 0.001, 0.5, 4) + band(noise(d), 2000, 8000) * env(len(tt), 0.0005, 0.03, 6) * 0.4


def sting():
    """Dun, dun, duuun (dramatic). Peaks at 0.0, 0.32 and 0.66 s."""
    def brass(f, d):
        tt = t(d)
        saw = sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 9))
        return saw * env(len(tt), 0.01, d * 0.8, 2.5)
    return mix(2.4, (0.0, brass(110, 0.3)), (0.32, brass(104, 0.3)), (0.66, brass(92.5, 1.7)))


def rumble():
    d = 2.2
    tt = t(d)
    return band(noise(d), 30, 260) * np.minimum(1, tt / 0.3) * np.minimum(1, (d - tt) / 0.6)


def net():
    d = 0.45
    return band(noise(d), 1500, 9000) * env(int(SR * d), 0.004, 0.25, 4)


def ding():
    d = 1.2
    tt = t(d)
    return sum(a * np.sin(2 * np.pi * f * tt) for f, a in [(1760, 1), (3520, 0.35), (5280, 0.15)]) * env(len(tt), 0.001, 0.8, 4)


def gulp():
    d = 0.25
    return sweep(180, 640, d, 0.7) * env(int(SR * d), 0.01, 0.15, 4)


def roar():
    """Distant crowd roar (layered band noise with drifting loudness), 3 s, swells in over 0.4 s."""
    d = 3.0
    tt = t(d)
    s = np.zeros(len(tt))
    for lo in (300, 500, 800, 1200, 1800):
        drift = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(0.3, 1.2) * tt + rng.uniform(0, 6))
        s += band(noise(d), lo, lo * 1.6) * drift
    return s * np.minimum(1, tt / 0.4) * np.minimum(1, (d - tt) / 1.0)


def swoosh():
    d = 0.5
    tt = t(d)
    n = noise(d)
    # rising then falling band, like air past the ear
    out = np.zeros(len(n))
    for i, c in enumerate((600, 1200, 2400)):
        out += band(n, c * 0.7, c * 1.3) * np.exp(-((tt - 0.18 - i * 0.03) / 0.09) ** 2)
    return out


def spin():
    """Whirl for a Roman spinning on the spot: fast tremolo whoosh, 0.8 s."""
    d = 0.8
    tt = t(d)
    return band(noise(d), 500, 3000) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * tt)) * env(len(tt), 0.02, 0.6, 3)


def rustle():
    d = 1.6
    tt = t(d)
    return band(noise(d), 1500, 7000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 3 * tt))) * np.sin(np.pi * tt / d)


SOUNDS = {
    "stomp": (stomp, "Army foot stamp: low thud + grit. Peak at 0 s."),
    "boing": (boing, "Cartoon spring boing (bounce, comic surprise)."),
    "dizzy": (dizzy, "Slide whistle down: someone gets dizzy / falls."),
    "tweet": (tweet, "Cartoon birds circling a dizzy head (1.1 s)."),
    "kick": (kick, "Ball kick: short thump + click."),
    "whistle": (whistle, "Referee pea whistle, 0.8 s."),
    "wind": (wind, "Western standoff wind, 4 s, swells in the middle."),
    "domino": (domino, "Domino chain falling, accelerating clicks, 2.6 s."),
    "tick": (tick, "Short counter tick."),
    "drumroll": (drumroll, "Snare roll with crescendo, 2.5 s (peak at the end)."),
    "heartbeat": (heartbeat, "Tension heartbeat (two thumps)."),
    "clang": (clang, "Metal shield clang."),
    "sting": (sting, "Dramatic dun-dun-duuun, hits at 0 / 0.32 / 0.66 s."),
    "rumble": (rumble, "Low ground rumble, 2.2 s (something rises)."),
    "net": (net, "Ball hits the net (swish)."),
    "ding": (ding, "Bright ding (trophy / gold ball lands)."),
    "gulp": (gulp, "Nervous gulp."),
    "roar": (roar, "Distant crowd roar, 3 s."),
    "swoosh": (swoosh, "Soft air swoosh for flying cards (peak 0.18 s)."),
    "spin": (spin, "Whirl of someone spinning on the spot, 0.8 s."),
    "rustle": (rustle, "Tumbleweed rustle, 1.6 s."),
}


def write(name, sig):
    sig = sig / max(1e-9, np.abs(sig).max()) * 0.84  # ~ -1.5 dBFS peak
    pcm = (sig * 32767).astype("<i2")
    with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return len(sig) / SR


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (fn, desc) in SOUNDS.items():
        dur = write(name, fn())
        manifest[name] = {"file": f"{name}.wav", "duration": round(dur, 3), "description": desc}
        print(f"{name:10s} {dur:5.2f}s")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
