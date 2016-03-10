# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import abc
import sys
import time
import traceback

from future.utils import raise_

from .exceptions import EzOutletError, EzOutletUsageError

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import requests

from . import constants
from ezoutlet.parser import Parser


def _get_url(hostname, path):
    return urlparse.urlunparse(('http', hostname, path, '', '', ''))


class EzOutlet:
    """Uses ezOutlet EZ-11b to reset a device.

    Uses the ezOutlet EZ-11b Internet IP-Enabled Remote Power Reboot Switch to
    reset a device under test (DUT).

    In addition to reset(), post_fail() is provided, meant to be given as a
    callback to a Session object.

    It uses undocumented but simple CGI scripts.
    """
    DEFAULT_EZ_OUTLET_RESET_INTERVAL = constants.DEFAULT_EZ_OUTLET_RESET_INTERVAL
    DEFAULT_TIMEOUT = 10
    DEFAULT_WAIT_TIME = 0
    RESET_URL_PATH = '/reset.cgi'
    EXPECTED_RESPONSE_CONTENTS = '0,0'
    NO_RESPONSE_MSG = "No response from EzOutlet after {0} seconds."
    UNEXPECTED_RESPONSE_MSG = ("Unexpected response from EzOutlet. Expected: " +
                               repr(EXPECTED_RESPONSE_CONTENTS) +
                               " Actual: {0}")
    LOG_REQUEST_MSG = 'HTTP GET {0}'

    def __init__(self, hostname, timeout=DEFAULT_TIMEOUT):
        """
        Args:
            hostname: Hostname or IP address of device.
            timeout: Time in seconds to wait for the EzOutlet to respond.
        """
        self._hostname = hostname
        self._timeout = timeout

    @property
    def url(self):
        return _get_url(self._hostname, self.RESET_URL_PATH)

    def reset(self, post_reset_delay=DEFAULT_WAIT_TIME, ez_outlet_reset_interval=DEFAULT_EZ_OUTLET_RESET_INTERVAL):
        """Send reset request to ezOutlet, check response, wait for reset.

        After sending HTTP request and receiving response, wait
        dut_reset_delay + ez_outlet_reset_interval seconds.

        If the outlet does not respond (after self._timeout seconds), or gives
        an unexpected response, this method will raise an exception.

        Args:
            post_reset_delay: Time in seconds to allow the device being reset
                to reboot. See also reset_delay.
            ez_outlet_reset_interval: Time to wait before returning (besides
                dut_reset_delay). This should be configured to match the time
                the ezOutlet device actually takes to turn off and on again.
                Set to 0 to make this method non-blocking.

        Returns: HTTP response contents.

        Raises:
            EzOutletResetError: If the reset fails due to:
                - no response in self._timeout seconds or
                - unexpected response contents (see
                  EzOutletReset.EXPECTED_RESPONSE_CONTENTS)
        """
        response = self._http_get(self.url)

        self._check_response_raise_if_unexpected(response)

        self._wait_for_reset(post_reset_delay + ez_outlet_reset_interval)

        return response

    def _http_get(self, url):
        """HTTP GET and return response.

        Args:
            url: Target to GET.

        Returns: Response contents.

        Raises:
            EzOutletResetError: If the reset fails due to:
                - no response in self._timeout seconds
        """
        try:
            return requests.get(url,
                                timeout=self._timeout,
                                proxies={"http": None, "https": None}).text
        except requests.exceptions.ConnectTimeout:
            raise_(EzOutletError(self.NO_RESPONSE_MSG.format(self._timeout)),
                   None,
                   sys.exc_info()[2])

    def _check_response_raise_if_unexpected(self, response):
        """Raise if response is unexpected.

        Args:
            response: Response.

        Returns: None

        Raises:
            EzOutletResetError: If the reset fails due to:
                - unexpected response contents (see
                  EzOutletReset.EXPECTED_RESPONSE_CONTENTS)
        """
        if response != self.EXPECTED_RESPONSE_CONTENTS:
            raise EzOutletError(self.UNEXPECTED_RESPONSE_MSG.format(response))

    @staticmethod
    def _wait_for_reset(total_delay):
        """Sleep for self._reset_delay + self._dut_reset_time.

        Returns: None
        """
        time.sleep(total_delay)


class _ICommand(object):
    """ Interface for Commands for this application.

    Implementors: Parsed arguments from argparse should be taken and checked
    for validity in the constructor.
    """
    @abc.abstractmethod
    def run(self):
        """ Run the command. """


class _ResetCommand(_ICommand):
    def __init__(self, parsed_args):
        self._args = parsed_args
        self._check_args()

    def _check_args(self):
        if self._args.reset_time < 0:
            raise EzOutletUsageError(constants.RESET_TIME_NEGATIVE_ERROR_MESSAGE)

    def run(self):
        ez_outlet = EzOutlet(hostname=self._args.target)
        ez_outlet.reset(post_reset_delay=self._args.reset_time)


class _NoCommand(_ICommand):
    def __init__(self, parsed_args):
        self._args = parsed_args

    def run(self):
        _print_help()


def _command_factory(subcommand, parsed_args):
    if subcommand == 'reset':
        return _ResetCommand(parsed_args=parsed_args)
    else:
        # Note: In Python 2, argparse will raise a SystemException when no
        # command is given, so this bit is for Python 3.
        return _NoCommand(parsed_args=parsed_args)


_parser = Parser()


def _print_usage():
    print(_parser.get_usage(), file=sys.stderr)


def _print_help():
    print(_parser.get_help(), file=sys.stderr)


def _print_error(msg):
    print(constants.ERROR_STRING.format(constants.PROGRAM_NAME, msg), file=sys.stderr)


def _usage_error(exception):
    _print_usage()
    _print_error(msg=exception)
    sys.exit(constants.EXIT_CODE_PARSER_ERR)


def _handle_error(exception):
    _print_error(msg=exception)
    sys.exit(constants.EXIT_CODE_ERR)


def _handle_unexpected_error(exception):
    _ = exception  # exception gets printed by traceback.format_exc()
    _print_error(msg=constants.UNHANDLED_ERROR_MESSAGE.format(traceback.format_exc()))
    sys.exit(constants.EXIT_CODE_ERR)


def _parse_args_and_run(argv):
    parsed_args = _parser.parse_args(argv)
    cmd = _command_factory(parsed_args.subcommand, parsed_args)
    cmd.run()


def main(argv):
    try:
        _parse_args_and_run(argv)
    except EzOutletUsageError as e:
        _usage_error(e)
    except EzOutletError as e:
        _handle_error(e)
    except Exception as e:
        _handle_unexpected_error(e)


if __name__ == "__main__":
    main(sys.argv)
