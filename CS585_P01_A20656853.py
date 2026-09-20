import argparse
import re
from pathlib import Path
import string


def clean_input(text):
    text = "".join(
        character
        for character in text
        if character == " " or character.isprintable()
    )

    return text.translate(
        str.maketrans("", "", string.punctuation)
    )

def txt_into_characters(text: str):

    cleaned_text = clean_input(text)


    cleaned_text  = re.sub(r"\s+", "|", cleaned_text)

    return cleaned_text




def read_text_file(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


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

    train_text= txt_into_characters(train_text)
    test_text = txt_into_characters(test_text)

    print(test_text)


    


if __name__ == "__main__":
    main()



