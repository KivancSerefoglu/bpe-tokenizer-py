import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("K", type=int)
    parser.add_argument("TRAIN_FILE", type=str)
    parser.add_argument("TEST_FILE", type=str)

    args = parser.parse_args()


    K= args.K
    TRAIN_FILE = args.TRAIN_FILE
    TEST_FILE = args.TEST_FILE

    if K < 1 or K > 5:
        K = 5

    if not TRAIN_FILE.is_file():
        parser.error(f"Training file does not exist: {TRAIN_FILE}")

    if not TEST_FILE.is_file():
        parser.error(f"Test file does not exist: {TEST_FILE}")

    print(K, TRAIN_FILE, TEST_FILE)


    


if __name__ == "__main__":
    main()



