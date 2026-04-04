"""Smoke test to verify the test infrastructure works."""


def test_import_package() -> None:
    """Verify the package can be imported."""
    import {{ cookiecutter.package_name }}

    assert {{ cookiecutter.package_name }} is not None
