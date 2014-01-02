from characters import accent, base, diaeresis, iota_subscript
from characters import ACUTE, CIRCUMFLEX

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


LONG = "long"
SHORT = "short"
UNKNOWN = "unknown"

def syllable_length(s, final=None):
    n = nucleus(s)
    if len(n) > 1:
        b = base(n[0]) + base(n[1])
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
            if b in "εο":
                return SHORT
            elif b in "ηω":
                return LONG
            else: # αιυ
                return UNKNOWN


def syllable_accent(s):
    for ch in nucleus(s):
        a = accent(ch)
        if a:
            return a

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

    assert onset("κός") == "κ"
    assert nucleus("κός") == "ό"
    assert coda("κός") == "ς"
    assert rime("κός") == "ός"
    assert body("κός") == "κό"

    assert not onset("οἰ")

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
