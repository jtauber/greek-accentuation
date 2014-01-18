# greek-accentuation

Python 3 library for accenting (and analyzing the accentuation of) Ancient Greek words

## Installation

    pip install greek-accentuation==0.5

## Change Log

* 0.5 fixed bug where possible_accentuations wouldn't work with single syllable words
* 0.4.1 added classifiers for PyPI
* 0.4 handle explicit length markers on vowels
* 0.3 attempts to make a word perispomenon or properispomenon will fall back to oxytone and paroxytone respectively if first attempt fails
* 0.2 better handling of final αι/οι
* 0.1 initial release
