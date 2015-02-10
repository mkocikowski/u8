Purpose
-------
Convert input str or unicode into utf-8 encoded str which contains only
xml-valid characters, and has a bunch of 'garbage' character classes
cleaned out.

Use
---

    import u8
    s = u8.u8("gnarly str or unicode with all kinds of weird characters")

Test
----

    python test_u8.py

