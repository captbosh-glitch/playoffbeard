"""
Fills in photos the feeds leave out. ESPN and Yahoo RSS carry no images, so:
  ESPN   the story id in the URL -> ESPN's news API (its pages block scripts)
  Yahoo  the article page's og:image share photo (some stories have none)
Each story is looked up once ('img_tried'), newest first, capped per run.
"""
import json
import re
import sys
import urllib.request

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
PER_RUN = 120
ESPN_ID = re.compile(r'espn\.com/.*/(?:story|id)/_/id/(\d+)|espn\.com/.*/_/id/(\d+)')
OG_IMAGE = re.compile(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]*content=["\']([^"\']+)'
                      r'|<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']og:image["\']')


def get(url, limit=None):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read(limit).decode('utf-8', 'ignore')


def espn_image(url):
    m = ESPN_ID.search(url)
    if not m:
        return None
    d = json.loads(get(f'https://content.core.api.espn.com/v1/sports/news/{m.group(1) or m.group(2)}'))
    for h in d.get('headlines') or []:
        for img in h.get('images') or []:
            if img.get('url'):
                return img['url']
    return None


def og_image(url):
    m = OG_IMAGE.search(get(url, 600_000))
    return (m.group(1) or m.group(2)).replace('&amp;', '&') if m else None


FINDERS = {'ESPN': espn_image, 'Yahoo Sports': og_image}


def fill(articles):
    todo = [a for a in articles if not a.get('image') and not a.get('img_tried') and a['source'] in FINDERS]
    found = 0
    for a in todo[:PER_RUN]:
        a['img_tried'] = True
        try:
            a['image'] = FINDERS[a['source']](a['url'])
        except Exception as e:   # a dead link or a blocked page: leave it photo-less
            print(f'  WARN image {a["source"]} {a["url"]}: {e}', file=sys.stderr)
        found += bool(a.get('image'))
    if todo:
        print(f'images: {found} found of {min(len(todo), PER_RUN)} looked up ({max(len(todo) - PER_RUN, 0)} left for next run)')
    return articles
