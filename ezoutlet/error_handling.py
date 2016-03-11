# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import traceback

from . import parser, constants


def usage_error(exception):
    """Handle an error in command line arguments.

    :param exception: Exception caught.
    :return: constants.EXIT_CODE_PARSER_ERR
    """
    parser.print_usage()
    parser.print_error(msg=exception)
    return constants.EXIT_CODE_PARSER_ERR


def runtime_error(exception):
    """Handle a runtime error, e.g., an unresponsive server.

    :param exception: Exception caught.
    :return: constants.EXIT_CODE_ERR
    """
    parser.print_error(msg=exception)
    return constants.EXIT_CODE_ERR


def unexpected_exception(exception):
    """Handle an unexpected exception.

    :param exception: Exception caught.
    :return: constants.EXIT_CODE_ERR
    """
    _ = exception  # exception gets printed by traceback.format_exc()
    parser.print_error(msg=constants.UNHANDLED_ERROR_MESSAGE.format(traceback.format_exc()))
    return constants.EXIT_CODE_ERR
