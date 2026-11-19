# news-image-20261119

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/rank/hyde1990.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

"Three Powers in Shenzhen" — a newspaper front page summing up the world
news of Thursday 19 November 2026 in a single 1024x1024 image, drawn
entirely with code (Pillow shapes and typography, no photos).

The seven stories: the first-ever three-way Trump–Xi–Putin summit in
Shenzhen; the ICJ ruling that Myanmar committed genocide against the
Rohingya; Ukraine's third strike on the Kerch Bridge in a week; Iran's
attacks on Gulf states and the Houthi rocket that damaged Riyadh's PIF
Tower; the Bangladesh lockdown and arson ahead of Sheikh Hasina's planned
return; Anthropic's record $81.3 billion IPO; and the launch of Grand
Theft Auto VI. The ticker adds the COP31 deadlock and the IEA's Hormuz
warning, a record $190.4 million Van Gogh sale, and Cyclone Akvan.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` to `out/entry.png`.

## Reproduce the image

```sh
python3 generate.py
```

`generate.py` (Python 3, Pillow only, deterministic — fixed seed, no
network, no clock) redraws `entry.png` from scratch.

Entered on [make.fun](https://make.fun/?ref=sqhp9r4t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards
