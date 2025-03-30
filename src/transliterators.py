from unicodedata import decomposition, normalize


# order: macron/breve, rough/smooth, accents
DIACRITICS = {
    "acute": "\u0301",  # á
    "grave": "\u0300",  # à
    "macron": "\u0304",  # ā
    "breve": "\u0306",  # ă
    "caron": "\u030c",  # ǎ
    "circumflex": "\u0302",  # â
    "tilde": "\u0303",  # ã
    "umlaut": "\u0308",  # ä
    "rough": "\u0314",  # ἁ
    "smooth": "\u0313",  # ἀ
    # The tildes for Latin and Greek are different!
    "tilde_greek": "\u0342",  # ᾶ
    "iota": "\u0345",  # ᾳ
}


GREEK_TO_LATIN_MAP = {
    # vowels
    "α": "a",
    "ε": "e",
    "η": "ē",
    "ι": "i",
    "ο": "o",
    "ω": "ō",
    "υ": "y",
    # consonants
    "β": "b",
    "π": "p",
    "φ": "pʰ",
    "δ": "d",
    "τ": "t",
    "θ": "tʰ",
    "γ": "g",
    "κ": "k",
    "χ": "kʰ",
    "ζ": "z",
    "σ": "s",
    "μ": "m",
    "ν": "n",
    "λ": "l",
    "ρ": "r",
    "ξ": "ks",
    "ψ": "ps",
    "ϝ": "w",
}

LATIN_TO_GREEK_MAP = {latin: greek for greek, latin in GREEK_TO_LATIN_MAP.items()} | {
    "u": "υ",
    "c": "κ",
    "cʰ": "χ",
    "f": "φ",
    "x": "ξ",
}


def decompose(letter: str) -> tuple[str, list[str]]:
    """decompose letter into bare letter and diacritics"""
    diacritics = []
    while True:
        s: str = decomposition(letter)
        if not s:
            break
        letter = chr(int(s[:4], 16))
        diacritics.append(chr(int(s[-4:], 16)))
    return letter, diacritics[::-1]


def combine(letter: str, diacritics: list[str]) -> str:
    """combine letter with diacritics"""
    return normalize("NFC", letter + "".join(diacritics))


def latin_to_greek(word: str, as_word: bool = True, breve: bool = False) -> str:
    """
    text: word to transliterate
    as_word: add smooth breathing, change final σ to ς
    breve: add breve to short vowels
    """

    chars = []  # letters
    diacs = []  # diacritics
    caps = []  # capitalizations
    rough = False

    for i in range(len(word)):
        char = word[i]

        if char in DIACRITICS.values():
            diacs[-1].append(char)
            continue

        if char == "ʰ":
            chars[-1] += "ʰ"
            continue

        letter, diacritics = decompose(char)

        capitalize = False
        if ord("A") <= ord(letter) <= ord("Z"):
            capitalize = True
            letter = chr(ord(letter) + 32)

        match letter:
            # initial h, pʰ, tʰ, kʰ, rʰ
            case "h":
                if i == 0:
                    rough = True
                elif len(chars) > 0:
                    chars[-1] += "ʰ"
            # dz -> z
            case "z" if len(chars) > 0 and chars[-1] == "d":
                chars[-1] = "z"
            # ps, ks
            case "s" if len(chars) > 0 and chars[-1] in "pk":
                chars[-1] += "s"
            case _:
                chars.append(letter)
                diacs.append(diacritics)
                caps.append(capitalize)

    if word[0] == "H":
        caps[0] = True

    # placement of rough/smooth breathing
    breathing = (
        DIACRITICS["rough"] if rough else DIACRITICS["smooth"] if as_word else ""
    )
    place_breathing = -1
    if (
        len(chars) >= 2
        and chars[0] in "aeēioōyu"
        and chars[1] in "iyu"
        and not (chars[0] == chars[1] or chars[0] in "yu" and chars[1] in "yu")
        and DIACRITICS["umlaut"] not in diacs[1]
    ):
        place_breathing = 1
    elif chars[0] in "aeēioōyu":
        place_breathing = 0

    t_chars = []
    for i in range(len(chars)):
        letter, diacritics, capitalize = chars[i], diacs[i], caps[i]

        if letter in "jqv" or (
            letter[-1] == "ʰ" and letter not in ["pʰ", "tʰ", "kʰ", "cʰ", "rʰ"]
        ):
            return f"Invalid input: {letter} in {word}."

        if letter == "rʰ":
            letter = "r"
            diacritics.insert(0, DIACRITICS["rough"])
            if i > 0 and chars[i - 1] == "r":
                t_chars[i - 1] = "ῤ"

        # ẽ, õ -> ē̃, ō̃
        if letter in "eo" and (
            DIACRITICS["macron"] in diacritics or DIACRITICS["tilde"] in diacritics
        ):
            letter = combine(letter, [DIACRITICS["macron"]])
            while DIACRITICS["macron"] in diacritics:
                diacritics.remove(DIACRITICS["macron"])

        if letter not in LATIN_TO_GREEK_MAP:
            t_chars.append(letter)
            continue

        t_char = LATIN_TO_GREEK_MAP[letter]

        if capitalize:
            t_char = chr(ord(t_char) - 32)
            if letter == "w":
                t_char = "Ϝ"

        if breathing and i == place_breathing:
            diacritics.insert(0, breathing)

        while DIACRITICS["tilde"] in diacritics:
            diacritics.remove(DIACRITICS["tilde"])
            diacritics.append(DIACRITICS["tilde_greek"])

        if as_word and i == len(chars) - 1 and t_char == "σ":
            t_char = "ς"

        if DIACRITICS["macron"] in diacritics:
            diacritics.remove(DIACRITICS["macron"])
            diacritics.insert(0, DIACRITICS["macron"])

        if breve and (
            letter in "eo"
            or letter in "aiyu"
            and DIACRITICS["macron"] not in diacritics
        ):
            diacritics.insert(0, DIACRITICS["breve"])

        t_chars.append(combine(t_char, diacritics))

    return "".join(t_chars)


def greek_to_latin(word: str, latinize: bool = False, breve: bool = False) -> str:
    chars = []
    diacs = []
    caps = []

    for i in range(len(word)):
        char = word[i]

        if char in DIACRITICS.values():
            diacs[-1].append(char)
            continue

        letter, diacritics = decompose(char)

        capitalize = False
        if ord("Α") <= ord(letter) <= ord("Ω"):
            capitalize = True
            letter = chr(ord(letter) + 32)

        chars.append(letter)
        diacs.append(diacritics)
        caps.append(capitalize)

    t_chars = []
    for i in range(len(chars)):
        letter, diacritics, capitalize = chars[i], diacs[i], caps[i]
        iota = False

        if letter == "ς":
            letter = "σ"

        if letter not in GREEK_TO_LATIN_MAP:
            t_chars.append(letter)
            continue

        t_char = GREEK_TO_LATIN_MAP[letter]

        if DIACRITICS["iota"] in diacritics:
            iota = True
            diacritics.remove(DIACRITICS["iota"])

        while DIACRITICS["tilde_greek"] in diacritics:
            diacritics.remove(DIACRITICS["tilde_greek"])
            diacritics.append(DIACRITICS["tilde"])

        if all(x in "aeēioōyu" for x in t_chars):
            if DIACRITICS["smooth"] in diacritics:
                diacritics.remove(DIACRITICS["smooth"])
            if DIACRITICS["rough"] in diacritics:
                diacritics.remove(DIACRITICS["rough"])
                if capitalize and all(x is False for x in caps[1:]):
                    capitalize = False
                    t_chars.insert(0, "H")
                else:
                    t_chars.insert(0, "H" if capitalize else "h")

        if t_char == "y" and (
            len(t_chars) > 0
            and t_chars[-1] in "aeēioō"
            and DIACRITICS["umlaut"] not in diacritics
        ):
            t_char = "u"

        if latinize:
            match t_char:
                # k -> c
                case "k":
                    t_char = "c"
                # ks -> x
                case "ks":
                    t_char = "x"
                # pʰ, tʰ, kʰ -> ph, th, ch
                case _ if t_char[-1] == "ʰ":
                    t_char = t_char[:-1] + "h"
                    if t_char == "kh":
                        t_char = "ch"
                # gg -> ng
                case "g" if len(t_chars) > 0 and t_chars[-1] == "g":
                    t_chars[-1] = "n"
                # ai, oi -> ae, oe
                case "i" if (
                    len(t_chars) > 0
                    and t_chars[-1] in "ao"
                    and DIACRITICS["umlaut"] not in diacritics
                ):
                    t_char = "e"
                # ei -> ī
                case "i" if (
                    len(t_chars) > 0
                    and t_chars[-1] == "e"
                    and DIACRITICS["umlaut"] not in diacritics
                ):
                    t_chars.pop()
                    diacritics.insert(0, DIACRITICS["macron"])
                # ou -> ū
                case "u" if (
                    len(t_chars) > 0
                    and t_chars[-1] == "o"
                    and DIACRITICS["umlaut"] not in diacritics
                ):
                    t_chars.pop()
                    t_char = "u"
                    diacritics.insert(0, DIACRITICS["macron"])

        if breve:
            if t_char in "aeioyu" and DIACRITICS["macron"] not in diacritics:
                diacritics.insert(0, DIACRITICS["breve"])

        if capitalize:
            t_char = t_char.capitalize()

        t_chars.append(combine(t_char, diacritics))
        if iota:
            t_chars[-1] += "i"

    return "".join(t_chars)
