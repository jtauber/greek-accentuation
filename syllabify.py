from characters import accent, base, diaeresis, iota_subscript, length
from characters import ACUTE, CIRCUMFLEX, GRAVE, SHORT, LONG

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
    return ".".join(w)


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
    return ["".join(syllable) for syllable in result]


def ultima(w):
    return syllabify(w)[-1]


def penult(w):
    s = syllabify(w)
    return s[-2] if len(s) >= 2 else None


def antepenult(w):
    s = syllabify(w)
    return s[-3] if len(s) >= 3 else None


def onset(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            return s[:i] if i > 0 else None


def nucleus(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            break
    for j, ch in enumerate(s[i:]):
        if not is_vowel(ch):
            return s[i:i+j]
    return s[i:]


def coda(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            break
    for j, ch in enumerate(s[i:]):
        if not is_vowel(ch):
            return s[i+j:]


def onset_nucleus_coda(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            onset = s[:i] if i > 0 else ""
            break
    nucleus = ""
    for j, ch in enumerate(s[i:]):
        if not is_vowel(ch):
            nucleus = s[i:i+j]
            coda = s[i+j:]
            break
    if not nucleus:
        nucleus = s[i:]
        coda = ""
    return onset, nucleus, coda


def rime(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            return s[i:]


def body(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            break
    for j, ch in enumerate(s[i:]):
        if not is_vowel(ch):
            return s[:i+j]
    return s


UNKNOWN = None


def syllable_length(s, final=None):
    n = nucleus(s)
    r = rime(s)
    if len(n) > 1:
        b = "".join(base(ch) for ch in r)
        if final is True:
            if b in ["αι", "οι"]:
                return SHORT
            else:
                return LONG
        elif final is False:
            return LONG
        else:
            if b in ["αι", "οι"]:
                return UNKNOWN
            else:
                return LONG
    else:
        if iota_subscript(n):
            return LONG
        else:
            b = base(n)
            if b in "εο" or length(n) == SHORT:
                return SHORT
            elif b in "ηω" or length(n) == LONG:
                return LONG
            else: # αιυ
                return UNKNOWN


def syllable_accent(s):
    for ch in nucleus(s):
        a = accent(ch)
        if a:
            return a


def oxytone(w):
    # acute on ultima
    return syllable_accent(ultima(w)) == ACUTE


def paroxytone(w):
    # acute on penult
    return syllable_accent(penult(w)) == ACUTE


def proparoxytone(w):
    # acute on antepenult
    return syllable_accent(antepenult(w)) == ACUTE


def perispomenon(w):
    # circumflex on ultima
    return syllable_accent(ultima(w)) == CIRCUMFLEX


def properispomenon(w):
    # circumflex on penult
    return syllable_accent(penult(w)) == CIRCUMFLEX


def barytone(w):
    # ultima unaccented
    return not syllable_accent(ultima(w))


def syllable_morae(s, number):
    a = syllable_accent(s)
    l = syllable_length(s, number == 0)
    if l == LONG:
        if a == ACUTE:
            return "mM"
        elif a == CIRCUMFLEX:
            return "Mm"
        elif not a:
            return "mm"
    elif l == SHORT:
        if a == ACUTE:
            return "M"
        elif a == GRAVE:
            return "m"
        elif not a:
            return "m"
    elif l == UNKNOWN:
        if a == CIRCUMFLEX:
            return "Mm"
        elif a == ACUTE:
            return "U"
        else:
            return "u"


def morae(w):
    return [
        syllable_morae(s, number)
        for number, s in enumerate(syllabify(w)[:-4:-1])
    ][::-1]


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

    assert onset("ναι") == "ν"
    assert nucleus("ναι") == "αι"
    assert not coda("ναι")
    assert rime("ναι") == "αι"
    assert body("ναι") == "ναι"

    assert onset_nucleus_coda("ναι") == ("ν", "αι", "")

    assert onset("κός") == "κ"
    assert nucleus("κός") == "ό"
    assert coda("κός") == "ς"
    assert rime("κός") == "ός"
    assert body("κός") == "κό"

    assert onset_nucleus_coda("κός") == ("κ", "ό", "ς")

    assert not onset("οἰ")

    assert onset_nucleus_coda("οἰ") == ("", "οἰ", "")

    assert onset_nucleus_coda("ἠ(ν)") == ("", "ἠ", "(ν)")

    assert syllable_length("κός") == SHORT
    assert syllable_length("οἰ", final=False) == LONG
    assert syllable_length("ναι") == UNKNOWN
    assert syllable_length("ναι", final=True) == SHORT
    assert syllable_length("ναι", final=False) == LONG
    assert syllable_length("σω") == LONG
    assert syllable_length("ᾳ") == LONG

    assert syllable_accent("κός") == ACUTE
    assert not syllable_accent("ναι")
    assert syllable_accent("φῶς") == CIRCUMFLEX

    assert oxytone("θεός")
    assert paroxytone("λόγος")
    assert proparoxytone("κύριος")
    assert perispomenon("θεοῦ")
    assert properispomenon("δοῦλος")
    assert barytone("λόγος")

    assert ".".join(morae("γυναικός")) == "u.mm.M"
    assert ".".join(morae("θεός")) == "m.M"
    assert ".".join(morae("λόγος")) == "M.m"
    assert ".".join(morae("κύριος")) == "U.u.m"
    assert ".".join(morae("θεοῦ")) == "m.Mm"
    assert ".".join(morae("δοῦλος")) == "Mm.m"
