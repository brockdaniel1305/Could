"""Shared world + ball physics for episode 003 (Curry vs the Great Wall).

Scale 100 px per metre. Shooter's feet at x 0 m (screen x 150), ground y 0 m (screen y 1250).
Release point (0.15 m, 2.4 m). Rim centre 7.24 m away (NBA three-point distance) at 3.05 m.
Wall centred at 3.62 m: 4.5 m wide on top (faces at 1.37 m and 5.87 m), 7 m tall.
Ball paths are integrated here (gravity only) and sampled at 60 Hz; the JS only plays the samples back.
"""
import json
import math

from scene import part  # noqa: F401

M, X0, GY = 100, 150, 1250
G = 9.81
REL = (0.15, 2.4)
RIM_X, RIM_Y, BOARD_X = 7.24, 3.05, 7.56
WALL_L, WALL_R, WALL_H, BALL_R = 1.37, 5.87, 7.0, 0.12


def sx(x):
    return X0 + x * M


def sy(y):
    return GY - y * M


def v_for(theta):
    """Launch speed that sends a ball released at REL through the rim centre."""
    c, t = math.cos(theta), math.tan(theta)
    dx, dy = RIM_X - REL[0], RIM_Y - REL[1]
    return math.sqrt(G * dx * dx / (2 * c * c * (dx * t - dy)))


def fly(theta_deg, v=None, bounce_wall=False, until=4.0, can_score=True):
    th = math.radians(theta_deg)
    v = v or v_for(th)
    x, y = REL
    vx, vy = v * math.cos(th), v * math.sin(th)
    dt, t, pts, events, bounced, scored = 1 / 240, 0.0, [], {}, 0, False
    while t < until:
        x, y, vy = x + vx * dt, y + vy * dt, vy - G * dt
        t += dt
        if bounce_wall and not bounced and vx > 0 and x + BALL_R >= WALL_L and y < WALL_H:
            vx, bounced = -0.55 * vx, 1
            events["wall"] = t
        if bounce_wall and bounced == 1 and vx < 0 and x <= 0.35 and y <= 2.75:   # Curry's head
            vx, vy, bounced = -0.4 * vx, 2.5, 2
            events["head"] = t
        if can_score and not scored and vy < 0 and abs(x - RIM_X) < 0.12 and abs(y - RIM_Y) < 0.06:
            scored, vx = True, 0.0
            events["swish"] = t
        if x + BALL_R >= BOARD_X and vx > 0 and RIM_Y - 0.1 < y < RIM_Y + 1.1:
            vx = -0.5 * vx
            events["board"] = t
        if y <= BALL_R:
            y, vy = BALL_R, -0.5 * vy
            events.setdefault("ground", t)
            if abs(vy) < 0.8:
                vy = 0.0
        if round(t * 240) % 4 == 0:
            pts.append([round(t, 4), round(sx(x), 1), round(sy(y), 1)])
    apex = max(p[2] for p in pts)
    return {"pts": pts, "events": {k: round(v, 3) for k, v in events.items()}, "v": v,
            "apex_m": round((GY - min(p[2] for p in pts)) / M, 2), "_": apex}


def world(sid, face=True):
    ruler = "".join(
        f'<path d="M40,{sy(m)} L{70 if m % 2 == 0 else 58},{sy(m)}" stroke="#1a1a2e" stroke-width="5" />'
        + (f'<text data-layout-ignore x="78" y="{sy(m) + 10}" font-family="Inter" font-weight="900" font-size="28" fill="#1a1a2e">{m} m</text>' if m % 2 == 0 and m else "")
        for m in range(0, 11))
    planks = "".join(f'<path d="M0,{y} L1080,{y}" stroke="#b9783f" stroke-width="3" />' for y in range(1290, 1920, 46))
    return f"""
{part("china-day", sid + "-land", GY=GY)}
<rect x="0" y="{GY}" width="1080" height="700" fill="#d99a5b" />{planks}
<path d="M{sx(RIM_X) - 470},1920 Q{sx(RIM_X) - 520},1500 {sx(RIM_X) - 380},{GY + 6}" fill="none" stroke="#f4efe6" stroke-width="10" />
<rect x="{sx(RIM_X) - 190}" y="{GY + 6}" width="300" height="680" fill="#1d428a" opacity="0.55" />
<path d="M0,{GY} L1080,{GY}" stroke="#1a1a2e" stroke-width="6" />
<g id="{sid}-ruler" opacity="0.85"><path d="M40,{sy(10)} L40,{GY}" stroke="#1a1a2e" stroke-width="5" />{ruler}</g>
<g transform="translate({sx(3.62)},{GY})">{part("great-wall", sid + "-w")}</g>
<g transform="translate({sx(RIM_X) + 100},{GY})">{part("hoop", sid + "-h")}</g>
<g transform="translate({X0},{GY})"><g id="{sid}-kwrap"><g transform="scale(0.845)">{part("point-guard", sid + "-p")}</g></g></g>
"""


def ball(sid, name="ball"):
    return f'<g id="{sid}-{name}"><g>{part("basketball", sid + "-" + name + "b")}</g></g>'


def dots(sid, name, path, step=6):
    pts = path["pts"][::step]
    return "".join(f'<circle id="{sid}-{name}{i}" cx="{p[1]}" cy="{p[2]}" r="5" fill="#f4efe6" stroke="#1a1a2e" stroke-width="2" opacity="0" />'
                   for i, p in enumerate(pts)), len(pts), [p[0] for p in pts]


def player_js():
    """JS helper: play(ballId, pts, sceneStart, slow, tEnd) moves the ball along precomputed samples."""
    return """
      const play = (id, P, at, slow = 1, tEnd = null) => {
        const el = document.querySelector(S + id), last = tEnd ?? P[P.length - 1][0];
        const pos = (t) => { let i = 1; while (i < P.length - 1 && P[i][0] < t) i++;
          const a = P[i - 1], b = P[i], k = Math.max(0, Math.min(1, (t - a[0]) / ((b[0] - a[0]) || 1)));
          return [a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]; };
        const p0 = P[0];
        tl.fromTo(el, { x: p0[1], y: p0[2] }, { x: p0[1], y: p0[2], duration: 0.01 }, Math.max(0, at - 0.02));
        tl.to({}, { duration: last * slow, ease: "none", onUpdate() {
          const t = this.time() / slow, [x, y] = pos(t);
          gsap.set(el, { x, y, rotation: t * 540 });
        } }, at);
      };
      const trail = (name, n, times, at, slow = 1) => { for (let i = 0; i < n; i++) tl.fromTo(S + name + i, { opacity: 0 }, { opacity: 0.9, duration: 0.01 }, at + times[i] * slow); };
"""


def J(obj):
    return json.dumps(obj, separators=(",", ":"))
