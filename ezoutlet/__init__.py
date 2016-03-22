# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = '1.0'

from . import constants
from . import error_handling
from . import exceptions
from . import ez_outlet
from . import parser
from .commands import parse_command

__all__ = [ez_outlet.EzOutlet,
           exceptions.EzOutletError, exceptions.EzOutletUsageError]


def main(argv):
    try:
        return _parse_args_and_run(argv)
    except exceptions.EzOutletUsageError as e:
        return error_handling.usage_error(e)
    except exceptions.EzOutletError as e:
        return error_handling.runtime_error(e)
    except Exception as e:
        return error_handling.unexpected_exception(e)
    except SystemExit as e:
        return e.code


def _parse_args_and_run(argv):
    parsed_args = parser.static_parser.parse_args(argv)
    cmd = parse_command.parse_command(parsed_args.subcommand, parsed_args)
    return cmd.run()
