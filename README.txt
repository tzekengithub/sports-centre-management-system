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
|   |-- common.py          (shared helpers, constants, Person class)
|   |-- booking.py         (Module 1: Facility & Court Booking)
|   |-- membership.py      (Module 2: Membership Registration)
|   |-- coaching.py        (Module 3: Coaching & Class Management)
|   |-- billing.py         (Module 4: Billing, Payments & Finance)
|   |-- data/              (created automatically, holds .txt records)
|       |-- members.txt, bookings.txt, coaches.txt, classes.txt, bills.txt
|       |-- receipts/      (one .txt receipt per payment)
|-- README.txt             (this file)
|-- Report Support/        (rubric check, flowcharts, test cases, audit
|                            report, AI usage log, etc.)

3. HOW TO RUN
--------------
Step 1: Open a terminal / command prompt.
Step 2: Move into the "Source Code" folder:
            cd "Sports Centre System/Source Code"
Step 3: Run the program:
            python main.py
Step 4: One window opens with a row of tabs along the top: Home,
        Booking, Membership, Coaching, Billing and a red Exit. Click a
        tab (or a module button on the Home tab) to switch to that
        module in the same window. Each tab asks "What would you like
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

5. AUTHORS
-----------
main.py, booking.py  : Teh Tze Ken (Group Leader / integration)
membership.py        : Teoh Zynn
coaching.py           : Tan Chor Koon
billing.py            : Low Yee Zhe
common.py             : Shared (all members)

6. AI DISCLOSURE
------------------
Parts of this program were generated with AI assistance (Claude Code).
See "Report Support/AI_USAGE_LOG.md" for what was asked, what was
produced, and what each member verified before submission.
