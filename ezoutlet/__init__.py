# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import traceback

from .parse_command import parse_command
from . import constants
from . import parser
from .exceptions import EzOutletError, EzOutletUsageError
from .ez_outlet import EzOutlet
from .no_command import NoCommand
from .reset_command import ResetCommand

__version__ = '0.0.1-dev3'


def _parse_args_and_run(argv):
    parsed_args = parser.static_parser.parse_args(argv)
    cmd = parse_command(parsed_args.subcommand, parsed_args)
    cmd.run()


def _usage_error(exception):
    parser.print_usage()
    parser.print_error(msg=exception)
    sys.exit(constants.EXIT_CODE_PARSER_ERR)


def _handle_error(exception):
    parser.print_error(msg=exception)
    sys.exit(constants.EXIT_CODE_ERR)


def _handle_unexpected_error(exception):
    _ = exception  # exception gets printed by traceback.format_exc()
    parser.print_error(msg=constants.UNHANDLED_ERROR_MESSAGE.format(traceback.format_exc()))
    sys.exit(constants.EXIT_CODE_ERR)


def main(argv):
    try:
        _parse_args_and_run(argv)
    except EzOutletUsageError as e:
        _usage_error(e)
    except EzOutletError as e:
        _handle_error(e)
    except Exception as e:
        _handle_unexpected_error(e)
