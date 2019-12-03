import enum

from .characters import add_diacritic
from .characters import Accent, Length, Breathing
from .syllabify import onset_nucleus_coda, syllabify, syllable_length
from .syllabify import syllable_accent, ultima, penult, antepenult


class Accentuation(enum.Enum):
    OXYTONE = (1, Accent.ACUTE)
    PERISPOMENON = (1, Accent.CIRCUMFLEX)
    PAROXYTONE = (2, Accent.ACUTE)
    PROPERISPOMENON = (2, Accent.CIRCUMFLEX)
    PROPAROXYTONE = (3, Accent.ACUTE)

    @property
    def position(self):
        return self.value[0]

    @property
    def character(self):
        return self.value[1].value

    @property
    def raw_value(self):
        return self.position, self.character

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        other_value = (
            other.raw_value if isinstance(other, Accentuation) else other
        )
        return self.raw_value < other_value

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        other_value = (
            other.raw_value if isinstance(other, Accentuation) else other
        )
        return self.raw_value > other_value

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    if isinstance(o, Breathing):
        return add_diacritic(add_diacritic(n, o), a) + c
    else:
        return o + add_diacritic(n, a) + c


def add_accentuation(s, accentuation):
    pos, accent = accentuation.value
    final = s[1 - pos:] if pos > 1 else [""]
    return "".join(s[:-pos] + [syllable_add_accent(s[-pos], accent)] + final)


def display_accentuation(accentuation):
    return accentuation.name.lower()


def make_oxytone(w):
    return add_accentuation(syllabify(w), Accentuation.OXYTONE)


def make_paroxytone(w):
    return add_accentuation(syllabify(w), Accentuation.PAROXYTONE)


def make_proparoxytone(w):
    return add_accentuation(syllabify(w), Accentuation.PROPAROXYTONE)


def make_perispomenon(w):
    s = syllabify(w)
    if Accentuation.PERISPOMENON in possible_accentuations(s):
        return add_accentuation(s, Accentuation.PERISPOMENON)
    else:
        return add_accentuation(s, Accentuation.OXYTONE)


def make_properispomenon(w):
    s = syllabify(w)
    if Accentuation.PROPERISPOMENON in possible_accentuations(s):
        return add_accentuation(s, Accentuation.PROPERISPOMENON)
    else:
        return add_accentuation(s, Accentuation.PAROXYTONE)


def get_accentuation(w):
    u = syllable_accent(ultima(w))
    if u == Accent.ACUTE:
        return Accentuation.OXYTONE
    elif u == Accent.CIRCUMFLEX:
        return Accentuation.PERISPOMENON
    p = syllable_accent(penult(w))
    if p == Accent.ACUTE:
        return Accentuation.PAROXYTONE
    elif p == Accent.CIRCUMFLEX:
        return Accentuation.PROPERISPOMENON
    a = syllable_accent(antepenult(w))
    if a == Accent.ACUTE:
        return Accentuation.PROPAROXYTONE


def possible_accentuations(
    s, treat_final_AI_OI_short=True, default_short=False
):
    ultima_length = syllable_length(s[-1], treat_final_AI_OI_short)
    penult_length = syllable_length(s[-2], False) if len(s) >= 2 else None
    if ultima_length == Length.UNKNOWN and default_short:
        ultima_length = Length.SHORT
    if penult_length == Length.UNKNOWN and default_short:
        penult_length = Length.SHORT

    yield Accentuation.OXYTONE

    if not (ultima_length == Length.SHORT):
        yield Accentuation.PERISPOMENON

    if (len(s) >= 2 and not
            (penult_length == Length.LONG and ultima_length == Length.SHORT)):
        yield Accentuation.PAROXYTONE

    if (len(s) >= 2 and not
            (penult_length == Length.SHORT or ultima_length == Length.LONG)):
        yield Accentuation.PROPERISPOMENON

    if (len(s) >= 3 and not
            (ultima_length == Length.LONG)):
        yield Accentuation.PROPAROXYTONE


def recessive(w, treat_final_AI_OI_short=True, default_short=False):
    if "|" in w:
        pre, w = w.split("|")
    else:
        pre = ""

    s = syllabify(w)
    return pre + add_accentuation(
        s,
        sorted(
            possible_accentuations(s, treat_final_AI_OI_short, default_short),
            reverse=True
        )[0]
    )


def on_penult(w, default_short=False):
    if "|" in w:
        pre, w = w.split("|")
    else:
        pre = ""

    s = syllabify(w)
    accentuations = list(
        possible_accentuations(s, default_short=default_short)
    )
    if Accentuation.PROPERISPOMENON in accentuations:
        return pre + add_accentuation(s, Accentuation.PROPERISPOMENON)
    elif Accentuation.PAROXYTONE in accentuations:
        return pre + add_accentuation(s, Accentuation.PAROXYTONE)
    elif Accentuation.OXYTONE:  # fall back to an oxytone if necessary
        return pre + add_accentuation(s, Accentuation.OXYTONE)


def persistent(w, lemma, default_short=False):
    w = w.replace("|", "")

    place, accent = get_accentuation(lemma).value
    s = syllabify(w)
    possible = [
        p.value for p in possible_accentuations(s, default_short=default_short)
    ]
    place2 = len(s) - len(syllabify(lemma)) + place
    accent_pair = (place2, accent)
    if accent_pair not in possible:
        if accent == Accent.ACUTE and (place2, Accent.CIRCUMFLEX) in possible:
            accent_pair = (place2, Accent.CIRCUMFLEX)
        elif (
            accent == Accent.CIRCUMFLEX and (place2, Accent.ACUTE) in possible
        ):
            accent_pair = (place2, Accent.ACUTE)
        else:
            for i in range(1, 4):
                if (place2 - i, Accent.ACUTE) in possible:
                    accent_pair = (place2 - i, Accent.ACUTE)
                    break
    return add_accentuation(s, Accentuation(accent_pair))
