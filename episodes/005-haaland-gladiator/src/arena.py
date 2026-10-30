"""Shared world for episode 005 (Haaland in the Colosseum).

Inside the Colosseum: Haaland left, opponents right, feet on y = GY. Below the captions: the arena sand (graphics only).
v2: the crowd-mood gauge was removed (creator: meters disturb the video); the crowd in the stands reacts instead.
"""
from scene import part  # noqa: F401

GY = 1150


def arena(sid):
    return part("colosseum", sid + "-col", GY=GY)


def haaland(sid, x=260, scale=1.15):
    return f'<g transform="translate({x},{GY})"><g id="{sid}-kwrap"><g transform="scale({scale})">{part("striker", sid + "-h")}</g></g></g>'


def fighter(sid, kind, name, x, scale=1.05):
    return f'<g transform="translate({x},{GY})"><g id="{sid}-{name}"><g transform="scale({scale})">{part(kind, sid + "-" + name + "p")}</g></g></g>'


MEDITATE_JS = """
      // sit down cross-legged and float a little (Haaland's meditation celebration)
      // v2: the hips drop to the ground and the legs cross IN FRONT (shins overlap) instead of splaying out;
      // hands rest on the knees. s = Haaland's scale (leg length ~92 px at scale 1).
      const meditate = (at, s = 1.15) => {
        const sit = 92 * s;
        tl.to(S + "kwrap", { y: sit, duration: 0.35, ease: "power2.inOut" }, at);
        tl.to(S + "h-legL", { rotation: -84, duration: 0.35 }, at);
        tl.to(S + "h-legR", { rotation: 84, duration: 0.35 }, at);
        tl.to(S + "h-armL", { rotation: -28, duration: 0.35 }, at + 0.1);
        tl.to(S + "h-armR", { rotation: 28, duration: 0.35 }, at + 0.1);
        tl.to(S + "h-lids", { opacity: 1, duration: 0.01 }, at + 0.4);
        tl.fromTo(S + "kwrap", { y: sit }, { y: sit - 22, duration: 0.9, ease: "sine.inOut", repeat: R(D - at - 0.4, 0.9), yoyo: true }, at + 0.4);
      };
      // the crowd in the stands jumps (replaces the old mood gauge)
      const cheer = (at, n = 3) => tl.fromTo(S + "col-crowd", { y: 0 }, { y: -14, duration: 0.14, yoyo: true, repeat: n * 2 - 1, ease: "power1.out" }, at);
"""
