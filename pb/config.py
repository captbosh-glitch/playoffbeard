"""
Playoff Beard settings: the news feeds per league, how long articles are
kept, and the site's name and address. Add a feed by adding a line under
its league; add a league by adding a block here plus data/teams/{key}.json.
"""

SITE_NAME = 'Playoff Beard'
SITE_URL = 'https://playoffbeard.com'
# Set to 'playoffbeard.com' once the domain's DNS points at GitHub; while it's
# None the site previews at https://captbosh-glitch.github.io/playoffbeard/
CUSTOM_DOMAIN = None
TAGLINE = 'Hockey first. Every league’s headlines, every team’s news.'

# League order on the site: hockey first.
LEAGUES = [
    {'key': 'nhl', 'label': 'NHL', 'name': 'Hockey'},
    {'key': 'nfl', 'label': 'NFL', 'name': 'Football'},
    {'key': 'nba', 'label': 'NBA', 'name': 'Basketball'},
    {'key': 'mlb', 'label': 'MLB', 'name': 'Baseball'},
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
}

KEEP_DAYS = 30          # articles older than this drop out of data/articles.json
LEAGUE_PAGE_LIMIT = 60  # newest articles on a league page
HOME_PER_LEAGUE = 8     # per league on the home page
TEAM_PAGE_LIMIT = 40    # newest articles on a team page
