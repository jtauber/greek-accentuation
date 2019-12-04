import enum
import unicodedata


class DiacriticEnum(enum.Enum):
    def __str__(self):
        return self.value

    @classmethod
    def values(cls):
        return {member.value for member in cls}

    @classmethod
    def strings(cls):
        return {value for value in cls.values() if isinstance(value, str)}


class Breathing(DiacriticEnum):
    SMOOTH = "\u0313"
    ROUGH = "\u0314"
    PSILI = SMOOTH
    DASIA = ROUGH


class Accent(DiacriticEnum):
    ACUTE = "\u0301"
    GRAVE = "\u0300"
    CIRCUMFLEX = "\u0342"
    OXIA = ACUTE
    VARIA = GRAVE
    PERISPOMENI = CIRCUMFLEX


class Diacritic(DiacriticEnum):
    DIAERESIS = "\u0308"


class Subscript(DiacriticEnum):
    IOTA = "\u0345"
    YPOGEGRAMMENI = IOTA


class Length(DiacriticEnum):
    SHORT = "\u0306"
    LONG = "\u0304"
    UNKNOWN = -1


def base(ch):
    return unicodedata.normalize("NFD", ch)[0]


def extract_diacritic(Enum, unknown_value=None):
    """
    Given an Enum of Unicode diacritics, return a function that takes a
    Unicode character and returns the member of the collection the character
    has (or None).
    """
    diacritics = Enum.strings()

    def _(ch):
        decomposed_form = unicodedata.normalize("NFD", ch)
        for diacritic in diacritics:
            if diacritic in decomposed_form:
                return Enum(diacritic)
        return unknown_value
    return _


def add_diacritic(base, diacritic):
    """
    Add the given diacritic to the given base character.
    """
    return unicodedata.normalize("NFC", base + diacritic.value)


def add_breathing(ch, breathing):
    """
    Add the given breathing to the given (possibly accented) character.
    """
    decomposed = unicodedata.normalize("NFD", ch)
    if len(decomposed) > 1 and decomposed[1] == Length.LONG.value:
        return unicodedata.normalize(
            "NFC", decomposed[0:2] + breathing.value + decomposed[2:])
    else:
        return unicodedata.normalize(
            "NFC", decomposed[0] + breathing.value + decomposed[1:])


def remove_diacritic(Enum):
    """
    Given an Enum of Unicode diacritics, return a function that takes a
    string and returns the string without those diacritics.
    """
    diacritics = Enum.strings()

    def _(text):
        return unicodedata.normalize("NFC", "".join(
            ch
            for ch in unicodedata.normalize("NFD", text)
            if ch not in diacritics)
        )
    return _


breathing = extract_diacritic(Breathing)
strip_breathing = remove_diacritic(Breathing)

accent = extract_diacritic(Accent)
strip_accents = remove_diacritic(Accent)

diaeresis = extract_diacritic(Diacritic)

iota_subscript = extract_diacritic(Subscript)
ypogegrammeni = iota_subscript

length = extract_diacritic(Length, unknown_value=Length.UNKNOWN)
strip_length = remove_diacritic(Length)


def remove_redundant_macron(word):

    # if a circumflex, no need for macron indicating length

    if "\u0304\u0342" in unicodedata.normalize("NFD", word):
        return strip_length(word)
    else:
        return word
