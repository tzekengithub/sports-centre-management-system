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
| MEM-11 | ID not reused after deleting the highest record | register, note ID, delete, register again | Next number is used; the deleted ID is never handed out again (changed in Entry 22) | New ID one higher | PASS |
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
| BKG-09 | Cancel a booking | own test booking | Status -> CANCELLED and the booking stays in bookings.txt (deleting bookings was removed in Entry 21) | Exactly so | PASS |
| BKG-10 | Cancel an already-CANCELLED booking | same booking again | ValueError "already cancelled", blocked | ValueError raised | PASS |
| BKG-11 | (removed) deleting a booking | - | No delete exists any more: cancelled bookings are kept on record | n/a | n/a |
| BKG-12 | `load_all_bookings` skips a malformed appended line | a line with 3 fields instead of 8 | No crash, malformed line skipped | Skipped correctly | PASS |
| BKG-13 | GUI: every button on Court Availability and Bookings, blank fields | sport buttons, calendar, Book, Search, Cancel Booking | No uncaught exception | Part of the 54-click run, no exception | PASS |
| BKG-14 | GUI: book from the grid, then cancel | date 20 days ahead, click Court 1 10:00 then 11:00, Book; then Bookings -> Cancel Booking | BKG created for 10:00-12:00 at RM 40.00; after cancelling it disappears from Cancel a Booking but stays in bookings.txt as CANCELLED | Exactly so | PASS |

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

## Manage Coaches page (Entry 18)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| MC-01 | Blank form adds a coach | Ch'ng Lee, 0189990000, rate "abc" then 45, commission 15 | "abc" -> "Please enter a valid number for Hourly rate."; 45 -> CCH003 added, every field empty again | Exactly so | PASS |
| MC-02 | Clicking a row loads it for updating | click Lim Wei's row | Form filled, row highlighted, button reads Save Changes, New shown | Exactly so | PASS |
| MC-03 | Save changes | rate 60 -> 65, Save Changes | "Coach CCH001 saved." | Exactly so | PASS |
| MC-04 | Delete beside a coach with classes | Delete on CCH001's row | Blocked: "... Cancel those classes first." | Exactly so | PASS |
| MC-05 | Delete beside a coach without classes | Delete on CCH003's row | Deleted; row disappears | Only CCH001 and CCH002 left | PASS |

## Manage Classes and Manage Members pages (Entry 19)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| MC-06 | Blank form schedules a class | date 20 days ahead, max people 0 then 5, fee 30 | 0 -> "Max people must be between 1 and 30."; 5 -> CLS003 scheduled | Exactly so | PASS |
| MC-07 | Clicking a class row loads it, coach and type locked | click CLS003 | Date, max people and fee filled; coach drop-down and both type buttons disabled | Exactly so | PASS |
| MC-08 | Save and Delete a class | fee 30 -> 35, Save Changes; Delete on its row | "Class CLS003 saved." then "Class CLS003 deleted." | Exactly so | PASS |
| MC-09 | Manage Members starts with no form | open the page | Only the search box shown; title "Click a member to edit them" | Exactly so | PASS |
| MC-10 | Edit a member with a bad phone | click Siti, phone 12345, Save Changes | "Phone must be 10-11 digits and start with 01." | Exactly so | PASS |
| MC-11 | Delete beside a member | Ahmad Faiz (upcoming booking) / a new member with nothing outstanding | Blocked / deleted | Both correct | PASS |
| MC-12 | Summary under the member list | open Manage Members | Total, members per type, expiring in 30 days | "5 members (Annual 2, Monthly 1, Pay-As-You-Go 1, VIP 1). 2 expiring in the next 30 days." | PASS |

## Hover hints and units (Entry 20)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| TIP-01 | Every interactive widget has a hover hint | every button, entry, drop-down and radio button on Home, every menu and every action page (rows clicked too) | none without a hint | 306 checked, none missing | PASS |
| TIP-02 | Hint timing and text | rest on a past and a free grid square | nothing at 0.2 s; at 0.7 s "Court 1, 08:00-09:00: this time has already passed." / "...: free, RM 20.00 for this hour. Click to select it ..." | Exactly so | PASS |
| TIP-03 | Hint closes | move the mouse away; click a button | hint closes both times | Closed | PASS |
| UNIT-01 | Booking grid columns show hours | open Book a Court | column labels 08:00, 09:00, ... 21:00 under "Start time"; info line says "free 1-hour slots" | Exactly so | PASS |
| UNIT-02 | Units in lists and forms | coach list, class list, bill list, coach and class forms | RM/hour, Comm %, People, Total RM, Hourly rate (RM/hour), Commission (%), Max people (1-30), Fee per person (RM), durations in hours | All shown | PASS |

## Exit warning, kept bookings, dark mode (Entry 21)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| EXIT-01 | Exit tab asks first | click Exit, answer No | "Are you sure you want to exit..." shown; program stays open | Exactly so | PASS |
| EXIT-02 | Window X asks first | close the window, answer No | Same question; program stays open | Exactly so | PASS |
| EXIT-03 | Exit after Yes | click Exit, answer Yes | Program closes | Closed | PASS |
| BKG-15 | No way to delete a booking | open Booking | Actions are only Book a Court and Cancel a Booking; `delete_booking` no longer exists | Exactly so | PASS |
| DARK-01 | Switch to dark mode keeps your place | on Coaching, click Dark Mode | Whole window redrawn dark, still on Coaching; data/settings.txt says theme=dark | Exactly so | PASS |
| DARK-02 | No light-coloured leftovers | visit every menu and page (rows clicked) and the calendar pop-up in dark mode | No widget with a white/light background or black text | None found | PASS |
| DARK-03 | Choice remembered | restart after choosing dark | Starts in dark mode | load_theme_choice() returned dark | PASS |
| DARK-04 | Every button in dark mode, blank fields | crash run with theme=dark | No uncaught exception | None raised | PASS |

## Tester's fixes T1-T13 (Entry 22)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| T1-01 | Duplicate coach phone on add | add a coach with an existing coach's phone | Rejected: phone already used | Rejected | PASS |
| T1-02 | Duplicate coach phone on update | change a coach's phone to another coach's | Rejected; keeping their own phone is allowed | Exactly so | PASS |
| T1-03 | Search classes by sport | Manage Classes, search "ten" | Only Tennis classes | Exactly so | PASS |
| T1-04 | Search Enrol by coach name / Remove by member name | type part of a name | Matching rows only | Exactly so | PASS |
| T1-05 | Hours & Commission names and search | open the page, search a coach name | Coach name is the first column; search shows only that coach | Exactly so | PASS |
| T1-06 | ID column headers | open class, coach, member, booking, bill lists | Headers read Class ID / Coach ID / Member ID / Booking ID / Bill ID | Exactly so | PASS |
| T2-01 | Date saved in standard form | schedule a class on 2026-12-7 | Saved as 2026-12-07; clash with a class typed 2026-12-07 still found | Exactly so | PASS |
| T3-01 | Start hour already passed today | schedule a class / book a court today at an hour that has begun | Rejected: already started | Rejected | PASS |
| T4-01 | File can't be saved | data file path is a folder | Friendly "Could not save ..." message, no crash | Exactly so | PASS |
| T5-01 | Damaged line kept | add a broken line to classes.txt, then update a class | Broken line still in the file | Kept | PASS |
| T6-01 | ID never reused | delete CLS900 (newest), schedule a class | New class is CLS901 | CLS901 | PASS |
| T7-01 | Fee rounds before the minimum check | fee 0.004 | Rejected (rounds to 0.00) | Rejected | PASS |
| T8-01 | Large totals | 3000 classes and 3000 bills | Totals worked out, no RecursionError | Exactly so | PASS |
| T9-01 | File saved with a BOM | members.txt starting with a BOM | First member still read; next ID doesn't restart at 001 | Exactly so | PASS |
| T10-01 | Enrol in a past class | enrol_participant on a class dated yesterday | Rejected: already taken place | Rejected | PASS |
| T11-01 | Private class member | Manage Classes, Private, pick a member, Schedule | Member row shown only for Private; class saved with that member (1/1) | Exactly so | PASS |
| T12-01 | Labelled details | click a row on any pick page | Lines like "Class ID:   CLS001", "Sport:      Tennis" | Exactly so | PASS |
| T13-01 | Long names cut | a member named Nurul Aisyah binti Abdullah | List shows the name ending in "…" | Exactly so | PASS |
| T-ALL | Every button, blank fields | crash run (77 clicks) | No uncaught exception | None raised | PASS |

## Tester's second round B1-B16, G1-G11 (Entry 23)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| B1-01 | Sample IDs learnt at start | fresh data folder | id_counters.txt has CLS 2 | CLS 2 | PASS |
| B1-02 | Deleted sample ID not reused | counter file removed, delete CLS001, schedule | New class is CLS003 | CLS003 | PASS |
| B1-03 | Class with a bill can't be deleted | delete CLS002 (bill BIL002) | Refused, names BIL002 | Refused | PASS |
| B2-01 | Fix a past class's fee | update a class dated yesterday, fee 30 | Saved | Saved (SUPERSEDED in Entry 28: now refused, see N2-01) | PASS then |
| B2-02 | Can't move a class into the past | change its date to 2 days ago | Refused | Refused | PASS |
| B3-01 | Class already started today | enrol into a class starting this hour | Refused; class not in the Enrol list | Exactly so | PASS |
| B4-01 | Delete question lists members | Delete beside CLS001 | Question says 2 members and names them | Exactly so | PASS |
| B5-01 | Member time clash | enrol MEM002 in two overlapping classes | Second refused, names the first class | Refused | PASS |
| B6-01 | Expired member | enrol a member whose membership ended yesterday | Refused; not in the member drop-down | Exactly so | PASS |
| B7-01 | Member in an upcoming class | delete MEM003 (in CLS001) | Refused, names CLS001 | Refused | PASS |
| B8-01 | Only finished classes count | report with one past and two upcoming classes | Worked = the past class; upcoming hours shown separately; Pay = hours x rate | Exactly so | PASS |
| B9-01 | Private session, bad member | schedule Private for an expired member | Refused, no empty class saved | Exactly so | PASS |
| B9-02 | Private session saved in one write | schedule Private for MEM004 | Class saved with MEM004 already in it | Exactly so | PASS |
| B11-01 | Sport change asks first | change CCH001 to Squash, answer No | Question gives class counts; nothing saved | Exactly so | PASS |
| B12-01 | Coach with upcoming classes | delete CCH001 | Refused | Refused | PASS |
| B12-02 | Coach with only past classes | delete after their upcoming class is gone | Kept as INACTIVE; can't be given a new class | Exactly so | PASS |
| B12-03 | Coach with no classes | add a coach, delete them | Deleted | Deleted | PASS |
| B12-04 | Old coach lines | coaches.txt with 6 fields | Loaded as ACTIVE | Loaded | PASS |
| B15-01 | Coach file can't be saved | coaches.txt read-only, change sport | Friendly error; classes.txt unchanged | Exactly so | PASS |
| B16-01 | Counter can't be saved | id_counters.txt read-only, add coach | Friendly error; coaches.txt unchanged | Exactly so | PASS |
| G1-01 | Long instructions wrap | open Manage Classes | Instruction text wraps to the window width | Exactly so | PASS |
| G2-01 | Pages fit the window | measure Manage Coaches/Classes, Enrol, Hours, Book a Court, Create Bill, Manage Members | All at most 1000 px wide (widest 995 px) | Exactly so | PASS |
| G3-01 | Long names in drop-downs | coach Nurul Izzah binti Abdullah (Swimming) / long member name | Name cut with ..., sport still shown, at most 24 characters | Exactly so | PASS |
| G4-01 | Find box | type "nurul" next to the Enrol member list | Only the matching member is listed | 1 entry | PASS |
| G5-01 | New class date | open Manage Classes | Date box shows tomorrow | Exactly so | PASS |
| G6-01 | Past classes greyed | class dated yesterday | Row shown in the grey past colour; note under the list | Exactly so | PASS |
| G7-01 | Calendar month and past days | type a date 45 days ahead, open the calendar; then today | Opens on that month; days before today disabled | Exactly so | PASS |
| G8-01 | Mouse wheel | pointer over a Manage list | Wheel is bound while the pointer is over the list | Bound | PASS |
| G9-01 | Long details | name of 39 characters in a details panel | Wraps onto a second line, nothing cut | Exactly so | PASS |
| B-ALL | Every button, blank fields | crash run (107 clicks) | No uncaught exception | None raised | PASS |

## Tester's Booking round (Entry 24)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| BK1-01 | Long member name | Find "haziq" (MEM090 Muhammad Haziq bin Abdullah Rahman), pick an hour, Book | Booked for MEM090 | Booked | PASS |
| BK1-02 | Same in Create Bill | Find "haziq" in Create Bill | Their booking listed, Create Bill enabled | Exactly so | PASS |
| BK2-01 | Nobody pre-selected | open Book a Court, pick an hour | Member shows "(choose one)", Book disabled | Exactly so | PASS |
| BK3-01 | Date box changed without redraw | change the box, click Book | Not booked; message, grid redrawn | Exactly so | PASS |
| BK3-02 | Box left after a change | type a date, focus leaves | Grid shows that date | Exactly so | PASS |
| BK4-01 | Expired member | book for a member who expired yesterday | Refused; not in the drop-down | Exactly so | PASS |
| BK4-02 | Booking after expiry | MEM001 (ends in 10 days), date in 400 days | Refused | Refused | PASS |
| BK5-01 | Past booking | cancel BKG050 dated yesterday | Refused; not in the Cancel list | Exactly so | PASS |
| BK6-01 | Billed booking | cancel / reschedule a booking with a PAID bill | Refused, names the bill | Exactly so | PASS |
| BK7-01 | Duplicate booking IDs in the file | two lines BKG060 | Lists still load | No crash | PASS |
| BK8-01 | Typing a date | 9 characters typed | Grid not redrawn yet | Exactly so | PASS |
| BK9-01 | Back and reopen | change date, Back, reopen | Today's date, no member picked | Exactly so | PASS |
| BK10-01 | Partial search | "mem00", a first name, "2026-11" | Matches part of ID / name / date | Exactly so | PASS |
| BKG1-01 | Free count today | today, after some hours passed | Past hours not counted as free | Exactly so | PASS |
| BKG5-01 | Past date | yesterday | "has passed, so it can't be booked" | Exactly so | PASS |
| BKG2-01 | View All | open View All Bookings | Cancelled and past bookings listed with status | Exactly so | PASS |
| BKG3-01 | Dark mode selected cell | select an hour | ✓ in dark text on amber | Exactly so | PASS |
| BKG4-01 | Cancel list columns | open Cancel a Booking | Header as wide as rows; member name shown | Exactly so | PASS |
| BKR1-01 | Reschedule | BKG002 to opening hour; clash; past date; past closing; bad court | Saved; the rest refused, booking unchanged | Exactly so | PASS |
| BKR2-01 | Day sheet | Save Day Sheet for a day with 2 bookings | File in data/day_sheets lists both, total 3 hours | Exactly so | PASS |
| BK-ALL | Every button, blank fields | crash run (104 clicks) | No uncaught exception | None raised | PASS |

## Tester's coaching round N1-N11, U1-U5 (Entry 28)

Two older results changed: **B2-01** (a past class's fee can be fixed) is
now refused, because a class that has started is a record (N2); and the
booking and class messages for a PAID bill changed, because a PAID bill
can never be voided.

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| N1-01 | Move a class past a member's expiry | class with a member whose membership ends in 5 days, move it 10 days ahead | Refused: "membership ends"; class unchanged | Exactly so | PASS |
| N1-02 | Move inside the membership | move to day 3 | Saved | Saved | PASS |
| N1-03 | Move or lengthen into the member's other class | second class at 13:00, move to 10:00, or start 09:00 for 2 hours | Refused, names the other class | Exactly so | PASS |
| N1-04 | Size-only change | max people 8 to 12 | Saved, no member check | Saved | PASS |
| N2-01 | Started class edit | fee, or size, of a class dated yesterday | Refused "already started"; unchanged | Exactly so | PASS |
| N2-02 | Billed class | change fee / duration of a class with an UNPAID bill | Refused, names the bill | Exactly so | PASS |
| N2-03 | Billed class, size only | max people 8 to 10 | Saved | Saved | PASS |
| N3-01 | Inactive coach delete | delete a coach twice | First: kept as INACTIVE. Second: "already inactive ... stay on record"; the confirm box says it too | Exactly so | PASS |
| N4-01 | Started class delete | delete a class dated yesterday | Refused; still in classes.txt | Exactly so | PASS |
| N5-01 | Remove a member with a bill | member with a PAID bill for that class | Refused, names the bill | Exactly so | PASS |
| N5-02 | Remove without a bill / from a started class | | Removed / refused | Exactly so | PASS |
| N5-03 | Remove page | open it | Started classes not listed; the page says why | Exactly so | PASS |
| N7 | Class vs court booking overlap | | Not checked: a class does not book a court in this system (out of scope, noted in the report) | n/a | n/a |
| N9-01 | Bad class rows | duration 0 and -2, max people 0, sport Chess, date 2026-02-30, Private for 3, hour 23, fee -5 and nan | Each loads as None (hidden) | All None | PASS |
| N9-02 | Unpadded date | 2027-1-5 | Loads as 2027-01-05 | Exactly so | PASS |
| N9-03 | Bad row kept | bad row in the file, then an enrol rewrite | Row still in classes.txt, hidden in the lists | Exactly so | PASS |
| N10-01 | Paid class / booking | delete a class or cancel/move a booking whose bill is PAID | Message says a paid bill can't be voided, so it is kept as a record | Exactly so | PASS |
| N10-02 | Billing void rule | void a PAID bill | "A PAID bill cannot be voided." (confirmed) | Exactly so | PASS |
| U1-01 | Month with nothing worked | Hours & Commission, pick a month that has only upcoming classes | "Nothing worked yet in this month." | Exactly so | PASS |
| U2-01 | Member hint | Manage Classes, choose Private | Hint under the Member box; hidden for Group | Exactly so | PASS |
| U4-01 | Stale list | a class starts while Enrol is open; click Enrol | Error shown, and the list reloads without that class | Exactly so | PASS |
| U5-01 | Laptop height | Manage Classes, Private form, default 1000 x 610 window; calendar pop-up | Nothing cut off; pop-up on screen | Fits with about 40 px spare | PASS |
| N11-01 | Header | all six files | `Member N: name (student ID: ____)` line | Present (IDs to fill in) | PASS |

## Dark mode keeps your place (Entry 27)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| DM-01 | Same page after switching | Membership > Register, type a name, click Dark Mode | Still on Register; typed name still there; button reads Light Mode; choice saved | Exactly so | PASS |
| DM-02 | Same colours as a fresh dark start | all 18 pages: switch in place, then compare every widget's colour options with a window started in dark mode | No differences | 2,807 widgets compared, 0 differences | PASS |
| DM-03 | Round trip | light > dark > light on all 18 pages | Every widget back to its original colours | 0 mismatches | PASS |
| DM-04 | Selected booking hour | pick an hour, switch | Still selected, amber with dark text; grid redraw after the switch uses dark colours | Exactly so | PASS |
| DM-05 | Highlighted list row | click a coach row, switch, click another row | Highlight kept; old row returns to the dark panel colour (not stale light) | Exactly so | PASS |
| DM-06 | Hover hint | theme button hint | Follows the current theme | Function-based hint, follows the theme | PASS |

## Rubric round: Record parent class and full re-run (Entry 26)

The logic cases of the sections above (MEM, COA, BKG, BIL, GEN, FIX) were
re-run on 2026-11-10 by one script that imports the real modules on a
fresh `data/` folder: **86 checks, 0 failed.** The script also covers the
new cases below. Cases that need real clicks (MEM-12/13, COA-13/14,
BKG-13/14, BIL-13/14) were not repeated click for click; the pages they
exercise are covered by the GUI suites (Entries 23-25: 18, 26 and 21
checks) and by a click-every-button run with blank fields (159 clicks, no
uncaught exception).

Cases whose **expected result changed** since they were first written
(the old text above is kept as history):

| Old case | Old expectation | Now |
|---|---|---|
| COA-11, FIX-06, MC-04 | a coach with any class is blocked | blocked only with *upcoming* classes; a coach with only past classes becomes INACTIVE (Entry 23, B12) |
| BKG-06/11 | removed earlier | still removed; bookings can now be rescheduled (Entry 24) |
| BIL-06 | message quoted as "already paid" | the message reads "This bill has already been paid." (unchanged code, shorthand in the old text) |

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| INH-01 | Booking and SportsClass inherit Record | `issubclass(...)` | Both True | Both True | PASS |
| INH-02 | Inherited getter | `get_record_id()` and `get_booking_id()` on BKG777 | Both "BKG777" | Both "BKG777" | PASS |
| INH-03 | Blank ID refused | `Record(" ")` | ValueError "blank" | ValueError | PASS |
| INH-04 | Parent `to_line` is abstract | `Record("X1").to_line()` | NotImplementedError | Raised | PASS |
| INH-05 | File text unchanged | every line of the sample bookings.txt and classes.txt loaded then saved with `to_line()`, plus 3 extra lines | Identical text | 0 differences | PASS |
| INH-06 | Blank ID in a data line | `line_to_booking("\|MEM001\|...")` | Line skipped (None), like other malformed lines | None | PASS |
| DT-01 | Days left on a membership | MEM002 | A positive number; "N day(s) left" in the details | Exactly so | PASS |
| DT-02 | Class date offset | class two days ahead | "in 2 day(s)" beside the date | Exactly so | PASS |
| RC-01 | Fresh start from another folder | delete `data/`, launch `main.py` by full path from the temp folder | Window builds; five data files, id_counters.txt and receipts/ recreated | Exactly so | PASS |

## Search-as-you-type member box (Entry 25)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| CB-01 | Starts empty | open Book a Court | Box shows "(choose one)"; no list | Exactly so | PASS |
| CB-02 | Type to search | click the box, type "haziq" | List drops down with only that member | 1 row | PASS |
| CB-03 | Click a row | click it | Member picked (name cut with ...), list closes | Exactly so | PASS |
| CB-04 | Arrow lists everyone | click the arrow; click again | All valid members listed; closes | Exactly so | PASS |
| CB-05 | No match / Esc | type "zzzz", press Esc | "No match"; box goes back to the last pick | Exactly so | PASS |
| CB-06 | Enter | type "siti", Enter | First match picked | Exactly so | PASS |
| CB-07 | Partial text can't book | type "sit" with hours chosen | Book disabled until a real pick | Exactly so | PASS |
| CB-08 | List removed with the page | open the list, click the Booking tab | No list left on screen | Exactly so | PASS |
| CB-09 | Billing and Coaching | pick a member in Create Bill, a coach in Manage Classes | Both picked | Exactly so | PASS |

## Tab navigation (main.py)

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| TAB-01 | Switch to every tab in turn | click Booking, Membership, Coaching, Billing, Home | Content area shows exactly one frame, the right module; no extra window opens; clicked tab highlighted | One frame each time, 0 extra windows | PASS |
| TAB-02 | Every tab opens on its action menu; every action opens its own page | all 17 actions in the four tabs | Menu shows one button per action; each page has Back, its name, one instruction line and one main button | All 23 pages correct (screenshots taken) | PASS |
| TAB-03 | Date picker opened from inside a tab | Booking, Coaching Classes, Billing Daily Revenue calendar buttons | Pop-up opens; picking a day refreshes the grid / revenue straight away | Opened, no error | PASS |
| TAB-04 | Typing a date without pressing Enter | type a new date in Booking's date box | Grid switches to that date as soon as the date is complete | Redrawn (found as a bug during testing and fixed) | PASS |
| TAB-05 | Every button on every action page, blank and with a row picked | 84 button clicks | No uncaught exception | None raised | PASS |
| TAB-06 | Clicking the tab you are on | open Billing > Pay Bill, click Billing | Back to the Billing menu | Menu shown | PASS |
| TAB-07 | Every action done through its page | Register, Renew, add coach (inf rate rejected), Schedule, Enrol, Remove Member, Cancel Class, Book, Cancel, Delete booking, Create Bill, Pay (nan rejected, change RM 12.00), View Receipt | Each succeeds with a clear message | All succeeded | PASS |

## Home header, multi-book and partial cancel (2026-11-11 re-run)

On a fresh `data/` folder, the logic cases of the sections above were
re-run by one script that imports the real modules (**119 checks, 0
failed**), and the GUI cases by a second script that drives the real
window with `.invoke()` (**55 checks, 0 failed**). They cover MEM-01 to
MEM-11 and MEM-13, COA-01 to COA-12, BKG-01 to BKG-10, BKG-12 and BKG-15,
BIL-01 to BIL-12, GEN-01 to GEN-05, FIX-02/03/05 to FIX-12, INH-01 to
INH-04 and INH-06, T1/T2/T3/T6/T7/T9/T10, B1-03, B7-01, N1-01, N2-01,
N4-01, N5-02, N9-01/02, N10, BK4-02, BK6-01, BKR1/BKR2, TAB-01/02/05/06,
DM-01/03, DARK-03, EXIT-01 to EXIT-03 and TIP-01 (Home page only).
**Not repeated this time** (they need typed text, timing or a read-only
file, so their earlier results still stand): MEM-12, COA-13/14,
BKG-13/14 (replaced by BKG-16 to BKG-21 below), BIL-13/14, TIP-02/03,
UNIT, the CB, DM-02/04/05 and T4/T5/T8/B15/B16/G/BK1-BK10 GUI cases, and
the coaching GUI cases FIX-01/04, MC-01 to MC-12, U1 to U5. Two script
mistakes were fixed while writing the re-run (a sample member whose
membership ends in 10 days, and a pop-up left open by the click-through);
the program code needed no change.

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| HOME-01 | Greeting by hour | `greeting_text` for 0, 4, 5, 11, 12, 17, 18, 23 | Evening, Evening, Morning, Morning, Afternoon, Afternoon, Evening, Evening | Exactly so | PASS |
| HOME-02 | Date text | 2026-11-11 and 2026-01-05 | "Wednesday - Nov 11, 2026" and "Monday - Jan 5, 2026" (no leading zero on the day) | Exactly so | PASS |
| HOME-03 | Header shows | open the program | Greeting, ADMIN label, welcome line, three shortcut buttons, clock card | All shown (screenshot checked, light and dark) | PASS |
| HOME-04 | Clock ticks | read the time label twice, 3.2 s apart; again when started from another folder | The time changes | 09:53:15 AM then 09:53:18 AM; the other run also changed | PASS |
| HOME-05 | Shortcut buttons | click Book a Court, Register Member, Create Bill | Each opens its own page; the tab menu is hidden | All three landed on the right page | PASS |
| HOME-06 | Dark mode on the header | click Dark Mode on Home | Greeting, clock card and buttons recolour at once | Greeting #2f6f4e to #7fd1a6, clock card #272c34 with text #e6e8eb (first, plain header; the canvas header is covered by HOME-10, HOME-15 and HOME-16) | PASS |
| HOME-07 | Fits the window | 1000 x 610 window | No widget past the window edge | None past the edge | PASS |
| HOME-08 | Clock stops with its page | switch tabs many times and close the program | No error from the 1-second timer | 0 uncaught exceptions | PASS |
| HOME-09 | Hover hints | every button on Home | A hint for each | No plain button on Home without one (the three rounded shortcut buttons get theirs from `add_tooltip` in `PillButton`) | PASS |
| BKG-16 | Book separate hours in one go | pick 10:00, 11:00 and 15:00 on Court 1 and 12:00 on Court 2, Book | 3 bookings: Court 1 10-12, Court 1 15-16, Court 2 12-13 | 3 bookings created | PASS |
| BKG-17 | Multi-book is all or nothing | pick a free hour on Court 2 plus a taken hour on Court 1 | Refused; nothing saved | Refused; Court 2 hour not saved | PASS |
| BKG-18 | Partial cancel (Cancel page) | book 10-14, cancel 11:00 until 13:00 | 11-13 CANCELLED under the original ID; 10-11 and 13-14 new CONFIRMED bookings | BKG004 11-13 CANCELLED, BKG005 10-11 and BKG006 13-14 CONFIRMED | PASS |
| BKG-19 | Cancel one hour from the grid | click a red hour of a 10-14 booking, answer Yes | Only that hour cancelled; the grid shows it free again | 11-12 CANCELLED, 10-11 and 12-14 kept; 4 red squares became 3 | PASS |
| BKG-20 | Cancel range checks | hours outside the booking, an empty range, an already cancelled booking | Each refused | All refused | PASS |
| BKG-21 | Grid click speed | click two free squares | No redraw of the whole grid | 7 to 11 ms per click; both squares show the tick | PASS |
| HOME-10 | Restyle: shapes | open Home in Dark and Light Mode | Dot + greeting + pill badge; rounded buttons (one filled with a glow, two outlined with a symbol); rounded clock card with glowing HH : MM : SS, AM label, date and GMT label | All shown; `Report Support/home_dark.png` and `home_light.png` | PASS |
| HOME-11 | No flicker | read the canvas item ids and count 2.3 s apart | Same items; only their text changed | Same ids, same count | PASS |
| HOME-12 | Time zone text | UTC offsets +8, 0, -5, +5:30, -3:30 | GMT+8, GMT, GMT-5, GMT+5:30, GMT-3:30 | Exactly so | PASS |
| HOME-13 | Button states | mouse over, press, leave on Book a Court | Colour changes on hover and press; leave restores it | Exactly so | PASS |
| HOME-14 | Keyboard | focus Create Bill, press Enter and Space | The button's command runs each time; all three canvases take focus | Exactly so | PASS |
| HOME-15 | Theme toggles | Dark / Light 6 times in a row | No error; canvas item count the same each time in the same theme (no leftovers) | Same count per theme; no exception | PASS |
| HOME-16 | Shortcuts in both themes | Book a Court, Register Member, Create Bill in Light and in Dark | Each opens its own page; menu hidden | Exactly so | PASS |
| HOME-17 | Narrow window | make the window 760 px wide (the program itself stops at 1000) | Clock card drops below the buttons; no overlap; inside the window | Exactly so (screenshot checked) | PASS |
| HOME-18 | Back to 1000 x 610 | widen again | Clock card beside the buttons, no overlap | Exactly so | PASS |

Known cosmetic difference found while checking dark mode (it was there before
this change): after Light > Dark > Light, the amber "today" button in the
calendar pop-up keeps dark text instead of white.

## What this does NOT cover

Pixel-level layout (text wrapping, overlap at unusual window sizes) was
not checked - no screenshot tool was available in this environment.
`OptionMenu` dropdowns were exercised by driving their underlying
`StringVar` directly rather than an actual mouse click-and-select, which
runs the same code path a real click would but was not literally a mouse
click. See `AUDIT_REPORT.md` for the full list of what was fixed and
what remains a documented decision rather than a defect.

The Home page was screenshotted in light and dark mode on this machine
(1000 x 610 window); other display scaling (125 %, 150 %) was not checked.


## Drop-down list stays inside the window

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| DD-01 | Box at the bottom of the page | Book a Court, click the arrow / type "member" (34 members) | List opens upward, fully inside the window; picking a row works | Exactly so | PASS |
| DD-02 | Very short window | window 330 px high, click the arrow | Fewer rows shown, list still inside the window | Exactly so | PASS |
| DD-03 | Box near the top | Manage Classes coach box | Still opens downward, inside the window | Exactly so | PASS |
| DD-04 | Narrow window | Create Bill in a 900 px window | List inside the window | Exactly so | PASS |


## Booking colours and badges

| ID | Description | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| CL-01 | Row colours | View All Bookings | CONFIRMED upcoming green, CANCELLED red, started grey | Exactly so | PASS |
| CL-02 | Badges | pick a paid / unbilled / unpaid / cancelled / started booking | CONFIRMED or CANCELLED; UPCOMING or STARTED / PAST; PAID (green), NOT BILLED (amber), UNPAID (red); a cancelled booking's NOT BILLED is grey | Exactly so for all five | PASS |
| CL-03 | Dark mode | switch with a row picked | Rows and badges recoloured in place; selection kept; a newly picked cancelled booking is red | Exactly so | PASS |
| CL-04 | Cancel / Reschedule pages | open each, pick a booking | Green rows and 3 badges | Exactly so | PASS |
| CL-05 | All pages after the switch | compare every widget with a fresh dark start | No differences | 2,942 widgets, 0 differences | PASS |
