# SnapBucket/snap

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/SnapBucket/snap/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/SnapBucket/snap/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One 1024x1024 front page that sums up the world news of Friday 20 November 2026:
27 stories across 7 regions and 10 fields, each labelled with how sure we are
and which outlets carried it. The date sits in a check panel that also lists
what we deliberately left out and what had not happened yet.

## Run it

```sh
python3 main.py /output
```

The picture is pre-rendered and committed as `entry.png`; `main.py` copies it
to the output directory, so the program needs no network and no packages.
`newsdata.py` holds the day's content and `render.py` draws the page.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
