
    This is a literate doctest.
    Run ``python -m doctest -v docs.rst`` to test.


Characters
==========

>>> from characters import *

The ``characters`` module provides basic analysis and manipulation of Greek
characters in terms of their Unicode diacritics as if decomposed.

For example:

>>> base('ᾳ')
'α'

>>> iota_subscript('ᾳ')
'\u0345'

>>> IOTA_SUBSCRIPT
'\u0345'

>>> iota_subscript('ᾳ') == IOTA_SUBSCRIPT
True

>>> not iota_subscript('α')
True

>>> add_diacritic('α', IOTA_SUBSCRIPT)
'ᾳ'


As well as ``iota_subscript``, this works for ``breathing``:

>>> breathing('ὅ') == ROUGH
True


``accent``:

>>> accent('ὅ') == ACUTE
True


``diaeresis``:

>>> diaeresis('ὅ') == DIAERESIS
False

>>> diaeresis('ϋ') == DIAERESIS
True


and ``length``:

>>> length('ῠ') == SHORT
True

>>> length('ῡ') == LONG
True

If the length is not indicated, ``length`` will return None:

>>> length('υ')


You can strip the length diacritic if one exists:

>>> strip_length('ῡ')
'υ'


``add_diacritic`` can be stacked:

>>> add_diacritic(add_diacritic('ο', ROUGH), ACUTE)
'ὅ'
