# -*- coding: utf-8 -*-
import platform

is_mac = platform.system() == 'Darwin'
is_linux = platform.system() == 'Linux'
is_windows = platform.system() == 'Windows'


class Icons:
    is_mac = is_mac
    is_linux = is_linux
    is_windows = is_windows
    has_support = is_linux or is_mac

    # --------------------------------------- #

    EMPTY = '  '
    BOOK = '📒' if has_support else ''
    CLOVER = '🍀' if has_support else '#'
    LINK = '🔗' if has_support else '-'
    HANDS = '🙏' if has_support else '-'
    ERROR = '❗' if has_support else '!'
    PARTY = '📦' if has_support else '$'
    SOUND = '🔊' if has_support else '<<'
    SPARKLE = '✨' if has_support else '*'
    INFO = '💁  ' if has_support else ': '
    RIGHT_ARROW = '➡' if has_support else '->'
# end def
