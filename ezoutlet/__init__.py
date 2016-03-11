# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import error_handling
from . import constants
from . import parser
from .exceptions import EzOutletError, EzOutletUsageError
from .ez_outlet import EzOutlet
from .no_command import NoCommand
from .parse_command import parse_command
from .reset_command import ResetCommand

__version__ = '0.0.1-dev3'


def main(argv):
    try:
        return _parse_args_and_run(argv)
    except EzOutletUsageError as e:
        return error_handling.usage_error(e)
    except EzOutletError as e:
        return error_handling.runtime_error(e)
    except Exception as e:
        return error_handling.unexpected_exception(e)
    except SystemExit as e:
        return e.code


def _parse_args_and_run(argv):
    parsed_args = parser.static_parser.parse_args(argv)
    cmd = parse_command(parsed_args.subcommand, parsed_args)
    return cmd.run()
