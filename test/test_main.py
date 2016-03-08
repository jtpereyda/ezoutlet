# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from __future__ import print_function
from __future__ import unicode_literals

import io
import re
import unittest

import pytest

try:
    import unittest.mock as mock
except ImportError:
    # mock is required as an extras_require:
    # noinspection PyPackageRequirements
    import mock

from ezoutlet import ez_outlet

EXIT_CODE_ERR = 1
EXIT_CODE_PARSER_ERR = 2
EZ_OUTLET_RESET_DEFAULT_WAIT_TIME = ez_outlet.EzOutlet.DEFAULT_WAIT_TIME


class TestEzOutletReset(unittest.TestCase):
    """
    EzOutletReset.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """

    arbitrary_msg_1 = 'arbitrary message'
    arbitrary_msg_2 = '"Always check a module in cleaner than when you checked it out." --Uncle Bob'

    sample_url = 'DEAD STRINGS TELL NO TALES'
    expected_response_contents = ez_outlet.EzOutlet.EXPECTED_RESPONSE_CONTENTS
    unexpected_response_contents = '1,0'

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_main_basic(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with a single argument.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == ez_outlet.DEFAULT_WAIT_TIME.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
        """
        hostname = '255.254.253.252'
        args = ['ez_outlet.py', hostname]

        ez_outlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        # Duplicate reference to DEFAULT_WAIT_TIME needed because
        # we mocked away EzOutlet.
        mock_ez_outlet.return_value.reset.assert_called_once_with(
            post_reset_delay=EZ_OUTLET_RESET_DEFAULT_WAIT_TIME)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_main_reset_time_long(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and --reset-time arguments.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == given value.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
        """
        hostname = '255.254.253.252'
        wait_time = 77
        args = ['ez_outlet.py', hostname, ez_outlet.RESET_TIME_ARG_LONG, str(wait_time)]

        ez_outlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        mock_ez_outlet.return_value.reset.assert_called_once_with(post_reset_delay=wait_time)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.EzOutlet')
    def test_main_reset_time_short(self, mock_ez_outlet):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and -t arguments.
        Then: EzOutlet constructor is called with hostname == given value
              and wait_time == given value.
         and: EzOutlet.reset is called
         and: STDOUT is silent.
         and: STDERR is silent.
        """
        hostname = '255.254.253.252'
        wait_time = 1
        args = ['ez_outlet.py', hostname, ez_outlet.RESET_TIME_ARG_SHORT, str(wait_time)]

        ez_outlet.main(args)

        mock_ez_outlet.assert_called_once_with(hostname=hostname)
        mock_ez_outlet.return_value.reset.assert_called_once_with(post_reset_delay=wait_time)
        assert ez_outlet.sys.stdout.getvalue() == ''
        assert ez_outlet.sys.stderr.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    def test_main_missing_target(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with no arguments.
        Then: SystemExit is raised with code EXIT_CODE_PARSER_ERR
         and: STDERR includes ".*: error: too few arguments"
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py']

        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        assert exception_info.value.code == EXIT_CODE_PARSER_ERR

        # Error message differs between Python 2 and 3 versions of argparse
        assert re.search(".*: (error: too few arguments|the following arguments are required:)",
                         ez_outlet.sys.stderr.getvalue()) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    def test_main_unknown_arg(self, ):
        """
        Given: Mock EzOutlet.
        When: Calling main() with required arguments and an extra unknown argument.
        Then: SystemExit is raised with code EXIT_CODE_PARSER_ERR
         and: STDERR <= ".*: error: unrecognized arguments: {0}".format(bad_arg)
         and: STDOUT is silent.
        """
        bad_arg = '--blab'
        args = ['ez_outlet.py', '1.2.3.4', bad_arg]

        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        assert exception_info.value.code == EXIT_CODE_PARSER_ERR

        assert re.search(".*: error: unrecognized arguments: {0}".format(bad_arg),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    def test_main_reset_time_negative(self):
        """
        Given: Mock EzOutlet.
        When: Calling main() with hostname and negative reset time argument.
        Then: SystemExit is raised with code EXIT_CODE_PARSER_ERR
         and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                      ez_outlet.RESET_TIME_NEGATIVE_ERROR_MESSAGE)
         and: STDOUT is silent.
        """
        args = ['ez_outlet.py', '1.2.3.4', ez_outlet.RESET_TIME_ARG_LONG, str(-1)]

        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        assert exception_info.value.code == EXIT_CODE_PARSER_ERR

        assert re.search(ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                       ez_outlet.RESET_TIME_NEGATIVE_ERROR_MESSAGE),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch.object(ez_outlet._Parser, 'parse_args',
                       side_effect=ez_outlet.EzOutletUsageError(arbitrary_msg_1))
    def test_error_handling_ez_outlet_reset_usage_error(self, mock_parser):
        """
        Given: Mock ez_outlet._Parser() configured to raise on
               parse_args().
          and: Mock STDERR, STDOUT.
         When: Calling main().
         Then: SystemExit is raised with code EXIT_CODE_PARSER_ERR
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_1)
          and: STDOUT is silent.
          and: Mock ez_outlet._Parser.parse_args() was called.
        """
        args = ['ez_outlet.py', '1.2.3.4']

        # When
        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        # Then
        assert exception_info.value.code == EXIT_CODE_PARSER_ERR

        assert re.search(ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_1),
                         ez_outlet.sys.stderr.getvalue()) is not None
        assert ez_outlet.sys.stdout.getvalue() == ''

        mock_parser.assert_called_with(args)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch('ezoutlet.ez_outlet.sys.stdout', new=io.StringIO())
    @mock.patch('ezoutlet.ez_outlet.sys.stderr', new=io.StringIO())
    @mock.patch.object(ez_outlet.EzOutlet, 'reset',
                       side_effect=ez_outlet.EzOutletError(arbitrary_msg_2))
    def test_error_handling_ez_outlet_reset_error(self, mock_ez_outlet):
        """
        Given: Mock ez_outlet.EzOutlet() configured to raise on
               EzOutletError on reset().
          and: Mock STDERR, STDOUT.
         When: Calling main().
         Then: SystemExit is raised with code EXIT_CODE_ERR
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_2)
          and: STDOUT is silent.
          and: Mock ez_outlet.EzOutlet.reset() was called.
        """
        args = ['ez_outlet.py', '1.2.3.4']

        # When
        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        # Then
        assert exception_info.value.code == EXIT_CODE_ERR

        assert re.search(ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME, self.arbitrary_msg_2),
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
         Then: SystemExit is raised with code EXIT_CODE_ERR
          and: STDERR <= ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                       ez_outlet.UNHANDLED_ERROR_MESSAGE.format(
                                                                 "Traceback.*{0}.*".format(self.arbitrary_msg_2)))
          and: STDOUT is silent.
          and: Mock ez_outlet.EzOutlet.reset() was called.
        """
        args = ['ez_outlet.py', '1.2.3.4']

        # When
        with pytest.raises(SystemExit) as exception_info:
            ez_outlet.main(args)

        # Then
        assert exception_info.value.code == EXIT_CODE_ERR

        assert re.search(ez_outlet.ERROR_STRING.format(ez_outlet.PROGRAM_NAME,
                                                       ez_outlet.UNHANDLED_ERROR_MESSAGE.format(
                                                                     "Traceback.*{0}.*".format(self.arbitrary_msg_2))),
                         ez_outlet.sys.stderr.getvalue(),
                         flags=re.DOTALL) is not None

        assert ez_outlet.sys.stdout.getvalue() == ''

        mock_ez_outlet.assert_called_with(post_reset_delay=ez_outlet.EzOutlet.DEFAULT_WAIT_TIME)
