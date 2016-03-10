# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

PROGRAM_NAME = os.path.basename(__file__)

DEFAULT_EZ_OUTLET_RESET_INTERVAL = 3.05
EXIT_CODE_ERR = 1
EXIT_CODE_PARSER_ERR = 2

# Arguments and commands
RESET_TIME_ARG_SHORT = '-t'
RESET_TIME_ARG_LONG = '--reset-time'

# Help strings
HELP_TEXT = (
    """Send reset command to ezOutlet EZ-11b device; wait for on/off cycle.

    Use --reset-time to wait additional time, e.g. for device reboot."""
)
HELP_TEXT_TARGET_ARG = 'IP address/hostname of ezOutlet device.'
HELP_TEXT_RESET_TIME_ARG = 'Extra time in seconds to wait, e.g. for device reboot.' \
                           ' Note that the script already waits {0} seconds for the' \
                           ' ezOutlet to turn off and on.'.format(DEFAULT_EZ_OUTLET_RESET_INTERVAL)

# Errors
ERROR_STRING = "{0}: error: {1}"
UNHANDLED_ERROR_MESSAGE = "Unhandled exception! Please file bug report.\n\n{0}"
RESET_TIME_NEGATIVE_ERROR_MESSAGE = "argument{0}/{1}: value must be non-negative.".format(RESET_TIME_ARG_LONG,
                                                                                          RESET_TIME_ARG_SHORT)
