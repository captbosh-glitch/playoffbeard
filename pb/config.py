"""
Playoff Beard settings: the news feeds per league, how long articles are
kept, and the site's name and address. Add a feed by adding a line under
its league; add a league by adding a block here plus data/teams/{key}.json.
"""

SITE_NAME = 'Playoff Beard'
SITE_URL = 'https://playoffbeard.com'
# Set to 'playoffbeard.com' once the domain's DNS points at GitHub; while it's
# None the site previews at https://captbosh-glitch.github.io/playoffbeard/
CUSTOM_DOMAIN = 'playoffbeard.com'
TAGLINE = 'Every league’s headlines, every team’s news.'

# League order on the site: hockey first.
LEAGUES = [
    {'key': 'nhl', 'label': 'NHL', 'name': 'Hockey'},
    {'key': 'nfl', 'label': 'NFL', 'name': 'Football'},
    {'key': 'nba', 'label': 'NBA', 'name': 'Basketball'},
    {'key': 'mlb', 'label': 'MLB', 'name': 'Baseball'},
    {'key': 'ufc', 'label': 'UFC', 'name': 'MMA', 'noun': 'UFC and MMA'},
    {'key': 'soccer', 'label': 'Soccer', 'name': 'Soccer', 'noun': 'soccer'},
]

# Checked Oct 26, 2026. NHL.com has no native feed; to-rss.xyz regenerates
# one from nhl.com/news. Sportsnet's feed stopped updating (July 2025).
FEEDS = {
    'nhl': {
        'NHL.com': 'https://www.to-rss.xyz/nhl/news/',
        'ESPN': 'https://www.espn.com/espn/rss/nhl/news',
        'Yahoo Sports': 'https://sports.yahoo.com/nhl/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/nhl/',
    },
    'nfl': {
        'ESPN': 'https://www.espn.com/espn/rss/nfl/news',
        'Yahoo Sports': 'https://sports.yahoo.com/nfl/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/nfl/',
    },
    'nba': {
        'ESPN': 'https://www.espn.com/espn/rss/nba/news',
        'Yahoo Sports': 'https://sports.yahoo.com/nba/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/nba/',
    },
    'mlb': {
        'ESPN': 'https://www.espn.com/espn/rss/mlb/news',
        'Yahoo Sports': 'https://sports.yahoo.com/mlb/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/mlb',
    },
    # News-only for now (no team pages): checked Oct 26, 2026
    'ufc': {
        'ESPN': 'https://www.espn.com/espn/rss/mma/news',
        'Yahoo Sports': 'https://sports.yahoo.com/mma/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/mma/',
    },
    'soccer': {
        'ESPN': 'https://www.espn.com/espn/rss/soccer/news',
        'Yahoo Sports': 'https://sports.yahoo.com/soccer/rss.xml',
        'CBS Sports': 'https://www.cbssports.com/rss/headlines/soccer/',
    },
}

# Highlights: official league videos, played in place from YouTube. Each
# feed is a channel's long-form uploads (the "UULF" playlist skips Shorts);
# `match` keeps game highlights (UFC: full fights), `skip` drops repeats
# (the NBA's "EXTENDED" cuts). MLB posts game highlights in season only.
# Soccer has no single league channel. Checked Nov 7, 2026.
def _uploads(channel_id):
    return 'https://www.youtube.com/feeds/videos.xml?playlist_id=UULF' + channel_id[2:]


VIDEO_FEEDS = {
    'nhl': {'source': 'NHL', 'match': r'\| NHL Highlights \|', 'url': _uploads('UCqFMzb-4AUf6WAIbl132QKA')},
    'nfl': {'source': 'NFL', 'match': r'Game Highlights \| \d{4} NFL Season', 'url': _uploads('UCDVYQ4Zhbm3S2dlz7P1GBDg')},
    'nba': {'source': 'NBA', 'match': r'FULL GAME HIGHLIGHTS', 'skip': r'^EXTENDED', 'url': _uploads('UCWJ2lWNubArHWmf3FIHbfcQ')},
    'mlb': {'source': 'MLB', 'match': r'Game Highlights', 'url': _uploads('UCoLrcjPV5PbUrUyXq5mjc_A')},
    'ufc': {'source': 'UFC', 'match': r'\| FULL FIGHT \|', 'url': _uploads('UCvgfXK4nTYKudb0rFR6noLA'), 'heading': 'Full fights'},
}
VIDEO_KEEP_DAYS = 14    # highlights older than this drop out of data/videos.json
HIGHLIGHTS_ROW = 12     # newest highlights in a league page's row (a team page shows 6)
VIDEO_PAIR_HOURS = 12   # a story shows a highlight of its team's game within this many hours

KEEP_DAYS = 30          # articles older than this drop out of data/articles.json
LEAGUE_PAGE_LIMIT = 60  # newest articles on a league page
HOME_PER_LEAGUE = 8     # per league on the home page
TEAM_PAGE_LIMIT = 40    # newest articles on a team page
