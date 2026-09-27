# analytics.py
# Analytics system for StudyVault CL v0.9.

from datetime import date

from database import get_connection


def get_count(table_name):
    """
    Return the number of rows in a StudyVault table.
    """

    allowed_tables = {
        "subjects",
        "notes",
        "flashcards",
        "quiz_attempts",
        "study_sessions",
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    connection = get_connection()

    try:
        result = connection.execute(
            f"SELECT COUNT(*) AS total FROM {table_name}"
        ).fetchone()

        return result["total"]

    finally:
        connection.close()


def overview():
    """
    Display a high-level overview of StudyVault.
    """

    subject_count = get_count("subjects")
    note_count = get_count("notes")
    flashcard_count = get_count("flashcards")
    quiz_count = get_count("quiz_attempts")
    study_session_count = get_count("study_sessions")

    connection = get_connection()

    try:
        study_result = connection.execute(
            """
            SELECT
                COALESCE(SUM(minutes_studied), 0) AS total_minutes
            FROM study_sessions
            """
        ).fetchone()

    finally:
        connection.close()

    total_minutes = study_result["total_minutes"]

    hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    print()
    print("========================================")
    print("           STUDYVAULT OVERVIEW")
    print("========================================")
    print(f"Total Subjects: {subject_count}")
    print(f"Total Notes: {note_count}")
    print(f"Total Flashcards: {flashcard_count}")
    print(f"Total Quiz Attempts: {quiz_count}")
    print(f"Total Study Sessions: {study_session_count}")
    print(f"Total Study Minutes: {total_minutes}")
    print(
        f"Total Study Time: "
        f"{hours} hour(s) {remaining_minutes} minute(s)"
    )


def study_analytics():
    """
    Display analytics about saved study sessions.
    """

    connection = get_connection()

    try:
        totals = connection.execute(
            """
            SELECT
                COUNT(*) AS session_count,
                COALESCE(SUM(minutes_studied), 0) AS total_minutes,
                COALESCE(AVG(minutes_studied), 0) AS average_minutes
            FROM study_sessions
            """
        ).fetchone()

        most_studied = connection.execute(
            """
            SELECT
                subjects.name AS subject_name,
                SUM(
                    study_sessions.minutes_studied
                ) AS total_minutes
            FROM study_sessions
            JOIN subjects
                ON study_sessions.subject_id
                = subjects.subject_id
            GROUP BY
                study_sessions.subject_id,
                subjects.name
            ORDER BY total_minutes DESC
            LIMIT 1
            """
        ).fetchone()

        subject_totals = connection.execute(
            """
            SELECT
                subjects.name AS subject_name,
                COUNT(
                    study_sessions.session_id
                ) AS session_count,
                SUM(
                    study_sessions.minutes_studied
                ) AS total_minutes
            FROM study_sessions
            JOIN subjects
                ON study_sessions.subject_id
                = subjects.subject_id
            GROUP BY
                study_sessions.subject_id,
                subjects.name
            ORDER BY total_minutes DESC
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("========================================")
    print("             STUDY ANALYTICS")
    print("========================================")

    if totals["session_count"] == 0:
        print("No study sessions have been logged yet.")
        return

    total_minutes = totals["total_minutes"]

    hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    print(f'Total Sessions: {totals["session_count"]}')
    print(f"Total Minutes: {total_minutes}")
    print(
        f"Total Time: "
        f"{hours} hour(s) {remaining_minutes} minute(s)"
    )
    print(
        f'Average Session: '
        f'{totals["average_minutes"]:.1f} minute(s)'
    )

    if most_studied is not None:
        print()
        print("MOST STUDIED SUBJECT")
        print("--------------------")
        print(
            f'{most_studied["subject_name"]}: '
            f'{most_studied["total_minutes"]} minute(s)'
        )

    print()
    print("BY SUBJECT")
    print("--------------------")

    for subject in subject_totals:
        print()
        print(subject["subject_name"])
        print(
            f'Sessions: {subject["session_count"]}'
        )
        print(
            f'Minutes: {subject["total_minutes"]}'
        )


def quiz_analytics():
    """
    Display analytics for completed quizzes.
    """

    connection = get_connection()

    try:
        quiz_data = connection.execute(
            """
            SELECT
                COUNT(*) AS attempt_count,
                COALESCE(AVG(percentage), 0) AS average_score,
                COALESCE(MAX(percentage), 0) AS highest_score,
                COALESCE(MIN(percentage), 0) AS lowest_score
            FROM quiz_attempts
            """
        ).fetchone()

        subject_results = connection.execute(
            """
            SELECT
                subject_name,
                COUNT(*) AS attempt_count,
                AVG(percentage) AS average_score
            FROM quiz_attempts
            GROUP BY subject_name
            ORDER BY average_score DESC
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("========================================")
    print("              QUIZ ANALYTICS")
    print("========================================")

    if quiz_data["attempt_count"] == 0:
        print("No quizzes have been completed yet.")
        return

    print(
        f'Total Attempts: '
        f'{quiz_data["attempt_count"]}'
    )
    print(
        f'Average Score: '
        f'{quiz_data["average_score"]:.1f}%'
    )
    print(
        f'Highest Score: '
        f'{quiz_data["highest_score"]:.1f}%'
    )
    print(
        f'Lowest Score: '
        f'{quiz_data["lowest_score"]:.1f}%'
    )

    print()
    print("BY SUBJECT")
    print("--------------------")

    for subject in subject_results:
        print()
        print(subject["subject_name"])
        print(
            f'Attempts: {subject["attempt_count"]}'
        )
        print(
            f'Average: '
            f'{subject["average_score"]:.1f}%'
        )


def flashcard_analytics():
    """
    Display spaced-repetition and flashcard analytics.
    """

    today = date.today().isoformat()

    connection = get_connection()

    try:
        totals = connection.execute(
            """
            SELECT
                COUNT(*) AS flashcard_count,
                COALESCE(SUM(review_count), 0)
                    AS total_reviews,
                COALESCE(SUM(correct_count), 0)
                    AS remembered,
                COALESCE(SUM(incorrect_count), 0)
                    AS forgotten
            FROM flashcards
            """
        ).fetchone()

        due_result = connection.execute(
            """
            SELECT COUNT(*) AS due_count
            FROM flashcards
            WHERE
                next_review IS NULL
                OR next_review <= ?
            """,
            (today,)
        ).fetchone()

        most_reviewed = connection.execute(
            """
            SELECT
                flashcards.question,
                flashcards.review_count,
                subjects.name AS subject_name
            FROM flashcards
            JOIN subjects
                ON flashcards.subject_id
                = subjects.subject_id
            ORDER BY
                flashcards.review_count DESC,
                flashcards.flashcard_id
            LIMIT 1
            """
        ).fetchone()

    finally:
        connection.close()

    print()
    print("========================================")
    print("           FLASHCARD ANALYTICS")
    print("========================================")

    if totals["flashcard_count"] == 0:
        print("You do not have any flashcards yet.")
        return

    total_reviews = totals["total_reviews"]
    remembered = totals["remembered"]
    forgotten = totals["forgotten"]

    if total_reviews == 0:
        accuracy = 0.0
    else:
        accuracy = (
            remembered / total_reviews
        ) * 100

    print(
        f'Total Flashcards: '
        f'{totals["flashcard_count"]}'
    )
    print(f"Total Reviews: {total_reviews}")
    print(f"Remembered: {remembered}")
    print(f"Forgotten: {forgotten}")
    print(f"Overall Accuracy: {accuracy:.1f}%")
    print(
        f'Cards Due Today: '
        f'{due_result["due_count"]}'
    )

    if most_reviewed is not None:
        print()
        print("MOST REVIEWED FLASHCARD")
        print("--------------------")
        print(most_reviewed["question"])
        print(
            f'Subject: '
            f'{most_reviewed["subject_name"]}'
        )
        print(
            f'Reviews: '
            f'{most_reviewed["review_count"]}'
        )


def analytics_menu():
    """
    Display the StudyVault analytics menu.
    """

    while True:
        print()
        print("========================================")
        print("               ANALYTICS")
        print("========================================")
        print("1. Overview")
        print("2. Study Analytics")
        print("3. Quiz Analytics")
        print("4. Flashcard Analytics")
        print("0. Back")
        print("========================================")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            overview()

        elif choice == "2":
            study_analytics()

        elif choice == "3":
            quiz_analytics()

        elif choice == "4":
            flashcard_analytics()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print(
                "Please choose 0, 1, 2, 3, or 4."
            )