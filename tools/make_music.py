#!/usr/bin/env python3
"""Quiet, theme-matched background music for an episode, synthesised locally (no licences needed).

    python3 tools/make_music.py <theme> <seconds> <out.wav> [--bpm 96]

Themes
  flamenco  nylon-guitar arpeggios over the Andalusian cadence (Am G F E), soft bass, faint shaker   - Spain, bulls, La Liga
  stadium   warm pad + slow pulse, distant crowd-like noise bed                                       - matches, big moments
  march     plucked strings on a light 2/4 pulse                                                      - history, armies
The track fades in/out and sits low; add it via narration.json: "music": {"src": "assets/music/theme.wav", "volume": 0.16}.
Plucks use Karplus-Strong (vectorised per period) so a minute renders in seconds.
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def hz(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave - 4) - 9) / 12)


def pluck(f, dur, rng, bright=0.5, decay=0.996):
    """Karplus-Strong string: noise burst through a damped delay line, computed one period at a time."""
    n, p = int(dur * SR), max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p) * 0.5
    buf = np.convolve(buf, np.ones(3) / 3, mode="same") * (0.6 + bright * 0.4)   # softer attack = nylon
    out = np.empty(n + p)
    out[:p] = buf
    i = p
    while i < n + p:
        prev = out[i - p:i]
        nxt = decay * 0.5 * (prev + np.roll(prev, 1))
        k = min(p, n + p - i)
        out[i:i + k] = nxt[:k]
        i += k
    y = out[:n]
    env = np.minimum(1, np.arange(n) / (0.004 * SR))
    return y * env


def tone(f, dur, kind="sine", attack=0.02, release=0.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) if kind == "sine" else (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t))
    env = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release).clip(0, 1)
    return y * env


def add(track, y, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= track.shape[0]:
        return
    y = y[: track.shape[0] - i] * gain
    track[i:i + len(y), 0] += y * (1 - max(0, pan))
    track[i:i + len(y), 1] += y * (1 + min(0, pan))


def flamenco(seconds, bpm, rng):
    tr = np.zeros((int(seconds * SR) + SR, 2))
    beat = 60 / bpm
    # Andalusian cadence, one chord per bar of 4 beats: Am - G - F - E
    chords = [[("A", 2), ("E", 3), ("A", 3), ("C", 4), ("E", 4)], [("G", 2), ("D", 3), ("G", 3), ("B", 3), ("D", 4)],
              [("F", 2), ("C", 3), ("F", 3), ("A", 3), ("C", 4)], [("E", 2), ("B", 2), ("E", 3), ("G#", 3), ("B", 3)]]
    pattern = [0, 2, 3, 4, 3, 2, 3, 4]          # arpeggio over eighth notes
    t, bar = 0.0, 0
    while t < seconds:
        ch = chords[bar % 4]
        add(tr, pluck(hz(*ch[0]), 2.6, rng, 0.35, 0.997), t, 0.55, -0.15)                       # bass string on the one
        add(tr, tone(hz(ch[0][0], 1), beat * 3.6, "sine", 0.03, 0.6), t, 0.10)                   # soft sub under it
        for k, idx in enumerate(pattern):
            n = ch[idx]
            add(tr, pluck(hz(*n), 1.6, rng, 0.45, 0.995), t + k * beat / 2 + rng.uniform(0, 0.012), 0.32, 0.2 if k % 2 else 0.05)
        if bar % 4 == 3:                         # little rasgueado flourish into the next round
            for j in range(4):
                for n in ch[1:]:
                    add(tr, pluck(hz(*n), 0.9, rng, 0.6, 0.99), t + 3.5 * beat + j * 0.045, 0.10, 0.1)
        for k in range(8):                       # faint shaker on the off-beats
            if k % 2:
                nz = rng.normal(0, 1, int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / (0.012 * SR))
                nz = np.diff(nz, prepend=0)       # high-passed
                add(tr, nz, t + k * beat / 2, 0.025, 0.3)
        t += 4 * beat
        bar += 1
    return tr


def stadium(seconds, bpm, rng):
    tr = np.zeros((int(seconds * SR) + SR, 2))
    beat = 60 / bpm
    prog = [("A", "C#", "E"), ("F#", "A", "C#"), ("D", "F#", "A"), ("E", "G#", "B")]
    t, bar = 0.0, 0
    while t < seconds:
        for i, nm in enumerate(prog[bar % 4]):
            add(tr, tone(hz(nm, 3 + (i > 0)), 4 * beat + 0.4, "warm", 0.6, 1.2), t, 0.09, (-0.3, 0, 0.3)[i])
        for k in range(4):
            add(tr, tone(hz(prog[bar % 4][0], 1), 0.35, "sine", 0.005, 0.25), t + k * beat, 0.16)
        t += 4 * beat
        bar += 1
    bed = rng.normal(0, 1, tr.shape[0])
    bed = np.convolve(bed, np.ones(400) / 400, mode="same") * 0.6
    tr[:, 0] += bed * 0.5
    tr[:, 1] += np.roll(bed, 977) * 0.5
    return tr


def march(seconds, bpm, rng):
    tr = np.zeros((int(seconds * SR) + SR, 2))
    beat = 60 / bpm
    line = [("D", 3), ("A", 3), ("D", 4), ("A", 3), ("C", 4), ("A", 3), ("G", 3), ("A", 3)]
    t = 0.0
    while t < seconds:
        for k, n in enumerate(line):
            add(tr, pluck(hz(*n), 1.0, rng, 0.6, 0.993), t + k * beat / 2, 0.3, 0.1)
        for k in range(4):
            nz = rng.normal(0, 1, int(0.08 * SR)) * np.exp(-np.arange(int(0.08 * SR)) / (0.02 * SR))
            add(tr, np.convolve(nz, np.ones(30) / 30, mode="same"), t + k * beat, 0.12 if k % 2 == 0 else 0.06)
        t += 4 * beat
    return tr


def main():
    theme, seconds, out = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3])
    bpm = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else {"flamenco": 96, "stadium": 84, "march": 104}[theme]
    rng = np.random.default_rng(7)
    tr = {"flamenco": flamenco, "stadium": stadium, "march": march}[theme](seconds, bpm, rng)[: int(seconds * SR)]
    # gentle fades so the loop point is soft, then normalise to -3 dBFS peak (the episode mix sets the real level)
    n = tr.shape[0]
    fade = np.ones(n)
    fi, fo = int(0.4 * SR), int(0.8 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    tr *= fade[:, None]
    tr *= 0.7 / max(1e-6, np.abs(tr).max())
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((tr * 32767).astype("<i2").tobytes())
    print(out, f"{seconds:.1f}s", theme)


if __name__ == "__main__":
    main()
