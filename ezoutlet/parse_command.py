# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .no_command import NoCommand
from .reset_command import ResetCommand
from .version_command import VersionCommand


def parse_command(subcommand, parsed_args):
    if subcommand == 'reset':
        return ResetCommand(parsed_args=parsed_args)
    elif subcommand == 'version':
        return VersionCommand(parsed_args=parsed_args)
    else:
        # Note: In Python 2, argparse will raise a SystemException when no
        # command is given, so this bit is for Python 3.
        return NoCommand(parsed_args=parsed_args)
