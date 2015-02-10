# -*- coding: UTF-8 -*-

import sys
import os
import unittest
import unicodedata

import u8


class UnicTest(unittest.TestCase):

    def test_unescape_html_entities(self):
        s = u8.unescape_html_entities(u"&copy;2014")
        self.assertEqual(s, u"©2014")


    def test_u8(self):
        s = u8.u8(u" MonkeyĄ;.,:-' “ʺ‒⟨ &copy;2014 &#8216; &#33; &#169; <@foo=bar>&quot;")
        self.assertEqual(s, ' MonkeyĄ;.,:-\' " 2014 " !  <@foo=bar>"')


if __name__ == "__main__":
    unittest.main()
