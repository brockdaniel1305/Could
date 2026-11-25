"""S2E14 world layer: 11 cats (purple vests, keeper green) vs 11 dogs of different breeds (orange vests, golden-retriever keeper yellow),
the referee in a mailman's kit, sleeping-cat props, the laser dot and the cardboard box.

Every animal is one sprite with two views (engine picks by direction, see tools/world3d/engine.js):
  .v-side  side view facing RIGHT, legs in .legA/.legB (swing about their top)
  .v-front cats: sitting, facing the camera (paws = -armL/-armR, pupils, mouth m-smile/m-o); dogs: standing head-on
Origin = on the ground under the animal. Drawn at P px per metre; the actor's h (m) and unit (px) come from META below."""
import json
import math
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

INK = "#1a1a2e"
P = 500                     # px per metre
CATV, CATK, DOGV, DOGK = "#7b3fe4", "#1f9d55", "#ff7a1a", "#ffd23f"   # vests: cats, cat keeper, dogs, dog keeper
META = {}                   # name -> {h (m), unit (px)}


def _e(cx, cy, rx, ry, fill, sw=5, extra=""):
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" {extra}/>'


def _vest(uid, cx, cy, rx, ry, x0, x1, color, num, numc="#fff", fs=None, ty=0):
    """team vest: a band over the body ellipse, clipped to it, with the shirt number"""
    fs = fs or ry * 0.95
    return (f'<clipPath id="{uid}"><ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx - 2.5:.1f}" ry="{ry - 2.5:.1f}"/></clipPath>'
            f'<g clip-path="url(#{uid})"><rect x="{x0:.1f}" y="{cy - ry - 5:.1f}" width="{x1 - x0:.1f}" height="{2 * ry + 10:.1f}" fill="{color}"/>'
            f'<rect x="{x0:.1f}" y="{cy - ry - 5:.1f}" width="6" height="{2 * ry + 10:.1f}" fill="#fff" opacity="0.35"/>'
            f'<text class="num" x="{(x0 + x1) / 2:.1f}" y="{cy + ty + fs * 0.36:.1f}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="{fs:.0f}" '
            f'fill="{numc}" stroke="{INK}" stroke-width="{fs * 0.06:.1f}" paint-order="stroke">{num}</text></g>'
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{INK}" stroke-width="5"/>')


# ---------------------------------------------------------------- dogs ----------------------------------------------------------------
BREEDS = {   # leg length, body rx/ry, head r, snout length, ears, tail, colours (coat, dark/far, belly/muzzle, ear)
    "retriever": dict(leg=118, rx=112, ry=50, hr=44, sn=40, ear="flop", tail="feather", c="#e3a857", d="#c98d3f", m="#f1c98a", ec="#c98d3f"),
    "greyhound": dict(leg=168, rx=104, ry=40, hr=34, sn=52, ear="fold", tail="thin", c="#9aa3ad", d="#7d8792", m="#c6ccd3", ec="#7d8792"),
    "dachshund": dict(leg=36, rx=122, ry=36, hr=38, sn=42, ear="long", tail="thin", c="#8b4a2b", d="#6e3820", m="#b46a43", ec="#5e2f1a"),
    "husky": dict(leg=112, rx=106, ry=48, hr=42, sn=34, ear="point", tail="curl", c="#7b8794", d="#5f6a76", m="#f4f4f2", ec="#5f6a76"),
    "pug": dict(leg=52, rx=70, ry=42, hr=42, sn=10, ear="tiny", tail="curl", c="#d9b98a", d="#bf9d6c", m="#2b2522", ec="#2b2522"),
    "corgi": dict(leg=40, rx=96, ry=40, hr=40, sn=30, ear="big", tail="stub", c="#d9893d", d="#b96f2b", m="#f4f4f2", ec="#b96f2b"),
    "dalmatian": dict(leg=120, rx=104, ry=44, hr=40, sn=40, ear="flop", tail="thin", c="#f4f4f2", d="#dcdcd8", m="#f4f4f2", ec="#2b2522", spots=True),
    "beagle": dict(leg=78, rx=92, ry=42, hr=40, sn=34, ear="flop", tail="thin", c="#c47a3a", d="#a5612b", m="#f4f4f2", ec="#8a4f22", saddle="#2b2522"),
    "poodle": dict(leg=112, rx=88, ry=44, hr=40, sn=36, ear="fluff", tail="puff", c="#f2efe9", d="#d9d4cb", m="#f2efe9", ec="#e6e1d8"),
    "labrador": dict(leg=112, rx=108, ry=48, hr=42, sn=40, ear="flop", tail="thin", c="#3a312c", d="#2b2522", m="#4a3f39", ec="#2b2522"),
    "collie": dict(leg=104, rx=100, ry=44, hr=40, sn=38, ear="semi", tail="feather", c="#2b2522", d="#1c1714", m="#f4f4f2", ec="#1c1714", saddle=None),
}


def dog(name, breed, num, vest, numc=INK, view_front_tongue=True):
    b = BREEDS[breed]
    leg, rx, ry, hr, sn = b["leg"], b["rx"], b["ry"], b["hr"], b["sn"]
    by = -(leg + ry * 0.55)                          # body centre
    hx, hy = rx * 0.92, by - ry - hr * 0.55          # head centre (side)
    uid = f"{name}"
    # ---------- side view (facing right) ----------
    s = []
    lw = max(18, min(26, leg * 0.2)) if breed != "greyhound" else 17
    def legs(x, col, cls):
        return (f'<g class="{cls}"><rect x="{x - lw / 2:.1f}" y="{by + ry * 0.1:.1f}" width="{lw:.1f}" height="{-by - ry * 0.1:.1f}" rx="{lw / 2:.1f}" '
                f'fill="{col}" stroke="{INK}" stroke-width="5"/><ellipse cx="{x + lw * 0.25:.1f}" cy="-6" rx="{lw * 0.75:.1f}" ry="9" fill="{col}" stroke="{INK}" stroke-width="5"/></g>')
    fx, bx = rx * 0.58, -rx * 0.62
    s.append(legs(fx - lw * 1.1, b["d"], "legB")); s.append(legs(bx - lw * 1.1, b["d"], "legA"))      # far legs
    # tail (behind body)
    tx, ty = -rx * 0.92, by - ry * 0.35
    t = b["tail"]
    if t == "feather":
        s.append(f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 60:.0f},{ty - 10:.0f} {tx - 78:.0f},{ty + 50:.0f}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
                 f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 60:.0f},{ty - 10:.0f} {tx - 78:.0f},{ty + 50:.0f}" fill="none" stroke="{b["c"]}" stroke-width="20" stroke-linecap="round"/>')
    elif t == "thin":
        s.append(f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 50:.0f},{ty - 40:.0f} {tx - 62:.0f},{ty - 92:.0f}" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
                 f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 50:.0f},{ty - 40:.0f} {tx - 62:.0f},{ty - 92:.0f}" fill="none" stroke="{b["c"]}" stroke-width="7" stroke-linecap="round"/>')
    elif t == "curl":
        s.append(f'<circle cx="{tx - 8:.0f}" cy="{by - ry - 6:.0f}" r="20" fill="none" stroke="{INK}" stroke-width="20"/>'
                 f'<circle cx="{tx - 8:.0f}" cy="{by - ry - 6:.0f}" r="20" fill="none" stroke="{b["c"]}" stroke-width="10"/>')
    elif t == "stub":
        s.append(_e(tx - 6, ty - 4, 16, 12, b["c"]))
    elif t == "puff":
        s.append(f'<path d="M{tx:.0f},{ty:.0f} L{tx - 30:.0f},{ty - 50:.0f}" stroke="{INK}" stroke-width="14"/>' + _e(tx - 34, ty - 62, 22, 22, b["c"]))
    # body
    s.append(_e(0, by, rx, ry, b["c"]))
    if b.get("saddle"):
        s.append(f'<clipPath id="{uid}-sc"><ellipse cx="0" cy="{by:.1f}" rx="{rx - 3:.1f}" ry="{ry - 3:.1f}"/></clipPath>'
                 f'<path d="M{-rx:.0f},{by - ry * 0.1:.0f} Q0,{by - ry * 0.5:.0f} {rx * 0.6:.0f},{by - ry * 0.2:.0f} L{rx * 0.6:.0f},{by - ry - 5:.0f} L{-rx:.0f},{by - ry - 5:.0f} Z" fill="{b["saddle"]}" clip-path="url(#{uid}-sc)"/>')
    if breed == "husky" or breed == "collie" or breed == "corgi" or breed == "beagle":
        s.append(f'<clipPath id="{uid}-bc"><ellipse cx="0" cy="{by:.1f}" rx="{rx - 3:.1f}" ry="{ry - 3:.1f}"/></clipPath>'
                 f'<ellipse cx="{rx * 0.1:.0f}" cy="{by + ry * 0.85:.0f}" rx="{rx * 0.8:.0f}" ry="{ry * 0.5:.0f}" fill="{b["m"]}" clip-path="url(#{uid}-bc)"/>')
    s.append(_vest(uid + "-vs", 0, by, rx, ry, -rx * 0.42, rx * 0.5, vest, num, numc))
    if b.get("spots"):
        for (px, py, r) in ((-rx * 0.7, by - 8, 9), (-rx * 0.55, by + 18, 7), (rx * 0.62, by + 10, 8), (rx * 0.7, by - 18, 6)):
            s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="#2b2522"/>')
    if breed == "poodle":
        for (px, py) in ((-rx * 0.85, by + 4), (rx * 0.85, by - 6)):
            s.append(_e(px, py, 26, 30, b["c"]))
    s.append(legs(fx, b["c"], "legA")); s.append(legs(bx, b["c"], "legB"))                              # near legs
    # neck + head
    s.append(f'<path d="M{rx * 0.55:.0f},{by - ry * 0.5:.0f} L{hx - hr * 0.5:.0f},{hy:.0f} L{hx + hr * 0.4:.0f},{hy + hr * 0.6:.0f} L{rx * 0.95:.0f},{by + ry * 0.1:.0f} Z" '
             f'fill="{b["c"]}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if b["ear"] in ("point", "big", "semi"):
        eh = hr * (1.3 if b["ear"] == "big" else 0.95)
        tip = f"{hx - hr * 0.35:.0f},{hy - hr - eh * 0.75:.0f}" if b["ear"] != "semi" else f"{hx - hr * 0.6:.0f},{hy - hr - eh * 0.35:.0f}"
        s.append(f'<path d="M{hx - hr * 0.8:.0f},{hy - hr * 0.5:.0f} L{tip} L{hx + hr * 0.05:.0f},{hy - hr * 0.8:.0f} Z" fill="{b["ec"]}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    s.append(_e(hx, hy, hr, hr * 0.92, b["c"]))
    if breed == "husky":
        s.append(f'<path d="M{hx - hr * 0.2:.0f},{hy - hr * 0.1:.0f} Q{hx + hr * 0.6:.0f},{hy - hr * 0.5:.0f} {hx + hr * 0.95:.0f},{hy + hr * 0.3:.0f} L{hx:.0f},{hy + hr * 0.8:.0f} Z" fill="#f4f4f2"/>')
    if breed == "collie":
        s.append(f'<path d="M{hx + hr * 0.05:.0f},{hy - hr * 0.9:.0f} L{hx + hr * 0.3:.0f},{hy + hr * 0.3:.0f} L{hx + hr * 0.95:.0f},{hy + hr * 0.4:.0f} L{hx + hr * 0.6:.0f},{hy - hr * 0.6:.0f} Z" fill="#f4f4f2"/>')
    # snout
    if sn > 12:
        s.append(_e(hx + hr * 0.62 + sn * 0.45, hy + hr * 0.28, sn * 0.7 + 8, hr * 0.42, b["m"] if breed in ("husky", "collie", "corgi", "beagle") else b["c"]))
        nx = hx + hr * 0.62 + sn * 1.1
    else:  # pug: flat dark face
        s.append(_e(hx + hr * 0.62, hy + hr * 0.18, hr * 0.42, hr * 0.5, b["m"]))
        nx = hx + hr * 0.95
    s.append(f'<ellipse cx="{nx:.0f}" cy="{hy + hr * 0.12:.0f}" rx="9" ry="7" fill="{INK}"/>')
    s.append(f'<path d="M{nx - 14:.0f},{hy + hr * 0.5:.0f} q-14,6 -26,0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<path d="M{nx - 22:.0f},{hy + hr * 0.52:.0f} q4,22 14,20 q8,-2 4,-18" fill="#e8587a" stroke="{INK}" stroke-width="3.5"/>')   # tongue
    s.append(f'<circle cx="{hx + hr * 0.3:.0f}" cy="{hy - hr * 0.22:.0f}" r="{hr * 0.2:.1f}" fill="#fff" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="{hx + hr * 0.36:.0f}" cy="{hy - hr * 0.2:.0f}" r="{hr * 0.11:.1f}" fill="{INK}"/>')
    if b["ear"] in ("flop", "long", "fluff", "tiny", "fold"):
        el = {"flop": hr * 1.05, "long": hr * 1.4, "fluff": hr * 1.1, "tiny": hr * 0.45, "fold": hr * 0.5}[b["ear"]]
        if b["ear"] == "fluff":
            s.append(_e(hx - hr * 0.35, hy + el * 0.25, hr * 0.42, el * 0.6, b["ec"]))
        else:
            s.append(f'<path d="M{hx - hr * 0.55:.0f},{hy - hr * 0.75:.0f} Q{hx - hr * 0.05:.0f},{hy - hr * 0.8:.0f} {hx - hr * 0.1:.0f},{hy - hr * 0.3:.0f} '
                     f'Q{hx - hr * 0.2:.0f},{hy - hr * 0.6 + el:.0f} {hx - hr * 0.55:.0f},{hy - hr * 0.6 + el:.0f} Q{hx - hr * 0.95:.0f},{hy - hr * 0.6 + el * 0.6:.0f} {hx - hr * 0.55:.0f},{hy - hr * 0.75:.0f} Z" '
                     f'fill="{b["ec"]}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if breed == "poodle":
        s.append(_e(hx - hr * 0.1, hy - hr * 0.85, hr * 0.65, hr * 0.45, b["c"]))
    top = min(hy - hr - (hr * 0.95 * 0.75 if b["ear"] in ("point", "big") else 0), by - ry)
    # ---------- front view (standing head-on) ----------
    f = []
    cw = ry * 1.05 + 8                               # chest half-width
    for x, cls in ((-cw * 0.5, "legA"), (cw * 0.5, "legB")):
        f.append(f'<g class="{cls}"><rect x="{x - lw / 2:.1f}" y="{by:.1f}" width="{lw:.1f}" height="{-by:.1f}" rx="{lw / 2:.1f}" fill="{b["c"]}" stroke="{INK}" stroke-width="5"/>'
                 f'<ellipse cx="{x:.1f}" cy="-6" rx="{lw * 0.8:.1f}" ry="9" fill="{b["c"]}" stroke="{INK}" stroke-width="5"/></g>')
    f.append(_e(0, by, cw, ry * 1.15, b["c"]))
    f.append(_vest(uid + "-vf", 0, by, cw, ry * 1.15, -cw, cw, vest, num, numc, fs=ry * 1.0))
    fhy = hy + hr * 0.1
    if b["ear"] in ("point", "big", "semi"):
        eh = hr * (1.35 if b["ear"] == "big" else 1.0)
        for sgn in (-1, 1):
            tipy = fhy - hr - eh * (0.75 if b["ear"] != "semi" else 0.3)
            f.append(f'<path d="M{sgn * hr * 0.25:.0f},{fhy - hr * 0.8:.0f} L{sgn * hr * 0.75:.0f},{tipy:.0f} L{sgn * hr * 0.95:.0f},{fhy - hr * 0.25:.0f} Z" fill="{b["ec"]}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    f.append(_e(0, fhy, hr * 1.08, hr, b["c"]))
    if breed == "husky":
        f.append(f'<path d="M0,{fhy - hr * 0.55:.0f} Q{-hr * 0.9:.0f},{fhy - hr * 0.2:.0f} {-hr * 0.7:.0f},{fhy + hr * 0.6:.0f} L{hr * 0.7:.0f},{fhy + hr * 0.6:.0f} Q{hr * 0.9:.0f},{fhy - hr * 0.2:.0f} 0,{fhy - hr * 0.55:.0f} Z" fill="#f4f4f2"/>')
    if breed == "collie":
        f.append(f'<path d="M-10,{fhy - hr:.0f} L10,{fhy - hr:.0f} L{hr * 0.45:.0f},{fhy + hr * 0.7:.0f} L{-hr * 0.45:.0f},{fhy + hr * 0.7:.0f} Z" fill="#f4f4f2"/>')
    if b.get("spots"):
        f.append(f'<circle cx="{-hr * 0.55:.0f}" cy="{fhy - hr * 0.45:.0f}" r="8" fill="#2b2522"/><circle cx="{hr * 0.6:.0f}" cy="{fhy + hr * 0.1:.0f}" r="6" fill="#2b2522"/>')
    # eyes + pupils
    for sgn, pid in ((-1, "pupL"), (1, "pupR")):
        f.append(f'<circle cx="{sgn * hr * 0.4:.0f}" cy="{fhy - hr * 0.2:.0f}" r="{hr * 0.22:.1f}" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
                 f'<g id="w3-{name}x-{pid}"><circle cx="{sgn * hr * 0.4:.0f}" cy="{fhy - hr * 0.17:.0f}" r="{hr * 0.12:.1f}" fill="{INK}"/></g>')
    # muzzle, nose, mouth
    mz = b["m"]
    f.append(_e(0, fhy + hr * 0.38, hr * 0.55, hr * 0.42, mz, 4))
    f.append(f'<ellipse cx="0" cy="{fhy + hr * 0.18:.0f}" rx="{hr * 0.2:.1f}" ry="{hr * 0.14:.1f}" fill="{INK}"/>')
    f.append(f'<g id="w3-{name}x-m-smile"><path d="M{-hr * 0.28:.0f},{fhy + hr * 0.5:.0f} Q0,{fhy + hr * 0.7:.0f} {hr * 0.28:.0f},{fhy + hr * 0.5:.0f}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
             f'<path d="M-9,{fhy + hr * 0.6:.0f} q0,{hr * 0.45:.0f} 9,{hr * 0.45:.0f} q9,0 9,{-hr * 0.45:.0f} Z" fill="#e8587a" stroke="{INK}" stroke-width="3"/></g>')
    f.append(f'<g id="w3-{name}x-m-o" opacity="0"><ellipse cx="0" cy="{fhy + hr * 0.62:.0f}" rx="{hr * 0.3:.1f}" ry="{hr * 0.26:.1f}" fill="#5a1626" stroke="{INK}" stroke-width="4"/>'
             f'<ellipse cx="0" cy="{fhy + hr * 0.75:.0f}" rx="{hr * 0.18:.1f}" ry="{hr * 0.1:.1f}" fill="#e8587a"/></g>')
    if b["ear"] in ("flop", "long", "fluff", "tiny", "fold"):
        el = {"flop": hr * 1.1, "long": hr * 1.4, "fluff": hr * 1.1, "tiny": hr * 0.5, "fold": hr * 0.55}[b["ear"]]
        for sgn in (-1, 1):
            if b["ear"] == "fluff":
                f.append(_e(sgn * hr * 1.05, fhy + hr * 0.1, hr * 0.4, el * 0.6, b["ec"]))
            else:
                f.append(f'<path d="M{sgn * hr * 0.6:.0f},{fhy - hr * 0.85:.0f} Q{sgn * hr * 1.35:.0f},{fhy - hr * 0.8:.0f} {sgn * hr * 1.3:.0f},{fhy - hr * 0.55 + el:.0f} '
                         f'Q{sgn * hr * 1.0:.0f},{fhy - hr * 0.4 + el:.0f} {sgn * hr * 0.85:.0f},{fhy - hr * 0.3:.0f} Z" fill="{b["ec"]}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if breed == "poodle":
        f.append(_e(0, fhy - hr * 0.9, hr * 0.75, hr * 0.45, b["c"]))
    hpx = -top + 4
    META[name] = dict(h=round(hpx / P, 3), unit=round(hpx))
    inner = (f'<ellipse cx="0" cy="4" rx="{rx * 0.95:.0f}" ry="14" fill="#000" opacity="0.32"/>'
             f'<g id="w3-{name}x"><g class="v-side">{"".join(s)}</g><g class="v-front" style="display:none">{"".join(f)}</g></g>')
    W = int(2 * (rx + hr * 2 + sn + 120)); H = int(hpx + 140)
    return sprite(name, inner, W, H, int(hpx + 70))


# ---------------------------------------------------------------- cats ----------------------------------------------------------------
CATS = [   # coat, dark (stripes/patches/far legs), belly/face, eye colour, pattern
    dict(c="#9aa0a8", d="#7f8690", m="#e9e9e6", eye="#7ec85a", pat="persian"),     # 0 keeper: fluffy grey persian
    dict(c="#2b2522", d="#1c1714", m="#3a322e", eye="#f2c94c", pat=None),          # 1 black
    dict(c="#9aa3ad", d="#7d8792", m="#c6ccd3", eye="#f2c94c", pat=None),          # 2 grey
    dict(c="#f4f1ea", d="#dcd7cc", m="#ffffff", eye="#6fb7e8", pat=None),          # 3 white
    dict(c="#f4f1ea", d="#d9893d", m="#ffffff", eye="#7ec85a", pat="calico"),      # 4 calico
    dict(c="#eadbc2", d="#5a4236", m="#f4ead9", eye="#5aa2e8", pat="siamese"),     # 5 siamese
    dict(c="#2b2522", d="#1c1714", m="#f4f4f2", eye="#7ec85a", pat="tux"),         # 6 tuxedo
    dict(c="#8a6a4f", d="#5c4535", m="#c9ad8f", eye="#7ec85a", pat="tabby"),       # 7 brown tabby
    dict(c="#e89a4c", d="#c4702a", m="#ffffff", eye="#7ec85a", pat="gingerwhite"), # 8 ginger & white
    dict(c="#a3a8ae", d="#6c737b", m="#d4d7da", eye="#f2c94c", pat="tabby"),       # 9 grey tabby
    dict(c="#e89a4c", d="#c4702a", m="#f6cf9e", eye="#7ec85a", pat="tabby"),       # 10 orange tabby (the ball pusher)
]


def cat(name, k, num, vest):
    cc = CATS[k]
    c, d, m, eye, pat = cc["c"], cc["d"], cc["m"], cc["eye"], cc["pat"]
    fluffy = pat == "persian"
    leg, rx, ry, hr = 76, 92 if not fluffy else 98, 40 if not fluffy else 46, 42 if not fluffy else 46
    by = -(leg + ry * 0.55)
    hx, hy = rx * 0.95, by - ry - hr * 0.6
    s = []
    lw = 20

    def legs(x, col, cls):
        return (f'<g class="{cls}"><rect x="{x - lw / 2:.1f}" y="{by + ry * 0.1:.1f}" width="{lw}" height="{-by - ry * 0.1:.1f}" rx="10" fill="{col}" stroke="{INK}" stroke-width="5"/>'
                f'<ellipse cx="{x + 4:.1f}" cy="-6" rx="15" ry="8" fill="{col if pat not in ("tux", "gingerwhite") else "#f4f4f2"}" stroke="{INK}" stroke-width="5"/></g>')
    fx, bx = rx * 0.55, -rx * 0.6
    s.append(legs(fx - 22, d, "legB")); s.append(legs(bx - 22, d, "legA"))
    # tail: long, curving up
    tx, ty = -rx * 0.92, by - ry * 0.2
    tw = 18 if not fluffy else 30
    tcol = d if pat == "siamese" else c
    s.append(f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 75:.0f},{ty + 10:.0f} {tx - 70:.0f},{ty - 80:.0f} Q{tx - 64:.0f},{ty - 130:.0f} {tx - 30:.0f},{ty - 132:.0f}" fill="none" stroke="{INK}" stroke-width="{tw + 10}" stroke-linecap="round"/>'
             f'<path d="M{tx:.0f},{ty:.0f} Q{tx - 75:.0f},{ty + 10:.0f} {tx - 70:.0f},{ty - 80:.0f} Q{tx - 64:.0f},{ty - 130:.0f} {tx - 30:.0f},{ty - 132:.0f}" fill="none" stroke="{tcol}" stroke-width="{tw}" stroke-linecap="round"/>')
    s.append(_e(0, by, rx, ry, c))
    if pat in ("tabby",):
        for xx in (-rx * 0.75, -rx * 0.62):
            s.append(f'<path d="M{xx:.0f},{by - ry * 0.9:.0f} q8,{ry * 0.6:.0f} -2,{ry * 1.1:.0f}" fill="none" stroke="{d}" stroke-width="8" stroke-linecap="round"/>')
    if pat == "calico":
        s.append(f'<circle cx="{-rx * 0.62:.0f}" cy="{by - 10:.0f}" r="20" fill="#d9893d"/><circle cx="{-rx * 0.7:.0f}" cy="{by + 14:.0f}" r="13" fill="#2b2522"/>')
    if pat in ("tux", "gingerwhite"):
        s.append(f'<clipPath id="{name}-bc"><ellipse cx="0" cy="{by:.1f}" rx="{rx - 3:.1f}" ry="{ry - 3:.1f}"/></clipPath>'
                 f'<ellipse cx="{rx * 0.2:.0f}" cy="{by + ry * 0.9:.0f}" rx="{rx * 0.8:.0f}" ry="{ry * 0.5:.0f}" fill="#f4f4f2" clip-path="url(#{name}-bc)"/>')
    s.append(_vest(name + "-vs", 0, by, rx, ry, -rx * 0.4, rx * 0.5, vest, num, "#fff"))
    s.append(legs(fx, c, "legA")); s.append(legs(bx, c, "legB"))
    # neck + head
    s.append(f'<path d="M{rx * 0.5:.0f},{by - ry * 0.6:.0f} L{hx - hr * 0.6:.0f},{hy:.0f} L{hx + hr * 0.3:.0f},{hy + hr * 0.6:.0f} L{rx * 0.95:.0f},{by + ry * 0.1:.0f} Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    ecol = d if pat == "siamese" else c
    s.append(f'<path d="M{hx - hr * 0.75:.0f},{hy - hr * 0.45:.0f} L{hx - hr * 0.55:.0f},{hy - hr * 1.55:.0f} L{hx - hr * 0.05:.0f},{hy - hr * 0.85:.0f} Z" fill="{ecol}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M{hx - hr * 0.05:.0f},{hy - hr * 0.8:.0f} L{hx + hr * 0.3:.0f},{hy - hr * 1.6:.0f} L{hx + hr * 0.6:.0f},{hy - hr * 0.6:.0f} Z" fill="{ecol}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    s.append(_e(hx, hy, hr * (1.05 if fluffy else 1), hr * 0.92, c))
    if pat == "siamese":
        s.append(_e(hx + hr * 0.6, hy + hr * 0.2, hr * 0.45, hr * 0.4, d, 0))
    if pat in ("tux", "gingerwhite"):
        s.append(_e(hx + hr * 0.6, hy + hr * 0.35, hr * 0.42, hr * 0.38, "#f4f4f2", 0))
    if pat == "tabby":
        s.append(f'<path d="M{hx - hr * 0.2:.0f},{hy - hr * 0.85:.0f} l6,18 M{hx + hr * 0.1:.0f},{hy - hr * 0.88:.0f} l2,18" stroke="{d}" stroke-width="6" stroke-linecap="round"/>')
    # eye (almond, side), nose, mouth, whiskers
    s.append(f'<ellipse cx="{hx + hr * 0.45:.0f}" cy="{hy - hr * 0.15:.0f}" rx="{hr * 0.2:.1f}" ry="{hr * 0.16:.1f}" fill="{eye}" stroke="{INK}" stroke-width="3"/>'
             f'<ellipse cx="{hx + hr * 0.5:.0f}" cy="{hy - hr * 0.15:.0f}" rx="{hr * 0.05:.1f}" ry="{hr * 0.14:.1f}" fill="{INK}"/>')
    nx = hx + hr * 0.98
    s.append(f'<path d="M{nx - 8:.0f},{hy + hr * 0.12:.0f} l8,-2 l-3,8 z" fill="#e88a9a" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<path d="M{nx - 4:.0f},{hy + hr * 0.3:.0f} q-8,8 -16,2" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<path d="M{nx - 14:.0f},{hy + hr * 0.25:.0f} l40,-6 M{nx - 14:.0f},{hy + hr * 0.32:.0f} l40,6" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>')
    if fluffy:
        s.append(f'<path d="M{hx - hr:.0f},{hy + hr * 0.3:.0f} q-10,22 10,30 q-4,16 16,16 q4,14 22,6" fill="{c}" stroke="{INK}" stroke-width="4"/>')
    top_side = hy - hr * 1.6
    # ---------- front view: sitting, facing the camera ----------
    f = []
    sy = -88                                         # sitting body centre
    srx, sry = (74, 92) if not fluffy else (84, 96)
    # tail curled round the front right
    f.append(f'<path d="M{srx * 0.75:.0f},-12 Q{srx * 1.35:.0f},-4 {srx * 1.25:.0f},-70" fill="none" stroke="{INK}" stroke-width="{tw + 10}" stroke-linecap="round"/>'
             f'<path d="M{srx * 0.75:.0f},-12 Q{srx * 1.35:.0f},-4 {srx * 1.25:.0f},-70" fill="none" stroke="{tcol}" stroke-width="{tw}" stroke-linecap="round"/>')
    f.append(_e(-srx * 0.6, -36, srx * 0.5, 38, c)); f.append(_e(srx * 0.6, -36, srx * 0.5, 38, c))          # haunches
    f.append(_e(0, sy, srx, sry, c))
    if pat in ("tux", "gingerwhite"):
        f.append(_e(0, sy + 10, srx * 0.55, sry * 0.8, "#f4f4f2", 0))
    if pat == "calico":
        f.append(f'<circle cx="{-srx * 0.55:.0f}" cy="{sy - 20:.0f}" r="22" fill="#d9893d"/><circle cx="{srx * 0.6:.0f}" cy="{sy + 30:.0f}" r="16" fill="#2b2522"/>')
    f.append(_vest(name + "-vf", 0, sy, srx, sry, -srx, srx, vest, num, "#fff", fs=54, ty=-sry * 0.42))
    # paws (rig arms: rotate about their top)
    pcol = "#f4f4f2" if pat in ("tux", "gingerwhite") else (d if pat == "siamese" else c)
    for sgn, aid in ((-1, "armL"), (1, "armR")):
        f.append(f'<g id="w3-{name}x-{aid}"><rect x="{sgn * 24 - 12:.0f}" y="-100" width="24" height="96" rx="12" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                 f'<ellipse cx="{sgn * 24:.0f}" cy="-8" rx="17" ry="11" fill="{pcol}" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M{sgn * 24 - 6:.0f},-14 l0,8 M{sgn * 24 + 6:.0f},-14 l0,8" stroke="{INK}" stroke-width="2.5"/></g>')
    fhy = sy - sry - hr * 0.75
    fhr = hr * 1.25
    for sgn in (-1, 1):
        f.append(f'<path d="M{sgn * fhr * 0.2:.0f},{fhy - fhr * 0.85:.0f} L{sgn * fhr * 0.75:.0f},{fhy - fhr * 1.55:.0f} L{sgn * fhr * 0.95:.0f},{fhy - fhr * 0.35:.0f} Z" fill="{ecol}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                 f'<path d="M{sgn * fhr * 0.45:.0f},{fhy - fhr * 0.85:.0f} L{sgn * fhr * 0.72:.0f},{fhy - fhr * 1.3:.0f} L{sgn * fhr * 0.8:.0f},{fhy - fhr * 0.65:.0f} Z" fill="#e88a9a"/>')
    f.append(_e(0, fhy, fhr * (1.12 if fluffy else 1.05), fhr * 0.9, c))
    if pat == "siamese":
        f.append(_e(0, fhy + fhr * 0.25, fhr * 0.55, fhr * 0.5, d, 0))
    if pat in ("tux", "gingerwhite"):
        f.append(f'<path d="M0,{fhy - fhr * 0.3:.0f} L{fhr * 0.5:.0f},{fhy + fhr * 0.8:.0f} L{-fhr * 0.5:.0f},{fhy + fhr * 0.8:.0f} Z" fill="#f4f4f2"/>')
    if pat == "tabby":
        f.append(f'<path d="M{-fhr * 0.25:.0f},{fhy - fhr * 0.85:.0f} l4,22 M0,{fhy - fhr * 0.9:.0f} l0,24 M{fhr * 0.25:.0f},{fhy - fhr * 0.85:.0f} l-4,22" stroke="{d}" stroke-width="7" stroke-linecap="round"/>')
    # eyes (half-closed lids = bored), pupils as slits
    for sgn, pid in ((-1, "pupL"), (1, "pupR")):
        ex, ey = sgn * fhr * 0.42, fhy - fhr * 0.08
        f.append(f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{fhr * 0.24:.1f}" ry="{fhr * 0.2:.1f}" fill="{eye}" stroke="{INK}" stroke-width="3.5"/>'
                 f'<g id="w3-{name}x-{pid}"><ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{fhr * 0.06:.1f}" ry="{fhr * 0.17:.1f}" fill="{INK}"/></g>'
                 f'<path d="M{ex - fhr * 0.26:.0f},{ey - fhr * 0.02:.0f} Q{ex:.0f},{ey - fhr * 0.26:.0f} {ex + fhr * 0.26:.0f},{ey - fhr * 0.02:.0f} L{ex + fhr * 0.26:.0f},{ey - fhr * 0.24:.0f} L{ex - fhr * 0.26:.0f},{ey - fhr * 0.24:.0f} Z" fill="{c if pat != "siamese" else d}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    f.append(f'<path d="M-9,{fhy + fhr * 0.2:.0f} l18,0 l-9,10 z" fill="#e88a9a" stroke="{INK}" stroke-width="3"/>')
    f.append(f'<g id="w3-{name}x-m-smile"><path d="M0,{fhy + fhr * 0.32:.0f} q-10,12 -20,4 M0,{fhy + fhr * 0.32:.0f} q10,12 20,4" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/></g>')
    f.append(f'<g id="w3-{name}x-m-o" opacity="0"><ellipse cx="0" cy="{fhy + fhr * 0.45:.0f}" rx="{fhr * 0.2:.1f}" ry="{fhr * 0.22:.1f}" fill="#5a1626" stroke="{INK}" stroke-width="3.5"/></g>')
    for sgn in (-1, 1):
        f.append(f'<path d="M{sgn * 26:.0f},{fhy + fhr * 0.3:.0f} l{sgn * 58:.0f},-10 M{sgn * 26:.0f},{fhy + fhr * 0.38:.0f} l{sgn * 58:.0f},6" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>')
    if fluffy:
        f.append(f'<path d="M{-fhr * 1.0:.0f},{fhy + fhr * 0.3:.0f} q-14,18 0,30 q-4,16 18,18 M{fhr * 1.0:.0f},{fhy + fhr * 0.3:.0f} q14,18 0,30 q4,16 -18,18" fill="none" stroke="{INK}" stroke-width="4"/>')
    top_front = fhy - fhr * 1.55
    hpx = -min(top_side, top_front) + 4
    META[name] = dict(h=round(hpx / P, 3), unit=round(hpx))
    inner = (f'<ellipse cx="0" cy="4" rx="80" ry="13" fill="#000" opacity="0.32"/>'
             f'<g id="w3-{name}x"><g class="v-side">{"".join(s)}</g><g class="v-front" style="display:none">{"".join(f)}</g></g>')
    return sprite(name, inner, 640, int(hpx + 140), int(hpx + 70))


# ---------------------------------------------------------------- props ----------------------------------------------------------------
def sleeping_cat(k):
    """curled-up cat (loaf), eyes shut, origin on the ground, ~120 tall"""
    cc = CATS[k]; c, d = cc["c"], cc["d"]
    return (f'<ellipse cx="0" cy="4" rx="96" ry="12" fill="#000" opacity="0.3"/>'
            f'<path d="M-70,-20 Q-118,-10 -96,24" fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round"/>'
            f'<path d="M-70,-20 Q-118,-10 -96,24" fill="none" stroke="{c}" stroke-width="18" stroke-linecap="round"/>'
            + _e(0, -46, 92, 48, c) + _vest(f"sl{k}", 0, -46, 92, 48, -40, 40, CATV, "", "#fff")
            + f'<path d="M30,-70 L44,-124 L70,-84 Z M70,-84 L98,-120 L104,-66 Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            + _e(66, -56, 48, 40, c)
            + f'<path d="M44,-58 q10,8 20,0 M78,-58 q10,8 20,0" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M66,-42 l8,0 l-4,5 z" fill="#e88a9a"/>'
            f'<path d="M-40,-2 Q20,10 90,-14" fill="none" stroke="{d}" stroke-width="8" stroke-linecap="round" opacity="0.6"/>'
            f'<text x="120" y="-120" font-family="Inter" font-weight="900" font-size="46" fill="#f4efe6" stroke="{INK}" stroke-width="3" paint-order="stroke">Z</text>'
            f'<text x="160" y="-170" font-family="Inter" font-weight="900" font-size="32" fill="#f4efe6" stroke="{INK}" stroke-width="3" paint-order="stroke">z</text>')


BOX = (f'<ellipse cx="0" cy="4" rx="130" ry="14" fill="#000" opacity="0.3"/>'
       f'<path d="M-110,-150 L-150,-196 L-40,-190 L-20,-150 Z" fill="#b98a52" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
       f'<path d="M110,-150 L150,-196 L40,-190 L20,-150 Z" fill="#b98a52" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
       f'<rect x="-120" y="-150" width="240" height="150" fill="#c99a5e" stroke="{INK}" stroke-width="6"/>'
       f'<rect x="-30" y="-150" width="60" height="150" fill="#d8b07a" opacity="0.6"/>'
       f'<text x="0" y="-60" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#6b4a24" opacity="0.8">THIS SIDE UP</text>')


def box_full():
    """the box with five cats inside: ears and tails sticking out"""
    bits = []
    for k, (x, col) in enumerate(((-80, CATS[1]["c"]), (-30, CATS[4]["d"]), (20, CATS[7]["c"]), (70, CATS[3]["c"]))):
        bits.append(f'<path d="M{x - 22},-150 L{x - 14},-196 L{x + 2},-152 Z M{x + 4},-152 L{x + 18},-198 L{x + 26},-150 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    for x, col, bend in ((-60, CATS[2]["c"], -1), (40, CATS[10]["c"], 1), (95, CATS[8]["c"], 1)):
        bits.append(f'<path d="M{x},-150 Q{x + bend * 40},-210 {x + bend * 10},-250" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>'
                    f'<path d="M{x},-150 Q{x + bend * 40},-210 {x + bend * 10},-250" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round"/>')
    return BOX.replace('<rect x="-120"', "".join(bits) + '<rect x="-120"', 1)


LASER = ('<circle cx="0" cy="-6" r="34" fill="#ff2a2a" opacity="0.25"/><circle cx="0" cy="-6" r="18" fill="#ff2a2a" opacity="0.55"/>'
         '<circle cx="0" cy="-6" r="9" fill="#ffe0e0"/>')

# mailman referee: blue kit + cap with a badge
CAP = ('<path d="M-31,-14 Q-34,-50 0,-52 Q34,-50 31,-14 Q22,-28 0,-29 Q-22,-28 -31,-14 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
       '<path d="M-36,-26 Q-34,-66 0,-68 Q34,-66 36,-26 Z" fill="#2b4f9e" stroke="#14141f" stroke-width="5" stroke-linejoin="round"/>'
       '<path d="M-38,-26 L46,-26 Q58,-22 52,-16 L-38,-18 Z" fill="#1d3a78" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
       '<rect x="-10" y="-58" width="20" height="16" rx="3" fill="#ffd23f" stroke="#14141f" stroke-width="3"/>')


sprites = []
DOGS = ["retriever", "greyhound", "dachshund", "husky", "pug", "corgi", "dalmatian", "beagle", "poodle", "labrador", "collie"]
for i in range(11):
    sprites.append(cat(f"C{i}", i, "1" if i == 0 else str(i + 1), CATK if i == 0 else CATV))
    sprites.append(dog(f"D{i}", DOGS[i], "1" if i == 0 else str(i + 1), DOGK if i == 0 else DOGV))
ref = part("athlete", "w3-REFx", HAIRSVG=CAP, KITC="#2b4f9e", KIT2="#2b4f9e", STRIPEOP=0, SHORTC="#1d3a78", SOCKC="#2b4f9e",
           NUMC="#ffd23f", NUM="✉", SKIN="#e3b48c")
sprites.append(sprite("REF", '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>' + ref, 460, 600, 520))
META["REF"] = dict(h=1.8, unit=360)
for k in (2, 3, 5, 7, 9):
    sprites.append(sprite(f"sleep{k}", sleeping_cat(k), 420, 300, 230))
sprites.append(sprite("box", BOX, 360, 300, 230))
sprites.append(sprite("boxfull", box_full(), 360, 340, 270))
sprites.append(sprite("laser", LASER, 100, 100, 50))
sprites.append(ball())

(EP / "world/meta.json").write_text(json.dumps(META, indent=1))
write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .bub.purple { background: #7b3fe4; color: #fff; }
    .bub.orange { background: #ff7a1a; color: #1a1a2e; }""")

(EP / "assets/world/meta.js").write_text("export default " + json.dumps(META) + ";\n")   # read by director.js
