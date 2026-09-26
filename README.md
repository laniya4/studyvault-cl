## Current Version

**Version 0.8**

Add these to the current features list:

- Logging study sessions
- Connecting study sessions to subjects
- Recording minutes studied
- Recording study activities
- Viewing study history
- Viewing total study time
- Viewing per-subject study totals
- Persistent study-session storage with SQLite

## Version 0.8 — Study Tracking

Version 0.8 introduced persistent study-session tracking.

Users can:

- Log a study session
- Choose the subject they studied
- Record the number of minutes studied
- Record what they worked on
- View previous study sessions
- View total study time
- View totals grouped by subject
- Keep study history after closing StudyVault

Example:

```text
Subject: Computer Science
Time: 45 minute(s)
Activity: Binary search and algorithms
```

StudyVault can also calculate totals such as:

```text
Total sessions: 2
Total study time: 75 minute(s)
Total time: 1 hour(s) 15 minute(s)

BY SUBJECT

Computer Science
Sessions: 1
Minutes: 45

Calculus I
Sessions: 1
Minutes: 30
```

Study sessions are stored persistently in SQLite.

### Planned Features

Remove:

```text
- Study-session tracking
```

Keep:

```text
- Study goals
- Progress analytics
- Study streaks
- CSV data export
- Automated testing
```

### Project Structure

Change the `studyvault/` section to:

```text
studyvault/
├── __init__.py
├── database.py
├── flashcards.py
├── main.py
├── notes.py
├── quizzes.py
├── search.py
├── spaced_repetition.py
├── study_tracking.py
└── subjects.py
```

### Main Menu

Update it to:

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
0. Exit
========================================
```

### Study Tracking Menu

Add:

```text
========================================
            STUDY TRACKING
========================================
1. Log Study Session
2. View Study History
3. View Study Totals
0. Back
========================================
```

### Persistent Storage

Add study sessions to the persistence list:

- Subjects
- Notes
- Flashcards
- Quiz history
- Spaced-repetition progress
- Review dates
- Review statistics
- Study sessions
- Study-time totals

### Development Roadmap

```text
Version 0.1 → Subjects ✅
Version 0.2 → Notes ✅
Version 0.3 → SQLite Database ✅
Version 0.4 → Flashcards ✅
Version 0.5 → Quiz System ✅
Version 0.6 → Spaced Repetition ✅
Version 0.7 → Search ✅
Version 0.8 → Study Tracking ✅
Version 0.9 → Analytics and Testing
Version 1.0 → Complete Portfolio Release
```

## Status

🚧 StudyVault CL is currently under active development.

Current release: **Version 0.8**

Next planned release: **Version 0.9 — Analytics and Testing**