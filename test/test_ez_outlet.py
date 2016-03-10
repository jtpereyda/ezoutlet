# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import unittest
import requests

import pytest

import ezoutlet.exceptions

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

sample_url = 'DEAD STRINGS TELL NO TALES'

PROXY_SETTINGS_NONE = {"http": None, "https": None}


# Suppress since PyCharm doesn't recognize @mock.patch.object
# noinspection PyUnresolvedReferences
@mock.patch.object(ez_outlet, '_get_url', return_value=sample_url)
@mock.patch('ezoutlet.ez_outlet.requests')
@mock.patch('ezoutlet.ez_outlet.time')
class TestEzOutlet(unittest.TestCase):
    """
    EzOutlet.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """
    expected_response_contents = ez_outlet.EzOutlet.EXPECTED_RESPONSE_CONTENTS

    def setup_method(self, _):
        self.hostname = '12.34.56.78'
        self.post_reset_delay = 12.34
        self.ez_outlet_reset_interval = 3.21
        self.timeout = 11.12
        self.uut = ez_outlet.EzOutlet(hostname=self.hostname,
                                      timeout=self.timeout)

    def configure_mock_requests(self, mock_requests):
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': self.expected_response_contents})})

    def test_reset_get(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: ez_outlet._get_url is called using the IP address with ez_outlet.RESET_URL_PATH.
         and: requests.get(ez_outlet._get_url's result, timeout, proxies=PROXY_SETTINGS_NONE) is called.
        """
        _ = mock_time

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        self.uut.reset(post_reset_delay=self.post_reset_delay,
                       ez_outlet_reset_interval=self.ez_outlet_reset_interval)

        # Then
        mock_get_url.assert_called_with(self.hostname, ez_outlet.EzOutlet.RESET_URL_PATH)
        mock_requests.get.assert_called_once_with(sample_url, timeout=self.timeout, proxies=PROXY_SETTINGS_NONE)

    def test_reset_result(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: expected_response_contents is returned.
        """
        _ = mock_time
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        result = self.uut.reset(post_reset_delay=self.post_reset_delay,
                                ez_outlet_reset_interval=self.ez_outlet_reset_interval)

        # Then
        self.assertEqual(self.expected_response_contents, result)

    def test_reset_sleep(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: time.sleep(post_reset_delay + ez_outlet_reset_interval) is called.
        """
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        self.uut.reset(post_reset_delay=self.post_reset_delay,
                       ez_outlet_reset_interval=self.ez_outlet_reset_interval)

        # Then
        mock_time.sleep.assert_called_once_with(self.post_reset_delay + self.ez_outlet_reset_interval)


# Suppress since PyCharm doesn't recognize @mock.patch.object
# noinspection PyUnresolvedReferences
@mock.patch.object(ez_outlet, '_get_url', return_value=sample_url)
@mock.patch('ezoutlet.ez_outlet.requests')
@mock.patch('ezoutlet.ez_outlet.time')
class TestEzOutletNoResponse(unittest.TestCase):
    """
    EzOutlet.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """

    def setup_method(self, _):
        self.hostname = '12.34.56.78'
        self.post_reset_delay = 12.34
        self.ez_outlet_reset_interval = 3.21
        self.timeout = 11.12
        self.uut = ez_outlet.EzOutlet(hostname=self.hostname,
                                      timeout=self.timeout)

    def configure_mock_requests(self, mock_requests):
        mock_requests.configure_mock(**{'get.side_effect': requests.exceptions.ConnectTimeout("Dummy reason")})
        mock_requests.exceptions = requests.exceptions  # Restore mocked-away exceptions

    def test_reset_no_response_get(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests configured to raise requests.exceptions.ConnectTimeout on get.
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: ez_outlet._get_url is called using the IP address with ez_outlet.RESET_URL_PATH.
         and: requests.get(ez_outlet._get_url's result, timeout, proxies=PROXY_SETTINGS_NONE) is called.
        """
        _ = mock_time

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        try:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)
        except ezoutlet.exceptions.EzOutletError:
            pass  # exception tested elsewhere

        # Then
        mock_get_url.assert_called_with(self.hostname, ez_outlet.EzOutlet.RESET_URL_PATH)
        mock_requests.get.assert_called_once_with(sample_url, timeout=self.timeout, proxies=PROXY_SETTINGS_NONE)

    def test_reset_no_response_raise(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests configured to raise requests.exceptions.ConnectTimeout on get.
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: reset() raises ez_outlet.EzOutletError, e.
         and: str(e) == ez_outlet.EzOutlet.NO_RESPONSE_MSG.format(timeout).
        """
        _ = mock_time
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        with self.assertRaises(ezoutlet.exceptions.EzOutletError) as e:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)

        # Then
        self.assertEqual(str(e.exception),
                         ez_outlet.EzOutlet.NO_RESPONSE_MSG.format(self.timeout))

    def test_reset_no_response_no_sleep(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests configured to raise requests.exceptions.ConnectTimeout on get.
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: time.sleep(post_reset_delay + ez_outlet_reset_interval) is _not_ called.
        """
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        try:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)
        except ezoutlet.exceptions.EzOutletError:
            pass  # exception tested elsewhere

        # Then
        mock_time.sleep.assert_not_called()


# Suppress since PyCharm doesn't recognize @mock.patch.object
# noinspection PyUnresolvedReferences
@mock.patch.object(ez_outlet, '_get_url', return_value=sample_url)
@mock.patch('ezoutlet.ez_outlet.requests')
@mock.patch('ezoutlet.ez_outlet.time')
class TestEzOutletUnexpectedResponse(unittest.TestCase):
    """
    EzOutlet.post_fail is basically all side-effects, so its test is
    rather heavy in mocks.
    """

    def setup_method(self, _):
        self.unexpected_response_contents = '1,0'

        self.hostname = '12.34.56.78'
        self.post_reset_delay = 12.34
        self.ez_outlet_reset_interval = 3.21
        self.timeout = 11.12
        self.uut = ez_outlet.EzOutlet(hostname=self.hostname,
                                      timeout=self.timeout)

    def configure_mock_requests(self, mock_requests):
        mock_requests.configure_mock(
                **{'get.return_value': mock.MagicMock(
                        **{'text': self.unexpected_response_contents})})

    def test_reset_unexpected_response_get(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module configured to give unexpected_response_contents
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: ez_outlet._get_url is called using the IP address with ez_outlet.RESET_URL_PATH.
         and: requests.get(ez_outlet._get_url's result, timeout, proxies=PROXY_SETTINGS_NONE) is called.
        """
        _ = mock_time

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        try:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)
        except ezoutlet.exceptions.EzOutletError:
            pass  # exception tested elsewhere

        # Then
        mock_get_url.assert_called_with(self.hostname, ez_outlet.EzOutlet.RESET_URL_PATH)
        mock_requests.get.assert_called_once_with(sample_url, timeout=self.timeout, proxies=PROXY_SETTINGS_NONE)

    def test_reset_unexpected_response_raises(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module configured to give unexpected_response_contents
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: reset() raises ez_outlet.EzOutletError, e.
         and: str(e) == ez_outlet.EzOutlet.UNEXPECTED_RESPONSE_MSG.format(unexpected_response_contents).
        """
        _ = mock_time
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        with self.assertRaises(ezoutlet.exceptions.EzOutletError) as e:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)

        # Then
        self.assertEqual(str(e.exception),
                         ez_outlet.EzOutlet.UNEXPECTED_RESPONSE_MSG.format(
                                 self.unexpected_response_contents))

    def test_reset_unexpected_response_no_sleep(self, mock_time, mock_requests, mock_get_url):
        """
        Given: Mock requests module configured to give unexpected_response_contents
          and: EzOutlet initialized with an IP address and timeout.
        When: Calling reset(post_reset_delay, ez_outlet_reset_interval).
        Then: time.sleep(post_reset_delay + ez_outlet_reset_interval) is _not_ called.
        """
        _ = mock_get_url

        # Given
        self.configure_mock_requests(mock_requests=mock_requests)

        # When
        try:
            self.uut.reset(post_reset_delay=self.post_reset_delay,
                           ez_outlet_reset_interval=self.ez_outlet_reset_interval)
        except ezoutlet.exceptions.EzOutletError:
            pass  # exception tested elsewhere

        # Then
        mock_time.sleep.assert_not_called()


@pytest.mark.parametrize("hostname,expected_url", [('1.2.3.4', 'http://1.2.3.4/reset.cgi')])
def test_url(hostname, expected_url):
    """
    Given: A hostname.
    When: Creating an EzOutlet using hostname.
    Then: Property `url` returns the expected URL.

    Args:
        hostname: test parameter
        expected_url: test parameter
    """
    uut = ez_outlet.EzOutlet(hostname=hostname)

    assert expected_url == uut.url
