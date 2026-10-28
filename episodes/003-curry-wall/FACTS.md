# Fakten – 003 Could Steph Curry make a three over the Great Wall of China?

| Im Video | Wert | Quelle / Rechenweg |
|----------|------|--------------------|
| Curry height | 1.88 m (6 ft 2 in) | offizielle NBA-Angabe |
| 4,000 three-pointers | erster Spieler mit 4.000 Dreiern (14. März 2025) | https://abc7news.com/post/golden-state-warriors-stephen-curry-becomes-1st-player-nba-make-4000-3-pointers/16019671/ |
| Release angle ~52° | Schätzungen 50–60° | https://www.spin.ph/basketball/nba/science-explains-steph-curry-s-picture-perfect-form-adv-con, https://www.scu.edu/illuminate/thought-leaders/phil-kesten/the-science-behind-the-warriors-3-point-shots.html |
| Three-point distance | 7.24 m (23 ft 9 in) | NBA-Regel |
| Rim height | 3.05 m | Regel |
| Wall height | bis ~7 m (Ming-Mauer im Schnitt 6–7 m) | Survey 2009, z. B. https://chinahighlights.com/greatwall/fact/great-wall-length.htm |
| Wall thickness | 4–5 m | dito |
| Wall length | 21,196 km | Survey 2012, https://www.cbc.ca/news/world/great-wall-of-china-even-longer-than-previously-thought-1.1263111 |

## Physik (`src/shot.py`, nur Schwerkraft, kein Luftwiderstand)
Abwurf bei (0.15 m, 2.4 m), Korb 7.24 m entfernt auf 3.05 m. Mauer mittig: Oberkante 7 m, oben 4.5 m breit (1.37–5.87 m).
- Normaler Wurf 52°: v ≈ 8.8 m/s, Scheitel 4.9 m → trifft die Mauer nach 0.2 s auf ~4 m Höhe ("~5 m apex").
- Über die Mauer: kleinste Geschwindigkeit bei 76.7° (gerundet 77°), v = 12.7 m/s = 45.8 km/h (gerundet 46 km/h), Scheitel 10.1 m, Flugzeit 2.45 s (normal 1.3 s → "double").
- Bolts Spitzengeschwindigkeit 44.7 km/h (siehe Folge 002) → "faster than Usain Bolt".
- Bei gleicher Geschwindigkeit 1° steiler → 51 cm zu kurz. Ringradius 22.5 cm minus Ballradius 12 cm ≈ 10 cm Spielraum → ±0.2°.
- Ball holen: halbe Mauerlänge 10,598 km bei 5 km/h = 2,120 h = 88 Tage.
- "Chance per shot: 2 %" ist eine Schätzung als Gag (Karte sagt "EST.").
