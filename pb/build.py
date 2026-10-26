"""
Builds the static site in docs/ (GitHub Pages serves that folder at
playoffbeard.com) from data/articles.json:

  docs/index.html                 latest headlines, every league
  docs/{league}/index.html        a league's news + its teams by division
  docs/{league}/{team}/index.html a team's news
  docs/assets/style.css, logos    (logos copied from RTYB)

Headlines link out to the publisher. Times are shown relative ("3h ago")
by a little script, with the ET time as the fallback.
"""
import html
import json
import os
import shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from pb import config, teams as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
ET = ZoneInfo('America/New_York')


def esc(s):
    return html.escape('' if s is None else str(s), quote=True)


def et_time(iso):
    t = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(ET)
    return t.strftime('%b %-d, %-I:%M %p ET')


def logo(team, depth, size=28):
    if not team or not team.get('logo'):
        code = esc((team or {}).get('code') or '?')
        return f'<span class="logo logo-fallback" style="width:{size}px;height:{size}px">{code}</span>'
    l = team['logo']
    light = f'{depth}assets/logos/{l["light"]}'
    if not l.get('dark'):
        return f'<span class="logo" style="width:{size}px;height:{size}px"><img src="{light}" alt="" loading="lazy"></span>'
    dark = f'{depth}assets/logos/{l["dark"]}'
    return (f'<span class="logo" style="width:{size}px;height:{size}px"><img class="lg-light" src="{light}" alt="" loading="lazy">'
            f'<img class="lg-dark" src="{dark}" alt="" loading="lazy"></span>')


BEARD = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">'
         '<path d="M6 9c0 9 3 17 10 20 7-3 10-11 10-20-2 3-5 4-10 4S8 12 6 9z" fill="currentColor"/>'
         '<path d="M11 18c2 1.5 8 1.5 10 0" stroke="var(--bg)" stroke-width="2" fill="none" stroke-linecap="round"/></svg>')


def page(title, desc, body, depth, current='home', updated=''):
    nav = [('home', 'Home', f'{depth}' or './')] + [(lg['key'], lg['label'], f'{depth}{lg["key"]}/') for lg in config.LEAGUES]
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if key == current else ""}>{esc(lbl)}</a>' for key, lbl, href in nav)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{depth}assets/style.css">
<script>try{{var t=localStorage.getItem('pb-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="{depth or './'}">{BEARD}<span>Playoff <b>Beard</b></span></a>
  <nav class="nav" aria-label="Leagues">{links}</nav>
  <button class="theme" id="themeBtn" type="button" aria-label="Toggle light / dark">&#9681;</button>
</div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap">
  <p>Headlines link to their publishers (NHL.com, ESPN, Yahoo Sports, CBS Sports). Playoff Beard collects and sorts them; it doesn&rsquo;t host articles.</p>
  <p class="muted">{esc(updated)}</p>
</div></footer>
<script>
(function() {{
  var root = document.documentElement;
  document.getElementById('themeBtn').onclick = function() {{
    var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try {{ localStorage.setItem('pb-theme', next); }} catch (e) {{}}
  }};
  var now = Date.now();
  document.querySelectorAll('time[datetime]').forEach(function(el) {{
    var m = Math.round((now - Date.parse(el.getAttribute('datetime'))) / 60000);
    if (isNaN(m) || m < 0) return;
    el.textContent = m < 1 ? 'just now' : m < 60 ? m + 'm ago' : m < 1440 ? Math.round(m / 60) + 'h ago' : Math.round(m / 1440) + 'd ago';
  }});
}})();
</script>
</body>
</html>
'''


def lead_first(items):
    """The newest story with a photo leads (the big card); the rest stay newest first."""
    i = next((n for n, a in enumerate(items[:6]) if a.get('image')), None)
    if i is None:
        return items, False
    return [items[i]] + items[:i] + items[i + 1:], True


def card(a, teams_by, depth, big=False, show_league=False):
    lg = next(l for l in config.LEAGUES if l['key'] == a['league'])
    chips = ''
    for slug in a['teams'][:4]:
        t = teams_by[a['league']].get(slug)
        if t:
            chips += f'<a class="chip" href="{depth}{a["league"]}/{t["slug"]}/">{logo(t, depth, 18)}{esc(t.get("nickname") or t["name"])}</a>'
    img = f'<a class="thumb" href="{esc(a["url"])}" target="_blank" rel="noopener"><img src="{esc(a["image"])}" alt="" loading="lazy"></a>' if a.get('image') else ''
    meta = ((f'<a class="lg" href="{depth}{lg["key"]}/">{esc(lg["label"])}</a> · ' if show_league else '') +
            f'{esc(a["source"])} · <time datetime="{esc(a["published"])}">{esc(et_time(a["published"]))}</time>')
    return (f'<article class="card{" big" if big else ""}{" has-img" if img else ""}">{img}<div class="c-body">'
            f'<div class="meta">{meta}</div>'
            f'<h3><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])}</a></h3>'
            + (f'<p>{esc(a["summary"])}</p>' if a.get('summary') and a['summary'] != a['title'] else '')
            + (f'<div class="chips">{chips}</div>' if chips else '') + '</div></article>')


def team_grid(league, teams, depth, counts):
    groups = {}
    for t in teams:
        groups.setdefault(t.get('division') or t.get('conference') or 'Teams', []).append(t)
    out = ''
    for g in sorted(groups):
        tiles = ''.join(f'<a class="tile" href="{depth}{league}/{t["slug"]}/">{logo(t, depth, 30)}<span>{esc(t.get("nickname") or t["name"])}</span>'
                        f'<small>{counts.get(t["slug"], 0)}</small></a>' for t in sorted(groups[g], key=lambda x: x['name']))
        out += f'<div class="div-group"><h4>{esc(g)}</h4><div class="tiles">{tiles}</div></div>'
    return out


def write(rel, html_text):
    path = os.path.join(DOCS, rel, 'index.html') if rel else os.path.join(DOCS, 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_text)


def build(now=None):
    now = now or datetime.now(timezone.utc)
    articles = json.load(open(os.path.join(ROOT, 'data', 'articles.json'), encoding='utf-8'))
    updated = 'Updated ' + now.astimezone(ET).strftime('%b %-d, %Y, %-I:%M %p ET')
    teams = {lg['key']: T.load(lg['key']) for lg in config.LEAGUES}
    teams_by = {k: {t['slug']: t for t in v} for k, v in teams.items()}
    by_league = {lg['key']: [a for a in articles if a['league'] == lg['key']] for lg in config.LEAGUES}

    # home
    secs = ''
    for lg in config.LEAGUES:
        items = by_league[lg['key']][:config.HOME_PER_LEAGUE]
        if not items:
            continue
        items, lead = lead_first(items)
        cards = ''.join(card(a, teams_by, '', big=(lead and i == 0)) for i, a in enumerate(items))
        secs += (f'<section class="sec"><div class="sec-head"><h2>{esc(lg["label"])}</h2>'
                 f'<a href="{lg["key"]}/">All {esc(lg["label"])} news &rarr;</a></div><div class="grid">{cards}</div></section>')
    hero = (f'<section class="hero"><h1>Playoff <span>Beard</span></h1><p>{esc(config.TAGLINE)}</p>'
            f'<div class="hero-links">' + ''.join(f'<a href="{lg["key"]}/">{esc(lg["label"])}</a>' for lg in config.LEAGUES) + '</div></section>')
    write('', page(f'{config.SITE_NAME} — Hockey first, every league’s headlines', config.TAGLINE, hero + secs, '', 'home', updated))

    # leagues and teams
    for lg in config.LEAGUES:
        key, items = lg['key'], by_league[lg['key']]
        counts = {}
        for a in items:
            for s in a['teams']:
                counts[s] = counts.get(s, 0) + 1
        shown, lead = lead_first(items[:config.LEAGUE_PAGE_LIMIT])
        cards = ''.join(card(a, teams_by, '../', big=(lead and i == 0)) for i, a in enumerate(shown))
        body = (f'<section class="lg-head"><h1>{esc(lg["label"])} <span>News</span></h1>'
                f'<p>{len(items)} headlines in the last {config.KEEP_DAYS} days from {esc(", ".join(config.FEEDS[key]))}.</p></section>'
                f'<details class="teams-box" open><summary>Teams</summary>{team_grid(key, teams[key], "../", counts)}</details>'
                f'<section class="sec"><div class="grid">{cards or "<p class=muted>No headlines yet.</p>"}</div></section>')
        write(key, page(f'{lg["label"]} News — {config.SITE_NAME}', f'The latest {lg["label"]} headlines from around the league.', body, '../', key, updated))
        for t in teams[key]:
            mine, lead = lead_first([a for a in items if t['slug'] in a['teams']][:config.TEAM_PAGE_LIMIT])
            rivals = [x for x in teams[key] if x.get('division') and x.get('division') == t.get('division') and x['slug'] != t['slug']]
            riv = ''.join(f'<a class="chip" href="../{x["slug"]}/">{logo(x, "../../", 18)}{esc(x.get("nickname") or x["name"])}</a>' for x in rivals)
            body = (f'<a class="back" href="../">&larr; All {esc(lg["label"])} news</a>'
                    f'<section class="team-head">{logo(t, "../../", 64)}<div><h1>{esc(t["name"])}</h1>'
                    f'<p>{esc(" · ".join(filter(None, [t.get("division"), t.get("conference")])))}</p></div></section>'
                    + (f'<div class="chips rivals"><span class="muted">Division:</span>{riv}</div>' if riv else '') +
                    f'<section class="sec"><div class="grid">'
                    + (''.join(card(a, teams_by, '../../', big=(lead and i == 0)) for i, a in enumerate(mine)) or
                       f'<p class="muted">No {esc(t["name"])} headlines in the last {config.KEEP_DAYS} days.</p>') + '</div></section>')
            write(f'{key}/{t["slug"]}', page(f'{t["name"]} News — {config.SITE_NAME}', f'The latest {t["name"]} headlines.', body, '../../', key, updated))

    # static bits
    for f in ('style.css', 'favicon.svg'):
        shutil.copy(os.path.join(ROOT, 'pb', 'static', f), os.path.join(DOCS, 'assets', f))
    with open(os.path.join(DOCS, 'CNAME'), 'w') as f:
        f.write('playoffbeard.com\n')
    open(os.path.join(DOCS, '.nojekyll'), 'w').close()
    print(f'built: home, {len(config.LEAGUES)} leagues, {sum(len(v) for v in teams.values())} team pages')
