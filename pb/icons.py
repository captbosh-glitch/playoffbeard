"""
League icons, the same ones RTYB uses: the puck (NHL), the NFL ball (no
stripes), the basketball (NBA) and the baseball (MLB), in full color. The
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


ICONS = {'nhl': lambda: puck(), 'nfl': lambda: football(stripes=False), 'nba': basketball, 'mlb': baseball}


def sport_icon(league, cls=''):
    draw = ICONS.get(league)
    if not draw:
        return ''
    return (f'<svg class="sport-icon{" " + cls if cls else ""}" viewBox="1 1 30 30" '
            f'aria-hidden="true" focusable="false">{draw()}</svg>')
