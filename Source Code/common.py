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
IMAGES_FOLDER = os.path.join(BASE_FOLDER, "images")   # membership card pictures (.png)
RECEIPT_FOLDER = os.path.join(DATA_FOLDER, "receipts")

MEMBERS_FILE = os.path.join(DATA_FOLDER, "members.txt")
BOOKINGS_FILE = os.path.join(DATA_FOLDER, "bookings.txt")
COACHES_FILE = os.path.join(DATA_FOLDER, "coaches.txt")
CLASSES_FILE = os.path.join(DATA_FOLDER, "classes.txt")
BILLS_FILE = os.path.join(DATA_FOLDER, "bills.txt")

FILE_ENCODING = "utf-8"
# Reading uses "utf-8-sig": it is the same as UTF-8 but silently skips the
# invisible BOM character some editors put at the start of a file, which
# would otherwise make the first record's ID unreadable.
READ_ENCODING = "utf-8-sig"

# Highest ID number ever handed out per prefix (e.g. CLS|7), so an ID is
# never reused after its record is deleted.
ID_COUNTER_FILE = os.path.join(DATA_FOLDER, "id_counters.txt")

# Recursive totals are used for the rubric, but Python stops recursion at
# about 1000 levels, so above this many items a plain loop is used.
RECURSION_SAFE_LIMIT = 500

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
# Two colour themes. Every widget takes its colours from the module-level
# names below at the moment it is built, so switching theme = calling
# apply_theme() and rebuilding the window (main.py does this).
THEMES = {
    "light": {
        "APP_BG": "#f2f4f7", "PANEL_BG": "#ffffff", "TEXT_COLOR": "#1f2328",
        "ACCENT_COLOR": "#2f6f4e", "BUTTON_COLOR": "#2f6f4e", "BUTTON_TEXT_COLOR": "#ffffff",
        "DANGER_COLOR": "#8c1c1c", "MUTED_TEXT_COLOR": "#5b6573", "BORDER_COLOR": "#d9dee5",
        "LIST_BORDER_COLOR": "#8a929c", "FREE_COLOR": "#d8efe0", "BOOKED_COLOR": "#f3d3d3",
        "SELECTED_COLOR": "#f6c453", "PAST_COLOR": "#e3e6ea", "DISABLED_TEXT_COLOR": "#9aa3ad",
        "TOOLTIP_BG": "#fff8dc", "TOOLTIP_TEXT_COLOR": "#2b2b2b", "SELECTED_TEXT_COLOR": "#1f2328",
        "INFO_COLOR": "#d3e4f7",
    },
    "dark": {
        "APP_BG": "#1c2026", "PANEL_BG": "#272c34", "TEXT_COLOR": "#e6e8eb",
        "ACCENT_COLOR": "#7fd1a6", "BUTTON_COLOR": "#2f7d55", "BUTTON_TEXT_COLOR": "#ffffff",
        "DANGER_COLOR": "#b13a3a", "MUTED_TEXT_COLOR": "#a3acb8", "BORDER_COLOR": "#3b424c",
        "LIST_BORDER_COLOR": "#4b535e", "FREE_COLOR": "#245a40", "BOOKED_COLOR": "#6e3030",
        "SELECTED_COLOR": "#e0a83a", "PAST_COLOR": "#353b44", "DISABLED_TEXT_COLOR": "#6c7480",
        "TOOLTIP_BG": "#3a3f47", "TOOLTIP_TEXT_COLOR": "#f2f2f2", "SELECTED_TEXT_COLOR": "#14171b",
        "INFO_COLOR": "#2a4a70",
    },
}
THEME_NAMES = ("light", "dark")
current_theme = {"name": "light"}

APP_BG = "#f2f4f7"
PANEL_BG = "#ffffff"
TEXT_COLOR = "#1f2328"
ACCENT_COLOR = "#2f6f4e"
BUTTON_COLOR = "#2f6f4e"
BUTTON_TEXT_COLOR = "#ffffff"
DANGER_COLOR = "#8c1c1c"
LIST_BORDER_COLOR = "#8a929c"
PAST_COLOR = "#e3e6ea"
DISABLED_TEXT_COLOR = "#9aa3ad"
TOOLTIP_TEXT_COLOR = "#2b2b2b"
TITLE_FONT = ("Segoe UI", 16, "bold")
LABEL_FONT = ("Segoe UI", 10)
ENTRY_FONT = ("Segoe UI", 10)
MONO_FONT = ("Consolas", 10)
BUTTON_FONT = ("Segoe UI", 10, "bold")
SMALL_FONT = ("Segoe UI", 9)
HEADING_FONT = ("Segoe UI", 11, "bold")
# Record zoom: ONLY the text of record lists (the rows and the heading
# above them: ID, name, type ...) is zoomed; everything else keeps its size.
RECORD_ZOOM_LEVELS = (100, 120, 140, 170, 200)
LIST_AREA_WIDTH = 570       # about how wide the list part of a page is at 100%
record_zoom = {"percent": 100}
MUTED_TEXT_COLOR = "#5b6573"
BORDER_COLOR = "#d9dee5"
FREE_COLOR = "#d8efe0"
BOOKED_COLOR = "#f3d3d3"
SELECTED_COLOR = "#f6c453"
SELECTED_TEXT_COLOR = "#1f2328"
INFO_COLOR = "#d3e4f7"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 560
BUTTON_WIDTH = 10
FIELD_PAD = 6


# ---------------------------------------------------------------------------
# SHARED GUI BUILDING BLOCKS (so every tab looks and behaves the same)
# ---------------------------------------------------------------------------
TOOLTIP_DELAY_MS = 450
TOOLTIP_BG = "#fff8dc"


def apply_theme(theme_name):
    """Switch every shared colour to the 'light' or 'dark' palette in
    THEMES. Widgets built afterwards use the new colours."""
    global APP_BG, PANEL_BG, TEXT_COLOR, ACCENT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR
    global DANGER_COLOR, MUTED_TEXT_COLOR, BORDER_COLOR, LIST_BORDER_COLOR, FREE_COLOR
    global BOOKED_COLOR, SELECTED_COLOR, PAST_COLOR, DISABLED_TEXT_COLOR, TOOLTIP_BG, TOOLTIP_TEXT_COLOR
    global SELECTED_TEXT_COLOR, INFO_COLOR
    if theme_name not in THEMES:
        theme_name = "light"
    palette = THEMES[theme_name]
    APP_BG = palette["APP_BG"]
    PANEL_BG = palette["PANEL_BG"]
    TEXT_COLOR = palette["TEXT_COLOR"]
    ACCENT_COLOR = palette["ACCENT_COLOR"]
    BUTTON_COLOR = palette["BUTTON_COLOR"]
    BUTTON_TEXT_COLOR = palette["BUTTON_TEXT_COLOR"]
    DANGER_COLOR = palette["DANGER_COLOR"]
    MUTED_TEXT_COLOR = palette["MUTED_TEXT_COLOR"]
    BORDER_COLOR = palette["BORDER_COLOR"]
    LIST_BORDER_COLOR = palette["LIST_BORDER_COLOR"]
    FREE_COLOR = palette["FREE_COLOR"]
    BOOKED_COLOR = palette["BOOKED_COLOR"]
    SELECTED_COLOR = palette["SELECTED_COLOR"]
    PAST_COLOR = palette["PAST_COLOR"]
    DISABLED_TEXT_COLOR = palette["DISABLED_TEXT_COLOR"]
    TOOLTIP_BG = palette["TOOLTIP_BG"]
    TOOLTIP_TEXT_COLOR = palette["TOOLTIP_TEXT_COLOR"]
    SELECTED_TEXT_COLOR = palette["SELECTED_TEXT_COLOR"]
    INFO_COLOR = palette["INFO_COLOR"]
    current_theme["name"] = theme_name


# Which palette names are used for which kind of widget option. Background
# and text options are mapped separately because a light-theme value can be
# shared between roles (white is both a panel background and button text).
BACKGROUND_ROLES = ("APP_BG", "PANEL_BG", "BUTTON_COLOR", "DANGER_COLOR", "FREE_COLOR", "BOOKED_COLOR",
                    "SELECTED_COLOR", "PAST_COLOR", "BORDER_COLOR", "LIST_BORDER_COLOR", "TOOLTIP_BG", "INFO_COLOR")
TEXT_ROLES = ("TEXT_COLOR", "ACCENT_COLOR", "BUTTON_TEXT_COLOR", "MUTED_TEXT_COLOR", "DISABLED_TEXT_COLOR",
              "TOOLTIP_TEXT_COLOR", "DANGER_COLOR")
BACKGROUND_OPTIONS = ("bg", "activebackground", "highlightbackground", "highlightcolor", "selectcolor",
                      "troughcolor", "disabledbackground", "readonlybackground", "selectbackground")
TEXT_OPTIONS = ("fg", "activeforeground", "disabledforeground", "insertbackground", "selectforeground")


def status_colours(kind):
    """Return (background, text colour) for a status kind, used for list rows
    and badges: 'good' (green), 'bad' (red), 'warn' (amber), 'info' (blue),
    'quiet' (grey). Read from the current palette each time."""
    match kind:
        case "good":
            return FREE_COLOR, TEXT_COLOR
        case "bad":
            return BOOKED_COLOR, TEXT_COLOR
        case "warn":
            return SELECTED_COLOR, SELECTED_TEXT_COLOR
        case "info":
            return INFO_COLOR, TEXT_COLOR
        case _:
            return PAST_COLOR, MUTED_TEXT_COLOR


def make_colour_map(old_theme_name, new_theme_name, role_names):
    """Return a dictionary of old colour -> new colour for the given palette names."""
    colour_map = {}
    for role_name in role_names:
        colour_map[THEMES[old_theme_name][role_name].lower()] = THEMES[new_theme_name][role_name]
    return colour_map


def recolour_widgets(root_window, old_theme_name, new_theme_name):
    """Change every widget under root_window from the old theme's colours to
    the new theme's, IN PLACE. Nothing is rebuilt, so the page you are on,
    typed text, selections and scroll positions all stay as they are. Call
    apply_theme() first so widgets built afterwards use the new colours."""
    background_map = make_colour_map(old_theme_name, new_theme_name, BACKGROUND_ROLES)
    text_map = make_colour_map(old_theme_name, new_theme_name, TEXT_ROLES)
    waiting = [root_window]
    while len(waiting) > 0:
        widget = waiting.pop()
        waiting.extend(widget.winfo_children())
        for option_names, colour_map in ((BACKGROUND_OPTIONS, background_map), (TEXT_OPTIONS, text_map)):
            for option in option_names:
                try:
                    current_colour = str(widget.cget(option)).lower()
                    if current_colour in colour_map:
                        widget.config(**{option: colour_map[current_colour]})
                except tk.TclError:
                    # This kind of widget doesn't have that option.
                    pass
        # List rows can each have their own colours (itemconfig): map those too.
        if widget.winfo_class() == "Listbox":
            for row_index in range(widget.size()):
                for item_option, item_map in (("background", background_map), ("foreground", text_map)):
                    item_colour = str(widget.itemcget(row_index, item_option)).lower()
                    if item_colour in item_map:
                        widget.itemconfig(row_index, **{item_option: item_map[item_colour]})
        # Options nobody sets get their colour from the option database's
        # "*Foreground" (a text colour), so those two options use the text map.
        for option in ("activebackground", "selectbackground"):
            try:
                current_colour = str(widget.cget(option)).lower()
                if current_colour in text_map:
                    widget.config(**{option: text_map[current_colour]})
            except tk.TclError:
                pass
        try:
            # Text typed in a box is highlighted as TEXT_COLOR with PANEL_BG letters, as in a new box.
            if widget.winfo_class() in ("Entry", "Canvas"):
                widget.config(selectbackground=TEXT_COLOR, selectforeground=PANEL_BG)
            # Dark text sits on the amber "selected" colour in both themes.
            if (widget.winfo_class() in ("Button", "Label") and str(widget.cget("bg")).lower() == SELECTED_COLOR.lower()
                    and str(widget.cget("text")).strip() != ""):
                widget.config(fg=SELECTED_TEXT_COLOR, activeforeground=SELECTED_TEXT_COLOR)
        except tk.TclError:
            pass


def apply_widget_defaults(root_window):
    """Set default colours (tkinter's option database) for widget options
    the code doesn't set itself - text colour, entry and list boxes,
    drop-down menus, radio buttons - so new widgets match the theme."""
    defaults = (
        ("*Foreground", TEXT_COLOR),
        ("*Label.Foreground", TEXT_COLOR),
        ("*Entry.Background", PANEL_BG),
        ("*Entry.Foreground", TEXT_COLOR),
        ("*Entry.insertBackground", TEXT_COLOR),
        ("*Entry.disabledBackground", PAST_COLOR),
        ("*Entry.disabledForeground", MUTED_TEXT_COLOR),
        ("*Listbox.Background", PANEL_BG),
        ("*Listbox.Foreground", TEXT_COLOR),
        ("*Menubutton.Foreground", TEXT_COLOR),
        ("*Menubutton.activeBackground", BORDER_COLOR),
        ("*Menubutton.activeForeground", TEXT_COLOR),
        ("*Menubutton.disabledForeground", DISABLED_TEXT_COLOR),
        ("*Menu.Background", PANEL_BG),
        ("*Menu.Foreground", TEXT_COLOR),
        ("*Menu.activeBackground", BUTTON_COLOR),
        ("*Menu.activeForeground", BUTTON_TEXT_COLOR),
        ("*Radiobutton.Foreground", TEXT_COLOR),
        ("*Radiobutton.activeForeground", TEXT_COLOR),
        ("*Radiobutton.selectColor", PANEL_BG),
        ("*Radiobutton.disabledForeground", DISABLED_TEXT_COLOR),
        ("*Button.Foreground", TEXT_COLOR),
        ("*Button.disabledForeground", DISABLED_TEXT_COLOR),
        ("*Canvas.Background", PANEL_BG),
    )
    for option_pattern, option_value in defaults:
        root_window.option_add(option_pattern, option_value)


SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.txt")


def load_setting(key, default_value):
    """Return the saved text for key in settings.txt, or default_value.
    The settings file is optional, so it is checked before reading."""
    if not os.path.isfile(SETTINGS_FILE):
        return default_value
    for line in read_lines(SETTINGS_FILE):
        if line.startswith(key + "="):
            return line[len(key) + 1:]
    return default_value


def save_setting(key, value):
    """Save key=value in settings.txt, keeping the other saved settings."""
    kept_lines = []
    if os.path.isfile(SETTINGS_FILE):
        for line in read_lines(SETTINGS_FILE):
            if not line.startswith(key + "="):
                kept_lines.append(line)
    kept_lines.append(key + "=" + str(value))
    write_lines(SETTINGS_FILE, kept_lines)


def load_theme_choice():
    """Return the theme saved last time ('light' if none was saved yet)."""
    theme_name = load_setting("theme", "light")
    if theme_name in THEMES:
        return theme_name
    return "light"


def save_theme_choice(theme_name):
    """Remember the chosen theme for the next time the program starts."""
    save_setting("theme", theme_name)


def load_record_zoom():
    """Return the record-text zoom % saved last time (100 if none or not a valid level)."""
    saved_text = load_setting("rowzoom", "100")
    if saved_text.isdigit() and int(saved_text) in RECORD_ZOOM_LEVELS:
        return int(saved_text)
    return 100


def save_record_zoom(zoom_percent):
    """Remember the record-text zoom % for the next time the program starts."""
    save_setting("rowzoom", zoom_percent)


def scaled_font(base_font, zoom_percent):
    """Return base_font ((family, size[, style])) with its size scaled by zoom_percent."""
    new_size = max(6, round(base_font[1] * zoom_percent / 100))
    return (base_font[0], new_size) + tuple(base_font[2:])


def record_font():
    """The font for record rows: the list font at the current record zoom."""
    return scaled_font(MONO_FONT, record_zoom["percent"])


def apply_record_zoom(zoom_percent):
    """Set the record-text zoom (100 = normal). Lists built afterwards use it."""
    record_zoom["percent"] = zoom_percent


def mark_record_text(widget):
    """Mark a widget as record text (a list row, a list heading or a
    list box) so rezoom_records resizes it. Returns the widget."""
    widget.record_text = True
    return widget


def rezoom_records(root_window):
    """Give every marked record-text widget under root_window the current
    record font, IN PLACE (nothing is rebuilt, so the page, typed text and
    selections stay). Everything else keeps its size."""
    waiting = [root_window]
    while len(waiting) > 0:
        widget = waiting.pop()
        waiting.extend(widget.winfo_children())
        if getattr(widget, "record_text", False):
            widget.config(font=record_font())


def add_tooltip(widget, tip_text):
    """Show a small yellow hint box explaining how to use widget when the
    mouse rests on it for a moment; it disappears when the mouse leaves
    or the widget is clicked. Does nothing if tip_text is None. tip_text
    may also be a function that returns the text when the hint opens."""
    if tip_text is None:
        return
    tip_state = {"window": None, "job": None}

    def show_tip():
        """Open the hint box just below the widget."""
        tip_state["job"] = None
        if tip_state["window"] is not None or not widget.winfo_exists():
            return
        x_position = widget.winfo_rootx() + 10
        y_position = widget.winfo_rooty() + widget.winfo_height() + 4
        tip_window = tk.Toplevel(widget)
        tip_window.wm_overrideredirect(True)
        tip_window.wm_geometry(f"+{x_position}+{y_position}")
        if callable(tip_text):
            shown_text = tip_text()
        else:
            shown_text = tip_text
        tk.Label(tip_window, text=shown_text, font=SMALL_FONT, bg=TOOLTIP_BG, fg=TOOLTIP_TEXT_COLOR,
                 relief="solid", bd=1, padx=7, pady=4, justify="left", wraplength=330).pack()
        tip_state["window"] = tip_window

    def hide_tip(event=None):
        """Cancel a pending hint and close an open one."""
        if tip_state["job"] is not None:
            widget.after_cancel(tip_state["job"])
            tip_state["job"] = None
        if tip_state["window"] is not None:
            tip_state["window"].destroy()
            tip_state["window"] = None

    def on_enter(event):
        """Start the short wait before showing the hint."""
        hide_tip()
        tip_state["job"] = widget.after(TOOLTIP_DELAY_MS, show_tip)

    widget.bind("<Enter>", on_enter, add="+")
    widget.bind("<Leave>", hide_tip, add="+")
    widget.bind("<ButtonPress>", hide_tip, add="+")


def make_button(parent, text, command, style="primary", width=None, tip=None):
    """Create a button in one of the shared styles: 'primary' (green),
    'danger' (red, for permanent actions) or 'light' (white with green
    text, for less important actions), with an optional hover hint.
    Returns the Button."""
    if style == "danger":
        background, foreground = DANGER_COLOR, BUTTON_TEXT_COLOR
    elif style == "light":
        background, foreground = PANEL_BG, ACCENT_COLOR
    else:
        background, foreground = BUTTON_COLOR, BUTTON_TEXT_COLOR
    button = tk.Button(parent, text=text, command=command, font=BUTTON_FONT,
                       bg=background, fg=foreground, activebackground=background,
                       activeforeground=foreground, disabledforeground=DISABLED_TEXT_COLOR,
                       relief="flat", bd=0, padx=12, pady=5, cursor="hand2")
    if width is not None:
        button.config(width=width)
    add_tooltip(button, tip)
    return button


def make_card(parent):
    """Create a white panel with a thin border, used to group a form."""
    return tk.Frame(parent, bg=PANEL_BG, padx=14, pady=12,
                    highlightbackground=BORDER_COLOR, highlightthickness=1)


def add_form_row(form_frame, row_index, label_text, widget, tip=None):
    """Place a label and its input widget on one row of a grid form. The
    optional hover hint is shown on both the label and the input."""
    row_label = tk.Label(form_frame, text=label_text, font=LABEL_FONT, bg=PANEL_BG, anchor="w")
    row_label.grid(row=row_index, column=0, sticky="w", padx=(0, 10), pady=4)
    widget.grid(row=row_index, column=1, sticky="w", pady=4)
    add_tooltip(row_label, tip)
    add_tooltip(widget, tip)


def make_entry(parent, width=24, tip=None):
    """Create a standard text-entry box with an optional hover hint."""
    entry = tk.Entry(parent, font=ENTRY_FONT, width=width, relief="solid", bd=1)
    add_tooltip(entry, tip)
    return entry


def make_option_menu(parent, variable, choices, command=None, width=22, tip=None):
    """Create a drop-down menu for the given choices (a list of strings).
    command, if given, is called with the chosen value; tip is an
    optional hover hint."""
    # Start with one blank entry, then fill in the real choices with the
    # same helper used when a list changes later.
    menu = tk.OptionMenu(parent, variable, "")
    set_option_menu_choices(menu, variable, choices, command)
    menu.config(font=ENTRY_FONT, width=width, bg=PANEL_BG, relief="solid", bd=1,
                highlightthickness=0, anchor="w")
    add_tooltip(menu, tip)
    return menu


def set_option_menu_choices(menu, variable, choices, command=None, placeholder=None):
    """Replace the choices of an existing drop-down (e.g. after the data
    it lists has changed). Keeps the current value if it is still a
    choice; otherwise shows placeholder (if given) or selects the first."""
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
        if placeholder is not None:
            variable.set(placeholder)
        elif len(choices) > 0:
            variable.set(choices[0])
        else:
            variable.set("")


# Shown in member/coach drop-downs until someone is really picked, so
# nobody is booked or billed by accident (it is never a real choice).
CHOOSE_TEXT = "(choose one)"


def make_filtered_menu(parent, variable, width=24, tip=None, command=None, stacked=False):
    """A search-as-you-type drop-down (a combo box built from an Entry, a
    small arrow button and a pop-up list). Click the box and type part of
    a name or ID: a list of matches drops down to click. Click the arrow
    to see everyone. Search uses the FULL text; the box shows (and the
    variable holds) the pick cut with ... to width, so pages key their
    lookups with fit_text(choice, width). Nothing is picked until the
    user picks: it starts on CHOOSE_TEXT, and typed text that isn't a
    real choice goes back to the last real pick when the user leaves.
    command(shown_text) is called when the pick changes.
    Returns (holder_frame, entry, set_choices); call set_choices(list)
    whenever the data changes. stacked is accepted but no longer needed."""
    holder = tk.Frame(parent, bg=PANEL_BG)
    entry = make_entry(holder, width=width,
                       tip=(tip + " " if tip else "") + "Click and type to search, or click the arrow to see everyone.")
    entry.config(textvariable=variable)
    entry.pack(side="left")
    state = {"full": [], "cut": [], "shown": [], "last_good": CHOOSE_TEXT, "was_valid": False, "popup": None,
             "list": None}

    def is_valid():
        """Is the box showing one of the real choices?"""
        return variable.get() in state["cut"]

    def tell_page():
        """Call the page's command when the pick became valid/invalid."""
        now_valid = is_valid()
        if now_valid:
            state["last_good"] = variable.get()
        if now_valid != state["was_valid"] or now_valid:
            state["was_valid"] = now_valid
            if command is not None:
                command(variable.get())

    def close_popup():
        """Hide the pop-up list."""
        if state["popup"] is not None:
            state["popup"].destroy()
            state["popup"] = None
            state["list"] = None

    def leave_box():
        """Close the list; text that isn't a real choice goes back to the last pick."""
        close_popup()
        if entry.winfo_exists() and not is_valid():
            variable.set(state["last_good"])
            tell_page()

    def pick(shown_text):
        """Choose one entry from the list."""
        variable.set(shown_text)
        close_popup()
        entry.icursor(tk.END)
        tell_page()

    def on_list_press(event):
        """Pick the row under the mouse (instead of Tk's own selection)."""
        index = state["list"].nearest(event.y)
        if 0 <= index < len(state["shown"]):
            pick(state["shown"][index])
        return "break"

    def on_list_motion(event):
        """Highlight the row under the mouse."""
        state["list"].selection_clear(0, tk.END)
        state["list"].selection_set(state["list"].nearest(event.y))

    def show_popup(matches):
        """Drop the list of matches (pairs of full/cut text) under the box."""
        close_popup()
        top = holder.winfo_toplevel()
        popup = tk.Frame(top, bg=PANEL_BG, highlightbackground=LIST_BORDER_COLOR, highlightthickness=1)
        scrollbar = tk.Scrollbar(popup)
        scrollbar.pack(side="right", fill="y")
        longest = width
        for full_text, cut_text in matches:
            longest = max(longest, min(len(full_text), POPUP_MAX_WIDTH))
        row_count = max(1, min(len(matches), 8))
        listbox = tk.Listbox(popup, font=ENTRY_FONT, width=longest, height=row_count, activestyle="none",
                             yscrollcommand=scrollbar.set, selectbackground=BUTTON_COLOR,
                             selectforeground=BUTTON_TEXT_COLOR, relief="flat", bd=0, exportselection=False)
        listbox.pack(side="left")
        scrollbar.config(command=listbox.yview)
        state["shown"] = []
        for full_text, cut_text in matches:
            listbox.insert(tk.END, fit_text(full_text, POPUP_MAX_WIDTH))
            state["shown"].append(cut_text)
        if len(matches) == 0:
            listbox.insert(tk.END, "No match")
        listbox.bind("<ButtonPress-1>", on_list_press)
        listbox.bind("<Motion>", on_list_motion)
        # Keep the whole list inside the window: drop it below the box if
        # there is room, otherwise open it upward (the member box on Book a
        # Court sits at the bottom of the page), shift it left if it would
        # run off the right edge, and as a last resort show fewer rows
        # (the list still scrolls).
        popup.update_idletasks()
        box_x = entry.winfo_rootx() - top.winfo_rootx()
        box_y = entry.winfo_rooty() - top.winfo_rooty()
        room_below = top.winfo_height() - (box_y + entry.winfo_height()) - 4
        room_above = box_y - 4
        list_height = popup.winfo_reqheight()
        if list_height > max(room_below, room_above) and row_count > 1:
            row_height = list_height / row_count
            fitting_rows = max(1, int((max(room_below, room_above) - 6) / row_height))
            listbox.config(height=fitting_rows)
            popup.update_idletasks()
            list_height = popup.winfo_reqheight()
        if list_height <= room_below or room_below >= room_above:
            list_y = box_y + entry.winfo_height()
        else:
            list_y = box_y - list_height
        list_x = max(0, min(box_x, top.winfo_width() - popup.winfo_reqwidth() - 4))
        popup.place(x=list_x, y=list_y)
        popup.lift()
        state["popup"] = popup
        state["list"] = listbox

    def matches_for(search_text):
        """Return (full, cut) pairs whose full text contains search_text."""
        search_text = search_text.strip().lower()
        matches = []
        for index in range(len(state["full"])):
            if search_text in state["full"][index].lower():
                matches.append((state["full"][index], state["cut"][index]))
        return matches

    def on_key(event):
        """Typing searches; Enter picks the first/highlighted match; Esc closes."""
        match event.keysym:
            case "Escape":
                leave_box()
            case "Return":
                if state["popup"] is not None and len(state["shown"]) > 0:
                    chosen = state["list"].curselection()
                    if len(chosen) > 0:
                        pick(state["shown"][chosen[0]])
                    else:
                        pick(state["shown"][0])
            case "Down" | "Up":
                if state["popup"] is None:
                    show_popup(matches_for(""))
                elif len(state["shown"]) > 0:
                    chosen = state["list"].curselection()
                    step = 1 if event.keysym == "Down" else -1
                    index = (chosen[0] + step) % len(state["shown"]) if len(chosen) > 0 else 0
                    state["list"].selection_clear(0, tk.END)
                    state["list"].selection_set(index)
                    state["list"].see(index)
            case "Tab" | "Shift_L" | "Shift_R" | "Left" | "Right" | "Home" | "End":
                pass
            case _:
                show_popup(matches_for(variable.get()))
                tell_page()

    def on_focus_in(event):
        """Clicking the box clears the "(choose one)" hint, or selects the pick so typing replaces it."""
        if variable.get() == CHOOSE_TEXT:
            variable.set("")
        else:
            entry.select_range(0, tk.END)

    def on_focus_out(event):
        """Tabbing away: tidy up (after a moment, so a click on the list still counts)."""
        entry.after(150, check_focus_left)

    def check_focus_left():
        """Close the list if the box really lost the focus."""
        if entry.winfo_exists() and entry.focus_get() is not entry:
            leave_box()

    def on_arrow():
        """Show or hide the full list of choices."""
        if state["popup"] is not None:
            close_popup()
            return
        entry.focus_set()
        show_popup(matches_for(""))

    arrow = make_button(holder, "\u25bc", on_arrow, style="light",
                        tip="Show everyone in a list, then click one.")
    arrow.config(padx=6, pady=1)
    arrow.pack(side="left", padx=(2, 0))

    def on_any_click(event):
        """A click anywhere else closes the list."""
        if not entry.winfo_exists() or state["popup"] is None:
            return
        clicked = str(event.widget)
        if clicked.startswith(str(state["popup"])) or clicked == str(entry) or clicked == str(arrow):
            return
        leave_box()

    def on_holder_destroyed(event):
        """The page is going away: remove the pop-up with it."""
        if event.widget is holder:
            close_popup()

    def on_entry_hidden(event):
        """The page was hidden (Back etc.): close the list."""
        close_popup()

    entry.bind("<KeyRelease>", on_key)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    entry.bind("<Unmap>", on_entry_hidden)
    holder.bind("<Destroy>", on_holder_destroyed)
    holder.winfo_toplevel().bind("<Button-1>", on_any_click, add="+")

    def set_choices(choices):
        """Replace the full list of choices. A pick that is still a choice is kept."""
        state["full"] = []
        state["cut"] = []
        for choice_text in choices:
            state["full"].append(choice_text)
            state["cut"].append(fit_text(choice_text, width))
        close_popup()
        if variable.get() not in state["cut"]:
            variable.set(CHOOSE_TEXT)
            state["last_good"] = CHOOSE_TEXT
            state["was_valid"] = False
        else:
            state["last_good"] = variable.get()
            state["was_valid"] = True

    return holder, entry, set_choices


POPUP_MAX_WIDTH = 42


def build_list_panel(parent, header_text, height=14):
    """Build a monospace column-header label above a scrollable list.
    Returns (panel_frame, listbox). The header is a separate label, so
    row 0 of the listbox is always real data."""
    panel_frame = tk.Frame(parent, bg=APP_BG)
    header_label = tk.Label(panel_frame, text=header_text, font=record_font(), bg=APP_BG,
                            fg=MUTED_TEXT_COLOR, anchor="w")
    header_label.pack(side="top", fill="x")
    mark_record_text(header_label)
    list_holder = tk.Frame(panel_frame, bg=APP_BG)
    list_holder.pack(side="top", fill="both", expand=True)
    scrollbar = tk.Scrollbar(list_holder)
    scrollbar.pack(side="right", fill="y")
    listbox = tk.Listbox(list_holder, font=record_font(), height=height, yscrollcommand=scrollbar.set,
                         activestyle="none", selectbackground=BUTTON_COLOR,
                         selectforeground=BUTTON_TEXT_COLOR, relief="solid", bd=1,
                         exportselection=False)
    listbox.pack(side="left", fill="both", expand=True)
    mark_record_text(listbox)
    scrollbar.config(command=listbox.yview)
    return panel_frame, listbox


def wrap_to_width(event):
    """Make a label's text wrap at the label's current width (bound to
    <Configure>, so it follows the window when it is resized)."""
    if event.width > 50:
        event.widget.config(wraplength=event.width - 4)


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
        menu_button = make_button(cell, action_name, make_open_command(action_name), width=22,
                                  tip=page_instructions)
        menu_button.config(pady=10)
        menu_button.pack()
        tk.Label(cell, text=menu_hint, font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR).pack(pady=(3, 0))

        outer_page = tk.Frame(window, bg=APP_BG)
        top_row = tk.Frame(outer_page, bg=APP_BG)
        top_row.pack(side="top", fill="x", padx=16, pady=(12, 2))
        make_button(top_row, "← Back", show_menu, style="light",
                    tip="Go back to the list of actions for this tab.").pack(side="left")
        tk.Label(top_row, text=action_name, font=TITLE_FONT, bg=APP_BG,
                 fg=ACCENT_COLOR).pack(side="left", padx=14)
        instructions_label = tk.Label(outer_page, text=page_instructions, font=LABEL_FONT, bg=APP_BG,
                                      fg=MUTED_TEXT_COLOR, anchor="w", justify="left",
                                      wraplength=WINDOW_WIDTH - 40)
        instructions_label.pack(side="top", fill="x", padx=16, pady=(4, 10))
        # Long instructions wrap onto a second line instead of being cut off.
        instructions_label.bind("<Configure>", wrap_to_width)
        content_frame = tk.Frame(outer_page, bg=APP_BG)
        content_frame.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 12))
        page_frames[action_name] = content_frame
        outer_pages[action_name] = outer_page

    def open_action_page(action_name):
        """Open one action's page directly, as if its menu button was clicked
        (used by the Home page shortcut buttons)."""
        if action_name in outer_pages:
            make_open_command(action_name)()

    # Kept on the tab's frame so the Home page can reach it after building the tab.
    window.open_action_page = open_action_page

    show_menu()
    return page_frames, page_hooks


def build_pick_page(page_frame, list_header, load_rows, action_label, action_function,
                    describe=None, build_form=None, fill_form=None, confirm_text=None,
                    danger=False, search_label=None, summary_text=None,
                    empty_text="Nothing to show here.", result_title="Done", action_tip=None,
                    refresh_on_error=False, badges=None):
    """Build a "pick one, then act" page: a list on the left and, on the
    right, the picked row's details plus ONE action button.
      load_rows(search_text)  -> list of (row_id, row_text[, kind]) to list;
                                 kind ('good', 'bad', 'warn', 'info',
                                 'quiet') colours that row
      badges(row_id)          -> list of (text, kind) shown as coloured
                                 badges above the details (optional)
      describe(row_id)        -> details text for the picked row
      build_form(form_frame)  -> adds input fields once (optional)
      fill_form(row_id)       -> fills those fields when a row is picked
      action_function(row_id) -> does the work and returns a message, or
                                 raises ValueError with a plain message
      confirm_text(row_id)    -> question to confirm first (optional)
      summary_text()          -> a line shown under the list (optional)
    action_label None means a view-only page with no button.
    refresh_on_error True reloads the list after a failed action, for pages
    whose list can go stale while open (e.g. a class that has started since).
    Returns a refresh function (put it in page_hooks)."""
    pick_state = {"row_id": None}
    row_ids = []

    # The card on the right is packed FIRST: pack hands out space in
    # order, so the details/button card keeps its full width and only the
    # list shrinks on a small screen.
    card = make_card(page_frame)
    card.pack(side="right", fill="y", padx=(12, 0))
    left_frame = tk.Frame(page_frame, bg=APP_BG)
    left_frame.pack(side="left", fill="both", expand=True)

    search_entry = None
    if search_label is not None:
        search_row = tk.Frame(left_frame, bg=APP_BG)
        search_row.pack(side="top", fill="x", pady=(0, 6))
        tk.Label(search_row, text=search_label, font=LABEL_FONT, bg=APP_BG).pack(side="left")
        search_entry = make_entry(search_row, width=18,
                                  tip=f"Type a {search_label} and press Enter or click Search. "
                                      "Leave it empty to show everything.")
        search_entry.pack(side="left", padx=6)

    list_panel, listbox = build_list_panel(left_frame, list_header)
    add_tooltip(listbox, "Click a row to see its details on the right.")
    list_panel.pack(side="top", fill="both", expand=True)
    summary_label = tk.Label(left_frame, text="", font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR,
                             anchor="w", justify="left", wraplength=520)
    summary_label.pack(side="top", fill="x", pady=(6, 0))

    # Coloured badges (e.g. CONFIRMED, NOT BILLED) sit above the details.
    badge_row = tk.Frame(card, bg=PANEL_BG)

    # Monospace so the "Label:  value" lines from details_text line up.
    details_label = tk.Label(card, text="", font=MONO_FONT, bg=PANEL_BG, justify="left",
                             anchor="w", width=DETAIL_LABEL_WIDTH + DETAIL_VALUE_WIDTH)
    details_label.pack(side="top", anchor="w")
    form_frame = tk.Frame(card, bg=PANEL_BG)
    if build_form is not None:
        build_form(form_frame)

    def show_pick():
        """Show the picked row's details, form and button (or a hint)."""
        form_frame.pack_forget()
        if action_button is not None:
            action_button.pack_forget()
        badge_row.pack_forget()
        for old_badge in badge_row.winfo_children():
            old_badge.destroy()
        row_id = pick_state["row_id"]
        if row_id is not None and badges is not None:
            for badge_text, badge_kind in badges(row_id):
                badge_bg, badge_fg = status_colours(badge_kind)
                tk.Label(badge_row, text=badge_text, font=BUTTON_FONT, bg=badge_bg, fg=badge_fg,
                         padx=7, pady=2).pack(side="left", padx=(0, 5))
            badge_row.pack(side="top", anchor="w", pady=(0, 8), before=details_label)
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
        for row in load_rows(search_text):
            listbox.insert(tk.END, row[1])
            row_ids.append(row[0])
            # An optional third item colours the row (green / red / grey ...).
            if len(row) > 2 and row[2] != "":
                row_bg, row_fg = status_colours(row[2])
                listbox.itemconfig(tk.END, background=row_bg, foreground=row_fg)
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
        except (ValueError, OSError) as error:
            messagebox.showerror("Please check", str(error))
            if refresh_on_error:
                refresh()
            return
        messagebox.showinfo(result_title, message)
        refresh()

    if search_entry is not None:
        def on_search_key(event):
            """Search when Enter is pressed in the search box."""
            refresh()

        search_entry.bind("<Return>", on_search_key)
        make_button(search_row, "Search", refresh,
                    tip="Show only the rows that match the text in the box.").pack(side="left")

    if action_tip is None and action_label is not None:
        action_tip = f"{action_label} for the row you clicked on the left."
    if action_label is None:
        action_button = None
    elif danger:
        action_button = make_button(card, action_label, on_action, style="danger",
                                    tip=action_tip + " You will be asked to confirm first.")
    else:
        action_button = make_button(card, action_label, on_action, tip=action_tip)

    return refresh


def build_scroll_area(parent):
    """Build a bordered, vertically scrolling area for a list made of
    widgets (e.g. rows that each carry their own button, which a Listbox
    cannot hold). Returns the inner frame to pack the rows into."""
    holder = tk.Frame(parent, bg=PANEL_BG, highlightbackground=LIST_BORDER_COLOR, highlightthickness=1)
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

    def on_mouse_wheel(event):
        """Scroll the rows with the mouse wheel. Windows/macOS send
        <MouseWheel> with event.delta; Linux sends Button-4 (up) and
        Button-5 (down) instead."""
        if not canvas.winfo_exists():
            return
        if canvas.yview() == (0.0, 1.0):
            return
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        else:
            canvas.yview_scroll(1, "units")

    def on_pointer_enter(event):
        """Send the mouse wheel to this list while the pointer is over it."""
        for wheel_event in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            canvas.bind_all(wheel_event, on_mouse_wheel)

    def on_pointer_leave(event):
        """Stop sending the wheel here once the pointer has really left
        (moving onto a row inside the list also fires <Leave>)."""
        pointer_x, pointer_y = holder.winfo_pointerxy()
        widget_under_pointer = holder.winfo_containing(pointer_x, pointer_y)
        if widget_under_pointer is not None and str(widget_under_pointer).startswith(str(holder)):
            return
        for wheel_event in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            canvas.unbind_all(wheel_event)

    inner_frame.bind("<Configure>", on_inner_resized)
    canvas.bind("<Configure>", on_canvas_resized)
    holder.bind("<Enter>", on_pointer_enter)
    holder.bind("<Leave>", on_pointer_leave)
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
      load_rows(search_text)    -> list of (record_id, row_text), or
                                   (record_id, row_text, "past") to show a
                                   row greyed out (e.g. a class that is over)
      build_form(form_frame)    -> adds the fields (grid rows from 0)
      clear_form()              -> empties every field
      fill_form(record_id)      -> loads a record into the fields
      save_action(record_id)    -> adds (record_id None) or saves; returns
                                   a message, None if the user cancelled,
                                   or raises ValueError
      delete_action(record_id)  -> deletes; returns a message or raises
      delete_question(record_id)-> confirmation question (None = don't ask)
      summary_text()            -> optional line under the list
    Returns the function to put in page_hooks (blank form, fresh list)."""
    page_state = {"editing_id": None}
    row_widgets = {}

    # --- right: the add / update form (packed first so it keeps its
    # width; only the list on the left shrinks on a small screen) ---
    card = make_card(page_frame)
    card.pack(side="right", fill="y", padx=(12, 0))

    # --- left: search + one row per record, each with its own Delete ---
    left_frame = tk.Frame(page_frame, bg=APP_BG)
    left_frame.pack(side="left", fill="both", expand=True)
    search_row = tk.Frame(left_frame, bg=APP_BG)
    search_row.pack(side="top", fill="x", pady=(0, 6))
    tk.Label(search_row, text=search_label, font=LABEL_FONT, bg=APP_BG).pack(side="left")
    search_entry = make_entry(search_row, width=18,
                              tip=f"Type a {search_label} and press Enter or click Search. "
                                  "Leave it empty to show everything.")
    search_entry.pack(side="left", padx=6)
    # padx lines the headings up with the row text below (rows have a 2 px indent inside their border).
    list_header_label = tk.Label(left_frame, text=list_header, font=record_font(), bg=APP_BG,
                                 fg=MUTED_TEXT_COLOR, anchor="w")
    list_header_label.pack(side="top", fill="x", padx=(2, 0))
    mark_record_text(list_header_label)
    summary_label = tk.Label(left_frame, text="", font=SMALL_FONT, bg=APP_BG, fg=MUTED_TEXT_COLOR,
                             anchor="w", justify="left", wraplength=520)
    summary_label.pack(side="bottom", fill="x", pady=(6, 0))
    rows_frame = build_scroll_area(left_frame)

    form_title = tk.Label(card, text="", font=HEADING_FONT, bg=PANEL_BG, fg=ACCENT_COLOR, justify="left")
    form_title.pack(side="top", anchor="w", pady=(0, 8))
    form_frame = tk.Frame(card, bg=PANEL_BG)
    build_form(form_frame)
    button_row = tk.Frame(form_frame, bg=PANEL_BG)
    button_row.grid(row=50, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def highlight_row(record_id):
        """Colour the row being edited so it is obvious which one it is."""
        for row_record_id in row_widgets:
            row_frame, row_label, row_is_past = row_widgets[row_record_id]
            if row_record_id == record_id:
                row_colour = FREE_COLOR
            elif row_is_past:
                row_colour = PAST_COLOR
            else:
                row_colour = PANEL_BG
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
        question = delete_question(record_id)
        # A question of None means "don't ask": go straight to the action.
        if question is not None and not messagebox.askyesno("Delete", question):
            return
        try:
            message = delete_action(record_id)
        except (ValueError, OSError) as error:
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
        for row in rows:
            record_id = row[0]
            row_text = row[1]
            # A "past" row (e.g. a class that is over) is greyed out.
            is_past = len(row) > 2 and row[2] == "past"
            if is_past:
                base_colour, text_colour = PAST_COLOR, MUTED_TEXT_COLOR
            else:
                base_colour, text_colour = PANEL_BG, TEXT_COLOR
            row_frame = tk.Frame(rows_frame, bg=base_colour, cursor="hand2")
            row_frame.pack(side="top", fill="x")
            delete_button = make_button(row_frame, "Delete", make_row_delete(record_id), style="danger",
                                        tip=f"Delete {record_id} permanently. You will be asked to confirm first.")
            delete_button.config(font=SMALL_FONT, padx=8, pady=1)
            delete_button.pack(side="right", padx=4, pady=2)
            row_label = tk.Label(row_frame, text=row_text, font=record_font(), bg=base_colour,
                                 fg=text_colour, anchor="w", cursor="hand2")
            mark_record_text(row_label)
            row_label.pack(side="left", fill="x", expand=True, padx=(2, 0))
            row_frame.bind("<Button-1>", make_row_click(record_id))
            row_label.bind("<Button-1>", make_row_click(record_id))
            add_tooltip(row_label, f"Click to load {record_id} into the form and change it.")
            row_widgets[record_id] = (row_frame, row_label, is_past)
        highlight_row(page_state["editing_id"])
        if summary_text is not None:
            summary_label.config(text=summary_text())

    def on_save():
        """Add a new record (blank form) or save the one being edited."""
        try:
            message = save_action(page_state["editing_id"])
        except (ValueError, OSError) as error:
            messagebox.showerror("Please check", str(error))
            return
        if message is None:
            return
        messagebox.showinfo("Saved", message)
        start_new()
        refresh_rows()

    def on_search_key(event):
        """Search when Enter is pressed in the search box."""
        refresh_rows()

    search_entry.bind("<Return>", on_search_key)
    make_button(search_row, "Search", refresh_rows,
                tip="Show only the rows that match the text in the box.").pack(side="left")
    if add_label is None:
        save_tip = f"Save the changes to the {item_name} you clicked."
    else:
        save_tip = (f"With a blank form: {add_label.lower()}. After clicking a row: "
                    f"save the changes to that {item_name}.")
    save_button = make_button(button_row, "Save Changes", on_save, tip=save_tip)
    save_button.pack(side="left")
    new_button = make_button(button_row, "New", start_new, style="light",
                             tip=f"Clear the form to add a new {item_name} instead.")

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
    # Every decimal in this program is money or a percentage, saved with 2
    # decimals - round first, so 0.004 becomes 0.00 and fails a 0.01 minimum
    # instead of passing and then being saved as 0.00.
    value = round(value, 2)
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


def fit_text(text, width):
    """Return text cut to at most width characters, ending in ... when it
    had to be shortened (so long names don't run into the next column)."""
    if len(text) <= width:
        return text
    return text[:width - 1] + "\u2026"


DETAIL_LABEL_WIDTH = 12
DETAIL_VALUE_WIDTH = 26


def wrap_words(text, width):
    """Split text into lines of at most width characters, breaking
    between words (a single word longer than width is cut into pieces)."""
    lines = []
    current_line = ""
    for word in text.split():
        while len(word) > width:
            if current_line != "":
                lines.append(current_line)
                current_line = ""
            lines.append(word[:width])
            word = word[width:]
        if current_line == "":
            current_line = word
        elif len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line != "" or len(lines) == 0:
        lines.append(current_line)
    return lines


def details_text(label_value_pairs):
    """Turn [("Class ID", "CLS001"), ("Sport", "Tennis"), ...] into neat
    lines like 'Class ID:   CLS001', one per pair, for the details panel.
    A long value wraps onto extra indented lines, so nothing is cut off.
    A label of "" makes a blank spacer line."""
    lines = []
    for label_text, value in label_value_pairs:
        if label_text == "":
            lines.append("")
            continue
        value_lines = wrap_words(str(value), DETAIL_VALUE_WIDTH)
        lines.append(f"{label_text + ':':<{DETAIL_LABEL_WIDTH}}{value_lines[0]}")
        for extra_line in value_lines[1:]:
            lines.append(" " * DETAIL_LABEL_WIDTH + extra_line)
    return "\n".join(lines)


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


def open_date_picker(parent, target_entry, on_picked=None, allow_past=True):
    """Open a small calendar pop-up (like a Google Forms date picker).
    Clicking a day fills target_entry with that date as YYYY-MM-DD and
    closes the pop-up; on_picked, if given, is then called so the screen
    can refresh straight away. It opens on the month already typed in the
    box (or this month). With allow_past False, days before today are
    greyed out and can't be clicked. Built from plain tkinter widgets."""
    today = datetime.now()
    picker_state = {"year": today.year, "month": today.month}
    if is_valid_date(target_entry.get()):
        typed_date = parse_date(target_entry.get())
        picker_state["year"] = typed_date.year
        picker_state["month"] = typed_date.month

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
              bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=go_previous_month).pack(side="left", padx=5)
    month_label.pack(side="left", padx=5)
    tk.Button(header_frame, text=">", width=3, font=BUTTON_FONT,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=go_next_month).pack(side="left", padx=5)

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
            day_text = f"{year:04d}-{month:02d}-{day_value:02d}"
            is_past_day = (not allow_past) and day_text < today_string()
            if is_today:
                button_bg = SELECTED_COLOR
            elif is_past_day:
                button_bg = PAST_COLOR
            else:
                button_bg = BUTTON_COLOR
            day_button = tk.Button(days_frame, text=str(day_value), width=4, font=LABEL_FONT,
                                    bg=button_bg, fg=BUTTON_TEXT_COLOR,
                                    disabledforeground=DISABLED_TEXT_COLOR,
                                    command=make_day_command(year, month, day_value))
            if is_past_day:
                day_button.config(state="disabled")
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

    # Remember the highest ID already in every file (sample rows, or rows
    # typed in by hand), so deleting one of them never frees its ID.
    for file_path in sample_rows:
        remember_highest_ids(read_lines(file_path))

    return is_first_run


def read_lines(file_path):
    """Read a text file and return a list of stripped, non-empty lines.
    Missing files are treated as empty (auto-recreated by ensure_data_files_exist)."""
    lines = []
    try:
        file_handle = open(file_path, "r", encoding=READ_ENCODING)
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


def file_error_message(file_path, error):
    """Plain message shown when a data file cannot be saved."""
    return (f"Could not save {os.path.basename(file_path)} ({error.strerror or error}). "
            "If the file is open in another program, close it and try again.")


def write_lines(file_path, lines):
    """Overwrite a text file with the given list of lines (one per line).
    Raises OSError with a plain message if the file cannot be opened. The
    file is only closed if it was actually opened."""
    try:
        file_handle = open(file_path, "w", encoding=FILE_ENCODING, newline="\n")
    except OSError as error:
        raise OSError(file_error_message(file_path, error))
    else:
        try:
            for line in lines:
                file_handle.write(line + "\n")
        finally:
            file_handle.close()


def append_line(file_path, line):
    """Remember the record's ID as used (so it is never handed out again,
    even after a delete), then append the line to the text file. The
    counter is saved FIRST: if that fails nothing has been saved yet, so
    trying again can't create the record twice."""
    note_used_id(line.split("|")[0])
    try:
        file_handle = open(file_path, "a", encoding=FILE_ENCODING, newline="\n")
    except OSError as error:
        raise OSError(file_error_message(file_path, error))
    else:
        try:
            file_handle.write(line + "\n")
        finally:
            file_handle.close()


def rewrite_records(file_path, record_lines, line_parser):
    """Overwrite a data file with record_lines, but keep every line that
    could not be read (line_parser returns None for it) at the end,
    unchanged - so a damaged or hand-edited line is never silently
    erased when another record is updated or deleted."""
    old_lines = read_lines(file_path)
    # Before anything is removed, remember the highest ID in the file, so
    # a deleted record's ID can never be given to a new one.
    remember_highest_ids(old_lines)
    unreadable_lines = []
    for line in old_lines:
        if line_parser(line) is None:
            unreadable_lines.append(line)
    write_lines(file_path, record_lines + unreadable_lines)


def read_id_counters():
    """Return a dictionary of prefix -> highest ID number ever used. The
    counter file is optional, so it is checked before reading."""
    counters = {}
    if not os.path.isfile(ID_COUNTER_FILE):
        return counters
    for line in read_lines(ID_COUNTER_FILE):
        fields = line.split("|")
        if len(fields) == 2 and fields[1].isdigit():
            counters[fields[0]] = int(fields[1])
    return counters


def split_record_id(record_id):
    """Split an ID like CLS007 into ("CLS", 7), or None if it isn't one."""
    prefix = ""
    for character in record_id:
        if character.isalpha():
            prefix += character
        else:
            break
    number_text = record_id[len(prefix):]
    if prefix == "" or not number_text.isdigit():
        return None
    return prefix, int(number_text)


def remember_highest_ids(lines):
    """Save, in id_counters.txt, the highest ID number of each prefix found
    at the start of these record lines, if it is higher than the one
    already saved. The file is only written when something changed."""
    counters = read_id_counters()
    changed = False
    for line in lines:
        id_parts = split_record_id(line.split("|")[0])
        if id_parts is None:
            continue
        prefix, number = id_parts
        if number > counters.get(prefix, 0):
            counters[prefix] = number
            changed = True
    if changed:
        counter_lines = []
        for counter_prefix in counters:
            counter_lines.append(f"{counter_prefix}|{counters[counter_prefix]}")
        write_lines(ID_COUNTER_FILE, counter_lines)


def note_used_id(record_id):
    """Record that record_id (e.g. CLS007) has been used, if its number is
    higher than any used before for that prefix."""
    remember_highest_ids([record_id])


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
    """Generate the next ID (e.g. MEM005) for a data file: one more than the
    highest number in the file OR the highest ever used (id_counters.txt),
    whichever is bigger. So deleting the newest record never frees its ID
    for a different record (an old bill could otherwise point at it)."""
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
    highest_number = max(highest_number, read_id_counters().get(prefix, 0))
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


# Malay name connectors stay lower-case, like a/l and s/o.
LOWERCASE_NAME_WORDS = {"bin", "binti", "bt", "bte"}


def format_name(name_text):
    """Tidy a name's capitals word by word: 'ch'ng wei' -> "Ch'ng Wei".
    Words containing '/' (a/l, s/o) and bin/binti are kept lower-case, and extra spaces
    are removed. str.title() is not used because it would turn Ch'ng
    into Ch'Ng."""
    tidy_words = []
    for word in name_text.split():
        if "/" in word or word.lower() in LOWERCASE_NAME_WORDS:
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


def normalize_date(date_text):
    """Return date_text written the standard way, YYYY-MM-DD (so 2027-1-5
    becomes 2027-01-05). Raises ValueError if it is not a real date.
    Saving every date in one form means comparisons and searches on the
    raw text always match."""
    return parse_date(date_text).strftime("%Y-%m-%d")


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
        "CCH001|Lim Wei|0171234567|Badminton|60.00|30.00|ACTIVE",
        "CCH002|Nurul Izzah|0192223344|Tennis|70.00|25.00|ACTIVE",
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
class Record:
    """Base class for a stored record that has an ID (a booking, a class).
    It keeps the ID private with a getter and a validating setter, and
    builds the first part of every data-file line. Booking (booking.py)
    and SportsClass (coaching.py) inherit from it and override to_line()."""

    def __init__(self, record_id):
        """Create the object and validate the ID."""
        self.__record_id = ""
        self.set_record_id(record_id)

    def get_record_id(self):
        """Return the record's ID, e.g. BKG001."""
        return self.__record_id

    def set_record_id(self, record_id):
        """Validate and store the ID (not blank, no | or ; characters)."""
        if record_id.strip() == "" or contains_forbidden_character(record_id):
            raise ValueError("A record ID can't be blank or contain | or ;.")
        self.__record_id = record_id.strip()

    def join_fields(self, other_fields):
        """Return the record's data-file line: its ID first, then the
        other fields (a list of text), separated by |. Child classes call
        this from their own to_line()."""
        return "|".join([self.__record_id] + other_fields)

    def to_line(self):
        """Child classes must override this to build their own line."""
        raise NotImplementedError("Child classes must define to_line().")


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
