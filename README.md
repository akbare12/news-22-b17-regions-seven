[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b17-regions-seven/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b17-regions-seven/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

A one-page newspaper front page summing up Sunday 22 November 2026 in 36 stories
across 7 regions, drawn with PIL (`draw.py`, standard library + Pillow at build time
only; the submitted program itself is stdlib-only).

## The day

- **COP31 Antalya collapses — NO DEAL.** The final text dropped all fossil-fuel
  language; the EU and ~130 parties rejected it; the $120bn adaptation target was
  dropped; the 35% electricity-2035 target was kept. First failure since 2009.
- **Russia fires 186 drones at Ukraine overnight; 161 shot down or jammed.**
  A five-storey block in Dymer falls: 1 dead, 14 unaccounted for. Strikes hit
  18 sites.
- **Iran claims 2 US Patriot radars hit in Bahrain** (al-Riffa and Awali);
  Bahrain denies a military strike — a civilian site at Sitra burns, 2 hurt,
  no deaths. Labelled CLAIM.

The page also carries a kanon number strip (186 / 161 / 720/9 / 98.79% / $120bn /
35% / 44h / 50 / 258), a colour region bar with story counts, a "THE DAY IN UTC"
strip, 10 small illustrated cards, a world map with 36 numbered pins, an
"ALSO ON SUNDAY" list grouped by region, and a red DATE CHECK box that names
what was left out (with dates) and what is not yet decided — so nothing dated
19–21 November is presented as Sunday news.

## How it is built

`draw.py` draws `entry.png` (1024×1024, < 1 MiB) with PIL. `main.py` copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG header, dimensions and
sha256 — it never writes anything next to itself.

Scenes are drawn illustrations, not photographs.

## License

MIT — see `LICENSE`.
