# greek-accentuation

[![Build Status](https://travis-ci.org/jtauber/greek-accentuation.svg)](https://travis-ci.org/jtauber/greek-accentuation)
[![Coverage Status](https://coveralls.io/repos/jtauber/greek-accentuation/badge.svg?branch=master&service=github)](https://coveralls.io/github/jtauber/greek-accentuation?branch=master)

Python 3 library for accenting (and analyzing the accentuation of) Ancient
Greek words.

For more of my work on Ancient Greek, see <http://jktauber.com/>.


## Installation

    pip install greek-accentuation==1.2.0


## Documentation

see [docs.rst](https://github.com/jtauber/greek-accentuation/blob/master/docs.rst)


## Change Log

### Changed in 1.2.0

* `on_penult` will now return an oxytone rather than None if input only has one syllable

### Fixed in 1.1.1

* handle VVι cluster better

### Added in 1.1.0

* `accentuation.persistent` now supports `default_short` parameter

### Fixed in 1.0.5

* fixed calculation of coda when syllable is vowel+macron+smooth

### Fixed in 1.0.4

* `syllabify.is_diphthong` now works with uppercase letters (fixes a syllabification bug when capitalized word begins with diphthong)
* `syllabify.add_necessary_breathing` now returns a NFKC normalized form (improving rebreath/debreath roundtripping)

### Fixed in 1.0.3

* `possible_accentuations` now correctly gives paroxytone as a possible accentuation when penult is long and length of ultima is indeterminate

### Fixed in 1.0.2

* fixed persistent accent placement where original accent needs to change from circumflex to acute

### Fixed in 1.0.1

* `syllabify.add_necessary_breathing` now works with uppercase initial vowels

### New in 1.0.0

* `syllabify.debreath`
* `syllabify.rebreath`
* `syllabify.add_necessary_breathing` can optionally add rough breathing
* `characters.add_breathing` properly handles macrons
* modules moved into `greek_accentuation` package
* universal wheel build


0.9.9 removed some unnecessary code

0.9.8 add_necessary_breathing now properly handles initial vowels with iota
subscripts

0.9.7 fixed another bug in macro + breathing + accent case

0.9.6 fixed a bug in macro + breathing + accent case

0.9.5 breathing is now considered part of the onset and syllabification now
works on words containing macron + breathing + accent on the same vowel

0.9.4 fixed syllabification of words containing macron and acute on same vowel

0.9.3 improved onset, nucleus, coda, and syllabify in cases where input has no
vowels.

0.9.2 fixed some edge-case bugs in syllable_morae and contonation and got
doctest coverage to 100%.

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
