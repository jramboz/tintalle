import unittest

import version_compare


class VersionCompareTests(unittest.TestCase):
    def test_higher_version(self):
        self.assertTrue(
            version_compare.is_higher("0.7.0", "0.6.1")
        )
        self.assertTrue(
            version_compare.is_higher("2.0", "1.10")
        )

    def test_lower_version(self):
        self.assertTrue(
            version_compare.is_lower("0.6.1", "0.7.0")
        )
        self.assertTrue(
            version_compare.is_lower("1.10", "2.0")
        )

    def test_equal_versions(self):
        self.assertTrue(
            version_compare.is_equal("0.6.1", "0.6.1")
        )

    def test_missing_components_are_zero(self):
        self.assertTrue(
            version_compare.is_equal("1", "1.0.0")
        )
        self.assertTrue(
            version_compare.is_equal("1.2", "1.2.0")
        )

    def test_leading_v_is_accepted(self):
        self.assertTrue(
            version_compare.is_equal("v0.6.1", "0.6.1")
        )
        self.assertTrue(
            version_compare.is_higher("v0.7.0", "0.6.1")
        )

    def test_whitespace_is_ignored(self):
        self.assertTrue(
            version_compare.is_equal(" 0.6.1 ", "0.6.1")
        )

    def test_invalid_versions_raise_value_error(self):
        invalid_versions = (
            "",
            "v",
            "1.",
            "1..0",
            "1.0-beta",
            "version-1.0",
        )

        for invalid_version in invalid_versions:
            with self.subTest(version=invalid_version):
                with self.assertRaises(ValueError):
                    version_compare.is_higher(
                        invalid_version,
                        "1.0",
                    )


if __name__ == "__main__":
    unittest.main()
