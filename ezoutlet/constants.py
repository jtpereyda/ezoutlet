# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import __version__
from . import __name__ as package_name

import os

PROGRAM_NAME = os.path.basename(__file__)
VERSION_FORMAT_STRING = package_name + ' {0}'
VERSION_STRING = VERSION_FORMAT_STRING.format(__version__)

DEFAULT_EZ_OUTLET_RESET_INTERVAL = 3.05
EXIT_CODE_OK = 0
EXIT_CODE_ERR = 1
EXIT_CODE_PARSER_ERR = 2

# Arguments and commands
RESET_TIME_ARG_SHORT = '-t'
RESET_TIME_ARG_LONG = '--reset-time'

# Help strings
HELP_TEXT = (
    """Control an ezOutlet EZ-11b device."""
)
HELP_TEXT_RESET = "Send reset command; wait for on/off cycle."
HELP_TEXT_VERSION = "Print version"
HELP_TEXT_TARGET_ARG = 'IP address/hostname of ezOutlet device.'
HELP_TEXT_RESET_TIME_ARG = 'Extra time in seconds to wait, e.g. for device reboot.' \
                           ' Note that the script already waits {0} seconds for the' \
                           ' ezOutlet to turn off and on.'.format(DEFAULT_EZ_OUTLET_RESET_INTERVAL)

# Errors
ERROR_STRING = "{0}: error: {1}"
UNHANDLED_ERROR_MESSAGE = "Unhandled exception! Please file bug report.\n\n{0}"
RESET_TIME_NEGATIVE_ERROR_MESSAGE = "argument{0}/{1}: value must be non-negative.".format(RESET_TIME_ARG_LONG,
                                                                                          RESET_TIME_ARG_SHORT)
