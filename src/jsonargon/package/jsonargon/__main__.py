import argparse


def get_args():

    parser = argparse.ArgumentParser()
    # add here parser.add_argument("-x", "--example")
    args, _ = parser.parse_known_args()
    return args


def main():

    # Ger args
    args = get_args()

    # Use them: args.example


if __name__ == '__main__':
    main()
