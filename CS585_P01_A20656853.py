import argparse
import re
from pathlib import Path
from collections import Counter


STOP = "|"


def read_text_file(file_name: str) -> str:
    return Path(file_name).read_text(encoding="utf-8")


def clean_input(text: str) -> str:
    return re.sub(r"[^A-Za-z]+", " ", text).strip()


def txt_into_words(text: str) -> list[str]:
    return clean_input(text).split()


def build_corpus(words: list[str]) -> dict[tuple[str, ...], int]:

    return {tuple(word) + (STOP,): count
            for word, count in Counter(words).items()}


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("K", type=int)
    parser.add_argument("TRAIN_FILE", type=Path)
    parser.add_argument("TEST_FILE", type=Path)

    args = parser.parse_args()

    if not 1 <= args.K <= 5:
        parser.error("K must be between 1 and 5")

    for file_path, file_label in (
        (args.TRAIN_FILE, "Training"),
        (args.TEST_FILE, "Test"),
    ):
        if not file_path.is_file():
            parser.error(f"{file_label} file does not exist: {file_path}")

    K = args.K
    train_text = read_text_file(args.TRAIN_FILE)
    test_text = read_text_file(args.TEST_FILE)

    train_text= txt_into_words(train_text)
    test_text = txt_into_words(test_text)

    print(test_text)


    


if __name__ == "__main__":
    main()



