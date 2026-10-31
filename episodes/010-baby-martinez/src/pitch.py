"""Shared world for episode 010 (short): Stamford Bridge-ish pitch (no badges), Martínez, a Chelsea-blue opponent, the referee, a baby."""
from scene import part  # noqa: F401

GY = 1200


def player(sid, name, x, num, kit, short, sock, numc="#f4f4f2", hair="#1a1410", skin="#8a5a3c", s=0.85):
    p = (part("mbappe", sid + "-" + name, KITC=kit, SHORTC=short, SOCKC=sock, NUMC=numc)
         .replace(">10</text>", f">{num}</text>").replace("#1a1410", hair).replace("#8a5a3c", skin))
    return f'<g transform="translate({x},{GY})"><g id="{sid}-{name}w"><g transform="scale({s})">{p}</g></g></g>'


def martinez(sid, x=380, s=0.85):
    return player(sid, "li", x, 6, "#d0202e", "#f4f4f2", "#1a1a2e", hair="#1a1410", skin="#d9a07a", s=s)


def opp(sid, x=620, s=0.85):
    return player(sid, "op", x, 8, "#1d4fbf", "#1d4fbf", "#f4f4f2", hair="#6b4a2a", skin="#f2c9a0", s=s)


def ref(sid, x=880, s=0.85):
    return player(sid, "rf", x, "", "#1a1a2e", "#1a1a2e", "#1a1a2e", hair="#3a2a1a", skin="#e3b48c", s=s)


def baby(sid, x, s=0.4, y=GY):
    return f'<g transform="translate({x},{y})"><g id="{sid}-bw"><g transform="scale({s})">{part("baby", sid + "-b")}</g></g></g>'


def pitch(sid):
    return part("pitch-day", sid + "-pd", GY=1010)


CSS = """
    .card s { text-decoration-thickness: 8px; text-decoration-color: #e0412f; }
    .stamp { position: absolute; left: 150px; top: 470px; width: 780px; height: 300px; border: 24px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 150px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.25); }
    .heart { position: absolute; left: 290px; top: 780px; width: 180px; height: 166px; opacity: 0; }"""

HEART = '<svg class="heart" id="HID" viewBox="0 0 100 92"><path d="M50,88 C10,60 0,40 0,25 C0,10 12,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C88,0 100,10 100,25 C100,40 90,60 50,88 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="5" /></svg>'

JS = """
      const look = (p, x, y, at, d = 0.2) => tl.to([S + p + "-pupL", S + p + "-pupR"], { x, y, duration: d }, at);
      const face = (p, show, at) => ["m-smile", "m-o", "m-flat"].forEach((m) => { const el = document.querySelector(S + p + "-" + m); if (el) tl.set(el, { opacity: m === show ? 1 : 0 }, at); });
"""
