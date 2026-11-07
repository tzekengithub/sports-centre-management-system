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

- **Mistakes never crash the program.** A message tells you what to fix,
  e.g. "Please enter a valid number for Hourly rate."
- **Dates:** type `YYYY-MM-DD`, or click 📅 for a calendar pop-up.
- **Search:** where there is a search box, type and press Enter (or click
  Search). Leave it empty to see everything.

---

## Module 1 — Facility & Court Booking

| Action | What you do |
|---|---|
| **Book a Court** | Pick a date and a sport. The grid shows every court (rows) and every hour (columns): green = free, red ✕ = booked, grey = past. Click a free hour; click the next hour on the same court to book longer (click a selected hour again to clear). Pick the member and click **Book**. The bar shows the court, time and price. |
| **Cancel a Booking** | Click the booking (search by Member ID if needed), then **Cancel Booking**. It stays on record as CANCELLED. |
| **Delete a Booking** | Only cancelled bookings are listed. Click one, then **Delete Booking**. |

You can't book a time that's taken or in the past. To change a booking's
time, cancel it and book the new time.

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
| **Manage Coaches** | One page for adding, updating and deleting coaches. **To add:** fill in the blank form (name, phone, sport — Badminton, Futsal, Tennis, Squash, Swimming or Yoga — hourly rate RM 1–500, commission 0–100 %) and click **Add Coach**. **To update:** click the coach's row (it turns green), change the details, click **Save Changes** (changing the sport also changes their upcoming classes); **New** goes back to a blank form. **To delete:** click **Delete** beside the coach — only possible once none of their classes are left on record. |
| **Manage Classes** | One page for scheduling, updating and deleting classes. **To schedule:** with nothing clicked, pick the coach, Private or Group, date, start time and duration (1–4 hours), type max people and the fee per person, click **Schedule Class** (a private session is always for 1 person; a group takes up to 30). **To update:** click the class's row, change date, time, duration, max people or fee (coach and type can't change), click **Save Changes**. **To delete:** click **Delete** beside the class. Type a Coach ID and click Search to see one coach's classes. |
| **Enrol Member** | Click an upcoming class that still has space, pick the member, **Enrol**. |
| **Remove Member** | Each row is one member in one class. Click the row, **Remove**. |
| **Hours & Commission** | Classes, hours and commission per coach, for all time or one month, plus a total. Commission = fee per person × people enrolled × the coach's %. |

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

Click the red **Exit** tab, or close the window.
