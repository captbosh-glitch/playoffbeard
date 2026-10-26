# Playoff Beard

Sports news at [playoffbeard.com](https://playoffbeard.com): the
latest NHL, NFL, NBA and MLB headlines from NHL.com, ESPN, Yahoo Sports and CBS
Sports, sorted by league and tagged by team. Headlines link to the publisher.

## How it works

- `pb/collect.py` reads every feed in `pb/config.py`, removes duplicates (same
  link or same headline), tags each article with the teams its headline names
  (`pb/teams.py`), and keeps the last 30 days in `data/articles.json`.
- `pb/build.py` writes the static site to `docs/`: the home page, a page per
  league (with its teams by division) and a page per team.
- `.github/workflows/update.yml` runs both every hour and commits the result;
  GitHub Pages serves `docs/` at playoffbeard.com.

Run it locally:

```bash
pip install -r requirements.txt
python3 run.py          # collect + build
python3 run.py build    # rebuild only
open docs/index.html
```

## Changing things

- **Feeds:** `FEEDS` in `pb/config.py`.
- **Teams:** `data/teams/{league}.json` (names, divisions); logos in
  `docs/assets/logos/`. Nicknames fans use ("Habs", "Canes") are `ALIASES` in
  `pb/teams.py`.
- **Look:** `pb/static/style.css` (colors are tokens at the top, with dark mode).

## One-time setup (GitHub + domain)

1. Repo **Settings → Pages**: Source "Deploy from a branch", branch `main`,
   folder `/docs`. Until the domain is ready the site previews at
   https://captbosh-glitch.github.io/playoffbeard/.
3. When DNS is set: `CUSTOM_DOMAIN = 'playoffbeard.com'` in `pb/config.py`
   (the build writes `docs/CNAME`), push, then tick **Enforce HTTPS** in
   Settings → Pages once it's offered.
2. At the domain registrar, DNS for `playoffbeard.com`:
   - `A` records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `CNAME` for `www`: `captbosh-glitch.github.io`
