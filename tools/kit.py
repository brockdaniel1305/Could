#!/usr/bin/env python3
"""Print a cartoon part from channel/kit/parts with its ids prefixed, ready to paste into a scene.

    python3 tools/kit.py keeper s4-k            -> <g id="s4-k"> ... ids s4-k-armL ...
    python3 tools/kit.py sea-night s4-sea WL=400
    python3 tools/kit.py --list
"""
import sys
from pathlib import Path

PARTS = Path(__file__).resolve().parent.parent / "channel/kit/parts"


def part(name, pfx, **subs):
    s = (PARTS / f"{name}.svg").read_text().replace("PFX", pfx)
    for k, v in subs.items():
        s = s.replace(k, str(v))
    return s


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] == "--list":
        print("\n".join(sorted(p.stem for p in PARTS.glob("*.svg"))))
        sys.exit(0)
    subs = dict(a.split("=", 1) for a in sys.argv[3:])
    print(part(sys.argv[1], sys.argv[2], **subs))
