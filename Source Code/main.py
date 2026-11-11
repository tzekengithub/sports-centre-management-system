"""
Module      : main.py
Member 1    : Teh Tze Ken (student ID: ________) - Group Leader, integration
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


def build_home_tab(parent, switch_to_tab):
    """Build the Home tab (title, help button and one big button per
    module) inside parent and return its frame. switch_to_tab(name) is
    called when a module button is clicked."""
    home_frame = tk.Frame(parent, bg=common.APP_BG)

    tk.Label(home_frame, text="Sports Centre Management System", font=common.TITLE_FONT,
             bg=common.APP_BG, fg=common.ACCENT_COLOR).pack(pady=(40, 10))
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


def build_window_contents(root_window, start_tab, on_theme_toggle, on_exit):
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

    switch_to_tab(start_tab)
    return theme_button


def main():
    """Build the single main window with its tab bar and run it."""
    is_first_run = common.ensure_data_files_exist()
    common.apply_theme(common.load_theme_choice())

    root_window = tk.Tk()
    root_window.title("Sports Centre Management System")
    common.centre_window(root_window, common.WINDOW_WIDTH,
                         common.WINDOW_HEIGHT + TAB_BAR_HEIGHT)
    root_window.minsize(common.WINDOW_WIDTH, common.WINDOW_HEIGHT + TAB_BAR_HEIGHT)
    window_state = {"theme_button": None}

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
        window_state["theme_button"].config(text=theme_button_text())

    root_window.protocol("WM_DELETE_WINDOW", on_exit)
    common.apply_widget_defaults(root_window)
    window_state["theme_button"] = build_window_contents(root_window, "home", on_theme_toggle, on_exit)

    if is_first_run:
        root_window.after(200, show_welcome_message)

    root_window.mainloop()


if __name__ == "__main__":
    main()
