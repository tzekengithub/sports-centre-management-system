# Home header summary

## 1. What changed

| File | Function / item | Change |
|---|---|---|
| `Source Code/main.py` | `greeting_text(hour)` | New. `if/elif/else`: 05:00-11:59 Good Morning!, 12:00-17:59 Good Afternoon!, otherwise Good Evening! |
| `Source Code/main.py` | `clock_text(now)`, `date_text(now)` | New. `09:05:03 AM` (`%I:%M:%S %p`) and `Wednesday - Nov 11, 2026` (day has no leading zero) |
| `Source Code/main.py` | `start_clock(...)` | New. Updates greeting, time and date now and then every second with `after(1000, ...)`. A `<Destroy>` binding cancels the pending tick when the page is left, and `try / except tk.TclError` covers a window that is already gone |
| `Source Code/main.py` | `build_home_header(...)`, `SHORTCUTS` | New. Greeting, ADMIN label, welcome line, three shortcut buttons (built with a `for` loop over `SHORTCUTS`, a list of (text, tab, page) tuples) on the left, the clock card on the right |
| `Source Code/main.py` | `build_home_tab` | Now builds the header first. Everything that was there (title, "How to Use This System", the four module buttons) is still there and unchanged |
| `Source Code/main.py` | `switch_to_tab(tab_name, page_name=None)` | New optional `page_name`. With it, the tab is built as usual and that page is then opened |
| `Source Code/common.py` | `build_action_menu` | Stores a small `open_action_page(name)` function on the tab's frame. It runs the same code as the tab's own menu button, so the page's refresh hook runs too |
| `Source Code/booking.py` | `BOOKING_ACTIONS` text | The one-line instruction of "Book a Court" was out of date after the multi-select change; it now describes the new behaviour |
| `README.txt`, `USER_GUIDE.md`, `QUICK_START_GUIDE.md`, `CODE_EXPLANATION.md`, `FLOWCHARTS.md`, `RUBRIC_CHECK.md`, `TEST_CASES.md`, `AI_USAGE_LOG.md` | | Updated for the Home header (and for the earlier booking changes, see section 3) |

No data file format, public function name or message-box text was changed.
`switch_to_tab` and `build_action_menu` kept their names; they only gained an optional argument or an extra attribute.

## 2. How it works

- **Greeting:** `greeting_text` picks the greeting from `datetime.now().hour`. The clock refresh also re-sets the greeting every second, so it changes by itself at 12:00 and 18:00.
- **Clock:** `start_clock` formats `datetime.now()` into the time label and the date label, then schedules itself again after 1000 ms. Leaving the Home page (a tab switch) or closing the window stops it without an error.
- **Shortcut buttons:** each calls `switch_to_tab(tab, page)`. That rebuilds the tab from the data files like any tab switch, then opens the page the same way the tab's own menu button does. No page-building code is duplicated.
- **Theme:** every colour comes from `common` (`APP_BG`, `PANEL_BG`, `BUTTON_COLOR`, `ACCENT_COLOR`, ...). The clock card is made with `common.make_card` (panel colour, thin border). Dark Mode recolours the header in place with the existing mechanism. The saved dark-mode choice is the existing `settings.txt` and is unchanged.
- **Hover hints:** the three shortcut buttons say "Open the ... page."; the ADMIN label says it is only a label.

## 3. Test results

On a fresh `data/` folder, 2026-11-11:

- **Logic script: 119 checks, 119 passed.** Covers the Membership, Coaching, Booking, Billing, general and inheritance cases of `TEST_CASES.md` (the list is at the top of its new section).
- **GUI script (real window, buttons pressed with `.invoke()`): 55 checks, 55 passed.** Covers every tab and all 19 pages opening, clicking Booking/Membership/Coaching/Billing again, every button on every page with blank fields (no uncaught exception), a Light > Dark > Light round trip on all 19 pages, the saved theme choice, Exit asking first (No keeps the program, Yes closes it), and hover hints on every Home button.
- **Home header checks (HOME-01 to HOME-09):** greeting for 8 hours, date text, header shows, the clock changed over 3.2 s (also when started from another folder), the three shortcuts land on the right pages, dark mode recolours the header, no widget past the window edge at 1000 x 610, and no timer error when leaving the page. Screenshots of Home in light and dark mode were looked at.
- **Fresh start:** `data/` deleted, program launched, window built, all data files and `receipts/` recreated with sample data. Also started from a different working directory.
- **Compile check and forbidden-syntax scan** (no lambdas, no comprehensions): clean.

Two of my own test-script mistakes were fixed along the way (a sample member whose membership ends in 10 days, and a pop-up left open by my click-through). The program code needed no fix.

**Not all 132 listed cases were re-run.** These were not repeated this time and keep their earlier results: MEM-12, COA-13/14, BKG-13/14, BIL-13/14, TIP-02/03, UNIT-01/02, the CB cases, DM-02/04/05 and the older coaching and tester GUI cases (FIX-01/04, MC-01 to MC-12, T4/T5/T8, B15/B16, G1 to G9, BK1 to BK10, U1 to U5). They need typed text, timing or a read-only file, and I did not script them. `TEST_CASES.md` says so.

Also changed earlier in this same session (not part of the Home brief): several booking-grid changes, namely choosing separate hours and booking them in one go, cancelling part of a booking, clicking a red hour to cancel just that hour, and faster grid clicks. Their cases are BKG-16 to BKG-21.

**Found, not fixed (it was already like this):** after Light > Dark > Light, the amber "today" button in the calendar pop-up keeps dark text instead of white.

## 4. What I could NOT verify (do these yourself on your Windows screen)

1. `cd "Source Code"`, then `python main.py`. Look at Home: greeting, ADMIN label, welcome line, three buttons on the left, clock card on the right. Watch the seconds change.
2. Click **Dark Mode**. The header, buttons and clock card should recolour at once. Click **Light Mode** to come back. Close and reopen the program after leaving it in Dark Mode: it should start dark.
3. Click **Book a Court**, **Register Member** and **Create Bill** on Home. Each must open its own page directly (not the tab menu).
4. Rest the mouse on each shortcut button and on ADMIN: a yellow hint should appear.
5. Windows display scaling: Settings > System > Display > Scale. Set **125 %**, restart the program, check Home (nothing cut off, no horizontal scroll bar, the clock card not hidden). Repeat at **150 %**. I only tested at the scaling of this machine.
6. Drag the window to its smallest size (it stops at 1000 px wide) and check Home again.
7. Leave the program open past 12:00 or 18:00 (or change the PC clock) to see the greeting change by itself.
8. Click **Exit** and answer No, then Yes.

## 5. Run command and backup

- Run: `cd "C:\Users\user\Downloads\Sports Centre System\Source Code"` then `python main.py`
- Backup of the whole project made before any change: `C:\Users\user\Downloads\SportsCentre_BACKUP_20261111_095207` (outside the project folder).
- Final tree: `Source Code/` (main.py, common.py, booking.py, membership.py, coaching.py, billing.py, data/), `README.txt`, `Report Support/`. One extra file, `CLAUDE.md`, was already in the project root (instructions for Claude Code) and was left in place. Test scripts, `__pycache__/` and `.pyc` files were deleted, and `data/` was put back to the state it had before this work.
- Because the brief said to use only the standard library and the project allows only `datetime`, the clock uses `datetime`, not `time`. `xvfb-run` was not needed (this is Windows with a real display).
