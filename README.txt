SPORTS CENTRE MANAGEMENT SYSTEM
AMCS1034 Software Development Fundamentals - Group Assignment
================================================================

1. REQUIREMENTS
----------------
- Python 3.10 or newer (the program uses "match" statements, which need
  Python 3.10+). If you run it on an older Python, main.py shows a
  message box explaining this and exits cleanly instead of crashing.
- No external libraries. Only the Python standard library is used:
  tkinter, tkinter.messagebox, datetime, os.
- No "pip install" is required.
- The program finds its own "data" folder based on where main.py itself
  is saved, so it runs correctly whether you launch it from inside
  "Source Code/" or from anywhere else.

2. FOLDER LAYOUT
-----------------
Sports Centre System/
|-- Source Code/
|   |-- main.py            (run this file to start the program)
|   |-- common.py          (shared helpers, constants, Record + Person base classes)
|   |-- booking.py         (Module 1: Facility & Court Booking)
|   |-- membership.py      (Module 2: Membership Registration)
|   |-- coaching.py        (Module 3: Coaching & Class Management)
|   |-- billing.py         (Module 4: Billing, Payments & Finance)
|   |-- data/              (created automatically, holds .txt records)
|       |-- members.txt, bookings.txt, coaches.txt, classes.txt, bills.txt
|       |-- id_counters.txt, settings.txt   (ID counters, light/dark theme)
|       |-- receipts/      (one .txt receipt per payment)
|       |-- day_sheets/    (printable booking lists from Save Day Sheet)
|   |-- images/            (membership card pictures card_<type>.png; the ZIP must include it)
|-- README.txt             (this file)
|-- Report Support/        (rubric check, flowcharts, test cases, audit
|                            report, AI usage log, etc.)

3. HOW TO RUN
--------------
Step 1: Open a terminal / command prompt.
Step 2: Move into the "Source Code" folder:
            cd "Sports Centre System/Source Code"
Step 3: Run the program:
            Windows:          python main.py
            macOS / Linux:    python3 main.py
        (Check your version first with "python --version" or
        "python3 --version": it must say 3.10 or higher.)
        You can also start it from any folder by giving the full path,
        e.g.  python "C:/path/to/Sports Centre System/Source Code/main.py"
Step 4: One window opens with a row of tabs along the top: Home,
        Booking, Membership, Coaching, Billing and a red Exit. Click a
        tab (or a module button on the Home tab) to switch to that
        module in the same window. The Home tab starts with a greeting
        (Good Morning / Afternoon / Evening), an ADMIN label, three
        shortcut buttons (Book a Court, Register Member, Create Bill)
        and a live clock with the date. Each tab asks "What would you like
        to do?" - click an action (e.g. Register, Book a Court, Pay
        Bill) and it opens on its own page with one line of
        instructions. "Back" returns to the actions. "Dark Mode" (top
        right) switches to dark colours and is remembered. Click "Exit"
        (or the window's X) to close - it asks you to confirm first.

The "data" folder and all five .txt files are created automatically the
first time the program runs, already filled with a few sample records so
the demo is not empty. If you delete the "data" folder or any of the
.txt files, the program will recreate them (with sample data) the next
time it starts.

4. SAMPLE IDS FOR THE DEMO
----------------------------
Members   : MEM001 (Ahmad Faiz, VIP), MEM002 (Siti Nurhaliza, Annual),
            MEM003 (Wong Mei Ling, Monthly), MEM004 (Ravi Kumar, Pay-As-You-Go)
Bookings  : BKG001 (CONFIRMED, Badminton), BKG002 (CONFIRMED, Futsal),
            BKG003 (CANCELLED, Tennis)
Coaches   : CCH001 (Lim Wei, Badminton), CCH002 (Nurul Izzah, Tennis)
Classes   : CLS001 (Badminton Group, coach CCH001), CLS002 (Tennis Private,
            coach CCH002)
Bills     : BIL001 (PAID, from booking BKG001), BIL002 (UNPAID, from class CLS002)

5. WHERE EACH RUBRIC CRITERION APPEARS
---------------------------------------
Every criterion is shown in each member's own module. One example
function per cell (the full list is in "Report Support/RUBRIC_CHECK.md").

Criterion            booking.py          membership.py        coaching.py              billing.py
-------------------  ------------------  -------------------  -----------------------  --------------------
Selection if/match   cell_tip_text /     duration_text /      validate_class_details / generate_bill /
                     search_bookings     search_members       search_coaches           search_bills
Loop for + while     build_availability_ load_all_members /   load_all_coaches /       load_all_bills /
                     grid / find_next_   find_member_by_id    find_coach_by_id         find_bill_by_id
                     free_hour
String processing    search_bookings     search_members /     get_participant_list     bill_rows_with_status
                                         format_name
File read + write    load_all_bookings / load_all_members /   load_all_classes /       load_all_bills /
                     create_booking,     register_member      schedule_class           pay_bill,
                     save_day_sheet                                                    write_receipt
List                 booking_list, grid  member_list          class_list               bill_list
Set / tuple / dict   has_clash (set),    get_phone_set (set), participant_set (set),   billed_references
                     SEARCH_FIELDS,      MEMBERSHIP_TYPES,    CLASS_TYPES, coach_      (set), BILL_
                     load_member_names   count_members_by_    hours_by_month (dict)    CATEGORIES, daily_
                                         type (dict)                                   revenue_summary
Predefined modules   datetime + os in    datetime in          datetime in              datetime + os in
                     day_sheet_text /    days_until_expiry    days_until_class         write_receipt
                     save_day_sheet
User functions       count_free_slots_   count_members_       total_commission_        total_bills_
(+ recursion)        recursive           recursive            recursive                recursive
Encapsulation        class Booking       class Member         class Coach / SportsClass class Bill
Inheritance          Booking(Record)     Member(Person)       Coach(Person),           RetailBill(Bill)
                                                              SportsClass(Record)
GUI design           action menu + one-page screens, hover hints, same colours in all four
GUI implementation   4 booking pages     3 member pages       5 coaching pages         6 billing pages
Exception handling   save_day_sheet      days_until_expiry /  update_coach /           read_receipt /
                     (try/except/else/   on_register          days_until_class         on_create
                     finally)
Comments             header docstring + one-line docstring per function + # comment blocks in
                     every file
Execution            python main.py (see section 3)

6. AUTHORS
-----------
main.py, booking.py  : Teh Tze Ken (Group Leader / integration)
membership.py        : Teoh Zynn
coaching.py           : Tan Chor Koon
billing.py            : Low Yee Zhe
common.py             : Shared (all members)

7. AI DISCLOSURE
------------------
Parts of this program were generated with AI assistance (Claude Code).
See "Report Support/AI_USAGE_LOG.md" for what was asked, what was
produced, and what each member verified before submission.
