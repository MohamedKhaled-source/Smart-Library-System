# 📚 Zewail City Library Management System

A Python-based library management system featuring both a **command-line interface (CLI)** and a full **graphical desktop application (GUI)** built with Tkinter. The system supports book cataloguing, borrowing/returning, sales transactions, statistics reporting, and CSV-style data import/export — all backed by a shared, in-memory data layer.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the GUI](#running-the-gui)
  - [Running the CLI](#running-the-cli)
- [Module Reference](#module-reference)
- [Import / Export File Format](#import--export-file-format)
- [Transaction Logging](#transaction-logging)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

This project models a library's book inventory and the operations performed on it — adding, updating, deleting, searching, borrowing, returning, and selling books — while tracking basic statistics (genre breakdown, oldest/newest titles, totals). It ships with a pre-populated dataset of ~295 books spanning genres from Classic literature to Horror and Action.

The codebase is split into clean layers:

| Layer | File | Responsibility |
|---|---|---|
| **Data** | `library_data.py` | Holds the in-memory book database and the ID counter |
| **Logic** | `library_functions.py` | Pure business logic — CRUD, search, borrow/return, sales, import/export, stats |
| **CLI** | `main.py` | Text-based menu interface for terminal use |
| **GUI** | `gui.py` | Tkinter desktop application with tabbed navigation |

---

## Features

**Book Management**
- Add, update, delete, and view books
- Auto-incrementing unique book IDs
- Search by title (partial, case-insensitive), author, or year
- Filter by genre/type
- Sort catalogue alphabetically by title

**Borrowing & Returns**
- Borrow a book to a named borrower for a set number of days
- Return tracking with automatic overdue flagging (loans over 7 days)
- Prevents borrowing a book that is already checked out

**Sales / Shop**
- Purchase books against available copy count
- Auto-generated itemized receipts
- Per-user purchase history log
- Copies and sold counters update automatically after each sale

**Statistics**
- Total book count
- Oldest and newest titles in the catalogue
- Breakdown of books by genre/type

**Data Import / Export**
- Export the entire catalogue to a delimited `.txt` file
- Import books from a correctly formatted `.txt` file back into the system

**Graphical Interface (`gui.py`)**
- Four-tab layout: *Manage Books*, *Borrow / Return*, *Shop / Sales*, *Statistics & Logs*
- Live-updating table (Treeview) of the full catalogue
- Search-and-filter controls by ID, author, and year
- Timestamped transaction logging to `transaction_log.txt`
- Confirmation-protected "Delete All Books" action

**Command-Line Interface (`main.py`)**
- Numbered menu system covering all core operations
- Paginated catalogue browsing (50 books per page) for large libraries

---

## Project Structure

```
library-management-system/
├── main.py                  # CLI entry point
├── gui.py                   # GUI entry point (Tkinter)
├── library_functions.py     # Core business logic
├── library_data.py          # In-memory database + starter dataset
├── transaction_log.txt      # Auto-generated GUI activity log (created at runtime)
└── README.md
```

---

## Data Model

Each book is stored as a dictionary inside the `library` dict in `library_data.py`, keyed by a unique integer ID:

```python
library = {
    1: {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "type_book": "Fiction",
        "global_rating": 4.3,
        "copies": 3,
        "price": 67.5,
        "sold": 0
    },
    ...
}
current_id = 295  # Next ID to be assigned to a new book
```

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Unique identifier (dictionary key) |
| `title` | `str` | Book title |
| `author` | `str` | Author name |
| `year` | `int` | Publication year (supports negative years for ancient texts, e.g. *The Iliad*) |
| `type_book` | `str` | Genre/category |
| `global_rating` | `float` | Rating out of 5 |
| `copies` | `int` | Copies currently available |
| `price` | `float` | Unit price (EGP) |
| `sold` | `int` | Total units sold |
| `borrowed` | `bool` | *(added dynamically)* Whether the book is currently checked out |
| `borrower_name` | `str` | *(added dynamically)* Name of current borrower |
| `days` / `due_day` | `int` | *(added dynamically)* Loan duration |
| `overdue` | `bool` | *(added dynamically)* Set on return if the loan exceeded 7 days |

> **Note:** The starter dataset in `library_data.py` includes ~295 pre-loaded titles across genres including Fiction, Classic, Fantasy/Sci-Fi, Horror, Action, and Poetry/Drama.

---

## Requirements

- **Python 3.8+**
- **Tkinter** (included with most standard Python installations; on some Linux distributions install via `sudo apt install python3-tk`)

No third-party packages are required — the project relies entirely on the Python standard library.

---

## Installation

1. Clone or download the project files into a single folder:
   ```
   main.py
   gui.py
   library_functions.py
   library_data.py
   ```
2. Confirm Python 3.8+ is installed:
   ```bash
   python --version
   ```
3. No further setup is required — there are no external dependencies to install.

---

## Usage

### Running the GUI

```bash
python gui.py
```

This launches the desktop application with four tabs:

| Tab | Purpose |
|---|---|
| **Manage Books** | Add/update/delete books, search by ID/author/year, view the full catalogue table |
| **Borrow / Return** | Check books in and out by ID |
| **Shop / Sales** | Purchase copies of a book and generate a receipt |
| **Statistics & Logs** | View catalogue statistics; import/export data as `.txt` |

All borrow, return, and sale actions are automatically logged with a timestamp to `transaction_log.txt` in the project directory.

### Running the CLI

```bash
python main.py
```

You'll be presented with a numbered menu:

```
==============================
   ZEWAIL CITY LIBRARY SYSTEM
==============================
1. Display all books
2. Search book by Title
3. Search books by Type
4. Add a new book
5. Borrow a book
6. Return a book
7. Show Library Statistics
8. Export/Save Data
9. BUY A BOOK
10. Show Books Sorted by Title
0. Exit
==============================
```

Enter the corresponding number and follow the prompts. Numeric fields (year, copies, price, IDs) are validated — invalid input is caught and reported without crashing the program.

---

## Module Reference

### `library_data.py`
Holds two module-level variables shared across the whole application:
- `library` — dictionary of all books, keyed by ID
- `current_id` — the next ID to assign when a book is added

### `library_functions.py`

| Function | Description |
|---|---|
| `add_book(...)` | Creates a new book entry and assigns it the next available ID |
| `delete_book(book_id)` | Removes a book by ID, returns the deleted record |
| `update_book(book_id, ...)` | Updates one or more fields of an existing book |
| `get_book(book_id)` | Retrieves a single book by ID |
| `search_book_by_title(title)` | Case-insensitive substring search across titles |
| `book_by_author(author)` | Returns all books by a given author |
| `book_by_year(year)` | Returns all books published in a given year |
| `search_books_by_type(library, wanted_type)` | Filters a supplied library dict by genre |
| `sort_books_by_title()` | Returns the catalogue sorted alphabetically |
| `count_books_by_type()` | Returns a genre → count breakdown |
| `library_stats(library)` | Prints total count, oldest/newest titles, and genre breakdown |
| `borrow_book(book_id, borrower_name, days)` | Marks a book as checked out |
| `return_book(book_id)` | Marks a book as returned, flags overdue loans (>7 days) |
| `buy_book(user_id, book_id, quantity, book_dict)` | Processes a sale, updates stock, generates a receipt |
| `generate_total(book, quantity)` | Calculates a purchase total |
| `import_book(file_path)` | Loads books from a delimited text file |
| `export_book(file_path)` | Writes the catalogue to a delimited text file |
| `display_all_books()` | Returns the full catalogue as a list |
| `clear_library()` | Empties the entire catalogue |

### `main.py`
Text-menu driver that wires user input to the functions in `library_functions.py`, with basic input validation and paginated output for large result sets.

### `gui.py`
Tkinter application (`LibraryApp` class) providing a tabbed interface over the same `library_functions.py` logic, plus:
- A `Treeview`-based catalogue table with live search/filter
- Timestamped activity logging via `log_transaction()`
- File dialogs for import/export

---

## Import / Export File Format

Books are exported and imported as plain comma-separated lines (no header row), matching this field order:

```
title,author,year,type_book,global_rating,copies,price,sold
```

**Example:**
```
The Hobbit,J.R.R. Tolkien,1937,Fantasy/Sci-Fi,4.3,1,12.5,0
```

> ⚠️ Field order and count must match exactly, or the corresponding line will be skipped during import.

---

## Transaction Logging

When using the GUI, every borrow, return, sale, and import operation is appended to `transaction_log.txt` in the project directory with a timestamp, e.g.:

```
[2026-07-04 14:32:07] Borrowed ID 12 to Ahmed
[2026-07-04 14:35:51] SALE: User Sara bought 2 of ID 8
[2026-07-04 14:40:03] Imported 42 books from new_titles.txt
```

This file is created automatically on first use and is not required to exist beforehand.

---

## Known Limitations

- **In-memory storage only** — all data resets to the hardcoded starter dataset in `library_data.py` each time the program restarts, unless manually exported/imported.
- **No concurrent access control** — the system is designed for single-user, single-session use.
- **Minimal input validation on import** — malformed lines in an import file are silently skipped rather than reported individually.
- **CLI and GUI cannot run simultaneously against the same live data** — each process holds its own copy of `library_data`.

## Roadmap

- [ ] Persist data automatically to disk (e.g. JSON or SQLite) instead of requiring manual export/import
- [ ] Add validation feedback for skipped rows during import
- [ ] Add authentication for multi-user borrowing scenarios
- [ ] Replace the flat-file format with a structured format (CSV with headers or JSON)

---

## License

This project is provided as-is for educational purposes. Add your preferred license (e.g. MIT) here before distribution.
