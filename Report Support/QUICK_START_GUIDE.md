# Quick Start Guide (one page)

## Run it
```
cd "Sports Centre System/Source Code"
python main.py
```
Needs Python 3.10+. No installs needed.

## How it works
1. Click a tab: **Booking**, **Membership**, **Coaching** or **Billing**.
2. It asks **"What would you like to do?"** — click an action.
3. The action opens on its own page with one line telling you what to
   do. Usually: click a row on the left, then click the button on the
   right.
4. **← Back** (or clicking the tab again) returns to the actions.

**Manage pages** (Manage Coaches, Manage Classes, Manage Members): click a
row to edit it, **Delete** sits beside each row, and a blank form adds
a new one.

**Not sure what something does? Rest the mouse on it** - a yellow hint
explains every button, box and grid square.

Dates: type `YYYY-MM-DD` or click 📅.

**Dark mode:** click **☾ Dark Mode** at the top right (and **☀ Light Mode** to
switch back). The program remembers your choice. **Exit** always asks
before closing. Red buttons are permanent and
always ask first.

## All actions

| Tab | Actions |
|---|---|
| **Booking** | Book a Court · Cancel a Booking (cancelled bookings are kept on record) |
| **Membership** | Register · Manage Members · Renew Membership |
| **Coaching** | Manage Coaches · Manage Classes · Enrol Member · Remove Member · Hours & Commission |
| **Billing** | Create Bill · Pay Bill · Void Bill · Delete Bill · View Receipt · Daily Revenue |

## Try it in a minute
- **Booking > Book a Court:** pick a date and sport, click a green hour
  (and the next one for 2 hours), pick a member, **Book**.
- **Membership > Register:** name, phone, click a card, **Register**.
- **Coaching > Enrol Member:** click a class, pick a member, **Enrol**.
- **Billing > Create Bill**, then **Pay Bill**.

## Sample IDs already in the system
- Members: `MEM001`–`MEM004`
- Bookings: `BKG001` (confirmed), `BKG002` (confirmed), `BKG003` (cancelled)
- Coaches: `CCH001`, `CCH002`
- Classes: `CLS001`, `CLS002`
- Bills: `BIL001` (paid), `BIL002` (unpaid)

## If something goes wrong
- A clear message always says what to fix, and the program doesn't crash.
- Deleted the `data` folder by accident? Run `python main.py` again and
  it is rebuilt with sample data.
