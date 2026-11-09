"""
Module      : booking.py
Author      : Teh Tze Ken
Purpose     : Facility & Court Booking module - a visual grid of court
              availability per hour for each sport, booking by clicking
              free slots, and viewing/cancelling bookings.
Date        : 2026-11-07
"""

import tkinter as tk
from tkinter import messagebox

import common


# ---------------------------------------------------------------------------
# CLASS (encapsulation)
# ---------------------------------------------------------------------------
class Booking:
    """A single court booking with private attributes, getters and setters."""

    def __init__(self, booking_id, member_id, sport, court_no, date_text,
                 start_hour, duration_hrs, status):
        """Create the object and validate its starting values."""
        self.__booking_id = booking_id
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
        """Return the booking ID."""
        return self.__booking_id

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
        return "|".join([
            self.__booking_id, self.__member_id, self.__sport, str(self.__court_no),
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


def has_clash(booking_list, sport, court_no, date_text, start_hour, duration_hrs):
    """Return True if an existing CONFIRMED booking overlaps this slot.
    Builds the set of hours being requested and, for each candidate
    booking on the same sport/court/date, the set of hours it already
    occupies - if the two sets share any hour, the slots clash."""
    requested_hours = set(range(start_hour, start_hour + duration_hrs))
    for booking in booking_list:
        if booking.get_status() != "CONFIRMED":
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
    if not member_exists(member_id):
        raise ValueError(f"No member found with ID {member_id}.")
    if not common.is_valid_date(date_text):
        raise ValueError("Booking date must be a real date in YYYY-MM-DD form.")
    # One standard form (2027-1-5 -> 2027-01-05), so clash checks compare like with like.
    date_text = common.normalize_date(date_text)
    if date_text < common.today_string():
        raise ValueError("You cannot book a date in the past.")
    if date_text == common.today_string() and start_hour <= common.current_hour():
        raise ValueError(f"{start_hour:02d}:00 has already started today. Pick a later time.")

    booking_list = load_all_bookings()
    if has_clash(booking_list, sport, court_no, date_text, start_hour, duration_hrs):
        raise ValueError("This court is already booked for the selected time.")

    new_id = common.generate_id(common.BOOKINGS_FILE, "BKG")
    new_booking = Booking(new_id, member_id, sport, court_no, date_text, start_hour, duration_hrs, "CONFIRMED")
    common.append_line(common.BOOKINGS_FILE, new_booking.to_line())
    return new_booking


def search_bookings(booking_list, search_field, search_text):
    """Search bookings by 'id', 'member', 'date' or 'sport'."""
    results = []
    search_text_lower = search_text.strip().lower()
    for booking in booking_list:
        match search_field:
            case "id":
                if booking.get_booking_id().lower() == search_text_lower:
                    results.append(booking)
            case "member":
                if booking.get_member_id().lower() == search_text_lower:
                    results.append(booking)
            case "date":
                if booking.get_date_text() == search_text.strip():
                    results.append(booking)
            case "sport":
                if booking.get_sport().lower() == search_text_lower:
                    results.append(booking)
    return results


def cancel_booking(booking_id):
    """Set a booking's status to CANCELLED. Blocked if it is already
    CANCELLED, so clicking Cancel twice gives a clear message."""
    booking_list = load_all_bookings()
    booking_found = False
    for booking in booking_list:
        if booking.get_booking_id() == booking_id:
            booking_found = True
            if booking.get_status() == "CANCELLED":
                raise ValueError("This booking is already cancelled.")
            booking.set_status("CANCELLED")
    if not booking_found:
        raise ValueError(f"No booking found with ID {booking_id}.")

    updated_lines = []
    for booking in booking_list:
        updated_lines.append(booking.to_line())
    common.rewrite_records(common.BOOKINGS_FILE, updated_lines, line_to_booking)


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
#   Book a Court     - date + sport, a courts x hours grid, click free
#                      hours, pick the member, click Book
#   Cancel a Booking - pick a confirmed booking, click Cancel Booking
# Cancelled bookings are never deleted: they stay on record as CANCELLED.
# ---------------------------------------------------------------------------
BOOKING_ACTIONS = [
    ("Book a Court", "See free courts and book one",
     "Pick a date and a sport. Click a free (green) hour - click the next hour on the same "
     "court to book longer. Choose the member, then click Book."),
    ("Cancel a Booking", "Cancel a confirmed booking",
     "Click the booking to cancel, then click Cancel Booking. Type a Member ID and click "
     "Search to find someone's bookings."),
]

BOOKING_LIST_HEADER = f"{'Booking ID':<11}{'Date':<11}{'Time':<12}{'Sport':<10}{'Court':<6}{'Member ID':<9}"


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
    page_hooks["Cancel a Booking"] = build_cancel_page(page_frames["Cancel a Booking"])
    return window


def booking_rows(status, search_text):
    """Return (booking_id, row_text) for bookings with this status,
    soonest first, filtered by member ID if search_text is given."""
    booking_list = load_all_bookings()
    if search_text != "":
        booking_list = search_bookings(booking_list, "member", search_text)
    sort_rows = []
    for booking in booking_list:
        if booking.get_status() == status:
            sort_rows.append((booking.get_date_text(), booking.get_start_hour(), booking.get_booking_id(), booking))
    sort_rows.sort()
    rows = []
    for date_text, start_hour, booking_id, booking in sort_rows:
        rows.append((booking_id, (f"{booking_id:<11}{date_text:<11}{booking_time_text(booking):<12}"
                                  f"{booking.get_sport():<10}{booking.get_court_no():<6}"
                                  f"{booking.get_member_id():<8}")))
    return rows


def describe_booking(booking_id):
    """Return the details text for one booking."""
    for booking in load_all_bookings():
        if booking.get_booking_id() == booking_id:
            return common.details_text([
                ("Booking ID", booking.get_booking_id()),
                ("Sport", booking.get_sport()),
                ("Court", booking.get_court_no()),
                ("Date", booking.get_date_text()),
                ("Time", booking_time_text(booking)),
                ("Duration", f"{booking.get_duration_hrs()} hour(s)"),
                ("Member ID", booking.get_member_id()),
                ("Price", f"RM {booking.get_price():.2f}"),
                ("Status", booking.get_status()),
            ])
    return "This booking no longer exists."


def build_cancel_page(page_frame):
    """Build the Cancel a Booking page and return its refresh function.
    Cancelled bookings are kept on record (status CANCELLED), never
    deleted, so the centre keeps a full history."""

    def load_rows(search_text):
        """Confirmed bookings only."""
        return booking_rows("CONFIRMED", search_text)

    def cancel_action(booking_id):
        """Cancel the picked booking."""
        cancel_booking(booking_id)
        return f"Booking {booking_id} cancelled. It stays on record as CANCELLED."

    def cancel_question(booking_id):
        """Confirmation question for cancelling."""
        return f"Cancel booking {booking_id}? This frees the court for others to book."

    return common.build_pick_page(page_frame, BOOKING_LIST_HEADER, load_rows, "Cancel Booking",
                                  cancel_action, describe=describe_booking, confirm_text=cancel_question,
                                  danger=True, search_label="Member ID", empty_text="No confirmed bookings.",
                                  action_tip="Cancel the booking you clicked. It stays on record as CANCELLED.")


def build_book_page(section_frame, page_hooks):
    """Build the Book a Court page: date + sport pickers, the
    courts-by-hours grid, and the member picker with a Book button."""
    grid_state = {"sport": list(common.SPORTS.keys())[0], "court": None, "hours": [], "date": ""}
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
    member_menu, member_dropdown, set_member_choices = common.make_filtered_menu(book_bar, member_variable, width=24,
                                          tip="The member who is booking. Their bill is made later in Billing.")
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
        info_label.config(text=(f"{sport}: RM {common.SPORTS[sport]['rate']:.0f} per hour.   "
                                f"{free_count} free 1-hour slots on {date_text}.   "
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
                if hour in past_hours:
                    cell_bg, cell_text, cell_state = common.PAST_COLOR, "", "disabled"
                elif grid[row_index][court_index] == "Booked":
                    cell_bg, cell_text, cell_state = common.BOOKED_COLOR, "✕", "normal"
                elif is_selected:
                    cell_bg, cell_text, cell_state = common.SELECTED_COLOR, "✓", "normal"
                else:
                    cell_bg, cell_text, cell_state = common.FREE_COLOR, "", "normal"
                cell = tk.Button(grid_frame, text=cell_text, width=4, height=2, font=common.BUTTON_FONT,
                                 bg=cell_bg, activebackground=cell_bg, relief="flat", bd=0,
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
        selection_label.config(text=(f"Court {grid_state['court']}, {start_hour:02d}:00-{end_hour:02d}:00 "
                                     f"({len(selected_hours)} hour(s))  =  RM {price:.2f}"))
        book_button.config(state="normal")

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
        """Redraw the grid as soon as the date box holds a complete, real
        date that differs from the one shown (or when Enter is pressed),
        so the grid never shows a different day from the box."""
        date_text = date_entry.get().strip()
        if event.keysym == "Return" or (common.is_valid_date(date_text) and date_text != shown_date["text"]):
            clear_selection_and_redraw()

    date_entry.bind("<KeyRelease>", on_date_typed)
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

    def on_book():
        """Book the selected hours for the chosen member."""
        if member_variable.get() not in member_choice_ids:
            messagebox.showerror("Please check", "Pick the member who is booking.")
            return
        selected_hours = grid_state["hours"]
        try:
            new_booking = create_booking(member_choice_ids[member_variable.get()], grid_state["sport"],
                                         grid_state["court"], date_entry.get().strip(),
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

    def on_show():
        """Reload members and redraw the grid whenever this page opens."""
        member_choice_ids.clear()
        member_choices = []
        member_names = load_member_names()
        for member_id in member_names:
            choice_text = f"{member_id} {member_names[member_id]}"
            member_choice_ids[choice_text] = member_id
            member_choices.append(choice_text)
        set_member_choices(member_choices)
        highlight_sport()
        draw_grid()

    page_hooks["Book a Court"] = on_show
