# Code Explanation (for Q&A / on-the-spot coding)

Each function below: what it does, its inputs, and what it returns. Grouped
by file/author. Updated after Entry 17 in `AI_USAGE_LOG.md` (each tab
asks what to do; one page per action).

## How every module's screen is built (shared pattern)
Each module file has a **logic layer** (the class plus plain functions
that read/write the data files and `raise ValueError` on bad input) and a
**GUI layer** starting at `build_X_tab(parent)`.

- `common.build_action_menu(window, title, action_list)` draws the tab's
  "What would you like to do?" menu: one big button per action (e.g.
  Register, Manage Members, Renew Membership). Each action gets its **own
  page** with a Back button, its name and one line of instructions. It
  returns `(page_frames, page_hooks)`; a function in
  `page_hooks[action_name]` refreshes that page every time it opens.
- Most actions are "pick one record, then do it", so they all use
  `common.build_pick_page(...)`: a list on the left, the picked record's
  details on the right and ONE action button. The module only supplies
  small functions: `load_rows` (what to list), `describe` (details
  text), `action_function` (the work; returns a message or raises
  `ValueError`), and optionally a form (`build_form` / `fill_form`), a
  confirmation question and a summary line under the list.
- Add / update / delete for one kind of record is ONE page built by
  `common.build_manage_page(...)` (Manage Coaches, Manage Classes,
  Manage Members): each list row has its own red Delete button beside
  it (rows are widgets in `common.build_scroll_area`, since a Listbox
  cannot hold buttons); clicking a row loads it into the form (the row
  is highlighted) and the button becomes Save Changes; a blank form adds
  a new record when the page offers adding. The module supplies
  `load_rows`, `build_form`, `clear_form`, `fill_form`, `save_action`
  (record ID `None` means add), `delete_action` and `delete_question`.
- Pages that are really a form (Register, Create Bill) or a picture
  (Book a Court grid, Hours & Commission, Daily Revenue) are built by
  their own `build_..._page` function.

## common.py (Shared)
- `centre_window(window, width, height)` - positions a tkinter window in
  the middle of the screen.
- `ensure_data_files_exist()` - creates `data/`/`data/receipts/` and any
  missing `.txt` files, filled with sample rows generated relative to
  today's date (`build_sample_rows()`).
- `read_lines` / `write_lines` / `append_line` - read/overwrite/append a
  text file in UTF-8. Reading uses `utf-8-sig`, which skips the invisible
  BOM some editors (Notepad) add, so the first record stays readable. If
  a file can't be opened they raise `OSError` with a plain message
  (`file_error_message`), and they only close a file that was opened.
- `rewrite_records(file_path, record_lines, line_parser)` - overwrites a
  data file with the updated records, then adds back every line the
  parser could not read, so a damaged line is never silently lost.
- `generate_id(file_path, prefix)` - next ID after the highest one in
  the file or the highest ever used (`read_id_counters` /
  `note_used_id`, saved in `data/id_counters.txt`), so a deleted
  record's ID is never handed out again.
- `normalize_date(text)` - rewrites a date as `YYYY-MM-DD` (2027-1-5 ->
  2027-01-05) before saving, so text comparisons always match.
- `fit_text(text, width)` - shortens long text for list columns, ending
  in "…". `details_text(pairs)` - builds the aligned "Label:  value"
  lines shown in every details panel.
- `split_fields(line, expected_field_count)` - splits a `|` line, or `None`
  if malformed, so loaders skip corrupted lines instead of crashing.
- `contains_forbidden_character(text)` - True if `text` contains `|` or `;`.
- `is_valid_name(text)` - letters, spaces, `/` and `'` only (so "Ravi a/l
  Kumar", "Muthu s/o Sami" and "Ch'ng" are accepted), must start with a
  letter, max 40 characters. `format_name(text)` tidies capitals word by
  word ("ch'ng wei" -> "Ch'ng Wei", "a/l" stays lower-case); `str.title()`
  is not used because it would give "Ch'Ng".
- `is_valid_phone`, `is_valid_date`, `parse_date`, `is_valid_hour`,
  `today_string`, `current_hour`, `add_days_to_date` - validators and
  date helpers built on `datetime`.
- `parse_decimal(text, field_name, minimum, maximum)` /
  `parse_whole_number(...)` - turn typed text into a number with a plain
  message ("Please enter a valid number for Hourly rate.") instead of
  Python's "could not convert string to float". `float()` accepts "nan"
  and "inf", so these are rejected explicitly (nan is the only value not
  equal to itself), and the value is capped to `[minimum, maximum]`.
  `is_finite_number(value)` is the same nan/inf check on its own.
- `add_tooltip(widget, tip_text)` - hover hint: on `<Enter>` it waits
  450 ms (`widget.after`), then opens a small borderless `Toplevel`
  (`wm_overrideredirect`) under the widget; `<Leave>` or a click closes
  it. `make_button`, `make_entry`, `make_option_menu` and `add_form_row`
  take a `tip=` argument, and the menu, pick and manage pages add hints
  to their own buttons, rows and search boxes, so every interactive
  widget has one. The booking grid gives each square its own hint
  (`cell_tip_text`: free with price / booked / selected / past).
- GUI building blocks used by every tab: `build_action_menu` and
  `build_pick_page` (see above), `make_button` (green, red "danger" or
  white "light" style), `make_card`, `make_entry`, `add_form_row`,
  `make_option_menu` + `set_option_menu_choices` (drop-downs whose
  choices can be reloaded), `build_list_panel`, `build_scroll_area`
  (scrolling list of row widgets), `selected_index`.
- `open_date_picker(parent, target_entry, on_picked=None, allow_past=True)`
  - calendar pop-up; `on_picked` lets a screen refresh as soon as a day
  is clicked. It opens on the month already typed in the box, and with
  `allow_past=False` (booking, classes) past days are grey and disabled.
- `make_filtered_menu(parent, variable, width, tip, command, stacked)` -
  a drop-down with a Find box: typing shortens the list (useful with
  100+ members). Long choices are cut with "…" to fit.
- `build_scroll_area` scrolls with the mouse wheel while the pointer is
  over it (`<MouseWheel>`, and Button-4/5 on Linux).
- `build_manage_page` greys out rows marked "past", and a
  `save_action` that returns None (the user said No) saves nothing.
- `remember_highest_ids(lines)` - saves the highest ID per prefix in
  `data/id_counters.txt`; run at start-up and before every rewrite, so
  sample-data IDs are never reused either. `append_line` saves the
  counter before the record.
- Constants: `SPORTS` (court sports with courts/rate), `COACHING_SPORTS`
  (court sports plus Swimming and Yoga, which need no court),
  `BILL_CATEGORY_NAMES` (on-screen names for the four bill categories).
- `class Person` - base class with private `__name`/`__phone`, validating
  getters/setters. `Member` and `Coach` inherit from it.

## membership.py (Teoh Zynn)
Logic:
- `class Member(Person)` - adds member ID, membership type, join/expiry
  dates; `to_line()` turns it back into a text-file row.
- `line_to_member` / `load_all_members` - load members, skipping bad lines.
- `get_phone_set(member_list)` - set of every phone in use (duplicate check).
- `register_member(name, phone, type)` - validates, new ID, join/expiry.
- `find_member_by_id(member_list, member_id)` - while-loop linear search
  (used when a member row is clicked).
- `search_members(member_list, field, text)` - `match` on id/name/type.
- `has_future_confirmed_booking` / `has_unpaid_bill` - checked before delete.
- `update_member` / `renew_member` / `delete_member`.
- `count_members_by_type` (dict), `members_expiring_within`,
  `count_members_recursive` (recursion) - shown in the Members summary line.

GUI (`build_membership_tab`) - menu of 3 actions, one page each:
- **Register** - name + phone, click a membership-type card (fee, length,
  discount), click Register.
- **Manage Members** (`build_manage_members_page`, on
  `common.build_manage_page`) - every member with a Delete button beside
  the row; click a row to edit name/phone/type and Save Changes. No add
  mode here: new members come from Register. The summary line under the
  list uses `count_members_recursive`, `count_members_by_type` and
  `members_expiring_within`.
- **Renew Membership** - pick a member, Renew.
- Helpers: `member_rows` (uses `search_members`), `describe_member` (uses
  the while-loop `find_member_by_id`), `renew_action`, `delete_action`.

## coaching.py (Tan Chor Koon)
Logic:
- `class Coach(Person)` - adds coach ID, sport (from `COACHING_SPORTS`),
  hourly rate (RM 1-500) and commission (0-100 %). The setters are written
  as `not (low <= x <= high)` so nan is rejected too.
- `class SportsClass` - private attributes (`__class_id`, `__date_text`,
  `__fee_per_pax`, ...) read with getters and changed with setters
  (`set_date_text`, `set_participant_list`, ...); `get_time_text()`
  ("10:00-12:00"), `to_line()`.
- `class Coach` also has a status, ACTIVE or INACTIVE (`get_status`,
  `set_status`, `is_active`). Old lines without it load as ACTIVE.
- `class_has_started`, `class_is_over`, `times_overlap` - time helpers
  used by enrolling, the lists and the report.
- `register_coach`, `find_coach_by_id` (while loop), `search_coaches`
  (`match`).
- `update_coach(...)` - saves the coach; if the sport changed, the coach's
  classes that haven't started are moved to the new sport too (past
  classes keep the sport that was actually taught). The classes file is
  written first; if saving the coach then fails, a `try/except OSError`
  puts the classes back and re-raises, so the files never disagree. The
  page asks first ("N upcoming classes will change, M have members").
- `classes_for_coach` / `upcoming_classes_for_coach` / `delete_coach` -
  a coach with upcoming classes can't be removed; one with only past
  classes is kept as INACTIVE (history stays); one with no classes is
  deleted. The confirm question names the coach and says which.
- `member_enrol_problem(...)` - why a member can't join a class: not
  found, membership ends before the class day, or already in another
  class at an overlapping time. Used by `enrol_participant` and by
  `schedule_class(..., member_id)`, which saves a private session with
  its member in one write. `members_valid_on(date)` fills the member
  drop-downs.
- `class_bill_id` / `cancel_class` - a class with a bill that isn't
  VOID can't be deleted; the confirm question lists enrolled members.
- `coach_phone_in_use(phone, ignore_coach_id)` - two coaches can't share
  a phone number (checked when adding and when updating).
- `validate_class_details(...)` - shared checks for scheduling and
  updating: real date not in the past (and, for today, a start hour that
  hasn't begun), duration 1-4 hours, inside opening hours, Private =
  exactly 1 person, Group = 1-30, fee RM 0.01-1000 (rounded to 2
  decimals first). `schedule_class`/`update_class` save the date through
  `normalize_date`. `enrol_participant` refuses a class that has
  already taken place.
- Manage Classes: when **Private** is picked while scheduling, a Member
  row appears; the chosen member is enrolled straight after the class
  is saved (a private session is for one named person). Classes can be
  searched by sport; Enrol Member by sport or coach name; Remove Member
  by member name. Hours & Commission shows the coach's name first and
  has a coach-name search. `total_commission` uses the recursive total
  up to 500 classes and a loop above that.
- `schedule_class`, `update_class`, `cancel_class`, `find_class_by_id`,
  `coach_has_time_clash`, `search_classes` (`match`).
- `load_member_names()` - dict of member ID -> name from members.txt.
- `enrol_participant` (set used to block duplicates; capped at max_pax) /
  `remove_participant`.
- `classes_in_month`, `coach_hours_by_month(class_list, month_text)` (dict
  of coach -> hours for one month, or all time), `calculate_commission`,
  `total_commission_recursive` (recursion).

GUI (`build_coaching_tab`) - menu of 5 actions, one page each:
- **Manage Coaches** (`build_manage_coaches_page`) and **Manage Classes**
  (`build_manage_classes_page`), both on `common.build_manage_page`: a
  blank form adds (Add Coach / Schedule Class), clicking a row loads it
  for Save Changes, Delete beside a row removes it (a coach only once
  no classes are left). New empties every field again. On an existing
  class the coach and type are locked; Private locks Max people at 1
  (`apply_class_type`, a `match`). Time and duration are drop-downs.
  The class search box takes a coach ID (`search_classes`).
- **Enrol Member** - pick an upcoming class with space, pick the member
  (only people not already in it are offered), Enrol.
- **Remove Member** - each row is one member in one class (row ID
  `CLASS;MEMBER`); pick it and Remove.
- **Hours & Commission** - one row per coach for a month or all time,
  counting only classes that are over (`split_worked_classes`): hours,
  pay (hours × hourly rate), commission, and upcoming hours shown
  separately. Uses `search_classes`, `coach_hours_by_month` and
  `total_commission_recursive`.

## booking.py (Teh Tze Ken)
Logic:
- `class Booking` - private attributes, each validated in its setter;
  `get_price()` = rate x duration.
- `load_all_bookings`, `load_member_names`, `member_exists`.
- `has_clash(...)` - set intersection of requested vs. existing hours
  (only CONFIRMED bookings count).
- `build_availability_grid(sport, date_text)` - list of lists of
  "Free"/"Booked" (hours x courts).
- `count_free_slots_recursive(grid)` - recursion; shown as "N free slots".
- `find_next_free_hour(grid, hours, court_index)` - while-loop scan; used
  for the "Earliest free" hint above the grid.
- `create_booking` (rejects past dates and clashes), `cancel_booking`,
  `search_bookings` (`match`). There is deliberately no delete: a
  cancelled booking stays on record as CANCELLED, so the history is kept.
- `booking_time_text`, `find_booking_at` - small display helpers.

GUI (`build_booking_tab`) - menu of 3 actions, one page each:
- **Book a Court** (`build_book_page`) - date + sport, a courts x hours
  grid (green free, red booked, grey past), click free hours on one
  court, pick the member, Book.
- **Cancel a Booking** (`build_cancel_page`) - pick a confirmed booking
  and cancel it; it stays on record as CANCELLED.
  `booking_rows` filters by member with `search_bookings`.

## billing.py (Low Yee Zhe)
Logic:
- `class Bill` / `class RetailBill(Bill)` (inheritance). Amount/discount
  setters reject nan as well as negatives.
- `get_member_type`, `get_booking_description`, `get_class_description`.
- `billed_references(member_id)` - set of (category, ref) already billed;
  `generate_bill` uses it to refuse billing the same booking/class twice.
- `load_member_choices`, `unbilled_bookings`, `unbilled_classes` - fill
  the New Bill drop-downs with only what can still be billed.
- `generate_bill(...)` - `match` on category; applies the member discount.
- `find_bill_by_id` (while loop), `pay_bill` (method in the
  `VALID_PAYMENT_METHODS` set; rejects nan or too little), `write_receipt`,
  `read_receipt`, `search_bills` (`match`), `void_bill`, `delete_void_bill`.
- `daily_revenue_summary(date_text)` - dict of category -> PAID total,
  grand total and counts.
- `total_bills_recursive` - recursion; "N bill(s) shown, adding up to RM X".

GUI (`build_billing_tab`) - menu of 6 actions, one page each:
- **Create Bill** - member, what it's for, live amount / discount /
  total preview, Create Bill.
- **Pay Bill** - pick an unpaid bill, Cash/Card/E-Wallet (only cash can
  be more than the total), Pay; the line under the list adds up what
  is still owed with `total_bills_recursive`.
- **Void Bill** / **Delete Bill** / **View Receipt** (`build_status_page`,
  a `match` on UNPAID / VOID / PAID) - pick and act.
- **Daily Revenue** - court rentals, coaching, retail sales and
  membership fees on separate lines with bars, plus the total.
- `bill_rows_with_status` uses `search_bills` and lists newest first
  with a while loop; `describe_bill` uses the while-loop
  `find_bill_by_id`.

## main.py (Teh Tze Ken - integration)
- Checks `sys.version_info` against Python 3.10 **before** importing the
  four modules (they use `match`), and contains no `match` itself.
- `build_home_tab(parent, switch_to_tab)` - Home tab with one button per
  module and "How to Use This System".
- `main()` - one window: tab bar (Home, Booking, Membership, Coaching,
  Billing, Exit) above a content area. `switch_to_tab` destroys the
  current tab and calls the module's `build_X_tab(content_frame)` with
  `if/elif`, so each tab always shows fresh data. Clicking the tab you
  are already on rebuilds it, which returns to its action menu.
- **Exit warning:** `on_exit` asks "Are you sure you want to exit?" and is
  used by both the Exit tab and the window's X button
  (`root_window.protocol("WM_DELETE_WINDOW", on_exit)`).
- **Dark mode:** `build_window_contents` builds the tab bar and tabs in
  the current theme. The Dark Mode / Light Mode button calls
  `on_theme_toggle`, which switches the palette with
  `common.apply_theme`, saves the choice (`common.save_theme_choice` ->
  `data/settings.txt`), destroys everything and rebuilds it on the same
  tab. In `common.py`, `THEMES` holds the light and dark palettes;
  `apply_theme` reassigns the shared colour names (`global`), and
  `apply_widget_defaults` sets tkinter option-database defaults (text
  colour, entry/list/menu colours) for options the code doesn't set
  itself. `load_theme_choice` reads the saved theme at start-up.

---

# On-the-spot coding practice tasks (5 per module)

## Membership
1. Add a search option that lists members whose join date is in a given
   month. *(Loop over `load_all_members()`, compare `get_join_date()[5:7]`
   to the target month string.)*
2. Add a function `count_vip_members(member_list)` that returns how many
   members have type "VIP", using a plain `for` loop and an `if`.
3. Change `register_member` so it also rejects a name shorter than 3
   characters (add a check after `is_valid_name`).
4. Add a "Members by phone prefix" report: dict of first 3 digits ->
   count, built with a `for` loop and a dictionary.
5. Add an `undo_last_registration()` that deletes the member with the
   highest numeric ID (use `generate_id`'s logic in reverse).

## Coaching
1. Add `average_class_fee(class_list)` returning the mean `fee_per_pax`
   across all classes (sum with a loop, divide by count).
2. Explain where the rule "a Private class's `max_pax` must be exactly 1"
   is enforced (`validate_class_details`) and where the GUI makes it
   impossible to break (`apply_class_type`).
3. Add `coaches_teaching(sport, coach_list)` returning a list of coaches
   who teach a given sport.
4. Add a function that counts how many classes are still accepting
   participants (`len(get_participant_list()) < max_pax`).
5. Explain why `update_class` refuses to shrink `max_pax` below the
   current enrolment, then add the same rule as a check inside
   `enrol_participant` for symmetry (it is already implied by the
   `len(participant_set) >= max_pax` check - show where).

## Booking
1. Add a function `bookings_on_date(date_text)` returning all CONFIRMED
   bookings on that date, across every sport.
2. Explain why `has_clash` builds two sets of hours and checks
   `.intersection()` instead of comparing start/end numbers directly -
   what would change if a booking could span midnight?
3. Add a `total_revenue_from_bookings()` using `SPORTS` rates and a loop.
4. Add validation that `court_no` must be a whole number before calling
   `Booking.set_court_no`.
5. Add a "busiest court" report: dict of (sport, court_no) -> booking
   count.

## Billing
1. Add a function `unpaid_bills_for_member(member_id)` returning that
   member's UNPAID bills.
2. Explain why `daily_revenue_summary` only counts PAID bills in its
   totals but `bill_count` counts every bill issued that day - then add
   a `void_count` to the returned tuple the same way.
3. Add `monthly_revenue_summary(year_month)` that sums `daily_revenue_
   summary` across every date starting with `year_month`.
4. Add a check that a RetailBill's item name cannot be empty (it already
   exists in `generate_bill` - find it and explain where).
5. Add a "most-billed category" report using `daily_revenue_summary`'s
   dictionary across multiple dates, summed with a loop.
