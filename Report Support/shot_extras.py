"""Contact sheet and INDEX.md for take_screenshots_real.py. The contact sheet
is only thumbnails of the REAL screenshots, for scanning; it is not for the
report. Nothing here draws a screenshot."""

import os

from PIL import Image, ImageDraw

CAPTIONS = {
    "Figure_01": "Home page (light mode)",
    "Figure_02": "Book a Court in dark mode",
    "Figure_03": "Book a Court: courts-by-hours grid",
    "Figure_04": "Reschedule Booking",
    "Figure_05": "Cancel a Booking",
    "Figure_06": "View All Bookings",
    "Figure_07": "Register Member (membership type cards)",
    "Figure_08": "Manage Members",
    "Figure_09": "Renew Membership",
    "Figure_10": "Manage Coaches",
    "Figure_11": "Manage Classes",
    "Figure_12": "Enrol Member",
    "Figure_13": "Remove Member",
    "Figure_14": "Hours & Commission",
    "Figure_15": "Create Bill",
    "Figure_16": "Pay Bill",
    "Figure_17": "Void Bill",
    "Figure_18": "Delete Bill",
    "Figure_19": "View Receipt",
    "Figure_20": "Daily Revenue",
    "Figure_08a_update_member": "Update a member: success message",
    "Figure_08b_delete_member_confirm": "Delete a member: confirmation question",
    "Figure_08b2_delete_member_done": "Delete a member: success message",
    "Figure_10a_add_coach": "Add a coach: success message",
    "Figure_10b_update_coach": "Update a coach: success message",
    "Figure_10c_delete_coach_confirm": "Delete a coach: confirmation question",
    "Figure_11a_schedule_class": "Schedule a class: success message",
    "Figure_11b_update_class": "Update a class: success message",
    "Figure_11c_delete_class_confirm": "Delete a class: confirmation question",
    "Figure_54": "Program after starting (Home)",
    "Figure_55": "Booking menu: click Book a Court",
    "Figure_56": "Book a Court: hours picked, member chosen, click Book",
    "Figure_57": "Reschedule Booking: booking picked, click Reschedule",
    "Figure_58": "Cancel a Booking: booking picked, click Cancel Booking",
    "Figure_59": "View All Bookings",
    "Figure_60": "Membership menu: click Register",
    "Figure_61": "Register Member: form filled, click Register",
    "Figure_62": "Manage Members: member picked, click Save Changes",
    "Figure_63": "Renew Membership: member picked, click Renew",
    "Figure_64": "Coaching menu: click Manage Coaches",
    "Figure_65": "Manage Coaches: coach picked, click Save Changes",
    "Figure_66": "Manage Classes: class picked, click Save Changes",
    "Figure_67": "Enrol Member: class and member chosen, click Enrol",
    "Figure_68": "Remove Member: row picked, click Remove",
    "Figure_69": "Hours & Commission",
    "Figure_70": "Billing menu: click Create Bill",
    "Figure_71": "Create Bill: member chosen, click Create Bill",
    "Figure_72": "Pay Bill: bill picked, click Pay",
    "Figure_73": "Void Bill: bill picked, click Void Bill",
    "Figure_74": "View Receipt: bill picked, click View Receipt",
    "Figure_75": "Daily Revenue: click Show",
    "Popup_success_booking_made": "Pop-up: booking confirmed",
    "Popup_confirm_cancel_booking": "Pop-up question: cancel (part of) a booking?",
    "Popup_success_booking_part_cancelled": "Pop-up: part of a booking cancelled",
    "Popup_success_booking_cancelled": "Pop-up: whole booking cancelled",
    "Popup_success_member_registered": "Pop-up: member registered",
    "Popup_success_bill_paid": "Pop-up: bill paid",
    "Popup_success_receipt_shown": "Pop-up: receipt shown",
    "Popup_confirm_remove_member": "Pop-up question: remove member from class?",
    "Popup_error_member_delete_blocked": "Pop-up error: member can't be deleted",
    "Popup_error_cancel_blocked_bill": "Pop-up error: booking has a bill, can't cancel",
    "Popup_error_class_full": "Pop-up error: class is full",
    "Popup_error_coach_double_booked": "Pop-up error: coach already has a class then",
    "Popup_error_booking_in_past": "Pop-up error: date is in the past",
}


def figure_order(name):
    """Sort key: figures by number, then sub-figures, then pop-ups."""
    return (0 if name.startswith("Figure") else 1, name)


def write_index(out_dir, popup_texts):
    """Write INDEX.md: file | figure | caption (plus the real pop-up text)."""
    names = []
    for file_name in os.listdir(out_dir):
        if file_name.endswith(".png") and not file_name.startswith("_"):
            names.append(file_name[:-4])
    names.sort(key=figure_order)
    lines = ["# Real screenshots index", "",
             "Every picture is a PIL.ImageGrab capture of the running program. Pop-ups are the real Windows message boxes.",
             "", "| File | Figure | Caption | What the pop-up said |", "|---|---|---|---|"]
    for name in names:
        figure = name.split("_")[0] + " " + name.split("_")[1] if name.startswith("Figure") else "Pop-up"
        said = ""
        if name + ".png" in popup_texts:
            said = popup_texts[name + ".png"][1].replace("\n", " ")[:110]
        lines.append(f"| {name}.png | {figure} | {CAPTIONS.get(name, '')} | {said} |")
    with open(os.path.join(out_dir, "INDEX.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def write_contact_sheet(out_dir):
    """Thumbnails of every real screenshot on one sheet (for scanning only)."""
    names = []
    for file_name in os.listdir(out_dir):
        if file_name.endswith(".png") and not file_name.startswith("_"):
            names.append(file_name)
    names.sort(key=figure_order)
    columns, thumb_w, thumb_h, label_h = 6, 250, 160, 16
    rows = (len(names) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, file_name in enumerate(names):
        picture = Image.open(os.path.join(out_dir, file_name)).convert("RGB")
        picture.thumbnail((thumb_w - 6, thumb_h - 4))
        x = (index % columns) * thumb_w + 3
        y = (index // columns) * (thumb_h + label_h)
        sheet.paste(picture, (x, y + label_h))
        draw.text((x, y + 2), file_name[:-4][:38], fill="black")
    sheet.save(os.path.join(out_dir, "_contact_sheet.png"))
