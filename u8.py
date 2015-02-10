# -*- coding: UTF-8 -*-

import sys
import logging
import unicodedata
from collections import defaultdict
import HTMLParser


logger = logging.getLogger(__name__)


C_PUNCTUATION = frozenset(("Pc", "Pd", "Ps", "Pe", "Po", "Lm"))
C_QUOTE = frozenset(("Pi", "Pf"))
C_MARK = frozenset(("Mn", "Mc", "Me"))
C_SYMBOL = frozenset(("Sk", "So"))
C_CONTROL = frozenset(("Cc", "Cf", "Cs", "Co", "Cn"))

def get_unicode_ordinals_for_categories(categories=C_CONTROL):
    ordinals = []
    for category in categories:
        ordinals[len(ordinals):] = [o for o in range(sys.maxunicode + 1)
            if unicodedata.category(unichr(o)) == category]
    return frozenset(ordinals)


def get_valid_xml_unicode_ordinals():
    s = [i for i in range(0x20, 0xD7FF)]
    s[len(s):] = [i for i in range(0xE000, 0xFFFD)]
    s[len(s):] = [i for i in range(0x10000, 0x10FFFF)]
    s[len(s):] = [0x9, 0xA, 0xD]
    return frozenset(s)


def get_invalid_xml_unicode_ordinals():
    s = frozenset(range(0x0, 0x10FFFF)).difference(get_valid_xml_unicode_ordinals())
    return s


def get_translation_table():
    d = {}
    invalid = get_invalid_xml_unicode_ordinals()
    strip = get_unicode_ordinals_for_categories(C_PUNCTUATION.union(C_MARK).union(C_SYMBOL).union(C_CONTROL))
    d.update({c: None for c in invalid.union(strip)})
    quotes = get_unicode_ordinals_for_categories(C_QUOTE)
    d.update({c: u'"' for c in quotes})
    d.update({ord(u): u for u in u"\":;'-,.<>@=!?$%"}) # these characters should always be allowed
    return d

TRANSLATION_TABLE = get_translation_table()


def _is_sane_unicode(unicode_s=None):
    assert(type(unicode_s) is unicode)
    u = unicode_s.encode('utf-8', errors='strict').decode('utf-8', errors='strict')
    if unicode_s == u: return True
    return False

def _unicode_to_unicode(unicode_s=None):
    assert(type(unicode_s) is unicode)
    s = unicode.encode(unicode_s, 'utf-8', errors='replace')
    return _str_to_unicode(s)

def _str_to_unicode(str_s=None):
    assert(type(str_s) is str)
    u = unicode(str_s, 'utf-8', errors='replace').replace(u"\ufffd", u"?")
    return u

def to_unicode(data=None):
    """Converts input to unicode.

    Returned unicode can be idempotently converted to utf-8 string and
    back with 'errors' set to 'strict'. The conversion itself runs with
    'errors' set to 'replace', meaning all errors will be replaced with
    '?'.

    Args:
        data: str or unicode

    Returns:
        unicode

    Raises:
        TypeError, UnicodeError

    """
    sanitized = None

    if type(data) is unicode:
        sanitized = _unicode_to_unicode(unicode_s=data)
    elif type(data) is str:
        sanitized = _str_to_unicode(str_s=data)
    else:
        raise TypeError("input must be str or unicode")

    if not _is_sane_unicode(sanitized):
        raise UnicodeError("input cannot be converted")

    return sanitized


def unescape_html_entities(unicode_s=None):
    """Unescapes html entities in input unicode.

    Args:
        unicode_s: unicode

    Returns:
        unicode
    """
    h = HTMLParser.HTMLParser()
    u = h.unescape(unicode_s)
    return u


def normalize(unicode_s=None):
    """Normalizes unicode to NFKC form."""

    u = unicodedata.normalize('NFKC', unicode_s)
    return u


def simplify(unicode_s=None):
    """Strips unwanted characters."""

    u = unicode_s.translate(TRANSLATION_TABLE)
    return u


def u8(data):
    """Converts input into sanitized, normalized utf-8 string.

    Top level module function, call this unless you need fine-grained functionality.

    Args:
        data: str or unicode

    Returns:
        utf-8 encoded string. This string can be idempotently converted
        to and from unicode using 'strict' errors.

    Raises:
        TypeError, UnicodeError
    """
    u = to_unicode(data)
    u = unescape_html_entities(u)
    u = normalize(u)
    u = simplify(u)
    return u.encode('utf-8')

