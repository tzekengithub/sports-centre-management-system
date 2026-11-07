"""
Module      : coaching.py
Author      : Tan Chor Koon
Purpose     : Coaching & Class Management module - assigns coaches to
              private sessions or group classes, enrols members, and
              tracks each coach's working hours and commission.
Date        : 2026-11-07
"""

import tkinter as tk
from tkinter import messagebox

import common


# Limits used to reject silly or dangerous input (e.g. "inf" or 99999).
MIN_HOURLY_RATE = 1.0
MAX_HOURLY_RATE = 500.0
MAX_COMMISSION_PCT = 100.0
MAX_CLASS_FEE = 1000.0
MAX_CLASS_DURATION = 4
MAX_GROUP_SIZE = 30


# ---------------------------------------------------------------------------
# CLASS (encapsulation + inheritance from common.Person)
# ---------------------------------------------------------------------------
class Coach(common.Person):
    """A coach. Inherits name/phone handling from Person and adds
    coaching-specific private attributes."""

    def __init__(self, coach_id, name, phone, sport, hourly_rate, commission_pct):
        """Create the object and validate its starting values."""
        super().__init__(name, phone)
        self.__coach_id = coach_id
        self.__sport = ""
        self.__hourly_rate = 0.0
        self.__commission_pct = 0.0
        self.set_sport(sport)
        self.set_hourly_rate(hourly_rate)
        self.set_commission_pct(commission_pct)

    def get_coach_id(self):
        """Return the coach's ID."""
        return self.__coach_id

    def get_sport(self):
        """Return the sport this coach teaches."""
        return self.__sport

    def set_sport(self, sport):
        """Validate and store the sport (must be one of COACHING_SPORTS)."""
        if sport not in common.COACHING_SPORTS:
            raise ValueError("Please choose a sport from the list.")
        self.__sport = sport

    def get_hourly_rate(self):
        """Return the coach's hourly rate."""
        return self.__hourly_rate

    def set_hourly_rate(self, hourly_rate):
        """Validate and store the hourly rate. Written as 'not (a <= x <= b)'
        so nan, which fails every comparison, is rejected too."""
        if not (MIN_HOURLY_RATE <= hourly_rate <= MAX_HOURLY_RATE):
            raise ValueError(f"Hourly rate must be between RM {MIN_HOURLY_RATE:g} and RM {MAX_HOURLY_RATE:g}.")
        self.__hourly_rate = hourly_rate

    def get_commission_pct(self):
        """Return the coach's commission percentage."""
        return self.__commission_pct

    def set_commission_pct(self, commission_pct):
        """Validate and store the commission percentage (nan rejected too)."""
        if not (0 <= commission_pct <= MAX_COMMISSION_PCT):
            raise ValueError(f"Commission must be between 0 and {MAX_COMMISSION_PCT:g} %.")
        self.__commission_pct = commission_pct

    def to_line(self):
        """Turn this coach into a pipe-delimited text-file line."""
        return "|".join([
            self.__coach_id, self.get_name(), self.get_phone(), self.__sport,
            f"{self.__hourly_rate:.2f}", f"{self.__commission_pct:.2f}",
        ])


# ---------------------------------------------------------------------------
# LOGIC LAYER - COACHES
# ---------------------------------------------------------------------------
COACH_FIELD_COUNT = 6
CLASS_FIELD_COUNT = 10
MEMBER_FIELD_COUNT = 6


def line_to_coach(line):
    """Convert one text-file line into a Coach object, or None if the
    line is malformed."""
    fields = common.split_fields(line, COACH_FIELD_COUNT)
    if fields is None:
        return None
    try:
        return Coach(fields[0], fields[1], fields[2], fields[3], float(fields[4]), float(fields[5]))
    except ValueError:
        return None


def load_all_coaches():
    """Read coaches.txt and return a list of Coach objects. Malformed
    lines are skipped rather than crashing the program."""
    coach_list = []
    for line in common.read_lines(common.COACHES_FILE):
        coach = line_to_coach(line)
        if coach is not None:
            coach_list.append(coach)
    return coach_list


def find_coach_by_id(coach_list, coach_id):
    """Linear search for a coach by ID using a while loop. Returns the
    Coach or None."""
    index = 0
    while index < len(coach_list):
        if coach_list[index].get_coach_id() == coach_id:
            return coach_list[index]
        index += 1
    return None


def register_coach(name, phone, sport, hourly_rate, commission_pct):
    """Validate input, build a new Coach, append it to the file, return it."""
    new_id = common.generate_id(common.COACHES_FILE, "CCH")
    new_coach = Coach(new_id, name, phone, sport, hourly_rate, commission_pct)
    common.append_line(common.COACHES_FILE, new_coach.to_line())
    return new_coach


def search_coaches(coach_list, search_field, search_text):
    """Search coaches by 'id', 'name' (partial) or 'sport'."""
    results = []
    search_text_lower = search_text.strip().lower()
    for coach in coach_list:
        match search_field:
            case "id":
                if coach.get_coach_id().lower() == search_text_lower:
                    results.append(coach)
            case "name":
                if search_text_lower in coach.get_name().lower():
                    results.append(coach)
            case "sport":
                if coach.get_sport().lower() == search_text_lower:
                    results.append(coach)
    return results


def update_coach(coach_id, new_name, new_phone, new_sport, new_rate, new_commission):
    """Update an existing coach's details. If the sport changes, the
    coach's upcoming classes (today or later) are moved to the new sport
    too, so they never show the old one. Past classes keep their sport,
    because that is what was actually taught. Returns how many classes
    were changed."""
    coach_list = load_all_coaches()
    coach_record = find_coach_by_id(coach_list, coach_id)
    if coach_record is None:
        raise ValueError(f"No coach found with ID {coach_id}.")
    old_sport = coach_record.get_sport()

    coach_record.set_name(new_name)
    coach_record.set_phone(new_phone)
    coach_record.set_sport(new_sport)
    coach_record.set_hourly_rate(new_rate)
    coach_record.set_commission_pct(new_commission)

    updated_lines = []
    for coach in coach_list:
        updated_lines.append(coach.to_line())
    common.write_lines(common.COACHES_FILE, updated_lines)

    changed_class_count = 0
    if new_sport != old_sport:
        today = common.today_string()
        class_list = load_all_classes()
        class_lines = []
        for sports_class in class_list:
            if sports_class.coach_id == coach_id and sports_class.date_text >= today:
                sports_class.sport = new_sport
                changed_class_count += 1
            class_lines.append(sports_class.to_line())
        common.write_lines(common.CLASSES_FILE, class_lines)
    return changed_class_count


def count_classes_for_coach(coach_id):
    """Return how many classes (past or upcoming) coach_id is linked to."""
    class_count = 0
    for line in common.read_lines(common.CLASSES_FILE):
        fields = common.split_fields(line, CLASS_FIELD_COUNT)
        if fields is not None and fields[1] == coach_id:
            class_count += 1
    return class_count


def delete_coach(coach_id):
    """Delete a coach permanently. Blocked while ANY class (past or
    upcoming) still points to this coach: otherwise the freed ID could be
    reused by the next new coach, and the old classes (with their hours
    and commission) would wrongly show up under that new person."""
    class_count = count_classes_for_coach(coach_id)
    if class_count > 0:
        raise ValueError(f"Cannot remove coach {coach_id}: {class_count} class(es) are still on "
                         "record for them (including past ones). Cancel those classes first.")
    coach_list = load_all_coaches()
    remaining_lines = []
    coach_found = False
    for coach in coach_list:
        if coach.get_coach_id() == coach_id:
            coach_found = True
        else:
            remaining_lines.append(coach.to_line())
    if not coach_found:
        raise ValueError(f"No coach found with ID {coach_id}.")
    common.write_lines(common.COACHES_FILE, remaining_lines)


# ---------------------------------------------------------------------------
# LOGIC LAYER - CLASSES
# ---------------------------------------------------------------------------
class SportsClass:
    """A scheduled coaching class (plain data holder, kept simple)."""

    def __init__(self, class_id, coach_id, sport, class_type, date_text, start_hour,
                 duration_hrs, max_pax, fee_per_pax, participants_text):
        """Create the object and validate its starting values."""
        self.class_id = class_id
        self.coach_id = coach_id
        self.sport = sport
        self.class_type = class_type
        self.date_text = date_text
        self.start_hour = start_hour
        self.duration_hrs = duration_hrs
        self.max_pax = max_pax
        self.fee_per_pax = fee_per_pax
        self.participants_text = participants_text

    def get_participant_list(self):
        """Split the ;-joined participants string into a list of member IDs."""
        if self.participants_text.strip() == "":
            return []
        return self.participants_text.split(";")

    def get_time_text(self):
        """Return the class time as e.g. '10:00-12:00'."""
        return f"{self.start_hour:02d}:00-{self.start_hour + self.duration_hrs:02d}:00"

    def to_line(self):
        """Turn this class into a pipe-delimited text-file line."""
        return "|".join([
            self.class_id, self.coach_id, self.sport, self.class_type, self.date_text,
            str(self.start_hour), str(self.duration_hrs), str(self.max_pax),
            f"{self.fee_per_pax:.2f}", self.participants_text,
        ])


def line_to_class(line):
    """Convert one text-file line into a SportsClass object, or None if
    the line is malformed."""
    fields = common.split_fields(line, CLASS_FIELD_COUNT)
    if fields is None:
        return None
    try:
        return SportsClass(fields[0], fields[1], fields[2], fields[3], fields[4],
                            int(fields[5]), int(fields[6]), int(fields[7]), float(fields[8]), fields[9])
    except ValueError:
        return None


def load_all_classes():
    """Read classes.txt and return a list of SportsClass objects.
    Malformed lines are skipped rather than crashing the program."""
    class_list = []
    for line in common.read_lines(common.CLASSES_FILE):
        sports_class = line_to_class(line)
        if sports_class is not None:
            class_list.append(sports_class)
    return class_list


def find_class_by_id(class_list, class_id):
    """Return the SportsClass with class_id from class_list, or None."""
    for sports_class in class_list:
        if sports_class.class_id == class_id:
            return sports_class
    return None


CLASS_TYPES = ("Private", "Group")


def coach_has_time_clash(class_list, coach_id, date_text, start_hour, duration_hrs, ignore_class_id=None):
    """Return True if coach_id already has a class overlapping this time
    slot. Two ranges [start, end) overlap when each one starts before the
    other ends."""
    new_end_hour = start_hour + duration_hrs
    for sports_class in class_list:
        if sports_class.coach_id != coach_id or sports_class.date_text != date_text:
            continue
        if ignore_class_id is not None and sports_class.class_id == ignore_class_id:
            continue
        existing_start_hour = sports_class.start_hour
        existing_end_hour = existing_start_hour + sports_class.duration_hrs
        if start_hour < existing_end_hour and new_end_hour > existing_start_hour:
            return True
    return False


def validate_class_details(class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax):
    """Check the details shared by scheduling and updating a class.
    Raises ValueError with a plain message for the first problem found."""
    if class_type not in CLASS_TYPES:
        raise ValueError("Class type must be Private or Group.")
    if not common.is_valid_date(date_text):
        raise ValueError("Class date must be a real date in YYYY-MM-DD form.")
    if date_text < common.today_string():
        raise ValueError("Class date cannot be in the past.")
    if duration_hrs < 1 or duration_hrs > MAX_CLASS_DURATION:
        raise ValueError(f"Duration must be between 1 and {MAX_CLASS_DURATION} hours.")
    if not common.is_valid_hour(start_hour) or not common.is_valid_hour(start_hour + duration_hrs - 1):
        raise ValueError(f"The class must fit within opening hours "
                         f"({common.OPENING_HOUR}:00-{common.CLOSING_HOUR}:00).")
    if class_type == "Private" and max_pax != 1:
        raise ValueError("A private session is for exactly 1 person.")
    if max_pax < 1 or max_pax > MAX_GROUP_SIZE:
        raise ValueError(f"Maximum people must be between 1 and {MAX_GROUP_SIZE}.")
    if not (0 < fee_per_pax <= MAX_CLASS_FEE):
        raise ValueError(f"Fee per person must be between RM 0.01 and RM {MAX_CLASS_FEE:g}.")


def schedule_class(coach_id, class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax):
    """Validate and create a new class. The class takes its sport from
    the coach. Raises ValueError on clash/invalid input."""
    coach_record = find_coach_by_id(load_all_coaches(), coach_id)
    if coach_record is None:
        raise ValueError(f"No coach found with ID {coach_id}.")
    validate_class_details(class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax)

    class_list = load_all_classes()
    if coach_has_time_clash(class_list, coach_id, date_text, start_hour, duration_hrs):
        raise ValueError("This coach already has a class at that time.")

    new_id = common.generate_id(common.CLASSES_FILE, "CLS")
    new_class = SportsClass(new_id, coach_id, coach_record.get_sport(), class_type, date_text,
                             start_hour, duration_hrs, max_pax, fee_per_pax, "")
    common.append_line(common.CLASSES_FILE, new_class.to_line())
    return new_class


def update_class(class_id, new_date_text, new_start_hour, new_duration_hrs, new_max_pax, new_fee_per_pax):
    """Update a class's date, hour, duration, maximum people and fee,
    re-checking the coach's time clash and that max_pax is not reduced
    below the number of members already enrolled."""
    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")

    validate_class_details(target_class.class_type, new_date_text, new_start_hour,
                           new_duration_hrs, new_max_pax, new_fee_per_pax)
    if new_max_pax < len(target_class.get_participant_list()):
        raise ValueError("Maximum people cannot be less than the number already enrolled.")
    if coach_has_time_clash(class_list, target_class.coach_id, new_date_text, new_start_hour,
                             new_duration_hrs, ignore_class_id=class_id):
        raise ValueError("This coach already has a class at that time.")

    target_class.date_text = new_date_text
    target_class.start_hour = new_start_hour
    target_class.duration_hrs = new_duration_hrs
    target_class.max_pax = new_max_pax
    target_class.fee_per_pax = new_fee_per_pax

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.write_lines(common.CLASSES_FILE, updated_lines)


def load_member_names():
    """Return a dictionary of member_id -> member name, read straight from
    members.txt (coaching does not import membership.py)."""
    member_names = {}
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            member_names[fields[0]] = fields[1]
    return member_names


def enrol_participant(class_id, member_id):
    """Add member_id to a class's participant list (no duplicates, capped at max_pax)."""
    if member_id not in load_member_names():
        raise ValueError(f"No member found with ID {member_id}.")

    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")

    participant_set = set(target_class.get_participant_list())
    if member_id in participant_set:
        raise ValueError("This member is already enrolled.")
    if len(participant_set) >= target_class.max_pax:
        raise ValueError("This class is already full.")
    participant_list = target_class.get_participant_list()
    participant_list.append(member_id)
    target_class.participants_text = ";".join(participant_list)

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.write_lines(common.CLASSES_FILE, updated_lines)


def remove_participant(class_id, member_id):
    """Remove member_id from a class's participant list."""
    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")
    participant_list = target_class.get_participant_list()
    if member_id not in participant_list:
        raise ValueError("This member is not enrolled in this class.")
    participant_list.remove(member_id)
    target_class.participants_text = ";".join(participant_list)

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.write_lines(common.CLASSES_FILE, updated_lines)


def search_classes(class_list, search_field, search_text):
    """Search classes by 'coach', 'date', 'sport' or 'type'."""
    results = []
    search_text_lower = search_text.strip().lower()
    for sports_class in class_list:
        match search_field:
            case "coach":
                if sports_class.coach_id.lower() == search_text_lower:
                    results.append(sports_class)
            case "date":
                if sports_class.date_text == search_text.strip():
                    results.append(sports_class)
            case "sport":
                if sports_class.sport.lower() == search_text_lower:
                    results.append(sports_class)
            case "type":
                if sports_class.class_type.lower() == search_text_lower:
                    results.append(sports_class)
    return results


def cancel_class(class_id):
    """Remove a class permanently from classes.txt."""
    class_list = load_all_classes()
    remaining_lines = []
    class_found = False
    for sports_class in class_list:
        if sports_class.class_id == class_id:
            class_found = True
        else:
            remaining_lines.append(sports_class.to_line())
    if not class_found:
        raise ValueError(f"No class found with ID {class_id}.")
    common.write_lines(common.CLASSES_FILE, remaining_lines)


def classes_in_month(class_list, month_text):
    """Return the classes whose date starts with month_text ('YYYY-MM').
    An empty month_text means every class."""
    if month_text == "":
        return class_list
    month_classes = []
    for sports_class in class_list:
        if sports_class.date_text.startswith(month_text):
            month_classes.append(sports_class)
    return month_classes


def coach_hours_by_month(class_list, month_text=""):
    """Return a dictionary of coach_id -> total hours of classes in
    month_text ('YYYY-MM'), or across all classes if month_text is empty."""
    hours_by_coach = {}
    for sports_class in classes_in_month(class_list, month_text):
        coach_id = sports_class.coach_id
        if coach_id in hours_by_coach:
            hours_by_coach[coach_id] += sports_class.duration_hrs
        else:
            hours_by_coach[coach_id] = sports_class.duration_hrs
    return hours_by_coach


def calculate_commission(sports_class, commission_pct):
    """Commission = fee_per_pax * number_of_participants * commission_pct / 100."""
    participant_count = len(sports_class.get_participant_list())
    return sports_class.fee_per_pax * participant_count * commission_pct / 100.0


def total_commission_recursive(class_list, coach_commission_pct, index=0):
    """Recursively total commission across class_list for a given commission
    percent, starting at index. Demonstrates recursion over a list."""
    if index >= len(class_list):
        return 0.0
    this_commission = calculate_commission(class_list[index], coach_commission_pct)
    return this_commission + total_commission_recursive(class_list, coach_commission_pct, index + 1)


# ---------------------------------------------------------------------------
# GUI LAYER
#
# The tab opens on a menu asking "What would you like to do?". Each
# action has its own one-page screen with a Back button:
#   Manage Coaches and Manage Classes (add, update and delete on one
#   page each: blank form adds, click a row to update, Delete beside it),
#   Enrol Member, Remove Member, Hours & Commission
# ---------------------------------------------------------------------------
COACHING_ACTIONS = [
    ("Manage Coaches", "Add, update or delete coaches",
     "Blank form = add a new coach. Click a coach to update them, then Save Changes. "
     "Click Delete beside a coach to remove them."),
    ("Manage Classes", "Schedule, update or delete classes",
     "Blank form = schedule a new class (a private session is for 1 person). Click a class to "
     "update it, then Save Changes. Click Delete beside a class to cancel it."),
    ("Enrol Member", "Add a member to a class",
     "Click an upcoming class, pick the member on the right, then click Enrol."),
    ("Remove Member", "Take a member out of a class",
     "Each row is one member in one class. Click the row, then click Remove."),
    ("Hours & Commission", "Coach hours and earnings",
     "Hours and commission per coach. Commission = fee per person x people enrolled x the coach's %."),
]

COACH_LIST_HEADER = f"{'ID':<8}{'Name':<20}{'Sport':<11}{'Rate':>7}{'Comm%':>7}"
CLASS_LIST_HEADER = f"{'ID':<7}{'Date':<11}{'Time':<12}{'Sport':<10}{'Type':<8}{'Pax':>5}"

HOUR_CHOICES = []
for choice_hour in range(common.OPENING_HOUR, common.CLOSING_HOUR):
    HOUR_CHOICES.append(f"{choice_hour:02d}:00")

DURATION_CHOICES = []
for choice_duration in range(1, MAX_CLASS_DURATION + 1):
    if choice_duration == 1:
        DURATION_CHOICES.append("1 hour")
    else:
        DURATION_CHOICES.append(f"{choice_duration} hours")


def coach_choice_text(coach):
    """Return the drop-down text for a coach, e.g. 'CCH001 Lim Wei (Badminton)'."""
    return f"{coach.get_coach_id()} {coach.get_name()} ({coach.get_sport()})"


def show_problem(error):
    """Show a ValueError's plain message in a standard error box."""
    messagebox.showerror("Please check", str(error))


def build_coaching_tab(parent):
    """Build the Coaching & Class Management tab inside parent (the main
    window's tab area) and return its frame. The tab opens on a menu
    asking what to do; each action has its own simple page."""
    window = tk.Frame(parent, bg=common.APP_BG)
    page_frames, page_hooks = common.build_action_menu(window, "Coaching & Class Management", COACHING_ACTIONS)
    build_manage_coaches_page(page_frames["Manage Coaches"], page_hooks)
    build_manage_classes_page(page_frames["Manage Classes"], page_hooks)
    page_hooks["Enrol Member"] = build_enrol_page(page_frames["Enrol Member"])
    page_hooks["Remove Member"] = common.build_pick_page(
        page_frames["Remove Member"], f"{'Class':<7}{'Date':<11}{'Sport':<10}{'Member':<8}{'Name':<20}",
        enrolment_rows, "Remove", remove_member_action, describe=describe_enrolment,
        confirm_text=remove_member_question, danger=True, empty_text="Nobody is enrolled in an upcoming class.")
    build_report_page(page_frames["Hours & Commission"], page_hooks)
    return window


# ----- rows and descriptions shared by the pick pages -----
def coach_rows(search_text):
    """Return (coach_id, row_text) for every coach, or those whose name
    contains search_text."""
    coach_list = load_all_coaches()
    if search_text != "":
        coach_list = search_coaches(coach_list, "name", search_text)
    rows = []
    for coach in coach_list:
        rows.append((coach.get_coach_id(), (f"{coach.get_coach_id():<8}{coach.get_name()[:19]:<20}"
                                            f"{coach.get_sport():<11}{coach.get_hourly_rate():>7.2f}"
                                            f"{coach.get_commission_pct():>7.0f}")))
    return rows


def class_rows(only_upcoming, only_with_space):
    """Return (class_id, row_text) for classes, soonest first. Can be
    limited to upcoming classes and/or classes that still have space."""
    today = common.today_string()
    sort_rows = []
    for sports_class in load_all_classes():
        if only_upcoming and sports_class.date_text < today:
            continue
        if only_with_space and len(sports_class.get_participant_list()) >= sports_class.max_pax:
            continue
        sort_rows.append((sports_class.date_text, sports_class.start_hour, sports_class.class_id, sports_class))
    sort_rows.sort()
    rows = []
    for date_text, start_hour, class_id, sports_class in sort_rows:
        pax_text = f"{len(sports_class.get_participant_list())}/{sports_class.max_pax}"
        rows.append((class_id, (f"{class_id:<7}{date_text:<11}{sports_class.get_time_text():<12}"
                                f"{sports_class.sport:<10}{sports_class.class_type:<8}{pax_text:>5}")))
    return rows


def describe_class(class_id):
    """Return the details text for one class."""
    sports_class = find_class_by_id(load_all_classes(), class_id)
    if sports_class is None:
        return "This class no longer exists."
    coach = find_coach_by_id(load_all_coaches(), sports_class.coach_id)
    coach_name = sports_class.coach_id
    if coach is not None:
        coach_name = f"{sports_class.coach_id} {coach.get_name()}"
    return (f"{sports_class.class_id}\n\n{sports_class.sport} {sports_class.class_type}\n"
            f"{sports_class.date_text}  {sports_class.get_time_text()}\n"
            f"Coach: {coach_name}\n"
            f"Enrolled: {len(sports_class.get_participant_list())} of {sports_class.max_pax}\n"
            f"Fee: RM {sports_class.fee_per_pax:.2f} per person")


def enrolment_rows(search_text):
    """One row per (upcoming class, enrolled member). The row ID is
    'CLASS_ID;MEMBER_ID' so Remove knows both."""
    member_names = load_member_names()
    today = common.today_string()
    sort_rows = []
    for sports_class in load_all_classes():
        if sports_class.date_text < today:
            continue
        for member_id in sports_class.get_participant_list():
            sort_rows.append((sports_class.date_text, sports_class.class_id, member_id, sports_class.sport))
    sort_rows.sort()
    rows = []
    for date_text, class_id, member_id, sport in sort_rows:
        rows.append((class_id + ";" + member_id,
                     f"{class_id:<7}{date_text:<11}{sport:<10}{member_id:<8}{member_names.get(member_id, '?')[:19]:<20}"))
    return rows


def describe_enrolment(row_id):
    """Details for one class/member pair."""
    class_id, member_id = row_id.split(";")
    member_name = load_member_names().get(member_id, "(member removed)")
    return f"{member_id} {member_name}\n\nis enrolled in\n\n" + describe_class(class_id)


def remove_member_action(row_id):
    """Take the member out of the class."""
    class_id, member_id = row_id.split(";")
    remove_participant(class_id, member_id)
    return f"{member_id} removed from {class_id}."


def remove_member_question(row_id):
    """Confirmation question for removing a member from a class."""
    class_id, member_id = row_id.split(";")
    return f"Remove {member_id} from {class_id}?"


# ----- pages with their own forms -----
def add_coach_fields(form_frame, first_row):
    """Add the five coach fields to form_frame starting at first_row and
    return them as a dictionary (used by Manage Coaches)."""
    fields = {}
    fields["name"] = common.make_entry(form_frame)
    common.add_form_row(form_frame, first_row, "Name", fields["name"])
    fields["phone"] = common.make_entry(form_frame)
    common.add_form_row(form_frame, first_row + 1, "Phone", fields["phone"])
    fields["sport"] = tk.StringVar(value=common.COACHING_SPORTS[0])
    common.add_form_row(form_frame, first_row + 2, "Sport", common.make_option_menu(
        form_frame, fields["sport"], list(common.COACHING_SPORTS), width=20))
    fields["rate"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 3, "Hourly rate (RM)", fields["rate"])
    fields["commission"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 4, "Commission (%)", fields["commission"])
    return fields


def read_coach_numbers(fields):
    """Return (hourly_rate, commission) from the form, with friendly
    errors for words, nan/inf or values outside the limits."""
    hourly_rate = common.parse_decimal(fields["rate"].get(), "Hourly rate", MIN_HOURLY_RATE, MAX_HOURLY_RATE)
    commission = common.parse_decimal(fields["commission"].get(), "Commission", 0, MAX_COMMISSION_PCT)
    return hourly_rate, commission


def add_class_time_fields(form_frame, first_row):
    """Add date (with calendar), start time, duration, max people and fee
    fields starting at first_row; return them as a dictionary (used by
    Manage Classes)."""
    fields = {}
    date_row = tk.Frame(form_frame, bg=common.PANEL_BG)
    fields["date"] = common.make_entry(date_row, width=12)
    fields["date"].pack(side="left")

    def on_pick_date():
        """Open the calendar pop-up for the class date."""
        common.open_date_picker(form_frame, fields["date"])

    common.make_button(date_row, "\U0001F4C5", on_pick_date, style="light").pack(side="left", padx=(4, 0))
    common.add_form_row(form_frame, first_row, "Date", date_row)
    fields["hour"] = tk.StringVar(value=HOUR_CHOICES[2])
    common.add_form_row(form_frame, first_row + 1, "Start time",
                        common.make_option_menu(form_frame, fields["hour"], HOUR_CHOICES, width=8))
    fields["duration"] = tk.StringVar(value=DURATION_CHOICES[0])
    common.add_form_row(form_frame, first_row + 2, "Duration",
                        common.make_option_menu(form_frame, fields["duration"], DURATION_CHOICES, width=8))
    fields["max_pax"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 3, "Max people", fields["max_pax"])
    fields["fee"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 4, "Fee per person (RM)", fields["fee"])
    return fields


def read_class_values(fields):
    """Return (date, start_hour, duration_hours, max_pax, fee) from the
    form, with friendly errors for bad numbers."""
    start_hour = int(fields["hour"].get()[0:2])
    duration_hours = int(fields["duration"].get().split()[0])
    max_pax = common.parse_whole_number(fields["max_pax"].get(), "Max people", 1, MAX_GROUP_SIZE)
    fee = common.parse_decimal(fields["fee"].get(), "Fee per person", 0.01, MAX_CLASS_FEE)
    return fields["date"].get().strip(), start_hour, duration_hours, max_pax, fee


def build_manage_coaches_page(page_frame, page_hooks):
    """Build the Manage Coaches page (add, update and delete on one page)
    with the shared common.build_manage_page."""
    fields = {}

    def build_form(form_frame):
        """Add the five coach fields."""
        fields.update(add_coach_fields(form_frame, 0))

    def clear_form():
        """Empty EVERY field, including rate and commission."""
        for field_name in ("name", "phone", "rate", "commission"):
            fields[field_name].delete(0, tk.END)
        fields["sport"].set(common.COACHING_SPORTS[0])

    def fill_form(coach_id):
        """Load the clicked coach (found with the while loop)."""
        coach = find_coach_by_id(load_all_coaches(), coach_id)
        if coach is None:
            return
        for field_name, value in (("name", coach.get_name()), ("phone", coach.get_phone()),
                                  ("rate", f"{coach.get_hourly_rate():.2f}"),
                                  ("commission", f"{coach.get_commission_pct():g}")):
            fields[field_name].insert(0, value)
        fields["sport"].set(coach.get_sport())

    def save_action(coach_id):
        """Add a new coach (coach_id None) or save the edited one."""
        hourly_rate, commission = read_coach_numbers(fields)
        if coach_id is None:
            new_coach = register_coach(fields["name"].get(), fields["phone"].get(), fields["sport"].get(),
                                       hourly_rate, commission)
            return f"Coach {new_coach.get_coach_id()} {new_coach.get_name()} added."
        moved_count = update_coach(coach_id, fields["name"].get(), fields["phone"].get(),
                                   fields["sport"].get(), hourly_rate, commission)
        message = f"Coach {coach_id} saved."
        if moved_count > 0:
            message += f"\n{moved_count} upcoming class(es) changed to {fields['sport'].get()}."
        return message

    def delete_action(coach_id):
        """Delete the coach (blocked while they have classes)."""
        delete_coach(coach_id)
        return f"Coach {coach_id} deleted."

    def delete_question(coach_id):
        """Confirmation question for deleting a coach."""
        return f"Delete coach {coach_id} permanently?"

    page_hooks["Manage Coaches"] = common.build_manage_page(
        page_frame, COACH_LIST_HEADER, coach_rows, "coach", build_form, clear_form, fill_form,
        save_action, delete_action, delete_question, add_label="Add Coach", search_label="Name",
        empty_text="No coaches found.")


def build_manage_classes_page(page_frame, page_hooks):
    """Build the Manage Classes page: a blank form schedules a class,
    clicking a row updates it, Delete beside a row cancels it."""
    fields = {}
    coach_choice_ids = {}
    type_buttons = []

    def apply_class_type():
        """A private session is always for 1 person, so fix Max people at
        1 and lock it; a group class lets the user type the size."""
        fields["max_pax"].config(state="normal")
        match fields["type"].get():
            case "Private":
                fields["max_pax"].delete(0, tk.END)
                fields["max_pax"].insert(0, "1")
                fields["max_pax"].config(state="disabled")
            case "Group":
                if fields["max_pax"].get().strip() == "1":
                    fields["max_pax"].delete(0, tk.END)

    def build_form(form_frame):
        """Add coach, type and the date/time/size/fee fields."""
        fields["coach"] = tk.StringVar(value="")
        fields["coach_menu"] = common.make_option_menu(form_frame, fields["coach"], [], width=24)
        common.add_form_row(form_frame, 0, "Coach", fields["coach_menu"])
        fields["type"] = tk.StringVar(value="Group")
        type_row = tk.Frame(form_frame, bg=common.PANEL_BG)
        for class_type in CLASS_TYPES:
            type_button = tk.Radiobutton(type_row, text=class_type, value=class_type, variable=fields["type"],
                                         command=apply_class_type, font=common.LABEL_FONT, bg=common.PANEL_BG,
                                         activebackground=common.PANEL_BG)
            type_button.pack(side="left", padx=(0, 8))
            type_buttons.append(type_button)
        common.add_form_row(form_frame, 1, "Type", type_row)
        fields.update(add_class_time_fields(form_frame, 2))

    def set_locked(locked):
        """Coach and type can't be changed on an existing class."""
        if locked:
            new_state = "disabled"
        else:
            new_state = "normal"
        fields["coach_menu"].config(state=new_state)
        for type_button in type_buttons:
            type_button.config(state=new_state)

    def clear_form():
        """Reload the coach list and reset every field for a new class."""
        coach_choice_ids.clear()
        choices = []
        for coach in load_all_coaches():
            coach_choice_ids[coach_choice_text(coach)] = coach.get_coach_id()
            choices.append(coach_choice_text(coach))
        common.set_option_menu_choices(fields["coach_menu"], fields["coach"], choices)
        set_locked(False)
        fields["type"].set("Group")
        fields["max_pax"].config(state="normal")
        for field_name in ("date", "max_pax", "fee"):
            fields[field_name].delete(0, tk.END)
        fields["date"].insert(0, common.today_string())
        fields["hour"].set(HOUR_CHOICES[2])
        fields["duration"].set(DURATION_CHOICES[0])

    def fill_form(class_id):
        """Load the clicked class; lock coach and type."""
        sports_class = find_class_by_id(load_all_classes(), class_id)
        if sports_class is None:
            return
        for choice_text in coach_choice_ids:
            if coach_choice_ids[choice_text] == sports_class.coach_id:
                fields["coach"].set(choice_text)
        fields["type"].set(sports_class.class_type)
        fields["date"].delete(0, tk.END)
        fields["date"].insert(0, sports_class.date_text)
        fields["hour"].set(f"{sports_class.start_hour:02d}:00")
        if 1 <= sports_class.duration_hrs <= MAX_CLASS_DURATION:
            fields["duration"].set(DURATION_CHOICES[sports_class.duration_hrs - 1])
        fields["max_pax"].delete(0, tk.END)
        fields["max_pax"].insert(0, str(sports_class.max_pax))
        if sports_class.class_type == "Private":
            fields["max_pax"].config(state="disabled")
        fields["fee"].insert(0, f"{sports_class.fee_per_pax:.2f}")
        set_locked(True)

    def save_action(class_id):
        """Schedule a new class (class_id None) or save the edited one."""
        date_text, start_hour, duration_hours, max_pax, fee = read_class_values(fields)
        if class_id is None:
            if fields["coach"].get() not in coach_choice_ids:
                raise ValueError("Please add a coach first (Manage Coaches).")
            new_class = schedule_class(coach_choice_ids[fields["coach"].get()], fields["type"].get(), date_text,
                                       start_hour, duration_hours, max_pax, fee)
            return (f"Class {new_class.class_id} scheduled: {new_class.sport} {new_class.class_type}, "
                    f"{new_class.date_text} {new_class.get_time_text()}.")
        update_class(class_id, date_text, start_hour, duration_hours, max_pax, fee)
        return f"Class {class_id} saved."

    def delete_action(class_id):
        """Cancel (permanently remove) the class."""
        cancel_class(class_id)
        return f"Class {class_id} deleted."

    def delete_question(class_id):
        """Confirmation question for deleting a class."""
        return f"Delete class {class_id}? This cannot be undone."

    def load_rows(search_text):
        """Every class, soonest first, or one coach's classes."""
        rows = class_rows(False, False)
        if search_text == "":
            return rows
        coach_class_ids = set()
        for sports_class in search_classes(load_all_classes(), "coach", search_text):
            coach_class_ids.add(sports_class.class_id)
        matching_rows = []
        for class_id, row_text in rows:
            if class_id in coach_class_ids:
                matching_rows.append((class_id, row_text))
        return matching_rows

    page_hooks["Manage Classes"] = common.build_manage_page(
        page_frame, CLASS_LIST_HEADER, load_rows, "class", build_form, clear_form, fill_form,
        save_action, delete_action, delete_question, add_label="Schedule Class", search_label="Coach ID",
        empty_text="No classes found.")


def build_enrol_page(page_frame):
    """Build the Enrol Member page and return its refresh function."""
    form_widgets = {}
    member_choice_ids = {}

    def build_form(form_frame):
        """Add the member drop-down."""
        form_widgets["member"] = tk.StringVar(value="")
        form_widgets["menu"] = common.make_option_menu(form_frame, form_widgets["member"], [], width=24)
        common.add_form_row(form_frame, 0, "Member", form_widgets["menu"])

    def fill_form(class_id):
        """List only members who are not already in the picked class."""
        sports_class = find_class_by_id(load_all_classes(), class_id)
        enrolled = []
        if sports_class is not None:
            enrolled = sports_class.get_participant_list()
        member_names = load_member_names()
        member_choice_ids.clear()
        choices = []
        for member_id in member_names:
            if member_id not in enrolled:
                choice_text = f"{member_id} {member_names[member_id]}"
                member_choice_ids[choice_text] = member_id
                choices.append(choice_text)
        common.set_option_menu_choices(form_widgets["menu"], form_widgets["member"], choices)

    def enrol_action(class_id):
        """Enrol the chosen member."""
        if form_widgets["member"].get() not in member_choice_ids:
            raise ValueError("Pick a member to enrol.")
        member_id = member_choice_ids[form_widgets["member"].get()]
        enrol_participant(class_id, member_id)
        return f"{member_id} enrolled in {class_id}."

    def open_rows(search_text):
        """Upcoming classes that still have space."""
        return class_rows(True, True)

    return common.build_pick_page(page_frame, CLASS_LIST_HEADER, open_rows, "Enrol", enrol_action,
                                  describe=describe_class, build_form=build_form, fill_form=fill_form,
                                  empty_text="No upcoming classes with space.")


def build_report_page(page_frame, page_hooks):
    """Build the Hours & Commission page: one row per coach for the
    chosen month (or all time)."""
    section_frame = page_frame
    top_row = tk.Frame(section_frame, bg=common.APP_BG)
    top_row.pack(side="top", fill="x", pady=(0, 6))
    tk.Label(top_row, text="Month:", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left")
    month_variable = tk.StringVar(value="All time")

    list_panel, report_listbox = common.build_list_panel(
        section_frame, f"{'Coach':<8}{'Name':<22}{'Classes':>8}{'Hours':>8}{'Commission (RM)':>18}")
    list_panel.pack(side="top", fill="both", expand=True)
    total_label = tk.Label(section_frame, text="", font=common.HEADING_FONT, bg=common.APP_BG,
                           fg=common.ACCENT_COLOR, anchor="w")
    total_label.pack(side="top", fill="x", pady=(8, 0))

    def refresh_report():
        """Recalculate hours and commission per coach for the chosen month."""
        if month_variable.get() == "All time":
            month_text = ""
        else:
            month_text = month_variable.get()
        all_classes = load_all_classes()
        month_classes = classes_in_month(all_classes, month_text)
        hours_dict = coach_hours_by_month(all_classes, month_text)

        report_listbox.delete(0, tk.END)
        total_hours = 0
        total_commission = 0.0
        for coach in load_all_coaches():
            coach_id = coach.get_coach_id()
            coach_classes = search_classes(month_classes, "coach", coach_id)
            commission = total_commission_recursive(coach_classes, coach.get_commission_pct())
            coach_hours = hours_dict.get(coach_id, 0)
            total_hours += coach_hours
            total_commission += commission
            report_listbox.insert(tk.END, (f"{coach_id:<8}{coach.get_name()[:21]:<22}{len(coach_classes):>8}"
                                           f"{coach_hours:>8}{commission:>18.2f}"))
        total_label.config(text=f"Total: {total_hours} hours, RM {total_commission:.2f} commission")

    def on_month_changed(chosen_month):
        """Recalculate when a different month is picked."""
        refresh_report()

    month_menu = common.make_option_menu(top_row, month_variable, ["All time"],
                                         command=on_month_changed, width=10)
    month_menu.pack(side="left", padx=6)

    def on_show():
        """Rebuild the month list (from class dates) and the report."""
        month_set = set()
        for sports_class in load_all_classes():
            month_set.add(sports_class.date_text[0:7])
        month_choices = ["All time"]
        for month_text in sorted(month_set):
            month_choices.append(month_text)
        common.set_option_menu_choices(month_menu, month_variable, month_choices, command=on_month_changed)
        refresh_report()

    page_hooks["Hours & Commission"] = on_show
