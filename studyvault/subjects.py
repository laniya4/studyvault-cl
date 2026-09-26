# subjects.py
# This file handles StudyVault subjects using SQLite.

from database import get_connection


def get_subjects():
    """
    Get all subjects from the database.

    Returns a list of database rows.
    """

    connection = get_connection()

    try:
        subjects = connection.execute(
            """
            SELECT subject_id, name
            FROM subjects
            ORDER BY name COLLATE NOCASE
            """
        ).fetchall()

        return subjects

    finally:
        connection.close()


def add_subject():
    """
    Add a new subject to the SQLite database.
    """

    print()
    print("ADD SUBJECT")
    print("--------------------")

    subject_name = input("Enter subject name: ").strip()

    if subject_name == "":
        print("Subject name cannot be empty.")
        return

    connection = get_connection()

    try:
        existing_subject = connection.execute(
            """
            SELECT subject_id
            FROM subjects
            WHERE name = ? COLLATE NOCASE
            """,
            (subject_name,)
        ).fetchone()

        if existing_subject is not None:
            print("That subject already exists.")
            return

        connection.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?)
            """,
            (subject_name,)
        )

        connection.commit()

        print(f'"{subject_name}" was added to StudyVault.')

    finally:
        connection.close()


def view_subjects():
    """
    Display all saved subjects.
    """

    subjects = get_subjects()

    print()
    print("YOUR SUBJECTS")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        return

    for number, subject in enumerate(subjects, start=1):
        print(f'{number}. {subject["name"]}')