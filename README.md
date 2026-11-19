[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Hunter-donot/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/Hunter-donot/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

# THE WORLD — 18 November 2026

A one-page newspaper front page summing up Wednesday 18 November 2026's
world news: the US strikes on Iran as the Gulf war flares, Xi and Putin
meeting in Shenzhen as APEC opens, Nvidia's $115.8 billion quarter, plus
9 more stories and 24 briefs from across the world.

`render_18nov.py` draws the page with PIL and real TTF fonts
(Noto Serif Display Black masthead, Noto Serif headlines/body,
DejaVu Sans kickers) and writes `entry.png` (1024x1024).
`main.py` copies it to `/output/entry.png`.

Run: `python3 render_18nov.py` once, then `python3 main.py`.
