# study_tracking.py
# Study-session tracking for StudyVault CL v0.8.

from database import get_connection
from subjects import get_subjects


def choose_subject():
    """
    Let the user select a saved subject.
    """

    subjects = get_subjects()

    print()
    print("CHOOSE A SUBJECT")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        print("Create a subject before logging study time.")
        return None

    for number, subject in enumerate(subjects, start=1):
        print(
            f'{number}. {subject["name"]}'
        )

    choice = input(
        "Choose a subject number: "
    ).strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return None

    choice_number = int(choice)

    if (
        choice_number < 1
        or choice_number > len(subjects)
    ):
        print("That subject number does not exist.")
        return None

    subject = subjects[choice_number - 1]

    return {
        "id": subject["subject_id"],
        "name": subject["name"]
    }


def log_study_session():
    """
    Record a completed study session.
    """

    print()
    print("========================================")
    print("            LOG STUDY SESSION")
    print("========================================")

    subject = choose_subject()

    if subject is None:
        return

    minutes_text = input(
        "How many minutes did you study? "
    ).strip()

    if not minutes_text.isdigit():
        print("Study time must be a whole number.")
        return

    minutes = int(minutes_text)

    if minutes <= 0:
        print("Study time must be greater than zero.")
        return

    activity = input(
        "What did you study? "
        "(Press Enter to skip): "
    ).strip()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO study_sessions (
                subject_id,
                minutes_studied,
                activity
            )
            VALUES (?, ?, ?)
            """,
            (
                subject["id"],
                minutes,
                activity
            )
        )

        connection.commit()

    finally:
        connection.close()

    print()
    print("Study session saved successfully.")
    print(
        f'Subject: {subject["name"]}'
    )
    print(
        f'Time studied: {minutes} minute(s)'
    )

    if activity != "":
        print(
            f'Activity: {activity}'
        )


def view_study_history():
    """
    Display all saved study sessions.
    """

    connection = get_connection()

    try:
        sessions = connection.execute(
            """
            SELECT
                study_sessions.session_id,
                study_sessions.minutes_studied,
                study_sessions.activity,
                study_sessions.studied_at,
                subjects.name AS subject_name
            FROM study_sessions
            JOIN subjects
                ON study_sessions.subject_id
                = subjects.subject_id
            ORDER BY
                study_sessions.session_id DESC
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("========================================")
    print("             STUDY HISTORY")
    print("========================================")

    if len(sessions) == 0:
        print(
            "You have not logged any study sessions yet."
        )
        return

    for session in sessions:
        print()
        print(
            f'Session ID: {session["session_id"]}'
        )
        print(
            f'Subject: {session["subject_name"]}'
        )
        print(
            f'Time: '
            f'{session["minutes_studied"]} minute(s)'
        )

        if (
            session["activity"] is not None
            and session["activity"] != ""
        ):
            print(
                f'Activity: {session["activity"]}'
            )

        print(
            f'Date: {session["studied_at"]}'
        )
        print("--------------------")


def view_study_totals():
    """
    Display total study time overall and
    grouped by subject.
    """

    connection = get_connection()

    try:

        overall = connection.execute(
            """
            SELECT
                COUNT(*) AS total_sessions,
                COALESCE(
                    SUM(minutes_studied),
                    0
                ) AS total_minutes
            FROM study_sessions
            """
        ).fetchone()

        subject_totals = connection.execute(
            """
            SELECT
                subjects.name AS subject_name,
                COUNT(
                    study_sessions.session_id
                ) AS total_sessions,
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
    print("              STUDY TOTALS")
    print("========================================")

    if overall["total_sessions"] == 0:
        print(
            "You have not logged any study sessions yet."
        )
        return

    total_minutes = overall["total_minutes"]

    hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    print(
        f'Total sessions: '
        f'{overall["total_sessions"]}'
    )

    print(
        f'Total study time: '
        f'{total_minutes} minute(s)'
    )

    print(
        f'Total time: '
        f'{hours} hour(s) '
        f'{remaining_minutes} minute(s)'
    )

    print()
    print("BY SUBJECT")
    print("--------------------")

    for subject in subject_totals:

        subject_minutes = subject["total_minutes"]

        subject_hours = subject_minutes // 60
        subject_remaining = subject_minutes % 60

        print()
        print(
            f'{subject["subject_name"]}'
        )
        print(
            f'Sessions: '
            f'{subject["total_sessions"]}'
        )
        print(
            f'Minutes: {subject_minutes}'
        )
        print(
            f'Time: '
            f'{subject_hours} hour(s) '
            f'{subject_remaining} minute(s)'
        )


def study_tracking_menu():
    """
    Display the Study Tracking menu.
    """

    while True:
        print()
        print("========================================")
        print("            STUDY TRACKING")
        print("========================================")
        print("1. Log Study Session")
        print("2. View Study History")
        print("3. View Study Totals")
        print("0. Back")
        print("========================================")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            log_study_session()

        elif choice == "2":
            view_study_history()

        elif choice == "3":
            view_study_totals()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print(
                "Please choose 0, 1, 2, or 3."
            )