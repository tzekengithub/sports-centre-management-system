# Demo data summary

## 1. Real cause of the delete problem
Delete Member refuses while the member has an UNPAID bill of ANY category. On the user's real data, `BIL003` (an UNPAID *membership fee* for MEM005) was the blocker even though all of that member's bookings were cancelled: the bill is not about a booking. Fix: Billing > Void Bill, then Delete. Proven by `a_cause` throw-away script: billed booking can't be cancelled (case 1, 3), void + cancel + delete works (case 2).
Real bug found (case 5): `generate_bill` accepted a CANCELLED booking, creating an UNPAID bill that blocks Delete for good. Now refused.

## 2. What changed
- `billing.py`: new `booking_is_cancelled`; `generate_bill` refuses a cancelled booking.
- `common.py`: `build_sample_rows` extended; new `write_sample_receipts` called from `ensure_data_files_exist` when bills.txt is created.
- No change to delete rules, message texts, file formats or public names.

## 3. Sample IDs
- Members: MEM001 (renew, 10 days left), MEM002 (blocked: booking+unpaid bill+class; Delete offers the force prompt, answer No), MEM001 (force delete not possible: paid bill BIL001 on BKG001), MEM003, MEM004 (update), **MEM005 Demo Delete** (deletable).
- Bookings: BKG002 (no bill: reschedule/cancel), BKG004 (UNPAID bill BIL003), BKG001 (PAID bill), BKG003 (cancelled).
- Coaches: CCH003 never taught, CCH004 past class only, CCH001/CCH002 have upcoming classes.
- Classes: CLS001 (group, free places, no bill), CLS002 (private, UNPAID BIL002), CLS003 (past).
- Membership fee: MEM001 and MEM002 fees are still billable (live demo); MEM003's is already paid (BIL006, dated 5 days ago), and Renew brings it back; MEM004 (Pay-As-You-Go) has no fee.
- Bills: BIL002 pay, BIL003 void, BIL004 VOID (delete), BIL001 PAID + receipt, BIL005 PAID retail today + receipt.

## 4. Test results (all run for real)
Delete-rule script: 5 checks pass (after fix). Demo walk: 25 steps pass. Existing suites updated for the new sample rows and re-run: 86, 27, 20, 43, 29 logic checks and 21, 26, 17, 11, 18, 9, 43 GUI checks, 0 failed. Click-through of every page with blank fields: 166 clicks, no unhandled error. py_compile and forbidden-syntax scan clean.

## 5. Not verified
- Demo walk was run at logic level, not clicked by hand through every GUI page in order.
- The user's existing `data/` is left alone (sample rows apply only when files are missing).
- Test suites are throw-away scripts outside the project.
