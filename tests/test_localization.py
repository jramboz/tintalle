import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from PySide6.QtCore import QLocale

import localization


class LocalizationTests(unittest.TestCase):

    @patch("localization.QTranslator")
    def test_installs_translation_when_catalogue_is_available(
        self,
        mock_translator_class,
    ):
        application = Mock()
        translator = mock_translator_class.return_value
        translator.load.return_value = True

        locale = QLocale("es_ES")
        translations_directory = Path("translations")

        result = localization.install_application_translator(
            application,
            translations_directory,
            locale=locale,
        )

        mock_translator_class.assert_called_once_with(application)

        load_arguments = translator.load.call_args.args
        self.assertEqual(load_arguments[0].name(), "es_ES")
        self.assertEqual(load_arguments[1], "tintalle")
        self.assertEqual(load_arguments[2], "_")
        self.assertEqual(
            load_arguments[3],
            str(translations_directory),
        )

        application.installTranslator.assert_called_once_with(translator)
        self.assertIs(result, translator)

    @patch("localization.QTranslator")
    def test_does_not_install_translation_when_catalogue_is_unavailable(
        self,
        mock_translator_class,
    ):
        application = Mock()
        translator = mock_translator_class.return_value
        translator.load.return_value = False

        result = localization.install_application_translator(
            application,
            "translations",
            locale=QLocale("fr_FR"),
        )

        application.installTranslator.assert_not_called()
        self.assertIsNone(result)

    @patch("localization.QLocale.system")
    @patch("localization.QTranslator")
    def test_uses_system_locale_when_locale_is_not_provided(
        self,
        mock_translator_class,
        mock_system_locale,
    ):
        application = Mock()
        translator = mock_translator_class.return_value
        translator.load.return_value = False

        mock_system_locale.return_value = QLocale("ca_ES")

        localization.install_application_translator(
            application,
            "translations",
        )

        mock_system_locale.assert_called_once_with()

        load_arguments = translator.load.call_args.args
        self.assertEqual(load_arguments[0].name(), "ca_ES")


if __name__ == "__main__":
    unittest.main()
