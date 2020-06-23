import argparse
from sys import version_info


class Serial(str):
    pass


def rgb(val):
    if len(val) != 6:
        raise argparse.ArgumentTypeError('Expected 6 characters but received "%s"' % val)

    try:
        return tuple(int(val[i : i + 2], 16) for i in (0, 2, 4))
    except:
        raise argparse.ArgumentTypeError("Invalid hex string: %s" % val)


def rgba(val):
    if len(val) != 8:
        raise argparse.ArgumentTypeError('Expected 8 characters but received "%s"' % val)

    try:
        return tuple(int(val[i : i + 2], 16) for i in (0, 2, 4, 6))
    except:
        raise argparse.ArgumentTypeError("Invalid hex string: %s" % val)


if version_info.minor >= 8:
    from typing import get_origin  # noqa: F401
else:

    def get_origin(data):
        """Finds the base datatype, with support for `typing` usage"""
        try:
            if version_info.minor == 7:
                return data.__origin__  # Python 3.7
            elif version_info.minor in (5, 6):
                return data.__extra__
        except AttributeError:
            return data.__class__
