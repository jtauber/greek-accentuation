from characters import add_diacritic
from characters import ACUTE, CIRCUMFLEX, SHORT, LONG
from syllabify import onset_nucleus_coda, syllabify, UNKNOWN, syllable_length
from syllabify import syllable_accent, ultima, penult, antepenult


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    return o + add_diacritic(n, a) + c


def add_accent(s, accent_type):
    pos, accent = accent_type
    final = s[1-pos:] if pos > 1 else [""]
    return "".join(s[:-pos] + [syllable_add_accent(s[-pos], accent)] + final)


OXYTONE = 1, ACUTE
PERISPOMENON = 1, CIRCUMFLEX
PAROXYTONE = 2, ACUTE
PROPERISPOMENON = 2, CIRCUMFLEX
PROPAROXYTONE = 3, ACUTE


def display_accent_type(accent_type):
    return {
        OXYTONE: "oxytone",
        PERISPOMENON: "perispomenon",
        PAROXYTONE: "paroxytone",
        PROPERISPOMENON: "properispomenon",
        PROPAROXYTONE: "proparoxytone",
    }[accent_type]


def make_oxytone(w):
    return add_accent(syllabify(w), OXYTONE)


def make_paroxytone(w):
    return add_accent(syllabify(w), PAROXYTONE)


def make_proparoxytone(w):
    return add_accent(syllabify(w), PROPAROXYTONE)


def make_perispomenon(w):
    s = syllabify(w)
    if PERISPOMENON in possible_accentuations(s):
        return add_accent(s, PERISPOMENON)
    else:
        return add_accent(s, OXYTONE)


def make_properispomenon(w):
    s = syllabify(w)
    if PROPERISPOMENON in possible_accentuations(s):
        return add_accent(s, PROPERISPOMENON)
    else:
        return add_accent(s, PAROXYTONE)


def get_accent_type(w):
    u = syllable_accent(ultima(w))
    if u == ACUTE:
        return OXYTONE
    elif u == CIRCUMFLEX:
        return PERISPOMENON
    p = syllable_accent(penult(w))
    if p == ACUTE:
        return PAROXYTONE
    elif p == CIRCUMFLEX:
        return PROPERISPOMENON
    a = syllable_accent(antepenult(w))
    if a == ACUTE:
        return PROPAROXYTONE


def possible_accentuations(s):
    ultima_length = syllable_length(s[-1], True)
    penult_length = syllable_length(s[-2], False) if len(s) >= 2 else None
    if ultima_length == SHORT:
        if len(s) >= 2:
            if len(s) >= 3:
                yield PROPAROXYTONE
            if penult_length == SHORT:
                yield PAROXYTONE
            elif penult_length == LONG:
                yield PROPERISPOMENON
            elif penult_length == UNKNOWN:
                # conditional on short penult
                yield PAROXYTONE
                # conditional on long penult
                yield PROPERISPOMENON
        yield OXYTONE
    elif ultima_length == LONG:
        if len(s) >= 2:
            yield PAROXYTONE
        yield OXYTONE
        yield PERISPOMENON
    elif ultima_length == UNKNOWN:
        if len(s) >= 2:
            if len(s) >= 3:
                # conditional on short ultima
                yield PROPAROXYTONE
            if penult_length == SHORT:
                yield PAROXYTONE
            elif penult_length == LONG:
                # conditional on short ultima
                yield PROPERISPOMENON
            elif penult_length == UNKNOWN:
                # conditional on short penult
                yield PAROXYTONE
                # conditional on long penult
                yield PROPERISPOMENON
        # conditional on long ultima
        yield PERISPOMENON
        yield OXYTONE


def recessive(w):
    s = syllabify(w)
    return add_accent(s, sorted(possible_accentuations(s), reverse=True)[0])
