"""Cold open for episode 012: the domino moment (Romans toppling column by column, Messi dribbling in front), used as
the first frame of s1 and again as the last frame of s6, so the loop closes with a hard cut on the same picture."""
from battle import army, ball, field, messi, army_defs  # noqa: F401

TITLE_CSS = """
    .title { position: absolute; left: 40px; right: 40px; top: 330px; text-align: center; font: 900 104px/0.98 "Inter";
             color: #ffd23f; -webkit-text-stroke: 7px #1a1a2e; paint-order: stroke fill; letter-spacing: -0.01em; }
    .title b { color: #f4efe6; }
    .rew { position: absolute; left: 380px; top: 760px; padding: 10px 26px; border-radius: 16px; background: #1a1a2e; color: #f4efe6;
           font: 900 64px/1 "Inter"; opacity: 0; }"""


def title(sid):
    return f'\n    <div class="title" id="{sid}-title">MESSI <b>vs.</b><br>380,000<br>ROMANS</div>'


def cold_world(sid, name="a", hidden=False):
    """Messi in front of the legion; the legion copies are sid-<name><r>-<c> (see cold_js)."""
    return (f'<g id="{sid}-cold" opacity="{0 if hidden else 1}">' + field(sid + "-" + name + "f") + army_defs(sid)
            + army(sid, 470, cols=6, rows=5, dx=110, name=name)
            + messi(sid + "-" + name, 260) + ball(sid + "-" + name, 306) + "</g>")


def cold_js(name="a", t0=0.0, freeze=False):
    """Domino state as a function of time: column c, row r topples at st = c*0.22 + r*0.08 - 0.55 (some already down at t=0).
    freeze=True: show the state at t=0 statically from t0 on (for the last frame of the episode)."""
    return f"""
      for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++) {{
        const el = S + "{name}" + r + "-" + c, st = c * 0.22 + r * 0.08 - 0.55, d = 0.35;
        const at0 = Math.max(0, Math.min(1, -st / d)) * 74;
        if ({str(freeze).lower()}) {{ tl.set(el, {{ rotation: at0, transformOrigin: "50% 100%" }}, {t0}); continue; }}
        if (st + d <= 0) tl.set(el, {{ rotation: 74, transformOrigin: "50% 100%" }}, {t0});
        else if (st < 0) tl.fromTo(el, {{ rotation: at0 }}, {{ rotation: 74, transformOrigin: "50% 100%", duration: st + d, ease: "power2.in" }}, {t0});
        else tl.fromTo(el, {{ rotation: 0 }}, {{ rotation: 74, transformOrigin: "50% 100%", duration: d, ease: "power2.in", immediateRender: false }}, {t0} + st);
      }}"""
