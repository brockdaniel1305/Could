"""Shared world for episode 008 (Mbappé and the French Revolution).

Street level at y = GY (Paris street, palace square, Bastille). Mbappé = mbappe.svg (navy kit in Paris, white in Madrid),
citizens = citizen.svg (front rows rigged, back rows <use> copies: a normal and an arms-crossed variant for the wave),
Napoleon = napoleon-horse.svg. Under the captions: the POPULARITY meter (graphics only). Top right: the calendar sheet.
"""
import math

from scene import part  # noqa: F401

GY = 1200
NAVY = dict(KITC="#1d2f6f", SHORTC="#1d2f6f", SOCKC="#1d2f6f", NUMC="#f4f4f2")
WHITE = dict(KITC="#f4f4f2", SHORTC="#f4f4f2", SOCKC="#f4f4f2", NUMC="#1a1a2e")


def mb(sid, x=300, y=GY, s=0.85, kit=NAVY, name="m"):
    """Mbappé: move sid-<name>w, rig ids sid-<name>-* (crown sid-<name>-crown, sash sid-<name>-sash)."""
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}w"><g transform="scale({s})">{part("mbappe", sid + "-" + name, **kit)}</g></g></g>'


def mate(sid, name, x, num, hair="#6b4a2a", skin="#e3b48c", s=0.8):
    """A generic team-mate (white kit, different number/hair/skin)."""
    p = part("mbappe", sid + "-" + name, **WHITE).replace(">10</text>", f">{num}</text>").replace("#1a1410", hair).replace("#8a5a3c", skin)
    return f'<g transform="translate({x},{GY})"><g id="{sid}-{name}w"><g transform="scale({s})">{p}</g></g></g>'


def cit(sid, name, x, y=GY, s=0.8, cap="#c0262d"):
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g transform="scale({s})">{part("citizen", sid + "-" + name + "p", CAPC=cap)}</g></g></g>'


def crowd_defs(sid):
    """<defs> with a normal citizen (sid-C), an arms-crossed one (sid-X) and a grey prisoner (sid-P)."""
    base = part("citizen", sid + "-Cp", CAPC="#c0262d")
    crossed = (part("citizen", sid + "-Xp", CAPC="#c0262d")
               .replace(f'<g id="{sid}-Xp-armL">', f'<g id="{sid}-Xp-armL" transform="rotate(-62)">')
               .replace(f'<g id="{sid}-Xp-armR">', f'<g id="{sid}-Xp-armR" transform="rotate(62)">')
               .replace(f'<g id="{sid}-Xp-fork">', f'<g id="{sid}-Xp-fork" opacity="0">')
               .replace(f'<ellipse id="{sid}-Xp-m-o"', f'<ellipse id="{sid}-Xp-m-o" opacity="0"')
               .replace(f'<path id="{sid}-Xp-m-smile" d="M-14,26 Q0,38 14,26" fill="none" stroke="#1a1a2e" stroke-width="5" stroke-linecap="round" opacity="0" />',
                        f'<path id="{sid}-Xp-m-smile" d="M-14,26 Q0,38 14,26" fill="none" stroke="#1a1a2e" stroke-width="5" stroke-linecap="round" />'))
    return f'<defs><g id="{sid}-C">{base}</g><g id="{sid}-X">{crossed}</g></defs>'


def crowd(sid, rows, x0=-40, dx=120, name="cr", crossed=False):
    """rows = [(y, scale, count)], drawn in the given order (back first). Each copy: sid-<name><r>-<c> (normal) and
    sid-<name>X<r>-<c> (arms crossed, opacity 0 unless crossed=True)."""
    out = []
    for r, (y, s, n) in enumerate(rows):
        for c in range(n):
            x = x0 + c * dx * s / 0.8 + (r % 2) * 50
            out.append(f'<g transform="translate({x:.0f},{y}) scale({s})"><g id="{sid}-{name}{r}-{c}" opacity="{0 if crossed else 1}"><use href="#{sid}-C" /></g>'
                       f'<g id="{sid}-{name}X{r}-{c}" opacity="{1 if crossed else 0}"><use href="#{sid}-X" /></g></g>')
    return f'<g id="{sid}-{name}">' + "".join(out) + "</g>"


def gauge(sid):
    """POPULARITY meter under the captions (no text): thumb down ... thumb up, needle sid-needle (rotate -80 .. 80)."""
    thumb = lambda x, up, col: (f'<g transform="translate({x},1760) scale(1,{1 if up else -1})"><rect x="-30" y="-18" width="60" height="50" rx="16" fill="{col}" stroke="#1a1a2e" stroke-width="6" />'
                                f'<rect x="-12" y="-62" width="22" height="50" rx="10" fill="{col}" stroke="#1a1a2e" stroke-width="6" /></g>')
    ticks = "".join(f'<path d="M{540 + 300 * math.cos(math.radians(180 - a)):.0f},{1760 - 300 * math.sin(math.radians(180 - a)):.0f} '
                    f'L{540 + 262 * math.cos(math.radians(180 - a)):.0f},{1760 - 262 * math.sin(math.radians(180 - a)):.0f}" stroke="#1a1a2e" stroke-width="8" />'
                    for a in range(0, 181, 30))
    return f'''<g id="{sid}-gauge">
  <path d="M240,1760 A300,300 0 0 1 840,1760 Z" fill="#f4efe6" stroke="#1a1a2e" stroke-width="8" />
  <path d="M240,1760 A300,300 0 0 1 390,1500 L540,1760 Z" fill="#e0412f" opacity="0.8" />
  <path d="M690,1500 A300,300 0 0 1 840,1760 L540,1760 Z" fill="#1f9d55" opacity="0.8" />
  {ticks}{thumb(170, False, "#e0412f")}{thumb(910, True, "#1f9d55")}
  <g transform="translate(540,1760)"><g id="{sid}-needle"><path d="M-14,0 L0,-250 L14,0 Z" fill="#1a1a2e" /></g></g>
  <circle cx="540" cy="1760" r="30" fill="#ffd23f" stroke="#1a1a2e" stroke-width="7" /></g>'''


def calendar(sid, day, mon, year):
    """Calendar sheet top right. Change its text with label("cd"/"cm"/"cy", steps)."""
    return (f'\n    <div class="cal" id="{sid}-cal"><div class="ch"><span id="{sid}-cm">{mon}</span></div>'
            f'<div class="cb"><span id="{sid}-cd">{day}</span></div><div class="cyy" id="{sid}-cy">{year}</div></div>')


def counter(sid, name, start="0"):
    return f'<span id="{sid}-{name}">{start}</span>'


def stamp(sid, word, color="#1f9d55"):
    return f'\n    <div class="stamp" id="{sid}-stamp" style="border-color: {color}; color: {color};">{word}</div>'


CSS = """
    .cal { position: absolute; left: 820px; top: 184px; width: 200px; background: #f4efe6; border: 5px solid #1a1a2e; border-radius: 14px;
           overflow: hidden; text-align: center; box-shadow: 0 6px 0 #1a1a2e; }
    .cal .ch { background: #c0262d; color: #fff; font: 700 28px/1 "CouldMono"; letter-spacing: 0.12em; padding: 8px 0; }
    .cal .cb { font: 900 64px/1 "Inter"; color: #1a1a2e; padding: 6px 0 0; }
    .cal .cyy { font: 700 30px/1 "CouldMono"; color: #1a1a2e; padding: 2px 0 10px; }
    .bar { width: 380px; height: 30px; margin-top: 10px; border: 4px solid #1a1a2e; border-radius: 10px; background: #f4efe6; overflow: hidden; }
    .bar i { display: block; width: 0; height: 100%; background: #e0412f; }
    .week { position: absolute; left: 40px; top: 360px; padding: 18px 20px 22px; background: #f4efe6; border: 6px solid #1a1a2e; border-radius: 22px; }
    .week .wk { font: 700 28px/1 "CouldMono"; letter-spacing: 0.08em; color: #6b6358; margin-bottom: 14px; }
    .week .row { display: flex; gap: 8px; }
    .week .d { width: 72px; height: 96px; border: 4px solid #1a1a2e; border-radius: 10px; background: #fff; display: flex; align-items: center;
               justify-content: center; font: 900 40px/1 "Inter"; color: #1a1a2e; }
    .week .d.r { width: 120px; background: #e0412f; color: #fff; font: 900 28px/1 "Inter"; }
    .stamp { position: absolute; left: 140px; top: 520px; width: 800px; height: 340px; border: 24px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 160px/1 "Inter"; opacity: 0; background: rgba(244, 239, 230, 0.25); }"""

JS = """
      const label = (id, steps) => {
        const el = document.querySelector(S + id);
        tl.to({}, { duration: D, ease: "none", onUpdate() {
          const t = this.time(); let txt = steps[0][1];
          for (const [at, s] of steps) if (t >= at) txt = s;
          if (el.textContent !== txt) el.textContent = txt;
        } }, 0);
      };
      const count = (id, a, b, t0, d, ease = "power2.out", suffix = "") => {
        const el = document.querySelector(S + id), o = { v: a };
        el.textContent = a.toLocaleString("en-US") + suffix;
        tl.fromTo(o, { v: a }, { v: b, duration: d, ease, onUpdate() { el.textContent = Math.round(o.v).toLocaleString("en-US") + suffix; } }, t0);
      };
      const look = (p, x, y, at, d = 0.2) => tl.to([S + p + "-pupL", S + p + "-pupR"], { x, y, duration: d }, at);
      const needle = (deg, at, d = 0.6) => tl.to(S + "needle", { rotation: deg, transformOrigin: "50% 100%", duration: d, ease: "back.out(1.6)" }, at);
      // Mbappé (rig prefix p, default "m") crosses his arms / lets them go
      const cross = (at, p = "m") => { tl.to(S + p + "-armL", { rotation: -62, duration: 0.25, ease: "back.out(2)" }, at); tl.to(S + p + "-armR", { rotation: 62, duration: 0.25, ease: "back.out(2)" }, at); };
      const uncross = (at, p = "m") => tl.to([S + p + "-armL", S + p + "-armR"], { rotation: 0, duration: 0.25 }, at);
      const run = (t0, t1, p = "m", cyc = 0.14) => {
        const n = R(t1 - t0, cyc);
        tl.fromTo(S + p + "-legL", { rotation: -30 }, { rotation: 30, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + p + "-legR", { rotation: 30 }, { rotation: -30, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + p + "-armL", { rotation: 30 }, { rotation: -30, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + p + "-armR", { rotation: -30 }, { rotation: 30, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.to([S + p + "-legL", S + p + "-legR", S + p + "-armL", S + p + "-armR"], { rotation: 0, duration: 0.12 }, t1);
      };
      // horse gallop (prefix p = Napoleon part prefix)
      const gallop = (t0, t1, p = "n", cyc = 0.2) => {
        const n = R(t1 - t0, cyc);
        [["-hFL", -30, 30], ["-hFR", 30, -30], ["-hBL", 25, -25], ["-hBR", -25, 25]].forEach(([l, a, b]) =>
          tl.fromTo(S + p + l, { rotation: a }, { rotation: b, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0));
        tl.fromTo(S + p + "-horse", { y: 0 }, { y: -18, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + p + "-cloak", { rotation: 0 }, { rotation: 10, transformOrigin: "100% 0%", duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.to([S + p + "-hFL", S + p + "-hFR", S + p + "-hBL", S + p + "-hBR"], { rotation: 0, duration: 0.15 }, t1);
      };
      const kickR = (at, p = "m") => {
        tl.to(S + p + "-legR", { rotation: 35, duration: 0.12, ease: "power2.in" }, at - 0.14);
        tl.to(S + p + "-legR", { rotation: -55, duration: 0.08, ease: "power3.out" }, at - 0.02);
        tl.to(S + p + "-legR", { rotation: 0, duration: 0.2 }, at + 0.1);
      };
      // parabolic flight of an element (offsets dx, dy, apex h)
      const arc = (sel, t0, d, dx, dy, h) => {
        const el = document.querySelector(sel), o = { p: 0 };
        tl.fromTo(o, { p: 0 }, { p: 1, duration: d, ease: "none", onUpdate() { const p = o.p; gsap.set(el, { x: dx * p, y: dy * p - 4 * h * p * (1 - p) }); } }, t0);
      };
      const stampIn = (at) => {
        tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "power4.in" }, at);
        tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, at + 0.18);
      };
      // crowd wave: row by row, the copies swap to the arms-crossed pose
      const crossWave = (name, rows, cols, t0, step = 0.25) => {
        for (let r = rows - 1; r >= 0; r--) for (let c = 0; c < cols; c++) {
          const at = t0 + (rows - 1 - r) * step + c * 0.03;
          if (!document.querySelector(S + name + r + "-" + c)) continue;
          tl.set(S + name + r + "-" + c, { opacity: 0 }, at); tl.set(S + name + "X" + r + "-" + c, { opacity: 1 }, at);
        }
      };
      const shakeCrowd = (sel, t0, d, amp = 4) => tl.fromTo(sel, { rotation: -amp }, { rotation: amp, transformOrigin: "50% 100%", duration: 0.2, yoyo: true, repeat: R(d, 0.2), ease: "sine.inOut" }, t0);
"""
