import argparse
import re
import time
from pathlib import Path
from collections import Counter


STOP = "|"

LAST_NAME = "Serefoglu"
FIRST_NAME = "Kivanc"
A_NUMBER = "A20656853"


def read_text_file(file_name: Path) -> str:
    return file_name.read_text(encoding="utf-8", errors="ignore")


def clean_input(text: str) -> str:
    return re.sub(r"[^A-Za-z]+", " ", text).strip()


def txt_into_words(text: str) -> list[str]:
    return clean_input(text).split()


def build_corpus(words: list[str]) -> dict[tuple[str, ...], int]:
    return {
        tuple(word) + (STOP,): count
        for word, count in Counter(words).items()
    }


def get_pair_counts(
    corpus: dict[tuple[str, ...], int]
) -> Counter:

    pair_counts = Counter()

    for word, frequency in corpus.items():
        for i in range(len(word) - 1):
            pair = (word[i], word[i + 1])
            pair_counts[pair] += frequency

    return pair_counts


def get_best_pair(
    pair_counts: Counter
) -> tuple[str, str] | None:

    if not pair_counts:
        return None

    return max(pair_counts, key=pair_counts.get)


def merge_pair(
    corpus: dict[tuple[str, ...], int],
    best_pair: tuple[str, str]
) -> dict[tuple[str, ...], int]:

    new_corpus = {}

    for word, frequency in corpus.items():

        new_word = []
        i = 0

        while i < len(word):

            if (
                i < len(word) - 1
                and word[i] == best_pair[0]
                and word[i + 1] == best_pair[1]
            ):
                new_word.append(word[i] + word[i + 1])
                i += 2

            else:
                new_word.append(word[i])
                i += 1

        new_corpus[tuple(new_word)] = frequency

    return new_corpus


def train_bpe(
    corpus: dict[tuple[str, ...], int],
    K: int
):
    merges = []

    for _ in range(K):

        pair_counts = get_pair_counts(corpus)

        if not pair_counts:
            break

        best_pair = get_best_pair(pair_counts)

        if best_pair is None:
            break

        merges.append(best_pair)

        corpus = merge_pair(corpus, best_pair)

    return corpus, merges


def build_vocabulary(
    merges: list[tuple[str, str]]
) -> list[str]:

    vocab = []

    # Initial vocabulary: A-Z
    for code in range(ord("A"), ord("Z") + 1):
        vocab.append(chr(code))

    # Initial vocabulary: a-z
    for code in range(ord("a"), ord("z") + 1):
        vocab.append(chr(code))

    # Stop token
    vocab.append(STOP)

    # Add learned BPE tokens in merge order
    for pair in merges:

        new_token = pair[0] + pair[1]

        if new_token not in vocab:
            vocab.append(new_token)

    return vocab


def tokenize_word(
    word: str,
    merges: list[tuple[str, str]]
) -> list[str]:

    tokens = list(word) + [STOP]

    # Apply learned merges in training order
    for pair in merges:

        new_tokens = []
        i = 0

        while i < len(tokens):

            if (
                i < len(tokens) - 1
                and tokens[i] == pair[0]
                and tokens[i + 1] == pair[1]
            ):
                new_tokens.append(tokens[i] + tokens[i + 1])
                i += 2

            else:
                new_tokens.append(tokens[i])
                i += 1

        tokens = new_tokens

    return tokens


def tokenize_text(
    words: list[str],
    merges: list[tuple[str, str]]
) -> list[str]:

    result = []

    for word in words:
        tokens = tokenize_word(word, merges)
        result.extend(tokens)

    return result


def save_vocabulary(
    vocab: list[str],
    file_name: Path
):

    with file_name.open("w", encoding="utf-8") as file:

        for token in vocab:
            file.write(token + "\n")


def save_result(
    tokens: list[str],
    file_name: Path
):

    with file_name.open("w", encoding="utf-8") as file:
        file.write(" ".join(tokens))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("K", type=int)
    parser.add_argument("TRAIN_FILE", type=Path)
    parser.add_argument("TEST_FILE", type=Path)

    args = parser.parse_args()



    K = args.K


    if K <= 0:
        K = 5


    script_directory = Path(__file__).resolve().parent

    train_file = script_directory / args.TRAIN_FILE.name
    test_file = script_directory / args.TEST_FILE.name

    if not train_file.is_file():
        parser.error(
            f"Training file does not exist: {args.TRAIN_FILE.name}"
        )

    if not test_file.is_file():
        parser.error(
            f"Test file does not exist: {args.TEST_FILE.name}"
        )


    train_text = read_text_file(train_file)
    test_text = read_text_file(test_file)



    train_words = txt_into_words(train_text)
    test_words = txt_into_words(test_text)

    train_corpus = build_corpus(train_words)

  

    training_start = time.perf_counter()

    _, merges = train_bpe(
        train_corpus,
        K
    )

    vocab = build_vocabulary(merges)

    training_end = time.perf_counter()

    training_time = training_end - training_start

    # ---------------------------
    # Test Tokenization
    # ---------------------------

    tokenization_start = time.perf_counter()

    test_tokens = tokenize_text(
        test_words,
        merges
    )

    tokenization_end = time.perf_counter()

    tokenization_time = (
        tokenization_end - tokenization_start
    )

    # ---------------------------
    # Output file names
    # ---------------------------

    vocab_file = (
        script_directory
        / f"CS585_P01_{A_NUMBER}_VOCAB.txt"
    )

    result_file = (
        script_directory
        / f"CS585_P01_{A_NUMBER}_RESULT.txt"
    )

    # ---------------------------
    # Save files
    # ---------------------------

    save_vocabulary(
        vocab,
        vocab_file
    )

    save_result(
        test_tokens,
        result_file
    )

    # ---------------------------
    # Screen output
    # ---------------------------

    print(
        f"{LAST_NAME}, {FIRST_NAME}, "
        f"{A_NUMBER} solution:"
    )

    print(f"Number of merges: {K}")
    print(
        f"Training file name: "
        f"{args.TRAIN_FILE.name}"
    )
    print(
        f"Test file name: "
        f"{args.TEST_FILE.name}"
    )

    print()

    print(
        f"Training time: "
        f"{training_time:.6f} seconds"
    )

    print(
        f"Tokenization time: "
        f"{tokenization_time:.6f} seconds"
    )

    print()

    # Only display first 20 tokens on screen
    if len(test_tokens) > 20:

        print(
            "Tokenization result:",
            " ".join(test_tokens[:20])
        )

        print(
            "Tokenized text is longer than 20 tokens"
        )

    else:

        print(
            "Tokenization result:",
            " ".join(test_tokens)
        )


if __name__ == "__main__":
    main()