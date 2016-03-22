# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .icommand import ICommand
from .. import parser
from .. import constants


class NoCommand(ICommand):
    def __init__(self, parsed_args):
        self._args = parsed_args

    def run(self):
        parser.print_help()
        return constants.EXIT_CODE_PARSER_ERR
