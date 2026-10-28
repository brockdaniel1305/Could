"""Shared world + race driver for episode 002 (Bolt vs T-Rex, 100 m).

Positions come from a model, not by hand:
  Bolt   = his 10 m splits from Berlin 2009 (9.58 s), then a 2 s run-out after the line
  T-Rex  = nose position, 12 m ahead at the gun (its own length), constant ~5.4 m/s (Sellers et al. 2017)
Scene time is mapped to race time with keyframes, so the race can run in slow motion.
"""
from scene import part  # noqa: F401

PX = 75          # pixels per metre on the course
NOSE = 405       # trex.svg nose offset at scale 1.5 (270 * 1.5)
REX_Y, BOLT_Y = 1100, 1180


def course(sid, start_blocks=True):
    marks = []
    for m in range(10, 100, 10):
        x = m * PX
        marks.append(f'<path d="M{x},876 L{x},1920" stroke="#f4efe6" stroke-width="5" opacity="0.7" />'
                     f'<g transform="translate({x},836)"><rect x="-52" y="-30" width="104" height="52" rx="8" fill="#f4efe6" stroke="#1a1a2e" stroke-width="4" />'
                     f'<text data-layout-ignore y="10" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#1a1a2e">{m} m</text></g>')
    F = 100 * PX
    checks = "".join(f'<rect x="{F + (i % 2) * 14}" y="{876 + i * 14}" width="14" height="14" fill="#1a1a2e" />' for i in range(75))
    blocks = (f'<g transform="translate(-26,{BOLT_Y})"><path d="M-20,0 L10,-26 L22,-26 L22,0 Z M14,0 L44,-22 L54,-22 L54,0 Z" fill="#9aa3ad" stroke="#1a1a2e" stroke-width="4" /></g>'
              if start_blocks else "")
    return f"""
<g id="{sid}-course">
  <rect x="-8" y="876" width="16" height="1044" fill="#f4efe6" />
  <text data-layout-ignore x="-110" y="1520" font-family="Inter" font-weight="900" font-size="200" fill="#f4efe6" opacity="0.85">4</text>
  <text data-layout-ignore x="-110" y="1800" font-family="Inter" font-weight="900" font-size="200" fill="#f4efe6" opacity="0.85">5</text>
  {''.join(marks)}
  <rect x="{F}" y="876" width="28" height="1044" fill="#f4efe6" />{checks}
  <g transform="translate({F + 14},0)"><path d="M-120,860 L-120,520 M120,860 L120,520" stroke="#1a1a2e" stroke-width="14" />
    <rect x="-170" y="500" width="340" height="80" rx="12" fill="#e0412f" stroke="#1a1a2e" stroke-width="6" />
    <text data-layout-ignore y="556" text-anchor="middle" font-family="Inter" font-weight="900" font-size="52" fill="#fff">FINISH</text></g>
  <path id="{sid}-tape" d="M{F + 14},960 L{F + 14},1190" stroke="#ffd23f" stroke-width="8" />
  {blocks}
  <g id="{sid}-rex"><g transform="translate(0,{REX_Y}) scale(1.5)">{part("trex", sid + "-r")}</g></g>
  <g id="{sid}-bolt"><g transform="translate(0,{BOLT_Y}) scale(1.3)">{part("sprinter", sid + "-b")}</g></g>
</g>"""


def tracker(sid):
    """Live race tracker under the captions: a 0-100 m bar with a Bolt dot (above) and a T-Rex dot (below). No text."""
    ticks = "".join(f'<path d="M{90 + m * 9},1500 L{90 + m * 9},1540" stroke="#1a1a2e" stroke-width="4" />' for m in range(10, 100, 10))
    checks = "".join(f'<rect x="{990 + (i % 2) * 12}" y="{1480 + i * 12}" width="12" height="12" fill="#1a1a2e" />' for i in range(7))
    return f"""
<g id="{sid}-trk">
  <rect x="70" y="1440" width="960" height="160" rx="30" fill="#1a1a2e" opacity="0.35" />
  <rect x="90" y="1500" width="900" height="40" rx="20" fill="#f4efe6" stroke="#1a1a2e" stroke-width="5" />{ticks}
  <rect x="990" y="1480" width="24" height="84" fill="#f4efe6" stroke="#1a1a2e" stroke-width="3" />{checks}
  <g id="{sid}-tb"><circle cx="90" cy="1478" r="26" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" /><path d="M90,1462 L80,1480 L92,1480 L86,1496" fill="none" stroke="#1f9d55" stroke-width="5" stroke-linejoin="round" /></g>
  <g id="{sid}-tr"><circle cx="90" cy="1562" r="26" fill="#5fa84a" stroke="#1a1a2e" stroke-width="5" /><path d="M74,1566 l6,-10 l6,10 l6,-10 l6,10 l6,-10" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round" /></g>
</g>"""


def driver(keys, cams):
    """keys: [[sceneTime, raceTime], ...]; cams: [[sceneTime, mode]] with mode a number (metres), "bolt", "rex" or "mid"."""
    return f"""
      // ---- race driver: everything below is a pure function of scene time ----
      const PX = {PX}, NOSE = {NOSE};
      const SPL = [[0,0],[1.89,10],[2.88,20],[3.78,30],[4.64,40],[5.47,50],[6.29,60],[7.10,70],[7.92,80],[8.75,90],[9.58,100]];
      const boltM = (t) => {{
        if (t <= 0) return 0;
        if (t >= 9.58) {{ const d = Math.min(t - 9.58, 2); return 100 + 10.4 * d - 2.6 * d * d; }}
        for (let i = 1; i < SPL.length; i++) if (t <= SPL[i][0]) {{ const [t0, m0] = SPL[i - 1], [t1, m1] = SPL[i]; return m0 + (m1 - m0) * (t - t0) / (t1 - t0); }}
      }};
      const rexM = (t) => 12 + 5.4 * Math.max(0, t);
      const lerpK = (k, x) => {{
        if (x <= k[0][0]) return k[0][1];
        for (let i = 1; i < k.length; i++) if (x <= k[i][0]) return k[i - 1][1] + (k[i][1] - k[i - 1][1]) * (x - k[i - 1][0]) / (k[i][0] - k[i - 1][0]);
        return k[k.length - 1][1];
      }};
      const KEYS = {keys}, CAMS = {cams};
      const target = (mode, b, r) => typeof mode === "number" ? mode : mode === "bolt" ? b + 1.5 : mode === "rex" ? r - 5 : (b + r - 5) / 2;
      const ss = (x) => x * x * (3 - 2 * x);
      const camAt = (lt, b, r) => {{
        let i = 0; while (i + 1 < CAMS.length && lt >= CAMS[i + 1][0]) i++;
        const cur = target(CAMS[i][1], b, r);
        if (i === 0) return cur;
        const k = Math.min(1, (lt - CAMS[i][0]) / 0.7);
        return target(CAMS[i - 1][1], b, r) + (cur - target(CAMS[i - 1][1], b, r)) * ss(k);
      }};
      const bolt = document.querySelector(S + "bolt"), rex = document.querySelector(S + "rex"), course = document.querySelector(S + "course");
      const clock = document.querySelector(S + "clock");
      const RIG = (p) => document.querySelector(S + p);
      const legsB = [RIG("b-legL"), RIG("b-legR"), RIG("b-armL"), RIG("b-armR")], legsR = [RIG("r-legL"), RIG("r-legR")];
      const race = {{ rt: 0 }};
      tl.to({{}}, {{ duration: D, ease: "none", onUpdate() {{
        const lt = this.time(), rt = lerpK(KEYS, lt), moving = lerpK(KEYS, lt + 0.05) > rt + 1e-4;
        race.rt = rt;
        const b = boltM(rt), r = rexM(rt);
        gsap.set(bolt, {{ x: b * PX }});
        gsap.set(rex, {{ x: r * PX - NOSE }});
        gsap.set(course, {{ x: 540 - camAt(lt, b, r) * PX }});
        if (clock) clock.textContent = rt.toFixed(2) + " s";
        const tb = document.querySelector(S + "tb"), tr = document.querySelector(S + "tr");
        if (tb) {{ gsap.set(tb, {{ x: Math.min(b, 100) * 9 }}); gsap.set(tr, {{ x: Math.min(r, 100) * 9 }}); }}
        if (moving && rt > 0.15 && boltM(rt) < 110.3) {{
          const a = Math.sin(rt * Math.PI * 2 * 2.2) * 38;
          gsap.set(legsB[0], {{ rotation: a }}); gsap.set(legsB[1], {{ rotation: -a }});
          gsap.set(legsB[2], {{ rotation: -a * 1.2 }}); gsap.set(legsB[3], {{ rotation: a * 1.2 }});
          gsap.set(RIG("b-body"), {{ rotation: 7, transformOrigin: "50% 100%" }});
        }}
        if (moving) {{
          const q = Math.sin(rt * Math.PI * 2 * 1.4) * 24;
          gsap.set(legsR[0], {{ rotation: q }}); gsap.set(legsR[1], {{ rotation: -q }});
          gsap.set(RIG("r-body"), {{ y: Math.abs(Math.sin(rt * Math.PI * 2 * 1.4)) * -10 }});
        }}
      }} }}, 0);
"""
