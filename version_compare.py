"""Utilities for comparing numeric version strings."""


def _parse_version(version: str) -> list[int]:
    """Convert a version string into a list of numeric components.

    Versions may optionally start with ``v`` or ``V``. Only numeric
    components separated by periods are supported.
    """

    normalized_version = version.strip()

    if normalized_version[:1].lower() == "v":
        normalized_version = normalized_version[1:]

    if not normalized_version:
        raise ValueError("Version cannot be empty.")

    components = normalized_version.split(".")

    if any(not component.isdigit() for component in components):
        raise ValueError(
            f"Invalid version '{version}'. "
            "Versions must contain only digits and periods."
        )

    return [int(component) for component in components]


def _process_version_strings(
    version_1: str,
    version_2: str,
) -> tuple[list[int], list[int]]:
    """Parse two versions and pad them to the same number of components."""

    components_1 = _parse_version(version_1)
    components_2 = _parse_version(version_2)

    component_count = max(len(components_1), len(components_2))

    components_1.extend(
        [0] * (component_count - len(components_1))
    )
    components_2.extend(
        [0] * (component_count - len(components_2))
    )

    return components_1, components_2


def compare_versions(version_1: str, version_2: str) -> int:
    """Compare two numeric version strings.

    Returns:
        1 if ``version_1`` is higher than ``version_2``.
        -1 if ``version_1`` is lower than ``version_2``.
        0 if both versions are equivalent.
    """

    components_1, components_2 = _process_version_strings(
        version_1,
        version_2,
    )

    return (components_1 > components_2) - (
        components_1 < components_2
    )


def is_higher(version_1: str, version_2: str) -> bool:
    """Return whether version_1 is higher than version_2."""

    return compare_versions(version_1, version_2) > 0


def is_lower(version_1: str, version_2: str) -> bool:
    """Return whether version_1 is lower than version_2."""

    return compare_versions(version_1, version_2) < 0


def is_equal(version_1: str, version_2: str) -> bool:
    """Return whether both versions are equivalent."""

    return compare_versions(version_1, version_2) == 0
