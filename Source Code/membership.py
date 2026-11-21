"""
Module      : membership.py
Member 2    : Teoh Zynn (student ID: 26PMD03025)
Purpose     : Membership Registration module - lets the public register
              for a membership type (Annual, Monthly, Pay-As-You-Go, VIP,
              Youth, Senior, Family), and view, edit, renew or remove
              members.
Date        : 2026-11-07
"""

# MAP OF THIS FILE (press Ctrl+F and type a section name to jump to it):
#   1 CLASS ............ Member (child of common.Person)
#   2 LOGIC (no screens) saving/loading members.txt, register / update / renew / delete, the RULES that
#                        stop a member being deleted, expiry and summary numbers
#   3 SCREEN (tkinter) . MEMBERSHIP_ACTIONS menu, the Register page (one card per membership type),
#                        the Manage Members page, the Renew page
#   4 ENTRY POINT ...... build_membership_tab(parent) is called by main.py
# members.txt line:  id|name|phone|membership type|join date|expiry date
# The membership TYPES, FEES, DISCOUNTS and DURATIONS live in common.py (SETTINGS), not here.
# Tip: a CHANGE HERE IF line above a function says when you would edit it.

import datetime
import os
import tkinter as tk
from tkinter import messagebox

import common


# ---------------------------------------------------------------------------
# CLASS (encapsulation + inheritance from common.Person)
# ---------------------------------------------------------------------------
class Member(common.Person):
    """A registered member. Inherits name/phone handling from Person and
    adds membership-specific private attributes."""

    def __init__(self, member_id, name, phone, membership_type, join_date, expiry_date):
        """Create the object and validate its starting values."""
        super().__init__(name, phone)
        self.__member_id = member_id
        self.__membership_type = ""
        if not common.is_valid_date(join_date):
            raise ValueError("Join date must be YYYY-MM-DD.")
        self.__join_date = common.normalize_date(join_date)
        self.__expiry_date = ""
        self.set_expiry_date(expiry_date)
        self.set_membership_type(membership_type)

    def get_member_id(self):
        """Return the member's ID."""
        return self.__member_id

    def get_membership_type(self):
        """Return the membership type."""
        return self.__membership_type

    def set_membership_type(self, membership_type):
        """Validate and store the membership type."""
        if membership_type not in common.MEMBERSHIP_TYPES:
            raise ValueError("Membership type is not recognised.")
        self.__membership_type = membership_type

    def get_join_date(self):
        """Return the join date (YYYY-MM-DD)."""
        return self.__join_date

    def get_expiry_date(self):
        """Return the expiry date (YYYY-MM-DD)."""
        return self.__expiry_date

    def set_expiry_date(self, expiry_date):
        """Validate and store a new expiry date."""
        if not common.is_valid_date(expiry_date):
            raise ValueError("Expiry date must be YYYY-MM-DD.")
        self.__expiry_date = common.normalize_date(expiry_date)

    def to_line(self):
        """Turn this member into a pipe-delimited text-file line."""
        return "|".join([
            self.__member_id, self.get_name(), self.get_phone(),
            self.__membership_type, self.__join_date, self.__expiry_date,
        ])


# ---------------------------------------------------------------------------
# LOGIC LAYER (plain functions, no tkinter - callable and testable on their own)
# ---------------------------------------------------------------------------
# Membership card pictures: aim for this width, never show wider than the maximum (pixels).
# Four cards per row must fit the 1000 px window with the Register button, so keep the max under 240.
CARD_PICTURE_WIDTH = 220
CARD_PICTURE_MAX_WIDTH = 230

# ===== SAVING: reading members.txt (a line with the wrong number of fields is skipped) =====
MEMBER_FIELD_COUNT = 6


def line_to_member(line):
    """Convert one text-file line into a Member object, or None if the
    line is malformed (wrong number of fields)."""
    fields = common.split_fields(line, MEMBER_FIELD_COUNT)
    if fields is None:
        return None
    # A hand-edited bad date (2027-13-40) makes the line unreadable: it is hidden but kept in the
    # file. Short dates (2027-1-5) are tidied to 2027-01-05, because dates are compared as text.
    if not common.is_valid_date(fields[4]) or not common.is_valid_date(fields[5]):
        return None
    try:
        return Member(fields[0], fields[1], fields[2], fields[3],
                      common.normalize_date(fields[4]), common.normalize_date(fields[5]))
    except ValueError:
        return None


def load_all_members():
    """Read members.txt and return a list of Member objects. Malformed
    lines are skipped rather than crashing the program."""
    member_list = []
    for line in common.read_lines(common.MEMBERS_FILE):
        member = line_to_member(line)
        if member is not None:
            member_list.append(member)
    return member_list


def get_phone_set(member_list):
    """Return a set of all phone numbers currently used (duplicate check)."""
    phone_set = set()
    for member in member_list:
        phone_set.add(member.get_phone())
    return phone_set


def find_member_by_id(member_list, member_id):
    """Linear search for a member by ID using a while loop (as opposed to
    the for-loop searches used elsewhere). Returns the Member or None."""
    index = 0
    while index < len(member_list):
        if member_list[index].get_member_id() == member_id:
            return member_list[index]
        index += 1
    return None


# ===== REGISTERING A MEMBER =====
# CHANGE HERE IF: you change the registration rules. Now: the phone must not already be registered,
# and expiry = join date + the type's days from common.MEMBERSHIP_DURATION_DAYS.
def register_member(name, phone, membership_type):
    """Validate input, build a new Member, append it to the file, return it.
    Raises ValueError on invalid input or duplicate phone number."""
    member_list = load_all_members()
    if phone.strip() in get_phone_set(member_list):
        raise ValueError("This phone number is already registered.")

    join_date = common.today_string()
    duration_days = common.MEMBERSHIP_DURATION_DAYS.get(membership_type, 365)
    expiry_date = common.add_days_to_date(join_date, duration_days)
    new_id = common.generate_id(common.MEMBERS_FILE, "MEM")

    new_member = Member(new_id, name, phone, membership_type, join_date, expiry_date)
    common.append_line(common.MEMBERS_FILE, new_member.to_line())
    return new_member


def search_members(member_list, search_field, search_text):
    """Return members matching search_field ('id', 'name', 'type') using
    case-insensitive partial match for name, exact for id/type."""
    results = []
    search_text_lower = search_text.strip().lower()
    for member in member_list:
        match search_field:
            case "id":
                if member.get_member_id().lower() == search_text_lower:
                    results.append(member)
            case "name":
                if search_text_lower in member.get_name().lower():
                    results.append(member)
            case "type":
                if member.get_membership_type().lower() == search_text_lower:
                    results.append(member)
    return results


BOOKING_FIELD_COUNT = 8
BILL_FIELD_COUNT = 10
CLASS_FIELD_COUNT = 10


# ===== RULES: what stops a member being deleted (all three are called by delete_member) =====
# CHANGE HERE IF: you change the 'upcoming booking' rule for deleting a member.
def has_future_confirmed_booking(member_id):
    """Return True if member_id has a CONFIRMED booking that has not started yet (a later date, or
    today with a start hour still to come). A booking that has already started today is
    reported by started_booking_today instead."""
    today = common.today_string()
    now_hour = common.current_hour()
    for line in common.read_lines(common.BOOKINGS_FILE):
        fields = common.split_fields(line, BOOKING_FIELD_COUNT)
        if fields is None:
            continue
        booking_member_id = fields[1]
        booking_date = fields[4]
        booking_status = fields[7]
        if booking_member_id != member_id or booking_status != "CONFIRMED" or booking_date < today:
            continue
        started = booking_date == today and fields[5].isdigit() and int(fields[5]) <= now_hour
        if not started:
            return True
    return False


def started_booking_today(member_id):
    """Return the ID of a CONFIRMED booking of member_id that has already started today (so it is
    kept as a record and can't be cancelled), or None."""
    today = common.today_string()
    now_hour = common.current_hour()
    for line in common.read_lines(common.BOOKINGS_FILE):
        fields = common.split_fields(line, BOOKING_FIELD_COUNT)
        if fields is None:
            continue
        if (fields[1] == member_id and fields[7] == "CONFIRMED" and fields[4] == today
                and fields[5].isdigit() and int(fields[5]) <= now_hour):
            return fields[0]
    return None


# CHANGE HERE IF: you change the 'enrolled in an upcoming class' rule for deleting a member.
def upcoming_class_for_member(member_id):
    """Return the ID of a class that hasn't started yet with member_id
    enrolled, or None. Read straight from classes.txt (membership does not
    import coaching.py)."""
    today = common.today_string()
    for line in common.read_lines(common.CLASSES_FILE):
        fields = common.split_fields(line, CLASS_FIELD_COUNT)
        if fields is None or not fields[5].isdigit():
            continue
        class_date = fields[4]
        not_started = class_date > today or (class_date == today and int(fields[5]) > common.current_hour())
        if not_started and member_id in fields[9].split(";"):
            return fields[0]
    return None


# CHANGE HERE IF: you change the 'unpaid bill' rule for deleting a member.
def has_unpaid_bill(member_id):
    """Return True if member_id has a bill that is still UNPAID."""
    for line in common.read_lines(common.BILLS_FILE):
        fields = common.split_fields(line, BILL_FIELD_COUNT)
        if fields is None:
            continue
        bill_member_id = fields[1]
        payment_status = fields[8]
        if bill_member_id == member_id and payment_status == "UNPAID":
            return True
    return False


# CHANGE HERE IF: you change what may be edited on a member and the checks on it (phone must stay unique).
def update_member(member_id, new_name, new_phone, new_type):
    """Update an existing member's name, phone and type. Returns the
    updated member list. Raises ValueError if member_id not found or
    the phone number clashes with another member."""
    member_list = load_all_members()
    updated_lines = []
    member_found = False

    for member in member_list:
        if member.get_member_id() == member_id:
            for other_member in member_list:
                if other_member.get_member_id() != member_id and other_member.get_phone() == new_phone.strip():
                    raise ValueError("Another member already uses this phone number.")
            member.set_name(new_name)
            member.set_phone(new_phone)
            if new_type != member.get_membership_type():
                # A different type starts a NEW membership period today (like Renew), so the expiry
                # is today + the new type's days. Billing works out "this period" from the expiry.
                member.set_membership_type(new_type)
                member.set_expiry_date(common.add_days_to_date(
                    common.today_string(), common.MEMBERSHIP_DURATION_DAYS.get(new_type, 365)))
            member_found = True
        updated_lines.append(member.to_line())

    if not member_found:
        raise ValueError(f"No member found with ID {member_id}.")

    common.rewrite_records(common.MEMBERS_FILE, updated_lines, line_to_member)
    return load_all_members()


# CHANGE HERE IF: you change how renewing works. Now: new expiry = TODAY + the type's duration.
def renew_member(member_id):
    """Extend a member's expiry date from today by their type's duration.
    Returns the new expiry date string."""
    member_list = load_all_members()
    updated_lines = []
    new_expiry = None

    # Renewing counts from TODAY, not from the old expiry date, so a member
    # who renews early does not get the unused days added on top, and one
    # who lapsed months ago is not charged for the gap.
    # Every member is written back (changed or not) because the file is
    # rewritten as a whole.
    for member in member_list:
        if member.get_member_id() == member_id:
            duration_days = common.MEMBERSHIP_DURATION_DAYS.get(member.get_membership_type(), 365)
            new_expiry = common.add_days_to_date(common.today_string(), duration_days)
            member.set_expiry_date(new_expiry)
        updated_lines.append(member.to_line())

    if new_expiry is None:
        raise ValueError(f"No member found with ID {member_id}.")

    common.rewrite_records(common.MEMBERS_FILE, updated_lines, line_to_member)
    return new_expiry


# CHANGE HERE IF: you change the rules that block deleting a member. The three checks are the first
# lines of this function: remove one to stop it blocking, or add a new check the same way.
def delete_member(member_id):
    """Delete a member permanently. Blocked if the member has a future
    confirmed booking or an unpaid bill."""
    # A member may only be removed when nothing else points at them:
    # no booking still to be used, no bill still to be paid, and no class
    # still to attend. Otherwise those records would name someone who no
    # longer exists. The checks read the other modules' files directly
    # (membership.py does not import booking.py or coaching.py).
    if has_future_confirmed_booking(member_id):
        raise ValueError("Cannot delete: member has an upcoming confirmed booking.")
    started_id = started_booking_today(member_id)
    if started_id is not None:
        raise ValueError(f"Cannot delete: booking {started_id} has already started today, so it is kept as a "
                         "record. Try again tomorrow.")
    if has_unpaid_bill(member_id):
        raise ValueError("Cannot delete: member has an unpaid bill.")
    class_id = upcoming_class_for_member(member_id)
    if class_id is not None:
        raise ValueError(f"Cannot delete: member is enrolled in upcoming class {class_id}. "
                         "Take them out first (Coaching > Remove Member).")

    member_list = load_all_members()
    remaining_lines = []
    member_found = False
    for member in member_list:
        if member.get_member_id() == member_id:
            member_found = True
        else:
            remaining_lines.append(member.to_line())

    if not member_found:
        raise ValueError(f"No member found with ID {member_id}.")

    common.rewrite_records(common.MEMBERS_FILE, remaining_lines, line_to_member)


# ===== FORCE DELETE: clear the records that block a delete, after the user agrees =====
# CHANGE HERE IF: you change what a force delete clears. It stays inside the project rules: bills are
# VOIDED (never deleted), bookings are CANCELLED (never deleted), and anything the rules can't undo (a
# PAID bill, a booking that has started) stops the force delete before anything is changed.
def readable_bill_line(line):
    """Parser for rewrite_records: the fields of a bills.txt line, or None if it is damaged."""
    return common.split_fields(line, BILL_FIELD_COUNT)


def readable_booking_line(line):
    """Parser for rewrite_records: the fields of a bookings.txt line, or None if it is damaged."""
    return common.split_fields(line, BOOKING_FIELD_COUNT)


def readable_class_line(line):
    """Parser for rewrite_records: the fields of a classes.txt line, or None if it is damaged."""
    return common.split_fields(line, CLASS_FIELD_COUNT)


def force_delete_plan(member_id):
    """Work out what a force delete of this member would do, WITHOUT changing anything.
    Returns a dictionary of lists: void_ids / void_bills (unpaid bills to void), cancel_bookings
    (upcoming CONFIRMED bookings to cancel), leave_classes (upcoming classes to take them out of)
    and stuck (reasons the project rules do not allow it; if any, nothing may be changed)."""
    today = common.today_string()
    now_hour = common.current_hour()
    plan = {"void_ids": [], "void_bills": [], "cancel_bookings": [], "leave_classes": [], "stuck": []}
    all_bills = common.read_fields(common.BILLS_FILE, BILL_FIELD_COUNT)
    for bill in all_bills:
        if bill[1] == member_id and bill[8] == "UNPAID":
            plan["void_ids"].append(bill[0])
            plan["void_bills"].append(f"{bill[0]} ({bill[4]}, RM {bill[7]})")

    for booking in common.read_fields(common.BOOKINGS_FILE, BOOKING_FIELD_COUNT):
        if booking[1] != member_id or booking[7] != "CONFIRMED" or booking[4] < today:
            continue
        if booking[4] == today and booking[5].isdigit() and int(booking[5]) <= now_hour:
            plan["stuck"].append(f"Booking {booking[0]} has already started, so it is kept as a record "
                                 "and can't be cancelled.")
            continue
        plan["cancel_bookings"].append(booking[0])
        for bill in all_bills:
            if bill[2] == "COURT" and bill[3] == booking[0] and bill[8] != "VOID" and bill[0] not in plan["void_ids"]:
                if bill[8] == "PAID":
                    plan["stuck"].append(f"Booking {booking[0]} has bill {bill[0]}, which is paid. A paid bill "
                                         "can't be voided, so the booking can't be cancelled.")
                else:
                    plan["stuck"].append(f"Booking {booking[0]} is billed to {bill[1]} (bill {bill[0]}), "
                                         "so it can't be cancelled.")

    for class_fields in common.read_fields(common.CLASSES_FILE, CLASS_FIELD_COUNT):
        if not class_fields[5].isdigit() or member_id not in class_fields[9].split(";"):
            continue
        not_started = class_fields[4] > today or (class_fields[4] == today and int(class_fields[5]) > now_hour)
        if not not_started:
            continue
        plan["leave_classes"].append(class_fields[0])
        for bill in all_bills:
            if (bill[2] == "COACHING" and bill[3] == class_fields[0] and bill[1] == member_id
                    and bill[8] != "VOID" and bill[0] not in plan["void_ids"]):
                plan["stuck"].append(f"Class {class_fields[0]} has bill {bill[0]} for this member, which is paid. "
                                     "A paid bill can't be voided, so they can't be taken out of the class.")
    return plan


def force_delete_text(plan):
    """The bullet list shown to the user: everything a force delete would do first."""
    lines = []
    if len(plan["void_bills"]) > 0:
        lines.append("- void " + str(len(plan["void_bills"])) + " unpaid bill(s): " + ", ".join(plan["void_bills"]))
    if len(plan["cancel_bookings"]) > 0:
        lines.append("- cancel " + str(len(plan["cancel_bookings"])) + " upcoming booking(s) (kept as CANCELLED): "
                     + ", ".join(plan["cancel_bookings"]))
    if len(plan["leave_classes"]) > 0:
        lines.append("- take the member out of " + str(len(plan["leave_classes"])) + " upcoming class(es): "
                     + ", ".join(plan["leave_classes"]))
    return "\n".join(lines)


def force_delete_member(member_id):
    """Void the member's unpaid bills, cancel their upcoming bookings, take them out of upcoming
    classes, then delete them with the normal rules. Raises ValueError (and changes NOTHING) if
    the project rules don't allow it. Returns the message to show."""
    if find_member_by_id(load_all_members(), member_id) is None:
        raise ValueError(f"No member found with ID {member_id}.")
    plan = force_delete_plan(member_id)
    if len(plan["stuck"]) > 0:
        raise ValueError("Force delete is not possible:\n- " + "\n- ".join(plan["stuck"]))

    # Four files are written one after another. If any write fails (e.g. a file open in another
    # program), every file is put back as it was, so the data is never left half changed.
    snapshot = common.snapshot_files((common.BILLS_FILE, common.BOOKINGS_FILE, common.CLASSES_FILE,
                                      common.MEMBERS_FILE))
    try:
        if len(plan["void_ids"]) > 0:
            new_lines = []
            for fields in common.read_fields(common.BILLS_FILE, BILL_FIELD_COUNT):
                if fields[0] in plan["void_ids"]:
                    fields[8] = "VOID"
                new_lines.append("|".join(fields))
            common.rewrite_records(common.BILLS_FILE, new_lines, readable_bill_line)
        if len(plan["cancel_bookings"]) > 0:
            new_lines = []
            for fields in common.read_fields(common.BOOKINGS_FILE, BOOKING_FIELD_COUNT):
                if fields[0] in plan["cancel_bookings"]:
                    fields[7] = "CANCELLED"
                new_lines.append("|".join(fields))
            common.rewrite_records(common.BOOKINGS_FILE, new_lines, readable_booking_line)
        if len(plan["leave_classes"]) > 0:
            new_lines = []
            for fields in common.read_fields(common.CLASSES_FILE, CLASS_FIELD_COUNT):
                if fields[0] in plan["leave_classes"]:
                    remaining = []
                    for participant in fields[9].split(";"):
                        if participant != member_id and participant != "":
                            remaining.append(participant)
                    fields[9] = ";".join(remaining)
                new_lines.append("|".join(fields))
            common.rewrite_records(common.CLASSES_FILE, new_lines, readable_class_line)

        delete_member(member_id)   # the normal blockers are cleared now, so the normal rules pass
    except (ValueError, OSError) as error:
        not_restored = common.restore_files(snapshot)
        if len(not_restored) == 0:
            raise ValueError(f"Force delete stopped: {error} Nothing was changed: your records were put back "
                             "as they were.")
        raise ValueError(f"Force delete stopped: {error} These files could not be put back, please check "
                         f"them: {', '.join(not_restored)}.")
    message = f"Member {member_id} deleted."
    if force_delete_text(plan) != "":
        message = message + "\nAlso done first:\n" + force_delete_text(plan)
    return message


def count_members_by_type(member_list):
    """Return a dictionary of membership_type -> count."""
    type_counts = {}
    for member in member_list:
        member_type = member.get_membership_type()
        if member_type in type_counts:
            type_counts[member_type] += 1
        else:
            type_counts[member_type] = 1
    return type_counts


# CHANGE HERE IF: you change the 'expiring soon' warning window (days) shown under the member list.
EXPIRY_WARNING_DAYS = 30


def members_expiring_within(member_list, days=EXPIRY_WARNING_DAYS):
    """Return members whose expiry date is within 'days' days from today
    (30 if the caller doesn't say: a default parameter value)."""
    today = common.parse_date(common.today_string())
    expiring_list = []
    for member in member_list:
        expiry = common.parse_date(member.get_expiry_date())
        days_left = (expiry - today).days
        if 0 <= days_left <= days:
            expiring_list.append(member)
    return expiring_list


def count_members_of_types(member_list, *membership_types):
    """Count the members whose type is any of the types passed in, e.g.
    count_members_of_types(members, "VIP", "Family"). The * in
    *membership_types collects any number of types into one tuple."""
    wanted_types = set(membership_types)
    counted = 0
    for member in member_list:
        if member.get_membership_type() in wanted_types:
            counted += 1
    return counted


def members_summary_numbers(member_list, days=EXPIRY_WARNING_DAYS):
    """Return FOUR values at once: (total, active, expired, expiring_soon).
    The caller unpacks them: total, active, expired, soon = members_summary_numbers(list)."""
    active_count = 0
    for member in member_list:
        if member_status(member) == "Active":
            active_count += 1
    total_count = count_members(member_list)
    expiring_count = len(members_expiring_within(member_list, days=days))
    return total_count, active_count, total_count - active_count, expiring_count


def count_members(member_list):
    """Count members: recursively (rubric) for normal sizes, with len()
    above common.RECURSION_SAFE_LIMIT, where recursion would crash."""
    if len(member_list) <= common.RECURSION_SAFE_LIMIT:
        return count_members_recursive(member_list)
    return len(member_list)


def count_members_recursive(member_list, index=0):
    """Recursively count members in member_list starting from index.
    Demonstrates recursion (taught topic) instead of len()."""
    if index >= len(member_list):
        return 0
    return 1 + count_members_recursive(member_list, index + 1)


def duration_text(days):
    """Turn a membership length in days into words, e.g. 365 -> '1 year'."""
    if days == 365:
        return "1 year"
    elif days == 30:
        return "1 month"
    elif days % 30 == 0:
        return f"{days // 30} months"
    else:
        return f"{days} days"


def days_until_expiry(member):
    """Return how many days are left on a membership (negative once it has
    expired), or None if the saved expiry date can't be read. Uses the
    datetime module directly."""
    try:
        expiry = datetime.datetime.strptime(member.get_expiry_date(), "%Y-%m-%d").date()
    except ValueError:
        return None
    else:
        return (expiry - datetime.date.today()).days


def days_left_text(member):
    """Words for days_until_expiry, e.g. '12 day(s) left' or 'expired 3 day(s) ago'."""
    days_left = days_until_expiry(member)
    if days_left is None:
        return "unknown"
    elif days_left < 0:
        return f"expired {-days_left} day(s) ago"
    return f"{days_left} day(s) left"


# CHANGE HERE IF: you change when a member counts as Active or Expired.
def member_status(member):
    """Return 'Active' or 'Expired' by comparing the expiry date to today."""
    if member.get_expiry_date() >= common.today_string():
        return "Active"
    return "Expired"


# ---------------------------------------------------------------------------
# GUI LAYER
#
# The tab opens on a menu asking "What would you like to do?". Each
# action has its own one-page screen with a Back button: Register,
# Manage Members (update and delete on one page), Renew Membership.
# ---------------------------------------------------------------------------
# ===== SCREEN: everything below builds the Membership tab's pages =====
# CHANGE HERE IF: you add or rename a button on the Membership menu (name, hint, page instructions).
MEMBERSHIP_ACTIONS = [
    ("Register", "Sign up a new member",
     "Type the name and phone, click the membership type they want, then click Register."),
    ("Manage Members", "See, update or delete members",
     "Click a member to update them, then Save Changes. Click Delete beside a member to remove "
     "them (not allowed with an upcoming booking or unpaid bill)."),
    ("Renew Membership", "Extend a membership",
     "Click the member, then click Renew. The membership is extended from today."),
]

MEMBER_LIST_HEADER = f"{'Member ID':<10}{'Name':<20}{'Type':<14}{'Expires':<11}{'Status':<8}"


# SCREEN: shows an error message box (used by every handler below).
def show_problem(error):
    """Show a ValueError's plain message in a standard error box."""
    messagebox.showerror("Please check", str(error))


# ===== SCREEN: the Membership tab entry point (called by main.py) =====
def build_membership_tab(parent):
    """Build the Membership Registration tab inside parent (the main
    window's tab area) and return its frame. The tab opens on a menu
    asking what to do; each action has its own simple page."""
    window = tk.Frame(parent, bg=common.APP_BG)
    page_frames, page_hooks = common.build_action_menu(window, "Membership Registration", MEMBERSHIP_ACTIONS)
    build_register_page(page_frames["Register"], page_hooks)
    build_manage_members_page(page_frames["Manage Members"], page_hooks)
    page_hooks["Renew Membership"] = common.build_pick_page(
        page_frames["Renew Membership"], MEMBER_LIST_HEADER, member_rows, "Renew", renew_action,
        describe=describe_member, search_label="Name", empty_text="No members yet.")
    return window


# ----- what each list row, the details panel and the summary line show -----
def member_rows(search_text):
    """Return (member_id, row_text) for every member, or for those whose
    name contains search_text."""
    member_list = load_all_members()
    if search_text != "":
        member_list = search_members(member_list, "name", search_text)
    rows = []
    for member in member_list:
        rows.append((member.get_member_id(), (f"{member.get_member_id():<10}"
                                              f"{common.fit_text(member.get_name(), 19):<20}"
                                              f"{member.get_membership_type():<14}{member.get_expiry_date():<11}"
                                              f"{member_status(member):<8}")))
    return rows


def describe_member(member_id):
    """Return the details text for one member (found with the while loop)."""
    member = find_member_by_id(load_all_members(), member_id)
    if member is None:
        return "This member no longer exists."
    return common.details_text([
        ("Member ID", member.get_member_id()),
        ("Name", member.get_name()),
        ("Phone", member.get_phone()),
        ("Type", member.get_membership_type()),
        ("Joined", member.get_join_date()),
        ("Expires", member.get_expiry_date()),
        ("Days left", days_left_text(member)),
        ("Status", member_status(member)),
    ])


# ----- button actions: each returns the message shown to the user, or raises ValueError -----
def renew_action(member_id):
    """Renew the picked member and say until when."""
    new_expiry = renew_member(member_id)
    return f"Membership renewed until {new_expiry}."


def delete_action(member_id):
    """Delete the picked member. If bookings, bills or classes block it, offer a FORCE DELETE:
    list what would be cleared first and ask Yes/No. Returns None if the user says No."""
    try:
        delete_member(member_id)
    except ValueError as error:
        plan = force_delete_plan(member_id)
        nothing_to_clear = (len(plan["void_ids"]) + len(plan["cancel_bookings"]) + len(plan["leave_classes"])
                            + len(plan["stuck"])) == 0
        if find_member_by_id(load_all_members(), member_id) is None or nothing_to_clear:
            raise
        if len(plan["stuck"]) > 0:
            raise ValueError(f"{error}\n\nForce delete is not possible:\n- " + "\n- ".join(plan["stuck"]))
        question = (f"{error}\n\nForce delete will first:\n{force_delete_text(plan)}\n\n"
                    "then delete the member. Past bookings and paid bills stay on record. "
                    "This cannot be undone.\n\nForce delete?")
        if not messagebox.askyesno("Force delete", question):
            return None
        return force_delete_member(member_id)
    return f"Member {member_id} deleted."


def delete_question(member_id):
    """Confirmation question for deleting a member, naming them."""
    member = find_member_by_id(load_all_members(), member_id)
    if member is None:
        return f"Delete member {member_id} permanently?"
    return f"Delete member {member_id} {member.get_name()} permanently?"


def members_summary():
    """One line under the Manage Members list: total (counted recursively),
    members per type, and how many expire within 30 days."""
    all_members = load_all_members()
    type_counts = count_members_by_type(all_members)
    count_parts = []
    for membership_type in common.MEMBERSHIP_TYPES:
        if membership_type in type_counts:
            count_parts.append(f"{membership_type} {type_counts[membership_type]}")
    total_count, active_count, expired_count, expiring_count = members_summary_numbers(all_members)
    premium_count = count_members_of_types(all_members, "VIP", "Family")
    return (f"{total_count} members ({active_count} active, {expired_count} expired; "
            f"{', '.join(count_parts)}). {premium_count} are VIP or Family. "
            f"{expiring_count} expiring in the next {EXPIRY_WARNING_DAYS} days.")


# ===== SCREEN: Manage Members page (click a row to edit, Delete beside a row) =====
def build_manage_members_page(page_frame, page_hooks):
    """Build the Manage Members page: every member listed with a Delete
    button beside each row; clicking a row loads that member into the
    form for updating. New members are added with Register (the cards)."""
    fields = {}

    def build_form(form_frame):
        """Add the name, phone and type fields, plus a line for the dates."""
        fields["name"] = common.make_entry(form_frame, width=22)
        common.add_form_row(form_frame, 0, "Name", fields["name"], tip="The person's full name. Letters, spaces, / and ' only (e.g. Ravi a/l Kumar).")
        fields["phone"] = common.make_entry(form_frame, width=22)
        common.add_form_row(form_frame, 1, "Phone", fields["phone"], tip="Malaysian mobile number: 10-11 digits starting with 01, no spaces or dashes.")
        fields["type"] = tk.StringVar(value=common.MEMBERSHIP_TYPES[0])
        common.add_form_row(form_frame, 2, "Type", common.make_option_menu(
            form_frame, fields["type"], list(common.MEMBERSHIP_TYPES), width=18),
            tip="The membership type. Changing it changes their discount; use Renew to extend the dates.")
        fields["dates"] = tk.Label(form_frame, text="", font=common.SMALL_FONT, bg=common.PANEL_BG,
                                   fg=common.MUTED_TEXT_COLOR, justify="left")
        fields["dates"].grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))

    def clear_form():
        """Empty the fields."""
        fields["name"].delete(0, tk.END)
        fields["phone"].delete(0, tk.END)
        fields["type"].set(common.MEMBERSHIP_TYPES[0])
        fields["dates"].config(text="")

    def fill_form(member_id):
        """Load the clicked member (found with the while loop)."""
        member = find_member_by_id(load_all_members(), member_id)
        if member is None:
            return
        fields["name"].insert(0, member.get_name())
        fields["phone"].insert(0, member.get_phone())
        fields["type"].set(member.get_membership_type())
        fields["dates"].config(text=(f"Joined {member.get_join_date()}\n"
                                     f"Expires {member.get_expiry_date()} ({member_status(member)})"))

    def save_action(member_id):
        """Save the edited name, phone and type. A changed type starts a new membership period."""
        old_member = find_member_by_id(load_all_members(), member_id)
        update_member(member_id, fields["name"].get(), fields["phone"].get(), fields["type"].get())
        new_member = find_member_by_id(load_all_members(), member_id)
        message = f"Member {member_id} saved."
        if old_member is not None and new_member is not None and old_member.get_membership_type() != new_member.get_membership_type():
            message = (message + f"\nThe type changed from {old_member.get_membership_type()} to "
                       f"{new_member.get_membership_type()}, so a new membership period starts today. "
                       f"It now expires on {new_member.get_expiry_date()}.")
        return message

    page_hooks["Manage Members"] = common.build_manage_page(
        page_frame, MEMBER_LIST_HEADER, member_rows, "member", build_form, clear_form, fill_form,
        save_action, delete_action, delete_question, add_label=None, search_label="Name",
        summary_text=members_summary, empty_text="No members found.")


# ===== SCREEN: Register page =====
# CHANGE HERE IF: you change how membership card pictures are found: images/card_<type>.png where
# <type> is the type in lower case (Pay-As-You-Go -> card_pay_as_you_go.png). No picture = text card.
def load_card_picture(membership_type):
    """Return the PhotoImage for a membership type, or None if there is no usable picture."""
    name = membership_type.lower().replace(" ", "_").replace("-", "_")
    for file_name in ("card_" + name + ".png", name + ".png"):
        path = os.path.join(common.IMAGES_FOLDER, file_name)
        if not os.path.isfile(path):
            continue
        try:
            picture = tk.PhotoImage(file=path)
            # Tk can only shrink by whole numbers: aim for about 240 pixels wide.
            shrink = -(-picture.width() // CARD_PICTURE_WIDTH)
            if shrink > 1:
                picture = picture.subsample(shrink)
            if picture.width() > CARD_PICTURE_MAX_WIDTH:
                return None
            return picture
        except (tk.TclError, OSError):
            # Not a real PNG (e.g. a renamed JPEG) or unreadable: use the text card instead.
            continue
    return None


# SCREEN: Register page. One card per type is made by a loop over common.MEMBERSHIP_TYPES, so a new
# type appears here by itself once it is added in common.py.
def build_register_page(section_frame, page_hooks):
    """Build the Register page: name/phone, one card per membership
    type, and a Register button."""
    register_state = {"type": None}
    type_buttons = {}

    details_row = tk.Frame(section_frame, bg=common.APP_BG)
    details_row.pack(side="top", fill="x")
    tk.Label(details_row, text="Name", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left")
    name_entry = common.make_entry(details_row, width=28, tip="The person's full name. Letters, spaces, / and ' only (e.g. Ravi a/l Kumar).")
    name_entry.pack(side="left", padx=(6, 20))
    tk.Label(details_row, text="Phone", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left")
    phone_entry = common.make_entry(details_row, width=16,
                                    tip="Malaysian mobile number: 10-11 digits starting with 01, no spaces or dashes. Each phone can only be registered once.")
    phone_entry.pack(side="left", padx=6)

    tk.Label(section_frame, text="Choose a membership type", font=common.HEADING_FONT, bg=common.APP_BG,
             fg=common.ACCENT_COLOR).pack(side="top", anchor="w", pady=(16, 6))
    cards_frame = tk.Frame(section_frame, bg=common.APP_BG)
    cards_frame.pack(side="top", anchor="w")

    bottom_row = tk.Frame(section_frame, bg=common.APP_BG)
    bottom_row.pack(side="top", fill="x", pady=(14, 0))
    summary_label = tk.Label(bottom_row, text="", font=common.LABEL_FONT, bg=common.APP_BG, anchor="w")
    summary_label.pack(side="left")

    # Keeps every PhotoImage alive as long as this page exists (tkinter forgets unreferenced ones).
    card_pictures = {}
    cards_frame.card_pictures = card_pictures   # the frame now owns them, so they live as long as the page
    card_frames = {}   # the coloured frame around each picture card

    def type_card_text(membership_type):
        """Return the text shown on one membership-type card (used when there is no picture)."""
        return f"{membership_type}\n{type_caption(membership_type)}"

    def type_caption(membership_type):
        """Return the one-line caption built from the real fee, duration and discount."""
        fee = common.MEMBERSHIP_FEES[membership_type]
        days = common.MEMBERSHIP_DURATION_DAYS[membership_type]
        discount = common.MEMBER_DISCOUNT_PCT[membership_type]
        if fee == 0:
            fee_text = "No fee"
        else:
            fee_text = f"RM {fee:.2f}"
        if discount == 0:
            discount_text = "no discount"
        else:
            discount_text = f"{discount:g}% off"
        return f"{fee_text} - {duration_text(days)} - {discount_text}"

    def highlight_type():
        """Show which card is chosen and describe it next to Register."""
        for membership_type in type_buttons:
            if membership_type == register_state["type"]:
                type_buttons[membership_type].config(bg=common.BUTTON_COLOR, fg=common.BUTTON_TEXT_COLOR)
                # A picture card is marked by a thick coloured frame around it.
                if membership_type in card_frames:
                    card_frames[membership_type].config(bg=common.BUTTON_COLOR)
            else:
                type_buttons[membership_type].config(bg=common.PANEL_BG, fg=common.ACCENT_COLOR)
                if membership_type in card_frames:
                    card_frames[membership_type].config(bg=common.APP_BG)
        chosen_type = register_state["type"]
        if chosen_type is None:
            summary_label.config(text="Click a card to choose a type.")
            register_button.config(state="disabled")
        else:
            expiry = common.add_days_to_date(common.today_string(), common.MEMBERSHIP_DURATION_DAYS[chosen_type])
            summary_label.config(text=(f"{chosen_type}: RM {common.MEMBERSHIP_FEES[chosen_type]:.2f}, "
                                       f"valid until {expiry}"))
            register_button.config(state="normal")

    def make_type_command(membership_type):
        """Return the command for one membership-type card."""
        def type_command():
            """Choose this membership type."""
            register_state["type"] = membership_type
            highlight_type()
        return type_command

    for type_index in range(len(common.MEMBERSHIP_TYPES)):
        membership_type = common.MEMBERSHIP_TYPES[type_index]
        picture = load_card_picture(membership_type)
        if picture is None:
            type_button = tk.Button(cards_frame, text=type_card_text(membership_type), width=17, height=4,
                                    font=common.BUTTON_FONT, bg=common.PANEL_BG, fg=common.ACCENT_COLOR,
                                    relief="solid", bd=1, cursor="hand2",
                                    command=make_type_command(membership_type))
        else:
            card_pictures[membership_type] = picture
            card_frame = tk.Frame(cards_frame, bg=common.APP_BG, padx=5, pady=5)
            card_frames[membership_type] = card_frame
            type_button = tk.Button(card_frame, image=picture, text=type_caption(membership_type),
                                    compound="top", font=common.SMALL_FONT, bg=common.PANEL_BG,
                                    fg=common.ACCENT_COLOR, relief="flat", bd=0, cursor="hand2",
                                    command=make_type_command(membership_type))
            type_button.pack()
        if membership_type in card_frames:
            card_frames[membership_type].grid(row=type_index // 4, column=type_index % 4, padx=1, pady=1)
        else:
            type_button.grid(row=type_index // 4, column=type_index % 4, padx=3, pady=3)
        common.add_tooltip(type_button, (
            f"Choose {membership_type}: RM {common.MEMBERSHIP_FEES[membership_type]:.2f} fee, lasts "
            f"{duration_text(common.MEMBERSHIP_DURATION_DAYS[membership_type])}, "
            f"{common.MEMBER_DISCOUNT_PCT[membership_type]:g}% off court bookings and classes."))
        type_buttons[membership_type] = type_button

    def reset_form():
        """Empty the form and un-choose the type."""
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        register_state["type"] = None
        highlight_type()

    def on_register():
        """Register the person with the chosen membership type."""
        try:
            new_member = register_member(name_entry.get(), phone_entry.get(),
                                       membership_type=register_state["type"])
        except (ValueError, OSError) as error:
            show_problem(error)
            return
        fee = common.MEMBERSHIP_FEES[new_member.get_membership_type()]
        message = (f"Welcome, {new_member.get_name()}!\n\n"
                   f"Member ID: {new_member.get_member_id()}\n"
                   f"{new_member.get_membership_type()} membership, valid until {new_member.get_expiry_date()}")
        if fee > 0:
            message += f"\n\nMembership fee RM {fee:.2f}: create the bill in Billing > Create Bill."
        messagebox.showinfo("Registered", message)
        reset_form()

    register_button = common.make_button(bottom_row, "Register", on_register,
                                         tip="Create the member with the name, phone and card chosen above. "
                                             "Click a card first.")
    register_button.pack(side="right")

    page_hooks["Register"] = reset_form
