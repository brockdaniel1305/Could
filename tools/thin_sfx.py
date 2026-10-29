#!/usr/bin/env python3
"""Keep sound effects sparse (creator, 2026-10-29: "nicht so viele, eher punktuell, wenn es Qualität gibt").

    python3 tools/thin_sfx.py episodes/<ep> [--strict]   (then run build_episode.py again)

Drops card swooshes, synthetic crowd/wind beds and UI ticks, removes the generated layer ("auto": true), and keeps
at most two of the same effect per scene (the first and the last). What stays are the accents on real events:
kick, net, stamp/impact, whistle, fall, clang, gallop, sting.
"""
import json
import sys
from pathlib import Path

DROP = {"swoosh", "whoosh-short", "roar", "wind", "rustle", "tick", "page", "sparkle", "ping", "pop", "drumroll",
        "heartbeat", "gulp", "whoosh-cinematic", "notification", "click", "click-soft", "chime", "typing", "key-press"}
MAX_SAME = 2

ep = Path(sys.argv[1])
if "--strict" in sys.argv:  # busy cartoon episodes: one of each per scene, no cartoon boings/birds
    MAX_SAME = 1
    DROP |= {"boing", "tweet", "spin", "ding"}
p = ep / "narration.json"
d = json.loads(p.read_text())
before = after = 0
for sc in d["scenes"]:
    fx = sc.get("sfx", [])
    before += len(fx)
    fx = [f for f in fx if not f.get("auto") and f["name"] not in DROP]
    keep = []
    for name in dict.fromkeys(f["name"] for f in fx):
        same = [f for f in fx if f["name"] == name]
        keep += same if len(same) <= MAX_SAME else ([same[0], same[-1]] if MAX_SAME == 2 else [same[0]])
    sc["sfx"] = [f for f in fx if any(f is k for k in keep)]
    after += len(sc["sfx"])
p.write_text(json.dumps(d, indent=2, ensure_ascii=False))
print(f"{ep.name}: {before} -> {after} sfx")
