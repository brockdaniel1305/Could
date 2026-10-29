"""Write the sound effects of s5-s7 into narration.json from the same timing plan the scenes use (battle.py).

Run after build_episode.py (needs timing.json), then run build_episode.py again (the voice is cached):
    python3 src/sfx.py && python3 ../../tools/build_episode.py . --preview
"""
import json
import sys
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP.parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from battle import FK_FLIGHT, FK_KICK, MOVES, pass_times  # noqa: E402

T = {s["id"]: s for s in json.loads((EP / "timing.json").read_text())["scenes"]}


def fx(name, at, vol=0.3):
    return {"name": name, "at": round(at, 3), "volume": vol}


def s5():
    C = T["s5-dribble"]["cues"]
    out = []
    for i, tp in enumerate(pass_times()):
        out += [fx("kick", tp - 0.35, 0.3), fx("spin", tp + 0.05, 0.28), fx("dizzy" if i % 2 == 0 else "tweet", tp + 0.45, 0.22)]
        if MOVES[i] == "nutmeg":
            out.append(fx("swoosh", tp - 0.3, 0.3))
    out += [fx("swoosh", C["rate"] + 0.4 + k * 0.8, 0.18) for k in range(4)]
    out += [fx("tick", C["rate"] + 0.8 + k * 0.8, 0.3) for k in range(4)]
    out += [fx("spin", C["fall"] - 0.25, 0.3), fx("dizzy", C["fall"] + 0.1, 0.25), fx("clang", C["fall"] + 0.75, 0.25),
            fx("domino", C["fall"] + 0.55, 0.45), fx("domino", C["fall"] + 2.9, 0.4),
            fx("roar", C["into"] + 0.4, 0.3), fx("whistle", C["into"] + 0.9, 0.3), fx("impact-bass-1", C["into"] + 0.83, 0.3)]
    return out


def s6():
    C = T["s6-strike"]["cues"]
    goal = C["fk"] + FK_KICK + FK_FLIGHT
    out = [fx("stomp", 0.3 + k * 0.28, 0.14) for k in range(12)]
    out += [fx("swoosh", C["a"] - 0.15, 0.3), fx("swoosh", C["tort"] - 0.1, 0.25), fx("whoosh-short", C["legs"], 0.3),
            fx("kick", C["nut"], 0.35), fx("swoosh", C["nut"] + 0.2, 0.3), fx("impact-bass-1", C["nut"] + 0.43, 0.25),
            fx("boing", C["nut"] + 0.9, 0.3), fx("clang", C["nut"] + 1.15, 0.25), fx("clang", C["nut"] + 1.3, 0.2), fx("clang", C["nut"] + 1.45, 0.2),
            fx("whoosh", C["b"], 0.3), fx("rumble", C["wall"], 0.5), fx("stomp", C["wall"] + 0.8, 0.4),
            fx("swoosh", C["hw"] - 0.1, 0.25), fx("swoosh", C["km"] - 0.1, 0.25),
            fx("whistle", C["fk"] + 0.1, 0.28), fx("drumroll", C["fk"] + FK_KICK - 2.5, 0.22), fx("kick", C["fk"] + FK_KICK, 0.4),
            fx("swoosh", C["fk"] + FK_KICK + 0.3, 0.3), fx("net", goal, 0.45), fx("roar", goal, 0.3), fx("impact-bass-1", goal + 0.03, 0.3),
            fx("dizzy", C["long"] + 0.3, 0.22), fx("tweet", C["long"] + 0.6, 0.2)]
    return out


def s7():
    C = T["s7-end"]["cues"]
    n = C["nobody"]
    return [fx("tweet", 0.2, 0.18), fx("sting", n, 0.45), fx("clang", n + 0.65, 0.2), fx("clang", n + 0.75, 0.2), fx("clang", n + 0.85, 0.2),
            fx("swoosh", n + 1.0, 0.25), fx("impact-bass-1", n + 1.91, 0.45), fx("roar", n + 2.0, 0.3)]


if __name__ == "__main__":
    p = EP / "narration.json"
    d = json.loads(p.read_text())
    gen = {"s5-dribble": s5(), "s6-strike": s6(), "s7-end": s7()}
    for s in d["scenes"]:
        if s["id"] in gen:
            s["sfx"] = gen[s["id"]]
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False))
    print({k: len(v) for k, v in gen.items()})
