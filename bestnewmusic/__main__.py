#!/usr/bin/env python

import argparse

from .sources import (
    allmusic,
    boomkat,
    forced_exposure,
    midheaven,
    pitchfork,
    resident_advisor,
    wfmu,
)

choices = ["am", "p4k", "ra", "bk", "fe", "mh", "wfmu"]


def main():
    parser = argparse.ArgumentParser(
        description="View recent releases and their reviews from the command line",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "source",
        type=str,
        choices=choices,
        help="""\
- am   : AllMusic Editor's Choice
- p4k  : Pitchfork 8.0+ Albums
- ra   : Resident Advisor Recommends
- bk   : Boomkat Weekly Best Sellers
- mh   : Midheaven Weekly Best Sellers
- fe   : Forced Exposure Weekly Best Sellers
- wfmu : WFMU Weekly Charts""",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Display items in reverse order (with most recent last)",
    )
    args = parser.parse_args()
    source = args.source.lower()
    reverse = args.reverse

    if source not in choices:
        vals = ", ".join(["'{}'".format(c) for c in choices])
        parser.error(
            "Unrecognized source '{}'. Valid entries are {}.".format(args.source, vals)
        )
    elif source == "am":
        allmusic(oldest_first=reverse)
    elif source == "p4k":
        pitchfork(oldest_first=reverse)
    elif source == "ra":
        resident_advisor(oldest_first=reverse)
    elif source == "fe":
        forced_exposure(oldest_first=reverse)
    elif source == "bk":
        boomkat(oldest_first=reverse)
    elif source == "wfmu":
        wfmu(oldest_first=reverse)
    elif source == "mh":
        midheaven(oldest_first=reverse)


if __name__ == "__main__":
    main()
