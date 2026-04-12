"""Pre-generation hook for cookiecutter-pyproject.

Validates user inputs before project generation begins.
"""

import re
import sys


def validate_package_name(name: str) -> bool:
    """Validate package_name is a valid Python identifier.

    Args:
        name: Package name to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name))


def validate_project_slug(slug: str) -> bool:
    """Validate project_slug is URL-safe.

    Args:
        slug: Project slug to validate

    Returns:
        True if valid, False otherwise
    """
    # URL-safe: lowercase letters, numbers, hyphens, no consecutive hyphens
    return bool(re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug))


def validate_python_version(version: str) -> bool:
    """Validate Python version is supported.

    Args:
        version: Python version string

    Returns:
        True if supported, False otherwise
    """
    supported = ["3.10", "3.11", "3.12", "3.13"]
    return version in supported


def validate_license(license_name: str) -> bool:
    """Validate license is supported.

    Args:
        license_name: License name

    Returns:
        True if supported, False otherwise
    """
    supported = ["MIT", "Apache-2.0"]
    return license_name in supported


def main() -> None:
    """Run all validations."""
    package_name = "{{ cookiecutter.package_name }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    python_version = "{{ cookiecutter.python_version }}"
    license_name = "{{ cookiecutter.license }}"

    errors = []

    if not validate_package_name(package_name):
        errors.append(
            f"ERROR: package_name '{package_name}' is not a valid Python identifier. "
            "It must start with a letter or underscore and contain only letters, "
            "numbers, and underscores (no hyphens)."
        )

    if not validate_project_slug(project_slug):
        errors.append(
            f"ERROR: project_slug '{project_slug}' is not URL-safe. "
            "It must contain only lowercase letters, numbers, and hyphens, "
            "with no consecutive hyphens."
        )

    if not validate_python_version(python_version):
        errors.append(
            f"ERROR: python_version '{python_version}' is not supported. "
            "Supported versions: 3.10, 3.11, 3.12, 3.13"
        )

    if not validate_license(license_name):
        errors.append(
            f"ERROR: license '{license_name}' is not supported. "
            "Supported licenses: MIT, Apache-2.0"
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
