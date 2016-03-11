# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import exceptions
from . import constants
from . import ez_outlet
from .icommand import ICommand


class ResetCommand(ICommand):
    def __init__(self, parsed_args):
        self._args = parsed_args
        self._check_args()

    def _check_args(self):
        if self._args.reset_time < 0:
            raise exceptions.EzOutletUsageError(constants.RESET_TIME_NEGATIVE_ERROR_MESSAGE)

    def run(self):
        ez = ez_outlet.EzOutlet(hostname=self._args.target)
        ez.reset(post_reset_delay=self._args.reset_time)
        return constants.EXIT_CODE_OK
