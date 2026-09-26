# subjects.py
# This file handles StudyVault subjects.

subjects = []


def add_subject():
    print()
    print("ADD SUBJECT")
    print("--------------------")

    subject_name = input("Enter subject name: ").strip()

    if subject_name == "":
        print("Subject name cannot be empty.")
        return

    for subject in subjects:
        if subject.lower() == subject_name.lower():
            print("That subject already exists.")
            return

    subjects.append(subject_name)

    print(f'"{subject_name}" was added to StudyVault.')


def view_subjects():
    print()
    print("YOUR SUBJECTS")
    print("--------------------")

    if len(subjects) == 0:
        print("You do not have any subjects yet.")
        return

    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}")