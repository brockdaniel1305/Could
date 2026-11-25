"""COULD? AI-clip episodes: cut generated video clips (and stills) into a 1080x1920 short, add text overlays
(hook, small subtitles, on-screen writing) and the audio mix. usage: python3 tools/pov/assemble.py episodes/<ep>
Reads <ep>/edit.json:
  { "end": 32.5,
    "shots": [ {"src": "assets/clips/c1.mp4", "in": 0, "out": 5, "at": 0},            # video clip (trimmed)
               {"src": "assets/frames/K5.png", "dur": 2, "at": 21, "zoom": [1.0, 1.12]} ],  # still with slow push-in
    "text": [ {"t0": 0, "t1": 2.3, "kind": "hook", "text": "Your reflection<br>just blinked first."},
              {"t0": 10.3, "t1": 14, "kind": "smear", "text": "DON'T TURN AROUND", "x": 540, "y": 700, "reveal": 1.6} ],
    "lines": [ ["yo_blink", "YOU", 1.2], ... ]       # assets/voice/<id>.wav, subtitles from whisper words
    "sfx":   [ ["brush", 0.0, 0.5], ["room", 0, 0.35, {"loop": true, "until": 32.5}] ],
    "music": ["tension", 0.08, 18.3] }                 # optional 3rd value: start time
  text kinds: hook, question, smear, endcard ({"text": "WHAT DOES<br>IT WANT?", "sub": "Comment PART 2 ..."})
Writes <ep>/renders/<ep>.mp4 (loudness -15 LUFS)."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ep = Path(sys.argv[1]).resolve(); cfg = json.loads((ep / "edit.json").read_text())
W, H, FPS, END = 1080, 1920, 30, cfg["end"]
tmp = ep / ".build"; tmp.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/"
run = lambda a: subprocess.run(a, check=True)
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

# ---------------- 1. picture: every shot to 1080x1920 @30, then concatenated in time order ----------------
parts = []
for i, s in enumerate(sorted(cfg["shots"], key=lambda s: s["at"])):
    out = tmp / f"shot{i:02d}.mp4"; src = ep / s["src"]
    if src.suffix in (".png", ".jpg"):
        d = s["dur"]; z0, z1 = s.get("zoom", [1.0, 1.08]); n = int(round(d * FPS))
        vf = (f"scale={W*2}:{H*2},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p")
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(src), "-vf", vf, "-frames:v", str(n), "-r", str(FPS), str(out)])
    else:
        d = s["out"] - s["in"]
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p" + (",hflip" if s.get("flip") else "")
        if s.get("speed"): vf = f"setpts=PTS/{s['speed']}," + vf
        if s.get("reverse"): vf = "reverse," + vf      # play the trimmed part backwards
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(s["in"]), "-t", str(d * s.get("speed", 1)), "-i", str(src), "-an", "-vf", vf,
             "-frames:v", str(int(round(d * FPS))), str(out)])
    parts.append(out)
(tmp / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts))
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c:v", "libx264", "-crf", "16", "-r", str(FPS), str(tmp / "picture.mp4")])

# ---------------- 2. text overlays rendered as PNGs (hook, subtitles, writing on the mirror) ----------------
timing = {l["id"]: l for l in json.loads((ep / "pov_timing.json").read_text())["lines"]} if (ep / "pov_timing.json").exists() else {}
overlays = []
def png(name, draw_fn):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(im); p = tmp / f"{name}.png"; im.save(p); return p
def shadow_text(im, xy, text, font, fill, anchor="la", blur=6, alpha=210):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text(xy, text, font=font, fill=(0, 0, 0, alpha), anchor=anchor)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); ImageDraw.Draw(im).text(xy, text, font=font, fill=fill, anchor=anchor)
for k, t in enumerate(cfg.get("text", [])):
    if t["kind"] == "hook":
        f = ImageFont.truetype(FONT + "Inter-Black.otf", 74); lines = t["text"].split("<br>")
        def d(im, lines=lines, f=f):
            for i, s in enumerate(lines): shadow_text(im, (60, 230 + i * 86), s, f, (255, 255, 255) if i == 0 else (255, 210, 63))
        overlays.append((png(f"hook{k}", d), t["t0"], t["t1"], 0.15))
    elif t["kind"] == "question":
        f = ImageFont.truetype(FONT + "Inter-ExtraBold.otf", 58)
        overlays.append((png(f"q{k}", lambda im, f=f, t=t: shadow_text(im, (W // 2, t.get("y", 1500)), t["text"], f, (255, 255, 255), "mm")), t["t0"], t["t1"], 0.3))
    elif t["kind"] == "endcard":
        # cliffhanger card: darkened frame, big title, small call to action
        fT = ImageFont.truetype(FONT + "Inter-Black.otf", t.get("size", 96)); fS = ImageFont.truetype(FONT + "Inter-SemiBold.otf", 46)
        def d(im, t=t, fT=fT, fS=fS):
            ImageDraw.Draw(im).rectangle((0, 0, W, H), fill=(0, 0, 0, 150))
            for i, s in enumerate(t["text"].split("<br>")): shadow_text(im, (W // 2, t.get("y", 860) + i * 112), s, fT, (255, 255, 255) if i else (255, 210, 63), "mm", 10, 255)
            if t.get("sub"): shadow_text(im, (W // 2, t.get("y", 860) + 330), t["sub"], fS, (235, 240, 245), "mm", 6, 230)
        overlays.append((png(f"end{k}", d), t["t0"], t["t1"], 0.35))
    elif t["kind"] == "chip":
        # info card: small label + big value in a dark rounded box (e.g. "GREYHOUND" / "70 KM/H", "GOAL" / "1-0")
        fk = ImageFont.truetype(FONT + "Inter-Bold.otf", 30); fv = ImageFont.truetype(FONT + "Inter-Black.otf", t.get("size", 70))
        def d(im, t=t, fk=fk, fv=fv):
            x, y = t.get("x", 70), t.get("y", 300); g = ImageDraw.Draw(im)
            w = max(g.textlength(t["label"], font=fk), g.textlength(t["text"], font=fv)) + 56; h = 56 + t.get("size", 70)
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 8, y + 8, x + w + 8, y + h + 8), 22, fill=(0, 0, 0, 150))
            im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
            g.rounded_rectangle((x, y, x + w, y + h), 22, fill=tuple(t.get("bg", (26, 26, 46))) + (238,), outline=tuple(t.get("fg", (255, 210, 63))), width=5)
            g.text((x + 28, y + 18), t["label"], font=fk, fill=tuple(t.get("fg", (255, 210, 63))))
            g.text((x + 28, y + 52), t["text"], font=fv, fill=(255, 255, 255))
        overlays.append((png(f"chip{k}", d), t["t0"], t["t1"], 0.15))
    elif t["kind"] == "smear":
        # toothpaste writing on the glass: thick, slightly wobbly white letters, revealed letter by letter
        f = ImageFont.truetype(FONT + "Inter-Black.otf", t.get("size", 92)); txt = t["text"]; n = len(txt); steps = 8
        for st in range(1, steps + 1):
            m = max(1, round(n * st / steps))
            def d(im, s=txt[:m], f=f, t=t):
                lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
                g.text((t["x"], t["y"]), s, font=f, fill=(245, 248, 250, 235), anchor="mm", stroke_width=3, stroke_fill=(210, 220, 228, 200))
                lay = lay.rotate(t.get("rot", -4), center=(t["x"], t["y"]), resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8))
                im.alpha_composite(lay)
            t0 = t["t0"] + t.get("reveal", 1.5) * (st - 1) / steps
            t1 = t["t0"] + t.get("reveal", 1.5) * st / steps if st < steps else t["t1"]
            overlays.append((png(f"sm{k}_{st}", d), t0, t1, 0))
# subtitles: small, unobtrusive, bottom
sub_font = ImageFont.truetype(FONT + "Inter-SemiBoldItalic.otf" if (Path(FONT) / "Inter-SemiBoldItalic.otf").exists() else FONT + "Inter-MediumItalic.otf", 38)
for name, who, t0 in cfg["lines"]:
    if name in cfg.get("nosub", []): continue
    l = timing.get(name); text = " ".join(w[0] for w in l["words"]) if l else name
    d0 = l["dur"] if l else dur(ep / f"assets/voice/{name}.wav")
    # wrap to lines that fit the frame (max ~900 px), stacked upward from y 1620
    rows, cur = [], ""
    for w in text.split():
        if cur and sub_font.getlength(cur + " " + w) > 900: rows.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    rows.append(cur)
    def dsub(im, rows=rows):
        for i, r in enumerate(rows): shadow_text(im, (W // 2, 1620 - (len(rows) - 1 - i) * 50), r, sub_font, (235, 245, 255, 235), "mm", 4, 230)
    overlays.append((png(f"sub_{name}", dsub), t0 - 0.05, t0 + d0 + 0.3, 0.12))

# ---------------- 3. composite overlays onto the picture ----------------
inputs, chain, last = ["-i", str(tmp / "picture.mp4")], "", "0:v"
for i, (p, t0, t1, fade) in enumerate(overlays):
    inputs += ["-loop", "1", "-t", f"{END:.2f}", "-i", str(p)]
    fl = f"[{i + 1}:v]format=rgba" + (f",fade=t=in:st={t0:.2f}:d={fade}:alpha=1,fade=t=out:st={max(t0, t1 - fade):.2f}:d={fade}:alpha=1" if fade else "") + f"[o{i}];"
    chain += fl + f"[{last}][o{i}]overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})'[v{i}];"; last = f"v{i}"
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", chain.rstrip(";"), "-map", f"[{last}]", "-t", f"{END:.2f}",
     "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp / "video.mp4")])

# ---------------- 4. audio mix ----------------
ain, fl, k = [], [], 0
def add(path, t0, vol, extra=""):
    global k
    ain.extend(["-i", str(path)]); fl.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo{extra},volume={vol},adelay={int(t0 * 1000)}|{int(t0 * 1000)}[a{k}]"); k += 1
for name, who, t0 in cfg["lines"]: add(ep / f"assets/voice/{name}.wav", t0, 1.0)
for s in cfg.get("sfx", []):
    name, t0, vol = s[0], s[1], s[2]; o = s[3] if len(s) > 3 else {}; p = ep / f"assets/sfx/{name}.wav"
    if o.get("loop"):
        L = o.get("until", END) - t0; q = tmp / f"loop_{name}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(p), "-t", f"{L:.2f}", "-af", f"afade=t=out:st={max(0, L - 1):.2f}:d=1", str(q)]); p = q
    add(p, t0, vol)
m, mv = cfg["music"][:2]; ms = cfg["music"][2] if len(cfg["music"]) > 2 else 0   # optional start time (music enters later)
add(ep / f"assets/music/{m}.wav", ms, mv, f",atrim=0:{END - ms},afade=t=in:d={0.8 if ms else 0.01},afade=t=out:st={END - ms - 1.5}:d=1.5")
fc = ";".join(fl) + ";" + "".join(f"[a{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0,atrim=0:{END},loudnorm=I=-15:TP=-1.5:LRA=11[aout]"
out = ep / "renders" / f"{ep.name}.mp4"; out.parent.mkdir(exist_ok=True)
run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), *ain, "-filter_complex", fc,
     "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{END:.2f}", str(out)])
print("wrote", out, f"{dur(out):.2f}s")
