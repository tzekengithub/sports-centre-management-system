# Membership picture cards - summary

## 1. What changed
- `common.py`: new `IMAGES_FOLDER` (built from `__file__`, like `DATA_FOLDER`).
- `membership.py`: new `load_card_picture(type)` (finds `card_<type>.png` then `<type>.png`, loads with `tk.PhotoImage`, `subsample` to ~240 px, returns None on a bad/missing file via `except tk.TclError`). `build_register_page` shows a picture card with a caption from `type_caption` (real fee/duration/discount); no picture = old text card. Chosen card gets a thick coloured frame (works in Light and Dark). PhotoImages kept on `cards_frame.card_pictures`.
- Images: all 7 supplied files were JPEGs named `.png` (Tk can't load them) and 1280x698. Converted once with Pillow (outside the program) to real PNG, 216x118 (240 px cards made 4 per row 1040 px wide, too wide for the 1000 px window). Originals are in the backup.
- Docs: README, USER_GUIDE, QUICK_START_GUIDE, CODE_EXPLANATION, RUBRIC_CHECK, AI_USAGE_LOG.
- Not changed: fees, discounts, durations, data formats, message texts. Optional item 7 (picture on Renew page) skipped to avoid crowding.

## 2. Tests (real, 18 checks, all pass)
7 cards / 7 pictures; each type clicked, frame marker moves, registered member has right type and expiry; renaming `card_vip.png` + `card_youth.png` -> those two fall back to text cards, no error; theme toggle keeps layout; starts from another working directory; compile check and forbidden-syntax scan clean. Found and fixed one bug on the way (pictures were garbage-collected).
Not re-run: the 269 older rows of `TEST_CASES.md` (not touched by this change); no new rows added there.
Screenshots: `register_light_none.png`, `register_light_selected.png`, `register_dark_selected.png` (1000x610).

## 3. Not verified - do on Windows yourself
1. Dark Mode, Register page, no card selected (no screenshot taken).
2. Windows display scaling 125% and 150%: open Membership > Register, check 4 cards per row still fit, no cut-off.
3. Narrow window: minimum size is 1000x610 (the program forbids smaller), so only checked at that size. Use A+ zoom and check the page.
4. Hover each card, tooltip appears.
No `xvfb` on Windows; tested on the real display.

## 4. Run / backup
`cd "Source Code"` then `python main.py`
Backup: `C:\Users\user\Downloads\SportsCentre_BACKUP_20261111_202050\`
Note: stray `annual.png`, `family.png` etc. in the project root are yours; I left them (final tree wants them gone - delete if unneeded).
