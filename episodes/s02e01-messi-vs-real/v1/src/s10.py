import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s10-ft"
D = TIMING[sid]["duration"]
w = world(sid, lineup(sid, FEET, 0.5) + messi_fig(sid, 540, FEET + 160, 0.72, name="m")) + closeup(sid)
rows = [("PLAYERS", "11", "1"), ("GOALS", "2", "3"), ("ONE-TWOS WITH AN AD BOARD", "0", "1"), ("LACES TIED", "0", "1"), ("SHIRTS SHOWN", "0", "1")]
cards = (hud(sid, h=2, a=3, minute="FT") + fulltime(sid, rows)
         + card(sid, "mlc", "MOST LIKED COMMENT", "Decides the next case ↓", 120, 980, "gold")
         + slam(sid, "s1", "PRIME<br>MESSI", 430, 150))
js = JS + CLOSE_JS + """
      crowdIdle(); stamina(3);
      tl.set(S + "cu", { opacity: 0 }, 0);
      tl.fromTo(S + "ft", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, 0.15);
      fly("mlc", C.mlc, null);
      // last 0.4 s: the cold-open picture again (Messi juggling, PRIME MESSI) - the loop closes on the same frame
      const CUT = D - 0.4;
      tl.set([S + "ft", S + "c-mlc", S + "hud", S + "stambox"], { opacity: 0 }, CUT);
      tl.set(S + "cu", { opacity: 1 }, CUT);
      tl.set(S + "s1", { opacity: 1, scale: 1.12, rotation: -3, transformOrigin: "50% 50%" }, CUT);
"""
scene(sid, w, js, cards, extra_css=CSS, loop_out="cut")
