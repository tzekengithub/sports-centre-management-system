# Morning Summary - inheritance gap and rubric check (Entry 26)

## 1. What I changed

| File | Function / class | Change, in plain English |
|---|---|---|
| `common.py` | new `class Record` | A small parent class: keeps a record's ID private (`get_record_id`, validating `set_record_id`), builds the start of every saved line (`join_fields`) and has an abstract `to_line()`. |
| `booking.py` | `class Booking(common.Record)` | Now inherits. `super().__init__(booking_id)` stores the ID, `get_booking_id()` returns the inherited `get_record_id()`, `to_line()` overrides the parent and calls the inherited `join_fields()`, so the parent code really runs on every save. |
| `coaching.py` | `class SportsClass(common.Record)` | Same pattern as Booking. |
| `membership.py` | `days_until_expiry`, `days_left_text` | New: uses `datetime` directly (it only used it through `common` before). Shown as a "Days left" line in the member details. `try/except ValueError/else`. |
| `coaching.py` | `days_until_class`, `class_when_text` | New: uses `datetime` directly, shown beside the class date ("2026-11-12 (in 2 day(s))"). `class_when_text` also gave coaching.py its first function with `if/elif/else` together. |
| `billing.py` | `read_receipt` | Now `try/except OSError/else`: an unreadable receipt gives a plain message instead of a crash. |
| `membership.py` | `renew_member`, `delete_member` | Added multi-line `#` comment blocks (the file had one). |
| `Report Support/RUBRIC_CHECK.md` | whole file | Rebuilt as the 16 x 4 matrix from a scan of the code. Several old claims were wrong (e.g. functions said to have if/elif/else that had none) and are corrected. |
| `README.txt` | sections 2, 3, 5, 7 | Windows and macOS/Linux run commands, folder layout (day_sheets, id_counters, settings), new "Where each rubric criterion appears" table. |
| `CODE_EXPLANATION.md`, `CLAUDE.md`, `TEST_CASES.md`, `AI_USAGE_LOG.md` (Entry 26) | | Updated to match. |

No data-file format changed. I did not rename any function or change any message-box text. `FLOWCHARTS.md` mentions no classes, so it needed no change.

## 2. The 16 x 4 matrix (one line each; full text in `RUBRIC_CHECK.md`)

| # | booking.py | membership.py | coaching.py | billing.py |
|---|---|---|---|---|
| 1 Selection | if/elif/else `draw_grid`; match `search_bookings` | if/elif/else `duration_text`; match `search_members` | if/elif/else `class_when_text`; match `search_coaches`, `apply_class_type` | if/elif/else `show_detail_row`; match `generate_bill`, `search_bills` |
| 2 Loop | for `build_availability_grid`; while `find_next_free_hour`, `find_booking_by_id` | for `load_all_members`; while `find_member_by_id` | for `load_all_coaches`; while `find_coach_by_id` | for `load_all_bills`; while `find_bill_by_id`, `bill_rows_with_status` |
| 3 String | `search_bookings` strip/lower; `day_sheet_text` | `search_members`; `format_name` | `get_participant_list` split `;`; `get_time_text` | `bill_rows_with_status` f-string; `unbilled_classes` split |
| 4 File | read `load_all_bookings`; write `create_booking`, `cancel_booking`; own `open()` in `save_day_sheet` | read `load_all_members`; write `register_member`, `update_member` | read `load_all_classes`; write `schedule_class`, `update_coach` | read `load_all_bills`; write `pay_bill`, `write_receipt` |
| 5 List | `booking_list`, `grid` | `member_list` | `class_list`, `participant_list` | `bill_list` |
| 6 Set/tuple/dict | set `has_clash`; tuple `SEARCH_FIELDS`; dict `load_member_names` | set `get_phone_set`; tuple `MEMBERSHIP_TYPES`; dict `count_members_by_type` | set `participant_set`; tuple `CLASS_TYPES`; dict `coach_hours_by_month` | set `billed_references`; tuple `BILL_CATEGORIES`; dict `category_totals` |
| 7 Predefined modules | `datetime.now` in `day_sheet_text`; `os` in `save_day_sheet` | `datetime` in `days_until_expiry` | `datetime` in `days_until_class` | `datetime`, `os` in `write_receipt` |
| 8 Recursion (called by GUI) | `count_free_slots_recursive` | `count_members_recursive` | `total_commission_recursive` | `total_bills_recursive` |
| 9 Encapsulation | `Booking` | `Member` | `Coach`, `SportsClass` | `Bill` |
| 10 Inheritance | `Booking(Record)` | `Member(Person)` | `Coach(Person)`, `SportsClass(Record)` | `RetailBill(Bill)` |
| 11 GUI design | action menu, grid, hover hints | action menu, type cards | action menu, search boxes | action menu, live preview |
| 12 GUI complete | 4 pages | 3 pages | 5 pages | 6 pages |
| 13 Exceptions | `save_day_sheet` try/except/else/finally | `days_until_expiry` try/except/else | `update_coach` try/except OSError (rollback) | `read_receipt` try/except/else |
| 14 Single-line comments | yes | yes | yes | yes |
| 15 Multi-line comments | header + 6 `#` blocks | header + 3 `#` blocks | header + 6 `#` blocks | header + 4 `#` blocks |
| 16 Execution | runs from any folder; fresh `data/` recreated | same | same | same |

**Cells I could not make strong (also listed in `RUBRIC_CHECK.md`):**
- **Row 4, membership / coaching / billing:** they read and write files only through the shared `common` helpers, not their own `open()`. This matches the teacher's example, but if your marker wants `open()` in every module file, that is a group decision.
- **Row 13, `finally`:** only booking.py has one, because only it opens a file itself. The others use `else` but not `finally`; closing happens inside `common.write_lines`.
- **Row 13, shared handlers:** most membership and billing buttons are built by `common.build_pick_page` / `build_manage_page`, so the visible `try/except` for them is in common.py.

## 3. Test results (run 2026-11-10, for real)

| Suite | Result |
|---|---|
| Re-run of the logic cases from `TEST_CASES.md` (MEM, COA, BKG, BIL, GEN, FIX) plus the new inheritance cases | 86 checks, 0 failed |
| Entry 23 logic suite / Entry 24 logic suite | 27 / 20 checks, 0 failed |
| Combo-box GUI suite / Booking GUI suite | 21 / 26 checks, 0 failed |
| Click every button with blank fields | 159 clicks, no uncaught exception |
| Fresh start: delete `data/`, launch `main.py` by full path from another folder | window builds; all files and `receipts/` recreated |
| Data files before/after | every sample booking and class line loads and saves back identical (0 differences) |
| Forbidden syntax scan (lambda, comprehensions, bare `except:`) | none |

**Behaviour changes:** a data line with a *blank ID* is now skipped like any malformed line (before it loaded). Three old test cases (COA-11, FIX-06, MC-04) expect a result that changed earlier, in Entry 23; this is recorded in `TEST_CASES.md`.

**Not re-run exactly:** the click-for-click GUI cases MEM-12/13, COA-13/14, BKG-13/14, BIL-13/14 were covered by the newer GUI suites and the 159-click run, not repeated step for step. My Entry 23 GUI script crashes in its old Find-box section (that box was replaced); its first 15 checks pass and the combo-box suite covers the rest.

## 4. What I could NOT verify (do these yourself)

The screen was off, so nothing was looked at; widths were measured, not seen.
1. Run `python main.py`, click **Booking > Book a Court**, click the member box, type `siti`, and check the list drops down under the box and is readable (also in **Dark Mode**).
2. Click the **▼** arrow: everyone should be listed and the list should close on a second click.
3. **Membership > Manage Members**, click a member: the details should show a **Days left** line.
4. **Coaching > Manage Classes**, click a class: the Date line should read like `2026-11-12 (in 2 day(s))` and not be cut off.
5. **Billing > View Receipt** on a paid bill: the receipt should show as before.
6. Look at the pages at your real Windows display scaling (I measured 100% only).

## 5. Run command and backup

- Windows: `cd "Sports Centre System/Source Code"` then `python main.py`
- macOS / Linux: `python3 main.py` (Python 3.10 or newer; no libraries to install)
- **Backup of the whole project from before this work:** `C:\Users\user\Downloads\SportsCentre_BACKUP_20261110_101922\` (outside the project folder).
- **Your `data/` folder:** I put back your real data (not the sample data) because it holds a real member's details; it is not in git. The app adds `id_counters.txt` next time it starts.
- The final tree is `Source Code/`, `README.txt`, `Report Support/`, plus `CLAUDE.md` and `.gitignore`, which the repository already had.
