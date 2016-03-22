# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import re
import unittest

import sys

import ezoutlet
import ezoutlet.constants
import ezoutlet.exceptions
import ezoutlet.parser

try:
    # mock in Python 2, unittest.mock in Python 3
    import unittest.mock as mock
except ImportError:
    # mock is required as an extras_require:
    # noinspection PyPackageRequirements
    import mock
try:
    # Choose StringIO implementation based on Python version in use.
    # StringIO should work for Python 2, but not 3.
    # Why:
    # Hybrid-safe code should not need StringIO.StringIO, unless:
    #  - You want to mock out sys.stdout/stderr using io.StringIO, but
    #  - You use a non hybrid-safe dependent library that confuses
    #    bytes/unicode/str (Python 2 argparse does this, for example).
    from StringIO import StringIO as Py23FlexibleStringIO
except ImportError:
    from io import StringIO as Py23FlexibleStringIO

import pytest

from ezoutlet import ez_outlet

EXIT_CODE_OK = 0
EXIT_CODE_ERR = 1
EXIT_CODE_PARSER_ERR = 2
EZ_OUTLET_RESET_DEFAULT_WAIT_TIME = ez_outlet.EzOutlet.DEFAULT_WAIT_TIME


class TestMainReset(unittest.TestCase):
    arbitrary_msg_1 = 'arbitrary message'
    arbitrary_msg_2 = '"Always check a module in cleaner than when you checked it out." --Uncle Bob'

    sample_url = 'DEAD STRINGS TELL NO TALES'
    expected_response_contents = ez_outlet.EzOutlet.EXPECTED_RESPONSE_CONTENTS
    unexpected_response_contents = '1,0'

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_reset_cmd(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with a single argument.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == ez_outlet.DEFAULT_WAIT_TIME.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
         and: EXIT_CODE_OK is returned
        """
        hostname = '255.254.253.252'
        args = ['ez_outlet.py', 'reset', hostname]

        exit_code = ezoutlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        # Duplicate reference to DEFAULT_WAIT_TIME needed because
        # we mocked away EzOutlet.
        mock_ez_outlet.return_value.reset.assert_called_once_with(
            post_reset_delay=EZ_OUTLET_RESET_DEFAULT_WAIT_TIME)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''
        assert exit_code == EXIT_CODE_OK

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_reset_cmd_reset_time_long(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and --reset-time arguments.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == given value.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
         and: EXIT_CODE_OK is returned
        """
        hostname = '255.254.253.252'
        wait_time = 77
        args = ['ez_outlet.py', 'reset', hostname, ezoutlet.constants.RESET_TIME_ARG_LONG, str(wait_time)]

        exit_code = ezoutlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        mock_ez_outlet.return_value.reset.assert_called_once_with(post_reset_delay=wait_time)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''
        assert exit_code == EXIT_CODE_OK

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_reset_cmd_reset_time_short(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and -t arguments.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == given value.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
         and: EXIT_CODE_OK is returned
        """
        hostname = '255.254.253.252'
        wait_time = 1
        args = ['ez_outlet.py', 'reset', hostname, ezoutlet.constants.RESET_TIME_ARG_SHORT, str(wait_time)]

        exit_code = ezoutlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        mock_ez_outlet.return_value.reset.assert_called_once_with(post_reset_delay=wait_time)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''
        assert exit_code == EXIT_CODE_OK

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_reset_cmd_missing_target(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with no arguments.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR includes ".*: error: too few arguments"
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py', 'reset']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        # Error message differs between Python 2 and 3 versions of argparse
        assert re.search(".*: (error: too few arguments|the following arguments are required:)",
                         ez_outlet.sys.stderr.getvalue()) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_reset_cmd_unknown_arg(self, ):
        """
        Given: Mock EzOutlet.
        When: Calling main() with required arguments and an extra unknown argument.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR <= ".*: error: unrecognized arguments: {0}".format(bad_arg)
         and: STDOUT is silent.
        """
        bad_arg = '--blab'
        args = ['ez_outlet.py', 'reset', '1.2.3.4', bad_arg]

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        assert re.search(".*: error: unrecognized arguments: {0}".format(bad_arg),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_reset_cmd_reset_time_negative(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and negative reset time argument.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                      ez_outlet.RESET_TIME_NEGATIVE_ERROR_MESSAGE)
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py', 'reset', '1.2.3.4', ezoutlet.constants.RESET_TIME_ARG_LONG, str(-1)]

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        assert re.search(ezoutlet.constants.ERROR_STRING.format(ezoutlet.constants.PROGRAM_NAME,
                                                                ezoutlet.constants.RESET_TIME_NEGATIVE_ERROR_MESSAGE),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    @mock.patch.object(ezoutlet.parser.Parser, 'parse_args',
                       side_effect=ezoutlet.exceptions.EzOutletUsageError(arbitrary_msg_1))
    def test_error_handling_ez_outlet_reset_usage_error(self, mock_parser):
        """
        Given: Mock ez_outlet._Parser() configured to raise on
               parse_args().
          and: Mock STDERR, STDOUT.
         When: Calling main().
         Then: EXIT_CODE_PARSER_ERR is returned
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_1)
          and: STDOUT is silent.
          and: Mock ez_outlet._Parser.parse_args() was called.
        """
        args = ['ez_outlet.py', 'reset', '1.2.3.4']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        assert re.search(ezoutlet.constants.ERROR_STRING.format(ezoutlet.constants.PROGRAM_NAME, self.arbitrary_msg_1),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

        mock_parser.assert_called_with(args)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch.object(ez_outlet.EzOutlet, 'reset',
                       side_effect=ezoutlet.exceptions.EzOutletError(arbitrary_msg_2))
    def test_error_handling_ez_outlet_reset_error(self, mock_ez_outlet):
        """
        Given: Mock ez_outlet.EzOutlet() configured to raise on
               EzOutletError on reset().
          and: Mock STDERR, STDOUT.
         When: Calling main().
         Then: EXIT_CODE_ERR is returned
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_2)
          and: STDOUT is silent.
          and: Mock ez_outlet.EzOutlet.reset() was called.
        """
        args = ['ez_outlet.py', 'reset', '1.2.3.4']

        # When
        exit_code = ezoutlet.main(args)

        # Then
        assert exit_code == EXIT_CODE_ERR

        assert re.search(ezoutlet.constants.ERROR_STRING.format(ezoutlet.constants.PROGRAM_NAME, self.arbitrary_msg_2),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

        mock_ez_outlet.assert_called_with(post_reset_delay=ez_outlet.EzOutlet.DEFAULT_WAIT_TIME)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch.object(ez_outlet.EzOutlet, 'reset',
                       side_effect=Exception(arbitrary_msg_2))
    def test_error_handling_unhandled_error(self, mock_ez_outlet):
        """
        Given: Mock ez_outlet.EzOutlet.reset() configured to raise an
               Exception on reset().
          and: Mock STDERR, STDOUT.
         When: Calling main().
         Then: EXIT_CODE_ERR is returned
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                       ez_outlet.UNHANDLED_ERROR_MESSAGE.format(
                                                                 "Traceback.*{0}.*".format(self.arbitrary_msg_2)))
          and: STDOUT is silent.
          and: Mock ez_outlet.EzOutlet.reset() was called.
        """
        args = ['ez_outlet.py', 'reset', '1.2.3.4']

        # When
        exit_code = ezoutlet.main(args)

        # Then
        assert exit_code == EXIT_CODE_ERR

        assert re.search(ezoutlet.constants.ERROR_STRING.format(ezoutlet.constants.PROGRAM_NAME,
                                                                ezoutlet.constants.UNHANDLED_ERROR_MESSAGE.format(
                                                                    "Traceback.*{0}.*".format(self.arbitrary_msg_2))),
                         ez_outlet.sys.stderr.getvalue(),
                         flags=re.DOTALL) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

        mock_ez_outlet.assert_called_with(post_reset_delay=ez_outlet.EzOutlet.DEFAULT_WAIT_TIME)


class TestMainVersion(unittest.TestCase):

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_version_command(self):
        """
        Given Nothing
        When Calling main() with 'version' argument
        Then EXIT_CODE_OK is returned
         and Application name and version are printed on STDOUT
         and STDERR is quiet
        """
        args = ['ez_outlet.py', 'version']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_OK

        assert re.match('\s*{0} {1}\s*'.format('ezoutlet', ezoutlet.__version__),
                        ez_outlet.sys.stdout.getvalue())

        assert ez_outlet.sys.stderr.getvalue() == ''


class TestMainNoCommand(unittest.TestCase):
    @pytest.mark.skipif(sys.version_info >= (3, 3),
                        reason="Behavior differs based on version.")
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_missing_cmd_py2(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with no arguments.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR includes ".*: error: too few arguments"
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        assert re.search(".*: (error: too few arguments)",
                         ez_outlet.sys.stderr.getvalue()) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

    @pytest.mark.skipif(sys.version_info < (3, 3),
                        reason="Behavior differs based on version.")
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_missing_cmd_py3(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with no arguments.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR includes ".*: error: too few arguments"
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        err_msg = ez_outlet.sys.stderr.getvalue()

        assert re.search("usage:", err_msg) is not None
        assert re.search("positional arguments:", err_msg) is not None
        assert re.search("optional arguments:", err_msg) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=Py23FlexibleStringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=Py23FlexibleStringIO())
    def test_unknown_cmd(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with no arguments.
        Then: EXIT_CODE_PARSER_ERR is returned
         and: STDERR includes ".*: error: argument subcommand: invalid choice:"
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py', 'someUnknownCommand']

        exit_code = ezoutlet.main(args)

        assert exit_code == EXIT_CODE_PARSER_ERR

        # Error message differs between Python 2 and 3 versions of argparse
        assert re.search(".*: (error: argument subcommand: invalid choice:)",
                         ez_outlet.sys.stderr.getvalue()) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''
