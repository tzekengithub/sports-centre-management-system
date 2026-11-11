"""
Module      : booking.py
Member 1    : Teh Tze Ken (student ID: ________)
Purpose     : Facility & Court Booking module - a visual grid of court
              availability per hour for each sport, booking by clicking
              free slots, rescheduling, cancelling, viewing every booking
              and saving a printable day sheet.
Date        : 2026-11-07
"""

import datetime
import os
import tkinter as tk
from tkinter import messagebox

import common


# ---------------------------------------------------------------------------
# CLASS (encapsulation)
# ---------------------------------------------------------------------------
class Booking(common.Record):
    """A single court booking with private attributes, getters and setters.
    It inherits the private ID and the line-building helper from common.Record."""

    def __init__(self, booking_id, member_id, sport, court_no, date_text,
                 start_hour, duration_hrs, status):
        """Create the object and validate its starting values."""
        super().__init__(booking_id)
        self.__member_id = member_id
        self.__sport = ""
        self.__court_no = 0
        self.__date_text = ""
        self.__start_hour = 0
        self.__duration_hrs = 0
        self.__status = ""
        self.set_sport(sport)
        self.set_court_no(court_no)
        self.set_date_text(date_text)
        self.set_start_hour(start_hour)
        self.set_duration_hrs(duration_hrs)
        self.set_status(status)

    def get_booking_id(self):
        """Return the booking ID (kept by the parent class, Record)."""
        return self.get_record_id()

    def get_member_id(self):
        """Return the member ID who made the booking."""
        return self.__member_id

    def get_sport(self):
        """Return the sport booked."""
        return self.__sport

    def set_sport(self, sport):
        """Validate and store the sport."""
        if sport not in common.SPORTS:
            raise ValueError("Sport is not recognised.")
        self.__sport = sport

    def get_court_no(self):
        """Return the court number."""
        return self.__court_no

    def set_court_no(self, court_no):
        """Validate and store the court number against the sport's court count."""
        max_courts = common.SPORTS[self.__sport]["courts"]
        if court_no < 1 or court_no > max_courts:
            raise ValueError(f"Court number must be between 1 and {max_courts} for {self.__sport}.")
        self.__court_no = court_no

    def get_date_text(self):
        """Return the booking date (YYYY-MM-DD)."""
        return self.__date_text

    def set_date_text(self, date_text):
        """Validate and store the booking date."""
        if not common.is_valid_date(date_text):
            raise ValueError("Booking date must be YYYY-MM-DD.")
        self.__date_text = date_text

    def get_start_hour(self):
        """Return the starting hour."""
        return self.__start_hour

    def set_start_hour(self, start_hour):
        """Validate and store the starting hour."""
        if not common.is_valid_hour(start_hour):
            raise ValueError(f"Start hour must be within opening hours ({common.OPENING_HOUR}-{common.CLOSING_HOUR}).")
        self.__start_hour = start_hour

    def get_duration_hrs(self):
        """Return the duration in hours."""
        return self.__duration_hrs

    def set_duration_hrs(self, duration_hrs):
        """Validate and store the duration in hours."""
        if duration_hrs <= 0:
            raise ValueError("Duration must be greater than zero hours.")
        if not common.is_valid_hour(self.__start_hour + duration_hrs - 1):
            raise ValueError("Booking would extend past closing hour.")
        self.__duration_hrs = duration_hrs

    def get_status(self):
        """Return the booking status."""
        return self.__status

    def set_status(self, status):
        """Validate and store the booking status."""
        if status not in common.BOOKING_STATUSES:
            raise ValueError("Status must be CONFIRMED or CANCELLED.")
        self.__status = status

    def get_price(self):
        """Price preview = sport rate x duration hours."""
        return common.SPORTS[self.__sport]["rate"] * self.__duration_hrs

    def to_line(self):
        """Turn this booking into a pipe-delimited text-file line."""
        # The parent's join_fields() puts the ID first and adds the | separators.
        return self.join_fields([
            self.__member_id, self.__sport, str(self.__court_no),
            self.__date_text, str(self.__start_hour), str(self.__duration_hrs), self.__status,
        ])


# ---------------------------------------------------------------------------
# LOGIC LAYER
# ---------------------------------------------------------------------------
BOOKING_FIELD_COUNT = 8


def line_to_booking(line):
    """Convert one text-file line into a Booking object, or None if the
    line is malformed (wrong field count or bad values)."""
    fields = common.split_fields(line, BOOKING_FIELD_COUNT)
    if fields is None:
        return None
    try:
        return Booking(fields[0], fields[1], fields[2], int(fields[3]), fields[4],
                        int(fields[5]), int(fields[6]), fields[7])
    except ValueError:
        return None


def load_all_bookings():
    """Read bookings.txt and return a list of Booking objects. Malformed
    lines are skipped rather than crashing the program."""
    booking_list = []
    for line in common.read_lines(common.BOOKINGS_FILE):
        booking = line_to_booking(line)
        if booking is not None:
            booking_list.append(booking)
    return booking_list


MEMBER_FIELD_COUNT = 6


def load_member_names():
    """Return a dictionary of member_id -> name, read from members.txt."""
    member_names = {}
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            member_names[fields[0]] = fields[1]
    return member_names


def member_exists(member_id):
    """Return True if member_id appears in members.txt."""
    return member_id in load_member_names()


def load_member_expiry_dates():
    """Return a dictionary of member_id -> membership end date (YYYY-MM-DD)."""
    expiry_dates = {}
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            expiry_dates[fields[0]] = common.normalize_date(fields[5])
    return expiry_dates


def members_valid_on(date_text):
    """Return (member_id, name) for every member whose membership is
    still valid on date_text, for the Book a Court drop-down."""
    member_names = load_member_names()
    expiry_dates = load_member_expiry_dates()
    valid_members = []
    for member_id in member_names:
        if expiry_dates.get(member_id, "") >= date_text:
            valid_members.append((member_id, member_names[member_id]))
    return valid_members


def check_member_can_book(member_id, date_text):
    """Raise ValueError if member_id doesn't exist or their membership
    ends before date_text (an expired member can't book)."""
    expiry_dates = load_member_expiry_dates()
    if member_id not in expiry_dates:
        raise ValueError(f"No member found with ID {member_id}.")
    if expiry_dates[member_id] < date_text:
        raise ValueError(f"{member_id}'s membership ends on {expiry_dates[member_id]}, before {date_text}. "
                         "Renew it in Membership first.")


def booking_has_started(booking):
    """Return True if the booking's first hour has begun (or its date has
    passed). Started bookings are history: they can't be changed."""
    today = common.today_string()
    if booking.get_date_text() < today:
        return True
    return booking.get_date_text() == today and booking.get_start_hour() <= common.current_hour()


BILL_FIELD_COUNT = 10


def booking_bill_info(booking_id):
    """Return (bill_id, status) of a bill (not VOID) charging for this
    booking, or None. Read straight from bills.txt (booking doesn't import
    billing)."""
    for line in common.read_lines(common.BILLS_FILE):
        fields = common.split_fields(line, BILL_FIELD_COUNT)
        if fields is None:
            continue
        if fields[2] == "COURT" and fields[3] == booking_id and fields[8] != "VOID":
            return fields[0], fields[8]
    return None


def booking_bill_id(booking_id):
    """Return the ID of a bill (not VOID) charging for this booking, or None."""
    bill_info = booking_bill_info(booking_id)
    if bill_info is None:
        return None
    return bill_info[0]


def bill_blocks_text(bill_info):
    """Words for why a billed booking can't change. A PAID bill can never be
    voided (billing refuses), so the booking then stays as it is."""
    if bill_info[1] == "PAID":
        return f"Bill {bill_info[0]} is paid and a paid bill can't be voided, so this booking stays as it is."
    return f"Bill {bill_info[0]} charges for this booking. Void the bill in Billing first."


def has_clash(booking_list, sport, court_no, date_text, start_hour, duration_hrs, ignore_id=None):
    """Return True if an existing CONFIRMED booking overlaps this slot
    (ignore_id skips the booking being rescheduled).
    Builds the set of hours being requested and, for each candidate
    booking on the same sport/court/date, the set of hours it already
    occupies - if the two sets share any hour, the slots clash."""
    requested_hours = set(range(start_hour, start_hour + duration_hrs))
    for booking in booking_list:
        if booking.get_status() != "CONFIRMED" or booking.get_booking_id() == ignore_id:
            continue
        if booking.get_sport() != sport or booking.get_court_no() != court_no or booking.get_date_text() != date_text:
            continue
        existing_hours = set(range(booking.get_start_hour(), booking.get_start_hour() + booking.get_duration_hrs()))
        if requested_hours.intersection(existing_hours):
            return True
    return False


def build_availability_grid(sport, date_text):
    """Build a list of lists: rows = hours, columns = courts, values =
    'Free' or 'Booked', for the given sport and date."""
    court_count = common.SPORTS[sport]["courts"]
    hour_list = list(range(common.OPENING_HOUR, common.CLOSING_HOUR))
    grid = []
    for hour in hour_list:
        row = []
        for court_index in range(court_count):
            row.append("Free")
        grid.append(row)

    for booking in load_all_bookings():
        if booking.get_sport() != sport or booking.get_date_text() != date_text:
            continue
        if booking.get_status() != "CONFIRMED":
            continue
        for hour in range(booking.get_start_hour(), booking.get_start_hour() + booking.get_duration_hrs()):
            if hour in hour_list:
                row_index = hour_list.index(hour)
                column_index = booking.get_court_no() - 1
                grid[row_index][column_index] = "Booked"
    return grid, hour_list, court_count


def count_free_slots_recursive(grid, row_index=0):
    """Recursively count how many 'Free' cells exist across all rows,
    starting from row_index. Demonstrates recursion over a list of lists."""
    if row_index >= len(grid):
        return 0
    free_in_row = 0
    for cell in grid[row_index]:
        if cell == "Free":
            free_in_row += 1
    return free_in_row + count_free_slots_recursive(grid, row_index + 1)


def find_next_free_hour(grid, hour_list, court_index):
    """Scan a court's column in the availability grid with a while loop
    and return the first free hour, or None if the court is fully booked."""
    row_index = 0
    while row_index < len(grid):
        if grid[row_index][court_index] == "Free":
            return hour_list[row_index]
        row_index += 1
    return None


def create_booking(member_id, sport, court_no, date_text, start_hour, duration_hrs):
    """Validate and create a new booking. Raises ValueError on invalid input or clash."""
    date_text = check_booking_time(date_text, start_hour)
    check_member_can_book(member_id, date_text)

    booking_list = load_all_bookings()
    if has_clash(booking_list, sport, court_no, date_text, start_hour, duration_hrs):
        raise ValueError("This court is already booked for the selected time.")

    new_id = common.generate_id(common.BOOKINGS_FILE, "BKG")
    new_booking = Booking(new_id, member_id, sport, court_no, date_text, start_hour, duration_hrs, "CONFIRMED")
    common.append_line(common.BOOKINGS_FILE, new_booking.to_line())
    return new_booking


def check_booking_time(date_text, start_hour):
    """Check a booking date and start hour are real and not in the past.
    Returns the date in standard YYYY-MM-DD form; raises ValueError."""
    if not common.is_valid_date(date_text):
        raise ValueError("Booking date must be a real date in YYYY-MM-DD form.")
    # One standard form (2027-1-5 -> 2027-01-05), so clash checks compare like with like.
    date_text = common.normalize_date(date_text)
    if date_text < common.today_string():
        raise ValueError("You cannot book a date in the past.")
    if date_text == common.today_string() and start_hour <= common.current_hour():
        raise ValueError(f"{start_hour:02d}:00 has already started today. Pick a later time.")
    return date_text


SEARCH_FIELDS = ("id", "member", "date", "sport", "status")


def search_bookings(booking_list, search_field, search_text, member_names=None):
    """Search bookings by 'id', 'member' (ID or name), 'date', 'sport' or
    'status'. Matches part of the text and ignores capitals, so 'mem00'
    or 'ahmad' or '2026-11' all work."""
    results = []
    search_text_lower = search_text.strip().lower()
    if member_names is None:
        member_names = {}
    for booking in booking_list:
        match search_field:
            case "id":
                if search_text_lower in booking.get_booking_id().lower():
                    results.append(booking)
            case "member":
                member_name = member_names.get(booking.get_member_id(), "").lower()
                if search_text_lower in booking.get_member_id().lower() or search_text_lower in member_name:
                    results.append(booking)
            case "date":
                if booking.get_date_text().startswith(search_text.strip()):
                    results.append(booking)
            case "sport":
                if search_text_lower in booking.get_sport().lower():
                    results.append(booking)
            case "status":
                if booking.get_status().lower() == search_text_lower:
                    results.append(booking)
    return results


def search_any_field(booking_list, search_text, member_names):
    """Return the bookings matching search_text in any SEARCH_FIELDS
    field, each listed once, in their original order."""
    matched_ids = set()
    for search_field in SEARCH_FIELDS:
        for booking in search_bookings(booking_list, search_field, search_text, member_names):
            matched_ids.add(booking.get_booking_id())
    results = []
    for booking in booking_list:
        if booking.get_booking_id() in matched_ids:
            results.append(booking)
    return results


def cancel_booking(booking_id):
    """Set a booking's status to CANCELLED. Blocked if it is already
    CANCELLED (clicking Cancel twice gives a clear message), if it has
    started (past bookings are history), or while a bill charges for it."""
    booking_list = load_all_bookings()
    booking_found = False
    for booking in booking_list:
        if booking.get_booking_id() == booking_id:
            booking_found = True
            if booking.get_status() == "CANCELLED":
                raise ValueError("This booking is already cancelled.")
            if booking_has_started(booking):
                raise ValueError("This booking has already started or passed, so it stays as it is.")
            bill_info = booking_bill_info(booking_id)
            if bill_info is not None:
                raise ValueError(bill_blocks_text(bill_info))
            booking.set_status("CANCELLED")
    if not booking_found:
        raise ValueError(f"No booking found with ID {booking_id}.")

    updated_lines = []
    for booking in booking_list:
        updated_lines.append(booking.to_line())
    common.rewrite_records(common.BOOKINGS_FILE, updated_lines, line_to_booking)


def reschedule_booking(booking_id, new_date_text, new_start_hour, new_court_no):
    """Move a CONFIRMED booking that hasn't started to another date, start
    hour and/or court of the same sport. The length stays the same, so
    the price doesn't change. Raises ValueError on any problem."""
    booking_list = load_all_bookings()
    booking = find_booking_by_id(booking_list, booking_id)
    if booking is None:
        raise ValueError(f"No booking found with ID {booking_id}.")
    if booking.get_status() != "CONFIRMED":
        raise ValueError("Only confirmed bookings can be rescheduled.")
    if booking_has_started(booking):
        raise ValueError("This booking has already started or passed, so it can't be moved.")
    bill_info = booking_bill_info(booking_id)
    if bill_info is not None and bill_info[1] == "PAID":
        raise ValueError(f"Bill {bill_info[0]} is paid and a paid bill can't be voided, so this booking "
                         "stays as it is.")
    if bill_info is not None:
        raise ValueError(f"Bill {bill_info[0]} already shows this booking's time. Void the bill first, "
                         "then reschedule and bill it again.")
    new_date_text = check_booking_time(new_date_text, new_start_hour)
    check_member_can_book(booking.get_member_id(), new_date_text)
    if has_clash(booking_list, booking.get_sport(), new_court_no, new_date_text, new_start_hour,
                 booking.get_duration_hrs(), ignore_id=booking_id):
        raise ValueError("That court is already booked for the new time.")
    # The setters check the court number and that it ends before closing.
    booking.set_court_no(new_court_no)
    booking.set_date_text(new_date_text)
    booking.set_start_hour(new_start_hour)
    booking.set_duration_hrs(booking.get_duration_hrs())
    updated_lines = []
    for each_booking in booking_list:
        updated_lines.append(each_booking.to_line())
    common.rewrite_records(common.BOOKINGS_FILE, updated_lines, line_to_booking)
    return booking


def find_booking_by_id(booking_list, booking_id):
    """Linear search with a while loop; return the Booking or None."""
    index = 0
    while index < len(booking_list):
        if booking_list[index].get_booking_id() == booking_id:
            return booking_list[index]
        index += 1
    return None


DAY_SHEET_FOLDER = os.path.join(common.DATA_FOLDER, "day_sheets")


def day_sheet_text(date_text):
    """Return the text of the printable day sheet for date_text: every
    CONFIRMED booking that day, sorted by sport, court and time."""
    member_names = load_member_names()
    sheet_rows = []
    for booking in load_all_bookings():
        if booking.get_date_text() == date_text and booking.get_status() == "CONFIRMED":
            sheet_rows.append((booking.get_sport(), booking.get_court_no(), booking.get_start_hour(),
                               booking.get_booking_id()))
    sheet_rows.sort()
    booking_list = load_all_bookings()
    printed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"Sports Centre - court bookings for {date_text}", f"Printed {printed_at}", "",
             f"{'Sport':<10}{'Court':<7}{'Time':<13}{'Booking ID':<12}Member"]
    total_hours = 0
    for sport, court_no, start_hour, booking_id in sheet_rows:
        booking = find_booking_by_id(booking_list, booking_id)
        member_text = f"{booking.get_member_id()} {member_names.get(booking.get_member_id(), '')}"
        lines.append(f"{sport:<10}{court_no:<7}{booking_time_text(booking):<13}{booking_id:<12}{member_text}")
        total_hours += booking.get_duration_hrs()
    if len(sheet_rows) == 0:
        lines.append("(no bookings)")
    lines.append("")
    lines.append(f"Total: {len(sheet_rows)} booking(s), {total_hours} court hour(s).")
    return "\n".join(lines) + "\n"


def save_day_sheet(date_text):
    """Write the day sheet to data/day_sheets/bookings_<date>.txt and
    return the file's path. Raises OSError if it can't be written."""
    if not common.is_valid_date(date_text):
        raise ValueError("Pick a real date first.")
    date_text = common.normalize_date(date_text)
    sheet_text = day_sheet_text(date_text)
    sheet_path = os.path.join(DAY_SHEET_FOLDER, f"bookings_{date_text}.txt")
    sheet_file = None
    try:
        os.makedirs(DAY_SHEET_FOLDER, exist_ok=True)
        sheet_file = open(sheet_path, "w", encoding="utf-8")
        sheet_file.write(sheet_text)
    except OSError as error:
        raise OSError(f"Could not save the day sheet: {error}")
    else:
        return sheet_path
    finally:
        # Runs whether the write worked or not, so the file is never left open.
        if sheet_file is not None:
            sheet_file.close()


def booking_time_text(booking):
    """Return a booking's time as e.g. '18:00-20:00'."""
    end_hour = booking.get_start_hour() + booking.get_duration_hrs()
    return f"{booking.get_start_hour():02d}:00-{end_hour:02d}:00"


def find_booking_at(booking_list, sport, court_no, date_text, hour):
    """Return the CONFIRMED booking covering this court and hour, or None."""
    for booking in booking_list:
        if booking.get_status() != "CONFIRMED":
            continue
        if (booking.get_sport() == sport and booking.get_court_no() == court_no
                and booking.get_date_text() == date_text):
            if booking.get_start_hour() <= hour < booking.get_start_hour() + booking.get_duration_hrs():
                return booking
    return None


# ---------------------------------------------------------------------------
# GUI LAYER
#
# The tab opens on a menu asking "What would you like to do?". Each
# action has its own one-page screen with a Back button:
#   Book a Court       - date + sport, a courts x hours grid, click free
#                        hours, pick the member, click Book (and Save Day
#                        Sheet writes that day's bookings to a text file)
#   Reschedule Booking - pick an upcoming booking, choose a new date,
#                        start time or court, click Reschedule
#   Cancel a Booking   - pick an upcoming booking, click Cancel Booking
#   View All Bookings  - every booking, confirmed and cancelled, with search
# Bookings are never deleted: a cancelled one stays on record as CANCELLED.
# ---------------------------------------------------------------------------
BOOKING_ACTIONS = [
    ("Book a Court", "See free courts and book one",
     "Pick a date and a sport. Click a free (green) hour - click the next hour on the same "
     "court to book longer. Choose the member, then click Book."),
    ("Reschedule Booking", "Move a booking to another time or court",
     "Click an upcoming booking, choose the new date, start time and court, then click "
     "Reschedule. The length and price stay the same."),
    ("Cancel a Booking", "Cancel an upcoming booking",
     "Click the booking to cancel, then click Cancel Booking. Search by member ID or name, "
     "booking ID or date."),
    ("View All Bookings", "Every booking, including cancelled ones",
     "All bookings, confirmed and cancelled. Search by booking ID, member ID or name, date "
     "(e.g. 2026-11), sport or status, then click a row for its details."),
]

MEMBER_COLUMN_WIDTH = 21
UPCOMING_LIST_HEADER = (f"{'Booking ID':<11}{'Date':<11}{'Time':<12}{'Sport':<10}{'Court':<6}"
                        f"{'Member':<{MEMBER_COLUMN_WIDTH}}")
ALL_LIST_HEADER = (f"{'Booking ID':<11}{'Date':<11}{'Time':<12}{'Sport':<10}{'Court':<6}"
                   f"{'Member ID':<10}{'Status':<9}")
SEARCH_LABEL = "Member / ID / date"
MEMBER_MENU_WIDTH = 24


def show_problem(error):
    """Show a ValueError's plain message in a standard error box."""
    messagebox.showerror("Please check", str(error))


def build_booking_tab(parent):
    """Build the Facility & Court Booking tab inside parent (the main
    window's tab area) and return its frame. The tab opens on a menu
    asking what to do; each action has its own simple page."""
    window = tk.Frame(parent, bg=common.APP_BG)
    page_frames, page_hooks = common.build_action_menu(window, "Facility & Court Booking", BOOKING_ACTIONS)
    build_book_page(page_frames["Book a Court"], page_hooks)
    page_hooks["Reschedule Booking"] = build_reschedule_page(page_frames["Reschedule Booking"])
    page_hooks["Cancel a Booking"] = build_cancel_page(page_frames["Cancel a Booking"])
    page_hooks["View All Bookings"] = build_view_all_page(page_frames["View All Bookings"])
    return window


def booking_rows(search_text, upcoming_only):
    """Return (booking_id, row_text) for the list pages, soonest first.
    upcoming_only True lists CONFIRMED bookings that haven't started (with
    the member's name); False lists every booking with its status."""
    booking_list = load_all_bookings()
    member_names = load_member_names()
    if search_text != "":
        booking_list = search_any_field(booking_list, search_text, member_names)
    # Sort on plain values only (date, hour, ID, then position): Booking
    # objects can't be compared, so two equal keys must never reach them.
    sort_rows = []
    for index in range(len(booking_list)):
        booking = booking_list[index]
        if upcoming_only and (booking.get_status() != "CONFIRMED" or booking_has_started(booking)):
            continue
        sort_rows.append((booking.get_date_text(), booking.get_start_hour(), booking.get_booking_id(), index))
    sort_rows.sort()
    rows = []
    for date_text, start_hour, booking_id, index in sort_rows:
        booking = booking_list[index]
        row_text = (f"{booking_id:<11}{date_text:<11}{booking_time_text(booking):<12}"
                    f"{booking.get_sport():<10}{booking.get_court_no():<6}")
        if upcoming_only:
            member_text = f"{booking.get_member_id()} {member_names.get(booking.get_member_id(), '?')}"
            row_text += f"{common.fit_text(member_text, MEMBER_COLUMN_WIDTH - 1):<{MEMBER_COLUMN_WIDTH}}"
        else:
            row_text += f"{booking.get_member_id():<10}{booking.get_status():<9}"
        rows.append((booking_id, row_text))
    return rows


def describe_booking(booking_id):
    """Return the details text for one booking."""
    booking = find_booking_by_id(load_all_bookings(), booking_id)
    if booking is None:
        return "This booking no longer exists."
    bill_id = booking_bill_id(booking_id)
    if bill_id is None:
        bill_text = "not billed"
    else:
        bill_text = bill_id
    if booking.get_status() == "CANCELLED":
        when_text = "cancelled"
    elif booking_has_started(booking):
        when_text = "started / past"
    else:
        when_text = "upcoming"
    return common.details_text([
        ("Booking ID", booking.get_booking_id()),
        ("Sport", booking.get_sport()),
        ("Court", booking.get_court_no()),
        ("Date", booking.get_date_text()),
        ("Time", booking_time_text(booking)),
        ("Duration", f"{booking.get_duration_hrs()} hour(s)"),
        ("Member", f"{booking.get_member_id()} {load_member_names().get(booking.get_member_id(), '')}"),
        ("Price", f"RM {booking.get_price():.2f}"),
        ("Bill", bill_text),
        ("Status", f"{booking.get_status()} ({when_text})"),
    ])


def build_cancel_page(page_frame):
    """Build the Cancel a Booking page and return its refresh function.
    Cancelled bookings are kept on record (status CANCELLED), never
    deleted, so the centre keeps a full history."""

    def load_rows(search_text):
        """Upcoming confirmed bookings only (past ones are history)."""
        return booking_rows(search_text, True)

    def cancel_action(booking_id):
        """Cancel the picked booking."""
        cancel_booking(booking_id)
        return f"Booking {booking_id} cancelled. It stays on record as CANCELLED (see View All Bookings)."

    def cancel_question(booking_id):
        """Confirmation question for cancelling, naming the booking."""
        booking = find_booking_by_id(load_all_bookings(), booking_id)
        if booking is None:
            return f"Cancel booking {booking_id}?"
        return (f"Cancel booking {booking_id} ({booking.get_sport()} Court {booking.get_court_no()}, "
                f"{booking.get_date_text()} {booking_time_text(booking)})? This frees the court for others.")

    return common.build_pick_page(page_frame, UPCOMING_LIST_HEADER, load_rows, "Cancel Booking",
                                  cancel_action, describe=describe_booking, confirm_text=cancel_question,
                                  danger=True, search_label=SEARCH_LABEL, empty_text="No upcoming bookings.",
                                  action_tip="Cancel the booking you clicked. It stays on record as CANCELLED.")


def build_view_all_page(page_frame):
    """Build the View All Bookings page (view only): every booking,
    including cancelled and past ones, with a search box."""

    def load_rows(search_text):
        """Every booking, with its status."""
        return booking_rows(search_text, False)

    def summary_text():
        """Count bookings by status under the list."""
        status_counts = {}
        for booking in load_all_bookings():
            status_counts[booking.get_status()] = status_counts.get(booking.get_status(), 0) + 1
        parts = []
        for status in common.BOOKING_STATUSES:
            parts.append(f"{status_counts.get(status, 0)} {status.lower()}")
        return "Bookings on record: " + ", ".join(parts) + ". Cancelled bookings are kept, never deleted."

    return common.build_pick_page(page_frame, ALL_LIST_HEADER, load_rows, None, None,
                                  describe=describe_booking, search_label=SEARCH_LABEL,
                                  summary_text=summary_text, empty_text="No bookings found.")


def hour_choice_text(hour):
    """Return the drop-down text for a start hour, e.g. '09:00'."""
    return f"{hour:02d}:00"


def build_reschedule_page(page_frame):
    """Build the Reschedule Booking page and return its refresh function."""
    form_widgets = {}

    def build_form(form_frame):
        """Add the new date (with calendar), start time and court."""
        date_row = tk.Frame(form_frame, bg=common.PANEL_BG)
        form_widgets["date"] = common.make_entry(date_row, width=12,
                                                 tip="The new day, as YYYY-MM-DD, or click the calendar.")
        form_widgets["date"].pack(side="left")

        def on_pick_date():
            """Open the calendar for the new date."""
            common.open_date_picker(form_frame, form_widgets["date"], allow_past=False)

        common.make_button(date_row, "\U0001F4C5", on_pick_date, style="light",
                           tip="Open a calendar and click the new day.").pack(side="left", padx=(4, 0))
        common.add_form_row(form_frame, 0, "New date", date_row, tip="The day to move the booking to.")
        form_widgets["start"] = tk.StringVar(value="")
        form_widgets["start_menu"] = common.make_option_menu(form_frame, form_widgets["start"], [], width=8,
                                                             tip="The new start time. The booking keeps its "
                                                                 "length, so it must end by closing time.")
        common.add_form_row(form_frame, 1, "Start time", form_widgets["start_menu"], tip="The new start time.")
        form_widgets["court"] = tk.StringVar(value="")
        form_widgets["court_menu"] = common.make_option_menu(form_frame, form_widgets["court"], [], width=8,
                                                             tip="The court to use (same sport).")
        common.add_form_row(form_frame, 2, "Court", form_widgets["court_menu"], tip="The court to use.")

    def fill_form(booking_id):
        """Start the form at the booking's current date, time and court."""
        booking = find_booking_by_id(load_all_bookings(), booking_id)
        if booking is None:
            return
        form_widgets["date"].delete(0, tk.END)
        form_widgets["date"].insert(0, booking.get_date_text())
        start_choices = []
        for hour in range(common.OPENING_HOUR, common.CLOSING_HOUR - booking.get_duration_hrs() + 1):
            start_choices.append(hour_choice_text(hour))
        form_widgets["start"].set(hour_choice_text(booking.get_start_hour()))
        common.set_option_menu_choices(form_widgets["start_menu"], form_widgets["start"], start_choices)
        court_choices = []
        for court_no in range(1, common.SPORTS[booking.get_sport()]["courts"] + 1):
            court_choices.append(f"Court {court_no}")
        form_widgets["court"].set(f"Court {booking.get_court_no()}")
        common.set_option_menu_choices(form_widgets["court_menu"], form_widgets["court"], court_choices)

    def chosen_values():
        """Return (date_text, start_hour, court_no) typed in the form."""
        start_text = form_widgets["start"].get()
        court_text = form_widgets["court"].get()
        if start_text == "" or court_text == "":
            raise ValueError("Pick the new start time and court.")
        return form_widgets["date"].get().strip(), int(start_text[0:2]), int(court_text.split(" ")[1])

    def reschedule_action(booking_id):
        """Move the picked booking."""
        date_text, start_hour, court_no = chosen_values()
        moved = reschedule_booking(booking_id, date_text, start_hour, court_no)
        return (f"Booking {booking_id} moved to {moved.get_date_text()} {booking_time_text(moved)}, "
                f"{moved.get_sport()} Court {moved.get_court_no()}.")

    def reschedule_question(booking_id):
        """Confirmation question naming the old and new times."""
        booking = find_booking_by_id(load_all_bookings(), booking_id)
        try:
            date_text, start_hour, court_no = chosen_values()
        except ValueError:
            return f"Reschedule booking {booking_id}?"
        if booking is None:
            return f"Reschedule booking {booking_id}?"
        end_hour = start_hour + booking.get_duration_hrs()
        return (f"Move booking {booking_id} from {booking.get_date_text()} {booking_time_text(booking)} "
                f"Court {booking.get_court_no()}\nto {date_text} {start_hour:02d}:00-{end_hour:02d}:00 "
                f"Court {court_no}?")

    return common.build_pick_page(page_frame, UPCOMING_LIST_HEADER, upcoming_rows, "Reschedule",
                                  reschedule_action, describe=describe_booking, build_form=build_form,
                                  fill_form=fill_form, confirm_text=reschedule_question,
                                  search_label=SEARCH_LABEL, empty_text="No upcoming bookings.",
                                  action_tip="Move the booking you clicked to the date, time and court above.")


def upcoming_rows(search_text):
    """Upcoming confirmed bookings, for the Reschedule list."""
    return booking_rows(search_text, True)


def build_book_page(section_frame, page_hooks):
    """Build the Book a Court page: date + sport pickers, the
    courts-by-hours grid, and the member picker with a Book button."""
    grid_state = {"sport": list(common.SPORTS.keys())[0], "court": None, "hours": [], "date": "",
                  "members_date": ""}
    sport_buttons = {}
    member_choice_ids = {}

    # --- top row: date and sport ---
    controls_row = tk.Frame(section_frame, bg=common.APP_BG)
    controls_row.pack(side="top", fill="x")
    tk.Label(controls_row, text="Date", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left")
    date_entry = common.make_entry(controls_row, width=12, tip="The day to check and book. Type it as YYYY-MM-DD, or click the calendar button.")
    date_entry.pack(side="left", padx=(6, 4))
    date_entry.insert(0, common.today_string())

    info_label = tk.Label(section_frame, text="", font=common.LABEL_FONT, bg=common.APP_BG,
                          fg=common.MUTED_TEXT_COLOR, anchor="w")
    grid_frame = tk.Frame(section_frame, bg=common.APP_BG)

    # --- bottom bar: member, selection summary, Book (packed first so the
    # grid can never squeeze it out of view) ---
    book_bar = common.make_card(section_frame)
    book_bar.pack(side="bottom", fill="x", pady=(8, 0))
    info_label.pack(side="top", fill="x", pady=(8, 4))
    grid_frame.pack(side="top", fill="both", expand=True)

    tk.Label(book_bar, text="Member", font=common.LABEL_FONT, bg=common.PANEL_BG).pack(side="left")
    member_variable = tk.StringVar(value="")
    def on_member_picked(chosen_text):
        """A member was picked: Book can be used once hours are chosen too."""
        update_selection_label()

    member_menu, member_dropdown, set_member_choices = common.make_filtered_menu(
        book_bar, member_variable, width=MEMBER_MENU_WIDTH, command=on_member_picked,
        tip="The member who is booking (members whose membership is valid on this date). "
            "Their bill is made later in Billing.")
    member_menu.pack(side="left", padx=(6, 12))
    selection_label = tk.Label(book_bar, text="", font=common.LABEL_FONT, bg=common.PANEL_BG)
    selection_label.pack(side="left")

    def draw_grid():
        """Redraw the whole grid for the chosen date and sport: one row per
        court, one column per opening hour."""
        for child_widget in grid_frame.winfo_children():
            child_widget.destroy()
        sport = grid_state["sport"]
        date_text = date_entry.get().strip()
        shown_date["text"] = date_text
        if not common.is_valid_date(date_text):
            info_label.config(text="Type a date as YYYY-MM-DD, or click the calendar.")
            update_selection_label()
            return
        # Compare in the standard form, so a date typed as 2027-1-5 still
        # matches bookings saved as 2027-01-05.
        date_text = common.normalize_date(date_text)
        grid_state["date"] = date_text
        if grid_state["members_date"] != date_text:
            refresh_member_choices(date_text)

        grid, hour_list, court_count = build_availability_grid(sport, date_text)
        booking_list = load_all_bookings()
        today = common.today_string()
        current_hour = common.current_hour()

        # Hours that have already started today (or any hour on a past
        # date) cannot be booked, so they are shown grey.
        past_hours = set()
        for hour in hour_list:
            if date_text < today or (date_text == today and hour <= current_hour):
                past_hours.add(hour)
        # A past hour is never "free": mark it so the count and the
        # earliest-free search below skip it.
        for row_index in range(len(hour_list)):
            if hour_list[row_index] in past_hours:
                for court_index in range(court_count):
                    grid[row_index][court_index] = "Past"

        # Info line: price, how many slots are free (recursive count) and
        # the earliest free slot (found by a while-loop scan per court).
        free_count = count_free_slots_recursive(grid)
        first_free_text = "none"
        first_free_hour = None
        for court_index in range(court_count):
            next_hour = find_next_free_hour(grid, hour_list, court_index)
            if next_hour is not None and (first_free_hour is None or next_hour < first_free_hour):
                first_free_hour = next_hour
                first_free_text = f"Court {court_index + 1} at {next_hour:02d}:00"
        if date_text < today:
            info_label.config(text=f"{date_text} has passed, so it can't be booked. Pick today or a later date.")
        else:
            info_label.config(text=(f"{sport}: RM {common.SPORTS[sport]['rate']:.0f} per hour.   "
                                    f"{free_count} free 1-hour slots left on {date_text}.   "
                                    f"Earliest free: {first_free_text}"))

        tk.Label(grid_frame, text="Start time", font=common.SMALL_FONT, bg=common.APP_BG,
                 fg=common.MUTED_TEXT_COLOR, anchor="w").grid(row=0, column=0, sticky="w")
        for column_index in range(len(hour_list)):
            hour_label = tk.Label(grid_frame, text=f"{hour_list[column_index]:02d}:00", font=common.SMALL_FONT,
                                  bg=common.APP_BG, fg=common.MUTED_TEXT_COLOR)
            hour_label.grid(row=0, column=column_index + 1)
            common.add_tooltip(hour_label, (f"The 1-hour slot from {hour_list[column_index]:02d}:00 to "
                                            f"{hour_list[column_index] + 1:02d}:00."))

        for court_index in range(court_count):
            court_no = court_index + 1
            court_label = tk.Label(grid_frame, text=f"Court {court_no}", font=common.BUTTON_FONT, bg=common.APP_BG,
                                   anchor="w")
            court_label.grid(row=court_no, column=0, sticky="w", padx=(0, 8), pady=2)
            common.add_tooltip(court_label, f"{sport} court number {court_no}. Each square to the right is one hour.")
            for row_index in range(len(hour_list)):
                hour = hour_list[row_index]
                is_selected = (grid_state["court"] == court_no and hour in grid_state["hours"])
                cell_fg = common.TEXT_COLOR
                if hour in past_hours:
                    cell_bg, cell_text, cell_state = common.PAST_COLOR, "", "disabled"
                elif grid[row_index][court_index] == "Booked":
                    cell_bg, cell_text, cell_state = common.BOOKED_COLOR, "✕", "normal"
                elif is_selected:
                    # Dark text on the amber cell, readable in both themes.
                    cell_bg, cell_text, cell_state = common.SELECTED_COLOR, "✓", "normal"
                    cell_fg = common.SELECTED_TEXT_COLOR
                else:
                    cell_bg, cell_text, cell_state = common.FREE_COLOR, "", "normal"
                cell = tk.Button(grid_frame, text=cell_text, width=4, height=2, font=common.BUTTON_FONT,
                                 bg=cell_bg, activebackground=cell_bg, fg=cell_fg, activeforeground=cell_fg,
                                 relief="flat", bd=0,
                                 state=cell_state, cursor="hand2",
                                 command=make_cell_command(booking_list, court_no, hour,
                                                           grid[row_index][court_index]))
                cell.grid(row=court_no, column=row_index + 1, padx=1, pady=2)
                common.add_tooltip(cell, cell_tip_text(court_no, hour, cell_bg, sport))

        legend_row = tk.Frame(grid_frame, bg=common.APP_BG)
        legend_row.grid(row=court_count + 1, column=0, columnspan=len(hour_list) + 1, sticky="w", pady=(8, 0))
        for legend_text, legend_color in (("Free", common.FREE_COLOR), ("Booked", common.BOOKED_COLOR),
                                          ("Selected", common.SELECTED_COLOR), ("Past", common.PAST_COLOR)):
            tk.Label(legend_row, text="   ", bg=legend_color).pack(side="left")
            tk.Label(legend_row, text=legend_text, font=common.SMALL_FONT, bg=common.APP_BG).pack(
                side="left", padx=(4, 14))
        update_selection_label()

    def cell_tip_text(court_no, hour, cell_bg, sport):
        """Return the hover hint for one grid cell, based on its colour."""
        slot_text = f"Court {court_no}, {hour:02d}:00-{hour + 1:02d}:00"
        if cell_bg == common.PAST_COLOR:
            return f"{slot_text}: this time has already passed."
        elif cell_bg == common.BOOKED_COLOR:
            return f"{slot_text}: already booked. Click to see which booking."
        elif cell_bg == common.SELECTED_COLOR:
            return f"{slot_text}: selected. Click it again to clear your selection."
        return (f"{slot_text}: free, RM {common.SPORTS[sport]['rate']:.2f} for this hour. Click to select it; "
                "then click the hour next to it on the same court to book longer.")

    def make_cell_command(booking_list, court_no, hour, cell_value):
        """Return the command for one grid cell."""
        def cell_command():
            """Handle a click on this grid cell."""
            if cell_value == "Booked":
                covering = find_booking_at(booking_list, grid_state["sport"], court_no,
                                           grid_state["date"], hour)
                if covering is not None:
                    messagebox.showinfo("Booked", (f"Court {court_no} at {hour:02d}:00 is booked\n"
                                                   f"({covering.get_booking_id()}, {booking_time_text(covering)})."))
                return
            on_free_cell_clicked(court_no, hour)
        return cell_command

    def on_free_cell_clicked(court_no, hour):
        """Grow, start or clear the selection. A booking must be one
        unbroken block on one court, so a click next to the current
        selection extends it and any other click starts a new one."""
        selected_hours = grid_state["hours"]
        if grid_state["court"] == court_no and hour in selected_hours:
            grid_state["court"] = None
            grid_state["hours"] = []
        elif (grid_state["court"] == court_no and len(selected_hours) > 0
              and (hour == min(selected_hours) - 1 or hour == max(selected_hours) + 1)):
            selected_hours.append(hour)
        else:
            grid_state["court"] = court_no
            grid_state["hours"] = [hour]
        draw_grid()

    def update_selection_label():
        """Describe the current selection and its price next to Book."""
        selected_hours = grid_state["hours"]
        if len(selected_hours) == 0:
            selection_label.config(text="Click free hours in the grid to choose a time.")
            book_button.config(state="disabled")
            return
        start_hour = min(selected_hours)
        end_hour = max(selected_hours) + 1
        price = common.SPORTS[grid_state["sport"]]["rate"] * len(selected_hours)
        selection_text = (f"Court {grid_state['court']}, {start_hour:02d}:00-{end_hour:02d}:00 "
                          f"({len(selected_hours)} hour(s))  =  RM {price:.2f}")
        if member_variable.get() in member_choice_ids:
            selection_label.config(text=selection_text)
            book_button.config(state="normal")
        else:
            selection_label.config(text=selection_text + "   - now choose the member.")
            book_button.config(state="disabled")

    def clear_selection_and_redraw():
        """Forget the selection (the date or sport changed) and redraw."""
        grid_state["court"] = None
        grid_state["hours"] = []
        draw_grid()

    def on_pick_date():
        """Open the calendar pop-up; redraw the grid once a day is picked."""
        common.open_date_picker(section_frame, date_entry, on_picked=clear_selection_and_redraw,
                                allow_past=False)

    shown_date = {"text": ""}

    def on_date_typed(event):
        """Redraw the grid when Enter is pressed, or once the box holds a
        full 10-character date (YYYY-MM-DD) that differs from the one
        shown - so typing 2026-12-25 doesn't redraw for 2026-12-2 first."""
        date_text = date_entry.get().strip()
        full_date = len(date_text) == 10 and common.is_valid_date(date_text)
        if event.keysym == "Return" or (full_date and date_text != shown_date["text"]):
            clear_selection_and_redraw()

    def on_date_left(event):
        """Leaving the box (e.g. after a mouse paste): redraw if it now
        holds a different day from the grid."""
        if date_entry.get().strip() != shown_date["text"]:
            clear_selection_and_redraw()

    date_entry.bind("<KeyRelease>", on_date_typed)
    date_entry.bind("<FocusOut>", on_date_left)
    common.make_button(controls_row, "\U0001F4C5", on_pick_date, style="light",
                       tip="Open a calendar and click a day to show that day's courts.").pack(side="left")
    tk.Label(controls_row, text="Sport", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left", padx=(24, 6))

    def make_sport_command(sport_name):
        """Return the command for one sport button."""
        def sport_command():
            """Show the grid for this sport."""
            grid_state["sport"] = sport_name
            highlight_sport()
            clear_selection_and_redraw()
        return sport_command

    def highlight_sport():
        """Show which sport button is currently chosen."""
        for sport_name in sport_buttons:
            if sport_name == grid_state["sport"]:
                sport_buttons[sport_name].config(bg=common.BUTTON_COLOR, fg=common.BUTTON_TEXT_COLOR)
            else:
                sport_buttons[sport_name].config(bg=common.PANEL_BG, fg=common.ACCENT_COLOR)

    for sport_name in common.SPORTS:
        sport_info = common.SPORTS[sport_name]
        sport_button = common.make_button(controls_row, sport_name, make_sport_command(sport_name), style="light",
                                          tip=(f"Show the {sport_info['courts']} {sport_name} court(s). "
                                               f"Price: RM {sport_info['rate']:.2f} per hour."))
        sport_button.pack(side="left", padx=2)
        sport_buttons[sport_name] = sport_button

    def on_save_day_sheet():
        """Save the shown day's bookings (all sports) to a text file."""
        try:
            sheet_path = save_day_sheet(grid_state["date"])
        except (ValueError, OSError) as error:
            show_problem(error)
            return
        messagebox.showinfo("Day sheet saved", f"Bookings for {grid_state['date']} saved to:\n{sheet_path}")

    common.make_button(controls_row, "Save Day Sheet", on_save_day_sheet, style="light",
                       tip="Save every sport's bookings for the date shown to a text file you can print "
                           "(data/day_sheets).").pack(side="right")

    def on_book():
        """Book the selected hours for the chosen member, on the date the
        GRID shows (if the box was changed without a redraw, redraw first)."""
        if member_variable.get() not in member_choice_ids:
            messagebox.showerror("Please check", "Pick the member who is booking.")
            return
        if date_entry.get().strip() != shown_date["text"]:
            clear_selection_and_redraw()
            messagebox.showerror("Please check", ("The date box was changed, so the grid now shows "
                                                  f"{date_entry.get().strip()}. Pick the hours again."))
            return
        selected_hours = grid_state["hours"]
        try:
            new_booking = create_booking(member_choice_ids[member_variable.get()], grid_state["sport"],
                                         grid_state["court"], grid_state["date"],
                                         min(selected_hours), len(selected_hours))
        except (ValueError, OSError) as error:
            show_problem(error)
            return
        messagebox.showinfo("Booked", (f"Booking {new_booking.get_booking_id()} confirmed.\n"
                                       f"{new_booking.get_sport()} Court {new_booking.get_court_no()}, "
                                       f"{new_booking.get_date_text()} {booking_time_text(new_booking)}\n"
                                       f"Price: RM {new_booking.get_price():.2f}"))
        clear_selection_and_redraw()

    book_button = common.make_button(book_bar, "Book", on_book,
                                     tip="Book the hours you selected in the grid for the chosen member. "
                                         "Select at least one free hour first.")
    book_button.pack(side="right")

    def refresh_member_choices(date_text):
        """List the members whose membership is valid on date_text. The
        menu shows each choice cut to its width, so the lookup uses that."""
        member_choice_ids.clear()
        member_choices = []
        for member_id, member_name in members_valid_on(date_text):
            choice_text = f"{member_id} {member_name}"
            member_choice_ids[common.fit_text(choice_text, MEMBER_MENU_WIDTH)] = member_id
            member_choices.append(choice_text)
        set_member_choices(member_choices)
        grid_state["members_date"] = date_text

    def on_show():
        """Start fresh whenever this page opens: today's date, no hours
        picked, the member list reloaded, the grid redrawn."""
        date_entry.delete(0, tk.END)
        date_entry.insert(0, common.today_string())
        grid_state["members_date"] = ""
        member_variable.set(common.CHOOSE_TEXT)
        highlight_sport()
        clear_selection_and_redraw()

    page_hooks["Book a Court"] = on_show
