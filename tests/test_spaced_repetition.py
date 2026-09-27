# test_spaced_repetition.py
# Spaced-repetition tests for StudyVault CL v1.0.

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUDYVAULT_FOLDER = PROJECT_ROOT / "studyvault"

sys.path.insert(0, str(STUDYVAULT_FOLDER))


import database
import spaced_repetition


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


def create_flashcard(
    question="What is binary search?",
    answer="An algorithm that repeatedly halves a sorted search space.",
    interval_days=0,
    next_review=None
):
    """
    Create a subject and flashcard in the temporary database.
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

        cursor = connection.execute(
            """
            INSERT INTO flashcards (
                subject_id,
                question,
                answer,
                interval_days,
                next_review
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                subject_id,
                question,
                answer,
                interval_days,
                next_review
            )
        )

        flashcard_id = cursor.lastrowid

        connection.commit()

        card = connection.execute(
            """
            SELECT *
            FROM flashcards
            WHERE flashcard_id = ?
            """,
            (flashcard_id,)
        ).fetchone()

        return card

    finally:
        connection.close()


def test_again_interval_is_one_day():
    """
    Rating 1 (Again) should reset the interval to 1 day.
    """

    assert spaced_repetition.calculate_interval("1", 0) == 1
    assert spaced_repetition.calculate_interval("1", 10) == 1


def test_hard_first_interval_is_two_days():
    """
    Rating 2 (Hard) should start at 2 days.
    """

    result = spaced_repetition.calculate_interval("2", 0)

    assert result == 2


def test_hard_increases_existing_interval():
    """
    Hard should increase an existing interval by about 1.2x.
    """

    result = spaced_repetition.calculate_interval("2", 10)

    assert result == 12


def test_good_first_interval_is_three_days():
    """
    Rating 3 (Good) should start at 3 days.
    """

    result = spaced_repetition.calculate_interval("3", 0)

    assert result == 3


def test_good_doubles_existing_interval():
    """
    Good should approximately double an existing interval.
    """

    result = spaced_repetition.calculate_interval("3", 5)

    assert result == 10


def test_easy_first_interval_is_seven_days():
    """
    Rating 4 (Easy) should begin with a 7-day interval.
    """

    result = spaced_repetition.calculate_interval("4", 0)

    assert result == 7


def test_new_flashcard_is_due(test_database):
    """
    A new flashcard with no next-review date should be due.
    """

    create_flashcard()

    cards = spaced_repetition.get_due_flashcards()

    assert len(cards) == 1
    assert cards[0]["question"] == "What is binary search?"


def test_future_flashcard_is_not_due(test_database):
    """
    A flashcard scheduled in the future should not be due today.
    """

    future_date = (
        date.today() + timedelta(days=7)
    ).isoformat()

    create_flashcard(
        next_review=future_date
    )

    cards = spaced_repetition.get_due_flashcards()

    assert len(cards) == 0


def test_save_good_review(test_database):
    """
    Saving a Good review should update review statistics
    and schedule the card three days later.
    """

    card = create_flashcard()

    new_interval, next_review_date = (
        spaced_repetition.save_review(
            card,
            "3"
        )
    )

    assert new_interval == 3
    assert next_review_date == (
        date.today() + timedelta(days=3)
    )

    connection = database.get_connection()

    try:
        saved_card = connection.execute(
            """
            SELECT *
            FROM flashcards
            WHERE flashcard_id = ?
            """,
            (card["flashcard_id"],)
        ).fetchone()

    finally:
        connection.close()

    assert saved_card["review_count"] == 1
    assert saved_card["correct_count"] == 1
    assert saved_card["incorrect_count"] == 0
    assert saved_card["interval_days"] == 3
    assert saved_card["last_reviewed"] == date.today().isoformat()
    assert saved_card["next_review"] == (
        date.today() + timedelta(days=3)
    ).isoformat()


def test_save_again_review(test_database):
    """
    Saving an Again review should count as forgotten
    and schedule the card one day later.
    """

    card = create_flashcard(
        interval_days=10
    )

    new_interval, next_review_date = (
        spaced_repetition.save_review(
            card,
            "1"
        )
    )

    assert new_interval == 1
    assert next_review_date == (
        date.today() + timedelta(days=1)
    )

    connection = database.get_connection()

    try:
        saved_card = connection.execute(
            """
            SELECT *
            FROM flashcards
            WHERE flashcard_id = ?
            """,
            (card["flashcard_id"],)
        ).fetchone()

    finally:
        connection.close()

    assert saved_card["review_count"] == 1
    assert saved_card["correct_count"] == 0
    assert saved_card["incorrect_count"] == 1
    assert saved_card["interval_days"] == 1


def test_reviewed_card_is_not_immediately_due(test_database):
    """
    Once a card is reviewed successfully,
    it should not immediately appear as due again.
    """

    card = create_flashcard()

    spaced_repetition.save_review(
        card,
        "3"
    )

    cards = spaced_repetition.get_due_flashcards()

    assert len(cards) == 0