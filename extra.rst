>>> from characters import add_diacritic, accent, breathing, length
>>> from characters import LONG, ACUTE, ROUGH, SMOOTH

>>> a = add_diacritic(add_diacritic(add_diacritic('ι', LONG), ACUTE), ROUGH)
>>> a
'ῑ́̔'

>>> b = add_diacritic(add_diacritic(add_diacritic('ι', LONG), ROUGH), ACUTE)
>>> b
'ῑ̔́'

>>> len(a)
3

>>> len(b)
3

>>> accent(a) == ACUTE, accent(b) == ACUTE
(True, True)

>>> breathing(a) == ROUGH, breathing(b) == ROUGH
(True, True)

>>> length(a) == LONG, length(b) == LONG
(True, True)

>>> from syllabify import syllabify, add_necessary_breathing
>>> from syllabify import onset, nucleus, coda, onset_nucleus_coda

>>> syllabify('ῑ́̔στην')
['ῑ́̔', 'στην']

>>> onset('ὅς') == ROUGH
True

>>> onset('οἱ') == ROUGH
True

>>> onset('ἀ') == SMOOTH
True

>>> onset('εἰ') == SMOOTH
True

>>> nucleus('ὅς')
'ό'

>>> coda('ὅς')
'ς'

>>> onset_nucleus_coda('ὅς')
('̔', 'ό', 'ς')

>>> onset(syllabify('κἀγω')[0])
'κ'

>>> nucleus(syllabify('κἀγω')[0])
'ἀ'

>>> coda(syllabify('κἀγω')[0])

>>> onset_nucleus_coda(syllabify('κἀγω')[0])
('κ', 'ἀ', '')

>>> onset(syllabify('ῑ̔́στην')[0])
'̔'

>>> nucleus(syllabify('ῑ̔́στην')[0])
'ῑ́'

>>> coda(syllabify('ῑ̔́στην')[0])

>>> onset_nucleus_coda(syllabify('ῑ̔́στην')[0])
('̔', 'ῑ́', '')

>>> add_necessary_breathing('ῑ̔́στην')
'ῑ̔́στην'

>>> from accentuation import recessive, add_accent, syllable_add_accent, PAROXYTONE

>>> syllabify('ῑ̔στην')
['ῑ̔', 'στην']

>>> onset_nucleus_coda(syllabify('ῑ̔στην')[0])
('̔', 'ῑ', '')

>>> syllable_add_accent(syllabify('ῑ̔στην')[0], ACUTE)
'ῑ̔́'

>>> add_accent(syllabify('ῑ̔στην'), PAROXYTONE)
'ῑ̔́στην'

>>> recessive('ῑ̔στην')
'ῑ̔́στην'

>>> onset_nucleus_coda('ῑ̔́')
('̔', 'ῑ́', '')

>>> add_necessary_breathing('ῑ̔́στην')
'ῑ̔́στην'
