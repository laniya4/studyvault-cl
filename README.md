## Current Version

**Version 0.9**

Add these to the current features list:

- Analytics dashboard
- StudyVault overview statistics
- Study-session analytics
- Quiz performance analytics
- Flashcard analytics
- Average study-session calculations
- Most-studied subject tracking
- Average, highest, and lowest quiz scores
- Flashcard review statistics
- Flashcard accuracy calculations
- Due-flashcard analytics
- Automated testing with pytest
- Temporary test databases
- Database isolation during tests
- Automated analytics tests

## Version 0.9 — Analytics and Testing

Version 0.9 introduced analytics and automated testing to StudyVault CL.

### Analytics

StudyVault can now analyze information already stored in the SQLite database.

The Analytics menu includes:

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

### Overview

The Overview screen summarizes the entire StudyVault database.

It can display:

- Total subjects
- Total notes
- Total flashcards
- Total quiz attempts
- Total study sessions
- Total study minutes
- Total study time

Example:

```text
========================================
           STUDYVAULT OVERVIEW
========================================
Total Subjects: 2
Total Notes: 3
Total Flashcards: 5
Total Quiz Attempts: 1
Total Study Sessions: 2
Total Study Minutes: 75
Total Study Time: 1 hour(s) 15 minute(s)
```

### Study Analytics

StudyVault can analyze study-session data including:

- Number of study sessions
- Total minutes studied
- Total study time
- Average session length
- Most-studied subject
- Study time grouped by subject

Example:

```text
========================================
             STUDY ANALYTICS
========================================
Total Sessions: 2
Total Minutes: 75
Total Time: 1 hour(s) 15 minute(s)
Average Session: 37.5 minute(s)

MOST STUDIED SUBJECT
--------------------
Computer Science: 45 minute(s)
```

### Quiz Analytics

StudyVault can analyze saved quiz attempts.

It tracks:

- Total quiz attempts
- Average quiz score
- Highest quiz score
- Lowest quiz score
- Quiz performance grouped by subject

Example:

```text
========================================
              QUIZ ANALYTICS
========================================
Total Attempts: 1
Average Score: 66.7%
Highest Score: 66.7%
Lowest Score: 66.7%
```

### Flashcard Analytics

StudyVault also analyzes flashcard and spaced-repetition activity.

It can display:

- Total flashcards
- Total reviews
- Remembered cards
- Forgotten cards
- Overall flashcard accuracy
- Cards currently due
- Most-reviewed flashcard

Example:

```text
========================================
           FLASHCARD ANALYTICS
========================================
Total Flashcards: 3
Total Reviews: 3
Remembered: 2
Forgotten: 1
Overall Accuracy: 66.7%
Cards Due Today: 0
```

## Automated Testing

Version 0.9 introduced automated testing with `pytest`.

Before automated testing, StudyVault features were tested manually by running the program and entering test data.

Now automated tests can verify expected behavior automatically.

Run the tests with:

```bash
python3 -m pytest -v
```

The first StudyVault automated test suite contains six tests.

Example successful result:

```text
collected 6 items

test_empty_database_counts PASSED
test_subject_count PASSED
test_multiple_subject_count PASSED
test_study_session_count PASSED
test_invalid_table_name PASSED
test_overview_output PASSED

6 passed
```

The tests currently verify:

- Empty-database analytics
- Subject counting
- Multiple-subject counting
- Study-session counting
- Invalid table-name handling
- Analytics overview output

StudyVault's tests use temporary SQLite databases.

This means automated tests can create and modify test information without changing the user's real `studyvault.db` file.

The testing process is:

```text
Create temporary database
        ↓
Initialize StudyVault tables
        ↓
Insert controlled test data
        ↓
Run function
        ↓
Compare actual result with expected result
        ↓
PASS ✅ or FAIL ❌
```

## Planned Features

Future versions of StudyVault CL will include:

- Study goals
- Study streaks
- CSV data export
- Additional automated tests
- GitHub Actions continuous testing
- Portfolio documentation and final polish

## Project Structure

Update the project structure to include Analytics and tests:

```text
studyvault-cl/
├── README.md
├── .gitignore
├── studyvault.db
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
└── tests/
    └── test_analytics.py
```

## Main Menu

Update the main menu documentation to:

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

## Technologies

StudyVault CL currently uses:

- Python
- SQLite
- SQL
- pytest
- Git
- GitHub
- VS Code

Future development will also use:

- GitHub Actions

## Computer Science Concepts Added in Version 0.9

Version 0.9 introduced additional concepts including:

- Data aggregation
- SQL aggregate functions
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- SQL grouping
- `GROUP BY`
- SQL sorting
- Automated testing
- Unit testing
- pytest
- Assertions
- Fixtures
- Temporary databases
- Test isolation
- Dependency replacement with `monkeypatch`
- Capturing terminal output
- Regression testing

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
Version 1.0 → Complete Portfolio Release
```

## Status

🚧 StudyVault CL is currently under active development.

Current release: **Version 0.9**

Next planned release: **Version 1.0 — Complete Portfolio Release**