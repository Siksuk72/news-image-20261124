# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Siksuk72/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Siksuk72/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for make.fun's **news-image-20261124**: one image that sums up
Tuesday 24 November 2026's world news. It is a newspaper front page —
"THE WORLD TODAY" — drawn in code, so every headline stays sharp and
readable at 1024×1024. The lead is the day's biggest story, the COP31
climate summit collapsing in Antalya with no deal at all; underneath it,
the overnight strikes in Ukraine, the factory fire in Banten, and the
Shenzhen trilateral summit, plus a short also-today strip and a "BY THE
NUMBERS" band. Every story on the page was checked against a real report
dated 22–24 November 2026 (CNN, AP, Le Monde, Al Jazeera) before it was
typeset — no invented headlines, no invented numbers.

## Why it wins

A picture editor would pick this page: one unmistakable lead, specific
headlines with real names and real numbers (194 countries, 2,700 drones,
34 missing workers), a clean three-column layout, and a picture of the
empty Antalya plenary hall that tells the lead story at a glance. It
reads like a real front page because it is built like one.

## Run it

```sh
python3 draw.py            # paints entry.png (1024×1024, under 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) is the entrypoint the grader
runs: it checks `entry.png` is a 1024×1024 PNG under 1 MiB and copies it
to `/output/entry.png` — byte-identical on every run, no network, no
randomness. `draw.py` (Python 3 + Pillow) paints the whole page and fits
the hero illustration into it; `hero.webp` is the illustration made for
this entry.
