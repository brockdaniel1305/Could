#!/usr/bin/env python3
"""Render a "Could...?" episode (script.json) into a vertical 1080x1920 TikTok video.

Usage:
    python3 tools/render.py episodes/001-neuer-titanic/script.json
    python3 tools/render.py episodes/001-neuer-titanic/script.json --music my_track.mp3

Voice-over is synthesised with Piper (offline TTS). Markup in "vo" / text fields:
    {1912|nineteen twelve}  -> shown as "1912" in subtitles, spoken as "nineteen twelve"
Optional per-scene "image": path (relative to the script) shown in the archive frame.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30
SR = 22050
SPEED = 0.85  # piper length scale: <1 = faster narration
ROOT = Path(__file__).resolve().parent.parent
VOICE_DIR = ROOT / "voices"
DEFAULT_VOICE = "en_GB-alan-medium"
VOICE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/"

BG = (14, 13, 11)
FG = (236, 228, 212)
DIM = (140, 132, 118)
ACCENT = (217, 164, 65)
RED = (196, 48, 38)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
F_SANS_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

MARKUP = re.compile(r"\{([^|}]*)\|([^}]*)\}")


def shown(text):
    return MARKUP.sub(r"\1", text)


def spoken(text):
    return MARKUP.sub(r"\2", text)


_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def lerp(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if draw.textlength(test, font=fnt) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- audio

def ensure_voice(name):
    model = VOICE_DIR / f"{name}.onnx"
    if not model.exists():
        if name != DEFAULT_VOICE:
            sys.exit(f"Voice model {model} not found.")
        VOICE_DIR.mkdir(exist_ok=True)
        for f in (f"{name}.onnx", f"{name}.onnx.json"):
            print(f"Downloading {f} ...")
            subprocess.run(["curl", "-sSL", "-o", str(VOICE_DIR / f), VOICE_URL + f], check=True)
    return model


def tts(text, model, cache_dir):
    key = hashlib.sha1((f"{model.name}{SPEED}" + text).encode()).hexdigest()[:16]
    out = cache_dir / f"{key}.wav"
    if not out.exists():
        subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "--length-scale", str(SPEED), "-f", str(out)],
                       input=text.encode(), check=True, capture_output=True)
    with wave.open(str(out)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        assert w.getframerate() == SR, "voice must be 22.05 kHz"
    return data


def music_bed(n):
    """Low documentary drone + quiet clock tick."""
    t = np.arange(n) / SR
    drone = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((55, 0.5), (82.41, 0.3), (110, 0.2), (164.8, 0.08)))
    drone *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * t)
    tick = np.zeros(n)
    tick_len = int(0.03 * SR)
    env = np.exp(-np.linspace(0, 8, tick_len)) * np.sin(2 * np.pi * 2400 * np.arange(tick_len) / SR)
    for start in range(0, n - tick_len, SR):
        tick[start:start + tick_len] += env * 0.35
    return drone * 0.035 + tick * 0.05


def thud(n_at, n):
    out = np.zeros(n)
    ln = int(0.6 * SR)
    tt = np.arange(ln) / SR
    s = np.sin(2 * np.pi * (70 - 30 * tt) * tt) * np.exp(-tt * 7) * 0.8
    end = min(n, n_at + ln)
    out[n_at:end] = s[: end - n_at]
    return out


# ---------------------------------------------------------------- visuals

def make_vignette():
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = np.clip(1 - 0.55 * np.clip(d - 0.35, 0, None) ** 1.4, 0, 1)
    base = np.zeros((H, W, 3), np.float32)
    base[:] = BG
    base[:, :, 0] += 10 * (1 - d.clip(0, 1))  # warm centre
    base[:, :, 1] += 6 * (1 - d.clip(0, 1))
    return Image.fromarray((base * v[..., None]).clip(0, 255).astype(np.uint8))


def grain_frames(k=6):
    rng = np.random.default_rng(7)
    return [rng.normal(0, 4, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1).astype(np.int16) for _ in range(k)]


class Ctx:
    def __init__(self, img, t):
        self.img, self.d, self.t = img, ImageDraw.Draw(img), t

    def p(self, delay, dur=0.45):
        return ease((self.t - delay) / dur)

    def text(self, xy, s, fnt, color, delay, anchor="la", slide=24):
        p = self.p(delay)
        if p <= 0:
            return
        x, y = xy
        self.d.text((x, y + (1 - p) * slide), s, font=fnt, fill=lerp(BG, color, p), anchor=anchor)

    def spaced(self, xy, s, fnt, color, delay, spacing=6, anchor="l"):
        p = self.p(delay)
        if p <= 0:
            return
        total = sum(self.d.textlength(c, font=fnt) + spacing for c in s) - spacing
        x, y = xy
        if anchor == "m":
            x -= total / 2
        for c in s:
            self.d.text((x, y), c, font=fnt, fill=lerp(BG, color, p))
            x += self.d.textlength(c, font=fnt) + spacing

    def line(self, x0, y, x1, color, delay, width=3):
        p = self.p(delay, 0.7)
        if p > 0:
            self.d.line([(x0, y), (x0 + (x1 - x0) * p, y)], fill=color, width=width)


def header(c, case_id):
    c.spaced((80, 120), "COULD?", font(F_BLACK, 40), FG, 0, spacing=4)
    c.text((W - 80, 128), f"FILE {case_id}", font(F_MONO, 30), DIM, 0, anchor="ra", slide=0)
    c.line(80, 190, W - 80, (60, 56, 50), 0, width=2)


def draw_title(c, sc, ep):
    c.spaced((W / 2, 560), sc.get("kicker", ""), font(F_MONO, 34), ACCENT, 0.1, spacing=8, anchor="m")
    fnt = font(F_SERIF, 112)
    lines = wrap(c.d, shown(sc["headline"]), fnt, W - 160)
    y = 660
    for i, ln in enumerate(lines):
        c.text((W / 2, y), ln, fnt, FG, 0.3 + 0.18 * i, anchor="ma")
        y += 132
    c.line(W / 2 - 120, y + 40, W / 2 + 120, ACCENT, 0.3 + 0.18 * len(lines), width=5)


def archive_frame(c, sc, base_dir, box, delay):
    x0, y0, x1, y1 = box
    p = c.p(delay, 0.6)
    if p <= 0:
        return
    img_path = sc.get("image")
    if img_path and (base_dir / img_path).exists():
        im = Image.open(base_dir / img_path).convert("L")
        im = ImageOps.fit(im, (x1 - x0, y1 - y0))
        im = ImageOps.colorize(ImageOps.autocontrast(im), (20, 16, 12), (235, 222, 196))
        im = Image.blend(Image.new("RGB", im.size, BG), im, p)
        c.img.paste(im, (x0, y0))
    else:
        c.d.rectangle(box, fill=lerp(BG, (26, 24, 21), p))
        c.text(((x0 + x1) / 2, (y0 + y1) / 2 - 20), sc.get("initials", "?"), font(F_SERIF, 190),
               (70, 64, 56), delay, anchor="mm", slide=0)
        c.text(((x0 + x1) / 2, y1 - 50), "NO PHOTO ON FILE", font(F_MONO, 26), (90, 84, 74), delay,
               anchor="ma", slide=0)
    c.d.rectangle(box, outline=lerp(BG, (90, 84, 74), p), width=3)


def draw_profile(c, sc, ep):
    c.spaced((80, 250), sc["label"], font(F_MONO, 34), ACCENT, 0.05, spacing=8)
    c.text((80, 300), shown(sc["name"]), font(F_SERIF, 96), FG, 0.2)
    c.text((80, 425), shown(sc.get("sub", "")), font(F_SANS, 38), DIM, 0.35)
    archive_frame(c, sc, ep["_dir"], (80, 500, W - 80, 880), 0.45)
    y = 930
    for i, (k, v) in enumerate(sc.get("stats", [])):
        d = 0.8 + 0.22 * i
        c.text((80, y), k.upper(), font(F_MONO, 32), DIM, d, slide=10)
        c.text((W - 80, y - 6), shown(v), font(F_SANS_B, 44), FG, d, anchor="ra", slide=10)
        c.line(80, y + 62, W - 80, (48, 45, 40), d, width=2)
        y += 80


def draw_compare(c, sc, ep):
    c.spaced((80, 250), sc["heading"], font(F_MONO, 34), ACCENT, 0.05, spacing=8)
    fnt = font(F_SERIF, 96)
    y = 300
    for i, ln in enumerate(wrap(c.d, shown(sc["title"]), fnt, W - 160)):
        c.text((80, y), ln, fnt, FG, 0.2 + 0.1 * i)
        y += 112
    y += 70
    for i, row in enumerate(sc["rows"]):
        label, value, frac = row
        d = 0.6 + 0.7 * i
        c.text((80, y), label.upper(), font(F_MONO, 32), DIM, d, slide=10)
        c.text((80, y + 48), shown(value), font(F_SANS_B, 52), FG, d, slide=10)
        p = c.p(d + 0.2, 1.4)
        bar_w = (W - 160) * frac * p
        if bar_w > 1:
            x1 = 80 + bar_w
            c.d.rectangle((80, y + 130, min(x1, W + 50), y + 160), fill=ACCENT if i else (120, 112, 98))
            if x1 > W:
                c.text((W - 80, y + 172), "(continues off-screen)", font(F_MONO, 24), DIM, d + 1.0,
                       anchor="ra", slide=0)
        y += 250
    if sc.get("result"):
        d = 0.6 + 0.7 * len(sc["rows"]) + 0.3
        fnt = font(F_BLACK, 70)
        for ln in wrap(c.d, shown(sc["result"]), fnt, W - 160):
            c.text((W / 2, y + 20), ln, fnt, ACCENT, d, anchor="ma")
            y += 84


def draw_verdict(c, sc, ep):
    c.spaced((W / 2, 300), sc["heading"], font(F_MONO, 40), ACCENT, 0.05, spacing=12, anchor="m")
    c.line(W / 2 - 160, 370, W / 2 + 160, ACCENT, 0.1, width=3)
    # rubber stamp slam
    d0 = sc.get("_stamp_at", 2.0)
    if c.t >= d0:
        k = ease((c.t - d0) / 0.22)
        scale = 1.8 - 0.8 * k
        layer = Image.new("RGBA", (760, 420), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((20, 20, 740, 400), radius=24, outline=RED + (255,), width=18)
        ld.text((380, 215), shown(sc["stamp"]), font=font(F_BLACK, 250), fill=RED + (255,), anchor="mm")
        layer = layer.rotate(-9, expand=True, resample=Image.BICUBIC)
        layer = layer.resize((int(layer.width * scale), int(layer.height * scale)), Image.BILINEAR)
        a = layer.getchannel("A").point(lambda v: int(v * min(1, k * 1.5) * 0.92))
        layer.putalpha(a)
        c.img.paste(layer, (int(W / 2 - layer.width / 2), int(720 - layer.height / 2)), layer)
    y = 1000
    for i, (k_, v) in enumerate(sc.get("lines", [])):
        d = d0 + 1.2 + 0.9 * i
        c.text((80, y), k_.upper(), font(F_MONO, 32), DIM, d, slide=10)
        c.text((W - 80, y - 8), shown(v), font(F_SANS_B, 52), FG, d, anchor="ra", slide=10)
        c.line(80, y + 66, W - 80, (48, 45, 40), d, width=2)
        y += 96


def draw_outro(c, sc, ep):
    fnt = font(F_SERIF, 104)
    y = 640
    for i, ln in enumerate(wrap(c.d, shown(sc["headline"]), fnt, W - 160)):
        c.text((W / 2, y), ln, fnt, FG, 0.1 + 0.15 * i, anchor="ma")
        y += 124
    c.spaced((W / 2, y + 50), sc.get("sub", "").upper(), font(F_MONO, 34), ACCENT, 0.6, spacing=8, anchor="m")


DRAW = {"title": draw_title, "profile": draw_profile, "compare": draw_compare,
        "verdict": draw_verdict, "outro": draw_outro}


def caption_chunks(text, max_chars=20):
    words, chunks, cur = shown(text).split(), [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if len(test) > max_chars and cur:
            chunks.append(cur)
            cur = w
        else:
            cur = test
        if cur.endswith((".", "?", "!", ":")):
            chunks.append(cur)
            cur = ""
    if cur:
        chunks.append(cur)
    return chunks


def draw_caption(img, text):
    d = ImageDraw.Draw(img)
    fnt = font(F_SANS_B, 58)
    tw = d.textlength(text, font=fnt)
    cx, cy = W / 2, 1390
    d.rounded_rectangle((cx - tw / 2 - 28, cy - 50, cx + tw / 2 + 28, cy + 46), radius=14, fill=(0, 0, 0))
    d.text((cx, cy), text, font=fnt, fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--music", help="optional music file to use instead of the generated drone")
    ap.add_argument("--out")
    ap.add_argument("--no-captions", action="store_true")
    args = ap.parse_args()

    script_path = Path(args.script).resolve()
    ep = json.loads(script_path.read_text())
    ep["_dir"] = script_path.parent
    out = Path(args.out) if args.out else script_path.parent / f"{script_path.parent.name}.mp4"
    build = script_path.parent / ".build"
    build.mkdir(exist_ok=True)
    model = ensure_voice(args.voice)

    # 1. voice-over per scene -> timeline
    lead, tail = 0.35, 0.55
    timeline, voice_parts, t0 = [], [], 0.0
    for sc in ep["scenes"]:
        audio = tts(spoken(sc["vo"]), model, build)
        dur = lead + len(audio) / SR + tail
        if sc["type"] == "verdict":
            # stamp lands right after the narrator's question
            q = shown(sc["vo"]).find("?")
            frac = (q + 1) / len(shown(sc["vo"])) if q > 0 else 0.4
            sc["_stamp_at"] = lead + frac * len(audio) / SR + 0.1
        timeline.append((t0, dur, sc, audio))
        t0 += dur
    total = t0
    n_frames = int(math.ceil(total * FPS))
    n_samples = int(n_frames / FPS * SR)

    # 2. mix audio
    mix = np.zeros(n_samples, np.float32)
    for start, dur, sc, audio in timeline:
        s = int((start + lead) * SR)
        mix[s:s + len(audio)] += audio[: n_samples - s]
        if sc["type"] == "verdict":
            mix += thud(int((start + sc["_stamp_at"]) * SR), n_samples).astype(np.float32)
    if not args.music:
        mix += music_bed(n_samples).astype(np.float32)
    mix = np.clip(mix, -1, 1)
    wav_path = build / "mix.wav"
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    # 3. captions timing (proportional to characters over each voice clip)
    caps = []
    for start, dur, sc, audio in timeline:
        chunks = caption_chunks(sc["vo"])
        total_chars = sum(len(c) + 3 for c in chunks)
        t = start + lead
        speech = len(audio) / SR
        for ch in chunks:
            d = speech * (len(ch) + 3) / total_chars
            caps.append((t, t + d, ch))
            t += d

    # 4. frames -> ffmpeg
    bg = make_vignette()
    grains = grain_frames()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav_path)]
    if args.music:
        cmd += ["-stream_loop", "-1", "-i", args.music, "-filter_complex",
                "[2:a]volume=0.12,afade=t=out:st=%.2f:d=1.5[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]"
                % (total - 1.5), "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    ci = 0
    for f in range(n_frames):
        t = f / FPS
        while ci + 1 < len(timeline) and t >= timeline[ci + 1][0]:
            ci += 1
        start, dur, sc, _ = timeline[ci]
        lt = t - start
        img = bg.copy()
        c = Ctx(img, lt)
        header(c, ep["id"])
        DRAW[sc["type"]](c, sc, ep)
        # slow push-in (Ken Burns) per scene
        z = 1 + 0.035 * (lt / dur)
        if z > 1.001:
            zw, zh = int(W * z), int(H * z)
            img = img.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2,
                                                              (zw - W) // 2 + W, (zh - H) // 2 + H))
        # scene fade from/to black
        fade = min(1, lt / 0.25, (dur - lt) / 0.2 if ci + 1 < len(timeline) else (dur - lt) / 0.8)
        if not args.no_captions:
            for a, b, txt in caps:
                if a <= t < b:
                    draw_caption(img, txt)
                    break
        arr = np.asarray(img).astype(np.int16) + grains[(f // 8) % len(grains)]
        if fade < 1:
            arr = arr * max(0.0, fade)
        ff.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
        if f % 150 == 0:
            print(f"  frame {f}/{n_frames}", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"Done: {out}  ({total:.1f}s)")


if __name__ == "__main__":
    main()
