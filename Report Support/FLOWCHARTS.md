# Flowcharts and Stepwise Refinement

Updated after the simpler-tabs rewrite (Entry 16 in `AI_USAGE_LOG.md`)
to match the final code. All Mermaid blocks below were
checked for valid syntax (no unescaped brackets/quotes inside node text).

## Main program flow

```mermaid
flowchart TD
    A[Start main.py] --> B{Python 3.10 or newer?}
    B -->|No| B1[Show friendly error, exit]
    B -->|Yes| C[Import the four modules]
    C --> D[ensure_data_files_exist]
    D --> E[Build one main window: tab bar and content area]
    E --> E1[Show Home tab]
    E1 --> F{User clicks a tab or Home button}
    F -->|Same tab as now| E1
    F -->|Different tab| X[Destroy current tab frame]
    X --> Y{Which tab?}
    Y -->|Home| Y0[build_home_tab]
    Y -->|Booking| Y1[build_booking_tab]
    Y -->|Membership| Y2[build_membership_tab]
    Y -->|Coaching| Y3[build_coaching_tab]
    Y -->|Billing| Y4[build_billing_tab]
    Y0 --> Y0a[Home header: greeting, clock every second, 3 shortcut buttons]
    Y0a --> Z[Show new frame, highlight its tab]
    Y0a -. shortcut button .-> S[switch_to_tab with a page name, then open_action_page opens that page]
    Y1 --> Z
    Y2 --> Z
    Y3 --> Z
    Y4 --> Z
    Z --> F
    F -->|Exit| K[Close program]
```

## Booking module flow (Court Availability section)

```mermaid
flowchart TD
    A[Pick date and sport] --> B[build_availability_grid]
    B --> C[count_free_slots_recursive and find_next_free_hour for the info line]
    C --> D[Draw courts x hours grid: free, booked, past]
    D --> E{User clicks a cell}
    E -->|Booked| E1[Show which booking holds it]
    E -->|Free, next to selection on same court| E2[Extend selection]
    E -->|Free, anywhere else| E3[Start new selection]
    E -->|Already selected| E4[Clear selection]
    E2 --> D
    E3 --> D
    E4 --> D
    D --> F{Book clicked}
    F --> G{Member exists, date not past, no clash - set intersection?}
    G -->|No| G1[Show error]
    G -->|Yes| H[create_booking, append to file, redraw grid]
```

## Coaching module flow (Enrolment section)

```mermaid
flowchart TD
    A[Open Enrolment] --> B[List upcoming classes]
    B --> C{User clicks a class}
    C --> D[Show enrolled members by name and members who can be added]
    D --> E{Button pressed}
    E -->|Enrol| F{Member exists, not already enrolled, class not full?}
    F -->|No| F1[Show error]
    F -->|Yes| F2[enrol_participant, rewrite file, refresh]
    E -->|Remove Selected| G{A name is selected in the enrolled list?}
    G -->|No| G1[Ask user to click a name first]
    G -->|Yes| G2[remove_participant, rewrite file, refresh]
```

## Stepwise refinement (problem -> modules -> sub-tasks -> functions)

```
Problem: Manage a sports centre's bookings, members, coaching and billing.
|
|-- Module: Booking
|   |-- Sub-task: Show court availability per hour, per court, per sport
|   |   `-- build_availability_grid, count_free_slots_recursive, find_next_free_hour
|   |-- Sub-task: Book / cancel a booking (cancelled bookings are kept)
|   |   `-- create_booking, cancel_booking, has_clash
|   `-- Sub-task: Find bookings
|       `-- search_bookings
|
|-- Module: Membership
|   |-- Sub-task: Register for a membership type
|   |   `-- register_member, get_phone_set
|   |-- Sub-task: Update / renew / delete a member
|   |   `-- update_member, renew_member, delete_member
|   |   (delete checks both future bookings AND unpaid bills)
|   |-- Sub-task: Find members
|   |   `-- search_members, find_member_by_id
|   `-- Sub-task: Report on members
|       `-- count_members_by_type, members_expiring_within, count_members_recursive
|
|-- Module: Coaching
|   |-- Sub-task: Manage coaches
|   |   `-- register_coach, update_coach (moves upcoming classes to a new sport),
|   |       delete_coach (blocked while classes remain), find_coach_by_id
|   |-- Sub-task: Assign coaches to private sessions / group classes
|   |   `-- schedule_class, update_class, cancel_class, validate_class_details
|   |-- Sub-task: Manage participants
|   |   `-- enrol_participant, remove_participant, load_member_names
|   `-- Sub-task: Track working hours and commission
|       `-- coach_hours_by_month, calculate_commission, total_commission_recursive
|
`-- Module: Billing
    |-- Sub-task: Create a bill
    |   `-- generate_bill, billed_references, unbilled_bookings, unbilled_classes
    |-- Sub-task: Take payment
    |   `-- pay_bill, write_receipt, read_receipt, find_bill_by_id
    |-- Sub-task: Manage bill status
    |   `-- void_bill, delete_void_bill, search_bills
    `-- Sub-task: Daily revenue by category (court, coaching, retail, membership)
        `-- daily_revenue_summary (PAID bills only), total_bills_recursive
```
