# main.py
# Main program for StudyVault CL

from database import initialize_database
from subjects import add_subject, view_subjects
from notes import notes_menu
from flashcards import flashcards_menu
from quizzes import quiz_menu
from spaced_repetition import spaced_repetition_menu


def show_menu():
    print()
    print("========================================")
    print("             STUDYVAULT CL")
    print("========================================")
    print("1. Add Subject")
    print("2. View Subjects")
    print("3. Notes")
    print("4. Flashcards")
    print("5. Quiz")
    print("6. Spaced Repetition")
    print("0. Exit")
    print("========================================")


def main():
    initialize_database()

    program_running = True

    while program_running:
        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            add_subject()

        elif choice == "2":
            view_subjects()

        elif choice == "3":
            notes_menu()

        elif choice == "4":
            flashcards_menu()

        elif choice == "5":
            quiz_menu()

        elif choice == "6":
            spaced_repetition_menu()

        elif choice == "0":
            print()
            print(
                "Thank you for using StudyVault CL."
            )
            print(
                "Your information has been saved."
            )
            print("Goodbye!")

            program_running = False

        else:
            print()
            print("That is not a valid option.")
            print(
                "Please choose "
                "0, 1, 2, 3, 4, 5, or 6."
            )


if __name__ == "__main__":
    main()