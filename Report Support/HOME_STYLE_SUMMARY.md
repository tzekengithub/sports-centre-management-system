# Home style summary

Screenshots: `Report Support/home_dark.png` and `Report Support/home_light.png` (1000 x 610 window).

## 1. What changed

| File | Function / class | Change |
|---|---|---|
| `Source Code/main.py` | `HEADER_PALETTE` | New. The only place with its own colours: one set for Dark Mode, one for Light Mode. The page colour still comes from `common.APP_BG` |
| `Source Code/main.py` | `mix_colour`, `round_rect`, `draw_halo` | New helpers. `mix_colour` blends two colours; `round_rect` draws a rounded rectangle as a smooth polygon; `draw_halo` draws three slightly bigger copies in fading colours (the fake glow) |
| `Source Code/main.py` | `class PillButton` | New. A rounded button on its own small canvas: hover and press colours, a focus ring, Enter and Space work, hover hint kept |
| `Source Code/main.py` | `class HomeHeader` | New. Dot + greeting + ADMIN pill, welcome line, the three shortcut buttons and the clock card. Moves the clock card below the text on a narrow window. `apply_theme` redraws it in the other theme |
| `Source Code/main.py` | `clock_parts`, `timezone_text` | New. Hours / minutes / seconds / AM-PM text, and the time zone as `GMT+8` |
| `Source Code/main.py` | `start_clock`, `build_home_header` | Now work with `HomeHeader`. The clock only changes the text of existing canvas items every second (no redraw, no flicker) |
| `Source Code/main.py` | `main` > `on_theme_toggle` | After the normal recolouring, also redraws the Home header |
| `README.txt` and the docs | | Home page descriptions, test cases, AI log and `CLAUDE.md` updated |

Kept as they were: the greeting by time of day (`greeting_text`), the live clock, the shortcut targets (Book a Court, Register, Create Bill), the module buttons and "How to Use This System". No data format, public function name or message-box text changed. No new file, image or module was added.

## 2. What looks like the reference, and what does not

**Looks like it:**
- Green status dot, large bold greeting, rounded ADMIN pill with a small icon.
- A muted welcome line.
- Three rounded buttons: one filled indigo with a soft glow, two dark with a thin coloured border, coloured text and a small symbol.
- A rounded clock card slightly lighter than the page with a thin border, large lavender digits that glow, dim colons, a small AM/PM label, and the date plus a `GMT+8` label.
- Dark Mode has the glow. Light Mode has a white card, a faint shadow ring, indigo accents and dark digits.

**Does not (honest list):**
- The glow is made of 3 flat rings, so it is a stepped halo, not a real blur. It looks soft at normal size, but you can see the steps if you look closely.
- The edges of canvas shapes are not anti-aliased, so very small curves look slightly rough.
- There is no real gradient on the page or the card (I kept it flat on purpose to stay subtle and fast).
- The page behind the header is the program's existing dark grey (`#1c2026`), not the deep navy of the reference, because the page colour belongs to the whole program. Only the header has its own colours.
- The symbols (people, card) are Windows emoji drawn in one colour by tkinter, so they look smaller and flatter than in a browser.
- The glowing digits use the Consolas font. If a computer has no Consolas, tkinter uses its default font and the digits are a little less even (each digit pair keeps its own fixed slot, so they do not jump).
- The time zone is the computer's UTC offset (for example `GMT+8`), not a named zone like "Kuala Lumpur".
- The narrow layout cannot happen in normal use: the program's window stops at 1000 px wide. It was tested by forcing the window to 760 px.
- The rest of the Home page (title, green module buttons) is unchanged, so the header and the lower half have different styles.

## 3. Test results

On a fresh `data/`, 2026-11-11:
- Header script (real window): **26 checks, 26 passed.** No flicker (same canvas items between ticks), digits change, AM/PM + date + GMT shown, time-zone text for five offsets, hover / press / leave colours, Enter and Space on a focused button, all three shortcuts land on the right pages in Light and Dark Mode, 6 theme toggles in a row (no error, no leftover items), narrow layout at 760 px and 1000 x 610 layout (no overlap), all 19 pages open.
- Logic script: **119 checks, 119 passed** (the module cases of `TEST_CASES.md`).
- GUI script: **55 checks, 55 passed** (tabs, every button with blank fields, Light > Dark > Light round trip, Exit).
- Started from another folder: the window builds, data files are created, the clock changes.
- Compile check and the no-lambda / no-comprehension scan are clean.
- That is **200 checks, all passed**, plus screenshots of both modes that I looked at myself. I fixed one real bug on the way (`timezone_text` ignored the time zone of a datetime that had one) and three mistakes in my own test scripts.

**Not all 132 listed cases in `TEST_CASES.md` were re-run.** The ones that were not (for example MEM-12, BIL-13/14, the CB and MC groups, the older coaching and tester GUI cases) keep their earlier results; the full list is at the top of the 2026-11-11 section in that file.

Found, not fixed (already there before): after Light > Dark > Light the amber "today" button in the calendar pop-up keeps dark text.

## 4. What I could NOT verify (do these yourself on Windows)

1. `cd "Source Code"`, `python main.py`. Look at Home in Light Mode. Click **Dark Mode** (top right): the header should switch to the glowing look at once. Click **Light Mode** to go back.
2. Close the program while in Dark Mode and start it again: it should start dark.
3. Watch the clock for 10 seconds, in both modes. The digits should change without the card flashing or shifting.
4. Click **Book a Court**, **Register Member** and **Create Bill**: each must open its page directly. Then press Tab until a shortcut button shows a white ring and press Enter.
5. Rest the mouse on each of the three buttons: a yellow hint should appear.
6. Display scaling: Settings > System > Display > Scale to **125 %**, restart the program, look at Home (nothing cut off, clock card not hidden, no horizontal scroll bar). Repeat at **150 %**. At larger scaling the canvas shapes keep their pixel size while the text grows, so check the greeting does not touch the ADMIN pill and the digits do not touch the card edge.
7. Make the window narrower: it stops at 1000 px, so the clock card should always stay beside the buttons. If you want to see the stacked layout, ask me for a smaller minimum width.
8. Wait past 12:00 or 18:00 (or change the PC clock) to see the greeting change by itself.

## 5. Run command and backup

- Run: `cd "C:\Users\user\Downloads\Sports Centre System\Source Code"` then `python main.py`
- Backup of the whole project made before any change: `C:\Users\user\Downloads\SportsCentre_BACKUP_20261111_100827` (outside the project folder).
- Final tree: `Source Code/` (main.py, common.py, booking.py, membership.py, coaching.py, billing.py, data/), `README.txt`, `Report Support/` (which now also holds the two screenshots). One extra file, `CLAUDE.md`, was already in the project root and was left in place. Test scripts, `__pycache__/` and `.pyc` files were deleted, and `data/` was put back to the state it had before this work.
- The clock and time zone use `datetime`, not `time`, because the project's rules allow only `datetime`, `os` and `sys`. `xvfb-run` was not needed (Windows with a real display).
