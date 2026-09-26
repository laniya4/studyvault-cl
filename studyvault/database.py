# database.py
# This file manages the SQLite database for StudyVault CL.

import sqlite3
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_FOLDER / "studyvault.db"


def get_connection():
    """
    Open a connection to the StudyVault SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def column_exists(connection, table_name, column_name):
    """
    Check whether a column already exists in a SQLite table.
    """

    columns = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    for column in columns:
        if column["name"] == column_name:
            return True

    return False


def initialize_database():
    """
    Create all StudyVault database tables and
    add newer columns when needed.
    """

    connection = get_connection()

    try:
        # ----------------------------------------
        # SUBJECTS TABLE
        # ----------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # ----------------------------------------
        # NOTES TABLE
        # ----------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(subject_id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_notes_subject_id
            ON notes(subject_id)
            """
        )

        # ----------------------------------------
        # FLASHCARDS TABLE
        # ----------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS flashcards (
                flashcard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(subject_id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_flashcards_subject_id
            ON flashcards(subject_id)
            """
        )

        # ----------------------------------------
        # v0.6 SPACED REPETITION COLUMNS
        # ----------------------------------------

        if not column_exists(
            connection,
            "flashcards",
            "review_count"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN review_count INTEGER NOT NULL DEFAULT 0
                """
            )

        if not column_exists(
            connection,
            "flashcards",
            "correct_count"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN correct_count INTEGER NOT NULL DEFAULT 0
                """
            )

        if not column_exists(
            connection,
            "flashcards",
            "incorrect_count"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN incorrect_count INTEGER NOT NULL DEFAULT 0
                """
            )

        if not column_exists(
            connection,
            "flashcards",
            "interval_days"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN interval_days INTEGER NOT NULL DEFAULT 0
                """
            )

        if not column_exists(
            connection,
            "flashcards",
            "last_reviewed"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN last_reviewed TEXT
                """
            )

        if not column_exists(
            connection,
            "flashcards",
            "next_review"
        ):
            connection.execute(
                """
                ALTER TABLE flashcards
                ADD COLUMN next_review TEXT
                """
            )

        # ----------------------------------------
        # QUIZ HISTORY TABLE
        # ----------------------------------------

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                subject_name TEXT NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                percentage REAL NOT NULL,
                completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(subject_id)
                    ON DELETE SET NULL
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_quiz_subject_id
            ON quiz_attempts(subject_id)
            """
        )

        connection.commit()

    finally:
        connection.close()