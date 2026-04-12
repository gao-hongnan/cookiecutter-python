"""Placeholder tests demonstrating the test infrastructure."""

import pytest
from pytest_mock import MockFixture


def test_import_package() -> None:
    """Verify the package can be imported."""
    import {{ cookiecutter.package_name }}

    assert {{ cookiecutter.package_name }} is not None


def test_with_fixture(sample_fixture: dict[str, str]) -> None:
    """Demonstrate using a fixture from conftest.py.

    Args:
        sample_fixture: Fixture from conftest.py
    """
    assert sample_fixture["key"] == "value"


@pytest.mark.unit
def test_unit_marker() -> None:
    """Demonstrate using the @pytest.mark.unit marker."""
    assert True


@pytest.mark.asyncio
async def test_async_example() -> None:
    """Demonstrate async testing with pytest-asyncio."""
    result = await async_add(1, 2)
    assert result == 3


async def async_add(a: int, b: int) -> int:
    """Simple async function for testing.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def test_with_mock(mocker: MockFixture) -> None:
    """Demonstrate using pytest-mock.

    Args:
        mocker: Pytest-mock fixture
    """
    mock_func = mocker.Mock(return_value=42)
    assert mock_func() == 42
    mock_func.assert_called_once()


@pytest.mark.parametrize(("value", "expected"), [(1, 1), (2, 4), (3, 9)])
def test_parametrized(value: int, expected: int) -> None:
    """Demonstrate parametrized tests.

    Args:
        value: Input value
        expected: Expected output
    """
    assert value * value == expected
