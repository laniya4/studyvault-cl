# database.py
# This file manages the SQLite database for StudyVault CL.

import sqlite3
from pathlib import Path


# Find the main StudyVault project folder.
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# The database will be stored here:
# studyvault-cl/studyvault.db
DATABASE_PATH = PROJECT_FOLDER / "studyvault.db"


def get_connection():
    """
    Open a connection to the StudyVault SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # This lets us access columns by name.
    # Example:
    # row["name"]
    # instead of:
    # row[0]
    connection.row_factory = sqlite3.Row

    # Turn on foreign-key rules.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """
    Create all StudyVault database tables if they
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

        # Index for finding notes by subject faster.
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

        # Index for finding flashcards by subject faster.
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_flashcards_subject_id
            ON flashcards(subject_id)
            """
        )

        # Save all database changes.
        connection.commit()

    finally:
        # Always close the database connection.
        connection.close()