import unicodedata

from .characters import accent, base, diaeresis, iota_subscript, length
from .characters import remove_redundant_macron
from .characters import breathing, strip_breathing, add_breathing
from .characters import SMOOTH, ROUGH, ACUTE, CIRCUMFLEX, SHORT, LONG


def is_vowel(ch):
    return ch == ACUTE or base(ch).lower() in "αεηιουω~"


def is_diphthong(chs):
    return base(chs[0]).lower() + base(chs[1]).lower() in [
        "αι", "ει", "οι", "υι",
        "αυ", "ευ", "ου", "ηυ",
    ] and not diaeresis(chs[1])


def is_valid_consonant_cluster(b, c):
    s = base(b).lower() + ("".join(base(b2) for b2 in c)).lower()
    return s.startswith((
        "βδ", "βλ", "βρ",
        "γλ", "γν", "γρ",
        "δρ",
        "θλ", "θν", "θρ",
        "κλ", "κν", "κρ", "κτ",
        "μν",
        "πλ", "πν", "πρ", "πτ",
        "σβ", "σθ", "σκ", "σμ", "σπ", "στ", "σφ", "σχ", "στρ",
        "τρ",
        "φθ", "φλ", "φρ",
        "χλ", "χρ",
    ))


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
            if is_vowel(ch) or ch == ROUGH:
                if current_syllable[0] == ACUTE:
                    current_syllable.insert(0, ch)
                elif current_syllable[0] == ROUGH:
                    current_syllable.insert(0, ch)
                elif is_diphthong(ch + current_syllable[0]):
                    if len(current_syllable) > 1 and \
                            current_syllable[1] == "ι":
                        result.insert(0, current_syllable[1:])
                        current_syllable = [ch, current_syllable[0]]
                    else:
                        current_syllable.insert(0, ch)
                else:
                    result.insert(0, current_syllable)
                    current_syllable = [ch]
            else:
                current_syllable.insert(0, ch)
                state = 2
        elif state == 2:
            if is_vowel(ch) or ch == ACUTE:
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
    return onset_nucleus_coda(s)[0] or None


def nucleus(s):
    return onset_nucleus_coda(s)[1] or None


def coda(s):
    return onset_nucleus_coda(s)[2] or None


def onset_nucleus_coda(s):
    for i, ch in enumerate(s):
        if is_vowel(ch):
            if i == 0 and breathing(ch):
                onset = breathing(ch)
                break
            elif i == 0 and len(s) > 1 and breathing(s[1]):
                onset = breathing(s[1])
                break
            else:
                onset = s[:i] if i > 0 else ""
                break
    else:
        return (s, "", "")
    for j, ch in enumerate(s[i:]):
        if not is_vowel(ch) and ch not in [SMOOTH, ROUGH]:
            nucleus = s[i:i + j]
            coda = s[i + j:]
            break
    else:
        nucleus = ""
    if not nucleus:
        nucleus = s[i:]
        coda = ""
    if onset == breathing(onset):
        nucleus = strip_breathing(nucleus)

    return onset, nucleus, coda


def rime(s):
    o, n, c = onset_nucleus_coda(s)
    return n + c


def body(s):
    o, n, c = onset_nucleus_coda(s)
    return o + n


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
            else:  # αιυ
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
        else:
            return "mm"
    elif l == SHORT:
        if a == ACUTE:
            return "M"
        else:
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


def contonation(w):
    s = syllabify(w)
    for i, syllable in enumerate(s):
        a = syllable_accent(syllable)
        if a == ACUTE:
            if i + 1 == len(s):
                return [i + 1]
            else:
                return [i + 1, i + 2]
        elif a == CIRCUMFLEX:
            return [i + 1]
    return []


def split_initial_breathing(word):
    s = syllabify(word)
    o, n, c = onset_nucleus_coda(s[0])
    if o in [SMOOTH, ROUGH]:
        return o, n + c + "".join(s[1:])
    else:
        return None, word


def debreath(word):
    a, word = split_initial_breathing(word)
    if a == ROUGH:
        return "h" + word
    else:
        return word


def rebreath(word):
    if word == "":
        return word
    if word.startswith("h"):
        word = add_necessary_breathing(word[1:], ROUGH)
    else:
        word = add_necessary_breathing(word)
    word = remove_redundant_macron(word)

    return word


def add_necessary_breathing(w, breathing=SMOOTH):
    s = syllabify(w)
    o, n, c = onset_nucleus_coda(s[0])
    if o == "":
        for i, ch in enumerate(n):
            if base(ch).lower() in "αεηιουω":
                last_vowel = i
        if last_vowel > 0:
            pre = n[:last_vowel]
        else:
            pre = ""
        if last_vowel + 1 < len(n):
            post = n[last_vowel + 1:]
        else:
            post = ""
        n = pre + add_breathing(n[last_vowel], breathing) + post
        return unicodedata.normalize("NFKC", o + n + c + "".join(s[1:]))
    else:
        return w
