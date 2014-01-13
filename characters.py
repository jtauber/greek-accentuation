import unicodedata


def base(ch):
    return unicodedata.normalize("NFD", ch)[0]


PSILI = SMOOTH = "\u0313"
DASIA = ROUGH = "\u0314"

def breathing(ch):
    decomposed_form = unicodedata.normalize("NFD", ch)
    for breathing_character in [SMOOTH, ROUGH]:
        if breathing_character in decomposed_form:
            return breathing_character


OXIA = ACUTE = "\u0301"
VARIA = GRAVE = "\u0300"
PERISPOMENI = CIRCUMFLEX = "\u0342"

def accent(ch):
    decomposed_form = unicodedata.normalize("NFD", ch)
    for accent_character in [ACUTE, GRAVE, CIRCUMFLEX]:
        if accent_character in decomposed_form:
            return accent_character


DIAERESIS = "\u0308"

def diaeresis(ch):
    decomposed_form = unicodedata.normalize("NFD", ch)
    for accent_character in [DIAERESIS]:
        if accent_character in decomposed_form:
            return accent_character


YPOGEGRAMMENI = IOTA_SUBSCRIPT = "\u0345"

def iota_subscript(ch):
    decomposed_form = unicodedata.normalize("NFD", ch)
    for accent_character in [IOTA_SUBSCRIPT]:
        if accent_character in decomposed_form:
            return accent_character
ypogegrammeni = iota_subscript


SHORT = "\u0306"
LONG = "\u0304"

def length(ch):
    decomposed_form = unicodedata.normalize("NFD", ch)
    for diacritic in [SHORT, LONG]:
        if diacritic in decomposed_form:
            return diacritic


def strip_length(t):
    return unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFD", t) if ch not in [SHORT, LONG]))



def add_diacritic(base, diacritic):
    return unicodedata.normalize("NFC", base + diacritic)


if __name__ == "__main__":
    assert base("ὅ") == "ο"
    assert breathing("ὅ") == ROUGH
    assert accent("ὅ") == ACUTE
    assert not diaeresis("ὅ")
    assert base("ϋ") == "υ"
    assert not breathing("ϋ")
    assert not accent("ϋ")
    assert diaeresis("ϋ") == DIAERESIS
    assert iota_subscript("ᾳ") == IOTA_SUBSCRIPT
    assert not iota_subscript("α")

    assert length("ῠ") == SHORT
    assert length("ῡ") == LONG
    assert length("υ") is None # i.e. unknown

    assert add_diacritic("υ", DIAERESIS) == "ϋ"
    assert add_diacritic("α", YPOGEGRAMMENI) == "ᾳ"
    assert add_diacritic(add_diacritic("ο", ROUGH), ACUTE) == "ὅ"
