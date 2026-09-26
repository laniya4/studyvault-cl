# flashcards.py
# This file handles StudyVault flashcards using SQLite.

from database import get_connection
from subjects import get_subjects


def choose_subject():
    """
    Let the user choose one saved subject.
    """

    subjects = get_subjects()

    print()
    print("CHOOSE A SUBJECT")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        print("Create a subject before creating a flashcard.")
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


def create_flashcard():
    """
    Create a flashcard and save it to SQLite.
    """

    print()
    print("CREATE FLASHCARD")
    print("--------------------")

    subject = choose_subject()

    if subject is None:
        return

    question = input("Enter flashcard question: ").strip()

    if question == "":
        print("Flashcard question cannot be empty.")
        return

    answer = input("Enter flashcard answer: ").strip()

    if answer == "":
        print("Flashcard answer cannot be empty.")
        return

    connection = get_connection()

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
                subject["id"],
                question,
                answer
            )
        )

        connection.commit()

        print()
        print("Flashcard created successfully.")

    finally:
        connection.close()


def get_flashcards():
    """
    Get all saved flashcards.
    """

    connection = get_connection()

    try:
        flashcards = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.question,
                flashcards.answer,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            ORDER BY flashcards.flashcard_id
            """
        ).fetchall()

        return flashcards

    finally:
        connection.close()


def view_flashcards():
    """
    Display all saved flashcards.
    """

    flashcards = get_flashcards()

    print()
    print("YOUR FLASHCARDS")
    print("--------------------")

    if len(flashcards) == 0:
        print("You do not have any flashcards yet.")
        return

    for card in flashcards:
        print(
            f'ID {card["flashcard_id"]}: '
            f'{card["question"]} '
            f'[{card["subject_name"]}]'
        )


def find_flashcard(flashcard_id):
    """
    Find one flashcard by ID.
    """

    connection = get_connection()

    try:
        flashcard = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.subject_id,
                flashcards.question,
                flashcards.answer,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            WHERE flashcards.flashcard_id = ?
            """,
            (flashcard_id,)
        ).fetchone()

        return flashcard

    finally:
        connection.close()


def get_flashcard_id():
    """
    Ask the user for a flashcard ID.
    """

    flashcard_id_text = input("Enter flashcard ID: ").strip()

    if not flashcard_id_text.isdigit():
        print("Please enter a valid flashcard ID number.")
        return None

    return int(flashcard_id_text)


def study_flashcards():
    """
    Study every flashcard one at a time.
    """

    flashcards = get_flashcards()

    if len(flashcards) == 0:
        print()
        print("You do not have any flashcards yet.")
        return

    print()
    print("STUDY FLASHCARDS")
    print("==============================")

    for card in flashcards:
        print()
        print(f'Subject: {card["subject_name"]}')
        print(f'Question: {card["question"]}')

        input("Press Enter to reveal the answer...")

        print(f'Answer: {card["answer"]}')

        input("Press Enter for the next card...")

    print()
    print("You finished this flashcard study session.")


def edit_flashcard():
    """
    Edit an existing flashcard.
    """

    flashcards = get_flashcards()

    if len(flashcards) == 0:
        print()
        print("You do not have any flashcards yet.")
        return

    view_flashcards()

    print()

    flashcard_id = get_flashcard_id()

    if flashcard_id is None:
        return

    card = find_flashcard(flashcard_id)

    if card is None:
        print("Flashcard not found.")
        return

    print()
    print(f'Current question: {card["question"]}')

    new_question = input(
        "Enter a new question, or press Enter to keep the current question: "
    ).strip()

    if new_question == "":
        new_question = card["question"]

    print()
    print(f'Current answer: {card["answer"]}')

    new_answer = input(
        "Enter a new answer, or press Enter to keep the current answer: "
    ).strip()

    if new_answer == "":
        new_answer = card["answer"]

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE flashcards
            SET
                question = ?,
                answer = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE flashcard_id = ?
            """,
            (
                new_question,
                new_answer,
                flashcard_id
            )
        )

        connection.commit()

        print()
        print("Flashcard updated successfully.")

    finally:
        connection.close()


def delete_flashcard():
    """
    Delete one flashcard.
    """

    flashcards = get_flashcards()

    if len(flashcards) == 0:
        print()
        print("You do not have any flashcards yet.")
        return

    view_flashcards()

    print()

    flashcard_id = get_flashcard_id()

    if flashcard_id is None:
        return

    card = find_flashcard(flashcard_id)

    if card is None:
        print("Flashcard not found.")
        return

    print()
    print(f'You are about to delete "{card["question"]}".')

    confirmation = input(
        "Type YES to delete this flashcard: "
    ).strip().upper()

    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM flashcards
            WHERE flashcard_id = ?
            """,
            (flashcard_id,)
        )

        connection.commit()

        print("Flashcard deleted successfully.")

    finally:
        connection.close()


def flashcards_menu():
    """
    Display the Flashcards menu.
    """

    while True:
        print()
        print("========================================")
        print("              FLASHCARDS")
        print("========================================")
        print("1. Create Flashcard")
        print("2. View Flashcards")
        print("3. Study Flashcards")
        print("4. Edit Flashcard")
        print("5. Delete Flashcard")
        print("0. Back")
        print("========================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_flashcard()

        elif choice == "2":
            view_flashcards()

        elif choice == "3":
            study_flashcards()

        elif choice == "4":
            edit_flashcard()

        elif choice == "5":
            delete_flashcard()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, 2, 3, 4, or 5.")