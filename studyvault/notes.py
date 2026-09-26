# notes.py
# This file handles StudyVault notes using SQLite.

from database import get_connection
from subjects import get_subjects


def choose_subject():
    """
    Show saved subjects and allow the user
    to select one.

    Returns a dictionary containing:
    - id
    - name

    Returns None if the choice is invalid.
    """

    subjects = get_subjects()

    print()
    print("CHOOSE A SUBJECT")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        print("Create a subject before creating a note.")
        return None

    for number, subject in enumerate(subjects, start=1):
        print(f'{number}. {subject["name"]}')

    choice = input("Choose a subject number: ").strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return None

    choice_number = int(choice)

    if choice_number < 1 or choice_number > len(subjects):
        print("That subject number does not exist.")
        return None

    chosen_subject = subjects[choice_number - 1]

    return {
        "id": chosen_subject["subject_id"],
        "name": chosen_subject["name"]
    }


def create_note():
    """
    Create a new note and save it permanently
    in the SQLite database.
    """

    print()
    print("CREATE NOTE")
    print("--------------------")

    subject = choose_subject()

    if subject is None:
        return

    title = input("Enter note title: ").strip()

    if title == "":
        print("Note title cannot be empty.")
        return

    content = input("Enter note content: ").strip()

    if content == "":
        print("Note content cannot be empty.")
        return

    connection = get_connection()

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
                subject["id"],
                title,
                content
            )
        )

        connection.commit()

        print()
        print(f'Note "{title}" was created successfully.')

    finally:
        connection.close()


def get_notes():
    """
    Get a short list of all notes.
    """

    connection = get_connection()

    try:
        notes = connection.execute(
            """
            SELECT
                notes.note_id,
                notes.title,
                subjects.name AS subject_name
            FROM notes
            JOIN subjects
                ON notes.subject_id = subjects.subject_id
            ORDER BY notes.note_id
            """
        ).fetchall()

        return notes

    finally:
        connection.close()


def view_notes():
    """
    Display all saved notes.
    """

    notes = get_notes()

    print()
    print("YOUR NOTES")
    print("--------------------")

    if len(notes) == 0:
        print("You do not have any notes yet.")
        return

    for note in notes:
        print(
            f'ID {note["note_id"]}: '
            f'{note["title"]} '
            f'[{note["subject_name"]}]'
        )


def find_note(note_id):
    """
    Find one note using its ID.
    """

    connection = get_connection()

    try:
        note = connection.execute(
            """
            SELECT
                notes.note_id,
                notes.subject_id,
                notes.title,
                notes.content,
                notes.created_at,
                notes.updated_at,
                subjects.name AS subject_name
            FROM notes
            JOIN subjects
                ON notes.subject_id = subjects.subject_id
            WHERE notes.note_id = ?
            """,
            (note_id,)
        ).fetchone()

        return note

    finally:
        connection.close()


def get_note_id():
    """
    Ask the user for a note ID.
    """

    note_id_text = input("Enter note ID: ").strip()

    if not note_id_text.isdigit():
        print("Please enter a valid note ID number.")
        return None

    return int(note_id_text)


def read_note():
    """
    Read one complete note.
    """

    notes = get_notes()

    if len(notes) == 0:
        print()
        print("You do not have any notes yet.")
        return

    view_notes()

    print()

    note_id = get_note_id()

    if note_id is None:
        return

    note = find_note(note_id)

    if note is None:
        print("Note not found.")
        return

    print()
    print("========================================")
    print(note["title"])
    print("========================================")
    print(f'Subject: {note["subject_name"]}')
    print()
    print(note["content"])
    print()
    print(f'Created: {note["created_at"]}')
    print(f'Updated: {note["updated_at"]}')
    print("========================================")


def edit_note():
    """
    Edit an existing note.
    """

    notes = get_notes()

    if len(notes) == 0:
        print()
        print("You do not have any notes yet.")
        return

    view_notes()

    print()

    note_id = get_note_id()

    if note_id is None:
        return

    note = find_note(note_id)

    if note is None:
        print("Note not found.")
        return

    print()
    print(f'Current title: {note["title"]}')

    new_title = input(
        "Enter a new title, or press Enter to keep the current title: "
    ).strip()

    if new_title == "":
        new_title = note["title"]

    print()
    print("Current content:")
    print(note["content"])

    new_content = input(
        "Enter new content, or press Enter to keep the current content: "
    ).strip()

    if new_content == "":
        new_content = note["content"]

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE notes
            SET
                title = ?,
                content = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE note_id = ?
            """,
            (
                new_title,
                new_content,
                note_id
            )
        )

        connection.commit()

        print()
        print("Note updated successfully.")

    finally:
        connection.close()


def delete_note():
    """
    Delete one note from the database.
    """

    notes = get_notes()

    if len(notes) == 0:
        print()
        print("You do not have any notes yet.")
        return

    view_notes()

    print()

    note_id = get_note_id()

    if note_id is None:
        return

    note = find_note(note_id)

    if note is None:
        print("Note not found.")
        return

    print()
    print(f'You are about to delete "{note["title"]}".')

    confirmation = input(
        "Type YES to delete this note: "
    ).strip().upper()

    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM notes
            WHERE note_id = ?
            """,
            (note_id,)
        )

        connection.commit()

        print("Note deleted successfully.")

    finally:
        connection.close()


def notes_menu():
    """
    Display the Notes menu.
    """

    while True:
        print()
        print("========================================")
        print("                 NOTES")
        print("========================================")
        print("1. Create Note")
        print("2. View Notes")
        print("3. Read Note")
        print("4. Edit Note")
        print("5. Delete Note")
        print("0. Back")
        print("========================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_note()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            read_note()

        elif choice == "4":
            edit_note()

        elif choice == "5":
            delete_note()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, 2, 3, 4, or 5.")