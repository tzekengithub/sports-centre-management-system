# Morning Summary — Overnight Audit

## 1. What happened, in plain terms

Ran 3 audit passes (stopped early — pass 3 found nothing new, so passes
4-5 would have just re-confirmed that). **18 issues found and fixed**: 6
High, 9 Medium, 3 Low. The 5 most important:

1. **The program would break if run from any folder other than `Source
   Code/`** — paths were relative to the current directory, not to
   main.py's own location. Fixed.
2. **A hand-edited or corrupted data file crashed the whole program**
   (one bad line in `members.txt` and "View All" would throw an
   exception). Every loader now skips a malformed line instead.
3. **Free-text fields could corrupt the data files** — a retail item
   name or a class type typed with a `|` character would silently break
   the pipe-delimited format on the next save. Both are now validated.
4. **Deleting a member only checked for future bookings, not unpaid
   bills** — a member who owed money could still be deleted. Fixed.
5. **A real bug I introduced myself while fixing something else** — a
   leftover variable reference crashed the Coaching window the instant
   it opened. Only caught because I actually launched the window on the
   real screen and clicked through it, not by reading the code. This is
   the strongest argument for why "launch main.py and click through
   it yourself" at the bottom of this file matters — static review
   missed this one.

Also fixed along the way: clicking a menu button twice opened two
windows instead of one; the daily revenue total was counting cancelled
and unpaid bills as if they were collected money; a recursive function
existed only to satisfy the rubric and was never actually called; coach
and class search only worked on one hardcoded field even though the
spec asks for several; there was no way to edit a scheduled class's own
details at all (only enrol/remove participants). Full list with
file:function detail is in `AUDIT_REPORT.md`.

## 2. Rubric marking simulation

Full 16-criteria × 4-module matrix is in `RUBRIC_CHECK.md`. Every cell
has function-level evidence after the fixes above. My honest estimate,
marking the way a strict lecturer would (deduct when unsure):

| Criterion | Marks | Estimated |
|---|---|---|
| Selection | 5 | 5 |
| Loop | 5 | 5 |
| String processing | 3 | 3 |
| File processing | 5 | 5 |
| Collections - list | 3 | 3 |
| Collections - set/tuple/dict | 3 | 3 |
| Predefined modules | 3 | 3 |
| User-defined functions (+recursion) | 3 | 3 |
| Encapsulation | 5 | 5 |
| Inheritance | 3 | 3 |
| GUI design | 5 | 4 (see note below) |
| GUI implementation | 3 | 3 |
| Exception handling | 5 | 5 |
| Comments - single-line | 3 | 3 |
| Comments - multi-line | 3 | 3 |
| Execution | 3 | 3 |
| **Total** | **60** | **59** |

The one point held back: Coaching's form reuses the same 9 fields for
both the coach and class forms (labels swap depending on view). It's
functional, consistent, and now clearly labelled, but a strict marker
could still call a shared form "less immediately obvious" than two
separate ones. This was a pre-existing design choice, not something
introduced tonight — rebuilding it into two separate forms was judged
out of scope for an audit-and-fix pass (see the "decisions made without
asking" section of `AUDIT_REPORT.md`). Everything else should be
defensible at full marks given the evidence in `RUBRIC_CHECK.md`.

## 3. What I could NOT verify — click through this yourself

Every button in every module was clicked programmatically on the real
screen tonight (via tkinter's own `.invoke()`, which runs exactly the
same code a mouse click would) with both blank and valid data, and that
caught the real bug in item 5 above. What that method cannot cover:

1. **Pixel-level layout** — text wrapping, overlap, whether anything
   looks cramped at an unusual window size. No screenshot tool was
   available. Open each of the four module windows and the main menu
   and just look at them.
2. **Actual mouse clicks on `OptionMenu` dropdowns** (Sport, Membership
   Type, Bill Category, Payment Method, the two "Search by" dropdowns
   in Coaching). These were exercised by setting their underlying value
   directly in code, which runs the same handler a real selection would
   — but click each dropdown open and pick a different option at least
   once to be sure the mouse interaction itself feels right.
3. **The full demo script in order**, as a dry run for the
   presentation: open Booking → check the Grid for Badminton on
   `BKG001`'s date (should show court 2 booked 18:00-20:00) → make a new
   booking → open Membership → register a member → open Coaching →
   switch to Class Management → schedule a class → enrol the member you
   just registered → open Billing → generate a bill from that class →
   Pay it → check the Revenue summary for today. Expected result at each
   step: no error dialogs except where you deliberately typed something
   invalid, and each screen reflecting the previous screen's changes
   immediately (the program always reloads from the data files, so
   nothing should look stale).

## 4. Remaining Low items / decisions you may want to reverse

All documented with reasoning in `AUDIT_REPORT.md`'s "Decisions made
without asking" section:
- Booking/Billing use a `Text` widget for results; Membership/Coaching
  use a `Listbox`. Both are allowed by the brief; left as-is.
- Cancelling a booking or class does not touch any bill already
  generated against it (no refund logic — not in the syllabus).
- `main.py` no longer contains a `match` statement (moved the version
  check ahead of it) — the four graded modules still each have one, so
  this costs nothing on the rubric.

## 5. Run command and backup location

Run command: `python main.py` from `Sports Centre System\Source Code\`
(or from anywhere else — see fix #1 above).

Backup of the project **before** tonight's audit touched anything:
`C:\Users\user\Downloads\SportsCentre_BACKUP_20261105_015158\`
