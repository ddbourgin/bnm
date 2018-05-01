#!/usr/bin/env python

import argparse
from .sources import allmusic, pitchfork, resident_advisor, forced_exposure, boomkat

choices = ['am', 'p4k', 'ra', 'bk', 'fe']


def main():
    parser = argparse.ArgumentParser(
        description='View recent highly-rated albums in the terminal')
    parser.add_argument('source', type=str, choices=choices,
                        help=("Review source."))
    args = parser.parse_args()
    source = args.source.lower()

    if source not in choices:
        vals = ', '.join(["'{}'".format(c) for c in choices])
        parser.error(
            "Unrecognized source '{}'. Valid entries are {}."
            .format(args.source, vals)
        )

    elif source == 'am':
        allmusic()
    elif source == 'p4k':
        pitchfork()
    elif source == 'ra':
        resident_advisor()
    elif source == 'fe':
        forced_exposure()
    elif source == 'bk':
        boomkat()


if __name__ == "__main__":
    main()
