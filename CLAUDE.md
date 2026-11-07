# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Sports Centre Management System: a university group assignment (AMCS1034 Software Development Fundamentals). It's a Python tkinter desktop app with four modules, and each module is written and graded per author (see `README.txt` §5). Code is marked against a fixed rubric of 16 criteria × 4 modules (`Report Support/RUBRIC_CHECK.md`), so every module file must keep showing each criterion on its own.

## Commands

```
cd "Source Code"
python main.py                      # run the app (Python 3.10+ required: uses match)
python -m py_compile *.py           # compile-check every file
grep -nE "lambda |\[.* for .* in .*\]" *.py   # forbidden-syntax scan, must return nothing
```

There's no test framework. Tests are throwaway scripts that import the logic functions directly (`import membership; membership.register_member(...)`). Delete them afterward and put `data/*.txt` back to the clean sample state. The simplest reset is to delete `Source Code/data/`; the next run recreates it with fresh sample rows dated relative to today. Record executed cases in `Report Support/TEST_CASES.md`.

## Syllabus constraints (hard rules)

- **Standard library only, from a whitelist:** `tkinter`, `tkinter.messagebox`, `datetime`, `os`, `sys`. No `ttk`, no `calendar` (`common.days_in_month` exists to avoid it), and no other imports.
- **No lambdas and no comprehensions.** Use named nested functions for tkinter `command=` callbacks (see `make_day_command` in `common.py`) and plain `for` loops.
- **Each module file must show everything below on its own:** if/elif and `match`, `for` and `while` loops (the while loops are the `find_*_by_id` linear searches), a set, tuple and dict, a recursive function that the GUI actually calls (`count_*_recursive` / `total_*_recursive`), a class with private `__attr` plus getters/setters, inheritance (`Member`/`Coach` → `common.Person`, `RetailBill` → `Bill`), and try/except. Don't remove any of these. Don't add dead code just to satisfy the rubric either: graders check that it's wired to a button.
- **Comment style:** a header docstring in every file (Module/Author/Purpose/Date), a one-line docstring on every function, and `#` comments on non-obvious logic.
- **`main.py` must stay parseable on old Python.** It checks the version *before* importing the other modules and contains no `match` statement itself.

## Architecture

- **`common.py`** is shared by every module. It holds absolute data paths built from `__file__` (so the app runs from any cwd), domain constants (`SPORTS` courts/rates, `MEMBERSHIP_FEES`, `MEMBER_DISCOUNT_PCT`, opening hours, statuses), GUI style constants, file I/O helpers, `generate_id`, validators, the `open_date_picker` pop-up and the `Person` base class. Every module styles its window from the constants here.
- **Each module file has two layers.** The top half is pure logic: the class, `line_to_X`/`load_all_X`, and CRUD functions that `raise ValueError` on bad input. The bottom half is `build_X_tab(parent)`, which builds the module into a `tk.Frame`, catches `ValueError` in each handler and shows it through `messagebox`.
- **Every tab opens on an action menu, with one page per action.** This is the user's explicit design: the tab asks "What would you like to do?", and each action (Register, Book a Court, Pay Bill…) is its own simple page with one main button. `common.build_action_menu(window, title, [(name, menu_hint, page_instructions), ...])` returns `(page_frames, page_hooks)`. Build each page into `page_frames[name]`, and put its refresh function in `page_hooks[name]` (it runs whenever the page opens). Most actions use `common.build_pick_page(...)`, which shows a list on the left and the picked record's details plus ONE button on the right. The module supplies `load_rows(search_text)`, `describe(id)` and `action_function(id)` (which returns a message or raises `ValueError`), plus an optional form, confirm text and summary line. Form or picture pages (Register, Add Coach, Schedule Class, Create Bill, Book a Court, Hours & Commission, Daily Revenue) have their own `build_..._page`. Clicking the current tab again rebuilds it, which goes back to the menu. Each action list follows the assignment guideline's purpose for that module: Booking is a courts × hours grid; Membership is registration by type; Coaching assigns coaches to private/group classes and tracks hours and commission; Billing produces daily revenue split by court/coaching/retail/membership. Use the shared widgets in `common` (`make_button`, `make_card`, `make_option_menu`/`set_option_menu_choices`, `build_list_panel`, `add_form_row`).
- **Number input** from the GUI goes through `common.parse_decimal` / `parse_whole_number`. They give friendly messages, reject nan and inf (`float()` accepts both), and cap the range. Logic-layer checks are written as `not (low <= x <= high)` so nan fails them too.
- **One window, tabs.** `main.py` builds a single `Tk` with a tab bar of plain `tk.Button`s (no `ttk.Notebook`, since it's off the syllabus) above a content frame. `switch_to_tab` destroys the current tab's frame and rebuilds the chosen one with `if/elif`, so every switch reloads fresh data and clears half-typed input. Modules must never open their own `Toplevel` for the main UI. Anything that needs a real window must use `widget.winfo_toplevel()`: `transient` owners (see `common.open_date_picker`) and key bindings (see Membership's Enter key, which is guarded with `winfo_exists()`).
- **Storage is pipe-delimited `.txt`, one record per line**, in `Source Code/data/`. There's no in-memory cache. Every operation re-reads the file through `common.read_lines`, then writes it back with `write_lines` (update/delete) or `append_line` (create). Loaders use `common.split_fields(line, n)` and skip malformed lines. Free text must go through `common.contains_forbidden_character` (it rejects `|` and `;`), because class participants are stored as a `;`-joined list (`MEM001;MEM003`). Receipts are written one per payment to `data/receipts/`.
- **IDs:** `PREFIX###` (MEM, BKG, CCH, CLS, BIL). Each new ID is the highest existing suffix + 1.
- **Modules read each other's data files directly, not each other's Python functions.** `membership` reads bookings/bills to block deleting a member with a future CONFIRMED booking or an UNPAID bill. `coaching` reads members when enrolling. `billing` reads members (for the discount %), bookings and classes to build a bill. If you change a record format, every reader in every module has to change too.
- **Record field orders** are defined by each class's `to_line()`. The sample rows in `common.build_sample_rows` show each one.
- **Business rules to keep:**
  - Booking clashes are detected with set intersection of hours, and only CONFIRMED bookings count.
  - Daily revenue counts PAID bills only.
  - Cancelling a booking deliberately leaves its bill untouched, because refunds aren't in the syllabus.
  - Delete is only allowed on CANCELLED bookings and VOID bills.
  - A coach can't be deleted while any class (past or upcoming) references them, because IDs get reused. Changing a coach's sport also moves their upcoming classes to the new sport.
  - A booking or class can't be billed twice (`billing.billed_references`). Past dates can't be booked or scheduled.
  - Names allow letters, spaces, `/` and `'` (`common.is_valid_name`). Capitalisation goes through `common.format_name`, never `str.title()`, which would give "Ch'Ng".
- **The Booking grid** has courts as rows and hours as columns. Clicking adjacent free hours on one court builds a contiguous selection; past hours are grey. The grid redraws on `<KeyRelease>` once the date box holds a complete valid date. Pack layout gotcha: pack a bottom bar with `side="bottom"` *before* any sibling that uses `expand=True`, or it gets zero space and silently never shows (check with `winfo_ismapped()`).

## Verifying GUI changes

Reading the code isn't enough: past bugs (a NameError when opening a window, an invisible button bar, a grid not redrawing for a typed date) only showed up when the window was actually launched. To check a change, patch `tk.Tk.mainloop` to run a test function and call `main.main()`. Then drive the buttons with `.invoke()` (monkey-patch `messagebox` so the dialogs don't block) and check visibility with `winfo_ismapped()`. Call `root.update()` before looking for widgets, since nothing is mapped until it runs. Menu button names are reused as page button names (e.g. "Register", "Cancel Class"), so pick the last mapped match. Each action module exposes its action list (`BOOKING_ACTIONS`, `MEMBERSHIP_ACTIONS`, `COACHING_ACTIONS`, `BILLING_ACTIONS`) for tests to loop over. `PIL.ImageGrab` is installed; screenshot the window to check layout.

## Report Support docs

`Report Support/` holds the documents submitted with the code: rubric matrix, code explanation, flowcharts, test cases, audit report, AI usage log and user guides. When you change behaviour or a function signature, update `CODE_EXPLANATION.md`, `RUBRIC_CHECK.md` and `TEST_CASES.md` to match, and add an entry to `AI_USAGE_LOG.md` (the AI disclosure is required).
