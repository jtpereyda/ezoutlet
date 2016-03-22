# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .. import constants
from .icommand import ICommand


class VersionCommand(ICommand):
    def __init__(self, parsed_args):
        self._args = parsed_args
        self._check_args()

    def _check_args(self):
        # version command accepts anything
        pass

    def run(self):
        print(constants.VERSION_STRING)
        return constants.EXIT_CODE_OK
