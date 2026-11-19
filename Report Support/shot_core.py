"""Shared helpers for take_screenshots_real.py: starts the REAL program from a
temporary copy of Source Code (so the real data is never touched), finds
widgets, and captures the REAL screen, including the real Windows message
boxes. Nothing here draws or fakes a picture: every image is PIL.ImageGrab.
This file is a tool for the report; it is not part of the submitted program."""

import ctypes
import ctypes.wintypes as wt
import json
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
SOURCE = os.path.join(PROJECT, "Source Code")
OUT_DIR = os.path.join(HERE, "Screenshots_Real")

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, OSError):
    pass

user32 = ctypes.windll.user32
WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
ENUM_PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)


GA_ROOT = 2


def top_handle(root):
    """The Win32 handle of the program's own window."""
    return user32.GetParent(root.winfo_id()) or root.winfo_id()


def ensure_front(hwnd, box):
    """Bring the program window to the very front and check (with
    WindowFromPoint) that it really is what is on screen at its top-left.
    Returns True if verified."""
    point_x, point_y = box[0] + 60, box[1] + 12
    for _attempt in range(8):
        user32.ShowWindow(hwnd, 9)
        user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.25)
        at_point = user32.WindowFromPoint(wt.POINT(point_x, point_y))
        if user32.GetAncestor(at_point, GA_ROOT) == hwnd:
            return True
    return False



def make_temp_copy():
    """Copy Source Code to a temp folder, without data and __pycache__."""
    temp_root = tempfile.mkdtemp(prefix="sports_shots_")
    target = os.path.join(temp_root, "src")
    shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns("data", "__pycache__", "*.pyc"))
    return temp_root, target


# ---------------------------------------------------------------- Win32
def window_text(hwnd):
    """Return a Win32 window's text."""
    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 2)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def class_name(hwnd):
    """Return a Win32 window's class name."""
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buffer, 255)
    return buffer.value


def window_rect(hwnd):
    """Return (left, top, right, bottom) of a window in screen pixels."""
    rect = wt.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


def find_dialogs():
    """Return the handles of all visible message boxes (class #32770)."""
    found = []

    def visit(hwnd, _lparam):
        if class_name(hwnd) == "#32770" and user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    user32.EnumWindows(ENUM_PROC(visit), 0)
    return found


def dialog_parts(dialog):
    """Return (title, message text, {button text: handle}) of a message box."""
    texts = []
    buttons = {}

    def visit(hwnd, _lparam):
        name = class_name(hwnd)
        text = window_text(hwnd)
        if name == "Static" and text.strip() != "":
            texts.append(text)
        elif name == "Button":
            buttons[text.replace("&", "").strip().lower()] = hwnd
        return True

    user32.EnumChildWindows(dialog, ENUM_PROC(visit), 0)
    return window_text(dialog), "\n".join(texts), buttons


def press_button(dialog, answer):
    """Click the dialog's button like a user would ('yes', 'no', 'ok')."""
    title, message, buttons = dialog_parts(dialog)
    if answer in buttons:
        user32.PostMessageW(buttons[answer], BM_CLICK, 0, 0)
    elif len(buttons) > 0:
        user32.PostMessageW(list(buttons.values())[0], BM_CLICK, 0, 0)
    else:
        user32.PostMessageW(dialog, WM_CLOSE, 0, 0)


# ---------------------------------------------------------------- widgets
def walk(widget):
    """Yield a widget and everything inside it (not other windows)."""
    import tkinter as tk
    yield widget
    for child in widget.winfo_children():
        if not isinstance(child, tk.Toplevel):
            yield from walk(child)


def shown(widget):
    """True when the widget and every ancestor are laid out (CLAUDE.md rule)."""
    import tkinter as tk
    while widget is not None:
        if widget.winfo_manager() == "" and not isinstance(widget, (tk.Tk, tk.Toplevel)):
            return False
        widget = widget.master
    return True


def visible(root, kind):
    """All laid-out widgets of one class."""
    root.update()
    found = []
    for widget in walk(root):
        if isinstance(widget, kind) and shown(widget):
            found.append(widget)
    return found


class Shooter:
    """Takes real screenshots of the running window and of real pop-ups."""

    def __init__(self, root):
        import tkinter as tk
        self.tk = tk
        self.root = root
        self.results = []      # (file, size, status, note)
        self.boxes = {}        # file -> {"target": [x, y, w, h], "window": [x, y]}
        self.popup_texts = {}  # file -> (title, message)
        self.warnings = []
        self.front_ok = True
        os.makedirs(OUT_DIR, exist_ok=True)

    # -- placing the window
    def place(self):
        """Put the window in the middle of the screen (where Windows puts message boxes), in front and focused."""
        self.root.update_idletasks()
        centre_x = max(0, (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2)
        centre_y = max(0, (self.root.winfo_screenheight() - self.root.winfo_height()) // 2 - 30)
        self.root.geometry(f"+{centre_x}+{centre_y}")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.focus_force()
        self.root.update()
        self.front_ok = ensure_front(top_handle(self.root), self.window_box())
        if not self.front_ok:
            self.warnings.append("program window could not be brought to the front")

    def window_box(self):
        """Screen rectangle of the program window (client area)."""
        self.root.update_idletasks()
        left = self.root.winfo_rootx()
        top = self.root.winfo_rooty()
        return left, top, left + self.root.winfo_width(), top + self.root.winfo_height()

    # -- saving and checking
    def save(self, image, name, target=None, note=""):
        """Save an image, check it is not blank, and record the result."""
        from PIL import ImageStat
        path = os.path.join(OUT_DIR, name)
        image.save(path)
        stat = ImageStat.Stat(image.convert("L"))
        ok = image.width > 400 and image.height > 300 and stat.mean[0] > 25
        self.results.append((name, f"{image.width}x{image.height}", "PASS" if ok else "FAIL", note))
        if target is not None:
            self.boxes[name] = self.target_box(target)
        return ok

    def target_box(self, widget):
        """Where a widget is on screen, relative to the saved picture."""
        left, top, _right, _bottom = self.window_box()
        return {"x": widget.winfo_rootx() - left, "y": widget.winfo_rooty() - top,
                "w": widget.winfo_width(), "h": widget.winfo_height()}

    def shot(self, name, target=None, note=""):
        """Real screenshot of the program window."""
        from PIL import ImageGrab
        self.place()
        self.root.update()
        import time
        time.sleep(0.25)
        self.root.update()
        image = ImageGrab.grab(bbox=self.window_box(), all_screens=True)
        ok = self.save(image, name, target, note)
        if not self.front_ok:
            self.results[-1] = (name, self.results[-1][1], "FAIL", "program window was not in front")
        return ok

    # -- real pop-ups
    def run_with_popups(self, action, plan, target=None):
        """Run action() (which opens real message boxes). plan is a list of
        (answer, file name or None). A helper thread watches for real dialogs
        (a native message box blocks Tk, so Tk timers can't be trusted), grabs
        the screen with the program window AND the dialog, then clicks the
        button like a user. Returns the (title, message) texts seen."""
        import threading
        import time
        from PIL import ImageGrab
        state = {"seen": [], "stop": False}
        self.place()
        window = self.window_box()
        window_handle = top_handle(self.root)
        if target is not None:
            target_info = self.target_box(target)
        else:
            target_info = None
        shooter = self

        def watch():
            index = 0
            while not state["stop"]:
                dialogs = find_dialogs()
                if len(dialogs) == 0:
                    time.sleep(0.1)
                    continue
                dialog = dialogs[0]
                time.sleep(0.5)
                if not user32.IsWindow(dialog):
                    continue
                title, message, _buttons = dialog_parts(dialog)
                answer, name = "ok", None
                if index < len(plan):
                    answer, name = plan[index]
                index += 1
                state["seen"].append((title, message))
                if name is not None:
                    ensure_front(window_handle, window)
                    dl, dt, dr, db = window_rect(dialog)
                    box = (min(window[0], dl), min(window[1], dt), max(window[2], dr), max(window[3], db))
                    if (box[2] - box[0]) * (box[3] - box[1]) > 12000000 or box[0] < -50 or box[1] < -50:
                        box = (dl, dt, dr, db)  # dialog far from the window: take the dialog alone
                    image = ImageGrab.grab(bbox=box, all_screens=True)
                    note = message.replace(chr(10), " ")[:90]
                    shooter.save(image, name, None, note=note)
                    shooter.popup_texts[name] = (title, message)
                    if target_info is not None:
                        shooter.boxes[name] = {"x": target_info["x"] + window[0] - box[0],
                                               "y": target_info["y"] + window[1] - box[1],
                                               "w": target_info["w"], "h": target_info["h"]}
                for _try in range(12):
                    user32.SetForegroundWindow(dialog)
                    press_button(dialog, answer)
                    waited = 0.0
                    while user32.IsWindow(dialog) and user32.IsWindowVisible(dialog) and waited < 0.6:
                        time.sleep(0.1)
                        waited += 0.1
                    if not (user32.IsWindow(dialog) and user32.IsWindowVisible(dialog)):
                        break
                time.sleep(0.4)

        helper = threading.Thread(target=watch, daemon=True)
        helper.start()
        action()
        time.sleep(0.8)
        state["stop"] = True
        helper.join(timeout=3)
        self.root.update()
        taken = len(state["seen"])
        for step in range(taken, len(plan)):
            if plan[step][1] is not None:
                self.results.append((plan[step][1], "-", "FAIL", "no pop-up appeared"))
        return state["seen"]

    def write_boxes(self):
        """Save target boxes for the annotation step."""
        with open(os.path.join(OUT_DIR, "boxes.json"), "w", encoding="utf-8") as handle:
            json.dump(self.boxes, handle, indent=1)
