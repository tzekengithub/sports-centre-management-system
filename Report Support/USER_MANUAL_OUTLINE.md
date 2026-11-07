# User Manual Outline

## Starting the program
1. Open a terminal in the `Source Code` folder (you can also run it from
   any other folder - the program finds its own `data/` folder either
   way).
2. Run `python main.py`. If your Python is older than 3.10, a message
   box explains this and the program exits instead of crashing.
3. One main window appears with a tab bar (Home, Booking, Membership,
   Coaching, Billing, Exit).
   - **Screenshot:** Home tab.
4. Clicking a module tab shows "What would you like to do?" with one
   button per action. Each action opens its own page with a Back button
   and one line of instructions.
   - **Screenshot:** one tab's action menu.

## Module 1 - Facility & Court Booking
1. **Book a Court:** pick a date and sport; the grid shows courts x
   hours (green free, red booked, grey past). Click free hours, pick the
   member, click Book.
   - **Screenshot:** grid with a selection and the price bar.
   - **Screenshot:** booking confirmation.
2. **Cancel a Booking:** click a confirmed booking, click Cancel Booking.
   - **Screenshot:** cancel confirmation.
3. **Delete a Booking:** click a cancelled booking, click Delete Booking.

## Module 2 - Membership Registration
1. **Register:** name, phone, click a membership card, click Register.
   - **Screenshot:** cards with one selected.
2. **Manage Members:** click a member to edit them and click Save
   Changes; click Delete beside a member to remove them (blocked with an
   upcoming booking or unpaid bill).
   - **Screenshot:** a member row highlighted while being edited.
   - **Screenshot:** delete-blocked message.
3. **Renew Membership:** click a member, Renew.

## Module 3 - Coaching & Class Management
1. **Manage Coaches:** fill the blank form and click Add Coach; click a
   coach's row to edit them and click Save Changes; click Delete beside
   a coach to remove them.
   - **Screenshot:** "Please enter a valid number" message for a bad rate.
   - **Screenshot:** a coach row highlighted while being edited.
2. **Manage Classes:** with nothing clicked, fill the form and click
   Schedule Class; click a class's row to edit it and click Save
   Changes; click Delete beside a class to cancel it.
   - **Screenshot:** Manage Classes with a class being edited.
3. **Enrol Member:** click a class, pick a member, Enrol.
4. **Remove Member:** click a class/member row, Remove.
   - **Screenshot:** Remove Member page.
5. **Hours & Commission:** pick a month or All time.
   - **Screenshot:** hours and commission table.

## Module 4 - Billing, Payments & Finance
1. **Create Bill:** member, what it's for, check the preview, Create Bill.
   - **Screenshot:** preview with discount.
2. **Pay Bill:** click an unpaid bill, choose the method, Pay.
   - **Screenshot:** payment message with change.
3. **Void Bill**, **Delete Bill**, **View Receipt:** click a bill, click
   the button.
   - **Screenshot:** receipt.
4. **Daily Revenue:** pick a date; four categories and the total.
   - **Screenshot:** daily revenue.

## Closing the program
Click the red **Exit** tab, or close the window.
