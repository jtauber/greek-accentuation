from characters import add_diacritic, ACUTE, CIRCUMFLEX
from syllabify import onset_nucleus_coda, syllabify, SHORT, LONG, UNKNOWN, syllable_length


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    return o + add_diacritic(n, a) + c


def possible_accentuations(w):
    s = ["".join(x) for x in syllabify(w)]
    ultima_length = syllable_length(s[-1], True)
    penult_length = syllable_length(s[-2], False)
    if ultima_length == SHORT:
        if len(s) >= 3:
            # proparoxytone
            yield "".join(s[:-3]) + syllable_add_accent(s[-3], ACUTE) + "".join(s[-2:])
        if penult_length == SHORT:
            # paroxytone
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], ACUTE) + s[-1]
        elif penult_length == LONG:
            # properispomenon
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], CIRCUMFLEX) + s[-1]
        elif penult_length == UNKNOWN:
            # paroxytone (conditional on short penult)
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], ACUTE) + s[-1]
            # properispomenon (conditional on long penult)
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], CIRCUMFLEX) + s[-1]
        # oxytone
        yield "".join(s[:-1]) + syllable_add_accent(s[-1], ACUTE)
    elif ultima_length == LONG:
        # paroxytone
        yield "".join(s[:-2]) + syllable_add_accent(s[-2], ACUTE) + s[-1]
        # oxytone
        yield "".join(s[:-1]) + syllable_add_accent(s[-1], ACUTE)
        # perispomenon
        yield "".join(s[:-1]) + syllable_add_accent(s[-1], CIRCUMFLEX)
    elif ultima_length == UNKNOWN:
        if len(s) >= 3:
            # proparoxytone (conditional on short ultima)
            yield "".join(s[:-3]) + syllable_add_accent(s[-3], ACUTE) + "".join(s[-2:])
        if penult_length == SHORT:
            # paroxytone
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], ACUTE) + s[-1]
        elif penult_length == LONG:
            # properispomenon (conditional on short ultima)
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], CIRCUMFLEX) + s[-1]
        elif penult_length == UNKNOWN:
            # paroxytone (conditional on short penult)
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], ACUTE) + s[-1]
            # properispomenon (conditional on long penult)
            yield "".join(s[:-2]) + syllable_add_accent(s[-2], CIRCUMFLEX) + s[-1]
        # perispomenon (condition on long ultima)
        yield "".join(s[:-1]) + syllable_add_accent(s[-1], CIRCUMFLEX)
        # oxytone
        yield "".join(s[:-1]) + syllable_add_accent(s[-1], ACUTE)


if __name__ == "__main__":
    assert syllable_add_accent("κος", ACUTE) == "κός"
    assert syllable_add_accent("ος", ACUTE) == "ός"
    assert syllable_add_accent("ου", CIRCUMFLEX) == "οῦ"
    assert syllable_add_accent("φως", CIRCUMFLEX) == "φῶς"
