from characters import add_diacritic, ACUTE, CIRCUMFLEX
from syllabify import onset_nucleus_coda


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    return o + add_diacritic(n, a) + c


if __name__ == "__main__":
    assert syllable_add_accent("κος", ACUTE) == "κός"
    assert syllable_add_accent("ος", ACUTE) == "ός"
    assert syllable_add_accent("ου", CIRCUMFLEX) == "οῦ"
    assert syllable_add_accent("φως", CIRCUMFLEX) == "φῶς"
