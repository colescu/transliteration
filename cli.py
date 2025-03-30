import argparse
from src.transliterators import latin_to_greek, greek_to_latin
from src.processor import process_text


def get_transliterator(args):
    match args.type:
        case "lg":
            return lambda word: latin_to_greek(
                word, as_word=args.not_word, breve=args.breve
            )
        case "gl":
            return lambda word: greek_to_latin(
                word, latinize=args.latinize, breve=args.breve
            )


def main():
    parser = argparse.ArgumentParser(
        prog="TRANSLITERATION",
        description="Colescu's CLI tool for transliteration",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["lg", "gl"],
        default="lg",
        help="Latin -> Greek, Greek -> Latin (default: Latin -> Greek)",
    )
    parser.add_argument(
        "-nw",
        "--not-word",
        action="store_false",
        help="do not treat as a word (Greek)",
    )
    parser.add_argument(
        "-l",
        "--latinize",
        action="store_true",
        help="Latinize the spelling (Greek -> Latin)",
    )
    parser.add_argument(
        "-b",
        "--breve",
        action="store_true",
        help="add breve to short vowels (Latin, Greek)",
    )
    args = parser.parse_args()

    transliterator = get_transliterator(args)

    while text := input():
        if text == "quit":
            return
        print(process_text(text, transliterator))


if __name__ == "__main__":
    main()
