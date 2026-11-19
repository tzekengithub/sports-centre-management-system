"""Step 1 of the numbered-marks job. Drives the REAL program (temporary copy, so
your data is safe), puts each page in the state a user has while following
the manual steps, takes a REAL screenshot of it (Screenshots_Real/Steps_Base/)
and records the real on-screen box of every widget that belongs to a step
(boxes_steps.json). Nothing is guessed from pixels. annotate_steps.py then
draws the numbered marks on copies of these pictures.
Run:  python take_step_marks.py   (leave the mouse alone for about a minute)"""

import json
import os
import sys

import take_screenshots_real as t
import shot_core as core
import tkinter as tk

BASE_DIR = os.path.join(core.OUT_DIR, "Steps_Base")
BOXES = {}      # figure -> list of {"step", "label", "boxes": [[x, y, w, h], ...]}
NOTES = []      # things that were not exactly as the prompt listed


# ---------------------------------------------------------------- geometry
def origin():
    """Screen position of the window's top-left corner."""
    left, top, _right, _bottom = t.S.window_box()
    return left, top


def box_of(widget):
    """[x, y, w, h] of a widget, relative to the window picture."""
    left, top = origin()
    return [widget.winfo_rootx() - left, widget.winfo_rooty() - top, widget.winfo_width(), widget.winfo_height()]


def union(widgets):
    """One box around several widgets."""
    boxes = []
    for widget in widgets:
        boxes.append(box_of(widget))
    x1 = min(b[0] for b in boxes)
    y1 = min(b[1] for b in boxes)
    x2 = max(b[0] + b[2] for b in boxes)
    y2 = max(b[1] + b[3] for b in boxes)
    return [x1, y1, x2 - x1, y2 - y1]


def selected_row_box():
    """Box of the picked row in the page's Listbox."""
    box = t.listbox()
    index = box.curselection()[0]
    x, y, w, h = box.bbox(index)
    left, top = origin()
    return [box.winfo_rootx() - left, box.winfo_rooty() - top + y, box.winfo_width(), h]


def label_with(prefix):
    """The visible label whose text starts with prefix."""
    for widget in core.visible(t.R, tk.Label):
        if widget.cget("text").lstrip().startswith(prefix):
            return widget
    raise LookupError("no label " + prefix)


def buttons_named(text):
    """All visible buttons with this text."""
    found = []
    for widget in core.visible(t.R, tk.Button):
        if widget.cget("text") == text:
            found.append(widget)
    return found


def entry_with_width(width):
    """First visible entry with this width."""
    for widget in t.entries():
        if int(widget.cget("width")) == width:
            return widget
    raise LookupError("no entry width %d" % width)


def radios(texts):
    """Visible radio buttons with these texts."""
    found = []
    for widget in core.visible(t.R, tk.Radiobutton):
        if widget.cget("text") in texts:
            found.append(widget)
    return found


def mark(step_number, label, *groups):
    """A step: each group is a box [x,y,w,h]; a list of widgets is unioned."""
    boxes = []
    for group in groups:
        if isinstance(group, list) and len(group) == 4 and isinstance(group[0], int):
            boxes.append(group)
        elif isinstance(group, (list, tuple)):
            boxes.append(union(list(group)))
        else:
            boxes.append(box_of(group))
    return {"step": step_number, "label": label, "boxes": boxes}


def take(figure, steps):
    """Take the real picture (already prepared) and store the step boxes."""
    os.makedirs(BASE_DIR, exist_ok=True)
    t.S.place()
    t.R.update()
    import time
    time.sleep(0.25)
    t.R.update()
    from PIL import ImageGrab
    image = ImageGrab.grab(bbox=t.S.window_box(), all_screens=True)
    path = os.path.join(BASE_DIR, figure + ".png")
    image.save(path)
    BOXES[figure] = steps()      # boxes are read now, while the window is in this exact place
    print(figure, image.size, [(s["step"], s["label"]) for s in BOXES[figure]])


# ---------------------------------------------------------------- one function per figure
def row_box_without_delete(row_label, delete_button):
    """The picked row's box, cut short so it does not include its own Delete button."""
    box = box_of(row_label.master)
    delete = box_of(delete_button)
    box[2] = delete[0] - box[0] - 6
    return box


def tab_step(tab_text):
    """Step 1 is always the module's tab."""
    return mark(1, tab_text + " tab", t.btn(tab_text))


def fig_55():
    t.open_page("Booking")
    take("Figure_55", lambda: [tab_step("Booking"), mark(2, "Book a Court button", t.btn("Book a Court"))])


def fig_56():
    t.open_page("Booking", "Book a Court")
    t.prepare_booking(t.TOMORROW, 2, "Siti")
    sports = []
    for name in common_sports():
        sports.extend(buttons_named(name))
    ticked = []
    for widget in core.visible(t.R, tk.Button):
        if widget.cget("text") == "✓":
            ticked.append(widget)
    take("Figure_56", lambda: [
        tab_step("Booking"),
        mark(2, "Date box and Sport buttons", union([entry_with_width(12), t.btn("📅")] + sports)),
        mark(3, "selected hours on one court", ticked),
        mark(4, "Member box", t.combo_entry().master),
        mark(5, "Book button", t.btn("Book"))])


def common_sports():
    """The sport names on the buttons."""
    return ["Badminton", "Futsal", "Tennis", "Squash"]


def fig_57():
    t.open_page("Booking", "Reschedule Booking")
    t.pick("BKG002")
    take("Figure_57", lambda: [
        tab_step("Booking"),
        mark(2, "picked booking row", selected_row_box()),
        mark(3, "new date, start time and court", [entry_with_width(12), t.btn("📅")] + t.option_menus()),
        mark(4, "Reschedule button", t.btn("Reschedule"))])


def fig_58():
    t.open_page("Booking", "Cancel a Booking")
    t.pick("BKG002")
    take("Figure_58", lambda: [
        tab_step("Booking"),
        mark(2, "picked booking row and search box", selected_row_box(), [entry_with_width(18), t.btn("Search")]),
        mark(3, "Cancel from and Cancel until", t.option_menus()),
        mark(4, "Cancel Booking button", t.btn("Cancel Booking"))])


def fig_59():
    t.open_page("Booking", "View All Bookings")
    t.pick("BKG001")
    take("Figure_59", lambda: [
        tab_step("Booking"),
        mark(2, "search box", [entry_with_width(18), t.btn("Search")]),
        mark(3, "picked row and details panel", selected_row_box(), label_with("Booking ID"))])


def fig_60():
    t.open_page("Membership")
    take("Figure_60", lambda: [tab_step("Membership"), mark(2, "Register button", t.btn("Register"))])


def fig_61():
    t.open_page("Membership", "Register")
    fields = t.entries()
    t.set_entry(fields[0], "Aisyah Binti Omar")
    t.set_entry(fields[1], "0125550001")
    chosen = None
    for widget in core.visible(t.R, tk.Button):
        if widget.cget("text").startswith("RM 60.00"):
            widget.invoke()
            chosen = widget
    t.R.update()
    take("Figure_61", lambda: [
        tab_step("Membership"),
        mark(2, "Name and Phone boxes", [fields[0], fields[1]]),
        mark(3, "chosen membership card", chosen.master),
        mark(4, "Register button", t.btn("Register"))])


def fig_62():
    t.open_page("Membership", "Manage Members")
    t.click_row("MEM004")
    row = t.row_label("MEM004")
    delete_beside = t.row_delete_button("MEM004")
    fields = t.entries()
    take("Figure_62", lambda: [
        tab_step("Membership"),
        mark(2, "picked member row and edit fields", row_box_without_delete(row, delete_beside), [fields[0], fields[1]] + t.option_menus()),
        mark(3, "Save Changes and Delete beside a member", t.btn("Save Changes"), delete_beside)])


def fig_63():
    t.open_page("Membership", "Renew Membership")
    t.pick("MEM001")
    take("Figure_63", lambda: [
        tab_step("Membership"), mark(2, "picked member row", selected_row_box()),
        mark(3, "Renew button", t.btn("Renew"))])


def fig_64():
    t.open_page("Coaching")
    take("Figure_64", lambda: [tab_step("Coaching"), mark(2, "Manage Coaches button", t.btn("Manage Coaches"))])


def fig_65():
    t.open_page("Coaching", "Manage Coaches")
    t.click_row("CCH003")
    row = t.row_label("CCH003")
    delete_beside = t.row_delete_button("CCH003")
    fields = t.entries()
    take("Figure_65", lambda: [
        tab_step("Coaching"),
        mark(2, "coach form fields and New button", [fields[0], fields[1], fields[2], fields[3]] + t.option_menus(), t.btn("New")),
        mark(3, "picked coach row and Save Changes", row_box_without_delete(row, delete_beside), t.btn("Save Changes")),
        mark(4, "Delete beside a coach", delete_beside)])


def fig_66():
    t.open_page("Coaching", "Manage Classes")
    t.click_row("CLS001")
    row = t.row_label("CLS001")
    delete_beside = t.row_delete_button("CLS001")
    fields = t.entries()
    form_widgets = [t.combo_entry().master, fields[1], btn_cal()] + radios(["Private", "Group"]) + t.option_menus() + [fields[2], fields[3]]
    take("Figure_66", lambda: [
        tab_step("Coaching"),
        mark(2, "class form fields and New button", form_widgets, t.btn("New")),
        mark(3, "picked class row and Save Changes", row_box_without_delete(row, delete_beside), t.btn("Save Changes")),
        mark(4, "Delete beside a class", delete_beside)])


def btn_cal():
    """The calendar button."""
    return t.btn("📅")


def fig_67():
    t.open_page("Coaching", "Enrol Member")
    t.pick("CLS001")
    t.combo_pick("Ravi")
    take("Figure_67", lambda: [
        tab_step("Coaching"), mark(2, "picked class row", selected_row_box()),
        mark(3, "Member box", t.combo_entry().master), mark(4, "Enrol button", t.btn("Enrol"))])


def fig_68():
    t.open_page("Coaching", "Remove Member")
    t.pick("CLS001")
    take("Figure_68", lambda: [
        tab_step("Coaching"), mark(2, "picked row", selected_row_box()), mark(3, "Remove button", t.btn("Remove"))])


def fig_69():
    t.open_page("Coaching", "Hours & Commission")
    take("Figure_69", lambda: [
        tab_step("Coaching"),
        mark(2, "All time / Month choice", t.option_menus()),
        mark(3, "coach name box and Search", [entry_with_width(18), btn_search()])])


def btn_search():
    """The Search button."""
    return t.btn("Search")


def fig_70():
    t.open_page("Billing")
    take("Figure_70", lambda: [tab_step("Billing"), mark(2, "Create Bill button", t.btn("Create Bill"))])


def fig_71():
    t.open_page("Billing", "Create Bill")
    t.combo_pick("Siti")
    t.R.update()
    preview = None
    for widget in core.visible(t.R, tk.Label):
        if widget.cget("text").startswith("Amount RM"):
            preview = widget
    court_box = t.option_menus()[0]
    take("Figure_71", lambda: [
        tab_step("Billing"),
        mark(2, "Member box and Bill for choices", t.combo_entry().master, radios(["Court Rental", "Coaching Class", "Membership Fee", "Retail Sale"])),
        mark(3, "booking box", court_box),
        mark(4, "amount line and Create Bill button", preview, t.btn("Create Bill"))])


def fig_72():
    t.open_page("Billing", "Pay Bill")
    t.pick("BIL002")
    take("Figure_72", lambda: [
        tab_step("Billing"), mark(2, "picked unpaid bill", selected_row_box()),
        mark(3, "payment method and amount received", radios(["Cash", "Card", "E-Wallet"]), entry_with_width(10)),
        mark(4, "Pay button", t.btn("Pay"))])


def fig_73():
    t.open_page("Billing", "Void Bill")
    t.pick("BIL003")
    take("Figure_73", lambda: [
        tab_step("Billing"), mark(2, "picked unpaid bill", selected_row_box()),
        mark(3, "Void Bill button", t.btn("Void Bill"))])


def fig_74():
    t.open_page("Billing", "View Receipt")
    t.pick("BIL001")
    take("Figure_74", lambda: [
        tab_step("Billing"), mark(2, "picked paid bill", selected_row_box()),
        mark(3, "View Receipt button", t.btn("View Receipt"))])


def fig_75():
    t.open_page("Billing", "Daily Revenue")
    t.click("Show")
    take("Figure_75", lambda: [
        tab_step("Billing"), mark(2, "date box", [entry_with_width(12), btn_cal()]), mark(3, "Show button", t.btn("Show"))])


FIGURES = [fig_55, fig_56, fig_57, fig_58, fig_59, fig_60, fig_61, fig_62, fig_63, fig_64, fig_65, fig_66,
           fig_67, fig_68, fig_69, fig_70, fig_71, fig_72, fig_73, fig_74, fig_75]


def run(root):
    """Take every figure from a clean copy of the sample data."""
    t.R = root
    t.S = core.Shooter(root)
    root.report_callback_exception = lambda *error: print("TK ERROR", error[1])
    t.S.place()
    t.snapshot_data()
    wanted = sys.argv[1:]
    for figure_function in FIGURES:
        if wanted and figure_function.__name__[4:] not in wanted:
            continue
        try:
            t.reset_data()
            figure_function()
        except Exception as error:
            print("FAILED", figure_function.__name__, repr(error))
    path = os.path.join(core.OUT_DIR, "boxes_steps.json")
    old = {}
    if wanted and os.path.isfile(path):
        old = json.load(open(path, encoding="utf-8"))
    old.update(BOXES)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(old, handle, indent=1)
    root.destroy()


tk.Tk.mainloop = lambda self, n=0: run(self)
if __name__ == "__main__":
    t.main.main()
    t.shutil.rmtree(t.TEMP_ROOT, ignore_errors=True)
