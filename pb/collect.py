"""
Collects every league's feeds into data/articles.json:
  [{id, league, source, title, url, summary, image, published (UTC ISO),
    collected (UTC ISO), teams [slugs]}]
Deduped by canonical URL and by headline (the same story from two feeds),
tagged with teams (teams.py), and trimmed to config.KEEP_DAYS.
"""
import hashlib
import html
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urlunparse

import feedparser

from pb import config, images, teams as T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'data', 'articles.json')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) PlayoffBeard/1.0'


def canonical(url):
    p = urlparse(url or '')
    return urlunparse((p.scheme or 'https', p.netloc.lower(), p.path.rstrip('/'), '', '', ''))


def headline_key(title):
    return re.sub(r'[^a-z0-9]+', ' ', (title or '').lower()).strip()


def clean(text, limit=320):
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text or ''))
    text = re.sub(r'\s+', ' ', text).strip()
    return text if len(text) <= limit else text[:limit].rsplit(' ', 1)[0] + '…'


def image_of(e):
    for key in ('media_content', 'media_thumbnail'):
        for m in e.get(key) or []:
            if m.get('url'):
                return m['url']
    for l in e.get('links') or []:
        if (l.get('type') or '').startswith('image/') and l.get('href'):
            return l['href']
    m = re.search(r'<img[^>]+src="([^"]+)"', e.get('summary') or '')
    return m.group(1) if m else None


def when(e, now):
    for key in ('published_parsed', 'updated_parsed'):
        t = e.get(key)
        if t:
            dt = datetime(*t[:6], tzinfo=timezone.utc)
            return min(dt, now).strftime('%Y-%m-%dT%H:%M:%SZ')
    return now.strftime('%Y-%m-%dT%H:%M:%SZ')   # no date in the feed: first seen


def load():
    if os.path.exists(PATH):
        return json.load(open(PATH, encoding='utf-8'))
    return []


def collect(now=None):
    now = now or datetime.now(timezone.utc)
    articles = load()
    seen_url = {a['id'] for a in articles}
    seen_head = {(a['league'], headline_key(a['title'])) for a in articles}
    added = {}
    for lg in config.LEAGUES:
        key = lg['key']
        m = T.matchers(key, T.load(key))
        for source, url in config.FEEDS.get(key, {}).items():
            feed = feedparser.parse(url, agent=UA)
            if feed.get('bozo') and not feed.entries:
                print(f'  WARN {key} {source}: {feed.get("bozo_exception")}', file=sys.stderr)
                continue
            for e in feed.entries:
                link = canonical(e.get('link'))
                title = clean(e.get('title'), 200)
                if not link or not title:
                    continue
                aid = hashlib.sha1(link.encode()).hexdigest()[:12]
                hk = (key, headline_key(title))
                if aid in seen_url or hk in seen_head:
                    continue
                summary = clean(e.get('summary') or e.get('description'))
                articles.append({
                    'id': aid, 'league': key, 'source': source, 'title': title, 'url': e.get('link'),
                    'summary': summary, 'image': image_of(e), 'published': when(e, now),
                    'collected': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    # the headline names the teams; the summary only when it names none
                    # (feed summaries often carry a blog's name, e.g. "Avalanche News")
                    'teams': T.tag(title, m) or T.tag(summary, m),
                })
                seen_url.add(aid)
                seen_head.add(hk)
                added[key] = added.get(key, 0) + 1
    cutoff = (now - timedelta(days=config.KEEP_DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
    articles = [a for a in articles if a['published'] >= cutoff]
    articles.sort(key=lambda a: a['published'], reverse=True)
    images.fill(articles)
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=0, ensure_ascii=False)
    print(f'collected: {sum(added.values())} new ({", ".join(f"{k} {v}" for k, v in added.items()) or "none"}), {len(articles)} kept')
    return articles
