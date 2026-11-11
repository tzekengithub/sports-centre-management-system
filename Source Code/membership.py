"""
Module      : membership.py
Member 2    : Teoh Zynn (student ID: 26PMD03025)
Purpose     : Membership Registration module - lets the public register
              for a membership type (Annual, Monthly, Pay-As-You-Go, VIP,
              Youth, Senior, Family), and view, edit, renew or remove
              members.
Date        : 2026-11-07
"""

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
        self.__join_date = join_date
        self.__expiry_date = expiry_date
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
        self.__expiry_date = expiry_date

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
CARD_PICTURE_WIDTH = 240
CARD_PICTURE_MAX_WIDTH = 260

MEMBERSHIP_DURATION_DAYS = {
    "Annual": 365, "Monthly": 30, "Pay-As-You-Go": 365,
    "VIP": 365, "Youth": 180, "Senior": 365, "Family": 365,
}


MEMBER_FIELD_COUNT = 6


def line_to_member(line):
    """Convert one text-file line into a Member object, or None if the
    line is malformed (wrong number of fields)."""
    fields = common.split_fields(line, MEMBER_FIELD_COUNT)
    if fields is None:
        return None
    try:
        return Member(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5])
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


def register_member(name, phone, membership_type):
    """Validate input, build a new Member, append it to the file, return it.
    Raises ValueError on invalid input or duplicate phone number."""
    member_list = load_all_members()
    if phone.strip() in get_phone_set(member_list):
        raise ValueError("This phone number is already registered.")

    join_date = common.today_string()
    duration_days = MEMBERSHIP_DURATION_DAYS.get(membership_type, 365)
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


def has_future_confirmed_booking(member_id):
    """Return True if member_id has a CONFIRMED booking on or after today."""
    today = common.today_string()
    for line in common.read_lines(common.BOOKINGS_FILE):
        fields = common.split_fields(line, BOOKING_FIELD_COUNT)
        if fields is None:
            continue
        booking_member_id = fields[1]
        booking_date = fields[4]
        booking_status = fields[7]
        if booking_member_id == member_id and booking_status == "CONFIRMED" and booking_date >= today:
            return True
    return False


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
            member.set_membership_type(new_type)
            member_found = True
        updated_lines.append(member.to_line())

    if not member_found:
        raise ValueError(f"No member found with ID {member_id}.")

    common.rewrite_records(common.MEMBERS_FILE, updated_lines, line_to_member)
    return load_all_members()


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
            duration_days = MEMBERSHIP_DURATION_DAYS.get(member.get_membership_type(), 365)
            new_expiry = common.add_days_to_date(common.today_string(), duration_days)
            member.set_expiry_date(new_expiry)
        updated_lines.append(member.to_line())

    if new_expiry is None:
        raise ValueError(f"No member found with ID {member_id}.")

    common.rewrite_records(common.MEMBERS_FILE, updated_lines, line_to_member)
    return new_expiry


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


def members_expiring_within(member_list, days):
    """Return members whose expiry date is within 'days' days from today."""
    today = common.parse_date(common.today_string())
    expiring_list = []
    for member in member_list:
        expiry = common.parse_date(member.get_expiry_date())
        days_left = (expiry - today).days
        if 0 <= days_left <= days:
            expiring_list.append(member)
    return expiring_list


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


def show_problem(error):
    """Show a ValueError's plain message in a standard error box."""
    messagebox.showerror("Please check", str(error))


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


def renew_action(member_id):
    """Renew the picked member and say until when."""
    new_expiry = renew_member(member_id)
    return f"Membership renewed until {new_expiry}."


def delete_action(member_id):
    """Delete the picked member."""
    delete_member(member_id)
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
    expiring_count = len(members_expiring_within(all_members, 30))
    return (f"{count_members(all_members)} members ({', '.join(count_parts)}). "
            f"{expiring_count} expiring in the next 30 days.")


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
        """Save the edited name, phone and type."""
        update_member(member_id, fields["name"].get(), fields["phone"].get(), fields["type"].get())
        return f"Member {member_id} saved."

    page_hooks["Manage Members"] = common.build_manage_page(
        page_frame, MEMBER_LIST_HEADER, member_rows, "member", build_form, clear_form, fill_form,
        save_action, delete_action, delete_question, add_label=None, search_label="Name",
        summary_text=members_summary, empty_text="No members found.")


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
        days = MEMBERSHIP_DURATION_DAYS[membership_type]
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
            expiry = common.add_days_to_date(common.today_string(), MEMBERSHIP_DURATION_DAYS[chosen_type])
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
            f"{duration_text(MEMBERSHIP_DURATION_DAYS[membership_type])}, "
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
            new_member = register_member(name_entry.get(), phone_entry.get(), register_state["type"])
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
