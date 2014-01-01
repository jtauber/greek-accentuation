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


if __name__ == "__main__":
    assert base("ὅ") == "ο"
    assert breathing("ὅ") == ROUGH
    assert accent("ὅ") == ACUTE
    assert not diaeresis("ὅ")
    assert base("ϋ") == "υ"
    assert not breathing("ϋ")
    assert not accent("ϋ")
    assert diaeresis("ϋ") == DIAERESIS
