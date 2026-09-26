# StudyVault CL

StudyVault CL is a beginner-friendly command-line study management application built with Python.

The goal of StudyVault is to create one place where students can organize subjects, notes, flashcards, quizzes, study sessions, goals, and learning progress directly from the command line.

## Current Version

**Version 0.3**

StudyVault currently supports:

- Adding subjects
- Viewing subjects
- Preventing duplicate subject names
- Rejecting empty subject names
- Creating notes
- Connecting notes to subjects
- Viewing notes
- Reading complete notes
- Editing notes
- Deleting notes
- Rejecting empty note titles and content
- Validating subject numbers and note IDs
- Confirming note deletion
- Handling invalid menu choices
- Exiting the application safely

## Version 0.3 — Notes System

Version 0.3 introduces a complete Notes system.

Users can:

- Create a note
- Assign a note to a subject
- View all notes
- Read an individual note
- Edit an existing note
- Delete a note
- Cancel a deletion
- Use unique note IDs

The Notes system demonstrates the four basic CRUD operations:

- **Create** — create a new note
- **Read** — view or read notes
- **Update** — edit an existing note
- **Delete** — remove a note

Currently, subjects and notes are stored temporarily in memory. They disappear when StudyVault closes.

Persistent storage will be introduced in Version 0.3 using SQLite.

## Planned Features

Future versions of StudyVault CL will include:

- Persistent SQLite database storage
- Flashcards
- Spaced repetition
- Quiz mode
- Study-session tracking
- Study goals
- Global search
- Progress analytics
- Study streaks
- CSV data export
- Automated testing

## Technologies

StudyVault CL currently uses:

- Python
- Git
- GitHub
- VS Code

Planned technologies include:

- SQLite
- pytest
- GitHub Actions

## Project Structure

```text
studyvault-cl/
├── README.md
├── .gitignore
├── pseudocode/
│   └── studyvault_cl.pseudo
└── studyvault/
    ├── __init__.py
    ├── main.py
    ├── subjects.py
    └── notes.py
```

## Running StudyVault

Make sure Python 3 is installed.

From the main project directory, run:

```bash
python3 studyvault/main.py
```

The main menu will display:

```text
========================================
             STUDYVAULT CL
========================================
1. Add Subject
2. View Subjects
3. Notes
0. Exit
========================================
```

The Notes menu includes:

```text
========================================
                 NOTES
========================================
1. Create Note
2. View Notes
3. Read Note
4. Edit Note
5. Delete Note
0. Back
========================================
```

## What I Learned in Version 0.3

While building the Notes system, I practiced:

- Creating and calling functions
- Importing functions between Python modules
- Using Python lists
- Using dictionaries to represent structured data
- Using unique IDs
- Using `if`, `elif`, and `else`
- Using `for` and `while` loops
- Working with user input
- Validating input
- Connecting notes to subjects
- Searching for a note by ID
- Implementing CRUD operations
- Handling invalid input and edge cases
- Breaking a larger program into separate modules

I also learned that Python lists begin counting at index `0`. Because users see subjects starting at `1`, StudyVault converts a user's selection using:

```python
subjects[choice_number - 1]
```

Version 0.3 also uses a `next_note_id` variable so each note receives a unique ID during the current program session.

## Current Limitation

Version 0.3 stores information only while StudyVault is running.

For example:

```text
Start StudyVault
       ↓
Create subjects and notes
       ↓
Information exists in memory
       ↓
Close StudyVault
       ↓
Information disappears
```

Version 0.3 will introduce SQLite so subjects and notes can remain saved after the program closes.

## Why I Built This Project

I created StudyVault CL to learn computer science by building a complete application from the ground up instead of only completing small programming exercises.

The project is being developed incrementally so that each version introduces new computer science concepts and improves the application.

Through this project, I am learning about:

- Variables
- Functions
- Conditionals
- Loops
- Lists
- Dictionaries
- Input validation
- Modules
- Program architecture
- CRUD operations
- Databases
- SQL
- Searching and sorting
- Algorithms
- Testing
- Git
- GitHub
- Software documentation

## Development Roadmap

StudyVault is being built in stages.

```text
Version 0.1 → Subjects ✅
Version 0.2 → Notes ✅
Version 0.3 → SQLite Database ✅
Version 0.4 → Flashcards
Version 0.5 → Quiz System
Version 0.6 → Spaced Repetition
Version 0.7 → Search
Version 0.8 → Study Tracking
Version 0.9 → Analytics and Testing
Version 1.0 → Complete Portfolio Release
```

A full pseudocode design document is included in the `pseudocode` directory.

## Status

🚧 StudyVault CL is currently under active development.

Current release: **Version 0.3**