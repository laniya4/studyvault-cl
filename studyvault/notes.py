# notes.py
# This file handles StudyVault notes.

from subjects import subjects


# This list temporarily stores all notes.
notes = []


# Every note gets its own ID number.
next_note_id = 1


def choose_subject():
    """
    Show the user's subjects and let them choose one.

    Returns the chosen subject name.
    Returns None if the choice is invalid.
    """

    print()
    print("CHOOSE A SUBJECT")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        print("Create a subject before creating a note.")
        return None

    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}")

    choice = input("Choose a subject number: ").strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return None

    choice_number = int(choice)

    if choice_number < 1 or choice_number > len(subjects):
        print("That subject number does not exist.")
        return None

    return subjects[choice_number - 1]


def create_note():
    """
    Create a new note and attach it to a subject.
    """

    global next_note_id

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

    note = {
        "id": next_note_id,
        "subject": subject,
        "title": title,
        "content": content
    }

    notes.append(note)

    print()
    print(f'Note "{title}" was created successfully.')

    next_note_id += 1


def view_notes():
    """
    Display a short list of every saved note.
    """

    print()
    print("YOUR NOTES")
    print("--------------------")

    if len(notes) == 0:
        print("You do not have any notes yet.")
        return

    for note in notes:
        print(
            f'ID {note["id"]}: '
            f'{note["title"]} '
            f'[{note["subject"]}]'
        )


def find_note(note_id):
    """
    Search for one note using its ID.

    Returns the note if found.
    Returns None if not found.
    """

    for note in notes:
        if note["id"] == note_id:
            return note

    return None


def get_note_id():
    """
    Ask the user for a note ID and make sure
    they entered a whole number.
    """

    note_id_text = input("Enter note ID: ").strip()

    if not note_id_text.isdigit():
        print("Please enter a valid note ID number.")
        return None

    return int(note_id_text)


def read_note():
    """
    Display the complete contents of one note.
    """

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
    print(f'Subject: {note["subject"]}')
    print()
    print(note["content"])
    print("========================================")


def edit_note():
    """
    Change the title or content of an existing note.
    """

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

    if new_title != "":
        note["title"] = new_title

    print()
    print("Current content:")
    print(note["content"])

    new_content = input(
        "Enter new content, or press Enter to keep the current content: "
    ).strip()

    if new_content != "":
        note["content"] = new_content

    print()
    print("Note updated successfully.")


def delete_note():
    """
    Permanently remove one note from the current session.
    """

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

    notes.remove(note)

    print("Note deleted successfully.")


def notes_menu():
    """
    Display the Notes menu until the user chooses Back.
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
            