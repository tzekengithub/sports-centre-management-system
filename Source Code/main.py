"""
Module      : main.py
Author      : Teh Tze Ken (Group Leader - integration)
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
    "booking": "See which courts are free each hour and book them; cancel or delete bookings.",
    "membership": "Register new members, update or delete them, renew memberships.",
    "coaching": "Coaches, classes, enrolment, and each coach's hours and commission.",
    "billing": "Create bills, take payments, view receipts and daily revenue.",
}

# Colours for the selected tab (looks "pressed in", same colour as the
# page below it) and for the other tabs (normal green buttons).
ACTIVE_TAB_BG = common.APP_BG
ACTIVE_TAB_FG = common.ACCENT_COLOR
INACTIVE_TAB_BG = common.BUTTON_COLOR
INACTIVE_TAB_FG = common.BUTTON_TEXT_COLOR

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
    "Sample data is already loaded (members MEM001-MEM004 and so on), "
    "so you can try things straight away."
)


def show_welcome_message():
    """Show the full getting-started message (also shown once
    automatically on a brand new install)."""
    messagebox.showinfo("How to Use This System", WELCOME_MESSAGE)


def build_home_tab(parent, switch_to_tab):
    """Build the Home tab (title, help button and one big button per
    module) inside parent and return its frame. switch_to_tab(name) is
    called when a module button is clicked."""
    home_frame = tk.Frame(parent, bg=common.APP_BG)

    tk.Label(home_frame, text="Sports Centre Management System", font=common.TITLE_FONT,
             bg=common.APP_BG, fg=common.ACCENT_COLOR).pack(pady=(40, 10))
    tk.Label(home_frame, text="Select a module below, or use the tabs along the top",
             font=common.LABEL_FONT, bg=common.APP_BG).pack(pady=(0, 10))
    help_button = tk.Button(home_frame, text="How to Use This System", width=30, font=common.BUTTON_FONT,
                            bg=common.ACCENT_COLOR, fg=common.BUTTON_TEXT_COLOR,
                            command=show_welcome_message)
    help_button.pack(pady=(0, 15))
    common.add_tooltip(help_button, "A short guide to the whole program. Tip: rest the mouse on any "
                                    "button or box to see what it does.")

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
        menu_button = tk.Button(menu_frame, text=item_label, width=30, font=common.BUTTON_FONT,
                                bg=common.BUTTON_COLOR, fg=common.BUTTON_TEXT_COLOR,
                                command=make_menu_command(tab_name))
        menu_button.pack(pady=6)
        common.add_tooltip(menu_button, TAB_TIPS[tab_name])

    return home_frame


def main():
    """Build the single main window with its tab bar and run it."""
    is_first_run = common.ensure_data_files_exist()

    root_window = tk.Tk()
    root_window.title("Sports Centre Management System")
    root_window.configure(bg=common.APP_BG)
    common.centre_window(root_window, common.WINDOW_WIDTH,
                         common.WINDOW_HEIGHT + TAB_BAR_HEIGHT)
    root_window.minsize(common.WINDOW_WIDTH, common.WINDOW_HEIGHT + TAB_BAR_HEIGHT)

    # Tab bar is packed first (side="top") so it always keeps its space
    # above the content area, which expands to fill the rest.
    tab_bar = tk.Frame(root_window, bg=common.BUTTON_COLOR)
    tab_bar.pack(side="top", fill="x")

    content_frame = tk.Frame(root_window, bg=common.APP_BG)
    content_frame.pack(side="top", fill="both", expand=True)

    # Which tab is showing, and its frame, so it can be destroyed on switch.
    tab_state = {"current_tab": None, "current_frame": None}
    tab_buttons = {}

    def switch_to_tab(tab_name):
        """Show tab_name in the content area. The previous tab's frame is
        destroyed and the new one rebuilt from the data files, so every
        tab always shows up-to-date records. Clicking the tab that is
        already showing rebuilds it too, which takes you back to its
        "What would you like to do?" menu."""
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

        # Highlight the selected tab, un-highlight the rest.
        for other_tab_name in TAB_ORDER:
            other_button = tab_buttons[other_tab_name]
            if other_tab_name == tab_name:
                other_button.config(bg=ACTIVE_TAB_BG, fg=ACTIVE_TAB_FG, relief="flat")
            else:
                other_button.config(bg=INACTIVE_TAB_BG, fg=INACTIVE_TAB_FG, relief="flat")

    def make_tab_command(tab_name):
        """Return the command for one tab button: switch to tab_name."""
        def tab_command():
            """Switch to this tab."""
            switch_to_tab(tab_name)
        return tab_command

    for tab_name in TAB_ORDER:
        tab_button = tk.Button(tab_bar, text=TAB_LABELS[tab_name], width=14,
                               font=common.BUTTON_FONT, bd=0, pady=12,
                               bg=INACTIVE_TAB_BG, fg=INACTIVE_TAB_FG,
                               activebackground=ACTIVE_TAB_BG,
                               activeforeground=ACTIVE_TAB_FG,
                               command=make_tab_command(tab_name))
        tab_button.pack(side="left")
        common.add_tooltip(tab_button, TAB_TIPS[tab_name])
        tab_buttons[tab_name] = tab_button

    tk.Button(tab_bar, text="Exit", width=10, font=common.BUTTON_FONT, bd=0, pady=12,
              bg=common.DANGER_COLOR, fg=common.BUTTON_TEXT_COLOR,
              command=root_window.destroy).pack(side="right")
    common.add_tooltip(tab_bar.winfo_children()[-1], "Close the program. Everything is already saved.")

    switch_to_tab("home")

    if is_first_run:
        root_window.after(200, show_welcome_message)

    root_window.mainloop()


if __name__ == "__main__":
    main()
