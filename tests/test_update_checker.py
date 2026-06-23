import unittest
from unittest.mock import Mock, patch

import requests

import update_checker


class UpdateCheckerTests(unittest.TestCase):
    @staticmethod
    def create_response(payload):
        response = Mock(spec=requests.Response)
        response.raise_for_status.return_value = None
        response.json.return_value = payload
        return response

    @patch("update_checker.requests.get")
    def test_fetch_latest_release(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "v0.7.0",
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/tag/v0.7.0"
                ),
                "name": "Tintallë 0.7.0",
            }
        )

        release = update_checker.fetch_latest_release()

        self.assertEqual(release.version, "v0.7.0")
        self.assertEqual(
            release.url,
            "https://github.com/jramboz/tintalle/releases/tag/v0.7.0",
        )
        self.assertEqual(release.name, "Tintallë 0.7.0")

        mock_get.assert_called_once_with(
            update_checker.LATEST_RELEASE_URL,
            headers=update_checker.REQUEST_HEADERS,
            timeout=update_checker.REQUEST_TIMEOUT,
        )

    @patch("update_checker.requests.get")
    def test_returns_newer_release(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "v0.7.0",
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/tag/v0.7.0"
                ),
            }
        )

        release = update_checker.find_available_update("0.6.1")

        self.assertIsNotNone(release)
        self.assertEqual(release.version, "v0.7.0")

    @patch("update_checker.requests.get")
    def test_same_version_returns_none(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "v0.6.1",
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/tag/v0.6.1"
                ),
            }
        )

        release = update_checker.find_available_update("0.6.1")

        self.assertIsNone(release)

    @patch("update_checker.requests.get")
    def test_older_release_returns_none(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "v0.5.5",
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/tag/v0.5.5"
                ),
            }
        )

        release = update_checker.find_available_update("0.6.1")

        self.assertIsNone(release)

    @patch("update_checker.requests.get")
    def test_connection_error_is_wrapped(self, mock_get):
        mock_get.side_effect = requests.ConnectionError(
            "Connection failed"
        )

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "Unable to connect to GitHub",
        ):
            update_checker.find_available_update("0.6.1")

    @patch("update_checker.requests.get")
    def test_http_error_is_wrapped(self, mock_get):
        response = self.create_response({})
        response.raise_for_status.side_effect = requests.HTTPError(
            "Server error"
        )
        mock_get.return_value = response

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "GitHub returned an error",
        ):
            update_checker.find_available_update("0.6.1")

    @patch("update_checker.requests.get")
    def test_invalid_json_is_rejected(self, mock_get):
        response = self.create_response({})
        response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = response

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "invalid JSON",
        ):
            update_checker.find_available_update("0.6.1")

    @patch("update_checker.requests.get")
    def test_missing_tag_name_is_rejected(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/latest"
                ),
            }
        )

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "tag_name",
        ):
            update_checker.find_available_update("0.6.1")

    @patch("update_checker.requests.get")
    def test_missing_release_url_is_rejected(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "v0.7.0",
            }
        )

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "html_url",
        ):
            update_checker.find_available_update("0.6.1")

    @patch("update_checker.requests.get")
    def test_invalid_release_version_is_rejected(self, mock_get):
        mock_get.return_value = self.create_response(
            {
                "tag_name": "latest-release",
                "html_url": (
                    "https://github.com/jramboz/tintalle/releases/latest"
                ),
            }
        )

        with self.assertRaisesRegex(
            update_checker.UpdateCheckError,
            "Unable to compare",
        ):
            update_checker.find_available_update("0.6.1")


if __name__ == "__main__":
    unittest.main()
