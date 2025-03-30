from unicodedata import category


def is_punctuation(char: str) -> bool:
    return category(char).startswith("P") or char in "᾽"


def process_text(text: str, transliterator) -> str:
    words = []
    curr = ""
    for c in text + " ":
        if c.isspace() or is_punctuation(c):
            if curr:
                words.append(transliterator(curr))
                curr = ""
            words.append(c)
        else:
            curr += c
    return "".join(words[:-1])
