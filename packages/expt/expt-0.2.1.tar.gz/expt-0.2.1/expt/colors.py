import sys
_thismodule = sys.modules[__name__]

# populate all matplotlib named colors as module attributes.
# https://matplotlib.org/examples/color/named_colors.html
from matplotlib import colors as mcolors
_colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

for color_name in _colors:
    setattr(_thismodule, color_name, color_name)

del sys
del _thismodule


# Sensible default color sets that are more distinguishable: 17 colors
# https://matplotlib.org/3.1.0/gallery/color/named_colors.html
DefaultColors = (
    'dimgray',
    'dodgerblue',
    'limegreen',
    'coral',
    'gold',
    'lightpink',
    'brown',
    'red',
    'purple',
    'green',
    'cadetblue',
    'burlywood',
    'royalblue',
    'violet',
    'lightseagreen',
    'yellowgreen',
    'sandybrown',
)

# 20 Distinct Colors Palette by Sasha Trubetskoy: 17 colors
# (Except for white, gray, and black that are quite invisible)
# https://sashamaps.net/docs/tools/20-colors/
Trubetskoy17 = (
    '#800000',   # Maroon (99.99%)
    '#4363d8',   # Blue (99.99%)
    '#ffe119',   # Yellow (99.99%)
    '#e6beff',   # Lavender (99.99%)
    '#f58231',   # Orange (99.99%)
    '#3cb44b',   # Green (99%)
    '#000075',   # Navy (99.99%)
    '#e6194b',   # Red (99%)
    '#46f0f0',   # Cyan (99%)
    '#f032e6',   # Magenta (99%)
    '#9a6324',   # Brown (99%)
    '#008080',   # Teal (99%)
    '#911eb4',   # Purple (95%*)
    '#aaffc3',   # Mint (99%)
    '#ffd8b1',   # Apiroct (95%)
    '#bcf60c',   # Lime (95%)
    '#fabed4',   # Pink (99%)
    '#808000',   # Olive (95%)
    '#fffac8',   # Beige (99%)
    #'#a9a9a9',
    #'#ffffff',
    #'#000000'
)


try:
    from pandas.plotting._matplotlib.style import _get_standard_colors
except:
    # support older pandas version as well
    from pandas.plotting._style import _get_standard_colors

get_standard_colors = _get_standard_colors
