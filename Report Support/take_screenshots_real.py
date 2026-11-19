"""Takes REAL screenshots of the running Sports Centre System (PIL.ImageGrab of
the real tkinter window, with the real Windows message boxes open). It runs the
program from a temporary COPY of Source Code, so your real data is never
touched, and it never edits the program. Run:  python take_screenshots_real.py
Output: Report Support/Screenshots_Real/. This is a report tool, not part of
the submitted program."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shot_core as core

TEMP_ROOT, SRC = core.make_temp_copy()
sys.path.insert(0, SRC)
import tkinter as tk
import common
import main

NAV = ("Home", "Booking", "Membership", "Coaching", "Billing", "Exit", "A+", "A-", "← Back", "Search")
TODAY = common.today_string()
TOMORROW = common.add_days_to_date(TODAY, 1)
YESTERDAY = common.add_days_to_date(TODAY, -1)
SNAPSHOT = os.path.join(TEMP_ROOT, "data_snapshot")

R = None   # the root window
S = None   # the Shooter
LOG = {}   # file name -> list of (title, message) pop-ups seen
FAILED_STEPS = []


# ---------------------------------------------------------------- helpers
def snapshot_data():
    """Remember the clean sample data of the temporary copy."""
    shutil.copytree(common.DATA_FOLDER, SNAPSHOT)


def reset_data():
    """Put the sample data back (between scenarios)."""
    shutil.rmtree(common.DATA_FOLDER, ignore_errors=True)
    shutil.copytree(SNAPSHOT, common.DATA_FOLDER)


def add_line(file_path, line):
    """Add one setup row to a data file of the temporary copy."""
    common.append_line(file_path, line)


def btn(text):
    """The last visible button with this text."""
    found = []
    for widget in core.visible(R, tk.Button):
        if widget.cget("text") == text:
            found.append(widget)
    if len(found) == 0:
        raise LookupError("no button " + text)
    return found[-1]


def click(text):
    """Invoke a visible button."""
    btn(text).invoke()
    R.update()


def open_page(tab, action=None):
    """Open a tab's menu, or one of its pages."""
    click(tab)
    click(tab)
    if action is not None:
        click(action)


def listbox():
    """The page's list."""
    return core.visible(R, tk.Listbox)[0]


def pick(prefix):
    """Select the list row that starts with prefix."""
    box = listbox()
    for index in range(box.size()):
        if box.get(index).strip().startswith(prefix):
            box.selection_clear(0, tk.END)
            box.selection_set(index)
            box.see(index)
            box.event_generate("<<ListboxSelect>>")
            R.update()
            return
    raise LookupError("no row " + prefix)


def row_label(prefix):
    """The widget-row label that starts with prefix (Manage pages)."""
    for widget in core.visible(R, tk.Label):
        if widget.cget("text").lstrip().startswith(prefix):
            return widget
    raise LookupError("no row " + prefix)


def click_row(prefix):
    """Click a Manage-page row so its form loads."""
    row_label(prefix).event_generate("<Button-1>")
    R.update()


def row_delete_button(prefix):
    """The Delete button on the same row as the label."""
    label = row_label(prefix)
    for widget in core.visible(R, tk.Button):
        if widget.cget("text") == "Delete" and widget.master is label.master:
            return widget
    raise LookupError("no Delete for " + prefix)


def entries():
    """Visible entries in page order."""
    return core.visible(R, tk.Entry)


def set_entry(widget, text):
    """Type into an entry like a user."""
    widget.focus_force()
    widget.delete(0, tk.END)
    widget.insert(0, text)
    widget.event_generate("<KeyRelease>", keysym="x")
    R.update()


def choose_option(current_text_start, wanted):
    """Pick a value in the OptionMenu whose current text starts as given."""
    for widget in core.visible(R, tk.OptionMenu):
        if widget.cget("text").startswith(current_text_start):
            menu = widget["menu"]
            for index in range(menu.index("end") + 1):
                if menu.entrycget(index, "label") == wanted:
                    menu.invoke(index)
                    R.update()
                    return
    raise LookupError("option " + wanted)


def option_menus():
    """Visible option menus in page order."""
    return core.visible(R, tk.OptionMenu)


def combo_entry():
    """The search entry next to a ▼ arrow."""
    for widget in entries():
        for sibling in widget.master.winfo_children():
            if isinstance(sibling, tk.Button) and sibling.cget("text") == "▼":
                return widget
    raise LookupError("no combo")


def combo_pick(search_text):
    """Type in the member/coach box and click the first match."""
    entry = combo_entry()
    set_entry(entry, search_text)
    popup = None
    for widget in R.winfo_children():
        if isinstance(widget, tk.Frame):
            for inner in widget.winfo_children():
                if isinstance(inner, tk.Listbox):
                    popup = inner
    inner = popup
    inner.event_generate("<ButtonPress-1>", x=5, y=inner.bbox(0)[1] + 3)
    R.update()


def free_cells():
    """Free (green, clickable) grid cells."""
    cells = []
    for widget in core.visible(R, tk.Button):
        if widget.cget("width") == 4 and widget.cget("bg") == common.FREE_COLOR and widget.cget("state") == "normal":
            cells.append(widget)
    return cells


def set_book_date(date_text):
    """Type a date in the Book a Court / Reschedule date box and redraw."""
    for widget in entries():
        if widget.cget("width") == 12:
            widget.delete(0, tk.END)
            widget.insert(0, date_text)
            widget.focus_force()
            widget.event_generate("<KeyRelease>", keysym="Return")
            R.update()
            return
    raise LookupError("no date box")


def prepare_booking(date_text, how_many=1, member="Siti"):
    """Fill Book a Court: date, free cells and the member. Returns the Book button."""
    set_book_date(date_text)
    cells = free_cells()
    cells[0].invoke()
    if how_many > 1:
        cells[1].invoke()
    if how_many > 2:
        cells[2].invoke()
    R.update()
    combo_pick(member)
    return btn("Book")


def page(name, tab, action, prepare=None, target_text=None, note=""):
    """Open a page, prepare it, and take a real screenshot."""
    open_page(tab, action)
    if prepare is not None:
        prepare()
    target = None
    if target_text is not None:
        target = btn(target_text)
    ok = S.shot(name, target, note)
    return ok


def popup(name_plan, action, target=None, key=None):
    """Run a click that opens real pop-ups; keep what they said."""
    seen = S.run_with_popups(action, name_plan, target)
    LOG[key or name_plan[0][1]] = seen
    R.update()
    return seen


def step(label, function):
    """Run one capture step; a failure is reported, not hidden."""
    try:
        function()
    except Exception as error:
        FAILED_STEPS.append((label, repr(error)))
        S.results.append((label, "-", "FAIL", "step crashed: " + repr(error)))
        try:
            R.update()
            for dialog in core.find_dialogs():
                core.press_button(dialog, "ok")
        except Exception:
            pass


# ---------------------------------------------------------------- section A and C
def sections_a_and_c():
    """System pages (Figures 1-20) and user-manual pages (Figures 54-75)."""
    reset_data()
    open_page("Home")
    S.shot("Figure_01.png", note="Home (light)")
    S.shot("Figure_54.png", note="Home after starting")

    # A: dark mode Book a Court (then back to light)
    open_page("Booking", "Book a Court")
    set_book_date(TOMORROW)
    click("☾ Dark Mode")
    R.update()
    S.shot("Figure_02.png", note="Book a Court in dark mode")
    click("☀ Light Mode") if any(w.cget("text").startswith("☀") for w in core.visible(R, tk.Button)) else None
    for widget in core.visible(R, tk.Button):
        if widget.cget("text").startswith("☀"):
            widget.invoke()
    R.update()

    def book_date():
        set_book_date(TOMORROW)

    step("Figure_03", lambda: page("Figure_03.png", "Booking", "Book a Court", book_date))
    step("Figure_04", lambda: page("Figure_04.png", "Booking", "Reschedule Booking"))
    step("Figure_05", lambda: page("Figure_05.png", "Booking", "Cancel a Booking"))
    step("Figure_06", lambda: page("Figure_06.png", "Booking", "View All Bookings"))
    step("Figure_07", lambda: page("Figure_07.png", "Membership", "Register"))
    step("Figure_08", lambda: page("Figure_08.png", "Membership", "Manage Members"))
    step("Figure_09", lambda: page("Figure_09.png", "Membership", "Renew Membership"))
    step("Figure_10", lambda: page("Figure_10.png", "Coaching", "Manage Coaches"))
    step("Figure_11", lambda: page("Figure_11.png", "Coaching", "Manage Classes"))
    step("Figure_12", lambda: page("Figure_12.png", "Coaching", "Enrol Member"))
    step("Figure_13", lambda: page("Figure_13.png", "Coaching", "Remove Member"))
    step("Figure_14", lambda: page("Figure_14.png", "Coaching", "Hours & Commission"))
    step("Figure_15", lambda: page("Figure_15.png", "Billing", "Create Bill"))
    step("Figure_16", lambda: page("Figure_16.png", "Billing", "Pay Bill"))
    step("Figure_17", lambda: page("Figure_17.png", "Billing", "Void Bill"))
    step("Figure_18", lambda: page("Figure_18.png", "Billing", "Delete Bill"))
    step("Figure_19", lambda: page("Figure_19.png", "Billing", "View Receipt"))
    step("Figure_20", lambda: page("Figure_20.png", "Billing", "Daily Revenue"))

    # C: user manual figures with the user's action visible
    def menu_shot(name, tab, entry_text):
        open_page(tab)
        S.shot(name, btn(entry_text), "menu")

    step("Figure_55", lambda: menu_shot("Figure_55.png", "Booking", "Book a Court"))

    def fig56():
        open_page("Booking", "Book a Court")
        book_button = prepare_booking(TOMORROW, 2)
        S.shot("Figure_56.png", book_button, "Book a Court filled")
    step("Figure_56", fig56)

    def picked(name, tab, action, prefix, button_text):
        open_page(tab, action)
        pick(prefix)
        S.shot(name, btn(button_text), prefix + " picked")

    step("Figure_57", lambda: picked("Figure_57.png", "Booking", "Reschedule Booking", "BKG002", "Reschedule"))
    step("Figure_58", lambda: picked("Figure_58.png", "Booking", "Cancel a Booking", "BKG002", "Cancel Booking"))

    def fig59():
        open_page("Booking", "View All Bookings")
        S.shot("Figure_59.png", btn("Search"), "View All")
    step("Figure_59", fig59)
    step("Figure_60", lambda: menu_shot("Figure_60.png", "Membership", "Register"))

    def fig61():
        open_page("Membership", "Register")
        entry_list = entries()
        set_entry(entry_list[0], "Aisyah Binti Omar")
        set_entry(entry_list[1], "0125550001")
        for widget in core.visible(R, tk.Button):
            if widget.cget("text").startswith("RM 60.00"):
                widget.invoke()
        R.update()
        S.shot("Figure_61.png", btn("Register"), "Register filled")
    step("Figure_61", fig61)

    def fig62():
        open_page("Membership", "Manage Members")
        click_row("MEM004")
        S.shot("Figure_62.png", btn("Save Changes"), "MEM004 loaded")
    step("Figure_62", fig62)
    step("Figure_63", lambda: picked("Figure_63.png", "Membership", "Renew Membership", "MEM001", "Renew"))
    step("Figure_64", lambda: menu_shot("Figure_64.png", "Coaching", "Manage Coaches"))

    def fig65():
        open_page("Coaching", "Manage Coaches")
        click_row("CCH003")
        S.shot("Figure_65.png", btn("Save Changes"), "CCH003 loaded")
    step("Figure_65", fig65)

    def fig66():
        open_page("Coaching", "Manage Classes")
        click_row("CLS001")
        S.shot("Figure_66.png", btn("Save Changes"), "CLS001 loaded")
    step("Figure_66", fig66)

    def fig67():
        open_page("Coaching", "Enrol Member")
        pick("CLS001")
        combo_pick("Ravi")
        S.shot("Figure_67.png", btn("Enrol"), "CLS001 + member")
    step("Figure_67", fig67)
    step("Figure_68", lambda: picked("Figure_68.png", "Coaching", "Remove Member", "CLS001", "Remove"))

    def fig69():
        open_page("Coaching", "Hours & Commission")
        S.shot("Figure_69.png", btn("Search"), "hours")
    step("Figure_69", fig69)
    step("Figure_70", lambda: menu_shot("Figure_70.png", "Billing", "Create Bill"))

    def fig71():
        open_page("Billing", "Create Bill")
        combo_pick("Siti")
        S.shot("Figure_71.png", btn("Create Bill"), "member chosen")
    step("Figure_71", fig71)
    step("Figure_72", lambda: picked("Figure_72.png", "Billing", "Pay Bill", "BIL002", "Pay"))
    step("Figure_73", lambda: picked("Figure_73.png", "Billing", "Void Bill", "BIL003", "Void Bill"))
    step("Figure_74", lambda: picked("Figure_74.png", "Billing", "View Receipt", "BIL001", "View Receipt"))

    def fig75():
        open_page("Billing", "Daily Revenue")
        click("Show")
        S.shot("Figure_75.png", btn("Show"), "revenue")
    step("Figure_75", fig75)


# ---------------------------------------------------------------- section B and D
def choose_group_radio():
    """Click the Group radio button on Manage Classes."""
    for widget in core.visible(R, tk.Radiobutton):
        if widget.cget("text") == "Group":
            widget.invoke()
    R.update()


def sections_b_and_d():
    """Add/update/delete steps and the pop-up pictures."""
    # ---- B: members
    def update_member():
        reset_data()
        open_page("Membership", "Manage Members")
        click_row("MEM004")
        set_entry(entries()[0], "Ravi Kumar Singh")
        popup([("ok", "Figure_08a_update_member.png")], btn("Save Changes").invoke, btn("Save Changes"))
    step("Figure_08a", update_member)

    def delete_member():
        reset_data()
        open_page("Membership", "Manage Members")
        popup([("yes", "Figure_08b_delete_member_confirm.png"), ("ok", "Figure_08b2_delete_member_done.png")],
              row_delete_button("MEM005").invoke, row_delete_button("MEM005"))
    step("Figure_08b", delete_member)

    # ---- B: coaches
    def add_coach():
        reset_data()
        open_page("Coaching", "Manage Coaches")
        fields = entries()
        set_entry(fields[0], "Farah Binti Ali")
        set_entry(fields[1], "0127776655")
        set_entry(fields[2], "48.00")
        set_entry(fields[3], "20")
        popup([("ok", "Figure_10a_add_coach.png")], btn("Add Coach").invoke, btn("Add Coach"))
    step("Figure_10a", add_coach)

    def update_coach():
        reset_data()
        open_page("Coaching", "Manage Coaches")
        click_row("CCH003")
        set_entry(entries()[2], "50.00")
        popup([("ok", "Figure_10b_update_coach.png")], btn("Save Changes").invoke, btn("Save Changes"))
    step("Figure_10b", update_coach)

    def delete_coach():
        reset_data()
        open_page("Coaching", "Manage Coaches")
        popup([("yes", "Figure_10c_delete_coach_confirm.png"), ("ok", None)],
              row_delete_button("CCH003").invoke, row_delete_button("CCH003"))
    step("Figure_10c", delete_coach)

    # ---- B: classes
    def schedule_class():
        reset_data()
        open_page("Coaching", "Manage Classes")
        choose_group_radio()
        combo_pick("Lim")
        fields = entries()
        set_entry(fields[1], common.add_days_to_date(TODAY, 6))
        set_entry(fields[2], "8")
        set_entry(fields[3], "20.00")
        popup([("ok", "Figure_11a_schedule_class.png")], btn("Schedule Class").invoke, btn("Schedule Class"))
    step("Figure_11a", schedule_class)

    def update_class():
        reset_data()
        open_page("Coaching", "Manage Classes")
        click_row("CLS001")
        set_entry(entries()[3], "30.00")
        popup([("ok", "Figure_11b_update_class.png")], btn("Save Changes").invoke, btn("Save Changes"))
    step("Figure_11b", update_class)

    def delete_class():
        reset_data()
        open_page("Coaching", "Manage Classes")
        popup([("yes", "Figure_11c_delete_class_confirm.png"), ("ok", None)],
              row_delete_button("CLS001").invoke, row_delete_button("CLS001"))
    step("Figure_11c", delete_class)

    # ---- D: success pop-ups
    def booking_made_and_part_cancel():
        reset_data()
        open_page("Booking", "Book a Court")
        book_button = prepare_booking(TOMORROW, 3, "Ravi")
        popup([("ok", "Popup_success_booking_made.png")], book_button.invoke, book_button)
        open_page("Booking", "Cancel a Booking")
        newest = None
        for row in listbox().get(0, tk.END):
            if "MEM004" in row:
                newest = row.strip().split()[0]
        pick(newest)
        menus = option_menus()
        menus[1]["menu"].invoke(0)
        R.update()
        popup([("yes", "Popup_confirm_cancel_booking.png"), ("ok", "Popup_success_booking_part_cancelled.png")],
              btn("Cancel Booking").invoke, btn("Cancel Booking"))
    step("Popup booking made/part cancel", booking_made_and_part_cancel)

    def cancel_whole():
        reset_data()
        open_page("Booking", "Cancel a Booking")
        pick("BKG002")
        popup([("yes", None), ("ok", "Popup_success_booking_cancelled.png")],
              btn("Cancel Booking").invoke, btn("Cancel Booking"))
    step("Popup booking cancelled", cancel_whole)

    def register_member():
        reset_data()
        open_page("Membership", "Register")
        fields = entries()
        set_entry(fields[0], "Aisyah Binti Omar")
        set_entry(fields[1], "0125550001")
        for widget in core.visible(R, tk.Button):
            if widget.cget("text").startswith("RM 60.00"):
                widget.invoke()
        popup([("ok", "Popup_success_member_registered.png")], btn("Register").invoke, btn("Register"))
    step("Popup member registered", register_member)

    def pay_bill():
        reset_data()
        open_page("Billing", "Pay Bill")
        pick("BIL002")
        popup([("ok", "Popup_success_bill_paid.png"), ("ok", None)], btn("Pay").invoke, btn("Pay"))
    step("Popup bill paid", pay_bill)

    def receipt():
        reset_data()
        open_page("Billing", "View Receipt")
        pick("BIL001")
        popup([("ok", "Popup_success_receipt_shown.png")], btn("View Receipt").invoke, btn("View Receipt"))
    step("Popup receipt", receipt)

    # ---- D: confirmation questions
    def confirm_remove_member():
        reset_data()
        open_page("Coaching", "Remove Member")
        pick("CLS001")
        popup([("yes", "Popup_confirm_remove_member.png"), ("ok", None)], btn("Remove").invoke, btn("Remove"))
    step("Popup remove member", confirm_remove_member)

    # ---- D: errors
    def err_member_delete_blocked():
        reset_data()
        open_page("Membership", "Manage Members")
        popup([("yes", None), ("ok", "Popup_error_member_delete_blocked.png")],
              row_delete_button("MEM002").invoke, row_delete_button("MEM002"))
    step("Popup member delete blocked", err_member_delete_blocked)

    def err_cancel_blocked():
        reset_data()
        open_page("Booking", "Cancel a Booking")
        pick("BKG004")
        popup([("yes", None), ("ok", "Popup_error_cancel_blocked_bill.png")],
              btn("Cancel Booking").invoke, btn("Cancel Booking"))
    step("Popup cancel blocked", err_cancel_blocked)

    def err_full_class():
        reset_data()
        add_line(common.CLASSES_FILE, "CLS090|CCH001|Badminton|Group|" + common.add_days_to_date(TODAY, 9)
                 + "|15|1|3|25.00|MEM001;MEM003")
        open_page("Coaching", "Enrol Member")
        pick("CLS090")
        combo_pick("Ravi")
        # another user fills the last place after the list was shown
        shutil.copy(common.CLASSES_FILE, common.CLASSES_FILE + ".bak")
        lines = common.read_lines(common.CLASSES_FILE)
        rewritten = []
        for line in lines:
            if line.startswith("CLS090"):
                line = line + ";MEM002"
            rewritten.append(line)
        common.write_lines(common.CLASSES_FILE, rewritten)
        popup([("ok", "Popup_error_class_full.png")], btn("Enrol").invoke, btn("Enrol"))
    step("Popup class full", err_full_class)

    def err_coach_double_booked():
        reset_data()
        open_page("Coaching", "Manage Classes")
        choose_group_radio()
        combo_pick("Lim")
        fields = entries()
        set_entry(fields[1], common.add_days_to_date(TODAY, 4))
        set_entry(fields[2], "8")
        set_entry(fields[3], "20.00")
        for menu_widget in option_menus():
            menu = menu_widget["menu"]
            for index in range(menu.index("end") + 1):
                if menu.entrycget(index, "label") == "10:00":
                    menu.invoke(index)
        R.update()
        popup([("ok", "Popup_error_coach_double_booked.png")], btn("Schedule Class").invoke, btn("Schedule Class"))
    step("Popup coach double booked", err_coach_double_booked)

    def err_past_booking():
        reset_data()
        open_page("Booking", "Reschedule Booking")
        pick("BKG002")
        set_entry(entries()[0], YESTERDAY)
        popup([("yes", None), ("ok", "Popup_error_booking_in_past.png")], btn("Reschedule").invoke, btn("Reschedule"))
    step("Popup booking in past", err_past_booking)


# ---------------------------------------------------------------- run
def run(root):
    global R, S
    R = root
    root.report_callback_exception = lambda *error: FAILED_STEPS.append(("Tk callback", str(error[1])))
    S = core.Shooter(root)
    S.place()
    snapshot_data()
    which = sys.argv[1:] or ["all"]
    if "all" in which or "ac" in which:
        sections_a_and_c()
    if "all" in which or "bd" in which:
        sections_b_and_d()
    S.write_boxes()
    import shot_extras
    shot_extras.write_index(core.OUT_DIR, S.popup_texts)
    shot_extras.write_contact_sheet(core.OUT_DIR)
    print_results()
    root.destroy()


def print_results():
    """Print the PASS/FAIL table."""
    print()
    print(f"{'file':52} {'size':>10}  result  note")
    for name, size, status, note in S.results:
        print(f"{name:52} {size:>10}  {status:6}  {note}")
    failed = 0
    for entry in S.results:
        if entry[2] != "PASS":
            failed += 1
    print(len(S.results), "images,", failed, "failed")
    for name, seen in LOG.items():
        print("POPUPS", name, [message.replace(chr(10), " / ")[:100] for title, message in seen])
    for label, error in FAILED_STEPS:
        print("STEP FAILED:", label, error)


tk.Tk.mainloop = lambda self, n=0: run(self)
if __name__ == "__main__":
    main.main()
    shutil.rmtree(TEMP_ROOT, ignore_errors=True)
