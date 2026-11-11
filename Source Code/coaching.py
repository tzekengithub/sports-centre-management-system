"""
Module      : coaching.py
Member 3    : Tan Chor Koon (student ID: 26PMD03614)
Purpose     : Coaching & Class Management module - assigns coaches to
              private sessions or group classes, enrols members, and
              tracks each coach's working hours and commission.
Date        : 2026-11-07
"""

import datetime
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

# A coach who has taught classes is never deleted (their hours and
# commission history would be lost); they are made INACTIVE instead.
COACH_STATUSES = ("ACTIVE", "INACTIVE")


# ---------------------------------------------------------------------------
# CLASS (encapsulation + inheritance from common.Person)
# ---------------------------------------------------------------------------
class Coach(common.Person):
    """A coach. Inherits name/phone handling from Person and adds
    coaching-specific private attributes."""

    def __init__(self, coach_id, name, phone, sport, hourly_rate, commission_pct, status="ACTIVE"):
        """Create the object and validate its starting values."""
        super().__init__(name, phone)
        self.__coach_id = coach_id
        self.__sport = ""
        self.__hourly_rate = 0.0
        self.__commission_pct = 0.0
        self.__status = "ACTIVE"
        self.set_sport(sport)
        self.set_hourly_rate(hourly_rate)
        self.set_commission_pct(commission_pct)
        self.set_status(status)

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

    def get_status(self):
        """Return ACTIVE or INACTIVE."""
        return self.__status

    def set_status(self, status):
        """Validate and store the status (ACTIVE or INACTIVE)."""
        if status not in COACH_STATUSES:
            raise ValueError("Coach status must be ACTIVE or INACTIVE.")
        self.__status = status

    def is_active(self):
        """Return True if the coach can be given new classes."""
        return self.__status == "ACTIVE"

    def to_line(self):
        """Turn this coach into a pipe-delimited text-file line."""
        return "|".join([
            self.__coach_id, self.get_name(), self.get_phone(), self.__sport,
            f"{self.__hourly_rate:.2f}", f"{self.__commission_pct:.2f}", self.__status,
        ])


# ---------------------------------------------------------------------------
# LOGIC LAYER - COACHES
# ---------------------------------------------------------------------------
COACH_FIELD_COUNT = 7
CLASS_FIELD_COUNT = 10
MEMBER_FIELD_COUNT = 6
BILL_FIELD_COUNT = 10


def line_to_coach(line):
    """Convert one text-file line into a Coach object, or None if the
    line is malformed. Lines saved before the status field existed (6
    fields) are read as ACTIVE coaches."""
    fields = common.split_fields(line, COACH_FIELD_COUNT)
    if fields is None:
        fields = common.split_fields(line, COACH_FIELD_COUNT - 1)
        if fields is None:
            return None
        fields.append("ACTIVE")
    try:
        return Coach(fields[0], fields[1], fields[2], fields[3], float(fields[4]), float(fields[5]), fields[6])
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


def coach_phone_in_use(phone, ignore_coach_id=None):
    """Return the ID of the coach already using phone (ignoring
    ignore_coach_id, the coach being edited), or None if it is free."""
    for coach in load_all_coaches():
        if coach.get_phone() == phone.strip() and coach.get_coach_id() != ignore_coach_id:
            return coach.get_coach_id()
    return None


def register_coach(name, phone, sport, hourly_rate, commission_pct):
    """Validate input, build a new Coach, append it to the file, return it.
    A phone number can only belong to one coach."""
    owner_id = coach_phone_in_use(phone)
    if owner_id is not None:
        raise ValueError(f"This phone number is already used by coach {owner_id}.")
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


def update_coach(coach_id, new_name, new_phone, new_sport, new_rate, new_commission, new_status="ACTIVE"):
    """Update an existing coach's details. If the sport changes, the
    coach's classes that haven't started yet are moved to the new sport
    too, so they never show the old one. Past classes keep their sport,
    because that is what was actually taught. Returns how many classes
    were changed.
    The classes file is written FIRST; if saving the coach then fails,
    the classes are put back as they were, so the two files never
    disagree."""
    coach_list = load_all_coaches()
    coach_record = find_coach_by_id(coach_list, coach_id)
    if coach_record is None:
        raise ValueError(f"No coach found with ID {coach_id}.")
    old_sport = coach_record.get_sport()
    owner_id = coach_phone_in_use(new_phone, ignore_coach_id=coach_id)
    if owner_id is not None:
        raise ValueError(f"This phone number is already used by coach {owner_id}.")
    if new_status == "INACTIVE" and len(upcoming_classes_for_coach(coach_id)) > 0:
        raise ValueError("This coach still has upcoming classes, so they can't be made inactive. "
                         "Delete those classes first (Manage Classes).")

    coach_record.set_name(new_name)
    coach_record.set_phone(new_phone)
    coach_record.set_sport(new_sport)
    coach_record.set_hourly_rate(new_rate)
    coach_record.set_commission_pct(new_commission)
    coach_record.set_status(new_status)
    updated_lines = []
    for coach in coach_list:
        updated_lines.append(coach.to_line())

    changed_class_count = 0
    old_class_lines = common.read_lines(common.CLASSES_FILE)
    if new_sport != old_sport:
        class_list = load_all_classes()
        class_lines = []
        for sports_class in class_list:
            if sports_class.get_coach_id() == coach_id and not class_has_started(sports_class):
                sports_class.set_sport(new_sport)
                changed_class_count += 1
            class_lines.append(sports_class.to_line())
        common.rewrite_records(common.CLASSES_FILE, class_lines, line_to_class)

    try:
        common.rewrite_records(common.COACHES_FILE, updated_lines, line_to_coach)
    except OSError:
        # The coach could not be saved: undo the class changes, then report it.
        if changed_class_count > 0:
            common.write_lines(common.CLASSES_FILE, old_class_lines)
        raise
    return changed_class_count


def classes_for_coach(coach_id):
    """Return every class (past or upcoming) taught by coach_id."""
    coach_classes = []
    for sports_class in load_all_classes():
        if sports_class.get_coach_id() == coach_id:
            coach_classes.append(sports_class)
    return coach_classes


def upcoming_classes_for_coach(coach_id):
    """Return the coach's classes that are not over yet."""
    upcoming = []
    for sports_class in classes_for_coach(coach_id):
        if not class_is_over(sports_class):
            upcoming.append(sports_class)
    return upcoming


def delete_coach(coach_id):
    """Remove a coach and return a message saying what happened:
      - with upcoming classes: refused (those classes need a coach);
      - with only past classes: kept but made INACTIVE, so their hours
        and commission history stay and they get no new classes;
      - with no classes at all: deleted permanently."""
    coach_list = load_all_coaches()
    coach_record = find_coach_by_id(coach_list, coach_id)
    if coach_record is None:
        raise ValueError(f"No coach found with ID {coach_id}.")
    upcoming_count = len(upcoming_classes_for_coach(coach_id))
    if upcoming_count > 0:
        raise ValueError(f"Coach {coach_id} still has {upcoming_count} upcoming class(es). Delete those "
                         "classes in Manage Classes first (past classes can stay).")
    past_count = len(classes_for_coach(coach_id))
    if past_count > 0 and not coach_record.is_active():
        # Already kept as INACTIVE: nothing more to do, and the history stays.
        return (f"Coach {coach_id} is already inactive. Their {past_count} past class(es) stay on record, "
                "so they can't be deleted.")
    if past_count > 0:
        coach_record.set_status("INACTIVE")
        updated_lines = []
        for coach in coach_list:
            updated_lines.append(coach.to_line())
        common.rewrite_records(common.COACHES_FILE, updated_lines, line_to_coach)
        return (f"Coach {coach_id} has {past_count} past class(es), so they were kept as INACTIVE: "
                "their hours and commission history stay, but they can't be given new classes.")
    remaining_lines = []
    for coach in coach_list:
        if coach.get_coach_id() != coach_id:
            remaining_lines.append(coach.to_line())
    common.rewrite_records(common.COACHES_FILE, remaining_lines, line_to_coach)
    return f"Coach {coach_id} deleted."


# ---------------------------------------------------------------------------
# LOGIC LAYER - CLASSES
# ---------------------------------------------------------------------------
class SportsClass(common.Record):
    """A scheduled coaching class. Its details are private attributes
    (encapsulation), read with get_...() and changed with set_...()."""

    def __init__(self, class_id, coach_id, sport, class_type, date_text, start_hour,
                 duration_hrs, max_pax, fee_per_pax, participants_text):
        """Create the object with its starting values."""
        super().__init__(class_id)
        self.__coach_id = coach_id
        self.__sport = sport
        self.__class_type = class_type
        self.__date_text = date_text
        self.__start_hour = start_hour
        self.__duration_hrs = duration_hrs
        self.__max_pax = max_pax
        self.__fee_per_pax = fee_per_pax
        self.__participants_text = participants_text

    def get_class_id(self):
        """Return the class ID, e.g. CLS001 (kept by the parent class, Record)."""
        return self.get_record_id()

    def get_coach_id(self):
        """Return the ID of the coach who teaches the class."""
        return self.__coach_id

    def get_sport(self):
        """Return the class's sport."""
        return self.__sport

    def set_sport(self, sport):
        """Change the sport (used when the coach's sport changes)."""
        if sport not in common.COACHING_SPORTS:
            raise ValueError("Please choose a sport from the list.")
        self.__sport = sport

    def get_class_type(self):
        """Return Private or Group."""
        return self.__class_type

    def get_date_text(self):
        """Return the class date as YYYY-MM-DD."""
        return self.__date_text

    def set_date_text(self, date_text):
        """Change the class date (already checked by validate_class_details)."""
        self.__date_text = date_text

    def get_start_hour(self):
        """Return the start hour (24-hour clock)."""
        return self.__start_hour

    def set_start_hour(self, start_hour):
        """Change the start hour."""
        self.__start_hour = start_hour

    def get_duration_hrs(self):
        """Return how long the class lasts, in hours."""
        return self.__duration_hrs

    def set_duration_hrs(self, duration_hrs):
        """Change the duration in hours."""
        self.__duration_hrs = duration_hrs

    def get_max_pax(self):
        """Return the maximum number of people."""
        return self.__max_pax

    def set_max_pax(self, max_pax):
        """Change the maximum number of people."""
        self.__max_pax = max_pax

    def get_fee_per_pax(self):
        """Return the fee per person in RM."""
        return self.__fee_per_pax

    def set_fee_per_pax(self, fee_per_pax):
        """Change the fee per person in RM."""
        self.__fee_per_pax = fee_per_pax

    def get_participant_list(self):
        """Split the ;-joined participants string into a list of member IDs."""
        if self.__participants_text.strip() == "":
            return []
        return self.__participants_text.split(";")

    def set_participant_list(self, participant_list):
        """Store the enrolled member IDs (joined with ;)."""
        self.__participants_text = ";".join(participant_list)

    def get_time_text(self):
        """Return the class time as e.g. '10:00-12:00'."""
        return f"{self.__start_hour:02d}:00-{self.__start_hour + self.__duration_hrs:02d}:00"

    def to_line(self):
        """Turn this class into a pipe-delimited text-file line."""
        # The parent's join_fields() puts the ID first and adds the | separators.
        return self.join_fields([
            self.__coach_id, self.__sport, self.__class_type, self.__date_text,
            str(self.__start_hour), str(self.__duration_hrs), str(self.__max_pax),
            f"{self.__fee_per_pax:.2f}", self.__participants_text,
        ])


def line_to_class(line):
    """Convert one text-file line into a SportsClass object, or None if
    the line is malformed or holds impossible values (a hand-edited row
    with duration 0, max people 0, an unknown sport, a bad date ...).
    The date is tidied to YYYY-MM-DD. A row that returns None is hidden
    from every list but stays in the file, because rewrite_records keeps
    unreadable lines."""
    fields = common.split_fields(line, CLASS_FIELD_COUNT)
    if fields is None:
        return None
    try:
        date_text = common.normalize_date(fields[4])
        start_hour = int(fields[5])
        duration_hrs = int(fields[6])
        max_pax = int(fields[7])
        fee_per_pax = float(fields[8])
        if fields[2] not in common.COACHING_SPORTS:
            raise ValueError("Unknown sport.")
        # The same range checks as scheduling, minus the "not in the past" ones.
        validate_class_details(fields[3], date_text, start_hour, duration_hrs, max_pax, fee_per_pax,
                               check_timing=False)
        return SportsClass(fields[0], fields[1], fields[2], fields[3], date_text,
                            start_hour, duration_hrs, max_pax, fee_per_pax, fields[9])
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
        if sports_class.get_class_id() == class_id:
            return sports_class
    return None


CLASS_TYPES = ("Private", "Group")


def times_overlap(start_hour, duration_hrs, other_start_hour, other_duration_hrs):
    """Return True if two time ranges [start, end) on the same day overlap:
    each one starts before the other ends."""
    return start_hour < other_start_hour + other_duration_hrs and other_start_hour < start_hour + duration_hrs


def class_has_started(sports_class):
    """Return True if the class's start time has been reached (any past
    day, or today at or after its start hour)."""
    today = common.today_string()
    if sports_class.get_date_text() != today:
        return sports_class.get_date_text() < today
    return sports_class.get_start_hour() <= common.current_hour()


def class_is_over(sports_class):
    """Return True once the class has finished (its end hour has passed)."""
    today = common.today_string()
    if sports_class.get_date_text() != today:
        return sports_class.get_date_text() < today
    return sports_class.get_start_hour() + sports_class.get_duration_hrs() <= common.current_hour()


def coach_has_time_clash(class_list, coach_id, date_text, start_hour, duration_hrs, ignore_class_id=None):
    """Return True if coach_id already has a class overlapping this time slot."""
    for sports_class in class_list:
        if sports_class.get_coach_id() != coach_id or sports_class.get_date_text() != date_text:
            continue
        if ignore_class_id is not None and sports_class.get_class_id() == ignore_class_id:
            continue
        if times_overlap(start_hour, duration_hrs, sports_class.get_start_hour(), sports_class.get_duration_hrs()):
            return True
    return False


def validate_class_details(class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax,
                           check_timing=True):
    """Check the details shared by scheduling and updating a class.
    date_text must already be tidied with common.normalize_date and the
    fee already rounded to 2 decimals. check_timing False skips the
    "not in the past / not started" checks: used when an existing class
    keeps its date and start time (so a past class's fee can still be
    corrected). Raises ValueError with a plain message for the first
    problem found."""
    if class_type not in CLASS_TYPES:
        raise ValueError("Class type must be Private or Group.")
    if not common.is_valid_date(date_text):
        raise ValueError("Class date must be a real date in YYYY-MM-DD form.")
    if check_timing and date_text < common.today_string():
        raise ValueError("Class date cannot be in the past.")
    if check_timing and date_text == common.today_string() and start_hour <= common.current_hour():
        raise ValueError(f"{start_hour:02d}:00 has already started today. Pick a later start time.")
    if duration_hrs < 1 or duration_hrs > MAX_CLASS_DURATION:
        raise ValueError(f"Duration must be between 1 and {MAX_CLASS_DURATION} hours.")
    if not common.is_valid_hour(start_hour) or not common.is_valid_hour(start_hour + duration_hrs - 1):
        raise ValueError(f"The class must fit within opening hours "
                         f"({common.OPENING_HOUR}:00-{common.CLOSING_HOUR}:00).")
    if class_type == "Private" and max_pax != 1:
        raise ValueError("A private session is for exactly 1 person.")
    if max_pax < 1 or max_pax > MAX_GROUP_SIZE:
        raise ValueError(f"Maximum people must be between 1 and {MAX_GROUP_SIZE}.")
    if not (0.01 <= fee_per_pax <= MAX_CLASS_FEE):
        raise ValueError(f"Fee per person must be between RM 0.01 and RM {MAX_CLASS_FEE:g}.")


def schedule_class(coach_id, class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax,
                   member_id=None):
    """Validate and create a new class. The class takes its sport from
    the coach. member_id (for a private session) is checked first and
    saved inside the new class in the same write, so a class is never
    left half-made. Raises ValueError on clash/invalid input."""
    coach_record = find_coach_by_id(load_all_coaches(), coach_id)
    if coach_record is None:
        raise ValueError(f"No coach found with ID {coach_id}.")
    if not coach_record.is_active():
        raise ValueError(f"Coach {coach_id} is inactive and can't be given new classes.")
    # Save the date in one standard form (2027-1-5 -> 2027-01-05) so clash
    # checks and searches, which compare the text, always match; round the
    # fee before checking it, because that is the value that gets saved.
    date_text = common.normalize_date(date_text)
    fee_per_pax = round(fee_per_pax, 2)
    validate_class_details(class_type, date_text, start_hour, duration_hrs, max_pax, fee_per_pax)

    class_list = load_all_classes()
    if coach_has_time_clash(class_list, coach_id, date_text, start_hour, duration_hrs):
        raise ValueError("This coach already has a class at that time.")
    participant_list = []
    if member_id is not None:
        problem = member_enrol_problem(member_id, date_text, start_hour, duration_hrs, class_list)
        if problem is not None:
            raise ValueError(problem)
        participant_list.append(member_id)

    new_id = common.generate_id(common.CLASSES_FILE, "CLS")
    new_class = SportsClass(new_id, coach_id, coach_record.get_sport(), class_type, date_text,
                             start_hour, duration_hrs, max_pax, fee_per_pax, ";".join(participant_list))
    common.append_line(common.CLASSES_FILE, new_class.to_line())
    return new_class


def update_class(class_id, new_date_text, new_start_hour, new_duration_hrs, new_max_pax, new_fee_per_pax):
    """Update a class's date, hour, duration, maximum people and fee,
    re-checking the coach's time clash, every enrolled member, and that
    max_pax is not reduced below the number already enrolled. A class that
    has started is history (hours, pay and commission are worked out from
    it) and can't be edited; a class with a bill keeps its fee and length."""
    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")

    # A class that has started (or is over) is a record of what happened:
    # editing it would rewrite the coach's worked hours, pay and commission.
    if class_has_started(target_class):
        raise ValueError(f"Class {class_id} has already started, so it is kept as a record and can't be edited.")

    new_date_text = common.normalize_date(new_date_text)
    new_fee_per_pax = round(new_fee_per_pax, 2)
    validate_class_details(target_class.get_class_type(), new_date_text, new_start_hour,
                           new_duration_hrs, new_max_pax, new_fee_per_pax)

    # A bill was worked out from this class's fee and length: changing
    # either would leave the bill showing the wrong amount.
    bill_info = class_bill_info(class_id)
    if bill_info is not None and (new_fee_per_pax != target_class.get_fee_per_pax()
                                  or new_duration_hrs != target_class.get_duration_hrs()):
        if bill_info[1] == "PAID":
            # A PAID bill can never be voided, so "void it first" would be wrong advice.
            raise ValueError(f"Bill {bill_info[0]} for this class is already paid and a paid bill can't be "
                             "voided, so the fee and duration can't be changed.")
        raise ValueError(f"Bill {bill_info[0]} was made for this class, so its fee and duration can't be changed. "
                         "Void the bill first (Billing > Void Bill), or leave them as they are.")

    if new_max_pax < len(target_class.get_participant_list()):
        raise ValueError("Maximum people cannot be less than the number already enrolled.")
    if coach_has_time_clash(class_list, target_class.get_coach_id(), new_date_text, new_start_hour,
                             new_duration_hrs, ignore_class_id=class_id):
        raise ValueError("This coach already has a class at that time.")

    # If the class moves or changes length, every member already in it must
    # still be able to attend at the new time (membership valid on the new
    # day, and not in another class at the same time).
    timing_changed = (new_date_text != target_class.get_date_text()
                      or new_start_hour != target_class.get_start_hour()
                      or new_duration_hrs != target_class.get_duration_hrs())
    if timing_changed:
        for member_id in target_class.get_participant_list():
            problem = member_enrol_problem(member_id, new_date_text, new_start_hour, new_duration_hrs,
                                           class_list, ignore_class_id=class_id)
            if problem is not None:
                raise ValueError(f"The class can't be changed to that time. {problem}")

    target_class.set_date_text(new_date_text)
    target_class.set_start_hour(new_start_hour)
    target_class.set_duration_hrs(new_duration_hrs)
    target_class.set_max_pax(new_max_pax)
    target_class.set_fee_per_pax(new_fee_per_pax)

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.rewrite_records(common.CLASSES_FILE, updated_lines, line_to_class)


def load_member_names():
    """Return a dictionary of member_id -> member name, read straight from
    members.txt (coaching does not import membership.py)."""
    member_names = {}
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            member_names[fields[0]] = fields[1]
    return member_names


def load_member_expiry_dates():
    """Return a dictionary of member_id -> membership expiry date (YYYY-MM-DD)."""
    expiry_dates = {}
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            expiry_dates[fields[0]] = fields[5]
    return expiry_dates


def members_valid_on(date_text):
    """Return (member_id, name) for members whose membership has not
    expired by date_text, for the member drop-downs."""
    member_names = load_member_names()
    expiry_dates = load_member_expiry_dates()
    valid_members = []
    for member_id in member_names:
        if expiry_dates.get(member_id, "") >= date_text:
            valid_members.append((member_id, member_names[member_id]))
    return valid_members


def member_enrol_problem(member_id, date_text, start_hour, duration_hrs, class_list, ignore_class_id=None):
    """Return a plain message saying why member_id can't join a class at
    this date and time, or None if they can: the member must exist, their
    membership must still be valid on the class day, and they can't be in
    another class at an overlapping time."""
    expiry_dates = load_member_expiry_dates()
    if member_id not in expiry_dates:
        return f"No member found with ID {member_id}."
    if expiry_dates[member_id] < date_text:
        return (f"{member_id}'s membership ends on {expiry_dates[member_id]}, before this class "
                f"({date_text}). Renew it first (Membership > Renew Membership).")
    for sports_class in class_list:
        if sports_class.get_class_id() == ignore_class_id or sports_class.get_date_text() != date_text:
            continue
        if member_id not in sports_class.get_participant_list():
            continue
        if times_overlap(start_hour, duration_hrs, sports_class.get_start_hour(), sports_class.get_duration_hrs()):
            return (f"{member_id} is already in class {sports_class.get_class_id()} at "
                    f"{sports_class.get_time_text()} that day.")
    return None


def enrol_participant(class_id, member_id):
    """Add member_id to a class's participant list: no duplicates, capped
    at max_pax, only before the class starts, only while the membership
    is valid on the class day, and not at the same time as another class
    the member is in."""
    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")

    # Nobody can join a class that is over or under way: its record is
    # history once it starts (see update_class).
    if target_class.get_date_text() < common.today_string():
        raise ValueError("This class has already taken place.")
    if class_has_started(target_class):
        raise ValueError("This class has already started today.")
    # A set makes the "already enrolled" and "is it full" checks simple:
    # it holds each member ID once, and len() is the head count.
    participant_set = set(target_class.get_participant_list())
    if member_id in participant_set:
        raise ValueError("This member is already enrolled.")
    if len(participant_set) >= target_class.get_max_pax():
        raise ValueError("This class is already full.")
    # The member must exist, be a member on the class day, and be free at
    # that time. ignore_class_id stops this class clashing with itself.
    problem = member_enrol_problem(member_id, target_class.get_date_text(), target_class.get_start_hour(),
                                   target_class.get_duration_hrs(), class_list, ignore_class_id=class_id)
    if problem is not None:
        raise ValueError(problem)
    participant_list = target_class.get_participant_list()
    participant_list.append(member_id)
    target_class.set_participant_list(participant_list)

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.rewrite_records(common.CLASSES_FILE, updated_lines, line_to_class)


def remove_participant(class_id, member_id):
    """Remove member_id from a class's participant list. Refused once the
    class has started (it is history) and while a bill (not VOID) was made
    for this member and class."""
    class_list = load_all_classes()
    target_class = find_class_by_id(class_list, class_id)
    if target_class is None:
        raise ValueError(f"No class found with ID {class_id}.")
    participant_list = target_class.get_participant_list()
    if member_id not in participant_list:
        raise ValueError("This member is not enrolled in this class.")
    if class_has_started(target_class):
        raise ValueError(f"Class {class_id} has already started, so who was in it is kept as a record.")
    bill_info = class_bill_info(class_id, member_id)
    if bill_info is not None:
        raise ValueError(f"{member_id} has bill {bill_info[0]} for this class, so they can't be taken out. "
                         "Void the bill first (Billing > Void Bill) - a paid bill can't be voided.")
    participant_list.remove(member_id)
    target_class.set_participant_list(participant_list)

    updated_lines = []
    for sports_class in class_list:
        updated_lines.append(sports_class.to_line())
    common.rewrite_records(common.CLASSES_FILE, updated_lines, line_to_class)


def search_classes(class_list, search_field, search_text):
    """Search classes by 'coach', 'date', 'sport' or 'type'."""
    results = []
    search_text_lower = search_text.strip().lower()
    for sports_class in class_list:
        match search_field:
            case "coach":
                if sports_class.get_coach_id().lower() == search_text_lower:
                    results.append(sports_class)
            case "date":
                if sports_class.get_date_text() == search_text.strip():
                    results.append(sports_class)
            case "sport":
                if search_text_lower in sports_class.get_sport().lower():
                    results.append(sports_class)
            case "type":
                if sports_class.get_class_type().lower() == search_text_lower:
                    results.append(sports_class)
    return results


def class_bill_info(class_id, member_id=None):
    """Return (bill_id, status) of a bill (not VOID) made for class_id, or
    None. With member_id, only that member's bill counts. If the class has
    several bills, a PAID one is reported first (it can never be voided, so
    it decides what advice the error message gives). Read straight from
    bills.txt (coaching does not import billing.py). Field 1 is the member,
    3 the class and 8 the status."""
    found_bill = None
    for line in common.read_lines(common.BILLS_FILE):
        fields = common.split_fields(line, BILL_FIELD_COUNT)
        if fields is None or fields[3] != class_id or fields[8] == "VOID":
            continue
        if member_id is None or fields[1] == member_id:
            if fields[8] == "PAID":
                return fields[0], fields[8]
            if found_bill is None:
                found_bill = (fields[0], fields[8])
    return found_bill


def cancel_class(class_id):
    """Remove a class permanently from classes.txt. Blocked once the class
    has started (it is history: worked hours and commission come from it)
    and while a bill (not VOID) points at it, because that bill would lose
    its class."""
    started_class = find_class_by_id(load_all_classes(), class_id)
    if started_class is not None and class_has_started(started_class):
        raise ValueError(f"Class {class_id} has already started, so it is kept as a record and can't be deleted.")
    bill_info = class_bill_info(class_id)
    if bill_info is not None and bill_info[1] == "PAID":
        # A PAID bill can never be voided (billing.void_bill refuses it).
        raise ValueError(f"Class {class_id} has a paid bill ({bill_info[0]}). Paid bills can't be voided, "
                         "so this class is kept as a record and can't be deleted.")
    if bill_info is not None:
        raise ValueError(f"Class {class_id} has bill {bill_info[0]}, so it can't be deleted. "
                         "Void the bill first (Billing > Void Bill).")
    class_list = load_all_classes()
    remaining_lines = []
    class_found = False
    for sports_class in class_list:
        if sports_class.get_class_id() == class_id:
            class_found = True
        else:
            remaining_lines.append(sports_class.to_line())
    if not class_found:
        raise ValueError(f"No class found with ID {class_id}.")
    common.rewrite_records(common.CLASSES_FILE, remaining_lines, line_to_class)


def classes_in_month(class_list, month_text):
    """Return the classes whose date starts with month_text ('YYYY-MM').
    An empty month_text means every class."""
    if month_text == "":
        return class_list
    month_classes = []
    for sports_class in class_list:
        if sports_class.get_date_text().startswith(month_text):
            month_classes.append(sports_class)
    return month_classes


def coach_hours_by_month(class_list, month_text=""):
    """Return a dictionary of coach_id -> total hours of classes in
    month_text ('YYYY-MM'), or across all classes if month_text is empty."""
    hours_by_coach = {}
    for sports_class in classes_in_month(class_list, month_text):
        coach_id = sports_class.get_coach_id()
        if coach_id in hours_by_coach:
            hours_by_coach[coach_id] += sports_class.get_duration_hrs()
        else:
            hours_by_coach[coach_id] = sports_class.get_duration_hrs()
    return hours_by_coach


def split_worked_classes(class_list):
    """Split classes into (worked, upcoming): worked ones are over, so
    their hours, pay and commission have really been earned."""
    worked_classes = []
    upcoming_classes = []
    for sports_class in class_list:
        if class_is_over(sports_class):
            worked_classes.append(sports_class)
        else:
            upcoming_classes.append(sports_class)
    return worked_classes, upcoming_classes


def calculate_commission(sports_class, commission_pct):
    """Commission = fee_per_pax * number_of_participants * commission_pct / 100."""
    participant_count = len(sports_class.get_participant_list())
    return sports_class.get_fee_per_pax() * participant_count * commission_pct / 100.0


def total_commission(class_list, coach_commission_pct):
    """Total commission for class_list. Uses the recursive version (rubric)
    for normal sizes, and a plain loop above common.RECURSION_SAFE_LIMIT,
    where recursion would hit Python's limit and crash."""
    if len(class_list) <= common.RECURSION_SAFE_LIMIT:
        return total_commission_recursive(class_list, coach_commission_pct)
    commission_sum = 0.0
    for sports_class in class_list:
        commission_sum += calculate_commission(sports_class, coach_commission_pct)
    return commission_sum


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
     "Click Delete beside a coach to remove them (a coach with past classes is kept as Inactive)."),
    ("Manage Classes", "Schedule, update or delete classes",
     "Blank form = schedule a new class (for a private session, pick its member). Click a class to "
     "update it, then Save Changes. Click Delete beside a class to cancel it. Grey rows are over: "
     "they are kept as a record and can't be edited or deleted."),
    ("Enrol Member", "Add a member to a class",
     "Click a class that hasn't started, pick the member on the right, then click Enrol. Full "
     "classes and members whose membership ends before the class are not listed."),
    ("Remove Member", "Take a member out of a class",
     "Each row is one member in a class that hasn't started yet (classes that have started are kept "
     "as a record, so they aren't listed). Click the row, then click Remove."),
    ("Hours & Commission", "Coach hours and earnings",
     "Hours, pay and commission per coach for classes that are over (upcoming hours are shown "
     "separately). Pay = hours x hourly rate. Commission = fee x people enrolled x the coach's %."),
]

COACH_LIST_HEADER = f"{'Coach ID':<9}{'Name':<20}{'Sport':<11}{'RM/hour':>8}{'Comm %':>8}  {'Status':<8}"
CLASS_LIST_HEADER = f"{'Class ID':<9}{'Date':<11}{'Time':<12}{'Sport':<10}{'Type':<8}{'People':>7}"
NAME_COLUMN_WIDTH = 19

STATUS_CHOICES = ("Active", "Inactive")
CHOICE_WIDTH = 24

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
    """Return the drop-down text for a coach, e.g. 'CCH001 Lim Wei (Badminton)'.
    A long name is shortened with ... so the sport stays visible."""
    sport_text = f" ({coach.get_sport()})"
    name_width = CHOICE_WIDTH - len(coach.get_coach_id()) - 1 - len(sport_text)
    return f"{coach.get_coach_id()} {common.fit_text(coach.get_name(), name_width)}{sport_text}"


def member_choice_text(member_id, member_name):
    """Return the drop-down text for a member, cut to fit the menu."""
    return common.fit_text(f"{member_id} {member_name}", CHOICE_WIDTH)


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
        page_frames["Remove Member"], f"{'Class ID':<9}{'Date':<11}{'Sport':<10}{'Member ID':<10}{'Name':<20}",
        enrolment_rows, "Remove", remove_member_action, describe=describe_enrolment,
        confirm_text=remove_member_question, danger=True, search_label="Member name",
        empty_text="Nobody is enrolled in a class that hasn't started.",
        refresh_on_error=True)
    build_report_page(page_frames["Hours & Commission"], page_hooks)
    return window


# ----- rows and descriptions shared by the pick pages -----
def coach_rows(search_text):
    """Return (coach_id, row_text[, "past"]) for every coach, or those
    whose name contains search_text. Inactive coaches are greyed out."""
    coach_list = load_all_coaches()
    if search_text != "":
        coach_list = search_coaches(coach_list, "name", search_text)
    rows = []
    for coach in coach_list:
        row_text = (f"{coach.get_coach_id():<9}"
                    f"{common.fit_text(coach.get_name(), NAME_COLUMN_WIDTH):<20}"
                    f"{coach.get_sport():<11}{coach.get_hourly_rate():>8.2f}"
                    f"{coach.get_commission_pct():>8.0f}  {coach.get_status().capitalize():<8}")
        if coach.is_active():
            rows.append((coach.get_coach_id(), row_text))
        else:
            rows.append((coach.get_coach_id(), row_text, "past"))
    return rows


def class_rows(only_upcoming, only_with_space):
    """Return (class_id, row_text[, "past"]) for classes, soonest first.
    only_upcoming keeps only classes that haven't started; otherwise
    classes that have started (under way or over) are marked "past"
    (shown greyed out), because they can't be edited or deleted.
    only_with_space keeps only classes that still have room."""
    sort_rows = []
    for sports_class in load_all_classes():
        if only_upcoming and class_has_started(sports_class):
            continue
        if only_with_space and len(sports_class.get_participant_list()) >= sports_class.get_max_pax():
            continue
        sort_rows.append((sports_class.get_date_text(), sports_class.get_start_hour(),
                          sports_class.get_class_id(), sports_class))
    sort_rows.sort()
    rows = []
    for date_text, start_hour, class_id, sports_class in sort_rows:
        pax_text = f"{len(sports_class.get_participant_list())}/{sports_class.get_max_pax()}"
        row_text = (f"{class_id:<9}{date_text:<11}{sports_class.get_time_text():<12}"
                    f"{sports_class.get_sport():<10}{sports_class.get_class_type():<8}{pax_text:>7}")
        if class_has_started(sports_class):
            rows.append((class_id, row_text, "past"))
        else:
            rows.append((class_id, row_text))
    return rows


def describe_class(class_id):
    """Return the details text for one class."""
    sports_class = find_class_by_id(load_all_classes(), class_id)
    if sports_class is None:
        return "This class no longer exists."
    coach = find_coach_by_id(load_all_coaches(), sports_class.get_coach_id())
    coach_name = "(coach removed)"
    if coach is not None:
        coach_name = coach.get_name()
    return common.details_text([
        ("Class ID", sports_class.get_class_id()),
        ("Sport", sports_class.get_sport()),
        ("Type", sports_class.get_class_type()),
        ("Date", f"{sports_class.get_date_text()} ({class_when_text(sports_class)})"),
        ("Time", sports_class.get_time_text()),
        ("Duration", f"{sports_class.get_duration_hrs()} hour(s)"),
        ("Coach ID", sports_class.get_coach_id()),
        ("Coach", coach_name),
        ("Enrolled", f"{len(sports_class.get_participant_list())} of {sports_class.get_max_pax()} people"),
        ("Fee", f"RM {sports_class.get_fee_per_pax():.2f} per person"),
        ("Status", class_status_text(sports_class)),
    ])


def days_until_class(sports_class):
    """Return how many days from today a class is on (negative if it was
    in the past), or None if its saved date can't be read. Uses the
    datetime module directly."""
    try:
        class_day = datetime.datetime.strptime(sports_class.get_date_text(), "%Y-%m-%d").date()
    except ValueError:
        return None
    else:
        return (class_day - datetime.date.today()).days


def class_when_text(sports_class):
    """Words for days_until_class, e.g. 'today', 'in 3 day(s)' or '2 day(s) ago'."""
    days_away = days_until_class(sports_class)
    if days_away is None:
        return "unknown"
    elif days_away == 0:
        return "today"
    elif days_away > 0:
        return f"in {days_away} day(s)"
    else:
        return f"{-days_away} day(s) ago"


def class_status_text(sports_class):
    """Return Upcoming, Under way or Over for a class."""
    if class_is_over(sports_class):
        return "Over"
    if class_has_started(sports_class):
        return "Under way"
    return "Upcoming"


def enrolment_rows(search_text):
    """One row per (class that hasn't started, enrolled member). The row
    ID is 'CLASS_ID;MEMBER_ID' so Remove knows both."""
    member_names = load_member_names()
    search_lower = search_text.strip().lower()
    sort_rows = []
    for sports_class in load_all_classes():
        if class_has_started(sports_class):
            continue
        for member_id in sports_class.get_participant_list():
            if search_lower not in member_names.get(member_id, "").lower():
                continue
            sort_rows.append((sports_class.get_date_text(), sports_class.get_class_id(), member_id, sports_class.get_sport()))
    sort_rows.sort()
    rows = []
    for date_text, class_id, member_id, sport in sort_rows:
        rows.append((class_id + ";" + member_id,
                     f"{class_id:<9}{date_text:<11}{sport:<10}{member_id:<10}"
                     f"{common.fit_text(member_names.get(member_id, '?'), NAME_COLUMN_WIDTH):<20}"))
    return rows


def describe_enrolment(row_id):
    """Details for one class/member pair."""
    class_id, member_id = row_id.split(";")
    member_name = load_member_names().get(member_id, "(member removed)")
    return (common.details_text([("Member ID", member_id), ("Name", member_name), ("", "")])
            + "\n" + describe_class(class_id))


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
    return them as a dictionary (used by Manage Coaches), plus a Status
    row (Active / Inactive) that can only be changed on an existing coach."""
    fields = {}
    fields["name"] = common.make_entry(form_frame)
    common.add_form_row(form_frame, first_row, "Name", fields["name"],
                        tip="The coach's full name. Letters, spaces, / and ' only (e.g. Ch'ng Wei).")
    fields["phone"] = common.make_entry(form_frame)
    common.add_form_row(form_frame, first_row + 1, "Phone", fields["phone"],
                        tip="Malaysian mobile number: 10-11 digits starting with 01, no spaces or dashes.")
    fields["sport"] = tk.StringVar(value=common.COACHING_SPORTS[0])
    common.add_form_row(form_frame, first_row + 2, "Sport", common.make_option_menu(
        form_frame, fields["sport"], list(common.COACHING_SPORTS), width=20),
        tip="The sport this coach teaches. Their classes use this sport.")
    fields["rate"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 3, "Hourly rate (RM/hour)", fields["rate"],
                        tip="How much the coach is paid per hour, in Ringgit. A number from 1 to 500, e.g. 60.")
    fields["commission"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 4, "Commission (%)", fields["commission"],
                        tip="The share of class fees the coach earns, in percent. A number from 0 to 100, e.g. 30.")
    fields["status"] = tk.StringVar(value=STATUS_CHOICES[0])
    fields["status_menu"] = common.make_option_menu(form_frame, fields["status"], list(STATUS_CHOICES), width=10)
    common.add_form_row(form_frame, first_row + 5, "Status", fields["status_menu"],
                        tip="Active coaches can be given new classes. Inactive ones are kept for their "
                            "history only. A new coach always starts Active.")
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
    fields["date"] = common.make_entry(date_row, width=12,
                                       tip="The day of the class, as YYYY-MM-DD. Today or later.")
    fields["date"].pack(side="left")

    def on_pick_date():
        """Open the calendar pop-up for the class date (past days greyed out)."""
        common.open_date_picker(form_frame, fields["date"], allow_past=False)

    common.make_button(date_row, "\U0001F4C5", on_pick_date, style="light",
                       tip="Open a calendar and click the day of the class.").pack(side="left", padx=(4, 0))
    common.add_form_row(form_frame, first_row, "Date", date_row)
    fields["hour"] = tk.StringVar(value=HOUR_CHOICES[2])
    common.add_form_row(form_frame, first_row + 1, "Start time",
                        common.make_option_menu(form_frame, fields["hour"], HOUR_CHOICES, width=8),
                        tip=f"When the class starts (24-hour clock). The centre is open "
                            f"{common.OPENING_HOUR:02d}:00-{common.CLOSING_HOUR:02d}:00.")
    fields["duration"] = tk.StringVar(value=DURATION_CHOICES[0])
    common.add_form_row(form_frame, first_row + 2, "Duration",
                        common.make_option_menu(form_frame, fields["duration"], DURATION_CHOICES, width=8),
                        tip=f"How long the class lasts, 1 to {MAX_CLASS_DURATION} hours. It must end by closing time.")
    fields["max_pax"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 3, f"Max people (1-{MAX_GROUP_SIZE})", fields["max_pax"],
                        tip=f"How many members can join. A group takes 1 to {MAX_GROUP_SIZE}; "
                            "a private session is always 1.")
    fields["fee"] = common.make_entry(form_frame, width=10)
    common.add_form_row(form_frame, first_row + 4, "Fee per person (RM)", fields["fee"],
                        tip="What each member pays for the class, in Ringgit, e.g. 25.")
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
        """Add the coach fields."""
        fields.update(add_coach_fields(form_frame, 0))

    def clear_form():
        """Empty EVERY field, including rate and commission; a new coach is Active."""
        for field_name in ("name", "phone", "rate", "commission"):
            fields[field_name].delete(0, tk.END)
        fields["sport"].set(common.COACHING_SPORTS[0])
        fields["status"].set(STATUS_CHOICES[0])
        fields["status_menu"].config(state="disabled")

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
        fields["status"].set(coach.get_status().capitalize())
        fields["status_menu"].config(state="normal")

    def sport_change_confirmed(coach_id):
        """If the sport is being changed, say how many classes that haven't
        started will change too (and how many already have members), and
        ask first. Returns False if the user says No."""
        coach = find_coach_by_id(load_all_coaches(), coach_id)
        new_sport = fields["sport"].get()
        if coach is None or new_sport == coach.get_sport():
            return True
        moving_count = 0
        with_members_count = 0
        for sports_class in classes_for_coach(coach_id):
            if not class_has_started(sports_class):
                moving_count += 1
                if len(sports_class.get_participant_list()) > 0:
                    with_members_count += 1
        if moving_count == 0:
            return True
        return messagebox.askyesno(
            "Change sport",
            f"{moving_count} upcoming class(es) of {coach_id} will change from {coach.get_sport()} to "
            f"{new_sport}, and {with_members_count} of them already have members enrolled.\n\n"
            "Save the change anyway?")

    def save_action(coach_id):
        """Add a new coach (coach_id None) or save the edited one. Returns
        None (nothing saved) if a sport change is not confirmed."""
        hourly_rate, commission = read_coach_numbers(fields)
        if coach_id is None:
            new_coach = register_coach(fields["name"].get(), fields["phone"].get(), fields["sport"].get(),
                                       hourly_rate, commission)
            return f"Coach {new_coach.get_coach_id()} {new_coach.get_name()} added."
        if not sport_change_confirmed(coach_id):
            return None
        moved_count = update_coach(coach_id, fields["name"].get(), fields["phone"].get(),
                                   fields["sport"].get(), hourly_rate, commission,
                                   fields["status"].get().upper())
        message = f"Coach {coach_id} saved."
        if moved_count > 0:
            message += f"\n{moved_count} upcoming class(es) changed to {fields['sport'].get()}."
        return message

    def delete_action(coach_id):
        """Delete the coach, or keep them as Inactive if they have past classes."""
        return delete_coach(coach_id)

    def delete_question(coach_id):
        """Confirmation question naming the coach and what will happen."""
        coach = find_coach_by_id(load_all_coaches(), coach_id)
        if coach is None:
            return f"Delete coach {coach_id}?"
        if len(classes_for_coach(coach_id)) > 0 and len(upcoming_classes_for_coach(coach_id)) == 0:
            if not coach.is_active():
                return (f"{coach_id} {coach.get_name()} is already inactive. Their past classes stay on "
                        "record, so they can't be deleted. Continue?")
            return (f"{coach_id} {coach.get_name()} has taught classes before, so they will be kept as "
                    "INACTIVE (their history stays) instead of being deleted. Continue?")
        return f"Delete coach {coach_id} {coach.get_name()} permanently?"

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

    page_state = {"adding": True}
    member_choice_ids = {}

    def show_member_row(visible):
        """Show or hide the private-session Member row."""
        if visible:
            fields["member_label"].grid(row=7, column=0, sticky="w", padx=(0, 10), pady=4)
            fields["member_menu"].grid(row=7, column=1, sticky="w", pady=4)
            fields["member_hint"].grid(row=8, column=1, sticky="w")
        else:
            fields["member_label"].grid_remove()
            fields["member_menu"].grid_remove()
            fields["member_hint"].grid_remove()

    def apply_class_type():
        """A private session is always for 1 person, so fix Max people at
        1, lock it and (when adding) ask which member it is for; a group
        class lets the user type the size."""
        fields["max_pax"].config(state="normal")
        match fields["type"].get():
            case "Private":
                fields["max_pax"].delete(0, tk.END)
                fields["max_pax"].insert(0, "1")
                fields["max_pax"].config(state="disabled")
                show_member_row(page_state["adding"])
            case "Group":
                if fields["max_pax"].get().strip() == "1":
                    fields["max_pax"].delete(0, tk.END)
                show_member_row(False)

    def build_form(form_frame):
        """Add coach, type and the date/time/size/fee fields."""
        fields["coach"] = tk.StringVar(value="")
        fields["coach_menu"], fields["coach_dropdown"], fields["set_coaches"] = common.make_filtered_menu(
            form_frame, fields["coach"], width=CHOICE_WIDTH, stacked=True,
            tip="Who teaches the class (active coaches only). The class uses this coach's sport. "
                "Can't be changed after scheduling.")
        common.add_form_row(form_frame, 0, "Coach", fields["coach_menu"],
                            tip="Who teaches the class. Click the box and type to search by name.")
        fields["type"] = tk.StringVar(value="Group")
        type_row = tk.Frame(form_frame, bg=common.PANEL_BG)
        for class_type in CLASS_TYPES:
            type_button = tk.Radiobutton(type_row, text=class_type, value=class_type, variable=fields["type"],
                                         command=apply_class_type, font=common.LABEL_FONT, bg=common.PANEL_BG,
                                         activebackground=common.PANEL_BG)
            type_button.pack(side="left", padx=(0, 8))
            type_buttons.append(type_button)
            if class_type == "Private":
                common.add_tooltip(type_button, "A private session: one coach and exactly 1 member.")
            else:
                common.add_tooltip(type_button, f"A group class: one coach and up to {MAX_GROUP_SIZE} members.")
        common.add_form_row(form_frame, 1, "Type", type_row,
                            tip="Private session or group class. Can't be changed after scheduling.")
        fields.update(add_class_time_fields(form_frame, 2))
        # Only shown when scheduling a NEW private session: the one member
        # it is for is chosen here and saved with the class.
        fields["member"] = tk.StringVar(value="")
        fields["member_label"] = tk.Label(form_frame, text="Member", font=common.LABEL_FONT,
                                          bg=common.PANEL_BG, anchor="w")
        fields["member_menu"], fields["member_dropdown"], fields["set_members"] = common.make_filtered_menu(
            form_frame, fields["member"], width=CHOICE_WIDTH, stacked=True,
            tip="The member this private session is for (members whose membership hasn't expired). "
                "They are enrolled as soon as you schedule it.")
        common.add_tooltip(fields["member_label"], "The member this private session is for.")
        # Members valid TODAY are listed; their membership is checked again for the class date on Save.
        fields["member_hint"] = tk.Label(form_frame, text="Members valid today are listed. Their membership "
                                         "is checked for the class date when you save.", font=common.SMALL_FONT,
                                         bg=common.PANEL_BG, fg=common.MUTED_TEXT_COLOR, anchor="w",
                                         justify="left", wraplength=240)

    def set_locked(locked):
        """Coach and type can't be changed on an existing class."""
        if locked:
            new_state = "disabled"
        else:
            new_state = "normal"
        # The coach box is an entry plus an arrow button: lock both.
        for coach_widget in fields["coach_menu"].winfo_children():
            coach_widget.config(state=new_state)
        for type_button in type_buttons:
            type_button.config(state=new_state)

    def clear_form():
        """Reload the coach and member lists and reset every field for a
        new class, dated tomorrow (a time today may already have passed)."""
        coach_choice_ids.clear()
        choices = []
        for coach in load_all_coaches():
            if coach.is_active():
                coach_choice_ids[coach_choice_text(coach)] = coach.get_coach_id()
                choices.append(coach_choice_text(coach))
        fields["set_coaches"](choices)
        member_choice_ids.clear()
        member_choices = []
        for member_id, member_name in members_valid_on(common.today_string()):
            choice_text = member_choice_text(member_id, member_name)
            member_choice_ids[choice_text] = member_id
            member_choices.append(choice_text)
        fields["set_members"](member_choices)
        page_state["adding"] = True
        show_member_row(False)
        set_locked(False)
        fields["type"].set("Group")
        fields["max_pax"].config(state="normal")
        for field_name in ("date", "max_pax", "fee"):
            fields[field_name].delete(0, tk.END)
        fields["date"].insert(0, common.add_days_to_date(common.today_string(), 1))
        fields["hour"].set(HOUR_CHOICES[2])
        fields["duration"].set(DURATION_CHOICES[0])

    def fill_form(class_id):
        """Load the clicked class; lock coach and type."""
        sports_class = find_class_by_id(load_all_classes(), class_id)
        if sports_class is None:
            return
        page_state["adding"] = False
        show_member_row(False)
        coach = find_coach_by_id(load_all_coaches(), sports_class.get_coach_id())
        if coach is not None:
            # Set directly: an inactive coach is not in the drop-down list.
            fields["coach"].set(coach_choice_text(coach))
        else:
            fields["coach"].set(f"{sports_class.get_coach_id()} (coach removed)")
        fields["type"].set(sports_class.get_class_type())
        fields["date"].delete(0, tk.END)
        fields["date"].insert(0, sports_class.get_date_text())
        fields["hour"].set(f"{sports_class.get_start_hour():02d}:00")
        if 1 <= sports_class.get_duration_hrs() <= MAX_CLASS_DURATION:
            fields["duration"].set(DURATION_CHOICES[sports_class.get_duration_hrs() - 1])
        fields["max_pax"].delete(0, tk.END)
        fields["max_pax"].insert(0, str(sports_class.get_max_pax()))
        if sports_class.get_class_type() == "Private":
            fields["max_pax"].config(state="disabled")
        fields["fee"].insert(0, f"{sports_class.get_fee_per_pax():.2f}")
        set_locked(True)

    def save_action(class_id):
        """Schedule a new class (class_id None) or save the edited one."""
        date_text, start_hour, duration_hours, max_pax, fee = read_class_values(fields)
        if class_id is None:
            if fields["coach"].get() not in coach_choice_ids:
                raise ValueError("Please pick a coach (or add one in Manage Coaches).")
            member_id = None
            if fields["type"].get() == "Private":
                if fields["member"].get() not in member_choice_ids:
                    raise ValueError("Pick the member this private session is for.")
                member_id = member_choice_ids[fields["member"].get()]
            new_class = schedule_class(coach_choice_ids[fields["coach"].get()], fields["type"].get(), date_text,
                                       start_hour, duration_hours, max_pax, fee, member_id)
            message = (f"Class {new_class.get_class_id()} scheduled: {new_class.get_sport()} "
                       f"{new_class.get_class_type()}, {new_class.get_date_text()} {new_class.get_time_text()}.")
            if member_id is not None:
                message += f"\n{member_id} is enrolled in it."
            return message
        update_class(class_id, date_text, start_hour, duration_hours, max_pax, fee)
        return f"Class {class_id} saved."

    def delete_action(class_id):
        """Cancel (permanently remove) the class."""
        cancel_class(class_id)
        return f"Class {class_id} deleted."

    def delete_question(class_id):
        """Confirmation question naming the class and any enrolled members,
        or None for a class that has started (no question: Delete just
        explains that it is kept as a record)."""
        sports_class = find_class_by_id(load_all_classes(), class_id)
        if sports_class is None:
            return f"Delete class {class_id}?"
        if class_has_started(sports_class):
            return None
        question = (f"Delete class {class_id} ({sports_class.get_sport()} {sports_class.get_class_type()}, "
                    f"{sports_class.get_date_text()} {sports_class.get_time_text()})?")
        participant_list = sports_class.get_participant_list()
        if len(participant_list) > 0:
            member_names = load_member_names()
            name_list = []
            for member_id in participant_list:
                name_list.append(f"{member_id} {member_names.get(member_id, '(member removed)')}")
            question += (f"\n\n{len(participant_list)} member(s) are enrolled and will be taken out of it:\n"
                         + "\n".join(name_list))
        return question + "\n\nThis cannot be undone."

    def load_rows(search_text):
        """Every class, soonest first, or only those of one sport."""
        rows = class_rows(False, False)
        if search_text == "":
            return rows
        sport_class_ids = set()
        for sports_class in search_classes(load_all_classes(), "sport", search_text):
            sport_class_ids.add(sports_class.get_class_id())
        matching_rows = []
        for row in rows:
            if row[0] in sport_class_ids:
                matching_rows.append(row)
        return matching_rows

    def summary_text():
        """Explain the grey rows under the list."""
        return ("Grey rows are classes that are over (or under way). They are kept as a record of the hours "
                "worked, so they can't be edited or deleted. A class with a bill keeps its fee and duration.")

    page_hooks["Manage Classes"] = common.build_manage_page(
        page_frame, CLASS_LIST_HEADER, load_rows, "class", build_form, clear_form, fill_form,
        save_action, delete_action, delete_question, add_label="Schedule Class", search_label="Sport",
        summary_text=summary_text, empty_text="No classes found.")


def build_enrol_page(page_frame):
    """Build the Enrol Member page and return its refresh function."""
    form_widgets = {}
    member_choice_ids = {}

    def build_form(form_frame):
        """Add the member search box (type to search, or click the arrow)."""
        form_widgets["member"] = tk.StringVar(value="")
        form_widgets["menu"], form_widgets["dropdown"], form_widgets["set_members"] = common.make_filtered_menu(
            form_frame, form_widgets["member"], width=CHOICE_WIDTH,
            tip="The member to add. People already in this class, and members whose membership "
                "ends before the class, are not listed.")
        common.add_form_row(form_frame, 0, "Member", form_widgets["menu"],
                            tip="The member to add. Click the box and type to search by name or ID.")

    def fill_form(class_id):
        """List members not already in the picked class whose membership
        is still valid on the class day."""
        sports_class = find_class_by_id(load_all_classes(), class_id)
        enrolled = []
        class_date = common.today_string()
        if sports_class is not None:
            enrolled = sports_class.get_participant_list()
            class_date = sports_class.get_date_text()
        member_choice_ids.clear()
        choices = []
        for member_id, member_name in members_valid_on(class_date):
            if member_id not in enrolled:
                choice_text = member_choice_text(member_id, member_name)
                member_choice_ids[choice_text] = member_id
                choices.append(choice_text)
        form_widgets["set_members"](choices)

    def enrol_action(class_id):
        """Enrol the chosen member."""
        if form_widgets["member"].get() not in member_choice_ids:
            raise ValueError("Pick a member to enrol.")
        member_id = member_choice_ids[form_widgets["member"].get()]
        enrol_participant(class_id, member_id)
        return f"{member_id} enrolled in {class_id}."

    def open_rows(search_text):
        """Classes that haven't started and still have space, optionally
        only those whose sport or coach's name contains search_text."""
        rows = class_rows(True, True)
        if search_text == "":
            return rows
        matching_ids = set()
        all_classes = load_all_classes()
        for sports_class in search_classes(all_classes, "sport", search_text):
            matching_ids.add(sports_class.get_class_id())
        for coach in search_coaches(load_all_coaches(), "name", search_text):
            for sports_class in search_classes(all_classes, "coach", coach.get_coach_id()):
                matching_ids.add(sports_class.get_class_id())
        matching_rows = []
        for class_id, row_text in rows:
            if class_id in matching_ids:
                matching_rows.append((class_id, row_text))
        return matching_rows

    return common.build_pick_page(page_frame, CLASS_LIST_HEADER, open_rows, "Enrol", enrol_action,
                                  refresh_on_error=True,
                                  describe=describe_class, build_form=build_form, fill_form=fill_form,
                                  search_label="Sport or coach name",
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
        section_frame, f"{'Coach name':<21}{'Coach ID':<9}{'Classes':>8}{'Hours':>7}{'Pay (RM)':>11}"
                       f"{'Commission (RM)':>17}{'Upcoming':>10}")
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
        # Only classes that are over count as worked: an upcoming class
        # hasn't been taught (or earned) yet, so it is listed separately.
        worked_classes, upcoming_classes = split_worked_classes(load_all_classes())
        month_classes = classes_in_month(worked_classes, month_text)
        hours_dict = coach_hours_by_month(worked_classes, month_text)
        upcoming_hours_dict = coach_hours_by_month(upcoming_classes, month_text)

        report_listbox.delete(0, tk.END)
        total_hours = 0
        total_upcoming_hours = 0
        pay_sum = 0.0
        commission_sum = 0.0
        coach_list = load_all_coaches()
        if search_entry.get().strip() != "":
            coach_list = search_coaches(coach_list, "name", search_entry.get())
        for coach in coach_list:
            coach_id = coach.get_coach_id()
            coach_classes = search_classes(month_classes, "coach", coach_id)
            commission = total_commission(coach_classes, coach.get_commission_pct())
            coach_hours = hours_dict.get(coach_id, 0)
            coach_pay = coach_hours * coach.get_hourly_rate()
            upcoming_hours = upcoming_hours_dict.get(coach_id, 0)
            total_hours += coach_hours
            total_upcoming_hours += upcoming_hours
            pay_sum += coach_pay
            commission_sum += commission
            coach_name = coach.get_name()
            if not coach.is_active():
                coach_name += " (inactive)"
            report_listbox.insert(tk.END, (f"{common.fit_text(coach_name, 20):<21}{coach_id:<9}"
                                           f"{len(coach_classes):>8}{coach_hours:>7}{coach_pay:>11.2f}"
                                           f"{commission:>17.2f}{str(upcoming_hours) + ' h':>10}"))
        summary_line = (f"Worked: {total_hours} hours, pay RM {pay_sum:.2f}, commission "
                        f"RM {commission_sum:.2f}.   Upcoming (not counted yet): "
                        f"{total_upcoming_hours} hours")
        if month_text != "" and len(month_classes) == 0:
            summary_line = "Nothing worked yet in this month.   " + summary_line
        total_label.config(text=summary_line)

    def on_month_changed(chosen_month):
        """Recalculate when a different month is picked."""
        refresh_report()

    month_menu = common.make_option_menu(top_row, month_variable, ["All time"],
                                         command=on_month_changed, width=10,
                                         tip="Pick a month (YYYY-MM) to see only that month's classes, "
                                             "or All time for everything.")
    month_menu.pack(side="left", padx=6)
    tk.Label(top_row, text="Coach name:", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left", padx=(16, 0))
    search_entry = common.make_entry(top_row, width=18,
                                     tip="Type part of a coach's name and press Enter or click Search. "
                                         "Leave it empty to show every coach.")
    search_entry.pack(side="left", padx=6)

    def on_search_key(event):
        """Search when Enter is pressed in the name box."""
        refresh_report()

    search_entry.bind("<Return>", on_search_key)
    common.make_button(top_row, "Search", refresh_report,
                       tip="Show only coaches whose name contains the text in the box.").pack(side="left")

    def on_show():
        """Rebuild the month list (from class dates) and the report."""
        month_set = set()
        for sports_class in load_all_classes():
            month_set.add(sports_class.get_date_text()[0:7])
        month_choices = ["All time"]
        for month_text in sorted(month_set):
            month_choices.append(month_text)
        common.set_option_menu_choices(month_menu, month_variable, month_choices, command=on_month_changed)
        refresh_report()

    page_hooks["Hours & Commission"] = on_show
