# Audit Report — Overnight "Strict Lecturer" Pass

Three audit passes were run against the working code (reading every file
fresh, then actually executing logic-layer tests and a real on-screen
GUI click-through with `messagebox` monkey-patched to avoid blocking).
Pass 3 found zero new High/Medium issues, so the loop stopped there
rather than mechanically running to 5 — further passes would only have
re-confirmed the same clean result.

## Pass 1 findings (12 fixed)

| # | Severity | File:function | Problem | Fix applied | Status |
|---|---|---|---|---|---|
| 1 | High | common.py (module paths) | Data paths were relative to the current working directory, so running `python main.py` from anywhere other than `Source Code/` would read/write `data/` in the wrong place. | Paths now built from `os.path.dirname(os.path.abspath(__file__))`. | Fixed |
| 2 | High | all `line_to_*` / loader functions | A malformed line (wrong field count, e.g. from manual editing or a half-written row) crashed `load_all_*` with an `IndexError`/`ValueError`, taking down "View All" and every screen that calls it. | Added `common.split_fields()` (returns `None` on wrong field count) and wrapped each conversion in try/except; malformed lines are now skipped. | Fixed |
| 3 | High | billing.generate_bill (RETAIL) | Retail item name was never validated — an empty name, a zero/negative amount, or a name containing `\|` (which would corrupt the pipe-delimited file) were all accepted. | Added checks: non-empty, no `\|`/`;`, amount > 0. | Fixed |
| 4 | High | coaching.schedule_class (class_type) | `class_type` came from a free-text Entry with no validation — any string, including one containing `\|`, was written straight into classes.txt. | Restricted to a `("Private", "Group")` whitelist. | Fixed |
| 5 | High | membership.delete_member | Checked for future confirmed bookings but not unpaid bills, so a member with money owed could still be deleted. | Added `has_unpaid_bill()` check. | Fixed |
| 6 | High | main.py | `match` statements need Python 3.10+, but a file containing `match` fails to even *parse* on older Python — so a runtime version check inside those files is impossible; the whole import would SyntaxError first. | Rewrote main.py so the version check runs, and shows a friendly messagebox, *before* importing any module that contains `match`; main.py itself no longer uses `match`. | Fixed |
| 7 | Medium | main.py / all four `open_*_window` | Clicking a menu button twice opened two independent copies of the same module window. | main.py now tracks open windows per module and brings the existing one to the front instead of opening a second copy; each `open_*_window` now returns its window. | Fixed |
| 8 | Medium | booking.py (price preview) | Price preview was refreshed on `sport_menu`'s `<Configure>` event, which does not reliably fire when the OptionMenu selection changes. | Switched to `sport_variable.trace_add("write", ...)`. | Fixed |
| 9 | Medium | booking.cancel_booking / billing.void_bill | Cancelling an already-CANCELLED booking, or voiding an already-VOID bill, silently "succeeded" a second time instead of telling the user nothing changed. | Both now raise a clear ValueError on the second attempt. | Fixed |
| 10 | Low | booking.has_clash / coaching.coach_has_time_clash | Overlap test had a redundant duplicate condition (`start_hour < existing_end_hour and existing_end_hour > start_hour` — the same comparison written twice). | Simplified to the standard two-condition overlap test. | Fixed |
| 11 | Low | all file opens | No explicit encoding, so text files opened with whatever the OS's default codepage is — a non-ASCII member name could read back differently on another machine. | All file opens now use `encoding="utf-8"` (and `newline="\n"` on write/append). | Fixed |
| 12 | Low | common.py (sample data) | Sample dates were hardcoded strings; useful today but would silently drift into the past (making the booking/class update/cancel demo impossible) on any machine running the project after those dates pass. | Sample data is now generated relative to `today_string()` every time it's (re)created, so bookings/classes are always safely in the future. | Fixed |

## Pass 2 findings (4 fixed)

| # | Severity | File:function | Problem | Fix applied | Status |
|---|---|---|---|---|---|
| 13 | High | coaching.py (introduced by my own pass-1 edit) | Renaming `labels_text` into `coach_labels_text`/`class_labels_text` left one leftover reference (`stats_label.grid(row=len(labels_text), ...)`), which raised `NameError` the instant the Coaching window opened. **Caught only because the window was actually launched on a real display and clicked through — reading the code did not catch it.** | Fixed the stale reference. | Fixed |
| 14 | Medium | coaching.py (recursion requirement) | `total_commission_recursive` was defined (to satisfy the "one recursive function per module" rubric row) but never called from the GUI — exactly the "recursion added only to tick a box" anti-pattern the brief warned against. | Wired it into the Coach Management stats panel, which now shows each coach's scheduled hours *and* commission earned. | Fixed |
| 15 | Medium | coaching.py (GUI completeness) | The module spec requires searching coaches by id/name/sport and classes by coach/date/sport/type, but the GUI only ever searched coaches by name and classes by sport — the other fields were unreachable even though the logic functions supported them. | Added a dedicated "Search by" dropdown (one for each view) plus a "Search text" field, replacing the hardcoded single-field search. | Fixed |
| 16 | Medium | coaching.py (GUI completeness) | The spec requires "update **and** cancel/remove a class" — but there was no way to change a scheduled class's date/hour/duration/fee/max_pax at all, only enrol/remove participants or cancel it outright. | Added `update_class()` (re-checks the coach's time clash, refuses to shrink `max_pax` below the current enrolment) and an "Update Class" button. | Fixed |
| 17 | Medium | billing.daily_revenue_summary | Totals summed bills of *any* status, including VOID (cancelled) and UNPAID ones — so "revenue" included money that was never collected, or was explicitly cancelled. | Grand total and category totals now count PAID bills only; `bill_count` still reports every bill issued that day for context. GUI wording updated to say "revenue collected" explicitly. | Fixed |
| 18 | Low | coaching.Coach.to_line | Commission percent was written with plain `str(float)`, so a seed value of `30` silently became `30.0` the first time any unrelated coach record was rewritten (e.g. after deleting a different coach) — correct value, inconsistent formatting. | Now formatted as `.2f` like every other money/percentage field. | Fixed |

## Pass 3

Full fresh re-read of coaching.py and billing.py (the two most heavily
patched files), plus a complete re-run of: `py_compile` on every file, a
23-case logic-layer edge-case suite (malformed lines, `\|`/`;` injection,
empty files, blank trailing lines, ID regeneration after deleting the
highest record, double-cancel/double-void, leap-year dates, hour
boundaries, revenue semantics), and a real on-screen click-through of
every button in all four modules with both blank and valid field values.
**Zero new High/Medium issues found.** The loop was stopped here rather
than continuing to passes 4-5, since another full pass would only
re-verify the same clean result at no further benefit.

## Decisions made without asking (documented per the brief's instruction)

- **Coaching module's form reuses the same 9 fields for both the coach
  form and the class form**, with labels that swap depending on which
  view is active (`update_field_labels()`). This was an existing design
  choice from the original build, not something introduced tonight; it
  was kept rather than rebuilt into two separate forms, since rebuilding
  it was out of scope for an audit-and-fix pass and the swapped labels
  make each field's purpose unambiguous on screen.
- **Booking/Billing use a `Text` widget for results; Membership/Coaching
  use a `Listbox`.** The original brief allows either ("monospace Listbox
  or Text widget"). Booking needs `Text` for the multi-line availability
  grid and Billing needs it for the multi-line revenue summary, so this
  was left as-is rather than forcing one widget type everywhere.
- **Cancelling a booking or a class does not touch any bill already
  generated against it.** There is no refund/credit-note logic in the
  syllabus, so a PAID bill for a since-cancelled booking is left exactly
  as it was — "sensible" was read as "does not crash or corrupt data,"
  not "implements refund accounting."
- **main.py no longer uses a `match` statement** (it dispatches with a
  tiny set of named functions instead). This was necessary so the
  Python-version check could run and show a friendly message *before*
  Python tries to parse a `match` statement on an incompatible
  interpreter — removing it from main.py has no rubric cost, since the
  four graded modules (booking/membership/coaching/billing) still each
  have a genuine `match` statement.
- **`has_future_confirmed_booking`/`has_unpaid_bill`-style cross-file
  checks read the raw text file directly** (not through the other
  module's `load_all_*`) to avoid one module importing another's
  internals; each check applies the same malformed-line guard as the
  loaders.

## What still could not be verified end-to-end

- The click-through tests invoked every button's `command` callback
  directly via `.invoke()`, which is how a real click behaves, but did
  not verify pixel-level layout (text wrapping, overlap at unusual
  window sizes) since no screenshot tool was available in this
  environment. A human should still eyeball each window once.
- `OptionMenu` selection via mouse (as opposed to setting the underlying
  `StringVar` directly) was not exercised, since `.invoke()` on an
  `OptionMenu` opens its dropdown rather than selecting an item. The
  price-preview `trace_add` fix and the coaching search-field dropdowns
  were instead verified by driving the `StringVar` directly, which
  triggers the same code path a real selection would.
