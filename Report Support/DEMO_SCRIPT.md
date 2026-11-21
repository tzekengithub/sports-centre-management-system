# Demo script (about 10 minutes, fresh sample data)

Start from a deleted `Source Code/data/` so the sample rows below exist. Dates are relative to today.

| # | Module > Page | Click | Expected |
|---|---|---|---|
| 1 | Membership > Register | Name, phone, type Annual, Register | New member card shown |
| 2 | Membership > Renew | Pick MEM001 (expires in 10 days) | Expiry moves on |
| 3 | Membership > Manage Members | Click MEM004, change type to Annual, Save Changes | "Member MEM004 saved." and a note that a new membership period starts today with the new expiry date |
| 4 | Membership > Manage Members | Delete beside MEM002, answer Yes, then answer **No** to the Force delete question | Question lists BIL002, BKG002 and CLS002 that would be cleared; No changes nothing (later steps still use MEM002) |
| 4a | Membership > Manage Members | Delete beside MEM001 | After the question: error "Force delete is not possible ... BIL001 ... paid" (a paid bill can't be voided) |
| 4b | Membership > Manage Members | Delete beside MEM003, answer Yes to both | MEM003 deleted; BIL003 voided, BKG004 cancelled, out of CLS001 (do this at the END of the demo: later steps use BKG004, BIL003 and CLS001) |
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
| 24a | Billing > Create Bill | Member MEM003 (fee already paid, BIL006), Membership Fee | Note "Membership fee already billed (BIL006, paid). Renew the membership in Membership to bill again."; no total; Create Bill disabled |
| 24b | Billing > Create Bill | Member MEM001 (fee still billable), Membership Fee, Create Bill | RM 1200.00 offered; bill created (unpaid); page then says "...already billed (BIL007, not paid yet)..." |
| 24c | Membership > Renew Membership, then Billing > Create Bill | Renew MEM003 (its fee was paid 5 days ago in the sample data), then Membership Fee for MEM003 | RM 60.00 fee offered again |
| 25 | Billing > Create Bill | Retail item, amount | New UNPAID bill |
| 26 | Billing > Daily Revenue | Today | PAID totals (BIL001, BIL005, BIL002) |
| 27 | Home | Theme toggle, zoom A+ | Colours and text size change in place |

**Fee demo rule:** use MEM001 (fee still billable) and MEM003 (fee already paid, 5 days ago). Do NOT pay a member's fee, Renew the same member and bill again on the same day: a fee billed today still counts for the renewed period until tomorrow. Step 2 (Renew MEM001) comes before MEM001's fee is billed, so the script never does that.
