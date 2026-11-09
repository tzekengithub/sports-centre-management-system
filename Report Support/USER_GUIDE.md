# Sports Centre Management System — User Guide

This guide explains how to start the program and use every feature in
each of the four modules. For a one-page cheat sheet instead, see
`QUICK_START_GUIDE.md`.

## Starting the program

1. Open a terminal / command prompt.
2. Move into the `Source Code` folder (or any folder — the program finds
   its own data folder either way):
   ```
   cd "Sports Centre System/Source Code"
   python main.py
   ```
3. One window opens with a row of tabs along the top: **Home**,
   **Booking**, **Membership**, **Coaching**, **Billing**, and a red
   **Exit**. Everything stays in this one window.
4. The first time it runs, the program creates a `data` folder next to
   `main.py` with a few sample records already in it, so every screen
   has something to look at immediately. Deleting that folder and
   restarting recreates it.

## How every tab works

1. Click a tab. It asks **"What would you like to do?"** and shows one big
   button per action (for example Register, Manage Members, Renew Membership).
2. Click an action. It opens on **its own page**, with one line at the top
   telling you exactly what to do, and one main button.
3. Click **← Back** (or the tab again) to choose another action.

Most pages work the same way: **click a row in the list**, its details
appear on the right, then click the button (e.g. Renew, Cancel Booking,
Pay). Permanent actions are red and always ask you to confirm first.

**Manage pages** (Manage Coaches, Manage Classes, Manage Members) do add,
update and delete on one page: click a row to edit it (it turns green)
and click **Save Changes**; click **Delete** beside a row to remove it;
with nothing clicked, the blank form adds a new one (**New** clears the
form again).

- **Hover for help.** Rest the mouse on any button, box, drop-down or
  grid square for half a second and a yellow hint explains what it does
  and what to type (e.g. "A number from 1 to 500, e.g. 60").
- **Units are always shown:** money in RM, times as 24-hour HH:00,
  durations in hours, commission in %, class sizes in people.
- **Dark mode:** click **☾ Dark Mode** at the top right for dark colours,
  and **☀ Light Mode** to switch back. The program remembers your choice
  next time it starts.
- **Mistakes never crash the program.** A message tells you what to fix,
  e.g. "Please enter a valid number for Hourly rate."
- **Dates:** type `YYYY-MM-DD`, or click 📅 for a calendar pop-up.
- **Search:** where there is a search box, type and press Enter (or click
  Search). Leave it empty to see everything.

---

## Module 1 — Facility & Court Booking

| Action | What you do |
|---|---|
| **Book a Court** | Pick a date and a sport (type the date and press Enter, or use the calendar). The grid shows every court (rows) and every 1-hour slot by its start time, 08:00 to 21:00 (columns): green = free, red ✕ = booked, grey = past. Click a free hour; click the next hour on the same court to book longer (click a selected hour again to clear). Choose the member (type part of a name in **Find** to search) and click **Book**. Only members whose membership is valid on that date are listed. **Save Day Sheet** saves that day's bookings to a text file in `data/day_sheets` for printing. |
| **Reschedule Booking** | Click an upcoming booking, choose the new date, start time and court, then **Reschedule**. The length and price stay the same. |
| **Cancel a Booking** | Click the booking (search by member ID or name, booking ID or date), then **Cancel Booking**. The court becomes free again. Cancelled bookings are never deleted - they stay on record as CANCELLED so the history is kept. |
| **View All Bookings** | Every booking, confirmed and cancelled, past and upcoming. Search by booking ID, member, date (e.g. 2026-11), sport or status; click a row for its details. |

You can't book a time that's taken or in the past. Bookings that have
started can't be cancelled or moved. A booking that has a bill can't be
cancelled or moved until the bill is voided in Billing.

---

## Module 2 — Membership Registration

| Action | What you do |
|---|---|
| **Register** | Type the name and phone, click a membership card (each shows the fee, how long it lasts and the member discount), then **Register**. The new Member ID is shown. |
| **Renew Membership** | Click the member, **Renew**. It's extended from today. |
| **Manage Members** | Everyone with their type, expiry and Active/Expired status; the line underneath shows members per type and how many expire within 30 days. **Click a member** to change name/phone/type, then **Save Changes**. **Delete** beside a member removes them — not allowed while they have an upcoming booking or an unpaid bill. New members are added with **Register**. |

- Names may contain letters, spaces, `/` and `'` — e.g. "Ravi a/l Kumar",
  "Muthu s/o Sami", "Ch'ng Wei".
- Phone: 10–11 digits starting with 01, and each phone only once.
- If the type has a fee, create its bill in **Billing > Create Bill**.

---

## Module 3 — Coaching & Class Management

| Action | What you do |
|---|---|
| **Manage Coaches** | One page for adding, updating and deleting coaches. **To add:** fill in the blank form (name, phone — each coach needs their own number, sport — Badminton, Futsal, Tennis, Squash, Swimming or Yoga — hourly rate RM 1–500, commission 0–100 %) and click **Add Coach**. **To update:** click the coach's row (it turns green), change the details, click **Save Changes** (changing the sport also changes their upcoming classes); **New** goes back to a blank form. **To delete:** click **Delete** beside the coach. A coach with upcoming classes can't be removed; a coach who has taught before is kept as **Inactive** (their hours stay in the report, but they can't get new classes — set Status back to Active to use them again). Changing a coach's sport asks first and says how many classes will change. |
| **Manage Classes** | One page for scheduling, updating and deleting classes. **To schedule:** with nothing clicked, pick the coach, Private or Group, date, start time and duration (1–4 hours), type max people and the fee per person, click **Schedule Class** (a private session is always for 1 person — pick who it is for in the **Member** box that appears when you choose Private; a group takes up to 30). **To update:** click the class's row, change date, time, duration, max people or fee (coach and type can't change), click **Save Changes**. **To delete:** click **Delete** beside the class — the question lists anyone enrolled; a class that has a bill can't be deleted until the bill is voided. Grey rows are classes that are over: you can still fix their fee, size or duration. Type a sport (e.g. Tennis) and click Search to see only those classes. Use the **Find** box under a drop-down to search it by name. |
| **Enrol Member** | Click a class that hasn't started and still has space, pick the member (type in **Find** to search), **Enrol**. Full classes, classes that have started, and members whose membership ends before the class aren't listed. A member can't be in two classes at the same time. Search by sport or coach name. |
| **Remove Member** | Each row is one member in one class. Click the row, **Remove**. Search by the member's name. |
| **Hours & Commission** | Classes, hours, pay (hours × hourly rate) and commission per coach for classes that are **over**, for all time or one month, plus a total. Upcoming hours are shown separately and not counted yet. Type part of a coach's name and click Search to see just that coach. Commission = fee per person × people enrolled × the coach's %. |

---

## Module 4 — Billing, Payments & Finance

| Action | What you do |
|---|---|
| **Create Bill** | Pick the member and what it's for: Court Rental or Coaching Class (pick which — only ones not billed yet are listed), Membership Fee, or Retail Sale (type item and price). Check the amount, discount and total due, then **Create Bill**. It starts UNPAID. |
| **Pay Bill** | Click the unpaid bill. Choose Cash, Card or E-Wallet. For cash, type the amount received (the change is worked out); card and e-wallet are always the exact amount. **Pay** saves a receipt in `data/receipts/`. The line under the list shows how much is still owed. |
| **Void Bill** | Click an unpaid bill that was a mistake, **Void Bill**. It stays on record as VOID. |
| **Delete Bill** | Only void bills are listed. Click one, **Delete Bill**. |
| **View Receipt** | Click a paid bill, **View Receipt**. |
| **Daily Revenue** | Pick a date. Court rentals, coaching, retail sales and membership fees are shown on separate lines with bars, plus the total collected. Only PAID bills count. |

---

## Closing the program

Click the red **Exit** tab, or close the window. Either way the program
asks "Are you sure you want to exit?" first - click **Yes** to close or
**No** to carry on. Everything you saved is kept.
