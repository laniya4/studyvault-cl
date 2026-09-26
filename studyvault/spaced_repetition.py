# spaced_repetition.py
# Spaced repetition system for StudyVault CL v0.6.

from datetime import date, timedelta

from database import get_connection


def get_due_flashcards():
    """
    Get flashcards that are ready to review.

    A card is due when:
    - it has never been reviewed, or
    - its next review date is today or earlier.
    """

    today = date.today().isoformat()

    connection = get_connection()

    try:
        cards = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.question,
                flashcards.answer,
                flashcards.review_count,
                flashcards.correct_count,
                flashcards.incorrect_count,
                flashcards.interval_days,
                flashcards.last_reviewed,
                flashcards.next_review,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            WHERE
                flashcards.next_review IS NULL
                OR flashcards.next_review <= ?
            ORDER BY flashcards.flashcard_id
            """,
            (today,)
        ).fetchall()

        return cards

    finally:
        connection.close()


def calculate_interval(rating, old_interval):
    """
    Calculate how many days until the card
    should be reviewed again.

    1 = Again
    2 = Hard
    3 = Good
    4 = Easy
    """

    if rating == "1":
        return 1

    elif rating == "2":
        if old_interval < 2:
            return 2

        return max(2, round(old_interval * 1.2))

    elif rating == "3":
        if old_interval == 0:
            return 3

        return max(3, round(old_interval * 2))

    elif rating == "4":
        if old_interval == 0:
            return 7

        return max(7, round(old_interval * 3))

    return 1


def save_review(card, rating):
    """
    Save the result of one flashcard review.
    """

    today = date.today()

    old_interval = card["interval_days"] or 0

    new_interval = calculate_interval(
        rating,
        old_interval
    )

    next_review_date = (
        today + timedelta(days=new_interval)
    )

    review_count = card["review_count"] + 1

    correct_count = card["correct_count"]
    incorrect_count = card["incorrect_count"]

    if rating == "1":
        incorrect_count += 1

    else:
        correct_count += 1

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE flashcards
            SET
                review_count = ?,
                correct_count = ?,
                incorrect_count = ?,
                interval_days = ?,
                last_reviewed = ?,
                next_review = ?
            WHERE flashcard_id = ?
            """,
            (
                review_count,
                correct_count,
                incorrect_count,
                new_interval,
                today.isoformat(),
                next_review_date.isoformat(),
                card["flashcard_id"]
            )
        )

        connection.commit()

    finally:
        connection.close()

    return new_interval, next_review_date


def review_due_flashcards():
    """
    Review all flashcards currently due.
    """

    cards = get_due_flashcards()

    print()
    print("========================================")
    print("          DUE FLASHCARD REVIEW")
    print("========================================")

    if len(cards) == 0:
        print("You do not have any flashcards due today.")
        return

    print(f"Cards due: {len(cards)}")

    for number, card in enumerate(cards, start=1):
        print()
        print(
            f'Card {number} of {len(cards)}'
        )
        print(
            f'Subject: {card["subject_name"]}'
        )
        print("--------------------")
        print(card["question"])

        input(
            "Press Enter to reveal the answer..."
        )

        print()
        print(f'Answer: {card["answer"]}')

        print()
        print("How well did you remember it?")
        print("1. Again - I forgot it")
        print("2. Hard  - I barely remembered")
        print("3. Good  - I remembered")
        print("4. Easy  - I knew it immediately")

        while True:
            rating = input(
                "Choose 1, 2, 3, or 4: "
            ).strip()

            if rating in ("1", "2", "3", "4"):
                break

            print(
                "Please choose 1, 2, 3, or 4."
            )

        interval, next_review_date = save_review(
            card,
            rating
        )

        print()
        print(
            f"Next review in {interval} day(s)."
        )
        print(
            f"Next review date: "
            f"{next_review_date.isoformat()}"
        )

    print()
    print("Review session complete.")


def view_review_schedule():
    """
    Show every flashcard and its next review date.
    """

    connection = get_connection()

    try:
        cards = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.question,
                flashcards.next_review,
                flashcards.interval_days,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            ORDER BY
                CASE
                    WHEN flashcards.next_review IS NULL
                    THEN 0
                    ELSE 1
                END,
                flashcards.next_review,
                flashcards.flashcard_id
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("========================================")
    print("            REVIEW SCHEDULE")
    print("========================================")

    if len(cards) == 0:
        print("You do not have any flashcards yet.")
        return

    for card in cards:
        print()
        print(
            f'ID {card["flashcard_id"]}: '
            f'{card["question"]}'
        )
        print(
            f'Subject: {card["subject_name"]}'
        )

        if card["next_review"] is None:
            print("Next review: Due now")
        else:
            print(
                f'Next review: '
                f'{card["next_review"]}'
            )

        print(
            f'Current interval: '
            f'{card["interval_days"]} day(s)'
        )

        print("--------------------")


def view_flashcard_progress():
    """
    Show spaced-repetition statistics.
    """

    connection = get_connection()

    try:
        cards = connection.execute(
            """
            SELECT
                flashcards.flashcard_id,
                flashcards.question,
                flashcards.review_count,
                flashcards.correct_count,
                flashcards.incorrect_count,
                flashcards.interval_days,
                flashcards.last_reviewed,
                flashcards.next_review,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id = subjects.subject_id
            ORDER BY flashcards.flashcard_id
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("========================================")
    print("          FLASHCARD PROGRESS")
    print("========================================")

    if len(cards) == 0:
        print("You do not have any flashcards yet.")
        return

    for card in cards:
        review_count = card["review_count"]

        if review_count == 0:
            accuracy = 0.0
        else:
            accuracy = (
                card["correct_count"]
                / review_count
            ) * 100

        print()
        print(
            f'ID {card["flashcard_id"]}: '
            f'{card["question"]}'
        )
        print(
            f'Subject: {card["subject_name"]}'
        )
        print(
            f'Reviews: {card["review_count"]}'
        )
        print(
            f'Remembered: '
            f'{card["correct_count"]}'
        )
        print(
            f'Forgotten: '
            f'{card["incorrect_count"]}'
        )
        print(
            f'Accuracy: {accuracy:.1f}%'
        )
        print(
            f'Interval: '
            f'{card["interval_days"]} day(s)'
        )

        if card["last_reviewed"] is None:
            print("Last reviewed: Never")
        else:
            print(
                f'Last reviewed: '
                f'{card["last_reviewed"]}'
            )

        if card["next_review"] is None:
            print("Next review: Due now")
        else:
            print(
                f'Next review: '
                f'{card["next_review"]}'
            )

        print("--------------------")


def spaced_repetition_menu():
    """
    Display the spaced repetition menu.
    """

    while True:
        print()
        print("========================================")
        print("          SPACED REPETITION")
        print("========================================")
        print("1. Review Due Flashcards")
        print("2. View Review Schedule")
        print("3. View Flashcard Progress")
        print("0. Back")
        print("========================================")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            review_due_flashcards()

        elif choice == "2":
            view_review_schedule()

        elif choice == "3":
            view_flashcard_progress()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, 2, or 3.")