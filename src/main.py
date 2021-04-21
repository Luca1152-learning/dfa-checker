import argparse
import sys

from src.definitions import ROOT_DIR
from src.dfa.dfa import DFA


def _init_argparse():
    parser = argparse.ArgumentParser("check whether words are in a DFA's language")
    parser.add_argument("file", metavar="INPUT FILE", type=str, help="the DFA input file's name")

    # Show the help message by default when arguments aren't provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the received arguments and store them in args's members
    args = parser.parse_args()

    # The INPUT FILE argument was provided
    if args.file:
        _run_for_file_name(args.file)


def _run_for_file_name(file_name: str):
    path = ROOT_DIR / "res" / file_name

    dfa = DFA()
    try:
        words_to_check = dfa.load_from_file(path).split('\n')[1:]
        for word in words_to_check:
            path = dfa.is_in_language(word)
            if path:
                print("DA")
                print(f"Traseu: {' '.join((str(x) for x in path))}")
            else:
                print("NU")
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found in the 'res/' directory.")


if __name__ == '__main__':
    _init_argparse()
