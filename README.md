## Current Version

**Version 1.0**

StudyVault CL currently supports:

- Adding and viewing subjects
- Persistent SQLite database storage
- Creating, reading, editing, and deleting notes
- Connecting notes to subjects
- Creating, viewing, studying, editing, and deleting flashcards
- Connecting flashcards to subjects
- Quiz mode
- Persistent quiz history
- Spaced repetition
- Due-date scheduling for flashcards
- Flashcard review statistics
- Global search
- Searching subjects
- Searching notes
- Searching flashcards
- Partial-text and case-insensitive search
- Study-session tracking
- Recording study minutes and activities
- Viewing study history
- Viewing study totals
- Per-subject study statistics
- Analytics dashboard
- StudyVault overview statistics
- Study-session analytics
- Quiz-performance analytics
- Flashcard analytics
- Automated testing with pytest
- Temporary isolated test databases
- 34 automated tests
- Continuous integration with GitHub Actions

---

## Version 1.0 — Complete Portfolio Release

Version 1.0 represents the first complete portfolio release of StudyVault CL.

StudyVault began as a small command-line program for storing subjects and gradually developed into a modular study-management application with persistent data storage, study tools, analytics, automated testing, and continuous integration.

The Version 1.0 release combines all of the major systems developed throughout Versions 0.1 through 0.9.

### Version 1.0 Includes

- Subject management
- Notes
- SQLite persistence
- Flashcards
- Quiz mode
- Spaced repetition
- Global search
- Study tracking
- Analytics
- Automated testing
- GitHub Actions continuous integration
- Modular Python architecture
- Input validation
- Persistent relationships between subjects and study data

---

## Main Menu

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
7. Search
8. Study Tracking
9. Analytics
0. Exit
========================================
```

---

## Core Features

### Subjects

Users can:

- Add subjects
- View saved subjects
- Prevent duplicate subject names
- Reject empty subject names
- Store subjects persistently with SQLite

### Notes

Users can:

- Create notes
- Connect notes to subjects
- View notes
- Read complete notes
- Edit notes
- Delete notes
- Validate note IDs
- Store notes persistently

### Flashcards

Users can:

- Create flashcards
- Connect flashcards to subjects
- View flashcards
- Study flashcards
- Edit flashcards
- Delete flashcards
- Store flashcards persistently

### Quiz System

Users can:

- Take quizzes generated from saved flashcards
- Answer study questions
- Receive immediate feedback
- View correct answers
- Receive a final score
- View percentage results
- Save quiz attempts
- View quiz history

### Spaced Repetition

StudyVault includes a spaced-repetition review system.

After reviewing a card, users rate how well they remembered it:

```text
1. Again
2. Hard
3. Good
4. Easy
```

StudyVault then calculates the next review interval and stores the next-review date in SQLite.

The system tracks:

- Review count
- Remembered count
- Forgotten count
- Accuracy
- Current interval
- Last review date
- Next review date
- Due flashcards

### Global Search

StudyVault can search across saved study information.

Users can search:

- Subjects
- Notes
- Flashcards

Search supports:

- Partial-text matching
- Case-insensitive matching
- Note-title matching
- Note-content matching
- Flashcard-question matching
- Flashcard-answer matching
- Search-result previews

### Study Tracking

Users can:

- Log study sessions
- Choose the subject studied
- Record study minutes
- Record study activities
- View study history
- View total study time
- View totals by subject

Study-session information remains available after StudyVault closes because it is stored in SQLite.

### Analytics

StudyVault can analyze stored learning data through four analytics screens:

```text
========================================
               ANALYTICS
========================================
1. Overview
2. Study Analytics
3. Quiz Analytics
4. Flashcard Analytics
0. Back
========================================
```

Analytics include:

- Total subjects
- Total notes
- Total flashcards
- Total quiz attempts
- Total study sessions
- Total study minutes
- Average study-session length
- Most-studied subject
- Average quiz score
- Highest quiz score
- Lowest quiz score
- Flashcard review totals
- Remembered and forgotten cards
- Flashcard accuracy
- Cards currently due

---

## Persistent Storage

StudyVault uses SQLite for persistent data storage.

Information can remain available after the application closes, including:

- Subjects
- Notes
- Flashcards
- Quiz history
- Spaced-repetition progress
- Review dates
- Review statistics
- Study sessions
- Study-time information

The application initializes the required database tables automatically when StudyVault starts.

---

## Automated Testing

StudyVault CL includes an automated test suite built with `pytest`.

Run all tests locally with:

```bash
python3 -m pytest -v
```

The Version 1.0 test suite contains:

```text
34 automated tests
```

Current test areas include:

### Analytics Tests

Tests verify:

- Empty-database analytics
- Subject counting
- Multiple-subject counting
- Study-session counting
- Invalid table-name protection
- Analytics output

### Database Tests

Tests verify:

- Database creation
- Subjects table
- Notes table
- Flashcards table
- Quiz-attempts table
- Study-sessions table
- SQLite foreign-key enforcement

### Search Tests

Tests verify:

- Subject search
- Case-insensitive searching
- Partial-text searching
- Note-title searching
- Note-content searching
- Flashcard-question searching
- Flashcard-answer searching
- No-result behavior
- Short search-result previews
- Long search-result previews

### Spaced-Repetition Tests

Tests verify:

- Again intervals
- Hard intervals
- Good intervals
- Easy intervals
- Due flashcard retrieval
- Future flashcards not appearing as due
- Saving successful reviews
- Saving forgotten reviews
- Review statistics
- Review scheduling
- Reviewed cards not immediately becoming due again

The tests use temporary SQLite databases so automated testing does not modify the user's real StudyVault data.

---

## Continuous Integration

StudyVault CL uses GitHub Actions for continuous integration.

The workflow is stored at:

```text
.github/workflows/tests.yml
```

GitHub automatically runs the StudyVault test suite when code is pushed to the `main` branch or when a pull request targets `main`.

The CI process is:

```text
Push code to GitHub
        ↓
GitHub Actions starts
        ↓
Repository is checked out
        ↓
Python is installed
        ↓
pytest is installed
        ↓
StudyVault tests run
        ↓
PASS ✅ or FAIL ❌
```

Version 1.0 has successfully passed the automated GitHub Actions workflow.

---

## Project Structure

```text
studyvault-cl/
├── .github/
│   └── workflows/
│       └── tests.yml
├── pseudocode/
│   └── studyvault_cl.pseudo
├── studyvault/
│   ├── __init__.py
│   ├── analytics.py
│   ├── database.py
│   ├── flashcards.py
│   ├── main.py
│   ├── notes.py
│   ├── quizzes.py
│   ├── search.py
│   ├── spaced_repetition.py
│   ├── study_tracking.py
│   └── subjects.py
├── tests/
│   ├── test_analytics.py
│   ├── test_database.py
│   ├── test_search.py
│   └── test_spaced_repetition.py
├── .gitignore
└── README.md
```

The local `studyvault.db` database is excluded from Git so personal StudyVault data is not committed to the repository.

---

## Technologies

StudyVault CL uses:

- Python
- SQLite
- SQL
- pytest
- Git
- GitHub
- GitHub Actions
- VS Code

---

## What I Learned

Building StudyVault CL provided practice with:

### Python

- Variables
- Functions
- Conditionals
- Loops
- Lists
- Dictionaries
- Modules
- User input
- Input validation
- Error handling
- Program organization

### Databases

- SQLite
- SQL
- Tables
- Primary keys
- Foreign keys
- Relationships
- CRUD operations
- Persistent storage
- Aggregate queries
- Database-generated IDs

### SQL

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `JOIN`
- `GROUP BY`
- `ORDER BY`

### Algorithms and Application Logic

- Searching
- Partial-text matching
- Case-insensitive matching
- Quiz scoring
- Spaced-repetition scheduling
- Study statistics
- Data aggregation

### Software Engineering

- Modular program architecture
- Separation of responsibilities
- Incremental development
- Versioning
- Git commits
- GitHub repositories
- Software documentation
- Automated testing
- Unit testing
- Regression testing
- Test isolation
- Continuous integration

### Testing

- pytest
- Assertions
- Fixtures
- Temporary databases
- `monkeypatch`
- Capturing terminal output
- Testing database behavior
- Testing search behavior
- Testing scheduling logic
- GitHub Actions

---

## Development Roadmap

```text
Version 0.1 → Subjects ✅
Version 0.2 → Notes ✅
Version 0.3 → SQLite Database ✅
Version 0.4 → Flashcards ✅
Version 0.5 → Quiz System ✅
Version 0.6 → Spaced Repetition ✅
Version 0.7 → Search ✅
Version 0.8 → Study Tracking ✅
Version 0.9 → Analytics and Testing ✅
Version 1.0 → Complete Portfolio Release ✅
```

---

## Future Enhancements

Version 1.0 completes the original StudyVault CL roadmap.

Possible future improvements include:

- Study goals
- Study streaks
- CSV data export
- Additional automated tests
- More advanced analytics
- Database migrations
- Configuration settings
- Packaging StudyVault as an installable Python application
- A graphical or web-based interface

These are future enhancements and are not required for the Version 1.0 release.

---

## Status

✅ **StudyVault CL Version 1.0 is complete.**

Current release: **Version 1.0**

Automated test suite: **34 tests passing**

Continuous integration: **GitHub Actions passing**

StudyVault CL now provides a complete command-line study-management system with persistent storage, study tools, analytics, automated testing, and continuous integration.