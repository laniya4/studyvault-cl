# search.py
# Global search system for StudyVault CL v0.7.

from database import get_connection


def search_subjects(search_term):
    """
    Search subject names.
    """

    connection = get_connection()

    try:
        results = connection.execute(
            """
            SELECT
                subject_id,
                name
            FROM subjects
            WHERE name LIKE ? COLLATE NOCASE
            ORDER BY name
            """,
            (f"%{search_term}%",)
        ).fetchall()

        return results

    finally:
        connection.close()


def search_notes(search_term):
    """
    Search note titles and note contents.
    """

    connection = get_connection()

    try:
        results = connection.execute(
            """
            SELECT
                notes.note_id,
                notes.title,
                notes.content,
                subjects.name AS subject_name
            FROM notes
            JOIN subjects
                ON notes.subject_id = subjects.subject_id
            WHERE
                notes.title LIKE ? COLLATE NOCASE
                OR notes.content LIKE ? COLLATE NOCASE
            ORDER BY notes.note_id
            """,
            (
                f"%{search_term}%",
                f"%{search_term}%"
            )
        ).fetchall()

        return results

    finally:
        connection.close()


def search_flashcards(search_term):
    """
    Search flashcard questions and answers.
    """

    connection = get_connection()

    try:
        results = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.question,
                flashcards.answer,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            WHERE
                flashcards.question LIKE ? COLLATE NOCASE
                OR flashcards.answer LIKE ? COLLATE NOCASE
            ORDER BY flashcards.flashcard_id
            """,
            (
                f"%{search_term}%",
                f"%{search_term}%"
            )
        ).fetchall()

        return results

    finally:
        connection.close()


def global_search():
    """
    Search subjects, notes, and flashcards
    using one search term.
    """

    print()
    print("========================================")
    print("              GLOBAL SEARCH")
    print("========================================")

    search_term = input(
        "Enter something to search for: "
    ).strip()

    if search_term == "":
        print("Search cannot be empty.")
        return

    subject_results = search_subjects(search_term)
    note_results = search_notes(search_term)
    flashcard_results = search_flashcards(search_term)

    total_results = (
        len(subject_results)
        + len(note_results)
        + len(flashcard_results)
    )

    print()
    print("========================================")
    print(f'SEARCH RESULTS FOR: "{search_term}"')
    print("========================================")

    if total_results == 0:
        print("No matching results were found.")
        return

    # ----------------------------------------
    # SUBJECT RESULTS
    # ----------------------------------------

    if len(subject_results) > 0:
        print()
        print("SUBJECTS")
        print("--------------------")

        for subject in subject_results:
            print(
                f'ID {subject["subject_id"]}: '
                f'{subject["name"]}'
            )

    # ----------------------------------------
    # NOTE RESULTS
    # ----------------------------------------

    if len(note_results) > 0:
        print()
        print("NOTES")
        print("--------------------")

        for note in note_results:
            print(
                f'ID {note["note_id"]}: '
                f'{note["title"]} '
                f'[{note["subject_name"]}]'
            )

            print(
                f'Preview: '
                f'{make_preview(note["content"])}'
            )

            print()

    # ----------------------------------------
    # FLASHCARD RESULTS
    # ----------------------------------------

    if len(flashcard_results) > 0:
        print()
        print("FLASHCARDS")
        print("--------------------")

        for card in flashcard_results:
            print(
                f'ID {card["flashcard_id"]}: '
                f'{card["question"]} '
                f'[{card["subject_name"]}]'
            )

            print(
                f'Answer: {card["answer"]}'
            )

            print()

    print(
        f"Total results: {total_results}"
    )


def make_preview(content, maximum_length=80):
    """
    Shorten long note content for search results.
    """

    cleaned_content = " ".join(content.split())

    if len(cleaned_content) <= maximum_length:
        return cleaned_content

    return (
        cleaned_content[:maximum_length]
        + "..."
    )


def search_notes_only():
    """
    Search only notes.
    """

    search_term = input(
        "Search notes for: "
    ).strip()

    if search_term == "":
        print("Search cannot be empty.")
        return

    results = search_notes(search_term)

    print()
    print("NOTE SEARCH RESULTS")
    print("==============================")

    if len(results) == 0:
        print("No matching notes were found.")
        return

    for note in results:
        print()
        print(
            f'ID {note["note_id"]}: '
            f'{note["title"]}'
        )
        print(
            f'Subject: {note["subject_name"]}'
        )
        print(
            f'Preview: '
            f'{make_preview(note["content"])}'
        )


def search_flashcards_only():
    """
    Search only flashcards.
    """

    search_term = input(
        "Search flashcards for: "
    ).strip()

    if search_term == "":
        print("Search cannot be empty.")
        return

    results = search_flashcards(search_term)

    print()
    print("FLASHCARD SEARCH RESULTS")
    print("==============================")

    if len(results) == 0:
        print("No matching flashcards were found.")
        return

    for card in results:
        print()
        print(
            f'ID {card["flashcard_id"]}: '
            f'{card["question"]}'
        )
        print(
            f'Subject: {card["subject_name"]}'
        )
        print(
            f'Answer: {card["answer"]}'
        )


def search_menu():
    """
    Display the StudyVault search menu.
    """

    while True:
        print()
        print("========================================")
        print("                 SEARCH")
        print("========================================")
        print("1. Global Search")
        print("2. Search Notes")
        print("3. Search Flashcards")
        print("0. Back")
        print("========================================")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            global_search()

        elif choice == "2":
            search_notes_only()

        elif choice == "3":
            search_flashcards_only()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, 2, or 3.")