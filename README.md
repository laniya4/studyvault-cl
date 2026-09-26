# StudyVault CL

StudyVault CL is a beginner-friendly command-line study management application built with Python.

The goal of StudyVault is to create one place where students can organize subjects, notes, flashcards, quizzes, study sessions, goals, and learning progress directly from the command line.

## Current Version

**Version 0.1**

StudyVault currently supports:

- Adding subjects
- Viewing subjects
- Preventing duplicate subject names
- Rejecting empty subject names
- Handling invalid menu choices
- Exiting the application safely

## Planned Features

Future versions of StudyVault CL will include:

- Persistent SQLite database storage
- Notes
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

StudyVault CL is being developed with:

- Python
- SQLite
- Git
- GitHub
- VS Code

Future versions will also use:

- pytest for automated testing
- GitHub Actions for continuous testing

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
    └── subjects.py
```

## Running StudyVault

Make sure Python 3 is installed.

From the main project directory, run:

```bash
python3 studyvault/main.py
```

The program will display:

```text
========================================
             STUDYVAULT CL
========================================
1. Add Subject
2. View Subjects
0. Exit
========================================
```

## Why I Built This Project

I created StudyVault CL to learn computer science by building a complete application from the ground up instead of only completing small programming exercises.

The project is being developed incrementally so that each version introduces new computer science concepts.

Through this project, I am learning about:

- Variables
- Functions
- Conditionals
- Loops
- Lists
- Input validation
- Modules
- Program architecture
- Databases
- SQL
- Searching and sorting
- Algorithms
- Testing
- Git
- GitHub
- Software documentation

## Development Approach

StudyVault is being built in stages.

```text
Version 0.1 → Subjects
Version 0.2 → Notes
Version 0.3 → SQLite Database
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

Current release: **Version 0.1**