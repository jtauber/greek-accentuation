# greek-accentuation

[![Build Status](https://travis-ci.org/jtauber/greek-accentuation.svg)](https://travis-ci.org/jtauber/greek-accentuation)

Python 3 library for accenting (and analyzing the accentuation of) Ancient
Greek words.


## Installation

    pip install greek-accentuation==0.9.1


## Change Log

0.9.1 slightly improved persistent accent calculation by falling back to
recessive if out of syllables (rather than raising an exception).


### New in 0.9

* initial documentation
* `accentuation.display_accent_type`
* `accentuation.get_accent_type`
* `accentuation.on_penult`
* `syllabify.contonation`
* `syllabify.add_necessary_breathing`
* `characters.strip_breathing`
* `characters.strip_accents`
* `characters.remove_redundant_macron`
* allow ~ to be used for unspecified vowel
* allow | to be used as a wall the accent can't cross
* allow treatment of final AI/OI length to be settable
* added option to treat unmarked vowels as short by default

### Previous Versions

* 0.8 fixed bug in nucleus/coda calculation
* 0.7 added make_proparoxytone function
* 0.6 fixed another bug where possible_accentuations wouldn't work with single
      syllable words
* 0.5 fixed bug where possible_accentuations wouldn't work with single syllable
      words
* 0.4.1 added classifiers for PyPI
* 0.4 handle explicit length markers on vowels
* 0.3 attempts to make a word perispomenon or properispomenon will fall back to
      oxytone and paroxytone respectively if first attempt fails
* 0.2 better handling of final αι/οι
* 0.1 initial release
