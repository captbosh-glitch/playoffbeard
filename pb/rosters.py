"""
Builds the "teams" for the leagues RTYB doesn't cover, refreshed once a day:
  soccer  Premier League + MLS clubs (ESPN), logos saved to docs/assets/logos/soccer/
  ufc     the UFC weight classes, with the champion and top 15 from UFC.com's
          official rankings; articles are tagged by weight class or ranked fighter
A failed fetch keeps the previous file, so a site outage never empties a league.
"""
import html
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAMS = os.path.join(ROOT, 'data', 'teams')
LOGOS = os.path.join(ROOT, 'docs', 'assets', 'logos', 'soccer')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
MAX_AGE = timedelta(hours=20)


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def words_pattern(words):
    return r'(?<!\w)(' + '|'.join(re.escape(w) for w in sorted(set(words), key=len, reverse=True)) + r')(?!\w)'


def ascii_fold(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


# ---- soccer ---------------------------------------------------------------

COMPETITIONS = [('eng.1', 'Premier League'), ('usa.1', 'MLS')]
# ESPN abbreviation -> (slug, short name, words that mean this club in a headline).
# Hand-picked: ESPN's nicknames ("Blues", "Reds", "United") are too vague.
CLUBS = {
    'eng.1': {
        'ARS': ('arsenal', 'Arsenal', ['arsenal', 'gunners']),
        'AVL': ('aston-villa', 'Aston Villa', ['aston villa']),
        'BOU': ('bournemouth', 'Bournemouth', ['bournemouth', 'cherries']),
        'BRE': ('brentford', 'Brentford', ['brentford']),
        'BHA': ('brighton', 'Brighton', ['brighton']),
        'BUR': ('burnley', 'Burnley', ['burnley']),
        'CHE': ('chelsea', 'Chelsea', ['chelsea']),
        'COV': ('coventry', 'Coventry', ['coventry']),
        'CRY': ('crystal-palace', 'Crystal Palace', ['crystal palace']),
        'EVE': ('everton', 'Everton', ['everton', 'toffees']),
        'FUL': ('fulham', 'Fulham', ['fulham']),
        'HUL': ('hull', 'Hull City', ['hull city']),
        'IPS': ('ipswich', 'Ipswich', ['ipswich']),
        'LEE': ('leeds', 'Leeds', ['leeds']),
        'LEI': ('leicester', 'Leicester', ['leicester']),
        'LIV': ('liverpool', 'Liverpool', ['liverpool']),
        'MNC': ('man-city', 'Man City', ['man city', 'manchester city']),
        'MAN': ('man-utd', 'Man United', ['man utd', 'man united', 'manchester united']),
        'NEW': ('newcastle', 'Newcastle', ['newcastle', 'magpies']),
        'NFO': ('nottm-forest', "Nott'm Forest", ['nottingham forest', "nott'm forest", 'nottm forest']),
        'SOU': ('southampton', 'Southampton', ['southampton']),
        'SUN': ('sunderland', 'Sunderland', ['sunderland']),
        'TOT': ('tottenham', 'Spurs', ['tottenham', 'spurs']),
        'WHU': ('west-ham', 'West Ham', ['west ham']),
        'WOL': ('wolves', 'Wolves', ['wolves', 'wolverhampton']),
    },
    'usa.1': {
        'ATL': ('atlanta-united', 'Atlanta United', ['atlanta united']),
        'ATX': ('austin', 'Austin FC', ['austin fc']),
        'MTL': ('montreal', 'CF Montréal', ['cf montréal', 'cf montreal']),
        'CLT': ('charlotte', 'Charlotte FC', ['charlotte fc']),
        'CHI': ('chicago-fire', 'Chicago Fire', ['chicago fire']),
        'COL': ('colorado', 'Rapids', ['colorado rapids', 'rapids']),
        'CLB': ('columbus', 'Crew', ['columbus crew']),
        'DC': ('dc-united', 'D.C. United', ['d.c. united', 'dc united']),
        'CIN': ('cincinnati', 'FC Cincinnati', ['fc cincinnati']),
        'DAL': ('dallas', 'FC Dallas', ['fc dallas']),
        'HOU': ('houston', 'Dynamo', ['houston dynamo', 'dynamo']),
        'MIA': ('inter-miami', 'Inter Miami', ['inter miami']),
        'LA': ('la-galaxy', 'Galaxy', ['la galaxy', 'galaxy']),
        'LAFC': ('lafc', 'LAFC', ['lafc', 'los angeles fc']),
        'MIN': ('minnesota', 'Minnesota United', ['minnesota united', 'loons']),
        'NSH': ('nashville', 'Nashville SC', ['nashville sc']),
        'NE': ('new-england', 'Revolution', ['new england revolution', 'revs']),
        'NYC': ('nycfc', 'NYCFC', ['nycfc', 'new york city fc', 'nyc fc']),
        'ORL': ('orlando', 'Orlando City', ['orlando city']),
        'PHI': ('philadelphia', 'Union', ['philadelphia union']),
        'POR': ('portland', 'Timbers', ['portland timbers', 'timbers']),
        'RSL': ('real-salt-lake', 'Real Salt Lake', ['real salt lake', 'rsl']),
        'RBNY': ('red-bulls', 'Red Bulls', ['red bulls', 'red bull new york']),
        'SD': ('san-diego', 'San Diego FC', ['san diego fc']),
        'SJ': ('san-jose', 'Earthquakes', ['san jose earthquakes', 'earthquakes']),
        'SEA': ('seattle', 'Sounders', ['seattle sounders', 'sounders']),
        'SKC': ('sporting-kc', 'Sporting KC', ['sporting kansas city', 'sporting kc', 'skc']),
        'STL': ('st-louis', 'St. Louis City', ['st. louis city', 'st louis city', 'st. louis city sc']),
        'TOR': ('toronto', 'Toronto FC', ['toronto fc']),
        'VAN': ('vancouver', 'Whitecaps', ['vancouver whitecaps', 'whitecaps']),
    },
}


def soccer():
    teams, logos = [], {}
    os.makedirs(LOGOS, exist_ok=True)
    for comp, comp_name in COMPETITIONS:
        base = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{comp}'
        conf = {}
        if comp == 'usa.1':   # MLS clubs play in two conferences
            for c in json.loads(get(f'https://site.api.espn.com/apis/v2/sports/soccer/{comp}/standings')).get('children', []):
                for e in c['standings']['entries']:
                    conf[e['team']['id']] = c['name']
        for x in json.loads(get(f'{base}/teams'))['sports'][0]['leagues'][0]['teams']:
            t = x['team']
            # a club promoted after this list was written still gets a page
            slug, short, words = CLUBS[comp].get(t['abbreviation']) or (
                re.sub(r'[^a-z0-9]+', '-', t['shortDisplayName'].lower()).strip('-'), t['shortDisplayName'], [t['shortDisplayName'].lower()])
            teams.append({'code': t['abbreviation'], 'name': t['displayName'], 'nickname': short, 'slug': slug,
                          'competition': comp_name, 'division': comp_name, 'conference': conf.get(t['id']),
                          'pattern': words_pattern(words + [t['displayName'].lower()])})
            have = {}
            for variant, suffix in (('500', ''), ('500-dark', '-dark')):
                path = os.path.join(LOGOS, f'{slug}{suffix}.png')
                if not os.path.exists(path):
                    try:
                        img = get(f'https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/{variant}/{t["id"]}.png&w=128&h=128')
                    except urllib.error.HTTPError:   # some clubs have no dark-mode logo
                        continue
                    open(path, 'wb').write(img)
                have[suffix] = open(path, 'rb').read()
            if '' in have:
                logos[slug] = {'dark': '-dark' in have and have['-dark'] != have['']}
    json.dump(logos, open(os.path.join(TEAMS, 'soccer-logos.json'), 'w'), indent=0)
    return teams


# ---- UFC -------------------------------------------------------------------

WEIGHT_CLASSES = [   # (UFC.com heading, slug, code, limit in lb)
    ('Flyweight', 'flyweight', 'FLW', 125), ('Bantamweight', 'bantamweight', 'BW', 135),
    ('Featherweight', 'featherweight', 'FW', 145), ('Lightweight', 'lightweight', 'LW', 155),
    ('Welterweight', 'welterweight', 'WW', 170), ('Middleweight', 'middleweight', 'MW', 185),
    ('Light Heavyweight', 'light-heavyweight', 'LHW', 205), ('Heavyweight', 'heavyweight', 'HW', 265),
    ("Women's Strawweight", 'womens-strawweight', 'W-SW', 115), ("Women's Flyweight", 'womens-flyweight', 'W-FLW', 125),
    ("Women's Bantamweight", 'womens-bantamweight', 'W-BW', 135),
]


def class_pattern(name):
    """The weight class in a headline, without "light heavyweight" counting as
    heavyweight or "women's flyweight" as the men's flyweight."""
    if name.startswith("Women's "):
        return r"women['’]?s " + re.escape(name.split(' ', 1)[1].lower())
    guard = r"(?<!women's )(?<!women’s )(?<!womens )"
    if name == 'Heavyweight':
        guard += r'(?<!light )(?<!light-)'
    return guard + re.escape(name.lower())


def ufc():
    page = get('https://www.ufc.com/rankings').decode('utf-8', 'ignore')
    page = page.split('meta_rankings')[0]   # the official rankings; a sponsored list follows
    found = {}
    for blk in page.split('class="view-grouping"')[1:]:
        head = re.search(r'view-grouping-header">\s*([^<]+)', blk)
        if not head:
            continue
        champ = re.search(r'<h5>\s*<a[^>]*>([^<]+)</a>', blk)
        ranked = re.findall(r'views-field-title[^>]*>\s*<a[^>]*>([^<]+)</a>', blk)
        found[html.unescape(head.group(1)).strip()] = {
            'champion': html.unescape(champ.group(1)).strip() if champ else None,
            'ranked': [html.unescape(n).strip() for n in ranked]}
    if not all(w[0] in found for w in WEIGHT_CLASSES):
        raise ValueError(f'UFC.com rankings changed shape: found {sorted(found)}')
    # a fighter's last name counts when no other ranked fighter shares it
    every = [n for w in WEIGHT_CLASSES for n in [found[w[0]]['champion']] + found[w[0]]['ranked'] if n]
    last = {}
    for n in set(every):
        if ' ' in n:
            ln = n.split(' ', 1)[1].lower()
            last[ln] = last.get(ln, 0) + 1
    teams = []
    for name, slug, code, lb in WEIGHT_CLASSES:
        r = found[name]
        alts = [class_pattern(name)]
        for n in [r['champion']] + r['ranked']:
            if not n:
                continue
            names = {n.lower(), ascii_fold(n).lower()}
            ln = n.split(' ', 1)[1].lower() if ' ' in n else ''
            if len(ln) >= 5 and last.get(ln) == 1:
                names |= {ln, ascii_fold(ln)}
            alts += [re.escape(x) for x in names]
        teams.append({'code': code, 'name': name, 'nickname': name, 'slug': slug,
                      'division': "Women's divisions" if name.startswith('Women') else "Men's divisions",
                      'conference': f'Up to {lb} lb', 'champion': r['champion'], 'ranked': r['ranked'],
                      'pattern': r'(?<!\w)(' + '|'.join(alts) + r')(?!\w)'})
    return teams


# ---- refresh ---------------------------------------------------------------

BUILDERS = {'soccer': soccer, 'ufc': ufc}


def refresh(force=False, now=None):
    now = now or datetime.now(timezone.utc)
    for league, build in BUILDERS.items():
        path = os.path.join(TEAMS, f'{league}.json')
        old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
        stamp = old.get('updated')
        if not force and old.get('teams') and stamp and now - datetime.fromisoformat(stamp) < MAX_AGE:
            continue
        try:
            teams = build()
        except Exception as e:
            print(f'  WARN rosters {league}: {e}', file=sys.stderr)
            continue
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'sport': league, 'updated': now.isoformat(timespec='seconds'), 'teams': teams}, f, indent=1, ensure_ascii=False)
        print(f'rosters: {league} {len(teams)} teams')


if __name__ == '__main__':
    refresh(force=True)
