# SnapBucket/snap

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/SnapBucket/snap/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/SnapBucket/snap/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One 1024x1024 front page that sums up the world news of Saturday 21 November
2026: 34 stories across 7 regions and 10 fields, each labelled with how sure we
are and which outlets carried it. The date sits at the top in the largest type
on the page; a check panel lists what we deliberately left out and what had not
happened yet.

## Run it

```sh
python3 main.py /output
```

The picture is pre-rendered and committed as `entry.png`; `main.py` copies it
to the output directory, so the program needs no network and no packages.
`newsdata.py` holds the day's content and `render.py` draws the page.

`render.py` measures the page as it draws it and refuses to save if a string
would be clipped, a box would leave the canvas, any two strings would overlap,
type would drop below 12 px, or the date's letters would be under 48 px tall.
It prints each band's height and the slack left at the bottom.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
