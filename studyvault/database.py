# database.py
# This file manages the SQLite database for StudyVault CL.

import sqlite3
from pathlib import Path


# Main project folder
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# Database location:
# studyvault-cl/studyvault.db
DATABASE_PATH = PROJECT_FOLDER / "studyvault.db"


def get_connection():
    """
    Open a connection to the StudyVault database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Lets us use:
    # row["name"]
    # instead of:
    # row[0]
    connection.row_factory = sqlite3.Row

    # Turn on foreign-key support.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """
    Create all StudyVault tables if they
    do not already exist.
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