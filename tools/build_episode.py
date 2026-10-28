#!/usr/bin/env python3
"""Voice + timing + captions + root timeline for a COULD? HyperFrames episode.

    python3 tools/build_episode.py episodes/001-neuer-titanic

Reads   <ep>/narration.json
Writes  <ep>/assets/voice/<scene>.wav      voice-over: Kokoro (npx hyperframes tts) or VoiceStudio
        <ep>/timing.json                   scene slots, word times, cue times (local to each scene)
        <ep>/compositions/captions.html    karaoke captions from the real word timings
        <ep>/index.html                    root: scene hosts, frame, captions, voice, sfx, music
        <ep>/compositions/<scene>.html     stub from channel/kit/scene-template.html if missing

Narration markup:
    {1912|nineteen twelve}  shown "1912" in captions, spoken "nineteen twelve"
    {{punch}}               cue marker: timing.json gets the time of the next word as cues.punch
    ||0.8||                 dramatic pause of 0.8 s in the voice-over

Voice provider (narration.json "provider"):
    "kokoro"       offline, voice e.g. "bm_george" (default)
    "voicestudio"  local VoiceStudio app (OpenAI-compatible API), voice = a VoiceStudio voice profile id.
                   Env: VOICESTUDIO_BASE_URL (default http://localhost:3900/v1), VOICESTUDIO_API_KEY (default "local").
"""
import difflib
import hashlib
import html
import json
import re
import shutil
import os
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SFX_LIB = ROOT / ".claude/skills/media-use/audio/assets/sfx"
KIT = ROOT / "channel/kit"
SFX_MANIFEST = json.loads((SFX_LIB / "manifest.json").read_text())
W, H = 1080, 1920
LEAD, TAIL, OUTRO_TAIL = 0.15, 0.45, 1.6

UNIT = re.compile(r"\{\{(\w+)\}\}|\{([^|{}]*)\|([^{}]*)\}|(\S+)")


def parse(text):
    """-> units [{shown, spoken:[tokens]}], cues {name: unit index}"""
    units, cues = [], {}
    for m in UNIT.finditer(text):
        if m.group(1):
            cues[m.group(1)] = len(units)
        elif m.group(2) is not None:
            units.append({"shown": m.group(2), "spoken": m.group(3).split()})
        elif units and not norm(m.group(4)):
            units[-1]["shown"] += m.group(4)  # punctuation after a {shown|spoken} unit
        else:
            units.append({"shown": m.group(4), "spoken": [m.group(4)]})
    return units, cues


PAUSE = re.compile(r"\|\|([\d.]+)\|\|")


VS_URL = os.environ.get("VOICESTUDIO_BASE_URL", "http://localhost:3900/v1").rstrip("/")
VS_KEY = os.environ.get("VOICESTUDIO_API_KEY", "local")


def voicestudio_health():
    url = VS_URL.rsplit("/v1", 1)[0] + "/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            info = json.loads(r.read())
    except (urllib.error.URLError, OSError, ValueError) as e:
        sys.exit(f"VoiceStudio is not reachable at {url} ({e}).\n"
                 "Start the VoiceStudio app (or set VOICESTUDIO_BASE_URL), or set \"provider\": \"kokoro\" in narration.json.")
    print(f"VoiceStudio {info.get('version')} on {info.get('device')}")


def voicestudio_tts(text, out, voice, speed, model):
    body = json.dumps({"model": model, "voice": voice, "input": text, "response_format": "wav", "speed": speed}).encode()
    req = urllib.request.Request(f"{VS_URL}/audio/speech", data=body, method="POST", headers={
        "Authorization": f"Bearer {VS_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"VoiceStudio refused the request ({e.code}): {e.read().decode(errors='replace')[:400]}")
    tmp = out.with_suffix(".raw")
    tmp.write_bytes(raw)
    # one format for every segment so pauses and parts concatenate cleanly
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-ac", "1", "-ar", "24000", "-sample_fmt", "s16", str(out)])
    tmp.unlink()


def voice_scene(sc, vdir, voice, speed, cache):
    """Synthesise a scene in segments split at ||pause|| markers -> units, spans, cues, speech length."""
    parts = PAUSE.split(sc["text"])
    segs = [(parts[i], float(parts[i + 1]) if i + 1 < len(parts) else 0.0) for i in range(0, len(parts), 2)]
    units, spans, cues, frames, params, t = [], [], {}, [], None, 0.0
    for k, (text, pause) in enumerate(segs):
        u, cue_idx = parse(text)
        spoken = " ".join(tok for x in u for tok in x["spoken"])
        part = vdir / f"{sc['id']}.part{k}.wav"
        words = synth(spoken, part, voice, speed, cache)
        with wave.open(str(part)) as w:
            params = w.getparams()
            data = w.readframes(w.getnframes())
            rate, width = w.getframerate(), w.getsampwidth() * w.getnchannels()
        seg_dur = len(data) / width / rate
        for name, i in cue_idx.items():
            cues[name] = len(units) + i
        spans += [(a + t, b + t) for a, b in align(u, words, seg_dur)]
        units += u
        frames.append(data + b"\x00" * (int(pause * rate) * width))
        t += seg_dur + pause
    with wave.open(str(vdir / f"{sc['id']}.wav"), "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames))
    return units, spans, cues, t


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


TTS = {"provider": "kokoro", "model": "tts-1"}


def synth(text, out, voice, speed, cache):
    tag = f"{voice}|{speed}" if TTS["provider"] == "kokoro" else f"voicestudio|{TTS['model']}|{voice}|{speed}"
    key = hashlib.sha1(f"{tag}|{text}".encode()).hexdigest()
    if cache.get(out.name, {}).get("key") == key and out.exists():
        return cache[out.name]["words"]
    if TTS["provider"] == "voicestudio":
        voicestudio_tts(text, out, voice, speed, TTS["model"])
    else:
        run(["npx", "--yes", "hyperframes", "tts", text, "-v", voice, "-s", str(speed), "-o", str(out), "--json"])
    words = []
    for line in run(["npx", "--yes", "hyperframes", "transcribe", str(out), "--model", "small.en", "--json"],
                    cwd=out.parent).splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "words":
            words += ev["words"]
    (out.parent / "transcript.json").unlink(missing_ok=True)
    cache[out.name] = {"key": key, "words": words}
    return words


def align(units, words, speech_dur):
    """Give every script unit a [start, end] from the transcript (matched by position)."""
    flat = [(ui, tok) for ui, u in enumerate(units) for tok in u["spoken"]]
    a = [norm(t) for _, t in flat]
    b = [norm(w["text"]) for w in words]
    times = [None] * len(flat)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w = words[blk.b + k]
            times[blk.a + k] = (w["start"], w["end"])
    spans = [None] * len(units)
    for (ui, _), t in zip(flat, times):
        if t:
            s, e = spans[ui] or (t[0], t[1])
            spans[ui] = (min(s, t[0]), max(e, t[1]))
    # interpolate units whisper heard differently (numbers, names)
    i = 0
    while i < len(units):
        if spans[i]:
            i += 1
            continue
        j = i
        while j < len(units) and not spans[j]:
            j += 1
        t0 = spans[i - 1][1] if i else 0.0
        t1 = spans[j][0] if j < len(units) else speech_dur
        weights = [len(units[k]["shown"]) + 2 for k in range(i, j)]
        total, acc = sum(weights), t0
        for k, wgt in zip(range(i, j), weights):
            d = (t1 - t0) * wgt / total
            spans[k] = (acc, acc + d)
            acc += d
        i = j
    return spans


def caption_groups(words, max_words=4, max_chars=22):
    groups, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        text_len = sum(len(x["text"]) + 1 for x in cur)
        brk = (w["text"][-1] in ".?!:;," or len(cur) >= max_words or text_len >= max_chars
               or not nxt or nxt["start"] - w["end"] >= 0.15)
        if brk:
            groups.append(cur)
            cur = []
    return groups


def captions_html(groups, total):
    rows = []
    for g, grp in enumerate(groups):
        spans = "".join(f'<span class="cw" id="cw-{g}-{i}">{html.escape(w["text"])}</span>'
                        for i, w in enumerate(grp))
        rows.append(f'      <div class="cg" id="cg-{g}"><div class="cl">{spans}</div></div>')
    data = [[round(grp[0]["start"], 3), round(grp[-1]["end"], 3), [round(w["start"], 3) for w in grp]]
            for grp in groups]
    tpl = (KIT / "captions-template.html").read_text()
    return (tpl.replace("__DURATION__", f"{total:.3f}")
               .replace("__GROUPS_HTML__", "\n".join(rows))
               .replace("__GROUPS_JSON__", json.dumps(data)))


def main():
    ep = Path(sys.argv[1]).resolve()
    cfg = json.loads((ep / "narration.json").read_text())
    voice, speed = cfg.get("voice", "bm_george"), cfg.get("speed", 1.0)
    TTS["provider"] = cfg.get("provider", "kokoro")
    TTS["model"] = cfg.get("model", "tts-1")
    if TTS["provider"] not in ("kokoro", "voicestudio"):
        sys.exit(f"unknown provider {TTS['provider']!r} (kokoro | voicestudio)")
    if TTS["provider"] == "voicestudio":
        voicestudio_health()
    vdir = ep / "assets/voice"
    vdir.mkdir(parents=True, exist_ok=True)
    (ep / "compositions").mkdir(exist_ok=True)
    cache_p = vdir / "cache.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}

    scenes, all_words, t = [], [], 0.0
    for n, sc in enumerate(cfg["scenes"]):
        print(f"[{sc['id']}] voice + timing", flush=True)
        units, spans, cue_idx, speech = voice_scene(sc, vdir, voice, speed, cache)
        cache_p.write_text(json.dumps(cache, indent=1))
        wav = vdir / f"{sc['id']}.wav"
        last = n == len(cfg["scenes"]) - 1
        dur = round(LEAD + speech + (OUTRO_TAIL if last else sc.get("tail", TAIL)), 3)
        local_words = [{"text": u["shown"], "start": round(LEAD + s, 3), "end": round(LEAD + e, 3)}
                       for u, (s, e) in zip(units, spans)]
        cues = {k: round(LEAD + spans[i][0], 3) if i < len(spans) else round(LEAD + speech, 3)
                for k, i in cue_idx.items()}
        scenes.append({"id": sc["id"], "start": round(t, 3), "duration": dur, "voice": f"assets/voice/{wav.name}",
                       "voiceStart": LEAD, "speech": round(speech, 3), "cues": cues, "words": local_words,
                       "sfx": sc.get("sfx", [])})
        all_words += [{**w, "start": round(w["start"] + t, 3), "end": round(w["end"] + t, 3)} for w in local_words]
        t += dur
    total = round(t, 3)
    (ep / "timing.json").write_text(json.dumps({"duration": total, "scenes": scenes}, indent=1))

    # captions
    (ep / "compositions/captions.html").write_text(captions_html(caption_groups(all_words), total))

    # scene stubs
    for s in scenes:
        p = ep / f"compositions/{s['id']}.html"
        if not p.exists():
            p.write_text((KIT / "scene-template.html").read_text().replace("__ID__", s["id"])
                         .replace("__DURATION__", str(s["duration"])))

    # fonts
    fdir = ep / "assets/fonts"
    fdir.mkdir(parents=True, exist_ok=True)
    for f in (KIT / "fonts").glob("*.woff2"):
        shutil.copy(f, fdir / f.name)

    # sfx files
    sdir = ep / "assets/sfx"
    audio_tags, z = [], 0
    for s in scenes:
        z += 1
        audio_tags.append(f'      <audio id="vo-{s["id"]}" class="clip" src="{s["voice"]}" data-start="{s["start"] + LEAD:.3f}" '
                          f'data-duration="{s["speech"]:.3f}" data-track-index="20" data-volume="1"></audio>')
        for k, fx in enumerate(s["sfx"]):
            src = SFX_LIB / f"{fx['name']}.mp3"
            if not src.exists():
                sys.exit(f"unknown sfx {fx['name']}")
            sdir.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, sdir / src.name)
            at = s["cues"][fx["cue"]] if "cue" in fx else fx.get("at", 0)
            at = max(0, s["start"] + at + fx.get("offset", 0))
            fx_dur = SFX_MANIFEST[fx["name"]]["duration"]
            audio_tags.append(f'      <audio id="fx-{s["id"]}-{k}" class="clip" src="assets/sfx/{src.name}" '
                              f'data-start="{at:.3f}" data-duration="{fx_dur}" data-track-index="{22 + k}" data-volume="{fx.get("volume", 0.35)}"></audio>')
    music = cfg.get("music")
    if music:
        audio_tags.append(f'      <audio id="music" class="clip" src="{music["src"]}" data-start="0" data-duration="{total}" '
                          f'data-track-index="24" data-volume="{music.get("volume", 0.14)}" data-fade-out="1.5"></audio>')

    hosts = [f'      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" '
             f'data-start="0" data-duration="{total}" data-track-index="0" data-track-kind="graphics" '
             f'data-width="{W}" data-height="{H}" style="z-index:1"></div>']
    for i, s in enumerate(scenes):
        hosts.append(f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
                     f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="{1 + i % 2}" '
                     f'data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:2"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{total}" data-track-index="10" data-track-kind="captions" '
                 f'data-width="{W}" data-height="{H}" style="z-index:5"></div>')
    if not (ep / "compositions/frame.html").exists():
        (ep / "compositions/frame.html").write_text((KIT / "frame.html").read_text().replace("__CASE__", html.escape(cfg["id"]))
                                                    .replace("__DURATION__", str(total)))

    idx = (KIT / "index-template.html").read_text()
    idx = (idx.replace("__TITLE__", html.escape(cfg["title"])).replace("__DURATION__", str(total))
              .replace("__HOSTS__", "\n".join(hosts)).replace("__AUDIO__", "\n".join(audio_tags))
              .replace("__CASE__", html.escape(cfg["id"])))
    (ep / "index.html").write_text(idx)

    print(f"\nTotal {total:.1f}s")
    for s in scenes:
        print(f"  {s['id']:<10} start {s['start']:6.2f}  dur {s['duration']:5.2f}  cues {s['cues']}")


if __name__ == "__main__":
    main()
