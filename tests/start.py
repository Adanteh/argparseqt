from pathlib import Path
import sys

parent = str(Path(__file__).parents[1])
if parent not in sys.path:
    sys.path.insert(0, parent)

import argparse  # noqa: E402
from argparseqt.decorator import QtArgparsed  # noqa :E402


@QtArgparsed("Arma terrain utils")
def main():
    parser = argparse.ArgumentParser(description="Main settings")
    parser.add_argument("--storeConst", action="store_const", const=999)

    textSettings = parser.add_argument_group("Strings", description="Text input")
    textSettings.add_argument(
        "--freetext", type=str, default="Enter freetext here", help="Type anything you want here",
    )
    textSettings.add_argument(
        "--pickText",
        default="I choo-choo-choose you",
        choices=["Bee mine", "I choo-choo-choose you"],
        help="Choose one of these",
    )

    return parser


if __name__ == "__main__":
    main()
