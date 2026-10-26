"""
Teams per league (data/teams/{league}.json, copied from RTYB) and the
keywords used to tag articles with them.

Tagging matches a team's nickname ("Maple Leafs", "Bruins") or full name,
plus its city only when no other team in the league shares it (so
"Chicago" doesn't tag both the Cubs and the White Sox). Matches are whole
words, case-insensitive, and only within the article's own league.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Extra names people use (lowercase).
ALIASES = {
    'nhl': {'MON': ['habs'], 'VGK': ['knights'], 'TOR': ['leafs'], 'CHI': ['hawks'], 'DET': ['wings'],
            'CAR': ['canes'], 'PIT': ['pens'], 'OTT': ['sens'], 'TB': ['bolts'], 'NSH': ['preds'], 'VAN': ['nucks'],
            'NYI': ['isles'], 'COL': ['avs'], 'WSH': ['caps'], 'CBJ': ['jackets', 'cbj'], 'SJ': ['sharks'], 'FLA': ['cats']},
    'nfl': {'sf': ['niners'], 'tb': ['bucs'], 'lac': ['bolts']},
    'nba': {'cle': ['cavs'], 'dal': ['mavs'], 'phi': ['sixers'], 'por': ['blazers'], 'min': ['wolves'], 'gs': ['dubs']},
    'mlb': {'ari': ['d-backs', 'dbacks'], 'ath': ["a's"], 'nyy': ['bronx bombers']},
}
# Nicknames that are everyday words: only count them next to the city.
WEAK = {'nhl': {'wild', 'stars'}, 'nba': {'heat', 'magic'}, 'nfl': set(), 'mlb': set()}


def load(league):
    path = os.path.join(ROOT, 'data', 'teams', f'{league}.json')
    teams = json.load(open(path, encoding='utf-8'))['teams']
    logos = {}
    lp = os.path.join(ROOT, 'data', 'teams', f'{league}-logos.json')
    if os.path.exists(lp):
        logos = json.load(open(lp, encoding='utf-8'))
    for t in teams:
        t['league'] = league
        if league == 'nhl':
            t['logo'] = {'light': f'nhl/{t["code"]}_light.svg', 'dark': f'nhl/{t["code"]}_dark.svg'}
        else:
            info = logos.get(t['slug'])
            t['logo'] = None if info is None else {'light': f'{league}/{t["slug"]}.png',
                                                    'dark': f'{league}/{t["slug"]}-dark.png' if info.get('dark') else None}
    return teams


def matchers(league, teams):
    """[(slug, compiled regex)] for one league."""
    cities = {}
    for t in teams:
        cities.setdefault((t.get('location') or '').lower(), []).append(t['slug'])
    out = []
    for t in teams:
        nick = (t.get('nickname') or t.get('short') or '').lower()
        loc = (t.get('location') or '').lower()
        words = {t['name'].lower(), f'{loc} {nick}'.strip()}
        if nick and nick not in WEAK.get(league, set()):
            words.add(nick)
        if loc and len(cities.get(loc, [])) == 1 and loc not in ('new york', 'los angeles'):
            words.add(loc)
        words |= set(ALIASES.get(league, {}).get(t.get('code') if league == 'nhl' else t['slug'], []))
        pat = r'(?<!\w)(' + '|'.join(re.escape(w) for w in sorted(words, key=len, reverse=True) if w) + r')(?!\w)'
        out.append((t['slug'], re.compile(pat, re.I)))
    return out


def tag(text, league_matchers):
    return [slug for slug, rx in league_matchers if rx.search(text or '')]
