# AI Usage Log

Tool used: Claude Code (Anthropic), one continuous build session.

## Entry 1 - Shared base
- **Asked:** Build the whole Sports Centre Management System in one run:
  `common.py` shared helpers/constants/Person class, following a strict
  syllabus whitelist/blacklist and a fixed file layout.
- **Produced:** `common.py` with file I/O helpers (`read_lines`,
  `write_lines`, `append_line`), `generate_id`, validators, GUI style
  constants, and the `Person` base class; plus embedded sample data for
  all five `.txt` files.
- **Verify:** Confirm the sample data in `data/*.txt` matches what you
  want to demo, and that `is_valid_phone`'s rule (01, 10-11 digits)
  matches what your lecturer expects for "Malaysian phone number".

## Entry 2 - Membership, Coaching, Booking, Billing logic + GUI
- **Asked:** Write all four module files (logic layer + tkinter GUI) per
  the module specifications, each with CRUD lifecycle, a recursive
  function, a class with encapsulation, and inheritance where specified.
- **Produced:** `membership.py`, `coaching.py`, `booking.py`, `billing.py`
  with the functions listed in `CODE_EXPLANATION.md`.
- **Verify:** Each member should read through their own file line by
  line and be ready to explain any function in Q&A - these were written
  by AI from a spec, not from the group's own design discussions.

## Entry 3 - main.py integration
- **Asked:** Build the main menu window with a `match`-statement dispatch
  to the four module windows.
- **Produced:** `main.py`.
- **Verify:** Confirm the menu button labels and order match what the
  group agreed on for the presentation.

## Entry 4 - Verification and syllabus compliance fix
- **Asked:** Run `py_compile` on every file, test every logic function
  with valid/invalid/edge inputs, and scan for forbidden syntax
  (comprehensions, lambda, etc.).
- **Produced:** All files compiled cleanly; the test run caught that the
  first draft used `lambda` in four places and two list comprehensions -
  these were rewritten as named functions and plain `for` loops. The test
  run also caught that no module had a genuine `while` loop (the spec
  requires both `for` and `while` per module) - this was fixed by adding
  a while-loop-based linear-search/scan function to each module (member/
  coach/bill lookup-by-ID, and next-free-hour), each wired to a real GUI
  button rather than left as dead code.
- **Verify:** Re-run the forbidden-syntax grep yourself before
  submission (`grep -nE "lambda |\[.* for .* in .*\]"` over `Source
  Code/*.py`) in case a later edit reintroduces something off-syllabus.
  Also click through every button in every module window at least once -
  this session could only compile-check and logic-test the code, not
  click through the GUI interactively.

## Entry 5 - Report support documents
- **Asked:** Produce `RUBRIC_CHECK.md`, `CODE_EXPLANATION.md`,
  `FLOWCHARTS.md`, `TEST_CASES.md`, `USER_MANUAL_OUTLINE.md` and this log.
- **Produced:** All five documents plus this log, based on the actual
  code written and the actual logic-layer test run (see
  `TEST_CASES.md`'s note on what was and wasn't executed).
- **Verify:** Take the screenshots listed in `USER_MANUAL_OUTLINE.md`
  yourself; the AI could not capture screenshots of the running GUI in
  this environment.

## Entry 6 - Overnight strict-lecturer audit and fix pass
- **Asked:** Role-play a hostile lecturer/tester/syllabus-checker, find
  every problem by actually reading and running the code (not just
  reading), fix each one, and re-audit from scratch until a full pass
  found nothing left to fix (section 4 of the audit prompt); work
  autonomously without asking questions.
- **Produced:** Three audit passes. Pass 1 fixed 12 issues: paths that
  broke when run from outside `Source Code/`, malformed-data-file crash
  risk in every loader, unvalidated free text that could corrupt the
  pipe-delimited files (retail item name, class type), a member-delete
  check that ignored unpaid bills, a Python-version crash that happened
  *before* any version-check code could run (fixed by removing `match`
  from main.py and deferring the other imports), duplicate module
  windows opening on a second click, an unreliable price-preview
  trigger, missing double-cancel/double-void guards, and a few Low
  cosmetic cleanups. Pass 2 found and fixed 6 more, including one real
  bug introduced by my own Pass-1 edit (a `NameError` on opening the
  Coaching window, caught only because the window was actually launched
  on the real display and clicked through, not just read), a recursive
  function that existed only to satisfy the rubric but was never called
  by the program, two GUI completeness gaps against the written module
  spec (class/coach search only worked on one hardcoded field; there was
  no way to update a scheduled class's own details at all), and a
  revenue total that counted cancelled and unpaid bills as if they were
  collected money. Pass 3 (full fresh re-read of the two most-patched
  files, plus a 23-case edge-case suite and a real on-screen click
  of every button in all four modules) found nothing new.
- **Verify:** Read `Report Support/AUDIT_REPORT.md` in full - it lists
  every finding with its severity and the exact fix, plus the design
  decisions I made without asking (why main.py dropped its `match`
  statement, why cancelling a booking doesn't touch its bill, etc.).
  Confirm you agree with those decisions before submission; they were
  reasonable calls under the "don't ask, just fix" instruction, not
  things the group discussed.

## Entry 7 - First-time-use friendliness pass
- **Asked:** "When I first use the system I don't know how to use it,
  can you make the system user friendly" - the written guides existed
  as separate files, but the running program itself gave no in-app
  guidance.
- **Produced:** A one-time welcome dialog that appears automatically
  the very first time the program is ever run (detected via
  `ensure_data_files_exist()` now returning whether it just created a
  fresh install), explaining the four modules and how screens work.
  A permanent "How to Use This System" button on the main menu brings
  that same message back any time. Each of the four module windows got
  a "Help" button explaining every field and every button on that
  specific screen in plain English (Coaching's Help message switches
  content depending on whether you're in the Coach or Class view).
  All done with `messagebox.showinfo`, so it stays inside the taught
  toolkit.
- **Verify:** Click "How to Use This System" on the main menu and each
  module's "Help" button yourself to confirm the wording matches what
  your group wants to say in the demo; the text can be freely edited
  in each file's `on_help`/`WELCOME_MESSAGE` without touching any logic.

## Entry 8 - Interactive booking grid
- **Asked:** "Make the forms like dropdown so I can select available
  ones, or make it interactive - select sport, visualise the courts,
  see a calendar of availability, click the available space to book."
- **Produced:** Court No changed from a free-text field to a dropdown
  that rebuilds itself to list exactly the courts that exist for
  whichever sport is selected (no typing a court number that doesn't
  exist). The "Grid" button now renders the availability table as
  actual clickable `tk.Button` cells instead of plain text - green
  "Free" cells book that exact hour/court immediately when clicked
  (after a confirmation dialog, using the Member ID and Duration
  already in the form), red "Booked" cells show which booking occupies
  them. Both built with plain tkinter widgets (Button, OptionMenu,
  Frame) - no new modules, no `ttk`, no lambdas.
- **Verify:** Click through it yourself - pick a sport, click Grid,
  book a free slot, and confirm the grid redraws showing it as booked.
  One design note: the Grid and Book buttons both call the exact same
  `create_booking` logic function, so results are identical either way
  - typing fields manually still works for anyone who prefers it.

## Entry 9 - Step-by-step booking wizard
- **Asked:** "Make it interactive and step by step, I don't want a
  boring form" - matching the earlier description (date, then sport,
  then court, then a calendar, click to book).
- **Produced:** Booking now opens to a landing screen with two paths.
  "Book a Court" is a 4-step wizard (date+member -> big sport buttons
  -> big court buttons -> a per-court hour calendar you click to book),
  built from plain Frames shown/hidden with `pack()`/`pack_forget()`.
  "Manage Existing Bookings" keeps the classic search/update/cancel/
  delete form, since editing a record by its ID doesn't suit a wizard.
- **Caught and fixed a real bug while testing:** the manage screen's
  button bar was being packed *after* two sibling frames that use
  `expand=True`, so by `pack()`'s cavity-allocation order it was given
  zero space and silently never rendered, even though `.pack()` ran
  without error. Confirmed via `winfo_ismapped()` on the real window,
  not by reading the code - the bug produced no exception, so a
  code-only review would have missed it. Fixed by packing the button
  bar first (`side="bottom"`) so it reserves its space before the
  expanding content claims the rest.
- **Verify:** Walk through the wizard yourself once, including the
  Back/Change Date buttons at every step - the automated test clicked
  every button and checked the right widgets became visible via
  `winfo_ismapped()`, but did not evaluate layout aesthetics.

## Entry 10 - Calendar date picker
- **Asked:** "Let me choose a calendar, like how Google Forms does it,
  when selecting the date."
- **Produced:** `common.open_date_picker(parent, target_entry)` - a
  reusable pop-up calendar (month/year header with `<`/`>` navigation,
  a `Today` shortcut, a grid of day buttons) built entirely from plain
  tkinter widgets. Month lengths are computed from `datetime` subtraction
  rather than importing the `calendar` module, since that module is not
  on the syllabus's allowed list. Wired to a 📅 button next to every
  manually-typed date field: the booking wizard's Step 1, the Manage
  Bookings screen, Coaching's class Date field (shown only in Class
  view, since that field is "Hourly Rate" in Coach view), and Billing's
  Revenue date field.
- **Verify:** Click a 📅 button yourself and try the month-navigation
  arrows near a year boundary (e.g. December -> January) - this was
  tested programmatically and rolled over the year correctly, but a
  visual check never hurts.

## Entry 11 - Click-slots-for-duration (removed the 1h/2h/3h/4h buttons)
- **Asked:** "No need to set 1h/2h buttons - if you want 2h, just click
  two slots, simple as that."
- **Produced:** Removed the duration-picker buttons entirely.
  `wizard_state["selected_hours"]` now tracks a growing list of clicked
  hours: clicking a free hour selects it (turns amber); clicking
  another free hour immediately adjacent to the current selection
  extends it; clicking a non-adjacent free hour starts a fresh
  selection there instead (a booking must be one contiguous block);
  clicking an already-selected hour clears the whole selection so you
  can restart. A "Book Selected" button (disabled until something is
  selected) confirms and creates the booking, using
  `min(selected_hours)` as the start hour and `len(selected_hours)` as
  the duration - both correct automatically since the list is only ever
  built from contiguous hours.
- **Verify:** Click two adjacent green hours yourself and confirm the
  status line under the calendar reads "Selected: 2 hour(s), HH:00 to
  HH:00" before you click Book Selected - this was tested
  programmatically (including the deselect-by-reclicking and
  non-adjacent-restarts-selection cases) but is worth seeing once live.

## Entry 12 - Click a row to edit it (Manage Existing Bookings)
- **Asked:** "For update bookings, make it so we can click on the row
  and edit that specific row - so basically if I click, the form where
  you key in Booking ID etc will show the one I selected."
- **Produced:** Switched the Manage screen's results display from a
  plain `Text` widget to a `Listbox` (matching the pattern already
  used in `membership.py`), and bound `<<ListboxSelect>>` to fill
  Booking ID, Date, Start Hour, Duration, Sport and Court No from
  whichever row was clicked. Clicking the header row is explicitly
  ignored (checked via `selection[0] == 0`) so it can't be mistaken
  for a real booking.
- **Verify:** Click a row yourself and confirm the form fills, then
  try Update/Cancel/Delete immediately after - no typing an ID by hand.
  Tested programmatically for the first, last, and header rows.

## Entry 13 - Same step-by-step wizard idea for every module
- **Asked:** "For each module use the same like idea like in booking
  step by step."
- **Produced:** Membership, Coaching and Billing were all rebuilt to
  the same landing-screen pattern Booking already used:
  - **Membership**: landing -> "Register New Member" (2-step wizard:
    name+phone, then a big button per membership type) or "Manage
    Existing Members" (the original search/update/renew/delete screen,
    unchanged, with its existing row-click-to-edit).
  - **Coaching**: landing -> "Register a Coach" (3-step wizard: name+
    phone, then a big button per sport, then rate+commission),
    "Schedule a Class" (3-step wizard: click a coach from a list, then
    a big Private/Group button, then date/hour/duration-pax/fee), or
    "Manage Coaches & Classes" (the original dual coach/class screen
    with its Add button removed, since registering/scheduling moved to
    the wizards - row-click-to-edit was ADDED here, since the original
    screen only had a Find-Coach button and no click-a-row-to-edit for
    either view).
  - **Billing**: landing -> "Generate a Bill" (3-step wizard: member,
    then a big button per category, then whatever that category needs),
    "Pay a Bill" (click an unpaid bill from a list, then a big button
    per payment method, then amount tendered), or "Manage Bills &
    Revenue" (search/void/delete/revenue, converted from a plain Text
    display to a Listbox so rows can be clicked to fill the Bill ID,
    matching the other three modules).
  All four modules' underlying logic functions (register_member,
  schedule_class, generate_bill, pay_bill, etc.) are completely
  unchanged - only the GUI layer was restructured, so every earlier
  test of the logic layer still applies unchanged.
- **Caught two more of my own mistakes while testing, same pattern as
  booking's manage screen before:** in both the first billing.py draft
  and the first coaching.py draft, I left in a broken placeholder line
  from copy-pasting the wizard-navigation pattern too quickly (one was
  a lambda assigned to a button that did nothing and was immediately
  `pack_forget()`-ed; the other was a dead `.bind()` call with an unused
  lambda) - neither crashed anything, but both were dead, confusing code
  that had no business being there. Found by re-reading the file before
  running it, not by the tests - a reminder that compiling clean and
  passing tests does not mean the code is free of leftover junk.
- **Verify:** Click through each module's landing screen and both new
  wizards yourself. Every wizard step, every button, and every row-click
  was exercised programmatically on the real window for all four
  modules (documented results: Membership 13 checks, Billing 19+3
  category checks, Coaching 20+7 checks, Booking regression unchanged)
  plus one combined pass clicking every button in all four modules with
  blank fields - all passed and the data files stayed exactly as they
  started every time.

## Entry 14 - Button-bar UI cleanup (grouping + colour, fewer buttons)
- **Asked:** "Follow UI principles - the buttons are all put together
  at the bottom, make everything as simple as possible."
- **Produced:** Every module's "Manage" screen had 8-9 buttons jammed
  into one unbroken row. Fixed with three concrete changes, not just a
  restyle:
  1. **Grouping (proximity principle)**: each manage screen's button
     bar is now two short rows instead of one long one - top row is
     everyday actions (View All/Search/Update/Renew/Revenue), bottom
     row is permanent/destructive actions plus navigation.
  2. **Colour as signal (visual hierarchy)**: added a shared
     `common.DANGER_COLOR` (the same dark red already used for "Exit"/
     "Back to Main Menu") and applied it to every genuinely
     irreversible action - Delete (all 4 modules), Cancel (booking),
     Void (billing) - so destructive buttons are visually distinct from
     safe ones at a glance, not identical green buttons sitting next to
     Clear and Help.
  3. **Removed redundant buttons**: Membership's "Find" and Coaching's
     "Find Coach" buttons did exactly what clicking a row in the
     results list already does, so both were deleted outright -
     2 fewer buttons across the two busiest screens.
- **Checked before deleting**: `find_member_by_id` and
  `find_coach_by_id` are the dedicated while-loop functions required by
  the rubric. Deleting their only caller would have left them wired to
  nothing - the exact "dead code" problem caught earlier in this
  session for a different function. Fixed by first switching each
  row-click handler to call the same while-loop function instead of its
  own separate for-loop, so the while loop stays genuinely used by the
  row click instead of a now-removed button.
- **Verify:** Open each module's Manage screen and look at the bottom -
  two visually separated rows, with Delete/Cancel/Void standing out in
  red. Tested programmatically (button y-positions span 2 distinct
  rows, danger buttons report the new colour, row-click still works
  for both removed-Find screens) and with a full blank-field
  click-through across all four modules - all passed, no regressions.

## Entry 15 - Tabs instead of multiple windows
- **Asked:** "Can u make it switch the tab instead of multiple windows."
- **Produced:** The program is now one main window with a tab bar
  along the top (Home, Booking, Membership, Coaching, Billing, plus a
  red Exit). `ttk.Notebook` is not on the syllabus list, so the tabs
  are plain `tk.Button`s; clicking one destroys the current tab's Frame
  and builds the chosen module in its place. Each module's
  `open_X_window(parent)` became `build_X_tab(parent, go_home)`: it
  builds into a `tk.Frame` instead of a `tk.Toplevel`, and its "Back to
  Main Menu" button now calls `go_home` (switch to the Home tab) instead
  of destroying a window. The module's own logic and screens are
  unchanged. Two small knock-on fixes: `common.open_date_picker` now
  owns its pop-up from `parent.winfo_toplevel()` (a Frame cannot be a
  `transient` owner), and Membership's Enter-to-search key is bound on
  the main window (a Frame only receives keys when focused) with a
  `winfo_exists()` guard for when the tab has been switched away.
  `main.py`'s menu dispatch uses `if/elif` instead of `match`, so the
  file parses on old Python and the version check can actually run.
- **Design decision:** a tab is rebuilt from the data files every time
  you switch to it, so it always shows the latest records (e.g. a member
  registered on the Membership tab appears straight away when you then
  enrol on the Coaching tab). The trade-off is that anything half-typed
  on the tab you leave is cleared.
- **Verify:** Tested on the real display: every tab and Home button
  switches correctly with only one window ever open, every "Back to
  Main Menu" returns to Home, the date picker opens from a tab, Enter
  after switching tabs raises no error, and a blank-field click of
  every button on every screen of every tab (41 clicks) raised no
  exception. Data files were restored afterward.

## Entry 16 - Simpler tabs that follow the module guideline, plus coaching fixes
- **Asked:** Follow the assignment guideline's function for each module
  ("that's enough"), keep few buttons per tab, make it easy to use and
  don't show too much information at once. Also fix nine reported
  problems, mostly in Coaching: (1) Remove Member did not work; (2)
  hourly rate and commission accepted nan/inf; (3) typing words into a
  number box showed Python's "could not convert" message; (4) the new
  coach form kept the last rate and commission; (5) changing a coach's
  sport left their classes on the old sport; (6) deleting a coach left
  past classes pointing at an ID that could be reused; (7) only the four
  court sports were allowed; (8) names like "a/l", "s/o" and "Ch'ng"
  were rejected; (9) a class could have a duration of 0.
- **Produced:**
  - Every tab now has the same layout from `common.build_sections`: a
    title, 2-4 section buttons and one Help button. Each section shows
    a list on the left and one form or detail panel on the right, with
    only the buttons that apply to the record that's picked (never more
    than three). The landing screens, wizards, nine-field shared forms,
    Clear/Back buttons and the Home/Back-to-Main-Menu buttons inside
    modules were removed; the tab bar already does that job.
  - Booking: one screen with date, sport buttons and a courts x hours
    grid (the guideline's "visual calendar grid ... per hour, by court
    number or sport type"), then member + Book. Bookings section to
    cancel/delete. `update_booking` was removed (cancel and re-book
    instead) to keep the tab simple; booking a past date is now refused.
  - Membership: seven membership-type cards showing fee, length and
    discount, then Register. Members section to edit/renew/delete.
  - Coaching: Coaches, Classes, Enrolment, Hours & Commission sections.
    Bug 1 was caused by the old shared form (in Coach view the "Class ID"
    box held a coach ID, clicking a class never filled Member ID, and
    enrolled members were never shown); Enrolment now lists the class's
    members by name and removes the one you click. Bugs 2-3:
    `common.parse_decimal` / `parse_whole_number` give "Please enter a
    valid number for ..." and reject nan/inf; rate is capped at RM 500,
    commission at 100 %, and the `Coach` setters reject nan too. Bug 4:
    the New button empties every field. Bug 5: `update_coach` moves the
    coach's upcoming classes to the new sport (past classes keep the
    sport that was taught). Bug 6: a coach can't be deleted while any
    class still points to them. Bug 7: `common.COACHING_SPORTS` adds
    Swimming and Yoga, picked from a drop-down. Bug 8:
    `common.is_valid_name` allows `/` and `'`, and `common.format_name`
    keeps "a/l" lower-case and writes "Ch'ng" (not "Ch'Ng"). Bug 9:
    `validate_class_details` requires 1-4 hours, and the GUI uses a
    duration drop-down. A Private session is fixed at 1 person, Group at
    1-30, and fee/date are checked too. Hours & Commission can now be
    shown for one month.
  - Billing: New Bill (member, what it's for, live amount / discount /
    total preview), Bills & Payments (Pay/Void, View Receipt or Delete
    depending on status), Daily Revenue (court rentals, coaching, retail
    sales and membership fees on separate lines with bars, as the
    guideline asks). A booking or class can no longer be billed twice,
    and nan is rejected for prices and payments.
- **Caught and fixed while testing:** typing a date in Booking (or Daily
  Revenue) without pressing Enter left the grid showing the old date.
  It now redraws as soon as a complete, valid date is typed.
- **Verify:** Logic tests for every one of the nine problems (see
  `TEST_CASES.md`, FIX-01 to FIX-12), screenshots of all 11 sections on
  the real display, full click-through flows (register, add coach with
  bad input, schedule, enrol/remove, book from the grid, cancel, create
  and pay a bill), and 54 button clicks with blank fields: no exception.
  Data files were restored afterward. Each member should open their own
  tab and read their section's Help text before the demo, since the
  screens look different from earlier entries.

## Entry 17 - Each tab asks "What would you like to do?"
- **Asked:** When you open a tab it should ask which action you want
  (e.g. Register, Booking, Delete), and each action should be one simple
  page.
- **Produced:** Every module tab now opens on a menu of big action
  buttons with a one-line hint under each (Booking 3, Membership 5,
  Coaching 9, Billing 6). Each action has its own page: a Back button,
  the action's name, one line of instructions, and one main button.
  Clicking the tab you are already on goes back to its menu. The
  section buttons and Help buttons from Entry 16 were removed; the
  instruction line on each page replaces Help.
  - New shared helpers in `common.py`: `build_action_menu` (the menu
    plus one page per action) and `build_pick_page` (list on the left,
    picked record's details and ONE button on the right). Every "pick a
    record, then do something" action uses it, so the module files only
    supply small functions saying what to list, how to describe a row,
    and what the button does.
  - Old combined screens were split into single actions, e.g. Members
    became Update Member / Renew Membership / Delete Member / View
    Members, and Bills & Payments became Pay Bill / Void Bill / Delete
    Bill / View Receipt. Coaching's Enrolment became Enrol Member and
    Remove Member (each row in Remove Member is one member in one class).
  - No logic-layer changes; the Entry 16 fixes are all kept.
- **Verify:** Screenshots of all 4 menus and all 23 action pages; every
  action done once through its page (register, renew, add coach with an
  "inf" rate rejected, schedule, enrol, remove member, cancel class,
  book/cancel/delete a booking, create and pay a bill with "nan"
  rejected, view the receipt); 84 button clicks with blank input and
  with a row picked: no exception. Data files were restored afterward.

## Entry 18 - Add, update and delete coaches on one page
- **Asked:** Merge Add Coach, Update Coach and Remove Coach into one
  page: typing into the blank form adds a coach, clicking a row updates
  that coach, and a Delete button sits beside each row.
- **Produced:** `build_manage_coaches_page` in `coaching.py`, replacing
  the three pages (Coaching now has 7 actions). A tkinter Listbox can't
  hold buttons, so the list is built from one row widget per coach
  (text + red Delete) inside the new `common.build_scroll_area`. The
  row being edited is highlighted; New returns to a blank form. The
  name search (which uses `search_coaches`) and the while-loop
  `find_coach_by_id` are still used. The rules are unchanged: bad
  numbers get a friendly message, and a coach with classes on record
  can't be deleted.
- **Verify:** Tested on the real display (add with a bad then a good
  rate, click a row, save, Delete blocked for a coach with a class,
  Delete for a new coach) and a 77-click blank-input run with no
  exception; see MC-01 to MC-05 in `TEST_CASES.md`. Data restored
  afterward.

## Entry 19 - Same one-page add/update/delete for classes and members
- **Asked:** Use the Manage Coaches pattern for classes and members too.
- **Produced:** The Manage Coaches page became a shared helper,
  `common.build_manage_page`, used by three pages:
  - Manage Coaches (unchanged behaviour, now on the helper).
  - Manage Classes replaces Schedule / Update / Cancel Class: a blank
    form schedules, clicking a row loads it (coach and type locked),
    Delete beside a row cancels it; search by coach ID.
  - Manage Members replaces Update Member / Delete Member / View
    Members: click a row to edit, Delete beside each row, and the
    member summary line under the list. Register keeps its own page
    for the membership cards, so this page has no add mode.
  Coaching now has 5 actions and Membership 3. No logic-layer changes.
- **Verify:** MC-06 to MC-12 in `TEST_CASES.md` run on the real
  program, plus the earlier coach cases again and an 86-click
  blank-input run: no exception. Screenshots could not be taken this
  time because the screen was off (they came out black), so check the
  two new pages by eye once. Data restored afterward.

## Entry 20 - Hour labels, units everywhere, hover hints on everything
- **Asked:** The booking grid's column labels had no units (just
  "08", "09"); make every number show its unit and be easy to see;
  and give every control a hover hint explaining how to use it.
- **Produced:**
  - Booking grid columns now read 08:00 ... 21:00 under a "Start
    time" label; the info line says "free 1-hour slots"; the selection
    says "(2 hour(s))"; booking details show the duration in hours.
  - Units added to list headers and form labels: RM/hour and Comm %
    (coaches), People (classes), Court (bookings), Total RM (bills),
    Hourly rate (RM/hour), Commission (%), Max people (1-30), "of N
    people" and "(N hour(s))" in class details.
  - `common.add_tooltip`: a yellow hint after 450 ms, closed on leave
    or click. The shared builders take `tip=`, so every button, entry,
    drop-down, radio button, menu action, list row, Delete button,
    tab and grid square has one. Grid squares explain their own state
    and price. The welcome message tells users to hover.
- **Verify:** An audit of all 306 interactive widgets across every
  page found none without a hint; the hint logic was tested by firing
  its Enter/Leave/click handlers (the screen was off, so real mouse
  events and screenshots weren't possible); 82-click blank-input run
  with no exception. Please hover over a few things once by eye.

## Entry 21 - Exit warning, keep cancelled bookings, dark mode
- **Asked:** Warn before exiting; don't delete cancelled bookings;
  enable dark mode.
- **Produced:**
  - Exit warning: the Exit tab and the window's X both ask "Are you
    sure you want to exit?" (`on_exit` in `main.py`).
  - Booking's Delete a Booking action and `delete_booking` were removed.
    A cancelled booking now always stays in bookings.txt as CANCELLED.
  - Dark mode: a ☾ Dark Mode / ☀ Light Mode button in the tab bar.
    `common.THEMES` has a light and a dark palette; `apply_theme`
    swaps the shared colours, `apply_widget_defaults` sets tkinter's
    option-database defaults for colours the code doesn't set itself,
    and `main.py` rebuilds the window on the same tab. The choice is
    saved in data/settings.txt (ignored by git, like the rest of
    data/). The few hard-coded colours (past slots, tooltip, list
    border, calendar buttons) now come from the palette.
- **Caught and fixed while testing:** removing `delete_booking` by
  cutting text also removed two helpers below it (`booking_time_text`,
  `find_booking_at`), which raised a NameError on Cancel a Booking.
  Restored from git; added an undefined-name scan of every file to the
  checks.
- **Verify:** EXIT-01 to DARK-04 in `TEST_CASES.md`: both exit paths
  ask and Yes closes; every page and the calendar in dark mode have no
  light-coloured widgets left; the choice survives a restart; crash runs
  in light (80 clicks) and dark (75 clicks) with no exception. The screen
  was off, so no screenshots - please look at dark mode once by eye.

## Entry 22 - Tester's fixes T1-T13
- **Asked:** A tester's list: unique coach phone (T1); searches by sport,
  coach name and member name, coach names on Hours & Commission, "Class
  ID" style headers (T1.1-T1.3); standard dates (T2); no start hour
  that has already passed (T3); safe file writing (T4); keep damaged
  lines (T5); never reuse IDs (T6); round fee before the 0.01 check
  (T7); recursion fallback (T8); read files with a BOM (T9); no enrolling
  in past classes (T10); private classes can't be enrolled (T11);
  labelled details panels (T12); truncate long names with "…" (T13).
- **Produced:** `common.py` gained `READ_ENCODING` (utf-8-sig),
  `file_error_message`, safer `write_lines`/`append_line`,
  `rewrite_records`, ID counters (`data/id_counters.txt`,
  `read_id_counters`, `note_used_id`), `normalize_date`, rounding in
  `parse_decimal`, `fit_text`, `details_text` and
  `RECURSION_SAFE_LIMIT`. Every module now rewrites files through
  `rewrite_records`, catches `OSError` in its GUI handlers, uses named
  ID headers, cut names and labelled details. Coaching: phone check,
  today/past checks, sport/coach/member searches, coach names and a
  search on Hours & Commission, and a Member box for Private classes.
  `count_members`, `total_bills` and `total_commission` wrap the
  recursive totals.
- **T11 cause:** enrolling into a private class worked; the sample
  private class CLS002 was already full (1/1), so it was hidden from
  the Enrol list. Following the tester's suggestion, the member is now
  picked when the private class is scheduled.
- **Also:** "bin", "binti", "bt", "bte" now stay lower-case in names
  (Malay names). MEM-11 changed: IDs are no longer reused after a delete.
- **Caught and fixed while testing:** a local variable named
  `total_commission` hid the new function of the same name and broke the
  Hours & Commission page ("'float' object is not callable"); renamed
  it `commission_sum`.
- **Verify:** T1-01 to T-ALL in `TEST_CASES.md`; crash run 77 clicks,
  no exception; docstring, match/while, import and undefined-name
  checks pass. The screen was off, so no screenshots.

## Entry 23 - Tester's second round (B1-B16, G1-G11)
- **Asked:** A tester's list of bugs (B1-B16) and likely GUI problems
  (G1-G11), each with a suggested fix.
- **Produced:**
  - IDs: the highest IDs already in the files (sample data included)
    are learnt at start-up and before every rewrite; the counter is
    saved before a record (B1, B16).
  - Classes: a class with a bill can't be deleted, and the delete
    question lists enrolled members (B1, B4); a class that is over can
    still have its fee/size/duration fixed (B2); enrolling is refused
    once a class has started, for an expired membership, or for a time
    clash with another class (B3, B5, B6); a private session is saved
    with its member in one write (B9).
  - Members in an upcoming class can't be deleted (B7).
  - Hours & Commission counts only finished classes and adds Pay =
    hours x hourly rate, with upcoming hours shown apart (B8).
  - Coaches: changing sport asks first with class counts (B11); a
    coach with only past classes becomes INACTIVE instead of being
    blocked (B12, G10); `update_coach` writes classes first and undoes
    them if the coach can't be saved (B15).
  - coaching.py: the unused `show_problem` was removed; `messagebox` is
    now used for the sport question; a visible `try/except OSError` is
    in `update_coach`; `SportsClass` now has private attributes with
    getters/setters (B13, B14).
  - GUI: wrapping instructions (G1); window 1000 px and the form card
    packed before the list (G2); drop-downs with a Find box and names
    cut with ... (G3, G4); new class dated tomorrow (G5); past classes
    greyed (G6); calendar opens on the typed month with past days
    disabled where they can't be used (G7); mouse wheel on the lists
    (G8); details wrap instead of cutting (G9); delete questions name
    the record (G11).
- **Not changed:** B14's file-processing point. coaching.py reads and
  writes its files through the shared `common` helpers, the same as
  booking.py and membership.py; whether the marker wants `open()` in
  each module file is a question for the group.
- **Caught while testing:** my first patch script cut functions in the
  wrong place (a regex matched at the start of a slice); caught by the
  compile check, restored from git and re-applied. Manage Classes
  measured 1025 px, so the Find box there was moved under its
  drop-down (995 px).
- **Verify:** B1-01 to B-ALL in `TEST_CASES.md`: 27 logic checks and 18
  GUI checks pass, crash run 107 clicks with no exception. The screen
  was off, so no screenshots; widths are measured, not looked at.

## Entry 24 - Tester's Booking round (B1-B10, G1-G5, R1-R4)
- **Asked:** A tester ran the real GUI on the Booking tab and listed
  bugs (B1-B10), GUI problems (G1-G5) and rubric points (R1-R4).
- **Produced:**
  - B1, B2 were caused by Entry 23's drop-down change: menus show text
    cut to fit, but pages looked it up by the full text. Pages now key
    their lookups with `fit_text`, Find searches the full text, and
    member/coach drop-downs start on "(choose one)" instead of the first
    member (Book a Court, Create Bill, Manage Classes, Enrol).
  - Booking: Book uses the grid's date and refuses if the box changed
    without a redraw (B3); members must be valid on the booking date
    (B4); started bookings can't be cancelled and aren't listed (B5); a
    billed booking can't be cancelled (B6); list sorting no longer
    compares Booking objects (B7); redraw on Enter / full date / focus
    out (B8); opening the page resets it (B9); part-match search on ID,
    member ID or name, date, sport, status (B10).
  - GUI: past hours are not counted as free and a past date says so
    (G1, G5); View All Bookings shows cancelled ones (G2); dark text on
    the selected cell, new `SELECTED_TEXT_COLOR` (G3); member name in
    the Cancel list and header matches the rows (G4).
  - Rubric: Reschedule Booking and View All Bookings pages (R1);
    `save_day_sheet` in booking.py writes its own file with `open()`,
    `datetime` and `try/except/else/finally` (R2).
- **Not changed:** R1's "delete old cancelled records" - the group's
  rule is that bookings are never deleted. R3 (explaining nested code)
  is rehearsal. R4: `Booking` still has no parent class; ask the tutor
  whether inheritance is marked per module.
- **Verify:** BK1-01 to BK-ALL in `TEST_CASES.md`: 20 logic checks and
  26 GUI checks pass; Entry 23's 27 + 18 checks still pass; crash run
  104 clicks, no exception.

## Entry 25 - Search-as-you-type member/coach box
- **Asked:** The user found the separate Find box confusing and wanted
  one box: type to search and pick from a drop-down, or click the arrow
  to see everyone.
- **Produced:** `common.make_filtered_menu` rewritten as a combo box
  from an Entry, a ▼ button and a pop-up Listbox placed on the toplevel
  (no ttk, no extra Toplevel). Used by Book a Court, Create Bill, Manage
  Classes (coach and member) and Enrol Member. Same return pattern as
  before, so pages only changed in how Manage Classes locks the coach
  box.
- **Verify:** CB-01 to CB-09 in `TEST_CASES.md` (21 GUI checks pass);
  earlier logic suites pass; crash run 162 clicks, no exception. My
  older scripts that looked for the old Find box were retired. No
  screenshots (screen off): please look at the list position by eye.

## Entry 26 - Inheritance gap and 16 x 4 rubric check
- **Asked:** (pasted brief) give Booking an inheritance relationship,
  prove all 16 rubric rows in every module, fix weak cells, update the
  README, re-run the tests and clean up.
- **Produced:**
  - `common.Record`: a private ID with getter and validating setter,
    `join_fields()` and an abstract `to_line()`. `Booking` and
    `SportsClass` inherit it, store their ID with `super().__init__`,
    return it from their old getters through `get_record_id()`, and build
    their saved line with the inherited `join_fields()`. File text is
    identical (checked line by line on the sample files).
  - Gaps found by scanning each module (not from the old table):
    membership.py and coaching.py never used `datetime` themselves
    (added `days_until_expiry` shown as "Days left", `days_until_class`
    shown beside the class date, each with try/except/else); coaching.py
    had no function with if/elif/else together (`class_when_text`
    now has one); billing.py had no `else` (`read_receipt` now has a
    try/except/else); membership.py had one multi-line comment block
    (now three).
  - `RUBRIC_CHECK.md` rebuilt; its function names were checked to exist
    and its if/elif/else claims against the syntax tree (several old
    claims were wrong and are corrected). README: run commands for
    Windows and macOS/Linux, folder layout, and a rubric section.
- **Not changed / left for the group:** file processing in membership,
  coaching and billing goes through the shared `common` helpers (listed
  as a weaker cell in the matrix). A data line with a blank ID is now
  skipped like any malformed line.
- **Differences from the brief:** the brief says lambda and
  comprehensions are allowed; this project's own rule (CLAUDE.md) is to
  avoid them, and none were added or removed.
- **Verify:** `TEST_CASES.md` section "Rubric round": 86 logic checks and
  all earlier GUI suites pass; fresh start from another folder works.

## Entry 27 - Dark mode keeps your place
- **Asked:** Why does switching to dark mode go back to the main menu?
  It should only change the colours and keep everything as it was.
- **Cause:** `on_theme_toggle` destroyed every widget and rebuilt the
  window, so each tab came back on its action menu and typed text was lost.
- **Produced:** `common.recolour_widgets` changes the colours of the
  existing widgets in place (old palette value to new, with separate maps
  for background and text options). Stale colours were fixed: the tab
  bar now reads the palette when a tab is chosen, manage-page rows
  remember "past or not" instead of a colour, and the theme button's
  hint is a function that follows the theme. The revenue bars now use
  `BUTTON_COLOR` (the old `ACCENT_COLOR` fill is ambiguous with it in
  light mode), so in dark mode they are a darker green than before.
- **Verify:** DM-01 to DM-06 in `TEST_CASES.md`. Earlier suites still
  pass. One old combo-box test assumed hours were still free today; it
  failed after 22:00 and now uses tomorrow.

## Entry 28 - Tester's coaching round (N1-N11, U1-U5)
- **Asked:** A tester's list of remaining bugs and possible GUI problems in
  the coaching module, with suggested fixes.
- **Produced:**
  - `update_class`: re-checks every enrolled member when the date, start
    or duration changes (N1); refuses a class that has started, and a fee
    or duration change while a bill exists (N2).
  - `cancel_class` refuses started classes (N4) and explains that a PAID
    bill can never be voided, so such a class is kept (N10, confirmed in
    `billing.void_bill`). The same wording fix was made for bookings in
    booking.py, which had the same wrong advice ("void the bill").
  - `delete_coach` and its question: an already-inactive coach gets
    "already inactive, history kept" (N3).
  - `remove_participant` refuses started classes and members with a bill
    for the class; the Remove page explains why started classes are not
    listed (N5).
  - `line_to_class` range-checks what it loads and tidies the date (N9).
  - Headers now have `Member N: name (student ID)` in all six files, and
    a few `#` comments were added in `update_class` / `enrol_participant`
    (N11). **The student IDs are blank (`________`): I don't have them.**
  - GUI: "Nothing worked yet in this month" (U1); a hint under the private
    class Member box (U2); Enrol reloads its list after a failed action
    (U4, via a new `refresh_on_error` option of `build_pick_page`); the
    tallest form fits the default window (U5, screenshot).
- **Decision for the group (conflict with an earlier round):** round 2's
  B2 asked that a class that is over could still have its fee/size
  edited; this round's N2 asks the opposite, to protect the hours and
  commission history. I followed the newest request (N2). If the group
  prefers B2, `update_class`'s `class_has_started` check is the one line.
- **Not done:** N7 (class vs court booking overlap): a class does not
  reserve a court in this system, so it is out of scope. U4's periodic
  refresh: pages already reload every time they are opened and the
  action itself re-checks, so a stale row only costs an error message
  (and now a reload); no timers were added.
- **Verify:** N1-01 to N11-01 in `TEST_CASES.md`: 43 logic and 17 GUI
  checks pass; earlier suites pass (two expectations updated: B2-01 and
  the PAID-bill wording); crash run 169 clicks, no exception.

## Entry 29 - Zoom

User asked to be able to zoom in on records/rows. AI added A-/A+ buttons and
Ctrl+wheel/+/- shortcuts that scale every font in place (no `tkinter.font`,
no rebuild), resize the window, and save the level in `settings.txt`.
Checked by driving the buttons in a launched window.

## Honest limitations of this session
- The GUI was only smoke-tested (launched without crashing); no button
  was interactively clicked by the AI. Each member must click-test their
  own module's window before the demo.
- The "Loop" rubric row's `while` loop was added as a deliberate fix in
  Entry 4, not present in the first draft - worth mentioning if asked how
  AI output was reviewed, since it's a concrete example of a rubric gap
  the group caught and fixed rather than submitting blind.
- **Entry 6 update:** the GUI *was* interactively exercised in that
  overnight session (every button in every module, clicked via
  tkinter's own `.invoke()`, with real valid data typed into the actual
  Entry widgets on a real display) - the limitation above applied to the
  original build session, not the audit session. What the audit session
  still could not do: judge pixel-level layout (wrapping, overlap at odd
  window sizes) without a screenshot tool, and exercise `OptionMenu`
  dropdowns via an actual mouse click (their underlying `StringVar` was
  driven directly instead, which exercises the same code path).

### Entry: Booking grid multi-select and faster clicks
- **Prompt:** user reported they could not book separate slots (e.g. 10:00 and 16:00) in one go, and that every grid click felt slow.
- **AI output:** `booking.py`: grid cell click now toggles a cell in a set and recolours cells in place (no full redraw); new `group_into_blocks` and `create_bookings` (validate every block first, then save one booking per run of consecutive hours); `on_book` shows a summary of all bookings.
- **Verify:** pick two separated blocks plus a cell on another court, choose a member, press Book, and check three bookings appear. Checked by the AI through the real window and by calling `create_bookings` directly (sample data restored afterwards).
- **Not done:** cancelling one hour of a longer booking is still whole-booking only.

### Entry: Partial cancel of a booking
- **Prompt:** user wanted cancelling 10-11 of a 10-14 booking to cancel only that hour.
- **AI output:** `booking.py`: new `cancel_booking_hours` (original ID keeps the cancelled hours as CANCELLED; hours before/after become new CONFIRMED bookings, one file write); Cancel page gets 'Cancel from' / 'Cancel until' drop-downs, defaulting to the whole booking.
- **Verify:** book 4 hours, cancel the middle two on the Cancel page, check View All Bookings shows one CANCELLED and two CONFIRMED pieces. The AI drove this through the real window and tested front/back/whole/invalid ranges (sample data restored afterwards).

### Entry: Home header (greeting, ADMIN label, shortcut buttons, live clock)
- **Prompt:** a pasted brief from a team member asking for a greeting that follows the time of day, an ADMIN label, a welcome line, three shortcut buttons (Book a Court, Register Member, Create Bill) and a live clock card on the Home page.
- **AI output:** `main.py`: `greeting_text`, `clock_text`, `date_text`, `start_clock`, `build_home_header`, a `SHORTCUTS` list; `switch_to_tab(tab, page=None)` now opens a page directly. `common.py`: `build_action_menu` stores an `open_action_page` function on the tab frame (same code as the menu buttons). The clock uses `datetime`, not `time`, because only `datetime` is on the allowed import list. Docs updated.
- **Verify:** start the program: the greeting matches the time of day, the clock changes every second, each shortcut opens the right page, Dark Mode recolours the header. The AI ran these through the real window (screenshots of light and dark Home) and re-ran 174 logic and GUI checks (see `TEST_CASES.md`). Display scaling 125 % and 150 % was not checked.

### Entry: Home header restyle (rounded, glowing, dashboard look)
- **Prompt:** a pasted brief asking the Home header to look like a reference picture: dark, rounded, glowing clock card, pill badge and three rounded shortcut buttons, using only what tkinter really has.
- **AI output:** `main.py`: `HEADER_PALETTE`, `mix_colour`, `round_rect`, `draw_halo`, `timezone_text`, `clock_parts`, `class PillButton`, `class HomeHeader`; `start_clock` now takes the header; the Dark/Light button redraws the header. No image, no extra module. Docs and screenshots (`home_dark.png`, `home_light.png`) added.
- **Verify:** start the program in both modes and compare with the screenshots; watch the seconds for flicker; Tab to a shortcut button and press Enter. The AI ran these through the real window (26 header checks) and re-ran 174 logic and GUI checks. Display scaling 125 % and 150 % was not checked.

### Entry: Membership picture cards on the Register page
- **Prompt:** a pasted brief asking for clickable picture cards for the 7 membership types, with a caption built from `common.py`, text-card fallback, a selected marker and light/dark support.
- **AI output:** `membership.py`: `load_card_picture`, `type_caption`, picture cards in `build_register_page`; `common.py`: `IMAGES_FOLDER`. The 7 supplied files were JPEGs named .png (Tk cannot load them), so they were converted once to real 216x118 PNG with Pillow outside the program (no library added to the program).
- **Verify:** open Membership > Register: 7 picture cards, click each, check the coloured frame moves; rename a picture and check the text card appears. The AI ran these in the real window (18 checks) in both themes. Display scaling 125 % and 150 % was not checked.

### Entry: V6 fixes (U4, N12, U7) and student IDs
- **Prompt:** a pasted list of three fixes plus the four members' student IDs.
- **AI output:** `coaching.py`: Remove Member page now passes `refresh_on_error=True` (U4); `class_bill_info` reports a PAID bill first and `update_class` says "already paid, can't be voided" for PAID and keeps "void it first" for UNPAID (N12; unused `class_bill_id` removed); `class_rows` greys a class as soon as it has started, and its `delete_question` returns None for a started class (U7). `common.py` `build_manage_page`: a `delete_question` of None skips the confirm box (shared change, other modules unaffected, tell teammates). Student IDs filled in the five file headers.
- **Verify:** edit the fee of a class with a PAID bill; make a class start this hour and press Delete (no question, "kept as a record" message, row greyed). The AI ran these in the real window; sample data restored. The Remove Member reload (U4) was not driven through the GUI.
