"""Stadium kit for "full" football scenes (Season 2): packed stands with moving fans, flags and flashbulbs, ad boards, pitch,
whole teams with number tags, referee, goal, confetti, broadcast graphic (score + match clock + stamina bar), full-time board.

Same cartoon style as the rest of the channel (flat colours, #1a1a2e outlines, boil filter from scene.py).
Usage in a scene:  from stadium import *   then  stands(sid) + pitch(sid) + team(...) and STADIUM_JS in the js.
Layout (1080x1920): stands y 300..STAND_BOTTOM, ad boards, pitch below; feet of players on y = FEET (default 1180).
"""
import random

from kit import part

STAND_TOP, STAND_BOTTOM, FEET = 330, 880, 1180
FAN_COLS = ["#f4f4f2", "#f4f4f2", "#f4f4f2", "#e6e6e3", "#6a3fb5", "#ffd23f", "#1d2f6f"]
SKINS = ["#f2c9a0", "#e3b48c", "#c68b5e", "#8a5a3c", "#f6d7b8"]


def stands(sid, top=STAND_TOP, bottom=STAND_BOTTOM, seed=7, fan_cols=FAN_COLS, cols=24):
    """Tiers of fans in column groups (sid-fc0..fcN for waves), whole stand group sid-fans (jump), flashbulbs sid-fl0..19."""
    rnd = random.Random(seed)
    colw = 1080 / cols
    groups = [[] for _ in range(cols)]
    y, row = top + 40, 0
    while y < bottom - 10:
        s = 0.55 + 0.45 * (y - top) / (bottom - top)       # rows nearer the pitch are bigger
        step = 34 * s
        x = (row % 2) * step / 2 - 10
        while x < 1090:
            c = rnd.choice(fan_cols)
            sk = rnd.choice(SKINS)
            j = min(cols - 1, max(0, int(x // colw)))
            arm = rnd.random() < 0.25
            groups[j].append(
                f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})">'
                f'<rect x="-14" y="-6" width="28" height="26" rx="8" fill="{c}" stroke="#1a1a2e" stroke-width="3" />'
                + (f'<path d="M10,-2 L20,-26" stroke="{sk}" stroke-width="7" stroke-linecap="round" />' if arm else "")
                + f'<circle cx="0" cy="-16" r="11" fill="{sk}" stroke="#1a1a2e" stroke-width="3" /></g>')
            x += step
        y += 30 * s
        row += 1
    tiers = "".join(f'<path d="M0,{t} L1080,{t}" stroke="#2a2f45" stroke-width="6" />' for t in range(top + 120, bottom, 140))
    fans = "".join(f'<g id="{sid}-fc{j}">{"".join(g)}</g>' for j, g in enumerate(groups))
    flags = "".join(f'<g transform="translate({x},{top + 60 + (i % 3) * 90})"><g id="{sid}-flag{i}"><path d="M0,0 L0,-90" stroke="#1a1a2e" stroke-width="5" />'
                    f'<path d="M0,-90 L70,-78 L0,-50 Z" fill="{c}" stroke="#1a1a2e" stroke-width="4" /></g></g>'
                    for i, (x, c) in enumerate(((120, "#f4f4f2"), (390, "#6a3fb5"), (660, "#ffd23f"), (930, "#f4f4f2"))))
    flashes = "".join(f'<g transform="translate({rnd.randint(30, 1050)},{rnd.randint(top + 30, bottom - 40)})"><g id="{sid}-fl{i}" opacity="0">'
                      f'<path d="M0,-16 L4,-4 L16,0 L4,4 L0,16 L-4,4 L-16,0 L-4,-4 Z" fill="#fffbe6" /></g></g>' for i in range(20))
    roof = (f'<rect x="0" y="0" width="1080" height="{top}" fill="#1b2340" />'
            f'<path d="M0,{top - 40} L1080,{top - 70} L1080,{top} L0,{top} Z" fill="#2a3355" stroke="#1a1a2e" stroke-width="5" />'
            + "".join(f'<g transform="translate({x},{top - 140})"><rect x="-40" y="-26" width="80" height="44" rx="6" fill="#3a4466" stroke="#1a1a2e" stroke-width="4" />'
                      f'<g fill="#fff8d0">{"".join(f"<circle cx={cx} cy={cy} r=7 />" for cx in (-24, -8, 8, 24) for cy in (-12, 4))}</g></g>'
                      for x in (180, 540, 900)))
    return (f'<g id="{sid}-stand">{roof}<rect x="0" y="{top}" width="1080" height="{bottom - top}" fill="#3b4462" />{tiers}'
            f'<g id="{sid}-fans">{fans}</g>{flags}{flashes}</g>')


def boards(sid, y=STAND_BOTTOM, text="COULD? · LIVE RECONSTRUCTION · "):
    """LED ad boards along the touchline (the text scrolls: animate sid-adtext x)."""
    return (f'<rect x="0" y="{y}" width="1080" height="60" fill="#14182b" stroke="#1a1a2e" stroke-width="5" />'
            f'<clipPath id="{sid}-adc"><rect x="0" y="{y}" width="1080" height="60" /></clipPath>'
            f'<g clip-path="url(#{sid}-adc)"><g id="{sid}-adtext"><text data-layout-ignore x="0" y="{y + 42}" font-family="CouldMono" font-weight="700" font-size="34" '
            f'fill="#ffd23f" letter-spacing="4">{text * 6}</text></g></g>')


def pitch(sid, top=STAND_BOTTOM + 60, lines=True):
    stripes = "".join(f'<rect x="{x}" y="{top}" width="135" height="{1920 - top}" fill="{"#4f9a45" if i % 2 else "#5aa84f"}" />' for i, x in enumerate(range(0, 1080, 135)))
    ln = (f'<g stroke="#f4f4f2" stroke-width="7" fill="none" opacity="0.85"><path d="M0,{top + 70} L1080,{top + 70}" />'
          f'<path d="M540,{top + 70} L540,1920" /><ellipse cx="540" cy="{top + 330}" rx="220" ry="80" /></g>') if lines else ""
    return f'<g id="{sid}-pitch">{stripes}{ln}</g>'


def player(sid, name, x, y=FEET, s=0.62, kit="#f4f4f2", shorts="#f4f4f2", socks="#f4f4f2", numc="#1a1a2e", num="", skin=None, hair=None, tag=True, flip=False):
    """One outfield player (mbappe.svg rig, recoloured): wrapper sid-<name>, rig sid-<name>p-*, number tag above the head."""
    rnd = random.Random(name)
    skin = skin or rnd.choice(SKINS)
    hair = hair or rnd.choice(["#1a1410", "#3b2416", "#6b4a2a", "#d9b46a", "#2a1a10"])
    p = (part("mbappe", f"{sid}-{name}p", KITC=kit, SHORTC=shorts, SOCKC=socks, NUMC=numc)
         .replace(">10</text>", f">{num}</text>").replace("#8a5a3c", skin).replace("#1a1410", hair))
    t = (f'<g transform="translate(0,{-int(345 * s)})"><rect x="-34" y="-20" width="68" height="34" rx="10" fill="#1a1a2e" opacity="0.85" />'
         f'<text data-layout-ignore x="0" y="7" text-anchor="middle" font-family="CouldMono" font-weight="700" font-size="22" fill="#f4efe6">#{num}</text></g>') if tag else ""
    sx = -s if flip else s
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g transform="scale({sx},{s})">{p}</g>{t}</g></g>'


REAL = dict(kit="#f4f4f2", shorts="#f4f4f2", socks="#f4f4f2", numc="#1a1a2e")
REAL_NUMS = [1, 2, 3, 4, 5, 6, 8, 10, 11, 7, 9]


def messi_fig(sid, x, y=FEET, s=0.62, name="m", tag=True):
    """Messi (messi.svg): wrapper sid-<name>, rig sid-<name>-* (like battle.messi)."""
    t = (f'<g transform="translate(0,{-int(345 * s)})"><rect x="-58" y="-20" width="116" height="34" rx="10" fill="#a50044" />'
         f'<text data-layout-ignore x="0" y="7" text-anchor="middle" font-family="CouldMono" font-weight="700" font-size="22" fill="#ffd23f">MESSI</text></g>') if tag else ""
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g transform="scale({s})">{part("messi", sid + "-" + name)}</g>{t}</g></g>'


def football(sid, x, y, s=0.6, name="ball"):
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g id="{sid}-{name}-spin"><g transform="scale({s})">{part("football", sid + "-" + name + "f")}</g></g></g></g>'


def goal_side(sid, x, y=FEET, h=230, d=150, name="goal", facing="left"):
    """Goal seen from the side (the ball enters from `facing`). Bulge with scaleX on sid-<name>."""
    k = -1 if facing == "right" else 1
    return (f'<g transform="translate({x},{y}) scale({k},1)"><g id="{sid}-{name}"><path d="M0,0 L0,{-h} L{d},{-h}" fill="none" stroke="#f4f4f2" stroke-width="10" />'
            f'<path d="M0,{-h} L{d},0 M40,{-h} L{d},-60 M80,{-h} L{d},-120 M0,-60 L80,0 M0,-120 L130,0 M0,-180 L{d},-20" stroke="#f4f4f2" stroke-width="3" opacity="0.8" /></g></g>')


def confetti(sid, n=60, seed=3):
    rnd = random.Random(seed)
    pieces = "".join(f'<rect class="cf" x="{rnd.randint(0, 1080)}" y="{rnd.randint(-400, -20)}" width="{rnd.randint(10, 18)}" height="{rnd.randint(16, 26)}" '
                     f'fill="{rnd.choice(["#ffd23f", "#e0412f", "#4f7cff", "#f4f4f2", "#1f9d55"])}" transform="rotate({rnd.randint(0, 90)})" />' for _ in range(n))
    return f'<g id="{sid}-conf" opacity="0">{pieces}</g>'


def hud(sid, home="RMA", away="MES", h=0, a=0, minute="1'"):
    """Broadcast graphic (top right): score + minute, stamina bar for Messi. Change with label()/tl tweens on sid-hs/-as/-min/-stam."""
    return (f'\n    <div class="hud" id="{sid}-hud"><span class="t">{home}</span><span class="sc"><b id="{sid}-hs">{h}</b>–<b id="{sid}-as">{a}</b></span>'
            f'<span class="t">{away}</span><span class="mn" id="{sid}-min">{minute}</span></div>'
            f'\n    <div class="stam" id="{sid}-stambox"><span>MESSI STAMINA</span><div class="bar"><i id="{sid}-stam"></i></div></div>')


def fulltime(sid, rows):
    """Full-time stats board (HTML), rows = [(label, left, right)]."""
    body = "".join(f'<tr><td>{l}</td><td class="k">{a}</td><td class="k">{b}</td></tr>' for a, b, l in [(r[1], r[2], r[0]) for r in rows])
    return (f'\n    <div class="ft" id="{sid}-ft"><div class="fth">FULL TIME</div><div class="fts">REAL MADRID <b>2–3</b> MESSI</div>'
            f'<table>{body}</table></div>')


def slam(sid, name, text, top=420, size=128, color="#ffd23f"):
    return f'\n    <div class="slam" id="{sid}-{name}" style="top: {top}px; font-size: {size}px; color: {color};">{text}</div>'


CSS = """
    .hud { position: absolute; left: 520px; top: 184px; display: flex; align-items: center; gap: 12px; padding: 10px 18px; background: #1a1a2e;
           border: 4px solid #f4efe6; border-radius: 14px; font: 700 30px/1 "CouldMono"; color: #f4efe6; }
    .hud .sc { font: 900 46px/1 "Inter"; color: #ffd23f; }
    .hud .mn { margin-left: 6px; padding: 6px 10px; border-radius: 8px; background: #e0412f; color: #fff; font: 700 28px/1 "CouldMono"; }
    .stam { position: absolute; left: 520px; top: 262px; display: flex; align-items: center; gap: 12px; font: 700 22px/1 "CouldMono"; color: #f4efe6;
            padding: 8px 14px; background: rgba(26, 26, 46, 0.85); border-radius: 12px; }
    .stam .bar { width: 230px; height: 18px; border: 3px solid #f4efe6; border-radius: 9px; overflow: hidden; }
    .stam .bar i { display: block; width: 100%; height: 100%; background: #1f9d55; }
    .slam { position: absolute; left: 30px; right: 30px; text-align: center; font-family: "Inter"; font-weight: 900; line-height: 0.95;
            -webkit-text-stroke: 8px #1a1a2e; paint-order: stroke fill; opacity: 0; }
    .ft { position: absolute; left: 90px; right: 90px; top: 360px; padding: 26px 30px 30px; background: #12162a; border: 6px solid #ffd23f;
          border-radius: 18px; color: #f4efe6; text-align: center; opacity: 0; }
    .ft .fth { font: 900 64px/1 "Inter"; color: #ffd23f; }
    .ft .fts { margin-top: 10px; font: 700 34px/1.2 "CouldMono"; }
    .ft .fts b { color: #ffd23f; font-family: "Inter"; font-size: 44px; }
    .ft table { width: 100%; margin-top: 16px; border-collapse: collapse; font: 700 26px/1.3 "CouldMono"; }
    .ft td { padding: 6px 4px; border-top: 2px solid #2a3355; text-align: left; }
    .ft td.k { text-align: right; width: 70px; color: #ffd23f; }"""

JS = """
      const label = (id, steps) => {
        const el = document.querySelector(S + id); if (!el) return;
        tl.to({}, { duration: D, ease: "none", onUpdate() { const t = this.time(); let txt = steps[0][1];
          for (const [at, s] of steps) if (t >= at) txt = s; if (el.textContent !== txt) el.textContent = txt; } }, 0);
      };
      const look = (p, x, y, at, d = 0.2) => tl.to([S + p + "-pupL", S + p + "-pupR"], { x, y, duration: d }, at);
      // crowd: idle bob, a Mexican wave, everyone jumps, flashbulbs
      const crowdIdle = () => { for (let j = 0; j < 24; j++) tl.fromTo(S + "fc" + j, { y: 0 }, { y: -5, duration: 0.3 + (j % 4) * 0.05, yoyo: true, repeat: R(D, 0.3 + (j % 4) * 0.05), ease: "sine.inOut" }, (j % 5) * 0.07);
        for (let i = 0; i < 4; i++) tl.fromTo(S + "flag" + i, { rotation: -6 }, { rotation: 6, transformOrigin: "0% 100%", duration: 0.5, yoyo: true, repeat: R(D, 0.5), ease: "sine.inOut" }, i * 0.1);
        tl.fromTo(S + "adtext", { x: 0 }, { x: -600, duration: D, ease: "none" }, 0); };
      const wave = (t0) => { for (let j = 0; j < 24; j++) tl.to(S + "fc" + j, { y: -34, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", overwrite: false }, t0 + j * 0.06); };
      const jump = (t0, n = 3) => tl.fromTo(S + "fans", { y: 0 }, { y: -22, duration: 0.15, yoyo: true, repeat: n * 2 - 1, ease: "power2.out" }, t0);
      const flashes = (t0, d) => { for (let i = 0; i < 20; i++) { const at = t0 + ((i * 0.37) % Math.max(0.4, d)); tl.set(S + "fl" + i, { opacity: 1 }, at); tl.set(S + "fl" + i, { opacity: 0 }, at + 0.08); } };
      const score = (h, a, m, at) => { label("hs", [[0, document.querySelector(S + "hs").textContent], [at, String(h)]]); label("as", [[0, document.querySelector(S + "as").textContent], [at, String(a)]]);
        label("min", [[0, document.querySelector(S + "min").textContent], [at, m]]); tl.fromTo(S + "hud", { scale: 1 }, { scale: 1.12, transformOrigin: "50% 50%", duration: 0.15, yoyo: true, repeat: 1 }, at); };
      const stamina = (pct, at = 0, d = 0.01) => tl.to(S + "stam", { width: pct + "%", backgroundColor: pct < 25 ? "#e0412f" : pct < 55 ? "#ffd23f" : "#1f9d55", duration: d }, at);
      const slamIn = (name, at, out) => { tl.fromTo(S + name, { opacity: 0, scale: 2.2, rotation: -4 }, { opacity: 1, scale: 1, rotation: -3, transformOrigin: "50% 50%", duration: 0.2, ease: "power4.in" }, at);
        tl.fromTo(S + "svg", { x: 0 }, { x: 12, duration: 0.04, yoyo: true, repeat: 5 }, at + 0.2); if (out != null) tl.to(S + name, { opacity: 0, scale: 0.8, duration: 0.15 }, out); };
      const confettiFall = (at) => { tl.set(S + "conf", { opacity: 1 }, at); tl.fromTo(S + "conf", { y: 0 }, { y: 2300, duration: 2.6, ease: "none" }, at); };
      const run = (p, t0, t1, cyc = 0.14) => { const n = R(t1 - t0, cyc);
        tl.fromTo(S + p + "-legL", { rotation: -28 }, { rotation: 28, duration: cyc, yoyo: true, repeat: n, ease: "sine.inOut" }, t0);
        tl.fromTo(S + p + "-legR", { rotation: 28 }, { rotation: -28, duration: cyc, yoyo: true, repeat: n, ease: "sine.inOut" }, t0);
        tl.to([S + p + "-legL", S + p + "-legR"], { rotation: 0, duration: 0.1 }, t1); };
      const arc = (sel, t0, d, dx, dy, h, spinSel) => { const el = document.querySelector(sel), o = { p: 0 };
        tl.fromTo(o, { p: 0 }, { p: 1, duration: d, ease: "none", onUpdate() { const p = o.p; gsap.set(el, { x: dx * p, y: dy * p - 4 * h * p * (1 - p) }); } }, t0);
        if (spinSel) tl.fromTo(spinSel, { rotation: 0 }, { rotation: 720, duration: d, ease: "none", transformOrigin: "50% 50%" }, t0); };
      const spinOut = (name, at) => { tl.to(S + name, { scaleX: -1, transformOrigin: "50% 100%", duration: 0.08, yoyo: true, repeat: 3, ease: "none" }, at);
        tl.to(S + name, { rotation: 80, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.in" }, at + 0.35); };
"""
