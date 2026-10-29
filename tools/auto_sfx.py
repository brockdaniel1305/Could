#!/usr/bin/env python3
"""Add a base layer of sound effects to an episode from its cues (the creator wants many SFX).

    python3 tools/auto_sfx.py episodes/<ep>      (needs timing.json; then run build_episode.py again)

Every cue gets a soft card swoosh (cards fly in on cues), the hook gets an ambience bed, the verdict a drum roll into the
stamp, the outro a pop on "comments". Hand-placed effects in narration.json stay; generated ones carry "auto": true
and are replaced on every run, so the script can be re-run safely.
"""
import json
import sys
from pathlib import Path

ep = Path(sys.argv[1])
nar = json.loads((ep / "narration.json").read_text())
tim = {s["id"]: s for s in json.loads((ep / "timing.json").read_text())["scenes"]}
STAMP = ("no", "yes", "tech")

for sc in nar["scenes"]:
    hand = [f for f in sc.get("sfx", []) if not f.get("auto")]
    taken = {f.get("cue") for f in hand}
    cues = tim[sc["id"]]["cues"]
    auto = []
    for name, t in cues.items():
        if name not in taken and t > 0.3:
            auto.append({"name": "swoosh", "at": round(t - 0.12, 3), "volume": 0.2, "auto": True})
    if sc["id"].startswith("s1"):
        auto.append({"name": "wind", "at": 0, "volume": 0.14, "auto": True})
        auto.append({"name": "whoosh", "at": 0.0, "volume": 0.3, "auto": True})
    if "verdict" in sc["id"]:
        st = next((cues[c] for c in STAMP if c in cues), None)
        if st and st > 2.6:
            auto.append({"name": "drumroll", "at": round(st - 2.5, 3), "volume": 0.2, "auto": True})
    if sc["id"].startswith("s8") and "c" in cues:
        auto.append({"name": "pop", "cue": "c", "volume": 0.3, "auto": True})
    sc["sfx"] = hand + auto
(ep / "narration.json").write_text(json.dumps(nar, indent=2, ensure_ascii=False))
print(ep.name, sum(len(s["sfx"]) for s in nar["scenes"]), "sfx")
