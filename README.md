# THE WORLD — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rehansky3-png/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rehansky3-png/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page summing up the world's news of Tuesday
24 November 2026, drawn entirely in code.

See the bounty: https://make.fun/bounty/news-image-20261124

## What the page shows

- **Masthead** — "Tuesday 24 November 2026" with the day's three big
  threads: Nvidia's 31% surge as Jensen Huang returns as CEO, Europe
  demanding a seat at the Ukraine peace talks, and an Israeli strike
  killing Hamas' internal security chief in Gaza.
- **3 illustrated lead panels** — the Nvidia rally, the Berlin Ukraine
  talks, and the Gaza strike.
- **The day in figures** — 700,000+ Russian soldiers killed in Ukraine;
  Nvidia +31% in a day; Nasdaq +6.5%; 26 dead in the Indonesia factory
  fire; 40 wounded in the Zaporizhzhia strike; 2.82m rials per dollar.
- **World map** — 15 labelled pins, from Washington to Shenzhen.
- **More of the day** — 40 more stories, from the Zaporizhzhia apartment
  strike and the Russian ships sunk off Libya to BepiColombo reaching
  Mercury orbit and Real Madrid's 5-1 Champions League win.

43 stories in total, every one of them happened, or was first reported,
on Tuesday 24 November 2026. Sources are named in the footer.

## How it is built

`build_image.py` draws the whole front page with Pillow: the masthead,
the three lead panels (illustrated images generated for this entry), the
figures strip, a world map rendered from Natural Earth land polygons
with the day's places pinned, and the 40-story grid. `main.py` copies
the finished `entry.png` to the grader's output directory — no network,
no randomness, byte-identical on every run.
