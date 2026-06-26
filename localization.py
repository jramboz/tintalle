from pathlib import Path

from PySide6.QtCore import QCoreApplication, QLocale, QTranslator


TRANSLATION_BASENAME = "tintalle"


def install_application_translator(
    application: QCoreApplication,
    translations_directory: str | Path,
    locale: QLocale | None = None,
) -> QTranslator | None:
    """Load and install the best available application translation.

    The system locale is used unless an explicit locale is supplied.
    English is the source language and therefore requires no translation
    catalogue.
    """
    selected_locale = locale or QLocale.system()
    translator = QTranslator(application)

    loaded = translator.load(
        selected_locale,
        TRANSLATION_BASENAME,
        "_",
        str(translations_directory),
    )

    if not loaded:
        return None

    application.installTranslator(translator)
    return translator
