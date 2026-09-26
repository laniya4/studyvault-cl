# StudyVault CL

StudyVault CL is a beginner-friendly command-line study management application built with Python and SQLite.

The goal of StudyVault CL is to create one place where students can organize subjects, notes, flashcards, quizzes, study sessions, goals, and learning progress directly from the command line.

## Current Version

**Version 0.4**

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
- Creating flashcards
- Connecting flashcards to subjects
- Viewing flashcards
- Studying flashcards
- Editing flashcards
- Deleting flashcards
- Rejecting empty flashcard questions and answers
- Validating flashcard IDs
- Confirming flashcard deletion
- Persistent SQLite storage
- Persistent subjects
- Persistent notes
- Persistent flashcards
- Database-generated IDs
- Handling invalid menu choices
- Exiting the application safely

## Version 0.1 — Subjects

Version 0.1 introduced the first working StudyVault CL application.

Users could:

- Create subjects
- View subjects
- Prevent duplicate subject names
- Reject empty subject names
- Navigate a command-line menu

This version introduced basic Python concepts such as:

- Variables
- Functions
- Lists
- Loops
- Conditionals
- User input
- Input validation
- Modules

At this stage, subjects were stored temporarily in memory.

## Version 0.2 — Notes System

Version 0.2 introduced a complete Notes system.

Users could:

- Create a note
- Assign a note to a subject
- View all notes
- Read an individual note
- Edit an existing note
- Delete a note
- Cancel a deletion
- Use unique note IDs

The Notes system introduced CRUD operations:

- **Create** — create a new note
- **Read** — view or read a note
- **Update** — edit an existing note
- **Delete** — remove a note

Version 0.2 still stored information temporarily in memory.

## Version 0.3 — SQLite Database

Version 0.3 introduced persistent data storage using SQLite.

Before Version 0.3:

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

Starting with Version 0.3:

```text
Start StudyVault
       ↓
Create subjects and notes
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
- Persistent storage
- SQL queries
- Relational database tables
- Primary keys
- Foreign keys
- Database-generated IDs
- Database connections
- Subject-note relationships
- SQL `INSERT`
- SQL `SELECT`
- SQL `UPDATE`
- SQL `DELETE`

StudyVault currently stores its local application data in:

```text
studyvault.db
```

The database file is excluded from Git using `.gitignore`.

## Version 0.4 — Flashcards

Version 0.4 introduced a persistent Flashcards system.

Users can:

- Create flashcards
- Assign flashcards to subjects
- View saved flashcards
- Study flashcards
- Reveal flashcard answers
- Edit flashcards
- Delete flashcards
- Cancel flashcard deletion
- Use database-generated flashcard IDs
- Keep flashcards after closing StudyVault

Example flashcard:

```text
Subject: Computer Science

Question:
What is binary search?

Answer:
An algorithm that repeatedly halves a sorted search space.
```

Flashcards are stored in SQLite and connected to subjects using a foreign key.

The Flashcards system also demonstrates CRUD:

- **Create** — create a flashcard
- **Read** — view and study flashcards
- **Update** — edit a flashcard
- **Delete** — delete a flashcard

## Database Structure

StudyVault currently uses three main SQLite tables:

```text
subjects
   │
   ├──── notes
   │
   └──── flashcards
```

A subject might have:

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

For example:

```text
subjects

subject_id | name
-----------|-----------------
1          | Calculus I
2          | Computer Science
```

A flashcard can reference:

```text
subject_id = 2
```

which means that flashcard belongs to:

```text
Computer Science
```

This is an example of a relational database relationship.

## Planned Features

Future versions of StudyVault CL will include:

- Quiz system
- Spaced repetition
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
    └── subjects.py
```

`studyvault.db` is stored locally and ignored by Git so personal study data is not uploaded with the source code.

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
- Error handling
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
- Git
- GitHub
- Version control
- Software documentation

## SQL and CRUD

StudyVault uses the four common CRUD operations.

```text
CRUD                    SQL

Create                  INSERT
Read                    SELECT
Update                  UPDATE
Delete                  DELETE
```

For example, creating a flashcard eventually causes StudyVault to execute an SQL `INSERT`.

Viewing flashcards uses `SELECT`.

Editing a flashcard uses `UPDATE`.

Deleting a flashcard uses `DELETE`.

## Parameterized Queries

StudyVault uses SQL parameter placeholders such as:

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

The `?` allows Python to safely provide data to SQLite instead of manually inserting user input directly into the SQL statement.

This is also an important protection against SQL injection.

## Persistent Storage

Starting with Version 0.3, StudyVault information remains saved after the application closes.

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

Version 0.4 extends that persistence to flashcards.

## Why I Built This Project

I created StudyVault CL to learn computer science by building a complete application from the ground up instead of only completing isolated programming exercises.

I am developing the project incrementally so each version introduces new features and new computer science concepts.

Rather than trying to build the entire application at once, each version represents a working development milestone.

## Development Roadmap

StudyVault is being built in stages.

```text
Version 0.1 → Subjects ✅
Version 0.2 → Notes ✅
Version 0.3 → SQLite Database ✅
Version 0.4 → Flashcards ✅
Version 0.5 → Quiz System ✅
Version 0.6 → Spaced Repetition
Version 0.7 → Search
Version 0.8 → Study Tracking
Version 0.9 → Analytics and Testing
Version 1.0 → Complete Portfolio Release
```

A full pseudocode design document is included in the `pseudocode` directory.

## Status

🚧 StudyVault CL is currently under active development.

Current release: **Version 0.4**

Next planned release: **Version 0.5 — Quiz System**