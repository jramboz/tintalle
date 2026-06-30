import platform
from pathlib import Path

from PySide6.QtCore import (
    QCoreApplication,
    QLibraryInfo,
    QLocale,
    QSettings,
    QTranslator,
)


APPLICATION_TRANSLATION_BASENAME = 'tintalle'
QT_TRANSLATION_BASENAME = 'qtbase'

SUPPORTED_APPLICATION_LOCALES = {
    'ca': 'ca_ES',
    'en': 'en_US',
    'es': 'es_ES',
}


def _get_macos_preferred_languages() -> list[str]:
    '''Return the preferred macOS user interface languages.'''
    settings = QSettings()
    languages = settings.value('AppleLanguages', [])

    if isinstance(languages, str):
        return [languages]

    if not isinstance(languages, (list, tuple)):
        return []

    return [str(language) for language in languages]

def _locale_from_language_preferences(
    languages: list[str],
) -> QLocale | None:
    '''Return the first locale supported by Tintallë.'''
    for language in languages:
        normalized_language = language.replace('-', '_')
        language_code = normalized_language.split('_', 1)[0].lower()

        locale_name = SUPPORTED_APPLICATION_LOCALES.get(language_code)

        if locale_name is not None:
            return QLocale(locale_name)

    return None

def _get_default_locale() -> QLocale:
    '''Return the locale that should be used for translations.'''
    if platform.system() == 'Darwin':
        preferred_locale = _locale_from_language_preferences(
            _get_macos_preferred_languages(),
        )

        if preferred_locale is not None:
            return preferred_locale

    return QLocale.system()

def _load_translator(
    application: QCoreApplication,
    locale: QLocale,
    basename: str,
    translations_directory: str | Path,
) -> QTranslator | None:
    '''Load and install a translation catalogue.'''
    translator = QTranslator(application)

    loaded = translator.load(
        locale,
        basename,
        '_',
        str(translations_directory),
    )

    if not loaded:
        return None

    application.installTranslator(translator)
    return translator

def install_application_translators(
    application: QCoreApplication,
    translations_directory: str | Path,
    locale: QLocale | None = None,
) -> list[QTranslator]:
    '''Install the Qt and Tintallë translation catalogues.'''
    selected_locale = locale or _get_default_locale()
    translators = []

    qt_translations_directory = QLibraryInfo.path(
        QLibraryInfo.LibraryPath.TranslationsPath
    )

    qt_translator = _load_translator(
        application,
        selected_locale,
        QT_TRANSLATION_BASENAME,
        qt_translations_directory,
    )

    if qt_translator is not None:
        translators.append(qt_translator)

    application_translator = _load_translator(
        application,
        selected_locale,
        APPLICATION_TRANSLATION_BASENAME,
        translations_directory,
    )

    if application_translator is not None:
        translators.append(application_translator)

    return translators