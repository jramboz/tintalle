import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

from PySide6.QtCore import QLocale

import localization


class LocalizationTests(unittest.TestCase):

    @patch(
        'localization.QLibraryInfo.path',
        return_value='/qt/translations',
    )
    @patch('localization.QTranslator')
    def test_installs_qt_and_application_translations(
        self,
        mock_translator_class,
        mock_library_path,
    ):
        application = Mock()

        qt_translator = Mock()
        application_translator = Mock()

        qt_translator.load.return_value = True
        application_translator.load.return_value = True

        mock_translator_class.side_effect = [
            qt_translator,
            application_translator,
        ]

        result = localization.install_application_translators(
            application,
            Path('translations'),
            locale=QLocale('es_ES'),
        )

        mock_library_path.assert_called_once_with(
            localization.QLibraryInfo.LibraryPath.TranslationsPath
        )

        qt_arguments = qt_translator.load.call_args.args
        self.assertEqual(qt_arguments[0].name(), 'es_ES')
        self.assertEqual(qt_arguments[1], 'qtbase')
        self.assertEqual(qt_arguments[2], '_')
        self.assertEqual(qt_arguments[3], '/qt/translations')

        application_arguments = (
            application_translator.load.call_args.args
        )
        self.assertEqual(application_arguments[0].name(), 'es_ES')
        self.assertEqual(application_arguments[1], 'tintalle')
        self.assertEqual(application_arguments[2], '_')
        self.assertEqual(
            application_arguments[3],
            'translations',
        )

        application.installTranslator.assert_has_calls(
            [
                call(qt_translator),
                call(application_translator),
            ]
        )

        self.assertEqual(
            result,
            [qt_translator, application_translator],
        )

    @patch(
        'localization.QLibraryInfo.path',
        return_value='/qt/translations',
    )
    @patch('localization.QTranslator')
    def test_ignores_unavailable_translation_catalogues(
        self,
        mock_translator_class,
        mock_library_path,
    ):
        application = Mock()

        qt_translator = Mock()
        application_translator = Mock()

        qt_translator.load.return_value = False
        application_translator.load.return_value = False

        mock_translator_class.side_effect = [
            qt_translator,
            application_translator,
        ]

        result = localization.install_application_translators(
            application,
            'translations',
            locale=QLocale('fr_FR'),
        )

        application.installTranslator.assert_not_called()
        self.assertEqual(result, [])

    @patch('localization.QLocale.system')
    @patch(
        'localization.QLibraryInfo.path',
        return_value='/qt/translations',
    )
    @patch('localization.QTranslator')
    def test_uses_system_locale_when_none_is_provided(
        self,
        mock_translator_class,
        mock_library_path,
        mock_system_locale,
    ):
        application = Mock()

        qt_translator = Mock()
        application_translator = Mock()

        qt_translator.load.return_value = False
        application_translator.load.return_value = False

        mock_translator_class.side_effect = [
            qt_translator,
            application_translator,
        ]

        mock_system_locale.return_value = QLocale('ca_ES')

        localization.install_application_translators(
            application,
            'translations',
        )

        mock_system_locale.assert_called_once_with()

        qt_arguments = qt_translator.load.call_args.args
        application_arguments = (
            application_translator.load.call_args.args
        )

        self.assertEqual(qt_arguments[0].name(), 'ca_ES')
        self.assertEqual(
            application_arguments[0].name(),
            'ca_ES',
        )


if __name__ == '__main__':
    unittest.main()