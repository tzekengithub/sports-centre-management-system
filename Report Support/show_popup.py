"""Opens the real program (from a temporary copy, so your data is safe), does the
steps for one pop-up, and LEAVES that pop-up open so you can screenshot it.
Close it with OK when you have the picture, and the program closes too.
Usage: python show_popup.py 1|2|3
  1 = member deleted message   2 = part of a booking cancelled   3 = bill paid"""

import sys
import threading
import time

import take_screenshots_real as t
import shot_core as core
import tkinter as tk

WHICH = sys.argv[1] if len(sys.argv) > 1 else "1"


def auto_answer_first_dialog():
    """Wait for the first (question) dialog and click Yes; leave the next one open."""
    def watch():
        while True:
            dialogs = core.find_dialogs()
            if len(dialogs) > 0:
                time.sleep(0.6)
                for _try in range(12):
                    core.user32.SetForegroundWindow(dialogs[0])
                    core.press_button(dialogs[0], "yes")
                    time.sleep(0.5)
                    if not core.user32.IsWindow(dialogs[0]):
                        return
                return
            time.sleep(0.1)
    threading.Thread(target=watch, daemon=True).start()


def run(root):
    t.R = root
    t.S = core.Shooter(root)
    root.report_callback_exception = lambda *error: print("ERR", error[1])
    t.S.place()
    t.snapshot_data()
    if WHICH == "1":
        t.open_page("Membership", "Manage Members")
        button = t.row_delete_button("MEM005")
        auto_answer_first_dialog()
        t.S.place()
        button.invoke()
    elif WHICH == "2":
        t.open_page("Booking", "Book a Court")
        book_button = t.prepare_booking(t.TOMORROW, 3, "Ravi")
        t.S.place()
        t.popup([("ok", None)], book_button.invoke)   # booking-made message closes by itself
        t.open_page("Booking", "Cancel a Booking")
        newest = None
        for row in t.listbox().get(0, tk.END):
            if "MEM004" in row:
                newest = row.strip().split()[0]
        t.pick(newest)
        t.option_menus()[1]["menu"].invoke(0)
        root.update()
        cancel_button = t.btn("Cancel Booking")
        auto_answer_first_dialog()
        t.S.place()
        cancel_button.invoke()
    else:
        t.open_page("Billing", "Pay Bill")
        t.pick("BIL002")
        pay_button = t.btn("Pay")
        t.S.place()
        pay_button.invoke()
    root.destroy()


tk.Tk.mainloop = lambda self, n=0: run(self)
if __name__ == "__main__":
    t.main.main()
    t.shutil.rmtree(t.TEMP_ROOT, ignore_errors=True)
