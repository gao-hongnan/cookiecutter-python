{% if cookiecutter.use_database %}"""Tests for {{ cookiecutter.project_name }} database session management.

The session helpers are pure lifecycle plumbing (commit on success, roll back on
error, always close), so they are exercised against a mocked session factory
rather than a live database.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockFixture

from {{ cookiecutter.package_name }} import db


def mock_session(mocker: MockFixture) -> AsyncMock:
    """Replace the module-level session factory with a mock.

    Parameters
    ----------
    mocker : MockFixture
        Pytest-mock fixture.

    Returns
    -------
    AsyncMock
        The session that the patched factory hands out.
    """
    session = mocker.AsyncMock()
    session_maker = mocker.MagicMock()
    session_maker.return_value.__aenter__.return_value = session
    mocker.patch.object(db, "async_session_maker", session_maker)
    return session


async def test_init_db_creates_tables(mocker: MockFixture) -> None:
    """`init_db` runs metadata creation inside a transaction."""
    conn = mocker.AsyncMock()
    engine = mocker.MagicMock()
    engine.begin.return_value.__aenter__.return_value = conn
    mocker.patch.object(db, "engine", engine)

    await db.init_db()

    conn.run_sync.assert_awaited_once()


async def test_get_session_commits_on_success(mocker: MockFixture) -> None:
    """`get_session` commits and closes when the caller succeeds."""
    session = mock_session(mocker)

    yielded = [got async for got in db.get_session()]

    assert yielded == [session]
    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()
    session.close.assert_awaited_once()


async def test_get_session_rolls_back_on_error(mocker: MockFixture) -> None:
    """`get_session` rolls back and re-raises when the caller fails."""
    session = mock_session(mocker)
    generator = db.get_session()
    await anext(generator)

    with pytest.raises(RuntimeError, match="boom"):
        await generator.athrow(RuntimeError("boom"))

    session.commit.assert_not_awaited()
    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()


async def test_get_db_context_commits_on_success(mocker: MockFixture) -> None:
    """`get_db_context` commits and closes when the block succeeds."""
    session = mock_session(mocker)

    async with db.get_db_context() as got:
        assert got is session

    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()
    session.close.assert_awaited_once()


async def test_get_db_context_rolls_back_on_error(mocker: MockFixture) -> None:
    """`get_db_context` rolls back and re-raises when the block fails."""
    session = mock_session(mocker)

    async def failing_block() -> None:
        async with db.get_db_context():
            raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        await failing_block()

    session.commit.assert_not_awaited()
    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()
{%- endif %}
