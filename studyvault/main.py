# main.py
# Main program for StudyVault CL

from subjects import add_subject, view_subjects


def show_menu():
    print()
    print("========================================")
    print("             STUDYVAULT CL")
    print("========================================")
    print("1. Add Subject")
    print("2. View Subjects")
    print("0. Exit")
    print("========================================")


def main():
    program_running = True

    while program_running:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_subject()

        elif choice == "2":
            view_subjects()

        elif choice == "0":
            print()
            print("Thank you for using StudyVault CL.")
            print("Goodbye!")

            program_running = False

        else:
            print()
            print("That is not a valid option.")
            print("Please choose 0, 1, or 2.")


if __name__ == "__main__":
    main()