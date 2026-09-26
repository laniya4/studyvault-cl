# quizzes.py
# Quiz system for StudyVault CL.
#
# Version 0.5 uses saved flashcards as quiz questions.

import random
import string

from database import get_connection
from subjects import get_subjects


def choose_subject():
    """
    Let the user choose a subject for the quiz.

    Returns a dictionary containing:
    - id
    - name

    Returns None if the selection is invalid.
    """

    subjects = get_subjects()

    print()
    print("CHOOSE A QUIZ SUBJECT")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
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

    selected_subject = subjects[choice_number - 1]

    return {
        "id": selected_subject["subject_id"],
        "name": selected_subject["name"]
    }


def get_subject_flashcards(subject_id):
    """
    Get all flashcards belonging to one subject.
    """

    connection = get_connection()

    try:
        flashcards = connection.execute(
            """
            SELECT
                flashcard_id,
                question,
                answer
            FROM flashcards
            WHERE subject_id = ?
            ORDER BY flashcard_id
            """,
            (subject_id,)
        ).fetchall()

        return flashcards

    finally:
        connection.close()


def normalize_answer(text):
    """
    Make answer checking a little more forgiving.

    Example:

    "Binary Search!"
    and
    "binary search"

    become approximately the same text.
    """

    text = text.strip().casefold()

    # Remove punctuation.
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove extra spaces.
    text = " ".join(text.split())

    return text


def save_quiz_result(
    subject_id,
    subject_name,
    total_questions,
    correct_answers,
    percentage
):
    """
    Save a completed quiz result to SQLite.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO quiz_attempts (
                subject_id,
                subject_name,
                total_questions,
                correct_answers,
                percentage
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                subject_id,
                subject_name,
                total_questions,
                correct_answers,
                percentage
            )
        )

        connection.commit()

    finally:
        connection.close()


def start_quiz():
    """
    Start a quiz using saved flashcards.
    """

    print()
    print("START QUIZ")
    print("==============================")

    subject = choose_subject()

    if subject is None:
        return

    flashcards = get_subject_flashcards(subject["id"])

    if len(flashcards) == 0:
        print()
        print(
            f'You do not have any flashcards '
            f'for {subject["name"]}.'
        )
        print("Create flashcards before starting this quiz.")
        return

    # Make a normal Python list so it can be shuffled.
    quiz_cards = list(flashcards)

    # Randomize question order.
    random.shuffle(quiz_cards)

    total_questions = len(quiz_cards)
    correct_answers = 0

    print()
    print(f'Subject: {subject["name"]}')
    print(f'Questions: {total_questions}')
    print()
    print("Quiz starting!")
    print("==============================")

    for question_number, card in enumerate(
        quiz_cards,
        start=1
    ):
        print()
        print(
            f'Question {question_number} '
            f'of {total_questions}'
        )
        print("--------------------")
        print(card["question"])

        user_answer = input("Your answer: ").strip()

        # Do not allow a blank answer.
        while user_answer == "":
            print("Answer cannot be empty.")
            user_answer = input("Your answer: ").strip()

        expected_answer = card["answer"]

        normalized_user_answer = normalize_answer(
            user_answer
        )

        normalized_expected_answer = normalize_answer(
            expected_answer
        )

        if normalized_user_answer == normalized_expected_answer:
            print("Correct! ✅")
            correct_answers += 1

        else:
            print("Incorrect. ❌")
            print(f'Correct answer: {expected_answer}')

    percentage = (
        correct_answers / total_questions
    ) * 100

    print()
    print("========================================")
    print("              QUIZ COMPLETE")
    print("========================================")
    print(
        f'Score: {correct_answers}/{total_questions}'
    )
    print(f'Percentage: {percentage:.1f}%')

    if percentage == 100:
        print("Perfect score!")

    elif percentage >= 80:
        print("Great job!")

    elif percentage >= 60:
        print("Good effort. Keep reviewing!")

    else:
        print("Keep practicing your flashcards!")

    print("========================================")

    save_quiz_result(
        subject["id"],
        subject["name"],
        total_questions,
        correct_answers,
        percentage
    )

    print("Quiz result saved.")


def view_quiz_history():
    """
    Show previous quiz results.
    """

    connection = get_connection()

    try:
        attempts = connection.execute(
            """
            SELECT
                quiz_id,
                subject_name,
                total_questions,
                correct_answers,
                percentage,
                completed_at
            FROM quiz_attempts
            ORDER BY quiz_id DESC
            """
        ).fetchall()

    finally:
        connection.close()

    print()
    print("QUIZ HISTORY")
    print("========================================")

    if len(attempts) == 0:
        print("You have not completed any quizzes yet.")
        return

    for attempt in attempts:
        print()
        print(f'Quiz ID: {attempt["quiz_id"]}')
        print(f'Subject: {attempt["subject_name"]}')
        print(
            f'Score: '
            f'{attempt["correct_answers"]}/'
            f'{attempt["total_questions"]}'
        )
        print(
            f'Percentage: '
            f'{attempt["percentage"]:.1f}%'
        )
        print(f'Date: {attempt["completed_at"]}')
        print("--------------------")


def quiz_menu():
    """
    Display the Quiz menu.
    """

    while True:
        print()
        print("========================================")
        print("                  QUIZ")
        print("========================================")
        print("1. Start Quiz")
        print("2. View Quiz History")
        print("0. Back")
        print("========================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_quiz()

        elif choice == "2":
            view_quiz_history()

        elif choice == "0":
            return

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, or 2.")