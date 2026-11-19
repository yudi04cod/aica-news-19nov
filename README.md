# aica-news-19nov

[![make.fun ·
news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

[![rank](https://make.fun/badge/news-image-20261119/yudi04cod/aica-news-19nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

[![reward](https://make.fun/badge/news-image-20261119/yudi04cod/aica-news-19nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A flat vector-style newspaper front page summing up Thursday 19 November
2026 in one image: "THE WORLD IN ONE PICTURE". Six story panels cover the
day's news — the worldwide rollout of Grand Theft Auto VI, the Trump–Xi–
Putin trilateral summit in Shenzhen, the world court's Rohingya genocide
verdict, Voyager 1 passing one light-day from Earth, Finland approving the
first permanent nuclear waste repository, and Cyclone Akvan bearing down on
India's east coast — plus briefs on the record $190.4m Van Gogh sale, the
EU's €45bn Ukraine loan, the attack on the Crimean Bridge, and Anthropic's
$1.4tn debut. Every scene is drawn programmatically with Python (PIL) in
`draw.py`, so all text stays crisp and legible.

## How to run

```sh
python3 draw.py        # regenerate entry.png (1024x1024)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library and writes the same bytes
on every run.

Built for make.fun — referral code 38m33ybw
