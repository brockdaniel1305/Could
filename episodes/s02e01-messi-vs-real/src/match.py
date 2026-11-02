"""Shared pieces for S2E01 (Messi alone vs Real Madrid at the Bernabéu), built on tools/stadium.py."""
from stadium import *  # noqa: F401,F403

LINE_X = [60 + i * 96 for i in range(11)]


def world(sid, inner, zoom=None):
    """Stadium + pitch + whatever the scene adds, inside a zoomable group sid-zoom (zoom = (x, y, scale) for a static close-up)."""
    tr = f' transform="translate({zoom[0]},{zoom[1]}) scale({zoom[2]}) translate({-zoom[0]},{-zoom[1]})"' if zoom else ""
    return f'<g id="{sid}-zoomwrap"{tr}><g id="{sid}-zoom">' + stands(sid) + boards(sid) + pitch(sid) + inner + "</g></g>"


def lineup(sid, y=FEET, s=0.5, prefix="r"):
    return "".join(player(sid, f"{prefix}{i}", x, y, s, num=n, **REAL) for i, (x, n) in enumerate(zip(LINE_X, REAL_NUMS)))


def closeup(sid, name="cu"):
    """The cold-open picture: Messi juggling in close-up in front of the stands (frame 0 and the loop's last frame)."""
    inner = messi_fig(sid, 540, FEET + 40, 0.62, name=name + "m", tag=False) + football(sid, 590, FEET - 120, 0.6, name=name + "b")
    return f'<g id="{sid}-{name}">' + world(sid + "-" + name, inner, zoom=(540, 1100, 2.3)) + "</g>"


CLOSE_JS = """
      // close-up juggling: the ball bounces between Messi's foot and knee
      const juggle = (pre, t0, d) => { tl.fromTo(S + pre + "b", { y: 0 }, { y: -110, duration: 0.28, ease: "power2.out", yoyo: true, repeat: R(d, 0.28) }, t0);
        tl.fromTo(S + pre + "b-spin", { rotation: 0 }, { rotation: 360, duration: 0.56, ease: "none", repeat: R(d, 0.56), transformOrigin: "50% 50%" }, t0);
        tl.fromTo(S + pre + "m-legR", { rotation: 0 }, { rotation: -30, duration: 0.28, ease: "power2.in", yoyo: true, repeat: R(d, 0.28) }, t0); };
"""
