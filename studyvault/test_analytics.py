# test_analytics.py
# Automated tests for StudyVault CL v0.9 analytics.

import sys
from pathlib import Path

import pytest


# Allow the tests folder to import StudyVault modules.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUDYVAULT_FOLDER = PROJECT_ROOT / "studyvault"

sys.path.insert(0, str(STUDYVAULT_FOLDER))


import database
import analytics


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """
    Create a temporary SQLite database for each test.

    This prevents automated tests from changing the
    user's real studyvault.db file.
    """

    temporary_database = tmp_path / "test_studyvault.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        temporary_database
    )

    database.initialize_database()

    return temporary_database


def test_empty_database_counts(test_database):
    """
    A new database should contain zero saved records.
    """

    assert analytics.get_count("subjects") == 0
    assert analytics.get_count("notes") == 0
    assert analytics.get_count("flashcards") == 0
    assert analytics.get_count("quiz_attempts") == 0
    assert analytics.get_count("study_sessions") == 0


def test_subject_count(test_database):
    """
    Analytics should count saved subjects correctly.
    """

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            ("Computer Science",)
        )

        connection.commit()

    finally:
        connection.close()

    assert analytics.get_count("subjects") == 1


def test_multiple_subject_count(test_database):
    """
    Analytics should count multiple subjects.
    """

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            ("Computer Science",)
        )

        connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            ("Calculus I",)
        )

        connection.commit()

    finally:
        connection.close()

    assert analytics.get_count("subjects") == 2


def test_study_session_count(test_database):
    """
    Analytics should count study sessions correctly.
    """

    connection = database.get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            ("Computer Science",)
        )

        subject_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO study_sessions (
                subject_id,
                minutes_studied,
                activity
            )
            VALUES (?, ?, ?)
            """,
            (
                subject_id,
                45,
                "Binary search practice"
            )
        )

        connection.commit()

    finally:
        connection.close()

    assert analytics.get_count("study_sessions") == 1


def test_invalid_table_name(test_database):
    """
    get_count() should reject table names
    that StudyVault does not allow.
    """

    with pytest.raises(ValueError):
        analytics.get_count("not_a_real_table")


def test_overview_output(test_database, capsys):
    """
    The Overview screen should print its main headings.
    """

    analytics.overview()

    output = capsys.readouterr().out

    assert "STUDYVAULT OVERVIEW" in output
    assert "Total Subjects: 0" in output
    assert "Total Notes: 0" in output
    assert "Total Flashcards: 0" in output
    assert "Total Quiz Attempts: 0" in output
    assert "Total Study Sessions: 0" in output