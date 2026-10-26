"""
Playoff Beard: collect every feed, then rebuild the site in docs/.
  python3 run.py           # collect + build
  python3 run.py build     # rebuild only (no fetching)
"""
import sys

from pb import build, collect

if __name__ == '__main__':
    if 'build' not in sys.argv[1:]:
        collect.collect()
    build.build()
