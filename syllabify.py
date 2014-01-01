from characters import base, diaeresis


def is_vowel(ch):
    return base(ch).lower() in "αεηιουω"


def is_diphthong(chs):
    return base(chs[0]) + base(chs[1]) in [
        "αι", "ει", "οι", "υι",
        "αυ", "ευ", "ου", "ηυ",
    ] and not diaeresis(chs[1])


def is_valid_consonant_cluster(b, c):
    s = base(b).lower() + ("".join(base(b2) for b2 in c)).lower()
    return s[:2] in [
              "βδ",             "βλ",                   "βρ",
                                "γλ",       "γν",       "γρ",
                                                        "δρ",
                                "θλ",       "θν",       "θρ",
                                "κλ",       "κν",       "κρ", "κτ",
                                            "μν",
                                "πλ",       "πν",       "πρ", "πτ",
        "σβ",       "σθ", "σκ",       "σμ",       "σπ",       "στ", "σφ", "σχ",
                                                        "τρ",
                    "φθ",       "φλ",                   "φρ",
                                "χλ",                   "χρ",
    ] or s[:3] in [
        "στρ",
    ]


def display_word(w):
    return ".".join("".join(s) for s in w)


def syllabify(word):
    state = 0
    result = []
    current_syllable = []
    for ch in word[::-1]:
        if state == 0:
            current_syllable.insert(0, ch)
            if is_vowel(ch):
                state = 1
        elif state == 1:
            if is_vowel(ch):
                if is_diphthong(ch + current_syllable[0]):
                    current_syllable.insert(0, ch)
                else:
                    result.insert(0, current_syllable)
                    current_syllable = [ch]
            else:
                current_syllable.insert(0, ch)
                state = 2
        elif state == 2:
            if is_vowel(ch):
                result.insert(0, current_syllable)
                current_syllable = [ch]
                state = 1
            else:
                if is_valid_consonant_cluster(ch, current_syllable):
                    current_syllable.insert(0, ch)
                else:
                    result.insert(0, current_syllable)
                    current_syllable = [ch]
                    state = 0
    result.insert(0, current_syllable)
    assert state != 0, word
    return result


def ultima(w):
    return "".join(syllabify(w)[-1])


def penult(w):
    s = syllabify(w)
    return "".join(s[-2]) if len(s) >= 2 else None


def antepenult(w):
    s = syllabify(w)
    return "".join(s[-3]) if len(s) >= 3 else None


if __name__ == "__main__":
    assert is_vowel("ὅ")
    assert not is_vowel("γ")

    assert is_diphthong("αι")
    assert not is_diphthong("αε")
    assert not is_diphthong("αϋ")

    assert display_word(syllabify("γυναικός")) == "γυ.ναι.κός"
    assert display_word(syllabify("οἰκία")) == "οἰ.κί.α"
    assert display_word(syllabify("καταλλάσσω")) == "κα.ταλ.λάσ.σω"

    assert ultima("γυναικός") == "κός"
    assert penult("οἰκία") == "κί"
    assert antepenult("καταλλάσσω") == "ταλ"
    assert not antepenult("λόγος")
