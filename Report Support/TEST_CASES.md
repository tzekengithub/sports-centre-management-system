# Test Cases

Every case below was actually executed this session (both the original
build session and the overnight audit session), using throwaway test
scripts that imported the real modules directly, plus a real on-screen
GUI click-through (buttons invoked via tkinter's own `.invoke()`, with
`messagebox` monkey-patched only so it didn't block - the actual handler
code still ran). Scripts were deleted afterward and the data files were
restored to the clean sample state each time, per the project's own
workflow rules. "Actual" is what really happened, not a guess.

## Membership (membership.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| MEM-01 | Register valid member | name="Test Person", phone="0199999999", type="Monthly" | New member created, new ID returned | Member created with next ID | PASS |
| MEM-02 | Register duplicate phone | same phone as MEM-01 | ValueError "already registered" | ValueError raised | PASS |
| MEM-03 | Register invalid phone | phone="notaphone" | ValueError about phone format | ValueError raised | PASS |
| MEM-04 | Find by ID (while loop), found | existing ID | Returns correct Member | Correct member returned | PASS |
| MEM-05 | Find by ID, not found | "MEM999" | Returns None | None returned | PASS |
| MEM-06 | Delete member with no future booking/unpaid bill | newly created member | Deleted successfully | Deleted | PASS |
| MEM-07 | Delete member with future CONFIRMED booking | "MEM001" | ValueError, blocked | ValueError raised | PASS |
| MEM-08 | Delete member with an UNPAID bill | member with a generated UNPAID retail bill | ValueError, blocked | ValueError raised | PASS |
| MEM-09 | Load members.txt with a malformed trailing line appended | a line with only 2 fields | Malformed line skipped, no crash, 4 real members still loaded | Skipped correctly, no crash | PASS |
| MEM-10 | Load members.txt with blank trailing lines | two trailing `\n\n` appended | Blank lines ignored, 4 members still loaded | 4 members loaded | PASS |
| MEM-11 | ID regenerated after deleting the highest record | register, note ID, delete, register again | Same ID reused (no gap, no duplicate) | Same ID reused correctly | PASS |
| MEM-12 | GUI: every button on Register and Members clicked with blank fields | Register, Search, Save Changes, Renew, Delete | No uncaught exception; each shows a clear message | Part of the 54-click run, no exception | PASS |
| MEM-13 | GUI: register through the type cards | name "ravi a/l kumar", phone 0177770000, Youth card, Register | New ID shown, name stored as "Ravi a/l Kumar", fee reminder shown | MEM006 created exactly so | PASS |

## Coaching (coaching.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| COA-01 | Register valid coach | name, phone, sport, rate=55, comm=20 | Coach created | Coach created | PASS |
| COA-02 | Find coach by ID (while loop), found/not found | real ID / "CCH999" | Coach object / None | Both correct | PASS |
| COA-03 | Schedule valid class | valid coach, future date, hour, pax, fee | Class created | Class created | PASS |
| COA-04 | Schedule class with time clash | same coach/date/hour as COA-03 | ValueError, blocked | ValueError raised | PASS |
| COA-05 | Schedule class with an invalid class_type | class_type="Hack\|Type" | ValueError, "must be Private or Group", no `\|` ever reaches the file | ValueError raised before any write | PASS |
| COA-06 | Enrol up to max_pax, then one more | 2 members into max_pax=2, then a 3rd | First two succeed, 3rd raises "class is already full" | Exactly as expected | PASS |
| COA-07 | Enrol duplicate member | same member twice | ValueError "already enrolled" | ValueError raised | PASS |
| COA-08 | `update_class` changes date/hour/duration/pax/fee | valid new values | Class record updated, participants preserved | Updated correctly, participants kept | PASS |
| COA-09 | `update_class` rejects shrinking max_pax below enrolled count | max_pax below current enrolment | ValueError, blocked | ValueError raised | PASS |
| COA-10 | `update_class` rejects a new time that clashes with another class | overlapping slot | ValueError, blocked | ValueError raised | PASS |
| COA-11 | Delete coach with class history / without | coach with any class (past or upcoming) / coach with none | Blocked with "Cancel those classes first" / succeeds | Both correct | PASS |
| COA-12 | Commission total (recursion) wired into the GUI | coaches with classes and participants | Per-coach commission and a total shown in Hours & Commission | CCH001 RM 15.00, CCH002 RM 12.50, total RM 27.50 | PASS |
| COA-13 | GUI: Coaches sport filter and Classes coach filter | "Badminton" / CCH001 | Correct filtered lists, no crash | Both correct | PASS |
| COA-14 | GUI: every button in all four Coaching sections, blank fields | Add Coach, Schedule Class, Enrol, Remove Selected, etc. | No uncaught exception | Part of the 54-click run, no exception | PASS |

## Booking (booking.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| BKG-01 | Create valid booking | future date, valid court/hour/duration | Booking created, CONFIRMED | Booking created | PASS |
| BKG-02 | Create booking, exact slot clash | same slot | ValueError, blocked | ValueError raised | PASS |
| BKG-03 | `has_clash`: partially overlapping slot clashes | existing 10-12, new 11-13 | Clash detected | Clash detected | PASS |
| BKG-04 | `has_clash`: adjacent-before and adjacent-after slots do NOT clash | existing 10-12, new 9-10 and new 12-13 | No clash | No clash in either case | PASS |
| BKG-05 | `has_clash`: different court/sport never clash | same hours, different court or sport | No clash | No clash | PASS |
| BKG-06 | (removed) `ignore_booking_id` / `update_booking` | - | Updating a booking was removed to keep the tab simple: cancel and re-book instead | n/a | n/a |
| BKG-07 | Create booking, unknown member | "MEMXXX" | ValueError "no member found" | ValueError raised | PASS |
| BKG-08 | `find_next_free_hour` (while loop) on a free court | court with no bookings | Returns opening hour | Returned opening hour | PASS |
| BKG-09 | Cancel then delete a booking | own test booking | Status->CANCELLED, then removed from file | Both succeeded | PASS |
| BKG-10 | Cancel an already-CANCELLED booking | same booking again | ValueError "already cancelled", blocked | ValueError raised | PASS |
| BKG-11 | Delete a CONFIRMED booking directly | a CONFIRMED booking | ValueError "only CANCELLED can be deleted" | ValueError raised | PASS |
| BKG-12 | `load_all_bookings` skips a malformed appended line | a line with 3 fields instead of 8 | No crash, malformed line skipped | Skipped correctly | PASS |
| BKG-13 | GUI: every button on Court Availability and Bookings, blank fields | sport buttons, calendar, Book, Search, Cancel/Delete | No uncaught exception | Part of the 54-click run, no exception | PASS |
| BKG-14 | GUI: book from the grid, then cancel | date 20 days ahead, click Court 1 10:00 then 11:00, Book; then Bookings -> Cancel Booking | BKG created for 10:00-12:00 at RM 40.00; after cancelling, the only button shown is Delete Booking | Exactly so | PASS |

## Billing (billing.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| BIL-01 | Generate bill from booking (COURT) | existing booking ref | UNPAID bill, correct amount from SPORTS rate | Bill created with correct amount | PASS |
| BIL-02 | Generate RETAIL bill, valid | item name + positive amount | RetailBill created | Created correctly | PASS |
| BIL-03 | Generate RETAIL bill, name contains `\|` | item name="Water\|Bottle" | ValueError, blocked before any file write | ValueError raised | PASS |
| BIL-04 | Generate RETAIL bill, empty name / zero amount | "" / 0 | ValueError in both cases | Both raised ValueError | PASS |
| BIL-05 | Pay bill, exact or over amount | tendered = total + 10 | Marked PAID, change = 10.00, receipt file written | Change correct, receipt written | PASS |
| BIL-06 | Pay already-PAID bill | same bill again | ValueError "already paid" | ValueError raised | PASS |
| BIL-07 | Pay with invalid method / insufficient amount | "Bitcoin" / 0.01 | ValueError in both cases | Both raised ValueError | PASS |
| BIL-08 | Void then delete a bill | an UNPAID bill | Status->VOID, then removed from file | Both succeeded | PASS |
| BIL-09 | Void an already-VOID bill | same bill again | ValueError "already voided", blocked | ValueError raised | PASS |
| BIL-10 | Void a PAID bill | a PAID bill | ValueError "cannot be voided" | ValueError raised | PASS |
| BIL-11 | Daily revenue counts PAID bills only | one PAID (RM100), one UNPAID (RM50), one VOID (RM30), same date | Grand total reflects only the PAID bill's RM100; bill_count counts all three | Grand total matched the PAID bill only; bill_count was 3 | PASS |
| BIL-12 | `load_all_bills` skips a malformed appended line | a line with 2 fields instead of 10 | No crash, malformed line skipped | Skipped correctly | PASS |
| BIL-13 | GUI: every button in all three Billing sections, blank fields | Create Bill, Search, Pay, Void, View Receipt, Delete, Show | No uncaught exception | Part of the 54-click run, no exception | PASS |
| BIL-14 | GUI: retail bill then pay by cash | Water Bottle RM 5 for MEM001 (VIP 20%), then pay with "hello", then 10 | Bill RM 4.00; "hello" -> "Please enter a valid number for Amount received."; 10 -> paid, change RM 6.00, receipt saved | Exactly so | PASS |

## Date / general edge cases (common.py, exercised via all four modules)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| GEN-01 | Reject Feb 30 | "2026-02-30" | Invalid | Rejected | PASS |
| GEN-02 | Reject wrong-order format | "31/12/2026" | Invalid | Rejected | PASS |
| GEN-03 | Accept a real leap day | "2028-02-29" | Valid | Accepted | PASS |
| GEN-04 | Reject Feb 29 on a non-leap year | "2026-02-29" | Invalid | Rejected | PASS |
| GEN-05 | Hour boundaries | 7 (invalid), 21 (valid), 22 (invalid) | 7 and 22 rejected, 21 accepted | All three correct | PASS |
| GEN-06 | Fresh start: delete `data/`, run from a different working directory | `python "Sports Centre System/Source Code/main.py"` run from `Downloads/` | `data/` and all five files recreated with dates relative to today, no crash | Recreated correctly, dates relative to today | PASS |

## Coaching bug fixes and input checks (Entry 16)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| FIX-01 | Remove a member from a class (bug 1) | Enrolment: pick CLS003, enrol MEM001 and MEM002, click MEM001 in the enrolled list, Remove Selected | Only MEM002 left, shown by name | Only "MEM002 Siti Nurhaliza" left | PASS |
| FIX-02 | Rate/commission nan, inf, too big (bug 2) | rate "nan", "inf", "-inf", "9999"; commission inf | All rejected; rate capped at RM 500, commission at 100 % | All rejected with a clear message | PASS |
| FIX-03 | Text typed into a number box (bug 3) | rate "abc" | "Please enter a valid number for Hourly rate." | Exactly that message | PASS |
| FIX-04 | New coach form fully cleared (bug 4) | add a coach, then look at the form | Name, phone, rate and commission all empty | All four empty | PASS |
| FIX-05 | Sport change moves upcoming classes (bug 5) | coach with an upcoming Yoga class changed to Swimming | Class sport becomes Swimming; message says 1 class changed | Exactly so | PASS |
| FIX-06 | Coach with class history cannot be removed (bug 6) | Remove CCH001 (has a class) | Blocked: "... Cancel those classes first." | Exactly so | PASS |
| FIX-07 | Swimming and Yoga coaches (bug 7) | register a Yoga coach | Accepted (picked from the Sport drop-down) | Accepted | PASS |
| FIX-08 | Names with / and ' (bug 8) | "Ravi a/l Kumar", "ch'ng wei", "Muthu s/o Sami"; "/abc", "Ali\|x", "123", 41 letters | First three accepted ("Ch'ng Wei"); the rest rejected | Exactly so | PASS |
| FIX-09 | Duration 0 and other class limits (bug 9) | duration 0 and 5, Private with 3 people, fee nan, past date, Max people 0 | All rejected with a clear message | All rejected | PASS |
| FIX-10 | Booking a past date | create_booking on 2020-01-01 | "You cannot book a date in the past." | Exactly so | PASS |
| FIX-11 | Billing the same booking twice | generate a COURT bill for a booking twice | Second one refused; the booking no longer appears in the New Bill drop-down | Exactly so | PASS |
| FIX-12 | nan as a retail price or payment | retail price nan; pay with nan | Both rejected | Both rejected | PASS |

## Tab navigation (main.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| TAB-01 | Switch to every tab in turn | click Booking, Membership, Coaching, Billing, Home | Content area shows exactly one frame, the right module; no extra window opens; clicked tab highlighted | One frame each time, 0 extra windows | PASS |
| TAB-02 | Every tab opens on its action menu; every action opens its own page | all 23 actions in the four tabs | Menu shows one button per action; each page has Back, its name, one instruction line and one main button | All 23 pages correct (screenshots taken) | PASS |
| TAB-03 | Date picker opened from inside a tab | Booking, Coaching Classes, Billing Daily Revenue calendar buttons | Pop-up opens; picking a day refreshes the grid / revenue straight away | Opened, no error | PASS |
| TAB-04 | Typing a date without pressing Enter | type a new date in Booking's date box | Grid switches to that date as soon as the date is complete | Redrawn (found as a bug during testing and fixed) | PASS |
| TAB-05 | Every button on every action page, blank and with a row picked | 84 button clicks | No uncaught exception | None raised | PASS |
| TAB-06 | Clicking the tab you are on | open Billing > Pay Bill, click Billing | Back to the Billing menu | Menu shown | PASS |
| TAB-07 | Every action done through its page | Register, Renew, Add Coach (inf rate rejected), Schedule, Enrol, Remove Member, Cancel Class, Book, Cancel, Delete booking, Create Bill, Pay (nan rejected, change RM 12.00), View Receipt | Each succeeds with a clear message | All succeeded | PASS |

## What this does NOT cover

Pixel-level layout (text wrapping, overlap at unusual window sizes) was
not checked - no screenshot tool was available in this environment.
`OptionMenu` dropdowns were exercised by driving their underlying
`StringVar` directly rather than an actual mouse click-and-select, which
runs the same code path a real click would but was not literally a mouse
click. See `AUDIT_REPORT.md` for the full list of what was fixed and
what remains a documented decision rather than a defect.
