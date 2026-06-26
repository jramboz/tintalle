from pathlib import Path

from PySide6.QtCore import (
    QCoreApplication,
    QLibraryInfo,
    QLocale,
    QTranslator,
)


APPLICATION_TRANSLATION_BASENAME = 'tintalle'
QT_TRANSLATION_BASENAME = 'qtbase'


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
    selected_locale = locale or QLocale.system()
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