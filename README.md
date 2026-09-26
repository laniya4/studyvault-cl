# StudyVault CL

StudyVault CL is a beginner-friendly command-line study management application built with Python and SQLite.

The goal of StudyVault CL is to create one place where students can organize subjects, notes, flashcards, quizzes, study sessions, goals, and learning progress directly from the command line.

## Current Version

**Version 0.6**

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
- Creating flashcards
- Connecting flashcards to subjects
- Viewing flashcards
- Studying flashcards
- Editing flashcards
- Deleting flashcards
- Creating quizzes from saved flashcards
- Selecting quiz subjects
- Checking quiz answers
- Calculating quiz scores and percentages
- Saving quiz history
- Viewing previous quiz results
- Reviewing due flashcards
- Rating flashcards as Again, Hard, Good, or Easy
- Calculating future review dates
- Tracking flashcard review counts
- Tracking remembered and forgotten cards
- Calculating flashcard accuracy
- Viewing review schedules
- Viewing flashcard progress
- Persistent SQLite storage
- Database-generated IDs
- Input validation
- Handling invalid menu choices
- Exiting the application safely

## Version 0.1 — Subjects

Version 0.1 introduced the first working version of StudyVault CL.

Users could:

- Create subjects
- View subjects
- Prevent duplicate subject names
- Reject empty subject names
- Navigate a command-line menu

This version introduced beginner Python concepts including:

- Variables
- Functions
- Lists
- Loops
- Conditionals
- User input
- Input validation
- Modules

At this stage, information existed only while the program was running.

## Version 0.2 — Notes System

Version 0.2 introduced the Notes system.

Users could:

- Create notes
- Assign notes to subjects
- View notes
- Read complete notes
- Edit notes
- Delete notes
- Cancel deletion
- Use unique note IDs

The Notes system introduced CRUD:

```text
C = Create
R = Read
U = Update
D = Delete
```

These operations are common throughout software development.

## Version 0.3 — SQLite Database

Version 0.3 introduced persistent SQLite database storage.

Before SQLite:

```text
Start StudyVault
       ↓
Create information
       ↓
Information exists in memory
       ↓
Close StudyVault
       ↓
Information disappears
```

Starting with Version 0.3:

```text
Start StudyVault
       ↓
Create information
       ↓
Python sends data to SQLite
       ↓
SQLite saves the information
       ↓
Close StudyVault
       ↓
Restart StudyVault
       ↓
Information is still available
```

Version 0.3 introduced:

- SQLite
- SQL
- Persistent storage
- Relational database tables
- Primary keys
- Foreign keys
- Database-generated IDs
- Database connections
- Subject-note relationships
- `INSERT`
- `SELECT`
- `UPDATE`
- `DELETE`

StudyVault stores local application data in:

```text
studyvault.db
```

The database file is excluded from Git using `.gitignore`.

## Version 0.4 — Flashcards

Version 0.4 introduced persistent flashcards.

Users can:

- Create flashcards
- Assign flashcards to subjects
- View flashcards
- Study flashcards
- Reveal answers
- Edit flashcards
- Delete flashcards
- Cancel deletion
- Keep flashcards after closing the application

Example:

```text
Subject: Computer Science

Question:
What is binary search?

Answer:
An algorithm that repeatedly halves a sorted search space.
```

Flashcards are connected to subjects using relational database relationships.

The Flashcards system also demonstrates CRUD:

```text
Create → INSERT
Read   → SELECT
Update → UPDATE
Delete → DELETE
```

## Version 0.5 — Quiz System

Version 0.5 introduced quizzes generated from saved flashcards.

Users can:

- Choose a quiz subject
- Answer saved flashcard questions
- Receive correct or incorrect feedback
- See the correct answer after a mistake
- Receive a final score
- Receive a percentage
- Save completed quiz attempts
- View quiz history after restarting StudyVault

Example:

```text
Question 1 of 3

What is binary search?

Your answer:
An algorithm that repeatedly halves a sorted search space.

Correct! ✅
```

At the end of a quiz, StudyVault calculates:

```text
Correct answers
      ÷
Total questions
      ×
100
      ↓
Percentage
```

Example:

```text
Score: 2/3
Percentage: 66.7%
```

Quiz results are stored persistently in SQLite.

## Version 0.6 — Spaced Repetition

Version 0.6 introduced a spaced-repetition review system.

Instead of showing every flashcard equally, StudyVault can now schedule flashcards for future review.

During a review, users rate how well they remembered a flashcard:

```text
1. Again — I forgot it
2. Hard  — I barely remembered
3. Good  — I remembered
4. Easy  — I knew it immediately
```

The rating determines when the flashcard should appear again.

For example:

```text
Again
  ↓
Review sooner

Good
  ↓
Review after a moderate interval

Easy
  ↓
Review after a longer interval
```

StudyVault now tracks:

- Review count
- Remembered count
- Forgotten count
- Accuracy percentage
- Current review interval
- Last review date
- Next review date

Example:

```text
Question:
What is binary search?

Reviews: 1
Remembered: 1
Forgotten: 0
Accuracy: 100.0%
Interval: 3 day(s)
Last reviewed: 2026-09-26
Next review: 2026-09-29
```

Review data remains saved after StudyVault closes because it is stored in SQLite.

## Database Structure

StudyVault currently stores several related types of information:

```text
subjects
   │
   ├── notes
   │
   └── flashcards
           │
           └── spaced-repetition data

quiz_attempts
```

A subject can have many notes and flashcards.

For example:

```text
Computer Science
       │
       ├── Note: Binary Search Notes
       │
       ├── Flashcard: What is binary search?
       │
       └── Flashcard: What is a hash table?
```

The database uses IDs to connect information.

Example:

```text
subjects

subject_id | name
-----------|-----------------
1          | Calculus I
2          | Computer Science
```

A flashcard containing:

```text
subject_id = 2
```

belongs to:

```text
Computer Science
```

This is an example of a relational database relationship.

## Planned Features

Future versions of StudyVault CL will include:

- Global search
- Study-session tracking
- Study goals
- Progress analytics
- Study streaks
- CSV data export
- Automated testing

## Technologies

StudyVault CL currently uses:

- Python
- SQLite
- SQL
- Git
- GitHub
- VS Code

Future versions will also use:

- pytest
- GitHub Actions

## Project Structure

```text
studyvault-cl/
├── README.md
├── .gitignore
├── studyvault.db
├── pseudocode/
│   └── studyvault_cl.pseudo
└── studyvault/
    ├── __init__.py
    ├── database.py
    ├── flashcards.py
    ├── main.py
    ├── notes.py
    ├── quizzes.py
    ├── spaced_repetition.py
    └── subjects.py
```

`studyvault.db` is stored locally and ignored by Git so local study data is not uploaded with the source code.

## Running StudyVault

Make sure Python 3 is installed.

From the main project directory, run:

```bash
python3 studyvault/main.py
```

The main menu displays:

```text
========================================
             STUDYVAULT CL
========================================
1. Add Subject
2. View Subjects
3. Notes
4. Flashcards
5. Quiz
6. Spaced Repetition
0. Exit
========================================
```

## Notes Menu

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

## Flashcards Menu

```text
========================================
              FLASHCARDS
========================================
1. Create Flashcard
2. View Flashcards
3. Study Flashcards
4. Edit Flashcard
5. Delete Flashcard
0. Back
========================================
```

## Quiz Menu

```text
========================================
                  QUIZ
========================================
1. Start Quiz
2. View Quiz History
0. Back
========================================
```

## Spaced Repetition Menu

```text
========================================
          SPACED REPETITION
========================================
1. Review Due Flashcards
2. View Review Schedule
3. View Flashcard Progress
0. Back
========================================
```

## Computer Science Concepts Used

StudyVault CL currently demonstrates:

- Variables
- Functions
- Conditionals
- `for` loops
- `while` loops
- Lists
- Dictionaries
- Modules
- Imports
- User input
- Input validation
- Program architecture
- CRUD operations
- Relational databases
- SQLite
- SQL
- Primary keys
- Foreign keys
- Database-generated IDs
- Database connections
- Parameterized SQL queries
- Persistent storage
- Searching by ID
- Randomization
- String normalization
- Date calculations
- Scheduling algorithms
- State tracking
- Accuracy calculations
- Git
- GitHub
- Version control
- Software documentation

## SQL and CRUD

StudyVault uses the four common CRUD operations:

```text
CRUD       SQL

Create     INSERT
Read       SELECT
Update     UPDATE
Delete     DELETE
```

For example:

```text
Create flashcard
      ↓
INSERT

View flashcards
      ↓
SELECT

Edit flashcard
      ↓
UPDATE

Delete flashcard
      ↓
DELETE
```

## Parameterized Queries

StudyVault uses SQL parameter placeholders.

Example:

```python
connection.execute(
    """
    SELECT subject_id
    FROM subjects
    WHERE name = ?
    """,
    (subject_name,)
)
```

The `?` placeholder lets Python safely provide information to SQLite without directly inserting user input into an SQL statement.

Parameterized queries also help protect the application from SQL injection.

## Persistent Storage

Starting with Version 0.3, StudyVault information remains saved after the program closes.

```text
User creates information
          ↓
Python processes it
          ↓
SQL query
          ↓
SQLite
          ↓
studyvault.db
          ↓
Information remains saved
```

Persistence now includes:

- Subjects
- Notes
- Flashcards
- Quiz history
- Spaced-repetition progress
- Review dates
- Review statistics

## Why I Built This Project

I created StudyVault CL to learn computer science by building a complete application from the ground up instead of only completing isolated programming exercises.

I am developing the project incrementally so that each version introduces new features and new computer science concepts.

Rather than trying to build the entire application at once, each version represents a working development milestone.

This project gives me hands-on experience with programming, databases, algorithms, testing, version control, debugging, and software documentation.

## Development Roadmap

StudyVault is being built in stages.

```text
Version 0.1 → Subjects ✅
Version 0.2 → Notes ✅
Version 0.3 → SQLite Database ✅
Version 0.4 → Flashcards ✅
Version 0.5 → Quiz System ✅
Version 0.6 → Spaced Repetition ✅
Version 0.7 → Search
Version 0.8 → Study Tracking
Version 0.9 → Analytics and Testing
Version 1.0 → Complete Portfolio Release
```

A full pseudocode design document is included in the `pseudocode` directory.

## Status

🚧 StudyVault CL is currently under active development.

Current release: **Version 0.6**

Next planned release: **Version 0.7 — Search**