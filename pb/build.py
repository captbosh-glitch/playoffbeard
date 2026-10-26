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

from pb import config, icons, teams as T

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


def page(title, desc, body, depth, current='home', updated=''):
    nav = [('home', 'Home', f'{depth}' or './')] + [(lg['key'], lg['label'], f'{depth}{lg["key"]}/') for lg in config.LEAGUES]
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if key == current else ""}>{icons.sport_icon(key)}{esc(lbl)}</a>' for key, lbl, href in nav)
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
<body class="{'lg-' + current if current != 'home' else 'home'}">
<header class="top"><div class="wrap top-in">
  <a class="brand" href="{depth or './'}" aria-label="Playoff Beard home">Playoff <b>Beard</b></a>
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


NHL_SIZES = [('t_ratio16_9-size30', 624), ('t_ratio16_9-size40', 832), ('t_ratio16_9-size50', 1280), ('t_ratio16_9-size60', 1920)]
CBS_WIDTHS = [640, 960, 1280, 1920]


def img_html(url, big):
    """The photo with a srcset, so the browser loads the sharpest size the
    card needs on this screen. Feeds send small (NHL.com: 416px) or huge (CBS:
    full-size originals) images; both servers can resize on request."""
    sizes = '(max-width: 600px) 100vw, 66vw' if big else '(max-width: 600px) 100vw, (max-width: 900px) 50vw, 33vw'
    if 'media.d3.nhle.com' in url and '/t_ratio16_9-size' in url:
        pre, rest = url.split('/t_ratio16_9-size', 1)
        rest = rest.split('/', 1)[1]
        srcset = ', '.join(f'{pre}/{t}/{rest} {w}w' for t, w in NHL_SIZES)
        src = f'{pre}/{NHL_SIZES[2 if big else 1][0]}/{rest}'
    elif 'cbsistatic.com' in url and '?' not in url:
        srcset = ', '.join(f'{url}?width={w} {w}w' for w in CBS_WIDTHS)
        src = f'{url}?width={1280 if big else 640}'
    else:
        return f'<img src="{esc(url)}" alt="" loading="lazy">'
    return f'<img src="{esc(src)}" srcset="{esc(srcset)}" sizes="{sizes}" alt="" loading="lazy" decoding="async">'


def lead_first(items):
    """The newest story with a photo leads (the big card); the rest stay newest first."""
    i = next((n for n, a in enumerate(items) if a.get('image')), None)
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
    img = f'<a class="thumb" href="{esc(a["url"])}" target="_blank" rel="noopener">{img_html(a["image"], big)}</a>' if a.get('image') else ''
    meta = ((f'<a class="lg" href="{depth}{lg["key"]}/">{esc(lg["label"])}</a> · ' if show_league else '') +
            f'{esc(a["source"])} · <time datetime="{esc(a["published"])}">{esc(et_time(a["published"]))}</time>')
    return (f'<article class="card{" big" if big else ""}{" has-img" if img else ""}">{img}<div class="c-body">'
            f'<div class="meta">{meta}</div>'
            f'<h3><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])}</a></h3>'
            + (f'<p>{esc(a["summary"])}</p>' if a.get('summary') and a['summary'] != a['title'] else '')
            + (f'<div class="chips">{chips}</div>' if chips else '') + '</div></article>')


def day_sections(items, teams_by, depth):
    """Stories grouped by day (ET), each section laid out like a home-page
    league section: a photo story leads, the rest follow newest first."""
    today = datetime.now(timezone.utc).astimezone(ET).date()
    days = {}
    for a in items:
        d = datetime.fromisoformat(a['published'].replace('Z', '+00:00')).astimezone(ET).date()
        days.setdefault(d, []).append(a)
    out = ''
    for d in sorted(days, reverse=True):
        label = 'Today' if d == today else 'Yesterday' if (today - d).days == 1 else d.strftime('%A, %b %-d')
        shown, lead = lead_first(days[d])
        cards = ''.join(card(a, teams_by, depth, big=(lead and i == 0)) for i, a in enumerate(shown))
        out += (f'<section class="sec"><div class="sec-head"><h2>{esc(label)}</h2><span class="sec-n">{len(shown)} '
                f'{"story" if len(shown) == 1 else "stories"}</span></div><div class="grid">{cards}</div></section>')
    return out


def logo_row(league, teams, depth):
    """Every team's logo in one row (alphabetical), each linking to its page."""
    return (f'<nav class="logo-row lr-{league}" aria-label="Teams">' + ''.join(
        f'<a href="{depth}{league}/{t["slug"]}/" title="{esc(t["name"])}" aria-label="{esc(t["name"])}">{logo(t, depth, 30)}</a>'
        for t in sorted(teams, key=lambda x: x['name'])) + '</nav>')


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
        secs += (f'<section class="sec lg-{lg["key"]}"><div class="sec-head"><h2>{icons.sport_icon(lg["key"])}{esc(lg["label"])}</h2>'
                 f'<a href="{lg["key"]}/">All {esc(lg["label"])} news &rarr;</a></div><div class="grid">{cards}</div></section>')
    hero = (f'<section class="hero"><h1>Playoff <span>Beard</span></h1><p>{esc(config.TAGLINE)}</p>'
            f'<div class="hero-links">' + ''.join(f'<a href="{lg["key"]}/">{icons.sport_icon(lg["key"])}{esc(lg["label"])}</a>' for lg in config.LEAGUES) + '</div></section>')
    write('', page(f'{config.SITE_NAME} — Hockey first, every league’s headlines', config.TAGLINE, hero + secs, '', 'home', updated))

    # leagues and teams
    for lg in config.LEAGUES:
        key, items = lg['key'], by_league[lg['key']]
        counts = {}
        for a in items:
            for s in a['teams']:
                counts[s] = counts.get(s, 0) + 1
        hero = (f'<section class="hero"><h1>{icons.sport_icon(key, "hero-icon")}{esc(lg["label"])} <span>News</span></h1>'
                f'<p>The latest {esc(lg["name"].lower())} headlines from {esc(", ".join(config.FEEDS[key]))}.</p>'
                f'{logo_row(key, teams[key], "../")}</section>')
        body = hero + (day_sections(items[:config.LEAGUE_PAGE_LIMIT], teams_by, '../') or '<p class="muted">No headlines yet.</p>')
        write(key, page(f'{lg["label"]} News — {config.SITE_NAME}', f'The latest {lg["label"]} headlines from around the league.', body, '../', key, updated))
        for t in teams[key]:
            mine = [a for a in items if t['slug'] in a['teams']][:config.TEAM_PAGE_LIMIT]
            rivals = [x for x in teams[key] if x.get('division') and x.get('division') == t.get('division') and x['slug'] != t['slug']]
            riv = ''.join(f'<a href="../{x["slug"]}/">{logo(x, "../../", 20)}{esc(x.get("nickname") or x["name"])}</a>' for x in rivals)
            loc, nick = t.get('location') or '', t.get('nickname') or ''
            title = (f'{esc(loc)} <span>{esc(nick)}</span>' if loc and nick and t['name'] == f'{loc} {nick}' else esc(t['name']))
            hero = (f'<section class="hero team-hero"><a class="back" href="../">{icons.sport_icon(key)}All {esc(lg["label"])} news</a>'
                    f'<div class="team-title">{logo(t, "../../", 84)}<h1>{title}</h1></div>'
                    f'<p>{esc(" · ".join(filter(None, [t.get("division"), t.get("conference")])))} &middot; {len(mine)} headline{"" if len(mine) == 1 else "s"} in the last {config.KEEP_DAYS} days</p>'
                    + (f'<div class="hero-links rivals">{riv}</div>' if riv else '') + '</section>')
            # teams get a few stories a day: one section, like a home-page league section
            shown, lead = lead_first(mine)
            latest = (f'<section class="sec"><div class="sec-head"><h2>Latest {esc(nick or t["name"])} news</h2>'
                      f'<span class="sec-n">{len(shown)} {"story" if len(shown) == 1 else "stories"}</span></div><div class="grid">'
                      + ''.join(card(a, teams_by, '../../', big=(lead and i == 0)) for i, a in enumerate(shown)) + '</div></section>') if shown else ''
            body = hero + (latest or
                           f'<p class="muted">No {esc(t["name"])} headlines in the last {config.KEEP_DAYS} days.</p>')
            write(f'{key}/{t["slug"]}', page(f'{t["name"]} News — {config.SITE_NAME}', f'The latest {t["name"]} headlines.', body, '../../', key, updated))

    # static bits
    for f in ('style.css', 'favicon.svg'):
        shutil.copy(os.path.join(ROOT, 'pb', 'static', f), os.path.join(DOCS, 'assets', f))
    cname = os.path.join(DOCS, 'CNAME')
    if config.CUSTOM_DOMAIN:
        with open(cname, 'w') as f:
            f.write(config.CUSTOM_DOMAIN + '\n')
    elif os.path.exists(cname):
        os.remove(cname)
    open(os.path.join(DOCS, '.nojekyll'), 'w').close()
    print(f'built: home, {len(config.LEAGUES)} leagues, {sum(len(v) for v in teams.values())} team pages')
