from characters import add_diacritic, ACUTE, CIRCUMFLEX
from syllabify import onset_nucleus_coda, syllabify, SHORT, LONG, UNKNOWN, syllable_length


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    return o + add_diacritic(n, a) + c


def add_accent(s, pos, accent):
    final = s[1-pos:] if pos > 1 else [""]
    return "".join(s[:-pos] + [syllable_add_accent(s[-pos], accent)] + final)


def oxytone(s):
    return add_accent(s, 1, ACUTE), 1


def paroxytone(s):
    return add_accent(s, 2, ACUTE), 3


def proparoxytone(s):
    return add_accent(s, 3, ACUTE), 5


def perispomenon(s):
    return add_accent(s, 1, CIRCUMFLEX), 2


def properispomenon(s):
    return add_accent(s, 2, CIRCUMFLEX), 4


def possible_accentuations(w):
    s = syllabify(w)
    ultima_length = syllable_length(s[-1], True)
    penult_length = syllable_length(s[-2], False) if len(s) >= 2 else None
    if ultima_length == SHORT:
        if len(s) >= 3:
            yield proparoxytone(s)
        if penult_length == SHORT:
            yield paroxytone(s)
        elif penult_length == LONG:
            yield properispomenon(s)
        elif penult_length == UNKNOWN:
            # conditional on short penult
            yield paroxytone(s)
            # conditional on long penult
            yield properispomenon(s)
        yield oxytone(s)
    elif ultima_length == LONG:
        if len(s) >= 2:
            yield paroxytone(s)
        yield oxytone(s)
        yield perispomenon(s)
    elif ultima_length == UNKNOWN:
        if len(s) >= 3:
            # conditional on short ultima
            yield proparoxytone(s)
        if penult_length == SHORT:
            yield paroxytone(s)
        elif penult_length == LONG:
            # conditional on short ultima
            yield properispomenon(s)
        elif penult_length == UNKNOWN:
            # conditional on short penult
            yield paroxytone(s)
            # conditional on long penult
            yield properispomenon(s)
        # conditional on long ultima
        yield perispomenon(s)
        yield oxytone(s)


def recessive(w):
    return sorted(possible_accentuations(w), key=lambda x: x[1], reverse=True)[0][0]


if __name__ == "__main__":
    assert syllable_add_accent("κος", ACUTE) == "κός"
    assert syllable_add_accent("ος", ACUTE) == "ός"
    assert syllable_add_accent("ου", CIRCUMFLEX) == "οῦ"
    assert syllable_add_accent("φως", CIRCUMFLEX) == "φῶς"

    assert recessive("εγινωσκον") == "εγίνωσκον"
    assert recessive("εγινωσκου") == "εγινώσκου"
