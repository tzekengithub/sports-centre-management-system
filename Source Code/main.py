"""
Module      : main.py
Member 1    : Teh Tze Ken (student ID: 26PMD03846) - Group Leader, integration
Purpose     : Main entry point - checks the Python version, then builds
              ONE main window with a row of tabs along the top (Home,
              Booking, Membership, Coaching, Billing). Clicking a tab
              swaps the content area to that member's module instead of
              opening a separate window.
Date        : 2026-11-07
"""

import sys

# The other modules (booking.py, membership.py, coaching.py, billing.py)
# use "match" statements, which need Python 3.10+. A file containing
# "match" fails to even parse on an older Python, so this check must run
# and exit BEFORE those modules are imported - it deliberately uses no
# syntax newer than Python 3 here (no "match" in this file), so this file
# itself always parses.
MINIMUM_PYTHON_VERSION = (3, 10)

if sys.version_info < MINIMUM_PYTHON_VERSION:
    import tkinter as tk
    from tkinter import messagebox

    error_window = tk.Tk()
    error_window.withdraw()
    messagebox.showerror(
        "Python Version Too Old",
        "This program needs Python 3.10 or newer (it uses 'match' statements).\n"
        f"You are running Python {sys.version_info.major}.{sys.version_info.minor}.\n"
        "Please install a newer Python and run 'python main.py' again.")
    sys.exit(1)

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import common
import booking
import membership
import coaching
import billing

# Tab order along the top bar (tuple) and the text shown on each tab (dict).
TAB_ORDER = ("home", "booking", "membership", "coaching", "billing")
TAB_LABELS = {
    "home": "Home",
    "booking": "Booking",
    "membership": "Membership",
    "coaching": "Coaching",
    "billing": "Billing",
}

TAB_BAR_HEIGHT = 50

# Hover hints for the tab bar.
TAB_TIPS = {
    "home": "Start page: open a module or read How to Use This System.",
    "booking": "See which courts are free each hour and book them; cancel bookings.",
    "membership": "Register new members, update or delete them, renew memberships.",
    "coaching": "Coaches, classes, enrolment, and each coach's hours and commission.",
    "billing": "Create bills, take payments, view receipts and daily revenue.",
}

EXIT_QUESTION = ("Are you sure you want to exit the Sports Centre Management System?\n\n"
                 "Everything you have saved is kept.")

WELCOME_MESSAGE = (
    "Welcome! This program manages a sports centre's bookings, members, "
    "coaching classes and billing.\n\n"
    "Use the tabs along the top:\n"
    "  - Booking - see which courts are free and book them\n"
    "  - Membership - register people and manage members\n"
    "  - Coaching - coaches, classes, enrolment, hours and commission\n"
    "  - Billing - bills, payments and daily revenue\n\n"
    "Each tab asks what you would like to do. Click an action and it "
    "opens on its own page, with one line telling you what to do. "
    "Click Back (or the tab again) to choose another action.\n\n"
    "Not sure what something does? Rest the mouse on any button, box "
    "or grid square for a moment and a yellow hint explains it.\n\n"
    "Prefer a dark screen? Click Dark Mode at the top right.\n\n"
    "Sample data is already loaded (members MEM001-MEM004 and so on), "
    "so you can try things straight away."
)


def show_welcome_message():
    """Show the full getting-started message (also shown once
    automatically on a brand new install)."""
    messagebox.showinfo("How to Use This System", WELCOME_MESSAGE)


# ---------------------------------------------------------------------------
# HOME HEADER (greeting, ADMIN badge, shortcut buttons, glowing clock card)
# ---------------------------------------------------------------------------
# tkinter has no blur, shadow or rounded corners, so the look is faked with
# Canvas shapes: rounded polygons, a few slightly bigger copies in fading
# colours for a "glow", and text drawn twice for glowing digits. All the
# drawing code for the header is in this one section.

# The ONLY place with its own colours. Page colour comes from common.APP_BG so
# the header always blends into the page; everything else is chosen here, one
# set for Dark Mode and one for Light Mode.
HEADER_PALETTE = {
    "dark": {
        "card": "#262b36", "card_border": "#434b5e", "halo": "#6366f1", "halo_strength": 0.22,
        "text": "#ffffff", "muted": "#94a3b8", "dot": "#22c55e",
        "badge_fill": "#2b3040", "badge_border": "#566077", "badge_text": "#cbd5e1",
        "primary": "#6366f1", "primary_text": "#ffffff", "glow": "#6366f1",
        "button_fill": "#1f2430", "accent_1": "#2dd4bf", "accent_2": "#f472b6",
        "digits": "#c4b5fd", "digits_glow": "#8b5cf6", "colon": "#5b5f86", "ampm": "#a5b4fc",
        "focus": "#e0e7ff",
    },
    "light": {
        "card": "#ffffff", "card_border": "#d3d9e2", "halo": "#6b7280", "halo_strength": 0.10,
        "text": "#1f2328", "muted": "#5b6573", "dot": "#16a34a",
        "badge_fill": "#eef2ff", "badge_border": "#c7d2fe", "badge_text": "#4338ca",
        "primary": "#4f46e5", "primary_text": "#ffffff", "glow": "#6b7280",
        "button_fill": "#ffffff", "accent_1": "#0f766e", "accent_2": "#be185d",
        "digits": "#4338ca", "digits_glow": "#6366f1", "colon": "#a5b4fc", "ampm": "#6366f1",
        "focus": "#312e81",
    },
}

HEADER_GREETING_FONT = ("Segoe UI", 22, "bold")
HEADER_BADGE_FONT = ("Segoe UI", 8, "bold")
HEADER_BUTTON_FONT = ("Segoe UI", 10, "bold")
HEADER_CLOCK_FONT_NAME = "Consolas"  # monospace, so the digits do not jump around
HEADER_CLOCK_SIZE = 30

BUTTON_WIDTH_PX = 164
BUTTON_HEIGHT_PX = 38
BUTTON_MARGIN_PX = 8      # room around a button for its glow
CARD_WIDTH_PX = 344
CARD_HEIGHT_PX = 126
LEFT_WIDTH_PX = 3 * (BUTTON_WIDTH_PX + 2 * BUTTON_MARGIN_PX) + 12

# The three shortcut buttons: (button text, tab to open, page inside that tab,
# symbol, colour key in the palette).
SHORTCUTS = [
    ("Book a Court", "booking", "Book a Court", "", "primary"),
    ("Register Member", "membership", "Register", "\U0001F465", "accent_1"),
    ("Create Bill", "billing", "Create Bill", "\U0001F4B3", "accent_2"),
]

# The header being shown (None when Home is not on screen), so the theme
# button can recolour it.
home_header_state = {"header": None}


def greeting_text(hour):
    """Return the greeting for an hour of the day (0-23)."""
    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"


def clock_text(now):
    """Return the time as HH:MM:SS with AM/PM, e.g. '09:05:03 AM'."""
    return now.strftime("%I:%M:%S %p")


def clock_parts(now):
    """Return the time as (hours, minutes, seconds, 'AM' or 'PM') text."""
    return now.strftime("%I"), now.strftime("%M"), now.strftime("%S"), now.strftime("%p")


def date_text(now):
    """Return the date as 'Wednesday - Nov 11, 2026' (day without a leading zero)."""
    return now.strftime("%A - %b ") + str(now.day) + now.strftime(", %Y")


def timezone_text(now):
    """Return the computer's time zone as 'GMT+8' or 'GMT+5:30' (from the clock's UTC offset)."""
    offset = now.utcoffset()
    if offset is None:
        # A plain datetime has no zone attached: use the computer's own.
        offset = now.astimezone().utcoffset()
    if offset is None:
        return "GMT"
    total_minutes = int(offset.total_seconds() // 60)
    if total_minutes == 0:
        return "GMT"
    if total_minutes < 0:
        sign = "-"
    else:
        sign = "+"
    hours, minutes = divmod(abs(total_minutes), 60)
    if minutes == 0:
        return f"GMT{sign}{hours}"
    return f"GMT{sign}{hours}:{minutes:02d}"


def colour_to_rgb(widget, colour):
    """Return (red, green, blue), each 0-255, for any tk colour name or #rrggbb."""
    red, green, blue = widget.winfo_rgb(colour)
    return red // 257, green // 257, blue // 257


def mix_colour(widget, colour_one, colour_two, fraction):
    """Return #rrggbb: colour_one with fraction (0 to 1) of colour_two mixed in."""
    first = colour_to_rgb(widget, colour_one)
    second = colour_to_rgb(widget, colour_two)
    mixed = []
    for index in range(3):
        mixed.append(int(round(first[index] * (1 - fraction) + second[index] * fraction)))
    return "#%02x%02x%02x" % (mixed[0], mixed[1], mixed[2])


def round_rect(canvas, x1, y1, x2, y2, radius, **options):
    """Draw a rounded rectangle on a canvas (a smooth polygon) and return its item id."""
    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)
    points = [x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
              x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
              x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1]
    return canvas.create_polygon(points, smooth=True, **options)


def draw_halo(canvas, x1, y1, x2, y2, radius, page_colour, glow_colour, strength):
    """Fake a soft glow: three rounded shapes, each a little bigger than the
    last, in colours fading from the page colour towards glow_colour. Drawn
    from the outside in, so the shape itself is drawn on top afterwards."""
    steps = (3, 2, 1)
    for ring in range(3):
        grow = steps[ring] * 2
        fraction = strength * (ring + 1) / 3
        round_rect(canvas, x1 - grow, y1 - grow, x2 + grow, y2 + grow, radius + grow,
                   fill=mix_colour(canvas, page_colour, glow_colour, fraction), outline="")


class PillButton:
    """A rounded button drawn on its own small Canvas. It changes colour on
    hover and press, shows a ring when it has keyboard focus (Tab), and works
    with Enter and Space as well as the mouse."""

    def __init__(self, parent, text, command, symbol, colour_key, tip, get_palette):
        """Create the button canvas; get_palette() returns the current colours."""
        self.__text = text
        self.__command = command
        self.__symbol = symbol
        self.__colour_key = colour_key
        self.__get_palette = get_palette
        self.__state = "normal"
        self.__focused = False
        width = BUTTON_WIDTH_PX + 2 * BUTTON_MARGIN_PX
        height = BUTTON_HEIGHT_PX + 2 * BUTTON_MARGIN_PX
        self.canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bd=0,
                                bg=common.APP_BG, cursor="hand2", takefocus=1)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<FocusIn>", self.on_focus_in)
        self.canvas.bind("<FocusOut>", self.on_focus_out)
        self.canvas.bind("<Return>", self.on_key)
        self.canvas.bind("<space>", self.on_key)
        common.add_tooltip(self.canvas, tip)
        self.draw()

    def get_text(self):
        """Return the button's text."""
        return self.__text

    def draw(self):
        """Draw (or redraw) the whole button with the current palette and state."""
        canvas = self.canvas
        palette = self.__get_palette()
        page = common.APP_BG
        canvas.delete("all")
        canvas.config(bg=page)
        x1, y1 = BUTTON_MARGIN_PX, BUTTON_MARGIN_PX
        x2, y2 = x1 + BUTTON_WIDTH_PX, y1 + BUTTON_HEIGHT_PX
        radius = BUTTON_HEIGHT_PX // 2
        colour = palette[self.__colour_key]
        if self.__colour_key == "primary":
            # Filled button with a glow (Dark Mode) or a faint shadow (Light Mode).
            draw_halo(canvas, x1, y1, x2, y2, radius, page, palette["glow"], palette["halo_strength"] * 1.6)
            fill = colour
            if self.__state == "hover":
                fill = mix_colour(canvas, colour, "#ffffff", 0.14)
            elif self.__state == "press":
                fill = mix_colour(canvas, colour, "#000000", 0.2)
            round_rect(canvas, x1, y1, x2, y2, radius, fill=fill, outline="")
            text_colour = palette["primary_text"]
        else:
            # Dark button with a thin coloured border and coloured text.
            fill = palette["button_fill"]
            if self.__state == "hover":
                fill = mix_colour(canvas, fill, colour, 0.18)
            elif self.__state == "press":
                fill = mix_colour(canvas, fill, colour, 0.32)
            round_rect(canvas, x1 + 1, y1 + 1, x2 - 1, y2 - 1, radius - 1, fill=fill, outline=colour, width=2)
            text_colour = colour
        label = self.__text
        if self.__symbol != "":
            label = self.__symbol + "  " + self.__text
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=label, fill=text_colour,
                           font=HEADER_BUTTON_FONT)
        if self.__focused:
            round_rect(canvas, x1 - 3, y1 - 3, x2 + 3, y2 + 3, radius + 3, fill="",
                       outline=palette["focus"], width=2)

    def set_state(self, new_state):
        """Remember normal / hover / press and redraw if it changed."""
        if new_state != self.__state:
            self.__state = new_state
            self.draw()

    def on_enter(self, event):
        """Mouse over the button."""
        self.set_state("hover")

    def on_leave(self, event):
        """Mouse left the button."""
        self.set_state("normal")

    def on_press(self, event):
        """Mouse button pushed down on the button."""
        self.canvas.focus_set()
        self.set_state("press")

    def on_release(self, event):
        """Mouse button released: run the command if the pointer is still on the button."""
        inside = 0 <= event.x < self.canvas.winfo_width() and 0 <= event.y < self.canvas.winfo_height()
        self.set_state("hover")
        if inside:
            self.invoke()

    def on_focus_in(self, event):
        """Keyboard focus arrived (Tab): show the ring."""
        self.__focused = True
        self.draw()

    def on_focus_out(self, event):
        """Keyboard focus left: hide the ring."""
        self.__focused = False
        self.draw()

    def on_key(self, event):
        """Enter or Space pressed while the button has focus."""
        self.invoke()

    def invoke(self):
        """Run the button's command (also used by tests)."""
        self.__command()


class HomeHeader:
    """The Home page's top part: greeting row, welcome line, three shortcut
    buttons and the clock card. On a wide window the clock card sits to the
    right; on a narrow one it drops below the text."""

    def __init__(self, parent, switch_to_tab):
        """Build the header inside parent (the Home frame)."""
        self.__switch_to_tab = switch_to_tab
        self.__greeting = ""
        self.__tz_text = ""
        self.__clock_items = {}
        self.__slots = {}
        self.frame = tk.Frame(parent, bg=common.APP_BG)
        self.frame.columnconfigure(0, weight=1)
        self.frame.bind("<Configure>", self.on_resized)

        self.left_side = tk.Frame(self.frame, bg=common.APP_BG)
        self.text_canvas = tk.Canvas(self.left_side, width=LEFT_WIDTH_PX, height=82, highlightthickness=0,
                                     bd=0, bg=common.APP_BG)
        self.text_canvas.pack(side="top", anchor="w")
        self.button_row = tk.Frame(self.left_side, bg=common.APP_BG)
        self.button_row.pack(side="top", anchor="w")
        self.buttons = {}
        for button_text, tab_name, page_name, symbol, colour_key in SHORTCUTS:
            button = PillButton(self.button_row, button_text,
                                self.make_shortcut_command(tab_name, page_name), symbol, colour_key,
                                f"Open the {button_text} page.", self.palette)
            button.canvas.pack(side="left")
            self.buttons[button_text] = button

        self.clock_canvas = tk.Canvas(self.frame, width=CARD_WIDTH_PX, height=CARD_HEIGHT_PX,
                                      highlightthickness=0, bd=0, bg=common.APP_BG)
        self.layout_wide = None
        self.relayout(1000)
        self.draw_all()

    def palette(self):
        """Return the colour set for the theme that is showing now."""
        return HEADER_PALETTE[common.current_theme["name"]]

    def make_shortcut_command(self, tab_name, page_name):
        """Return the command for one shortcut: open that page of that tab."""
        def shortcut_command():
            """Switch to the tab and open the page, as if clicked by hand."""
            self.__switch_to_tab(tab_name, page_name)
        return shortcut_command

    def on_resized(self, event):
        """The header was resized: move the clock card if the room changed."""
        self.relayout(event.width)

    def relayout(self, width):
        """Put the clock card beside the text when there is room, else below it."""
        wide = width >= LEFT_WIDTH_PX + CARD_WIDTH_PX + 30
        if wide == self.layout_wide:
            return
        self.layout_wide = wide
        self.left_side.grid(row=0, column=0, sticky="w")
        if wide:
            self.clock_canvas.grid(row=0, column=1, sticky="e", padx=(10, 0))
        else:
            self.clock_canvas.grid(row=1, column=0, sticky="w", pady=(6, 0))

    def apply_theme(self):
        """Redraw every part in the colours of the current theme (Dark/Light button)."""
        self.draw_all()

    def draw_all(self):
        """Redraw the text canvas, the buttons and the clock card, then show the time."""
        for canvas in (self.frame, self.left_side, self.button_row):
            canvas.config(bg=common.APP_BG)
        self.draw_text()
        for button in self.buttons.values():
            button.draw()
        self.draw_clock_card()
        self.show_time(datetime.now(), True)

    def draw_text(self):
        """Draw the status dot, greeting, ADMIN badge and welcome line."""
        canvas = self.text_canvas
        palette = self.palette()
        canvas.delete("all")
        canvas.config(bg=common.APP_BG)
        canvas.create_oval(BUTTON_MARGIN_PX + 2, 21, BUTTON_MARGIN_PX + 12, 31,
                           fill=palette["dot"], outline=mix_colour(canvas, common.APP_BG, palette["dot"], 0.4),
                           width=3)
        greeting_id = canvas.create_text(BUTTON_MARGIN_PX + 24, 26, text=self.__greeting, anchor="w",
                                         fill=palette["text"], font=HEADER_GREETING_FONT)
        box = canvas.bbox(greeting_id)
        badge_x = box[2] + 14
        round_rect(canvas, badge_x, 14, badge_x + 78, 38, 12, fill=palette["badge_fill"],
                   outline=palette["badge_border"])
        canvas.create_text(badge_x + 39, 26, text="★  ADMIN", fill=palette["badge_text"],
                           font=HEADER_BADGE_FONT)
        canvas.create_text(BUTTON_MARGIN_PX + 2, 62, anchor="w", fill=palette["muted"], font=common.LABEL_FONT,
                           text="Welcome to the Sports Centre Management System")

    def draw_clock_card(self):
        """Draw the clock card: halo, rounded card, glowing HH : MM : SS, AM/PM,
        and the date line with the time zone. The text items are kept so each
        second only changes their text."""
        canvas = self.clock_canvas
        palette = self.palette()
        page = common.APP_BG
        canvas.delete("all")
        canvas.config(bg=page)
        self.__clock_items = {}
        x1, y1 = 12, 12
        x2, y2 = CARD_WIDTH_PX - 12, CARD_HEIGHT_PX - 12
        draw_halo(canvas, x1, y1, x2, y2, 20, page, palette["halo"], palette["halo_strength"])
        round_rect(canvas, x1, y1, x2, y2, 20, fill=palette["card"], outline=palette["card_border"])

        digit_font = (HEADER_CLOCK_FONT_NAME, HEADER_CLOCK_SIZE, "bold")
        halo_font = (HEADER_CLOCK_FONT_NAME, HEADER_CLOCK_SIZE + 3, "bold")
        wide_font = (HEADER_CLOCK_FONT_NAME, HEADER_CLOCK_SIZE + 7, "bold")
        ampm_font = (HEADER_CLOCK_FONT_NAME, 11, "bold")
        # Measure one pair of digits and one colon so the slots are fixed (no jumping).
        probe = canvas.create_text(0, 0, text="00", font=digit_font)
        box = canvas.bbox(probe)
        pair_width = box[2] - box[0]
        canvas.itemconfig(probe, text=":")
        box = canvas.bbox(probe)
        colon_width = box[2] - box[0] + 2
        canvas.delete(probe)
        ampm_width = 34
        total = 3 * pair_width + 2 * colon_width + 8 + ampm_width
        start = (x1 + x2) / 2 - total / 2
        row_y = 52
        slot_x = {}
        position = start
        for name in ("hh", "c1", "mm", "c2", "ss"):
            if name.startswith("c"):
                width = colon_width
            else:
                width = pair_width
            slot_x[name] = position + width / 2
            position += width
        slot_x["ampm"] = position + 8 + ampm_width / 2

        for name in ("hh", "mm", "ss"):
            # Two dim, bigger copies behind the bright digits = glow.
            if common.current_theme["name"] == "dark":
                outer = canvas.create_text(slot_x[name], row_y, text="00", font=wide_font,
                                           fill=mix_colour(canvas, palette["card"], palette["digits_glow"], 0.16))
                inner = canvas.create_text(slot_x[name], row_y, text="00", font=halo_font,
                                           fill=mix_colour(canvas, palette["card"], palette["digits_glow"], 0.38))
            else:
                outer = None
                inner = canvas.create_text(slot_x[name] + 1, row_y + 2, text="00", font=digit_font,
                                           fill=mix_colour(canvas, palette["card"], palette["digits_glow"], 0.18))
            bright = canvas.create_text(slot_x[name], row_y, text="00", font=digit_font, fill=palette["digits"])
            self.__clock_items[name] = (outer, inner, bright)
        for name in ("c1", "c2"):
            canvas.create_text(slot_x[name], row_y - 2, text=":", font=digit_font, fill=palette["colon"])
        ampm_glow = canvas.create_text(slot_x["ampm"], row_y + 6, text="", font=(HEADER_CLOCK_FONT_NAME, 12, "bold"),
                                       fill=mix_colour(canvas, palette["card"], palette["ampm"], 0.3))
        ampm_main = canvas.create_text(slot_x["ampm"], row_y + 6, text="", font=ampm_font, fill=palette["ampm"])
        self.__clock_items["ampm"] = (None, ampm_glow, ampm_main)

        # Date on the left, a small time-zone pill on the right.
        date_id = canvas.create_text(x1 + 18, 94, text="", anchor="w", font=common.LABEL_FONT,
                                     fill=palette["muted"])
        self.__clock_items["date"] = (None, None, date_id)
        zone_id = canvas.create_text(x2 - 18, 94, text=self.__tz_text, anchor="e", font=("Segoe UI", 8, "bold"),
                                     fill=palette["muted"])
        self.__clock_items["zone"] = (None, None, zone_id)

    def set_item_text(self, name, text):
        """Change the text of a clock item (and its glow copies) without redrawing."""
        for item_id in self.__clock_items[name]:
            if item_id is not None:
                self.clock_canvas.itemconfig(item_id, text=text)

    def show_time(self, now, force=False):
        """Show the time, date and greeting for 'now'. Only text items change
        every second; the left side is redrawn only when the greeting changes."""
        greeting = greeting_text(now.hour)
        zone = timezone_text(now)
        if force or zone != self.__tz_text:
            self.__tz_text = zone
            self.clock_canvas.itemconfig(self.__clock_items["zone"][2], text=zone)
        if greeting != self.__greeting:
            self.__greeting = greeting
            self.draw_text()
        hours, minutes, seconds, ampm = clock_parts(now)
        self.set_item_text("hh", hours)
        self.set_item_text("mm", minutes)
        self.set_item_text("ss", seconds)
        self.set_item_text("ampm", ampm)
        self.set_item_text("date", date_text(now))

    def item_count(self):
        """Return how many items the header canvases hold (tests check it does not grow)."""
        total = len(self.text_canvas.find_all()) + len(self.clock_canvas.find_all())
        for button in self.buttons.values():
            total += len(button.canvas.find_all())
        return total


def start_clock(home_frame, header):
    """Show the time now, then again every second until home_frame is
    destroyed (a tab switch or closing the program)."""
    clock_state = {"job": None}

    def refresh_clock():
        """Update the header's clock and schedule the next update."""
        try:
            if not home_frame.winfo_exists():
                return
            header.show_time(datetime.now())
            clock_state["job"] = home_frame.after(1000, refresh_clock)
        except tk.TclError:
            # The window was closed between two ticks: nothing left to update.
            clock_state["job"] = None

    def stop_clock(event):
        """Cancel the pending tick when the Home page is destroyed."""
        if event.widget is not home_frame:
            return
        home_header_state["header"] = None
        if clock_state["job"] is None:
            return
        try:
            home_frame.after_cancel(clock_state["job"])
        except tk.TclError:
            pass
        clock_state["job"] = None

    home_frame.bind("<Destroy>", stop_clock, add="+")
    refresh_clock()


def build_home_header(home_frame, switch_to_tab):
    """Build the top of the Home page (see HomeHeader), start its clock and
    return it. The theme button recolours it through home_header_state."""
    header = HomeHeader(home_frame, switch_to_tab)
    header.frame.pack(side="top", fill="x", padx=30, pady=(8, 0))
    home_header_state["header"] = header
    start_clock(home_frame, header)
    return header


def build_home_tab(parent, switch_to_tab):
    """Build the Home tab (greeting header, title, help button and one big
    button per module) inside parent and return its frame. switch_to_tab(name)
    is called when a module button is clicked."""
    home_frame = tk.Frame(parent, bg=common.APP_BG)

    build_home_header(home_frame, switch_to_tab)

    tk.Label(home_frame, text="Sports Centre Management System", font=common.TITLE_FONT,
             bg=common.APP_BG, fg=common.ACCENT_COLOR).pack(pady=(16, 6))
    tk.Label(home_frame, text="Select a module below, or use the tabs along the top",
             font=common.LABEL_FONT, bg=common.APP_BG).pack(pady=(0, 10))
    help_button = common.make_button(home_frame, "How to Use This System", show_welcome_message, width=30,
                                     tip="A short guide to the whole program. Tip: rest the mouse on any "
                                         "button or box to see what it does.")
    help_button.pack(pady=(0, 15))

    menu_frame = tk.Frame(home_frame, bg=common.APP_BG)
    menu_frame.pack(pady=10)

    def make_menu_command(tab_name):
        """Return the command for one Home-tab button: switch to tab_name."""
        def menu_command():
            """Switch to this menu button's tab."""
            switch_to_tab(tab_name)
        return menu_command

    menu_items = [
        ("Facility & Court Booking", "booking"),
        ("Membership Registration", "membership"),
        ("Coaching & Class Management", "coaching"),
        ("Billing, Payments & Finance", "billing"),
    ]

    for item_label, tab_name in menu_items:
        common.make_button(menu_frame, item_label, make_menu_command(tab_name), width=30,
                           tip=TAB_TIPS[tab_name]).pack(pady=6)

    return home_frame


def theme_button_text():
    """Return the label for the theme button: the mode you would switch TO."""
    if common.current_theme["name"] == "dark":
        return "☀ Light Mode"
    return "☾ Dark Mode"


def theme_tip():
    """Return the hover hint for the theme button (follows the current theme)."""
    if common.current_theme["name"] == "dark":
        return "Switch back to the light colours. Your choice is remembered next time."
    return "Switch to dark colours, easier on the eyes at night. Your choice is remembered next time."


def build_window_contents(root_window, start_tab, on_theme_toggle, on_exit, on_zoom_in, on_zoom_out):
    """Build the tab bar and content area inside root_window using the
    current theme's colours, and show start_tab. Returns the theme button,
    so its label can be changed when the theme is switched (the rest of
    the window is recoloured in place, not rebuilt)."""
    # Selected tab looks "pressed in" (same colour as the page below it);
    # the other tabs are normal buttons. Read when used, not at import
    # time, so they follow the current theme.
    active_tab_bg = common.APP_BG
    active_tab_fg = common.ACCENT_COLOR
    inactive_tab_bg = common.BUTTON_COLOR
    inactive_tab_fg = common.BUTTON_TEXT_COLOR

    root_window.configure(bg=common.APP_BG)

    # Tab bar is packed first (side="top") so it always keeps its space
    # above the content area, which expands to fill the rest.
    tab_bar = tk.Frame(root_window, bg=common.BUTTON_COLOR)
    tab_bar.pack(side="top", fill="x")

    content_frame = tk.Frame(root_window, bg=common.APP_BG)
    content_frame.pack(side="top", fill="both", expand=True)

    # Which tab is showing, and its frame, so it can be destroyed on switch.
    tab_state = {"current_tab": None, "current_frame": None}
    tab_buttons = {}

    def switch_to_tab(tab_name, page_name=None):
        """Show tab_name in the content area. The previous tab's frame is
        destroyed and the new one rebuilt from the data files, so every
        tab always shows up-to-date records. Clicking the tab that is
        already showing rebuilds it too, which takes you back to its
        "What would you like to do?" menu. With page_name given, that
        page of the tab is opened straight away (Home shortcut buttons)."""
        if tab_state["current_frame"] is not None:
            tab_state["current_frame"].destroy()

        # if/elif instead of match, so this file still parses on old
        # Python and the version check above can run.
        if tab_name == "home":
            new_frame = build_home_tab(content_frame, switch_to_tab)
        elif tab_name == "booking":
            new_frame = booking.build_booking_tab(content_frame)
        elif tab_name == "membership":
            new_frame = membership.build_membership_tab(content_frame)
        elif tab_name == "coaching":
            new_frame = coaching.build_coaching_tab(content_frame)
        elif tab_name == "billing":
            new_frame = billing.build_billing_tab(content_frame)
        else:
            messagebox.showerror("Unknown Option", "This menu option is not recognised.")
            return

        new_frame.pack(fill="both", expand=True)
        tab_state["current_tab"] = tab_name
        tab_state["current_frame"] = new_frame
        if page_name is not None:
            # Uses the same open-page function as that tab's own menu button.
            new_frame.open_action_page(page_name)

        # Highlight the selected tab, un-highlight the rest (using the
        # colours of the theme that is showing now).
        for other_tab_name in TAB_ORDER:
            other_button = tab_buttons[other_tab_name]
            if other_tab_name == tab_name:
                other_button.config(bg=common.APP_BG, fg=common.ACCENT_COLOR, relief="flat",
                                    activebackground=common.APP_BG, activeforeground=common.ACCENT_COLOR)
            else:
                other_button.config(bg=common.BUTTON_COLOR, fg=common.BUTTON_TEXT_COLOR, relief="flat",
                                    activebackground=common.APP_BG, activeforeground=common.ACCENT_COLOR)

    def make_tab_command(tab_name):
        """Return the command for one tab button: switch to tab_name."""
        def tab_command():
            """Switch to this tab."""
            switch_to_tab(tab_name)
        return tab_command

    for tab_name in TAB_ORDER:
        tab_button = tk.Button(tab_bar, text=TAB_LABELS[tab_name], width=12,
                               font=common.BUTTON_FONT, bd=0, pady=12,
                               bg=inactive_tab_bg, fg=inactive_tab_fg,
                               activebackground=active_tab_bg,
                               activeforeground=active_tab_fg,
                               command=make_tab_command(tab_name))
        tab_button.pack(side="left")
        common.add_tooltip(tab_button, TAB_TIPS[tab_name])
        tab_buttons[tab_name] = tab_button

    exit_button = tk.Button(tab_bar, text="Exit", width=8, font=common.BUTTON_FONT, bd=0, pady=12,
                            bg=common.DANGER_COLOR, fg=common.BUTTON_TEXT_COLOR,
                            activebackground=common.DANGER_COLOR, activeforeground=common.BUTTON_TEXT_COLOR,
                            command=on_exit)
    exit_button.pack(side="right")
    common.add_tooltip(exit_button, "Close the program (you will be asked to confirm). "
                                    "Everything is already saved.")

    theme_button = tk.Button(tab_bar, text=theme_button_text(), width=13, font=common.BUTTON_FONT, bd=0, pady=12,
                             bg=inactive_tab_bg, fg=inactive_tab_fg, activebackground=active_tab_bg,
                             activeforeground=active_tab_fg, command=on_theme_toggle)
    theme_button.pack(side="right")
    common.add_tooltip(theme_button, theme_tip)

    # Record-zoom buttons (right of the theme button): they make ONLY the
    # record rows (ID, name, type ...) bigger or smaller. Ctrl + mouse wheel
    # and Ctrl + / Ctrl - / Ctrl 0 do the same, see main().
    zoom_in_button = tk.Button(tab_bar, text="A+", width=4, font=common.BUTTON_FONT, bd=0, pady=12,
                               bg=inactive_tab_bg, fg=inactive_tab_fg, activebackground=active_tab_bg,
                               activeforeground=active_tab_fg, command=on_zoom_in)
    zoom_in_button.pack(side="right")
    common.add_tooltip(zoom_in_button, "Zoom in on the records: make the rows in the lists "
                                       "(ID, name, type ...) bigger. Everything else stays the same size. "
                                       "Shortcut: Ctrl + mouse wheel up, or Ctrl and +.")
    zoom_out_button = tk.Button(tab_bar, text="A-", width=4, font=common.BUTTON_FONT, bd=0, pady=12,
                                bg=inactive_tab_bg, fg=inactive_tab_fg, activebackground=active_tab_bg,
                                activeforeground=active_tab_fg, command=on_zoom_out)
    zoom_out_button.pack(side="right")
    common.add_tooltip(zoom_out_button, "Zoom out on the records: make the rows in the lists smaller again. "
                                        "Shortcut: Ctrl + mouse wheel down, or Ctrl and -.")

    switch_to_tab(start_tab)
    return theme_button


def main():
    """Build the single main window with its tab bar and run it."""
    is_first_run = common.ensure_data_files_exist()
    common.apply_theme(common.load_theme_choice())
    common.apply_record_zoom(common.load_record_zoom())

    root_window = tk.Tk()
    root_window.title("Sports Centre Management System")
    window_state = {"theme_button": None}

    def window_size_for(zoom_percent):
        """Return (width, height) of the window at a record zoom. Only the
        list part of a page needs more room for bigger rows, so the window
        gets wider by that part's share; the height stays the same."""
        width = common.WINDOW_WIDTH + common.LIST_AREA_WIDTH * (zoom_percent - 100) // 100
        height = common.WINDOW_HEIGHT + TAB_BAR_HEIGHT
        return width, height

    def zoom_fits_screen(zoom_percent):
        """True if the window at this zoom fits across this screen. A bigger
        zoom would cut the rows off, so it isn't offered (a small laptop
        screen just has fewer zoom levels than a big monitor)."""
        width, height = window_size_for(zoom_percent)
        return width <= root_window.winfo_screenwidth() - 40

    def fit_window_to_zoom():
        """Resize and centre the window for the current record zoom."""
        width, height = window_size_for(common.record_zoom["percent"])
        root_window.minsize(common.WINDOW_WIDTH, height)
        common.centre_window(root_window, width, height)

    def change_zoom(step):
        """Move one record-zoom level up (step 1) or down (step -1), or back
        to 100% (step 0). Only the record rows are resized, in place, so the
        page stays as it is."""
        old_percent = common.record_zoom["percent"]
        if step == 0:
            new_percent = 100
        else:
            new_index = common.RECORD_ZOOM_LEVELS.index(old_percent) + step
            if new_index < 0 or new_index >= len(common.RECORD_ZOOM_LEVELS):
                return
            new_percent = common.RECORD_ZOOM_LEVELS[new_index]
        if new_percent == old_percent or not zoom_fits_screen(new_percent):
            return
        common.apply_record_zoom(new_percent)
        common.rezoom_records(root_window)
        fit_window_to_zoom()
        try:
            common.save_record_zoom(new_percent)
        except OSError:
            # Not being able to remember the zoom is not worth an error box.
            pass

    def on_zoom_in():
        """Zoom in one level."""
        change_zoom(1)

    def on_zoom_out():
        """Zoom out one level."""
        change_zoom(-1)

    def on_key_zoom_in(event):
        """Ctrl and + (or =) zoom in."""
        change_zoom(1)

    def on_key_zoom_out(event):
        """Ctrl and - zoom out."""
        change_zoom(-1)

    def on_key_zoom_reset(event):
        """Ctrl and 0 go back to normal size."""
        change_zoom(0)

    def on_ctrl_wheel(event):
        """Ctrl + mouse wheel: up zooms in, down zooms out."""
        if event.delta > 0:
            change_zoom(1)
        else:
            change_zoom(-1)

    def on_exit():
        """Ask before closing - used by the Exit tab AND the window's X."""
        if messagebox.askyesno("Exit", EXIT_QUESTION, icon="warning"):
            root_window.destroy()

    def on_theme_toggle():
        """Switch light <-> dark and remember the choice. Every widget is
        recoloured in place, so you stay on the same tab and page with
        whatever you had typed or selected."""
        old_theme = common.current_theme["name"]
        if old_theme == "dark":
            new_theme = "light"
        else:
            new_theme = "dark"
        common.apply_theme(new_theme)
        try:
            common.save_theme_choice(new_theme)
        except OSError:
            # Not being able to remember the choice is not worth an error box.
            pass
        common.recolour_widgets(root_window, old_theme, new_theme)
        common.apply_widget_defaults(root_window)
        if home_header_state["header"] is not None:
            # The Home header is drawn on canvases, so it is redrawn in the new colours.
            try:
                home_header_state["header"].apply_theme()
            except tk.TclError:
                pass
        window_state["theme_button"].config(text=theme_button_text())

    # A zoom saved on a bigger screen may not fit this one: use the biggest that does.
    while common.record_zoom["percent"] > 100 and not zoom_fits_screen(common.record_zoom["percent"]):
        common.apply_record_zoom(common.RECORD_ZOOM_LEVELS[
            common.RECORD_ZOOM_LEVELS.index(common.record_zoom["percent"]) - 1])

    root_window.protocol("WM_DELETE_WINDOW", on_exit)
    common.apply_widget_defaults(root_window)
    window_state["theme_button"] = build_window_contents(root_window, "home", on_theme_toggle, on_exit,
                                                         on_zoom_in, on_zoom_out)
    fit_window_to_zoom()
    root_window.bind_all("<Control-MouseWheel>", on_ctrl_wheel)
    root_window.bind_all("<Control-plus>", on_key_zoom_in)
    root_window.bind_all("<Control-equal>", on_key_zoom_in)
    root_window.bind_all("<Control-minus>", on_key_zoom_out)
    root_window.bind_all("<Control-Key-0>", on_key_zoom_reset)

    if is_first_run:
        root_window.after(200, show_welcome_message)

    root_window.mainloop()


if __name__ == "__main__":
    main()
