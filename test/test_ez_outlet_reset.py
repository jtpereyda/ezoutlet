# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import unittest
import urllib2

import pytest

try:
    import unittest.mock as mock
except ImportError:
    # mock is required as an extras_require:
    # noinspection PyPackageRequirements
    import mock

from ezoutlet import ez_outlet_reset

EXIT_CODE_ERR = 1
EXIT_CODE_PARSER_ERR = 2
EZ_OUTLET_RESET_DEFAULT_WAIT_TIME = ez_outlet_reset.EzOutletReset.DEFAULT_WAIT_TIME


class TestEzOutletReset(unittest.TestCase):
    """
    EzOutletReset.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """
    sample_url = 'DEAD STRINGS TELL NO TALES'
    expected_response_contents = ez_outlet_reset.EzOutletReset.EXPECTED_RESPONSE_CONTENTS

    def setup_method(self, _):
        self.hostname = '12.34.56.78'
        self.wait_time = 12.34
        self.reset_delay = 3.21
        self.timeout = 11.12
        self.uut = ez_outlet_reset.EzOutletReset(hostname=self.hostname,
                                                 wait_time=self.wait_time,
                                                 timeout=self.timeout,
                                                 reset_delay=self.reset_delay)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch.object(ez_outlet_reset, '_get_url', return_value=sample_url)
    @mock.patch('ezoutlet.ez_outlet_reset.urllib2')
    @mock.patch('ezoutlet.ez_outlet_reset.time')
    def test_reset_get(self, mock_time, mock_urllib2, mock_get_url):
        """
        Given: Mock urllib2 configured such that
               urlopen returns a mock whose read() method returns expected_response_contents.
          and: EzOutletReset initialized with an IP address, wait_time, timeout, and reset_delay.
        When: Calling reset().
        Then: ez_outlet_reset._get_url is called using the IP address with ez_outlet_reset.RESET_URL_PATH.
         and: urllib2.urlopen(ez_outlet_reset._get_url's result, timeout) is called.
        """
        # Given
        mock_urllib2.configure_mock(
                **{'urlopen.return_value': mock.MagicMock(
                        **{'read.return_value': self.expected_response_contents})})

        # When
        self.uut.reset()

        # Then
        mock_get_url.assert_called_with(self.hostname, ez_outlet_reset.EzOutletReset.RESET_URL_PATH)
        mock_urllib2.urlopen.assert_called_once_with(self.sample_url, timeout=self.timeout)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch.object(ez_outlet_reset, '_get_url', return_value=sample_url)
    @mock.patch('ezoutlet.ez_outlet_reset.urllib2')
    @mock.patch('ezoutlet.ez_outlet_reset.time')
    def test_reset_result(self, mock_time, mock_urllib2, mock_get_url):
        """
        Given: Mock urllib2 configured such that
               urlopen returns a mock whose read() method returns expected_response_contents.
          and: EzOutletReset initialized with an IP address, wait_time, timeout, and reset_delay.
        When: Calling reset().
        Then: expected_response_contents is returned.
        """
        # Given
        mock_urllib2.configure_mock(
                **{'urlopen.return_value': mock.MagicMock(
                        **{'read.return_value': self.expected_response_contents})})

        # When
        result = self.uut.reset()

        # Then
        self.assertEqual(self.expected_response_contents, result)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch.object(ez_outlet_reset, '_get_url', return_value=sample_url)
    @mock.patch('ezoutlet.ez_outlet_reset.urllib2')
    @mock.patch('ezoutlet.ez_outlet_reset.time')
    def test_reset_sleep(self, mock_time, mock_urllib2, mock_get_url):
        """
        Given: Mock urllib2 configured such that
               urlopen returns a mock whose read() method returns expected_response_contents.
          and: EzOutletReset initialized with an IP address, wait_time, timeout, and reset_delay.
        When: Calling reset().
        Then: time.sleep(wait_time + reset_delay) is called.
        """
        # Given
        mock_urllib2.configure_mock(
                **{'urlopen.return_value': mock.MagicMock(
                        **{'read.return_value': self.expected_response_contents})})

        # When
        self.uut.reset()

        # Then
        mock_time.sleep.assert_called_once_with(self.wait_time + self.reset_delay)


class TestEzOutletResetExceptions(unittest.TestCase):
    """
    EzOutletReset.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """

    arbitrary_msg_1 = 'arbitrary message'
    arbitrary_msg_2 = '"Always check a module in cleaner than when you checked it out." --Uncle Bob'

    sample_url = 'DEAD STRINGS TELL NO TALES'
    expected_response_contents = ez_outlet_reset.EzOutletReset.EXPECTED_RESPONSE_CONTENTS
    unexpected_response_contents = '1,0'

    def setup_method(self, _):
        self.hostname = '12.34.56.78'
        self.wait_time = 12.34
        self.reset_delay = 3.21
        self.timeout = 11.12
        self.uut = ez_outlet_reset.EzOutletReset(hostname=self.hostname,
                                                 wait_time=self.wait_time,
                                                 timeout=self.timeout,
                                                 reset_delay=self.reset_delay)

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch.object(ez_outlet_reset, '_get_url', return_value=sample_url)
    @mock.patch('ezoutlet.ez_outlet_reset.urllib2')
    @mock.patch('ezoutlet.ez_outlet_reset.time')
    def test_reset_no_response(self, mock_time, mock_urllib2, mock_get_url):
        """
        Given: Mock urllib2 configured to raise urllib2.URLError on urlopen.
          and: EzOutletReset initialized with an IP address, wait_time, timeout, and reset_delay.
        When: Calling reset().
        Then: reset() raises ez_outlet_reset.EzOutletResetError, e.
         and: e.message == ez_outlet_reset.EzOutletReset.NO_RESPONSE_MSG.format(timeout).
         and: ez_outlet_reset._get_url is called using the IP address with ez_outlet_reset.RESET_URL_PATH.
         and: urllib2.urlopen(ez_outlet_reset._get_url's result, timeout) is called.
         and: time.sleep(wait_time + reset_delay) is _not_ called.
        """
        # Given
        mock_urllib2.configure_mock(**{'urlopen.side_effect': urllib2.URLError("Dummy reason")})
        mock_urllib2.URLError = urllib2.URLError  # Restore mocked-away URLError

        # When
        with self.assertRaises(ez_outlet_reset.EzOutletResetError) as e:
            self.uut.reset()

        # Then
        self.assertEqual(e.exception.message,
                         ez_outlet_reset.EzOutletReset.NO_RESPONSE_MSG.format(self.timeout))
        mock_get_url.assert_called_with(self.hostname, ez_outlet_reset.EzOutletReset.RESET_URL_PATH)
        mock_urllib2.urlopen.assert_called_once_with(self.sample_url, timeout=self.timeout)
        mock_time.sleep.assert_not_called()

    # Suppress since PyCharm doesn't recognize @mock.patch.object
    # noinspection PyUnresolvedReferences
    @mock.patch.object(ez_outlet_reset, '_get_url', return_value=sample_url)
    @mock.patch('ezoutlet.ez_outlet_reset.urllib2')
    @mock.patch('ezoutlet.ez_outlet_reset.time')
    def test_reset_unexpected_response(self, mock_time, mock_urllib2, mock_get_url):
        """
        Given: Mock urllib2 configured such that
               urlopen returns a mock whose read() method returns unexpected_response_contents.
          and: EzOutletReset initialized with an IP address, wait_time, timeout, and reset_delay.
        When: Calling reset().
        Then: reset() raises ez_outlet_reset.EzOutletResetError, e.
         and: e.message == ez_outlet_reset.EzOutletReset.UNEXPECTED_RESPONSE_MSG.format(unexpected_response_contents).
         and: ez_outlet_reset._get_url is called using the IP address with ez_outlet_reset.RESET_URL_PATH.
         and: urllib2.urlopen(ez_outlet_reset._get_url's result, timeout) is called.
         and: time.sleep(wait_time + reset_delay) is _not_ called.
        """
        # Given
        mock_urllib2.configure_mock(
                **{'urlopen.return_value': mock.MagicMock(
                        **{'read.return_value': self.unexpected_response_contents})})

        # When
        with self.assertRaises(ez_outlet_reset.EzOutletResetError) as e:
            self.uut.reset()

        # Then
        self.assertEqual(e.exception.message,
                         ez_outlet_reset.EzOutletReset.UNEXPECTED_RESPONSE_MSG.format(
                                 self.unexpected_response_contents))
        mock_get_url.assert_called_with(self.hostname, ez_outlet_reset.EzOutletReset.RESET_URL_PATH)
        mock_urllib2.urlopen.assert_called_once_with(self.sample_url, timeout=self.timeout)
        mock_time.sleep.assert_not_called()


@pytest.mark.parametrize("hostname,expected_url", [('1.2.3.4', 'http://1.2.3.4/reset.cgi')])
def test_url(hostname, expected_url):
    """
    Given: A hostname.
    When: Creating an EzOutletReset using hostname.
    Then: Property `url` returns the expected URL.

    Args:
        hostname: test parameter
        expected_url: test parameter
    """
    uut = ez_outlet_reset.EzOutletReset(hostname=hostname)

    assert expected_url == uut.url
