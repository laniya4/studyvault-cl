# test_search.py
# Search tests for StudyVault CL v1.0.

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUDYVAULT_FOLDER = PROJECT_ROOT / "studyvault"

sys.path.insert(0, str(STUDYVAULT_FOLDER))


import database
import search


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """
    Create a temporary SQLite database for each test.
    """

    temporary_database = tmp_path / "test_studyvault.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        temporary_database
    )

    database.initialize_database()

    return temporary_database


def add_test_subject(name="Computer Science"):
    """
    Add a subject to the temporary database.
    """

    connection = database.get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            (name,)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def test_search_subject(test_database):
    """
    Search should find a subject by name.
    """

    subject_id = add_test_subject()

    results = search.search_subjects("Computer")

    assert len(results) == 1
    assert results[0]["subject_id"] == subject_id
    assert results[0]["name"] == "Computer Science"


def test_subject_search_case_insensitive(test_database):
    """
    Subject search should ignore capitalization.
    """

    add_test_subject()

    results = search.search_subjects("computer")

    assert len(results) == 1
    assert results[0]["name"] == "Computer Science"


def test_partial_subject_search(test_database):
    """
    Subject search should support partial text.
    """

    add_test_subject()

    results = search.search_subjects("put")

    assert len(results) == 1
    assert results[0]["name"] == "Computer Science"


def test_search_note_title(test_database):
    """
    Search should find text in a note title.
    """

    subject_id = add_test_subject()

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO notes (
                subject_id,
                title,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                subject_id,
                "Binary Search Notes",
                "Binary search divides the search space."
            )
        )

        connection.commit()

    finally:
        connection.close()

    results = search.search_notes("Binary")

    assert len(results) == 1
    assert results[0]["title"] == "Binary Search Notes"


def test_search_note_content(test_database):
    """
    Search should find text inside note content.
    """

    subject_id = add_test_subject()

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO notes (
                subject_id,
                title,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                subject_id,
                "Algorithms",
                "A sorted search space can be divided in half."
            )
        )

        connection.commit()

    finally:
        connection.close()

    results = search.search_notes("sorted")

    assert len(results) == 1
    assert results[0]["title"] == "Algorithms"


def test_search_flashcard_question(test_database):
    """
    Search should find flashcard-question text.
    """

    subject_id = add_test_subject()

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO flashcards (
                subject_id,
                question,
                answer
            )
            VALUES (?, ?, ?)
            """,
            (
                subject_id,
                "What is binary search?",
                "An algorithm that repeatedly halves a sorted search space."
            )
        )

        connection.commit()

    finally:
        connection.close()

    results = search.search_flashcards("binary")

    assert len(results) == 1
    assert results[0]["question"] == "What is binary search?"


def test_search_flashcard_answer(test_database):
    """
    Search should find text inside an answer.
    """

    subject_id = add_test_subject()

    connection = database.get_connection()

    try:
        connection.execute(
            """
            INSERT INTO flashcards (
                subject_id,
                question,
                answer
            )
            VALUES (?, ?, ?)
            """,
            (
                subject_id,
                "What is binary search?",
                "An algorithm that repeatedly halves a sorted search space."
            )
        )

        connection.commit()

    finally:
        connection.close()

    results = search.search_flashcards("halves")

    assert len(results) == 1


def test_search_no_results(test_database):
    """
    Search should return an empty result
    when nothing matches.
    """

    add_test_subject()

    results = search.search_subjects("xyzabc123")

    assert len(results) == 0


def test_make_preview_short_text():
    """
    Short note content should remain unchanged.
    """

    content = "Short note."

    preview = search.make_preview(content)

    assert preview == "Short note."


def test_make_preview_long_text():
    """
    Long note content should be shortened.
    """

    content = "A" * 100

    preview = search.make_preview(
        content,
        maximum_length=20
    )

    assert preview == ("A" * 20) + "..."