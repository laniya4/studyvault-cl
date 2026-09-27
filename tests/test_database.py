# test_database.py
# Database tests for StudyVault CL v1.0.

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUDYVAULT_FOLDER = PROJECT_ROOT / "studyvault"

sys.path.insert(0, str(STUDYVAULT_FOLDER))


import database


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """
    Create a temporary StudyVault database.
    """

    temporary_database = (
        tmp_path / "test_studyvault.db"
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        temporary_database
    )

    database.initialize_database()

    return temporary_database


def test_database_file_created(test_database):
    """
    initialize_database() should create
    the SQLite database file.
    """

    assert test_database.exists()


def test_subjects_table_exists(test_database):
    """
    The subjects table should exist.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'subjects'
            """
        ).fetchone()

    finally:
        connection.close()

    assert result is not None


def test_notes_table_exists(test_database):
    """
    The notes table should exist.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'notes'
            """
        ).fetchone()

    finally:
        connection.close()

    assert result is not None


def test_flashcards_table_exists(test_database):
    """
    The flashcards table should exist.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'flashcards'
            """
        ).fetchone()

    finally:
        connection.close()

    assert result is not None


def test_quiz_attempts_table_exists(test_database):
    """
    The quiz_attempts table should exist.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'quiz_attempts'
            """
        ).fetchone()

    finally:
        connection.close()

    assert result is not None


def test_study_sessions_table_exists(test_database):
    """
    The study_sessions table should exist.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'study_sessions'
            """
        ).fetchone()

    finally:
        connection.close()

    assert result is not None


def test_foreign_keys_enabled(test_database):
    """
    StudyVault should enable SQLite
    foreign-key enforcement.
    """

    connection = database.get_connection()

    try:
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

    finally:
        connection.close()

    assert result[0] == 1