"""Check whether a newer Tintallë release is available."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import requests

import version_compare


LATEST_RELEASE_URL = (
    "https://api.github.com/repos/jramboz/tintalle/releases/latest"
)
REQUEST_TIMEOUT = 5.0
REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Tintalle-update-checker",
}


class UpdateCheckError(RuntimeError):
    """Raised when the latest release cannot be retrieved or processed."""


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    """Information about a published Tintallë release."""

    version: str
    url: str
    name: str | None = None


def _required_string(payload: dict[str, Any], key: str) -> str:
    """Return a required non-empty string from a GitHub API response."""

    value = payload.get(key)

    if not isinstance(value, str) or not value.strip():
        raise UpdateCheckError(
            f"GitHub release response is missing a valid '{key}' field."
        )

    return value.strip()


def fetch_latest_release(
    *,
    timeout: float = REQUEST_TIMEOUT,
    request_get: Callable[..., requests.Response] | None = None,
) -> ReleaseInfo:
    """Retrieve information about the latest published Tintallë release."""

    getter = request_get or requests.get

    try:
        response = getter(
            LATEST_RELEASE_URL,
            headers=REQUEST_HEADERS,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise UpdateCheckError(
            "Unable to connect to GitHub while checking for updates."
        ) from exc

    try:
        response.raise_for_status()
    except requests.RequestException as exc:
        raise UpdateCheckError(
            "GitHub returned an error while checking for updates."
        ) from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise UpdateCheckError(
            "GitHub returned an invalid JSON response."
        ) from exc

    if not isinstance(payload, dict):
        raise UpdateCheckError(
            "GitHub returned an unexpected release response."
        )

    version = _required_string(payload, "tag_name")
    url = _required_string(payload, "html_url")

    name = payload.get("name")

    if not isinstance(name, str) or not name.strip():
        name = None
    else:
        name = name.strip()

    return ReleaseInfo(
        version=version,
        url=url,
        name=name,
    )


def find_available_update(
    current_version: str,
    *,
    timeout: float = REQUEST_TIMEOUT,
    request_get: Callable[..., requests.Response] | None = None,
) -> ReleaseInfo | None:
    """Return the latest release if it is newer than current_version."""

    release = fetch_latest_release(
        timeout=timeout,
        request_get=request_get,
    )

    try:
        update_available = version_compare.is_higher(
            release.version,
            current_version,
        )
    except ValueError as exc:
        raise UpdateCheckError(
            "Unable to compare the installed and published versions."
        ) from exc

    if update_available:
        return release

    return None
