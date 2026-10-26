"""
League icons, the same ones RTYB uses: the puck (NHL), the NFL ball (no
stripes), the basketball (NBA) and the baseball (MLB), in full color, plus
Playoff Beard's own soccer ball and MMA glove in the same style. The
colors are CSS classes on the --ball-* tokens in pb/static/style.css, so
the outlines adapt to light and dark mode.

  sport_icon('nhl') -> inline <svg>
"""


def puck():
    ticks = ''.join(f'<line x1="{x}" y1="15.2" x2="{x}" y2="20.6"/>' for x in (5, 8.7, 12.4, 16, 19.6, 23.3, 27))
    return ('<ellipse class="bi-puck-side" cx="16" cy="21" rx="14.5" ry="6"/>'
            '<rect class="bi-puck-side" x="1.5" y="12" width="29" height="9"/>'
            f'<g class="bi-puck-grip" stroke-width="1" stroke-linecap="round">{ticks}</g>'
            '<ellipse class="bi-puck-top" cx="16" cy="12" rx="14.5" ry="6"/>'
            '<ellipse class="bi-puck-shine" cx="12" cy="10.6" rx="5.5" ry="1.8"/>'
            '<path class="bi-rim" d="M1.5 12 V21 A14.5 6 0 0 0 30.5 21 V12" fill="none" stroke-width="1"/>')


def football(stripes=True):
    laces = ''.join(f'<line x1="{x}" y1="14.4" x2="{x}" y2="17.6"/>' for x in (12.6, 14.9, 17.1, 19.4))
    # Rotated and scaled up so it fills the same box as the round balls.
    return ('<g transform="rotate(-35 16 16) translate(16 16) scale(1.16) translate(-16 -16)">'
            # light outline under the leather (like the puck's rim) so it shows on dark
            '<path class="bi-leather-rim" d="M2.5 16 Q16 3 29.5 16 Q16 29 2.5 16 Z" fill="none" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path class="bi-leather" d="M2.5 16 Q16 3 29.5 16 Q16 29 2.5 16 Z" stroke-width="1" stroke-linejoin="round"/>'
            + ('<path class="bi-stripe" d="M7.2 11.4 Q8.7 16 7.2 20.6 M24.8 11.4 Q23.3 16 24.8 20.6" fill="none" stroke-width="1.4"/>' if stripes else '') +
            f'<g class="bi-lace" stroke-width="1.2" stroke-linecap="round"><line x1="11.3" y1="16" x2="20.7" y2="16"/>{laces}</g>'
            '</g>')


def basketball():
    return ('<circle class="bi-basketball" cx="16" cy="16" r="13" stroke-width="1.1"/>'
            '<g class="bi-seam" fill="none" stroke-width="1.3" stroke-linecap="round">'
            '<line x1="16" y1="3" x2="16" y2="29"/><line x1="3" y1="16" x2="29" y2="16"/>'
            '<path d="M7.2 6.4 Q12.5 16 7.2 25.6"/><path d="M24.8 6.4 Q19.5 16 24.8 25.6"/></g>')


def baseball():
    return ('<circle class="bi-baseball" cx="16" cy="16" r="13" stroke-width="1.1"/>'
            '<g class="bi-stitch" fill="none" stroke-linecap="round">'
            '<path d="M8.6 5.4 Q14.2 16 8.6 26.6" stroke-width="1"/>'
            '<path d="M23.4 5.4 Q17.8 16 23.4 26.6" stroke-width="1"/>'
            '<path d="M8.6 5.4 Q14.2 16 8.6 26.6" stroke-width="2.6" stroke-dasharray="0.9 1.9" stroke-linecap="butt" opacity="0.9"/>'
            '<path d="M23.4 5.4 Q17.8 16 23.4 26.6" stroke-width="2.6" stroke-dasharray="0.9 1.9" stroke-linecap="butt" opacity="0.9"/>'
            '</g>')


def soccer_ball():
    # a white ball, black center pentagon and five edge patches (clipped to
    # the ball), seams joining them; outline on the --ball-white-edge token
    return ('<defs><clipPath id="pb-ball-clip"><circle cx="16" cy="16" r="13"/></clipPath></defs>'
            '<circle class="bi-baseball" cx="16" cy="16" r="13" stroke-width="1.1"/>'
            '<g class="bi-soccer-patch" clip-path="url(#pb-ball-clip)">'
            '<polygon points="16.00,11.40 20.37,14.58 18.70,19.72 13.30,19.72 11.63,14.58"/>'
            '<polygon points="20.70,9.53 19.39,5.50 22.82,3.02 26.24,5.50 24.93,9.53"/>'
            '<polygon points="23.61,18.47 27.03,15.98 30.46,18.47 29.15,22.50 24.92,22.50"/>'
            '<polygon points="16.00,24.00 19.42,26.49 18.12,30.51 13.88,30.51 12.58,26.49"/>'
            '<polygon points="8.39,18.47 7.08,22.50 2.85,22.50 1.54,18.47 4.97,15.98"/>'
            '<polygon points="11.30,9.53 7.07,9.53 5.76,5.50 9.18,3.02 12.61,5.50"/></g>'
            '<g class="bi-soccer-seam" stroke-width="1" stroke-linecap="round">'
            '<line x1="16" y1="11.4" x2="16" y2="7.4"/><line x1="20.37" y1="14.58" x2="24.18" y2="13.34"/>'
            '<line x1="18.7" y1="19.72" x2="21.05" y2="22.96"/><line x1="13.3" y1="19.72" x2="10.95" y2="22.96"/>'
            '<line x1="11.63" y1="14.58" x2="7.82" y2="13.34"/></g>'
            '<circle class="bi-baseball-edge" cx="16" cy="16" r="13" fill="none" stroke-width="1.1"/>')


def fight_glove():
    # an open-finger MMA glove from the front: a wide fist with finger slits
    # and a thumb crease, on a wrist cuff with a white strap; rim on the
    # puck-rim token so it shows on dark
    return ('<path class="bi-glove" d="M6 13 C6 7 10 4 16 4 C22 4 26.5 7 26.5 13 L26.5 17 C26.5 20 24.5 21.5 22 21.5 L10 21.5 C7.6 21.5 6 19.8 6 17.5 Z" stroke-width="1"/>'
            '<g class="bi-glove-slit" fill="none" stroke-width="1.1" stroke-linecap="round">'
            '<line x1="11.5" y1="5" x2="11.5" y2="8.8"/><line x1="15" y1="4.4" x2="15" y2="8.4"/>'
            '<line x1="18.5" y1="4.4" x2="18.5" y2="8.4"/><line x1="22" y1="5" x2="22" y2="8.8"/>'
            '<path d="M7.2 15.4 C9.6 13.8 12.6 14.2 13.8 17.2"/></g>'
            '<rect class="bi-glove" x="8" y="21" width="16.5" height="8" rx="2.5" stroke-width="1"/>'
            '<rect class="bi-glove-strap" x="7.4" y="23.4" width="17.7" height="3.4" rx="1.2"/>')

ICONS = {'nhl': lambda: puck(), 'nfl': lambda: football(stripes=False), 'nba': basketball, 'mlb': baseball,
         'ufc': fight_glove, 'soccer': soccer_ball}


def sport_icon(league, cls=''):
    draw = ICONS.get(league)
    if not draw:
        return ''
    return (f'<svg class="sport-icon{" " + cls if cls else ""}" viewBox="1 1 30 30" '
            f'aria-hidden="true" focusable="false">{draw()}</svg>')
