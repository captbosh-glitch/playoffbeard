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
    # A classic ball, projected from a real truncated icosahedron (the shape of
    # a real ball) turned so a white hexagon faces front, with the three
    # black pentagons around it and slivers of the next ring at the edge.
    return (
            '<defs><clipPath id="pb-ball-clip"><circle cx="16" cy="16" r="13"/></clipPath></defs><circle class="bi-soccer-w'
            'hite" cx="16" cy="16" r="13"/><g clip-path="url(#pb-ball-clip)"><g class="bi-soccer-seam" stroke-width="0.8" s'
            'troke-linecap="round"><line x1="6.20" y1="24.49" x2="8.07" y2="24.49"/><line x1="13.55" y1="3.27" x2="12.61" y'
            '2="4.89"/><line x1="27.32" y1="13.38" x2="23.93" y2="10.75"/><line x1="27.32" y1="13.38" x2="28.25" y2="11.76"'
            '/><line x1="27.32" y1="13.38" x2="27.32" y2="18.62"/><line x1="23.93" y1="10.75" x2="20.54" y2="13.38"/><line '
            'x1="23.93" y1="10.75" x2="21.48" y2="6.51"/><line x1="28.25" y1="11.76" x2="25.80" y2="7.51"/><line x1="11.46"'
            ' y1="18.62" x2="16.00" y2="21.25"/><line x1="11.46" y1="18.62" x2="11.46" y2="13.38"/><line x1="11.46" y1="18.'
            '62" x2="7.49" y2="20.24"/><line x1="28.25" y1="20.24" x2="25.80" y2="24.49"/><line x1="28.25" y1="20.24" x2="2'
            '7.32" y2="18.62"/><line x1="20.54" y1="13.38" x2="20.54" y2="18.62"/><line x1="20.54" y1="13.38" x2="16.00" y2'
            '="10.75"/><line x1="13.55" y1="28.73" x2="12.61" y2="27.11"/><line x1="18.45" y1="28.73" x2="22.42" y2="27.11"'
            '/><line x1="3.75" y1="11.76" x2="3.17" y2="16.00"/><line x1="18.45" y1="3.27" x2="22.42" y2="4.89"/><line x1="'
            '8.07" y1="7.51" x2="6.20" y2="7.51"/><line x1="8.07" y1="7.51" x2="7.49" y2="11.76"/><line x1="8.07" y1="7.51"'
            ' x2="12.61" y2="4.89"/><line x1="25.80" y1="24.49" x2="22.42" y2="27.11"/><line x1="20.54" y1="18.62" x2="16.0'
            '0" y2="21.25"/><line x1="20.54" y1="18.62" x2="23.93" y2="21.25"/><line x1="3.75" y1="20.24" x2="3.17" y2="16.'
            '00"/><line x1="27.32" y1="18.62" x2="23.93" y2="21.25"/><line x1="16.00" y1="21.25" x2="16.58" y2="25.49"/><li'
            'ne x1="16.58" y1="6.51" x2="16.00" y2="10.75"/><line x1="16.58" y1="6.51" x2="12.61" y2="4.89"/><line x1="16.5'
            '8" y1="6.51" x2="21.48" y2="6.51"/><line x1="7.49" y1="11.76" x2="5.04" y2="16.00"/><line x1="7.49" y1="11.76"'
            ' x2="11.46" y2="13.38"/><line x1="5.04" y1="16.00" x2="3.17" y2="16.00"/><line x1="5.04" y1="16.00" x2="7.49" '
            'y2="20.24"/><line x1="11.46" y1="13.38" x2="16.00" y2="10.75"/><line x1="12.61" y1="27.11" x2="16.58" y2="25.4'
            '9"/><line x1="12.61" y1="27.11" x2="8.07" y2="24.49"/><line x1="22.42" y1="27.11" x2="21.48" y2="25.49"/><line'
            ' x1="23.93" y1="21.25" x2="21.48" y2="25.49"/><line x1="7.49" y1="20.24" x2="8.07" y2="24.49"/><line x1="16.58'
            '" y1="25.49" x2="21.48" y2="25.49"/><line x1="21.48" y1="6.51" x2="22.42" y2="4.89"/><line x1="25.80" y1="7.51'
            '" x2="22.42" y2="4.89"/></g><g class="bi-soccer-patch"><polygon points="16.00,10.75 20.54,13.38 23.93,10.75 21'
            '.48,6.51 16.58,6.51"/><polygon points="7.49,20.24 11.46,18.62 11.46,13.38 7.49,11.76 5.04,16.00"/><polygon poi'
            'nts="16.58,25.49 21.48,25.49 23.93,21.25 20.54,18.62 16.00,21.25"/><polygon points="9.58,27.11 13.55,28.73 12.'
            '61,27.11 8.07,24.49 6.20,24.49"/><polygon points="6.20,7.51 8.07,7.51 12.61,4.89 13.55,3.27 9.58,4.89"/><polyg'
            'on points="27.32,18.62 28.25,20.24 28.83,16.00 28.25,11.76 27.32,13.38"/></g></g><circle class="bi-soccer-edge'
            '" cx="16" cy="16" r="13" fill="none" stroke-width="1.3"/>')


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
