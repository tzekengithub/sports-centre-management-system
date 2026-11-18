# Demo script (about 10 minutes, fresh sample data)

Start from a deleted `Source Code/data/` so the sample rows below exist. Dates are relative to today.

| # | Module > Page | Click | Expected |
|---|---|---|---|
| 1 | Membership > Register | Name, phone, type Annual, Register | New member card shown |
| 2 | Membership > Renew | Pick MEM001 (expires in 10 days) | Expiry moves on |
| 3 | Membership > Manage Members | Click MEM004, change type, Update | Saved |
| 4 | Membership > Manage Members | Delete beside MEM002 | Refused (booking, unpaid bill, class) |
| 5 | Membership > Manage Members | Delete beside MEM005 (Demo Delete) | Member removed |
| 6 | Booking > Book a Court | Pick member, free cells, Book | "Booked" message with Hours line |
| 7 | Booking > Reschedule | BKG002, new date/hour | Moved |
| 8 | Booking > Cancel | BKG002 | Cancelled, row stays |
| 9 | Booking > Cancel | BKG004 | "Bill BIL003 charges for this booking. Void the bill in Billing first." |
| 10 | Booking > Cancel | BKG001 | "...paid and a paid bill can't be voided, so this booking stays as it is." |
| 11 | Booking > View All Bookings | Open | Counts per status |
| 12 | Coaching > Manage Coaches | Delete CCH003 (Demo Coach) | Removed |
| 13 | Coaching > Manage Coaches | Delete CCH004 (Tan Mei Hua) | Made INACTIVE (history kept) |
| 14 | Coaching > Manage Coaches | Delete CCH001 | Refused: upcoming class CLS001 |
| 15 | Coaching > Enrol Member | CLS001, MEM002 | Enrolled (places free) |
| 16 | Coaching > Remove Member | CLS001, MEM002 | Removed |
| 17 | Coaching > Manage Classes | CLS001, change a value, Update | Saved |
| 18 | Coaching > Hours & Commission | Open | Shows CLS003 (past class) with pay |
| 19 | Coaching > Manage Classes | Delete CLS001 | Deleted (no bill) |
| 20 | Billing > Pay Bill | BIL002, Cash, 100 | Paid, change shown, receipt |
| 21 | Billing > View Receipt | BIL001 | Receipt text |
| 22 | Billing > Void Bill | BIL003 | Voided |
| 23 | Booking > Cancel | BKG004 again | Now cancelled |
| 24 | Billing > Delete Bill | BIL004 (VOID) | Deleted |
| 25 | Billing > Create Bill | Retail item, amount | New UNPAID bill |
| 26 | Billing > Daily Revenue | Today | PAID totals (BIL001, BIL005, BIL002) |
| 27 | Home | Theme toggle, zoom A+ | Colours and text size change in place |
