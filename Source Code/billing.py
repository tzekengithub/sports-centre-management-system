"""
Module      : billing.py
Author      : Low Yee Zhe
Purpose     : Billing, Payments & Finance module - create bills, take
              payments with receipts, and daily revenue summaries that
              separate court rentals, coaching, retail sales and
              membership fees.
Date        : 2026-11-07
"""

import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import common


# ---------------------------------------------------------------------------
# CLASSES (encapsulation + inheritance)
# ---------------------------------------------------------------------------
class Bill:
    """A bill with private attributes, getters and setters."""

    def __init__(self, bill_id, member_id, category, ref_id, description,
                 amount, discount, payment_status, date_text):
        """Create the object and validate its starting values."""
        self.__bill_id = bill_id
        self.__member_id = member_id
        self.__category = ""
        self.__ref_id = ref_id
        self.__description = description
        self.__amount = 0.0
        self.__discount = 0.0
        self.__payment_status = ""
        self.__date_text = date_text
        self.set_category(category)
        self.set_amount(amount)
        self.set_discount(discount)
        self.set_payment_status(payment_status)

    def get_bill_id(self):
        """Return the bill ID."""
        return self.__bill_id

    def get_member_id(self):
        """Return the member ID this bill is for."""
        return self.__member_id

    def get_category(self):
        """Return the bill category."""
        return self.__category

    def set_category(self, category):
        """Validate and store the bill category."""
        if category not in common.BILL_CATEGORIES:
            raise ValueError("Bill category is not recognised.")
        self.__category = category

    def get_ref_id(self):
        """Return the reference ID (booking/class/retail item)."""
        return self.__ref_id

    def get_description(self):
        """Return the bill description."""
        return self.__description

    def get_amount(self):
        """Return the bill's original amount."""
        return self.__amount

    def set_amount(self, amount):
        """Validate and store the bill amount."""
        # Written as "not (x >= 0)" so nan, which fails every comparison,
        # is rejected as well as negative numbers.
        if not (amount >= 0):
            raise ValueError("Amount cannot be negative.")
        self.__amount = amount

    def get_discount(self):
        """Return the discount amount applied."""
        return self.__discount

    def set_discount(self, discount):
        """Validate and store the discount amount."""
        if not (discount >= 0):
            raise ValueError("Discount cannot be negative.")
        self.__discount = discount

    def get_total(self):
        """Total = amount - discount."""
        return self.__amount - self.__discount

    def get_payment_status(self):
        """Return the payment status."""
        return self.__payment_status

    def set_payment_status(self, payment_status):
        """Validate and store the payment status."""
        if payment_status not in common.BILL_STATUSES:
            raise ValueError("Payment status must be UNPAID, PAID or VOID.")
        self.__payment_status = payment_status

    def get_date_text(self):
        """Return the bill date."""
        return self.__date_text

    def to_line(self):
        """Turn this bill into a pipe-delimited text-file line."""
        return "|".join([
            self.__bill_id, self.__member_id, self.__category, self.__ref_id,
            self.__description, f"{self.__amount:.2f}", f"{self.__discount:.2f}",
            f"{self.get_total():.2f}", self.__payment_status, self.__date_text,
        ])


class RetailBill(Bill):
    """A retail-item bill. Inherits from Bill (demonstrates inheritance)
    and adds an item name kept inside the description."""

    def __init__(self, bill_id, member_id, item_name, amount, discount, payment_status, date_text):
        """Create the object and validate its starting values."""
        description = f"Retail item: {item_name}"
        super().__init__(bill_id, member_id, "RETAIL", "MANUAL", description,
                          amount, discount, payment_status, date_text)
        self.__item_name = item_name

    def get_item_name(self):
        """Return the retail item name."""
        return self.__item_name


# ---------------------------------------------------------------------------
# LOGIC LAYER
# ---------------------------------------------------------------------------
BILL_FIELD_COUNT = 10
MEMBER_FIELD_COUNT = 6
BOOKING_FIELD_COUNT = 8
CLASS_FIELD_COUNT = 10
MAX_RETAIL_AMOUNT = 10000.0
MAX_TENDERED_AMOUNT = 100000.0


def line_to_bill(line):
    """Convert one text-file line into a Bill object, or None if the
    line is malformed."""
    fields = common.split_fields(line, BILL_FIELD_COUNT)
    if fields is None:
        return None
    try:
        return Bill(fields[0], fields[1], fields[2], fields[3], fields[4],
                    float(fields[5]), float(fields[6]), fields[8], fields[9])
    except ValueError:
        return None


def load_all_bills():
    """Read bills.txt and return a list of Bill objects. Malformed lines
    are skipped rather than crashing the program."""
    bill_list = []
    for line in common.read_lines(common.BILLS_FILE):
        bill = line_to_bill(line)
        if bill is not None:
            bill_list.append(bill)
    return bill_list


def get_member_type(member_id):
    """Return the membership type for member_id, or None if not found."""
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is None:
            continue
        if fields[0] == member_id:
            return fields[3]
    return None


def get_booking_description(booking_id):
    """Return (amount, description) for a booking, using SPORTS rate."""
    for line in common.read_lines(common.BOOKINGS_FILE):
        fields = common.split_fields(line, BOOKING_FIELD_COUNT)
        if fields is None:
            continue
        if fields[0] == booking_id:
            sport, court_no = fields[2], fields[3]
            try:
                duration_hrs = int(fields[6])
            except ValueError:
                continue
            if sport not in common.SPORTS:
                continue
            rate = common.SPORTS[sport]["rate"]
            amount = round(rate * duration_hrs, 2)
            description = f"{sport} Court {court_no}, {duration_hrs}h"
            return amount, description
    raise ValueError(f"No booking found with ID {booking_id}.")


def get_class_description(class_id):
    """Return (amount, description) for a class, using fee_per_pax."""
    for line in common.read_lines(common.CLASSES_FILE):
        fields = common.split_fields(line, CLASS_FIELD_COUNT)
        if fields is None:
            continue
        if fields[0] == class_id:
            sport, class_type = fields[2], fields[3]
            try:
                fee_per_pax = round(float(fields[8]), 2)
            except ValueError:
                continue
            description = f"{sport} {class_type} Lesson"
            return fee_per_pax, description
    raise ValueError(f"No class found with ID {class_id}.")


def generate_bill(member_id, category, ref_id, retail_item_name=None, retail_amount=0.0):
    """Create a new UNPAID bill from a booking, class, membership fee or
    manual retail item, applying the member's discount percentage."""
    member_type = get_member_type(member_id)
    if member_type is None:
        raise ValueError(f"No member found with ID {member_id}.")
    discount_pct = common.MEMBER_DISCOUNT_PCT.get(member_type, 0.0)

    # A booking or class must not be billed twice for the same member.
    if category in ("COURT", "COACHING") and (category, ref_id) in billed_references(member_id):
        raise ValueError(f"{ref_id} has already been billed to {member_id}.")

    match category:
        case "COURT":
            amount, description = get_booking_description(ref_id)
        case "COACHING":
            amount, description = get_class_description(ref_id)
        case "MEMBERSHIP":
            amount = common.MEMBERSHIP_FEES.get(member_type, 0.0)
            description = f"{member_type} Membership Fee"
        case "RETAIL":
            if retail_item_name is None or retail_item_name.strip() == "":
                raise ValueError("Enter a retail item name.")
            if common.contains_forbidden_character(retail_item_name):
                raise ValueError("Retail item name cannot contain '|' or ';'.")
            # Round first: that is the value that gets saved.
            retail_amount = round(retail_amount, 2)
            if not (0.01 <= retail_amount <= MAX_RETAIL_AMOUNT):
                raise ValueError(f"Retail amount must be between RM 0.01 and RM {MAX_RETAIL_AMOUNT:g}.")
            amount = retail_amount
            description = f"Retail item: {retail_item_name}"
        case _:
            raise ValueError("Unknown bill category.")

    discount = round(amount * discount_pct / 100.0, 2)
    new_id = common.generate_id(common.BILLS_FILE, "BIL")
    bill_date = common.today_string()

    if category == "RETAIL":
        new_bill = RetailBill(new_id, member_id, retail_item_name, amount, discount, "UNPAID", bill_date)
    else:
        new_bill = Bill(new_id, member_id, category, ref_id, description, amount, discount, "UNPAID", bill_date)

    common.append_line(common.BILLS_FILE, new_bill.to_line())
    return new_bill


def billed_references(member_id):
    """Return a set of (category, ref_id) pairs already billed to
    member_id on bills that are not VOID, used to stop double billing."""
    reference_set = set()
    for bill in load_all_bills():
        if bill.get_member_id() == member_id and bill.get_payment_status() != "VOID":
            reference_set.add((bill.get_category(), bill.get_ref_id()))
    return reference_set


def load_member_choices():
    """Return a list of (member_id, name, membership_type) tuples from
    members.txt, for the member drop-down."""
    member_rows = []
    for line in common.read_lines(common.MEMBERS_FILE):
        fields = common.split_fields(line, MEMBER_FIELD_COUNT)
        if fields is not None:
            member_rows.append((fields[0], fields[1], fields[3]))
    return member_rows


def unbilled_bookings(member_id):
    """Return a list of (booking_id, label) for member_id's CONFIRMED
    bookings that have not been billed yet."""
    already_billed = billed_references(member_id)
    booking_rows = []
    for line in common.read_lines(common.BOOKINGS_FILE):
        fields = common.split_fields(line, BOOKING_FIELD_COUNT)
        if fields is None or fields[1] != member_id or fields[7] != "CONFIRMED":
            continue
        if ("COURT", fields[0]) in already_billed:
            continue
        label = f"{fields[0]} {fields[2]} Ct{fields[3]} {fields[4]} {fields[5]:0>2}:00"
        booking_rows.append((fields[0], label))
    return booking_rows


def unbilled_classes(member_id):
    """Return a list of (class_id, label) for classes member_id is
    enrolled in that have not been billed to them yet."""
    already_billed = billed_references(member_id)
    class_rows = []
    for line in common.read_lines(common.CLASSES_FILE):
        fields = common.split_fields(line, CLASS_FIELD_COUNT)
        if fields is None or member_id not in fields[9].split(";"):
            continue
        if ("COACHING", fields[0]) in already_billed:
            continue
        label = f"{fields[0]} {fields[2]} {fields[3]} {fields[4]}"
        class_rows.append((fields[0], label))
    return class_rows


def find_bill_by_id(bill_list, bill_id):
    """Linear search for a bill by ID using a while loop. Returns the
    Bill or None."""
    index = 0
    while index < len(bill_list):
        if bill_list[index].get_bill_id() == bill_id:
            return bill_list[index]
        index += 1
    return None


def pay_bill(bill_id, payment_method, amount_tendered):
    """Mark a bill PAID after validating the payment method and amount.
    Returns (bill, change). Raises ValueError on invalid input."""
    if payment_method not in common.VALID_PAYMENT_METHODS:
        raise ValueError("Payment method must be Cash, Card or E-Wallet.")

    bill_list = load_all_bills()
    target_bill = None
    for bill in bill_list:
        if bill.get_bill_id() == bill_id:
            target_bill = bill
            break
    if target_bill is None:
        raise ValueError(f"No bill found with ID {bill_id}.")
    if target_bill.get_payment_status() == "PAID":
        raise ValueError("This bill has already been paid.")
    if target_bill.get_payment_status() == "VOID":
        raise ValueError("This bill has been voided and cannot be paid.")
    if not common.is_finite_number(amount_tendered):
        raise ValueError("Please enter a valid amount received.")
    if amount_tendered < target_bill.get_total():
        raise ValueError(f"Amount tendered is less than the total due (RM {target_bill.get_total():.2f}).")

    change = round(amount_tendered - target_bill.get_total(), 2)
    target_bill.set_payment_status("PAID")

    updated_lines = []
    for bill in bill_list:
        updated_lines.append(bill.to_line())
    common.rewrite_records(common.BILLS_FILE, updated_lines, line_to_bill)

    write_receipt(target_bill, payment_method, amount_tendered, change)
    return target_bill, change


def write_receipt(bill, payment_method, amount_tendered, change):
    """Write a receipt text file to data/receipts/<bill_id>.txt."""
    receipt_path = os.path.join(common.RECEIPT_FOLDER, bill.get_bill_id() + ".txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    receipt_lines = [
        "SPORTS CENTRE - PAYMENT RECEIPT",
        "--------------------------------",
        f"Bill ID       : {bill.get_bill_id()}",
        f"Member ID     : {bill.get_member_id()}",
        f"Description   : {bill.get_description()}",
        f"Amount        : RM {bill.get_amount():.2f}",
        f"Discount      : RM {bill.get_discount():.2f}",
        f"Total Paid    : RM {bill.get_total():.2f}",
        f"Payment Method: {payment_method}",
        f"Tendered      : RM {amount_tendered:.2f}",
        f"Change        : RM {change:.2f}",
        f"Printed At    : {timestamp}",
    ]
    common.write_lines(receipt_path, receipt_lines)


def read_receipt(bill_id):
    """Read back a receipt file as a single string, or None if missing."""
    receipt_path = os.path.join(common.RECEIPT_FOLDER, bill_id + ".txt")
    if not os.path.isfile(receipt_path):
        return None
    return "\n".join(common.read_lines(receipt_path))


def search_bills(bill_list, search_field, search_text):
    """Search bills by 'id', 'member', 'status', 'date' or 'category'."""
    results = []
    search_text_lower = search_text.strip().lower()
    for bill in bill_list:
        match search_field:
            case "id":
                if bill.get_bill_id().lower() == search_text_lower:
                    results.append(bill)
            case "member":
                if bill.get_member_id().lower() == search_text_lower:
                    results.append(bill)
            case "status":
                if bill.get_payment_status().lower() == search_text_lower:
                    results.append(bill)
            case "date":
                if bill.get_date_text() == search_text.strip():
                    results.append(bill)
            case "category":
                if bill.get_category().lower() == search_text_lower:
                    results.append(bill)
    return results


def void_bill(bill_id):
    """Set a bill's status to VOID (keeps the record). Blocked if the
    bill is PAID or already VOID, so clicking Void twice gives a clear
    message instead of silently doing nothing."""
    bill_list = load_all_bills()
    bill_found = False
    for bill in bill_list:
        if bill.get_bill_id() == bill_id:
            bill_found = True
            if bill.get_payment_status() == "PAID":
                raise ValueError("A PAID bill cannot be voided.")
            if bill.get_payment_status() == "VOID":
                raise ValueError("This bill is already voided.")
            bill.set_payment_status("VOID")
    if not bill_found:
        raise ValueError(f"No bill found with ID {bill_id}.")

    updated_lines = []
    for bill in bill_list:
        updated_lines.append(bill.to_line())
    common.rewrite_records(common.BILLS_FILE, updated_lines, line_to_bill)


def delete_void_bill(bill_id):
    """Permanently delete a bill, only if its status is VOID."""
    bill_list = load_all_bills()
    remaining_lines = []
    bill_found = False
    for bill in bill_list:
        if bill.get_bill_id() == bill_id:
            bill_found = True
            if bill.get_payment_status() != "VOID":
                raise ValueError("Only VOID bills can be deleted.")
        else:
            remaining_lines.append(bill.to_line())
    if not bill_found:
        raise ValueError(f"No bill found with ID {bill_id}.")
    common.rewrite_records(common.BILLS_FILE, remaining_lines, line_to_bill)


def daily_revenue_summary(date_text):
    """Return (category_totals_dict, grand_total, bill_count, paid_count,
    unpaid_count) for bills dated date_text. The totals count only PAID
    bills, so "revenue" means money actually collected that day, not
    money billed - an UNPAID bill is not revenue yet, and a VOID bill
    was cancelled and is never revenue. bill_count still counts every
    bill issued that day (any status) for context."""
    category_totals = {}
    for category in common.BILL_CATEGORIES:
        category_totals[category] = 0.0
    grand_total = 0.0
    bill_count = 0
    paid_count = 0
    unpaid_count = 0

    for bill in load_all_bills():
        if bill.get_date_text() != date_text:
            continue
        bill_count += 1
        if bill.get_payment_status() == "PAID":
            paid_count += 1
            category_totals[bill.get_category()] += bill.get_total()
            grand_total += bill.get_total()
        elif bill.get_payment_status() == "UNPAID":
            unpaid_count += 1

    return category_totals, grand_total, bill_count, paid_count, unpaid_count


def total_bills(bill_list):
    """Add up bill totals: recursively (rubric) for normal sizes, with a
    plain loop above common.RECURSION_SAFE_LIMIT, where recursion would
    crash."""
    if len(bill_list) <= common.RECURSION_SAFE_LIMIT:
        return total_bills_recursive(bill_list)
    running_total = 0.0
    for bill in bill_list:
        running_total += bill.get_total()
    return running_total


def total_bills_recursive(bill_list, index=0):
    """Recursively sum the totals of bill_list starting at index.
    Demonstrates recursion over a list of objects."""
    if index >= len(bill_list):
        return 0.0
    return bill_list[index].get_total() + total_bills_recursive(bill_list, index + 1)


# ---------------------------------------------------------------------------
# GUI LAYER
#
# The tab opens on a menu asking "What would you like to do?". Each
# action has its own one-page screen with a Back button: Create Bill,
# Pay Bill, Void Bill, Delete Bill, View Receipt, Daily Revenue.
# ---------------------------------------------------------------------------
BILLING_ACTIONS = [
    ("Create Bill", "Bill a member",
     "Pick the member and what the bill is for. Check the total (member discount included), "
     "then click Create Bill."),
    ("Pay Bill", "Take a payment",
     "Click the unpaid bill, choose how they pay (for cash, type the amount received), then click Pay."),
    ("Void Bill", "Cancel an unpaid bill",
     "Click the unpaid bill that was a mistake, then click Void Bill. It stays on record as VOID."),
    ("Delete Bill", "Remove a void bill",
     "Only void bills are listed. Click one, then click Delete Bill."),
    ("View Receipt", "Show a paid bill's receipt",
     "Click a paid bill, then click View Receipt."),
    ("Daily Revenue", "Money collected on a day",
     "Pick a date. Court rentals, coaching, retail sales and membership fees are shown separately. "
     "Only paid bills count."),
]

CATEGORY_CHOICES = (("COURT", "Court Rental"), ("COACHING", "Coaching Class"),
                    ("MEMBERSHIP", "Membership Fee"), ("RETAIL", "Retail Sale"))
REVENUE_BAR_WIDTH = 260
CATEGORY_TIPS = {
    "COURT": "Bill one of the member's court bookings (sport rate x hours).",
    "COACHING": "Bill a coaching class the member is enrolled in (the class fee per person).",
    "MEMBERSHIP": "Bill the yearly or monthly fee for the member's membership type.",
    "RETAIL": "Bill something sold at the counter: type the item and its price.",
}
METHOD_TIPS = {
    "Cash": "Paid in cash. Type how much they handed over; the change is worked out.",
    "Card": "Paid by card. Always the exact total.",
    "E-Wallet": "Paid by e-wallet. Always the exact total.",
}
BILL_LIST_HEADER = f"{'Bill ID':<9}{'Date':<11}{'Member ID':<10}{'For':<16}{'Total RM':>9}"


def show_problem(error):
    """Show a ValueError's plain message in a standard error box."""
    messagebox.showerror("Please check", str(error))


def build_billing_tab(parent):
    """Build the Billing, Payments & Finance tab inside parent (the main
    window's tab area) and return its frame. The tab opens on a menu
    asking what to do; each action has its own simple page."""
    window = tk.Frame(parent, bg=common.APP_BG)
    page_frames, page_hooks = common.build_action_menu(window, "Billing, Payments & Finance", BILLING_ACTIONS)
    build_create_bill_page(page_frames["Create Bill"], page_hooks)
    page_hooks["Pay Bill"] = build_pay_page(page_frames["Pay Bill"])
    page_hooks["Void Bill"] = build_status_page(page_frames["Void Bill"], "UNPAID")
    page_hooks["Delete Bill"] = build_status_page(page_frames["Delete Bill"], "VOID")
    page_hooks["View Receipt"] = build_status_page(page_frames["View Receipt"], "PAID")
    build_revenue_page(page_frames["Daily Revenue"], page_hooks)
    return window


def bill_rows_with_status(status, search_text):
    """Return (bill_id, row_text) for bills with this status, newest
    first, filtered by member ID if search_text is given."""
    bill_list = search_bills(load_all_bills(), "status", status)
    if search_text != "":
        bill_list = search_bills(bill_list, "member", search_text)
    rows = []
    index = len(bill_list) - 1
    while index >= 0:
        bill = bill_list[index]
        category_name = common.BILL_CATEGORY_NAMES.get(bill.get_category(), bill.get_category())
        rows.append((bill.get_bill_id(), (f"{bill.get_bill_id():<9}{bill.get_date_text():<11}"
                                          f"{bill.get_member_id():<10}{category_name:<16}{bill.get_total():>9.2f}")))
        index -= 1
    return rows


def describe_bill(bill_id):
    """Return the details text for one bill (found with the while loop)."""
    bill = find_bill_by_id(load_all_bills(), bill_id)
    if bill is None:
        return "This bill no longer exists."
    category_name = common.BILL_CATEGORY_NAMES.get(bill.get_category(), bill.get_category())
    return common.details_text([
        ("Bill ID", bill.get_bill_id()),
        ("Status", bill.get_payment_status()),
        ("Member ID", bill.get_member_id()),
        ("For", category_name),
        ("Item", bill.get_description()),
        ("Date", bill.get_date_text()),
        ("", ""),
        ("Amount", f"RM {bill.get_amount():>8.2f}"),
        ("Discount", f"RM {bill.get_discount():>8.2f}"),
        ("Total", f"RM {bill.get_total():>8.2f}"),
    ])


def build_status_page(page_frame, status):
    """Build the Void Bill (UNPAID), Delete Bill (VOID) or View Receipt
    (PAID) page and return its refresh function."""

    def load_rows(search_text):
        """List the bills this page can act on."""
        return bill_rows_with_status(status, search_text)

    def void_action(bill_id):
        """Void the picked bill."""
        void_bill(bill_id)
        return f"Bill {bill_id} voided."

    def delete_action(bill_id):
        """Delete the picked void bill."""
        delete_void_bill(bill_id)
        return f"Bill {bill_id} deleted."

    def receipt_action(bill_id):
        """Return the saved receipt text to show."""
        receipt_text = read_receipt(bill_id)
        if receipt_text is None:
            return "No receipt file was found for this bill."
        return receipt_text

    def void_question(bill_id):
        """Confirmation question for voiding."""
        return f"Void bill {bill_id}?"

    def delete_question(bill_id):
        """Confirmation question for deleting."""
        return f"Delete bill {bill_id} permanently?"

    match status:
        case "UNPAID":
            return common.build_pick_page(page_frame, BILL_LIST_HEADER, load_rows, "Void Bill", void_action,
                                          describe=describe_bill, confirm_text=void_question, danger=True,
                                          search_label="Member ID", empty_text="No unpaid bills.")
        case "VOID":
            return common.build_pick_page(page_frame, BILL_LIST_HEADER, load_rows, "Delete Bill", delete_action,
                                          describe=describe_bill, confirm_text=delete_question, danger=True,
                                          search_label="Member ID", empty_text="No void bills.")
        case _:
            return common.build_pick_page(page_frame, BILL_LIST_HEADER, load_rows, "View Receipt",
                                          receipt_action, describe=describe_bill, search_label="Member ID",
                                          empty_text="No paid bills.", result_title="Receipt")


def build_pay_page(page_frame):
    """Build the Pay Bill page and return its refresh function."""
    form_widgets = {}
    pay_state = {"bill_id": None}

    def lock_amount_unless_cash():
        """Card and e-wallet are always the exact amount; only cash can be
        more (giving change), so the box is only editable for cash."""
        amount_entry = form_widgets["amount"]
        amount_entry.config(state="normal")
        bill = find_bill_by_id(load_all_bills(), pay_state["bill_id"])
        if bill is not None:
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, f"{bill.get_total():.2f}")
        if form_widgets["method"].get() != "Cash":
            amount_entry.config(state="disabled")

    def build_form(form_frame):
        """Add the payment method choice and the amount received box."""
        form_widgets["method"] = tk.StringVar(value="Cash")
        method_row = tk.Frame(form_frame, bg=common.PANEL_BG)
        for method_name in ("Cash", "Card", "E-Wallet"):
            method_button = tk.Radiobutton(method_row, text=method_name, value=method_name,
                                           variable=form_widgets["method"], command=lock_amount_unless_cash,
                                           font=common.LABEL_FONT, bg=common.PANEL_BG,
                                           activebackground=common.PANEL_BG)
            method_button.pack(side="left")
            common.add_tooltip(method_button, METHOD_TIPS[method_name])
        common.add_form_row(form_frame, 0, "Paid by", method_row, tip="How the member is paying.")
        form_widgets["amount"] = common.make_entry(form_frame, width=10)
        common.add_form_row(form_frame, 1, "Amount received (RM)", form_widgets["amount"],
                            tip="Ringgit handed over. Must be at least the total; any extra is given back "
                                "as change.")

    def fill_form(bill_id):
        """Start with cash and the exact total."""
        pay_state["bill_id"] = bill_id
        form_widgets["method"].set("Cash")
        lock_amount_unless_cash()

    def pay_action(bill_id):
        """Take payment and report the change."""
        amount_received = common.parse_decimal(form_widgets["amount"].get(), "Amount received", 0,
                                               MAX_TENDERED_AMOUNT)
        paid_bill, change = pay_bill(bill_id, form_widgets["method"].get(), amount_received)
        message = f"Bill {paid_bill.get_bill_id()} paid by {form_widgets['method'].get()}. Receipt saved."
        if change > 0:
            message += f"\n\nChange to give back: RM {change:.2f}"
        return message

    def load_rows(search_text):
        """Unpaid bills only."""
        return bill_rows_with_status("UNPAID", search_text)

    def unpaid_summary():
        """Total still owed, added up recursively."""
        unpaid_bills = search_bills(load_all_bills(), "status", "UNPAID")
        return f"{len(unpaid_bills)} unpaid bill(s), RM {total_bills(unpaid_bills):.2f} still owed."

    return common.build_pick_page(page_frame, BILL_LIST_HEADER, load_rows, "Pay", pay_action,
                                  describe=describe_bill, build_form=build_form, fill_form=fill_form,
                                  search_label="Member ID", summary_text=unpaid_summary,
                                  empty_text="No unpaid bills.", result_title="Paid")


def build_create_bill_page(section_frame, page_hooks):
    """Build the Create Bill page: member, category, the item being
    billed, a live price preview and a Create Bill button."""
    member_choice_ids = {}
    member_types = {}
    reference_choice_ids = {}

    card = common.make_card(section_frame)
    card.pack(side="top", anchor="w")

    member_variable = tk.StringVar(value="")
    category_variable = tk.StringVar(value="COURT")
    reference_variable = tk.StringVar(value="")

    def on_member_changed_later(chosen_text):
        """Pass a member pick on to on_member_changed (defined further down)."""
        on_member_changed(chosen_text)

    member_menu, member_dropdown, set_member_choices = common.make_filtered_menu(
        card, member_variable, width=30, command=on_member_changed_later)
    common.add_form_row(card, 0, "Member", member_menu,
                        tip="Who the bill is for. Their membership type sets the discount.")

    category_row = tk.Frame(card, bg=common.PANEL_BG)
    common.add_form_row(card, 1, "Bill for", category_row, tip="Choose what the member is paying for.")

    # Row 2 changes with the category: a drop-down of bookings/classes,
    # a plain note for a membership fee, or item + price for retail.
    detail_label = tk.Label(card, text="", font=common.LABEL_FONT, bg=common.PANEL_BG, anchor="w")
    detail_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
    reference_menu = common.make_option_menu(card, reference_variable, [], width=30,
                                             tip="Pick the booking or class to bill. Only ones not billed yet "
                                                 "are listed.")
    retail_row = tk.Frame(card, bg=common.PANEL_BG)
    item_entry = common.make_entry(retail_row, width=18, tip="What was sold, e.g. Water Bottle.")
    item_entry.pack(side="left")
    tk.Label(retail_row, text="  Price RM", font=common.LABEL_FONT, bg=common.PANEL_BG).pack(side="left")
    price_entry = common.make_entry(retail_row, width=8,
                                    tip="The price in Ringgit before the member discount, e.g. 5.50.")
    price_entry.pack(side="left", padx=(4, 0))
    note_label = tk.Label(card, text="", font=common.LABEL_FONT, bg=common.PANEL_BG, anchor="w")

    preview_label = tk.Label(card, text="", font=common.HEADING_FONT, bg=common.PANEL_BG,
                             fg=common.ACCENT_COLOR, anchor="w", justify="left")
    preview_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 10))

    def chosen_member_id():
        """Return the member ID picked in the drop-down, or None."""
        return member_choice_ids.get(member_variable.get())

    def show_detail_row():
        """Show the input that matches the chosen category."""
        reference_menu.grid_remove()
        retail_row.grid_remove()
        note_label.grid_remove()
        member_id = chosen_member_id()
        category = category_variable.get()
        reference_rows = []
        if category == "COURT":
            detail_label.config(text="Booking")
            if member_id is not None:
                reference_rows = unbilled_bookings(member_id)
        elif category == "COACHING":
            detail_label.config(text="Class")
            if member_id is not None:
                reference_rows = unbilled_classes(member_id)
        elif category == "MEMBERSHIP":
            detail_label.config(text="")
            member_type = member_types.get(member_id, "")
            note_label.config(text=f"{member_type} membership fee")
            note_label.grid(row=2, column=1, sticky="w", pady=4)
        else:
            detail_label.config(text="Item")
            retail_row.grid(row=2, column=1, sticky="w", pady=4)

        if category in ("COURT", "COACHING"):
            reference_choice_ids.clear()
            reference_choices = []
            for reference_id, label in reference_rows:
                reference_choice_ids[label] = reference_id
                reference_choices.append(label)
            if len(reference_choices) == 0:
                note_label.config(text="Nothing left to bill for this member.")
                note_label.grid(row=2, column=1, sticky="w", pady=4)
                reference_variable.set("")
            else:
                common.set_option_menu_choices(reference_menu, reference_variable, reference_choices,
                                               command=on_reference_changed)
                reference_menu.grid(row=2, column=1, sticky="w", pady=4)
        update_preview()

    def work_out_amount():
        """Return the bill amount before discount for the current form,
        or raise ValueError if something is still missing."""
        member_id = chosen_member_id()
        if member_id is None:
            raise ValueError("Pick a member.")
        category = category_variable.get()
        match category:
            case "COURT":
                if reference_variable.get() not in reference_choice_ids:
                    raise ValueError("Pick a booking.")
                amount, description = get_booking_description(reference_choice_ids[reference_variable.get()])
            case "COACHING":
                if reference_variable.get() not in reference_choice_ids:
                    raise ValueError("Pick a class.")
                amount, description = get_class_description(reference_choice_ids[reference_variable.get()])
            case "MEMBERSHIP":
                amount = common.MEMBERSHIP_FEES.get(member_types[member_id], 0.0)
            case _:
                amount = common.parse_decimal(price_entry.get(), "Price", 0.01, MAX_RETAIL_AMOUNT)
        return amount

    def update_preview():
        """Show amount, member discount and total due for the current form."""
        try:
            amount = work_out_amount()
        except ValueError as error:
            # When there is nothing to bill, the note above already says
            # so; repeating "Pick a booking." underneath would be noise.
            if category_variable.get() in ("COURT", "COACHING") and len(reference_choice_ids) == 0:
                preview_label.config(text="")
            else:
                preview_label.config(text=str(error), fg=common.MUTED_TEXT_COLOR)
            create_button.config(state="disabled")
            return
        member_type = member_types[chosen_member_id()]
        discount_pct = common.MEMBER_DISCOUNT_PCT.get(member_type, 0.0)
        discount = round(amount * discount_pct / 100.0, 2)
        preview_label.config(text=(f"Amount RM {amount:.2f}  -  {member_type} discount {discount_pct:g}% "
                                   f"(RM {discount:.2f})\nTotal due: RM {amount - discount:.2f}"),
                             fg=common.ACCENT_COLOR)
        create_button.config(state="normal")

    def on_member_changed(chosen_text):
        """Refresh the item list and preview for the newly picked member."""
        show_detail_row()

    def on_reference_changed(chosen_text):
        """Refresh the preview when a different booking/class is picked."""
        update_preview()

    def on_price_typed(event):
        """Refresh the preview as the retail price is typed."""
        update_preview()

    price_entry.bind("<KeyRelease>", on_price_typed)

    for category_code, category_label in CATEGORY_CHOICES:
        category_button = tk.Radiobutton(category_row, text=category_label, value=category_code,
                                         variable=category_variable, command=show_detail_row,
                                         font=common.LABEL_FONT, bg=common.PANEL_BG,
                                         activebackground=common.PANEL_BG)
        category_button.pack(side="left", padx=(0, 6))
        common.add_tooltip(category_button, CATEGORY_TIPS[category_code])

    def on_create():
        """Create the bill shown in the preview."""
        member_id = chosen_member_id()
        category = category_variable.get()
        reference_id = reference_choice_ids.get(reference_variable.get(), "")
        try:
            if category == "RETAIL":
                retail_amount = common.parse_decimal(price_entry.get(), "Price", 0.01, MAX_RETAIL_AMOUNT)
                new_bill = generate_bill(member_id, category, "MANUAL", item_entry.get(), retail_amount)
            elif category == "MEMBERSHIP":
                new_bill = generate_bill(member_id, category, "FEE")
            else:
                new_bill = generate_bill(member_id, category, reference_id)
        except (ValueError, OSError) as error:
            show_problem(error)
            return
        messagebox.showinfo("Bill created", (f"Bill {new_bill.get_bill_id()} created: RM {new_bill.get_total():.2f} "
                                             f"(unpaid).\nTake payment with Pay Bill."))
        item_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        show_detail_row()

    create_button = common.make_button(card, "Create Bill", on_create,
                                       tip="Create the bill shown in the preview. It starts UNPAID; take "
                                           "payment with Pay Bill.")
    create_button.grid(row=4, column=0, columnspan=2, sticky="w")

    def on_show():
        """Reload the member list whenever this page opens."""
        member_choice_ids.clear()
        member_types.clear()
        member_choices = []
        for member_id, name, member_type in load_member_choices():
            choice_text = f"{member_id} {name} ({member_type})"
            member_choice_ids[choice_text] = member_id
            member_types[member_id] = member_type
            member_choices.append(choice_text)
        set_member_choices(member_choices)
        show_detail_row()

    page_hooks["Create Bill"] = on_show


def build_revenue_page(section_frame, page_hooks):
    """Build the Daily Revenue page: a date picker and one row per
    bill category with its total and a bar, plus the day's grand total."""
    date_row = tk.Frame(section_frame, bg=common.APP_BG)
    date_row.pack(side="top", fill="x")
    tk.Label(date_row, text="Date", font=common.LABEL_FONT, bg=common.APP_BG).pack(side="left")
    date_entry = common.make_entry(date_row, width=12,
                                   tip="The day to add up, as YYYY-MM-DD. The table updates as soon as "
                                       "the date is complete.")
    date_entry.pack(side="left", padx=(6, 4))
    date_entry.insert(0, common.today_string())

    card = common.make_card(section_frame)
    card.pack(side="top", anchor="w", pady=(12, 0))
    count_label = tk.Label(section_frame, text="", font=common.LABEL_FONT, bg=common.APP_BG,
                           fg=common.MUTED_TEXT_COLOR, anchor="w")
    count_label.pack(side="top", fill="x", pady=(8, 0))

    def refresh_revenue():
        """Recalculate and redraw the revenue table for the typed date."""
        for child_widget in card.winfo_children():
            child_widget.destroy()
        date_text = date_entry.get().strip()
        if not common.is_valid_date(date_text):
            tk.Label(card, text="Type a date as YYYY-MM-DD, or click the calendar.", font=common.LABEL_FONT,
                     bg=common.PANEL_BG).grid(row=0, column=0)
            count_label.config(text="")
            return
        # Bills are saved as YYYY-MM-DD, so 2027-1-5 must be tidied to match.
        date_text = common.normalize_date(date_text)
        category_totals, grand_total, bill_count, paid_count, unpaid_count = daily_revenue_summary(date_text)

        tk.Label(card, text=f"Revenue on {date_text}", font=common.HEADING_FONT, bg=common.PANEL_BG,
                 fg=common.ACCENT_COLOR).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        largest_total = 0.0
        for category in category_totals:
            if category_totals[category] > largest_total:
                largest_total = category_totals[category]

        row_index = 1
        for category in ("COURT", "COACHING", "RETAIL", "MEMBERSHIP"):
            category_total = category_totals[category]
            tk.Label(card, text=common.BILL_CATEGORY_NAMES[category], font=common.LABEL_FONT,
                     bg=common.PANEL_BG, anchor="w", width=16).grid(row=row_index, column=0, sticky="w", pady=3)
            tk.Label(card, text=f"RM {category_total:>9.2f}", font=common.MONO_FONT,
                     bg=common.PANEL_BG).grid(row=row_index, column=1, sticky="e", padx=(0, 12))
            # Bar length is proportional to the biggest category that day.
            bar_holder = tk.Frame(card, bg=common.APP_BG, width=REVENUE_BAR_WIDTH, height=14)
            bar_holder.grid(row=row_index, column=2, sticky="w")
            bar_holder.pack_propagate(False)
            if largest_total > 0 and category_total > 0:
                bar_width = int(REVENUE_BAR_WIDTH * category_total / largest_total)
                tk.Frame(bar_holder, bg=common.ACCENT_COLOR, width=bar_width, height=14).pack(side="left")
            row_index += 1

        tk.Frame(card, bg=common.BORDER_COLOR, height=1).grid(row=row_index, column=0, columnspan=3,
                                                              sticky="we", pady=6)
        tk.Label(card, text="Total collected", font=common.BUTTON_FONT, bg=common.PANEL_BG,
                 anchor="w").grid(row=row_index + 1, column=0, sticky="w")
        tk.Label(card, text=f"RM {grand_total:>9.2f}", font=("Consolas", 11, "bold"), bg=common.PANEL_BG,
                 fg=common.ACCENT_COLOR).grid(row=row_index + 1, column=1, sticky="e", padx=(0, 12))
        void_count = bill_count - paid_count - unpaid_count
        count_label.config(text=(f"{bill_count} bill(s) dated {date_text}: {paid_count} paid, "
                                 f"{unpaid_count} unpaid, {void_count} void. Only paid bills count as revenue."))

    def on_pick_date():
        """Open the calendar pop-up; refresh once a day is picked."""
        common.open_date_picker(section_frame, date_entry, on_picked=refresh_revenue)

    def on_date_typed(event):
        """Refresh as soon as a complete, real date is typed (or on Enter)."""
        if event.keysym == "Return" or common.is_valid_date(date_entry.get().strip()):
            refresh_revenue()

    date_entry.bind("<KeyRelease>", on_date_typed)
    common.make_button(date_row, "\U0001F4C5", on_pick_date, style="light",
                       tip="Open a calendar and click a day to see its revenue.").pack(side="left")
    common.make_button(date_row, "Show", refresh_revenue,
                       tip="Recalculate the revenue for the date in the box.").pack(side="left", padx=6)

    page_hooks["Daily Revenue"] = refresh_revenue
