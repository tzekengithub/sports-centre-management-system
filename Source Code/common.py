"""
Module      : common.py
Author      : Shared (all members)
Purpose     : Shared constants, file helpers, ID generator, validators,
              GUI style constants and the Person base class used by
              every module in the Sports Centre Management System.
Date        : 2026-11-05
"""

import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# FOLDER / FILE PATHS
# ---------------------------------------------------------------------------
# Built from this file's own location (not the current working directory)
# so the program works the same whether it is launched with
# "python main.py" from Source Code/, or from any other folder.
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, "data")
RECEIPT_FOLDER = os.path.join(DATA_FOLDER, "receipts")

MEMBERS_FILE = os.path.join(DATA_FOLDER, "members.txt")
BOOKINGS_FILE = os.path.join(DATA_FOLDER, "bookings.txt")
COACHES_FILE = os.path.join(DATA_FOLDER, "coaches.txt")
CLASSES_FILE = os.path.join(DATA_FOLDER, "classes.txt")
BILLS_FILE = os.path.join(DATA_FOLDER, "bills.txt")

FILE_ENCODING = "utf-8"

# ---------------------------------------------------------------------------
# DOMAIN CONSTANTS
# ---------------------------------------------------------------------------
SPORTS = {
    "Badminton": {"courts": 4, "rate": 20.0},
    "Futsal": {"courts": 2, "rate": 80.0},
    "Tennis": {"courts": 3, "rate": 30.0},
    "Squash": {"courts": 2, "rate": 25.0},
}

MEMBERSHIP_TYPES = ("Annual", "Monthly", "Pay-As-You-Go", "VIP", "Youth", "Senior", "Family")

MEMBERSHIP_FEES = {
    "Annual": 600.0,
    "Monthly": 60.0,
    "Pay-As-You-Go": 0.0,
    "VIP": 1200.0,
    "Youth": 300.0,
    "Senior": 350.0,
    "Family": 900.0,
}

MEMBER_DISCOUNT_PCT = {
    "Annual": 10.0,
    "Monthly": 5.0,
    "Pay-As-You-Go": 0.0,
    "VIP": 20.0,
    "Youth": 8.0,
    "Senior": 10.0,
    "Family": 12.0,
}

# Coaches can teach the court sports above plus non-court activities
# (swimming lessons, yoga classes). Classes do not book a court, so these
# extra sports need no court count or rate.
COACHING_SPORTS = ("Badminton", "Futsal", "Tennis", "Squash", "Swimming", "Yoga")

# Friendly names for the four bill categories, used on screen.
BILL_CATEGORY_NAMES = {
    "COURT": "Court Rental",
    "COACHING": "Coaching",
    "RETAIL": "Retail Sales",
    "MEMBERSHIP": "Membership Fees",
}

OPENING_HOUR = 8
CLOSING_HOUR = 22

VALID_PAYMENT_METHODS = {"Cash", "Card", "E-Wallet"}

BOOKING_STATUSES = ("CONFIRMED", "CANCELLED")
BILL_CATEGORIES = ("COURT", "COACHING", "MEMBERSHIP", "RETAIL")
BILL_STATUSES = ("UNPAID", "PAID", "VOID")

# ---------------------------------------------------------------------------
# GUI STYLE CONSTANTS (used by every module so the whole program looks alike)
# ---------------------------------------------------------------------------
APP_BG = "#f2f4f7"
PANEL_BG = "#ffffff"
ACCENT_COLOR = "#2f6f4e"
BUTTON_COLOR = "#2f6f4e"
BUTTON_TEXT_COLOR = "#ffffff"
DANGER_COLOR = "#8c1c1c"
TITLE_FONT = ("Segoe UI", 16, "bold")
LABEL_FONT = ("Segoe UI", 10)
ENTRY_FONT = ("Segoe UI", 10)
MONO_FONT = ("Consolas", 10)
BUTTON_FONT = ("Segoe UI", 10, "bold")
SMALL_FONT = ("Segoe UI", 9)
HEADING_FONT = ("Segoe UI", 11, "bold")
MUTED_TEXT_COLOR = "#5b6573"
BORDER_COLOR = "#d9dee5"
FREE_COLOR = "#d8efe0"
BOOKED_COLOR = "#f3d3d3"
SELECTED_COLOR = "#f6c453"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 560
BUTTON_WIDTH = 10
FIELD_PAD = 6


# ---------------------------------------------------------------------------
# SHARED GUI BUILDING BLOCKS (so every tab looks and behaves the same)
# ---------------------------------------------------------------------------
def make_button(parent, text, command, style="primary", width=None):
    """Create a button in one of the shared styles: 'primary' (green),
    'danger' (red, for permanent actions) or 'light' (white with green
    text, for less important actions). Returns the Button."""
    if style == "danger":
        background, foreground = DANGER_COLOR, BUTTON_TEXT_COLOR
    elif style == "light":
        background, foreground = PANEL_BG, ACCENT_COLOR
    else:
        background, foreground = BUTTON_COLOR, BUTTON_TEXT_COLOR
    button = tk.Button(parent, text=text, command=command, font=BUTTON_FONT,
                       bg=background, fg=foreground, activebackground=background,
                       activeforeground=foreground, disabledforeground="#9aa3ad",
                       relief="flat", bd=0, padx=12, pady=5, cursor="hand2")
    if width is not None:
        button.config(width=width)
    return button


def make_card(parent):
    """Create a white panel with a thin border, used to group a form."""
    return tk.Frame(parent, bg=PANEL_BG, padx=14, pady=12,
                    highlightbackground=BORDER_COLOR, highlightthickness=1)


def add_form_row(form_frame, row_index, label_text, widget):
    """Place a label and its input widget on one row of a grid form."""
    tk.Label(form_frame, text=label_text, font=LABEL_FONT, bg=PANEL_BG,
             anchor="w").grid(row=row_index, column=0, sticky="w", padx=(0, 10), pady=4)
    widget.grid(row=row_index, column=1, sticky="w", pady=4)


def make_entry(parent, width=24):
    """Create a standard text-entry box."""
    return tk.Entry(parent, font=ENTRY_FONT, width=width, relief="solid", bd=1)


def make_option_menu(parent, variable, choices, command=None, width=22):
    """Create a drop-down menu for the given choices (a list of strings).
    command, if given, is called with the chosen value."""
    # Start with one blank entry, then fill in the real choices with the
    # same helper used when a list changes later.
    menu = tk.OptionMenu(parent, variable, "")
    set_option_menu_choices(menu, variable, choices, command)
    menu.config(font=ENTRY_FONT, width=width, bg=PANEL_BG, relief="solid", bd=1,
                highlightthickness=0, anchor="w")
    return menu


def set_option_menu_choices(menu, variable, choices, command=None):
    """Replace the choices of an existing drop-down (e.g. after the data
    it lists has changed). Keeps the current value if it is still a
    choice, otherwise selects the first one."""
    dropdown = menu["menu"]
    dropdown.delete(0, "end")

    def make_choice_command(choice_text):
        """Return the command for one drop-down entry."""
        def choice_command():
            """Select this drop-down entry."""
            variable.set(choice_text)
            if command is not None:
                command(choice_text)
        return choice_command

    for choice_text in choices:
        dropdown.add_command(label=choice_text, command=make_choice_command(choice_text))
    if variable.get() not in choices:
        if len(choices) > 0:
            variable.set(choices[0])
        else:
            variable.set("")


def build_list_panel(parent, header_text, height=14):
    """Build a monospace column-header label above a scrollable list.
    Returns (panel_frame, listbox). The header is a separate label, so
    row 0 of the listbox is always real data."""
    panel_frame = tk.Frame(parent, bg=APP_BG)
    tk.Label(panel_frame, text=header_text, font=MONO_FONT, bg=APP_BG,
             fg=MUTED_TEXT_COLOR, anchor="w").pack(side="top", fill="x")
    list_holder = tk.Frame(panel_frame, bg=APP_BG)
    list_holder.pack(side="top", fill="both", expand=True)
    scrollbar = tk.Scrollbar(list_holder)
    scrollbar.pack(side="right", fill="y")
    listbox = tk.Listbox(list_holder, font=MONO_FONT, height=height, yscrollcommand=scrollbar.set,
                         activestyle="none", selectbackground=ACCENT_COLOR, relief="solid", bd=1,
                         exportselection=False)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)
    return panel_frame, listbox


def build_action_menu(window, title_text, action_list):
    """Build the standard tab layout: a "What would you like to do?" menu
    with one big button per action, and one page per action.
    action_list is a list of (action_name, menu_hint, page_instructions).
    Each page has a Back button, its name, one line of instructions and an
    empty content frame. Returns (page_frames, page_hooks): page_frames
    maps action_name -> content frame to build the page in; a function put
    in page_hooks[action_name] is called every time that page opens."""
    menu_frame = tk.Frame(window, bg=APP_BG)
    page_frames = {}
    page_hooks = {}
    outer_pages = {}

    def show_menu():
        """Hide every action page and show the menu."""
        for outer_page in outer_pages.values():
            outer_page.pack_forget()
        menu_frame.pack(fill="both", expand=True)

    def make_open_command(action_name):
        """Return the command for one menu button: open that action's page."""
        def open_command():
            """Show this action's page and refresh it."""
            menu_frame.pack_forget()
            outer_pages[action_name].pack(fill="both", expand=True)
            if action_name in page_hooks:
                page_hooks[action_name]()
        return open_command

    tk.Label(menu_frame, text=title_text, font=TITLE_FONT, bg=APP_BG,
             fg=ACCENT_COLOR).pack(pady=(30, 4))
    tk.Label(menu_frame, text="What would you like to do?", font=HEADING_FONT, bg=APP_BG,
             fg=MUTED_TEXT_COLOR).pack(pady=(0, 20))
    button_grid = tk.Frame(menu_frame, bg=APP_BG)
    button_grid.pack()

    # 3 buttons per row when there are many actions, otherwise 2.
    if len(action_list) > 4:
        column_count = 3
    else:
        column_count = 2

    for action_index, (action_name, menu_hint, page_instructions) in enumerate(action_list):
        cell = tk.Frame(button_grid, bg=APP_BG)
        cell.grid(row=action_index // column_count, column=action_index % column_count, padx=10, pady=8)
        menu_button = make_button(cell, action_name, make_open_command(action_name), width=22)
        menu_button.config(pady=10)
        menu_button.pack()
        tk.Label(cell, text=menu_hint, font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR).pack(pady=(3, 0))

        outer_page = tk.Frame(window, bg=APP_BG)
        top_row = tk.Frame(outer_page, bg=APP_BG)
        top_row.pack(side="top", fill="x", padx=16, pady=(12, 2))
        make_button(top_row, "← Back", show_menu, style="light").pack(side="left")
        tk.Label(top_row, text=action_name, font=TITLE_FONT, bg=APP_BG,
                 fg=ACCENT_COLOR).pack(side="left", padx=14)
        tk.Label(outer_page, text=page_instructions, font=LABEL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR,
                 anchor="w", justify="left").pack(side="top", fill="x", padx=16, pady=(4, 10))
        content_frame = tk.Frame(outer_page, bg=APP_BG)
        content_frame.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 12))
        page_frames[action_name] = content_frame
        outer_pages[action_name] = outer_page

    show_menu()
    return page_frames, page_hooks


def build_pick_page(page_frame, list_header, load_rows, action_label, action_function,
                    describe=None, build_form=None, fill_form=None, confirm_text=None,
                    danger=False, search_label=None, summary_text=None,
                    empty_text="Nothing to show here.", result_title="Done"):
    """Build a "pick one, then act" page: a list on the left and, on the
    right, the picked row's details plus ONE action button.
      load_rows(search_text)  -> list of (row_id, row_text) to list
      describe(row_id)        -> details text for the picked row
      build_form(form_frame)  -> adds input fields once (optional)
      fill_form(row_id)       -> fills those fields when a row is picked
      action_function(row_id) -> does the work and returns a message, or
                                 raises ValueError with a plain message
      confirm_text(row_id)    -> question to confirm first (optional)
      summary_text()          -> a line shown under the list (optional)
    action_label None means a view-only page with no button.
    Returns a refresh function (put it in page_hooks)."""
    pick_state = {"row_id": None}
    row_ids = []

    left_frame = tk.Frame(page_frame, bg=APP_BG)
    left_frame.pack(side="left", fill="both", expand=True)

    search_entry = None
    if search_label is not None:
        search_row = tk.Frame(left_frame, bg=APP_BG)
        search_row.pack(side="top", fill="x", pady=(0, 6))
        tk.Label(search_row, text=search_label, font=LABEL_FONT, bg=APP_BG).pack(side="left")
        search_entry = make_entry(search_row, width=18)
        search_entry.pack(side="left", padx=6)

    list_panel, listbox = build_list_panel(left_frame, list_header)
    list_panel.pack(side="top", fill="both", expand=True)
    summary_label = tk.Label(left_frame, text="", font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR,
                             anchor="w", justify="left", wraplength=520)
    summary_label.pack(side="top", fill="x", pady=(6, 0))

    card = make_card(page_frame)
    card.pack(side="right", fill="y", padx=(12, 0))
    details_label = tk.Label(card, text="", font=LABEL_FONT, bg=PANEL_BG, justify="left",
                             anchor="w", width=32)
    details_label.pack(side="top", anchor="w")
    form_frame = tk.Frame(card, bg=PANEL_BG)
    if build_form is not None:
        build_form(form_frame)

    def show_pick():
        """Show the picked row's details, form and button (or a hint)."""
        form_frame.pack_forget()
        if action_button is not None:
            action_button.pack_forget()
        row_id = pick_state["row_id"]
        if row_id is None:
            if len(row_ids) == 0:
                details_label.config(text=empty_text)
            else:
                details_label.config(text="Click one on the left.")
            return
        if describe is not None:
            details_label.config(text=describe(row_id))
        else:
            details_label.config(text="")
        if build_form is not None:
            if fill_form is not None:
                fill_form(row_id)
            form_frame.pack(side="top", anchor="w", pady=(10, 0))
        if action_button is not None:
            action_button.pack(side="top", anchor="w", pady=(12, 0))

    def refresh():
        """Reload the list (using the search text, if any) and forget the pick."""
        search_text = ""
        if search_entry is not None:
            search_text = search_entry.get().strip()
        listbox.delete(0, tk.END)
        row_ids.clear()
        for row_id, row_text in load_rows(search_text):
            listbox.insert(tk.END, row_text)
            row_ids.append(row_id)
        if summary_text is not None:
            summary_label.config(text=summary_text())
        pick_state["row_id"] = None
        show_pick()

    def on_row_selected(event):
        """Remember the clicked row and show it on the right."""
        row_index = selected_index(listbox)
        if row_index is None:
            return
        pick_state["row_id"] = row_ids[row_index]
        show_pick()

    listbox.bind("<<ListboxSelect>>", on_row_selected)

    def on_action():
        """Confirm if needed, run the action, show the result, refresh."""
        row_id = pick_state["row_id"]
        if row_id is None:
            return
        if confirm_text is not None and not messagebox.askyesno(action_label, confirm_text(row_id)):
            return
        try:
            message = action_function(row_id)
        except ValueError as error:
            messagebox.showerror("Please check", str(error))
            return
        messagebox.showinfo(result_title, message)
        refresh()

    if search_entry is not None:
        def on_search_key(event):
            """Search when Enter is pressed in the search box."""
            refresh()

        search_entry.bind("<Return>", on_search_key)
        make_button(search_row, "Search", refresh).pack(side="left")

    if action_label is None:
        action_button = None
    elif danger:
        action_button = make_button(card, action_label, on_action, style="danger")
    else:
        action_button = make_button(card, action_label, on_action)

    return refresh


def build_scroll_area(parent):
    """Build a bordered, vertically scrolling area for a list made of
    widgets (e.g. rows that each carry their own button, which a Listbox
    cannot hold). Returns the inner frame to pack the rows into."""
    holder = tk.Frame(parent, bg=PANEL_BG, highlightbackground="#000000", highlightthickness=1)
    holder.pack(side="top", fill="both", expand=True)
    canvas = tk.Canvas(holder, bg=PANEL_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(holder, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)
    inner_frame = tk.Frame(canvas, bg=PANEL_BG)
    inner_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_inner_resized(event):
        """Let the scrollbar cover all the rows."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resized(event):
        """Stretch the rows to the full width of the area."""
        canvas.itemconfigure(inner_window, width=event.width)

    inner_frame.bind("<Configure>", on_inner_resized)
    canvas.bind("<Configure>", on_canvas_resized)
    return inner_frame


def build_manage_page(page_frame, list_header, load_rows, item_name, build_form, clear_form, fill_form,
                      save_action, delete_action, delete_question, add_label=None, search_label="Name",
                      summary_text=None, empty_text="Nothing found."):
    """Build an add / update / delete page for one kind of record:
      - the list on the left has one row per record, each with its own
        red Delete button beside it;
      - clicking a row loads that record into the form on the right
        (highlighted), and the button becomes Save Changes;
      - with add_label given, a blank form adds a new record ("New"
        returns to a blank form); without it, the form only appears once
        a row is clicked.
    The module supplies:
      load_rows(search_text)    -> list of (record_id, row_text)
      build_form(form_frame)    -> adds the fields (grid rows from 0)
      clear_form()              -> empties every field
      fill_form(record_id)      -> loads a record into the fields
      save_action(record_id)    -> adds (record_id None) or saves; returns
                                   a message or raises ValueError
      delete_action(record_id)  -> deletes; returns a message or raises
      delete_question(record_id)-> confirmation question
      summary_text()            -> optional line under the list
    Returns the function to put in page_hooks (blank form, fresh list)."""
    page_state = {"editing_id": None}
    row_widgets = {}

    # --- left: search + one row per record, each with its own Delete ---
    left_frame = tk.Frame(page_frame, bg=APP_BG)
    left_frame.pack(side="left", fill="both", expand=True)
    search_row = tk.Frame(left_frame, bg=APP_BG)
    search_row.pack(side="top", fill="x", pady=(0, 6))
    tk.Label(search_row, text=search_label, font=LABEL_FONT, bg=APP_BG).pack(side="left")
    search_entry = make_entry(search_row, width=18)
    search_entry.pack(side="left", padx=6)
    tk.Label(left_frame, text=" " + list_header, font=MONO_FONT, bg=APP_BG,
             fg=MUTED_TEXT_COLOR, anchor="w").pack(side="top", fill="x")
    summary_label = tk.Label(left_frame, text="", font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR,
                             anchor="w", justify="left", wraplength=520)
    summary_label.pack(side="bottom", fill="x", pady=(6, 0))
    rows_frame = build_scroll_area(left_frame)

    # --- right: the add / update form ---
    card = make_card(page_frame)
    card.pack(side="right", fill="y", padx=(12, 0))
    form_title = tk.Label(card, text="", font=HEADING_FONT, bg=PANEL_BG, fg=ACCENT_COLOR, justify="left")
    form_title.pack(side="top", anchor="w", pady=(0, 8))
    form_frame = tk.Frame(card, bg=PANEL_BG)
    build_form(form_frame)
    button_row = tk.Frame(form_frame, bg=PANEL_BG)
    button_row.grid(row=50, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def highlight_row(record_id):
        """Colour the row being edited so it is obvious which one it is."""
        for row_record_id in row_widgets:
            if row_record_id == record_id:
                row_colour = FREE_COLOR
            else:
                row_colour = PANEL_BG
            row_frame, row_label = row_widgets[row_record_id]
            row_frame.config(bg=row_colour)
            row_label.config(bg=row_colour)

    def start_new():
        """Blank form (add mode), or hide the form if adding isn't offered."""
        page_state["editing_id"] = None
        clear_form()
        highlight_row(None)
        new_button.pack_forget()
        if add_label is None:
            form_title.config(text=f"Click a {item_name} to edit them")
            form_frame.pack_forget()
        else:
            form_title.config(text=f"New {item_name}")
            save_button.config(text=add_label)
            form_frame.pack(side="top", anchor="w")

    def edit_record(record_id):
        """Load the clicked record into the form for updating."""
        page_state["editing_id"] = record_id
        clear_form()
        fill_form(record_id)
        form_title.config(text=f"Edit {item_name} {record_id}")
        save_button.config(text="Save Changes")
        form_frame.pack(side="top", anchor="w")
        if add_label is not None:
            new_button.pack(side="left", padx=(6, 0))
        highlight_row(record_id)

    def remove_record(record_id):
        """Delete the record on this row (after confirming)."""
        if not messagebox.askyesno("Delete", delete_question(record_id)):
            return
        try:
            message = delete_action(record_id)
        except ValueError as error:
            messagebox.showerror("Please check", str(error))
            return
        messagebox.showinfo("Deleted", message)
        if page_state["editing_id"] == record_id:
            start_new()
        refresh_rows()

    def make_row_click(record_id):
        """Return the click handler for one row."""
        def row_click(event):
            """Edit this row's record."""
            edit_record(record_id)
        return row_click

    def make_row_delete(record_id):
        """Return the command for one row's Delete button."""
        def row_delete():
            """Delete this row's record."""
            remove_record(record_id)
        return row_delete

    def refresh_rows():
        """Rebuild one row (text + Delete button) per matching record."""
        for child_widget in rows_frame.winfo_children():
            child_widget.destroy()
        row_widgets.clear()
        rows = load_rows(search_entry.get().strip())
        if len(rows) == 0:
            tk.Label(rows_frame, text=empty_text, font=LABEL_FONT, bg=PANEL_BG,
                     fg=MUTED_TEXT_COLOR).pack(side="top", anchor="w", padx=6, pady=6)
        for record_id, row_text in rows:
            row_frame = tk.Frame(rows_frame, bg=PANEL_BG, cursor="hand2")
            row_frame.pack(side="top", fill="x")
            delete_button = make_button(row_frame, "Delete", make_row_delete(record_id), style="danger")
            delete_button.config(font=SMALL_FONT, padx=8, pady=1)
            delete_button.pack(side="right", padx=4, pady=2)
            row_label = tk.Label(row_frame, text=row_text, font=MONO_FONT, bg=PANEL_BG,
                                 anchor="w", cursor="hand2")
            row_label.pack(side="left", fill="x", expand=True, padx=(2, 0))
            row_frame.bind("<Button-1>", make_row_click(record_id))
            row_label.bind("<Button-1>", make_row_click(record_id))
            row_widgets[record_id] = (row_frame, row_label)
        highlight_row(page_state["editing_id"])
        if summary_text is not None:
            summary_label.config(text=summary_text())

    def on_save():
        """Add a new record (blank form) or save the one being edited."""
        try:
            message = save_action(page_state["editing_id"])
        except ValueError as error:
            messagebox.showerror("Please check", str(error))
            return
        messagebox.showinfo("Saved", message)
        start_new()
        refresh_rows()

    def on_search_key(event):
        """Search when Enter is pressed in the search box."""
        refresh_rows()

    search_entry.bind("<Return>", on_search_key)
    make_button(search_row, "Search", refresh_rows).pack(side="left")
    save_button = make_button(button_row, "Save Changes", on_save)
    save_button.pack(side="left")
    new_button = make_button(button_row, "New", start_new, style="light")

    def on_show():
        """Start with a blank form and a fresh list whenever the page opens."""
        search_entry.delete(0, tk.END)
        start_new()
        refresh_rows()

    return on_show


def selected_index(listbox):
    """Return the index of the selected row in listbox, or None."""
    selection = listbox.curselection()
    if len(selection) == 0:
        return None
    return selection[0]


# ---------------------------------------------------------------------------
# NUMBER INPUT (friendly messages instead of Python's own error text)
# ---------------------------------------------------------------------------
def parse_decimal(text, field_name, minimum, maximum):
    """Turn typed text into a number between minimum and maximum.
    Raises ValueError with a plain message for words, empty input,
    'nan'/'inf' (which float() would otherwise accept) or out-of-range
    values."""
    try:
        value = float(text.strip())
    except ValueError:
        raise ValueError(f"Please enter a valid number for {field_name}.")
    # nan is the only value that is not equal to itself.
    if value != value or value == float("inf") or value == float("-inf"):
        raise ValueError(f"Please enter a valid number for {field_name}.")
    if value < minimum or value > maximum:
        raise ValueError(f"{field_name} must be between {minimum:g} and {maximum:g}.")
    return value


def parse_whole_number(text, field_name, minimum, maximum):
    """Turn typed text into a whole number between minimum and maximum,
    raising ValueError with a plain message otherwise."""
    try:
        value = int(text.strip())
    except ValueError:
        raise ValueError(f"Please enter a whole number for {field_name}.")
    if value < minimum or value > maximum:
        raise ValueError(f"{field_name} must be between {minimum} and {maximum}.")
    return value


def is_finite_number(value):
    """Return True if value is a real, finite number (not nan or inf)."""
    return value == value and value != float("inf") and value != float("-inf")


def centre_window(window, width, height):
    """Centre a tkinter window on the screen. Inputs: window, width, height."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


MONTH_NAMES = ("January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December")
WEEKDAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def days_in_month(year, month):
    """Return how many days are in a given month, worked out from
    datetime instead of the calendar module (not on the allowed list)."""
    first_of_month = datetime(year, month, 1)
    if month == 12:
        first_of_next_month = datetime(year + 1, 1, 1)
    else:
        first_of_next_month = datetime(year, month + 1, 1)
    return (first_of_next_month - first_of_month).days


def open_date_picker(parent, target_entry, on_picked=None):
    """Open a small calendar pop-up (like a Google Forms date picker).
    Clicking a day fills target_entry with that date as YYYY-MM-DD and
    closes the pop-up; on_picked, if given, is then called so the screen
    can refresh straight away. Built entirely from plain tkinter widgets."""
    today = datetime.now()
    picker_state = {"year": today.year, "month": today.month}

    # parent may be a tab's Frame, but transient() needs a real window,
    # so the pop-up is owned by the main window that holds the tab.
    owner_window = parent.winfo_toplevel()
    picker_window = tk.Toplevel(owner_window)
    picker_window.title("Pick a Date")
    picker_window.configure(bg=PANEL_BG)
    picker_window.resizable(False, False)
    picker_window.transient(owner_window)
    picker_window.grab_set()

    header_frame = tk.Frame(picker_window, bg=PANEL_BG, pady=8)
    header_frame.pack()

    month_label = tk.Label(header_frame, text="", font=LABEL_FONT, bg=PANEL_BG, width=16)

    def go_previous_month():
        """Move the pop-up back one month and redraw it."""
        if picker_state["month"] == 1:
            picker_state["month"] = 12
            picker_state["year"] -= 1
        else:
            picker_state["month"] -= 1
        rebuild_calendar()

    def go_next_month():
        """Move the pop-up forward one month and redraw it."""
        if picker_state["month"] == 12:
            picker_state["month"] = 1
            picker_state["year"] += 1
        else:
            picker_state["month"] += 1
        rebuild_calendar()

    def go_to_today():
        """Jump the pop-up back to the current month and redraw it."""
        picker_state["year"] = today.year
        picker_state["month"] = today.month
        rebuild_calendar()

    tk.Button(header_frame, text="<", width=3, font=BUTTON_FONT,
              bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, command=go_previous_month).pack(side="left", padx=5)
    month_label.pack(side="left", padx=5)
    tk.Button(header_frame, text=">", width=3, font=BUTTON_FONT,
              bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, command=go_next_month).pack(side="left", padx=5)

    weekday_frame = tk.Frame(picker_window, bg=PANEL_BG)
    weekday_frame.pack()
    for column_index, weekday_name in enumerate(WEEKDAY_NAMES):
        tk.Label(weekday_frame, text=weekday_name, font=LABEL_FONT,
                 bg=PANEL_BG, width=4).grid(row=0, column=column_index)

    days_frame = tk.Frame(picker_window, bg=PANEL_BG, pady=5)
    days_frame.pack()

    def make_day_command(year_value, month_value, day_value):
        """Return the command for one day button: fill the entry and close."""
        def day_command():
            """Fill the date box with this day and close the pop-up."""
            target_entry.delete(0, tk.END)
            target_entry.insert(0, f"{year_value:04d}-{month_value:02d}-{day_value:02d}")
            picker_window.destroy()
            if on_picked is not None:
                on_picked()
        return day_command

    def rebuild_calendar():
        """Redraw the weekday grid of day buttons for the current
        picker_state['year']/['month']."""
        year = picker_state["year"]
        month = picker_state["month"]
        month_label.config(text=f"{MONTH_NAMES[month - 1]} {year}")

        for child_widget in days_frame.winfo_children():
            child_widget.destroy()

        first_of_month = datetime(year, month, 1)
        starting_weekday = first_of_month.weekday()
        total_days = days_in_month(year, month)

        row_index = 0
        column_index = starting_weekday
        for day_value in range(1, total_days + 1):
            is_today = (year == today.year and month == today.month and day_value == today.day)
            if is_today:
                button_bg = ACCENT_COLOR
            else:
                button_bg = BUTTON_COLOR
            day_button = tk.Button(days_frame, text=str(day_value), width=4, font=LABEL_FONT,
                                    bg=button_bg, fg=BUTTON_TEXT_COLOR,
                                    command=make_day_command(year, month, day_value))
            day_button.grid(row=row_index, column=column_index, padx=1, pady=1)
            column_index += 1
            if column_index > 6:
                column_index = 0
                row_index += 1

    rebuild_calendar()

    tk.Button(picker_window, text="Today", font=BUTTON_FONT,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=go_to_today).pack(pady=(0, 10))


# ---------------------------------------------------------------------------
# FILE HELPERS
# ---------------------------------------------------------------------------
def ensure_data_files_exist():
    """Create the data folder, receipts folder and any missing text files
    (filled with sample rows) so the program never starts with empty data.
    Returns True the very first time this runs on a fresh install (so
    main.py can show a one-time welcome message), False otherwise."""
    is_first_run = False
    if not os.path.isdir(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        is_first_run = True
    if not os.path.isdir(RECEIPT_FOLDER):
        os.makedirs(RECEIPT_FOLDER)

    sample_rows = build_sample_rows()
    for file_path, sample_lines in sample_rows.items():
        if not os.path.isfile(file_path):
            write_lines(file_path, sample_lines)
            is_first_run = True

    return is_first_run


def read_lines(file_path):
    """Read a text file and return a list of stripped, non-empty lines.
    Missing files are treated as empty (auto-recreated by ensure_data_files_exist)."""
    lines = []
    try:
        file_handle = open(file_path, "r", encoding=FILE_ENCODING)
    except FileNotFoundError:
        ensure_data_files_exist()
        return read_lines(file_path)
    else:
        for raw_line in file_handle:
            stripped_line = raw_line.strip()
            if stripped_line != "":
                lines.append(stripped_line)
        file_handle.close()
    return lines


def write_lines(file_path, lines):
    """Overwrite a text file with the given list of lines (one per line)."""
    try:
        file_handle = open(file_path, "w", encoding=FILE_ENCODING, newline="\n")
    except OSError as error:
        raise OSError(f"Could not write to {file_path}: {error}")
    else:
        for line in lines:
            file_handle.write(line + "\n")
    finally:
        file_handle.close()


def append_line(file_path, line):
    """Append a single record line to a text file."""
    try:
        file_handle = open(file_path, "a", encoding=FILE_ENCODING, newline="\n")
    except OSError as error:
        raise OSError(f"Could not append to {file_path}: {error}")
    else:
        file_handle.write(line + "\n")
    finally:
        file_handle.close()


def split_fields(line, expected_field_count):
    """Split a pipe-delimited line and return its fields, or None if the
    line does not have the expected number of fields (a malformed line).
    Every loader uses this so a corrupted or hand-edited data file is
    skipped instead of crashing the program."""
    fields = line.split("|")
    if len(fields) != expected_field_count:
        return None
    return fields


def contains_forbidden_character(text):
    """Return True if text contains '|' or ';', which would corrupt the
    pipe-delimited file format or a ';'-joined participant list."""
    return "|" in text or ";" in text


def generate_id(file_path, prefix):
    """Generate the next ID (e.g. MEM005) for a data file. Reads the file,
    finds the highest numeric suffix on lines starting with prefix, and
    returns prefix + next number zero-padded to 3 digits."""
    highest_number = 0
    for line in read_lines(file_path):
        fields = line.split("|")
        record_id = fields[0]
        if record_id.startswith(prefix):
            number_text = record_id[len(prefix):]
            if number_text.isdigit():
                number_value = int(number_text)
                if number_value > highest_number:
                    highest_number = number_value
    next_number = highest_number + 1
    return prefix + str(next_number).zfill(3)


# ---------------------------------------------------------------------------
# VALIDATORS
# ---------------------------------------------------------------------------
# Besides letters and spaces, names may contain "/" (a/l, s/o, d/o) and
# an apostrophe (Ch'ng, O'Neil). Neither can corrupt the "|" file format.
NAME_EXTRA_CHARACTERS = {" ", "/", "'"}
MAX_NAME_LENGTH = 40
NAME_RULE_MESSAGE = ("Name can only contain letters, spaces, / and ' "
                     "(e.g. Ravi a/l Kumar, Ch'ng Wei), up to 40 characters.")


def is_valid_name(name_text):
    """Return True if name_text starts with a letter, is at most
    MAX_NAME_LENGTH long, and only uses letters plus NAME_EXTRA_CHARACTERS."""
    cleaned_name = name_text.strip()
    if cleaned_name == "" or len(cleaned_name) > MAX_NAME_LENGTH:
        return False
    if not cleaned_name[0].isalpha():
        return False
    for character in cleaned_name:
        if not (character.isalpha() or character in NAME_EXTRA_CHARACTERS):
            return False
    return True


def format_name(name_text):
    """Tidy a name's capitals word by word: 'ch'ng wei' -> "Ch'ng Wei".
    Words containing '/' (a/l, s/o) are kept lower-case, and extra spaces
    are removed. str.title() is not used because it would turn Ch'ng
    into Ch'Ng."""
    tidy_words = []
    for word in name_text.split():
        if "/" in word:
            tidy_words.append(word.lower())
        else:
            tidy_words.append(word[0].upper() + word[1:].lower())
    return " ".join(tidy_words)


def is_valid_phone(phone_text):
    """Return True for a Malaysian-style phone: digits only, 10-11 digits,
    starting with 01."""
    cleaned_phone = phone_text.strip()
    if not cleaned_phone.isdigit():
        return False
    if len(cleaned_phone) < 10 or len(cleaned_phone) > 11:
        return False
    if not cleaned_phone.startswith("01"):
        return False
    return True


def is_valid_date(date_text):
    """Return True if date_text parses as YYYY-MM-DD."""
    try:
        datetime.strptime(date_text.strip(), "%Y-%m-%d")
    except ValueError:
        return False
    return True


def parse_date(date_text):
    """Parse YYYY-MM-DD into a datetime object, raising ValueError with a
    clear message on failure (caught by GUI handlers)."""
    try:
        parsed = datetime.strptime(date_text.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format, e.g. 2026-12-01")
    return parsed


def is_valid_hour(hour_value):
    """Return True if hour_value is within opening hours."""
    return OPENING_HOUR <= hour_value < CLOSING_HOUR


def today_string():
    """Return today's date as YYYY-MM-DD using datetime."""
    return datetime.now().strftime("%Y-%m-%d")


def current_hour():
    """Return the current hour of the day (0-23) using datetime."""
    return datetime.now().hour


def add_days_to_date(date_text, number_of_days):
    """Return date_text plus number_of_days, as a YYYY-MM-DD string."""
    base_date = parse_date(date_text)
    new_date = base_date + timedelta(days=number_of_days)
    return new_date.strftime("%Y-%m-%d")


def build_sample_rows():
    """Build the sample data rows relative to today's date, so bookings and
    classes are always in the future (and member expiry dates always make
    sense) no matter what day the program is first run on. Only used by
    ensure_data_files_exist when a data file is missing."""
    today = today_string()

    member_rows = [
        "MEM001|Ahmad Faiz|0123456789|VIP|" + add_days_to_date(today, -370) + "|" + add_days_to_date(today, 10),
        "MEM002|Siti Nurhaliza|0134567890|Annual|" + add_days_to_date(today, -200) + "|" + add_days_to_date(today, 165),
        "MEM003|Wong Mei Ling|0169876543|Monthly|" + add_days_to_date(today, -5) + "|" + add_days_to_date(today, 25),
        "MEM004|Ravi Kumar|0145551234|Pay-As-You-Go|" + add_days_to_date(today, -300) + "|" + add_days_to_date(today, 65),
    ]
    booking_rows = [
        "BKG001|MEM001|Badminton|2|" + add_days_to_date(today, 5) + "|18|2|CONFIRMED",
        "BKG002|MEM002|Futsal|1|" + add_days_to_date(today, 8) + "|20|1|CONFIRMED",
        "BKG003|MEM003|Tennis|1|" + add_days_to_date(today, 3) + "|9|1|CANCELLED",
    ]
    coach_rows = [
        "CCH001|Lim Wei|0171234567|Badminton|60.00|30.00",
        "CCH002|Nurul Izzah|0192223344|Tennis|70.00|25.00",
    ]
    class_rows = [
        "CLS001|CCH001|Badminton|Group|" + add_days_to_date(today, 4) + "|10|1|8|25.00|MEM001;MEM003",
        "CLS002|CCH002|Tennis|Private|" + add_days_to_date(today, 7) + "|14|1|1|50.00|MEM002",
    ]
    bill_rows = [
        "BIL001|MEM001|COURT|BKG001|Badminton Court 2, 2h|40.00|8.00|32.00|PAID|" + today,
        "BIL002|MEM002|COACHING|CLS002|Tennis Private Lesson|50.00|0.00|50.00|UNPAID|" + today,
    ]

    return {
        MEMBERS_FILE: member_rows,
        BOOKINGS_FILE: booking_rows,
        COACHES_FILE: coach_rows,
        CLASSES_FILE: class_rows,
        BILLS_FILE: bill_rows,
    }


# ---------------------------------------------------------------------------
# PERSON BASE CLASS (encapsulation + inheritance base)
# ---------------------------------------------------------------------------
class Person:
    """Base class holding a person's private name and phone number.
    Member (membership.py) and Coach (coaching.py) inherit from this class,
    which demonstrates inheritance; the double-underscore attributes and
    validating setters demonstrate encapsulation."""

    def __init__(self, name, phone):
        """Create the object and validate its starting values."""
        self.__name = ""
        self.__phone = ""
        self.set_name(name)
        self.set_phone(phone)

    def get_name(self):
        """Return the person's name."""
        return self.__name

    def set_name(self, name):
        """Validate and store the person's name."""
        if not is_valid_name(name):
            raise ValueError(NAME_RULE_MESSAGE)
        self.__name = format_name(name)

    def get_phone(self):
        """Return the person's phone number."""
        return self.__phone

    def set_phone(self, phone):
        """Validate and store the person's phone number."""
        if not is_valid_phone(phone):
            raise ValueError("Phone must be 10-11 digits and start with 01.")
        self.__phone = phone.strip()
