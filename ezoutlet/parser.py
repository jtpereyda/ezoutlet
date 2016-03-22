# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from . import constants


def print_error(msg):
    print(constants.ERROR_STRING.format(constants.PROGRAM_NAME, msg), file=sys.stderr)


def print_help():
    print(static_parser.get_help(), file=sys.stderr)


def print_usage():
    print(static_parser.get_usage(), file=sys.stderr)


class Parser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description=constants.HELP_TEXT)
        subparsers = self._parser.add_subparsers(dest='subcommand')

        _add_reset_parser(subparsers)
        _add_version_parser(subparsers)

    def get_usage(self):
        return self._parser.format_usage()

    def get_help(self):
        return self._parser.format_help()

    def parse_args(self, argv):
        return self._parser.parse_args(argv[1:])


def _add_reset_parser(subparsers):
    parser_reset = subparsers.add_parser('reset', help=constants.HELP_TEXT_RESET)
    parser_reset.add_argument('target', help=constants.HELP_TEXT_TARGET_ARG)
    parser_reset.add_argument(constants.RESET_TIME_ARG_LONG, constants.RESET_TIME_ARG_SHORT,
                              type=float,
                              default=0,
                              help=constants.HELP_TEXT_RESET_TIME_ARG)


def _add_version_parser(subparsers):
    subparsers.add_parser('version', help=constants.HELP_TEXT_VERSION)


static_parser = Parser()
