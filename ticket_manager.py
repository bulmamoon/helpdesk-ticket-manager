"""
HelpDesk Ticket Manager
========================
A command-line IT Help Desk ticketing system that allows technicians to
create, update, search, and close support tickets. All tickets are saved
to a local CSV file for persistence.

Usage:
    python ticket_manager.py
"""

import csv
import os
import datetime
import random
import string

TICKETS_FILE = "tickets.csv"

FIELDNAMES = ["ticket_id", "created_at", "updated_at", "requester", "category",
              "priority", "subject", "description", "status", "assigned_to", "resolution"]

CATEGORIES = ["Hardware", "Software", "Network", "Account/Access", "Email", "Printer", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES   = ["Open", "In Progress", "Pending User", "Resolved", "Closed"]


def generate_ticket_id():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"TKT-{suffix}"


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_csv():
    if not os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"[INFO] Ticket database created: {TICKETS_FILE}")


def load_tickets():
    tickets = []
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tickets.append(row)
    return tickets


def save_tickets(tickets):
    with open(TICKETS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tickets)


def pick_from_list(label, options):
    print(f"\n  {label}:")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        choice = input("  Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Invalid choice. Please try again.")


def create_ticket():
    print("\n" + "="*50)
    print("  CREATE NEW TICKET")
    print("="*50)
    ticket = {
        "ticket_id":   generate_ticket_id(),
        "created_at":  get_timestamp(),
        "updated_at":  get_timestamp(),
        "requester":   input("  Requester name: ").strip(),
        "category":    pick_from_list("Category", CATEGORIES),
        "priority":    pick_from_list("Priority", PRIORITIES),
        "subject":     input("  Subject: ").strip(),
        "description": input("  Description: ").strip(),
        "status":      "Open",
        "assigned_to": input("  Assign to technician (leave blank for unassigned): ").strip() or "Unassigned",
        "resolution":  ""
    }
    tickets = load_tickets()
    tickets.append(ticket)
    save_tickets(tickets)
    print(f"\n  [SUCCESS] Ticket created: {ticket['ticket_id']}")
    return ticket["ticket_id"]


def list_tickets(filter_status=None):
    tickets = load_tickets()
    if filter_status:
        tickets = [t for t in tickets if t["status"] == filter_status]
    if not tickets:
        print("\n  No tickets found.")
        return
    print("\n" + "="*80)
    print(f"  {'ID':<12} {'Status':<14} {'Priority':<10} {'Category':<16} {'Subject':<25} {'Requester'}")
    print("-"*80)
    for t in tickets:
        print(f"  {t['ticket_id']:<12} {t['status']:<14} {t['priority']:<10} {t['category']:<16} {t['subject'][:24]:<25} {t['requester']}")
    print("="*80)
    print(f"  Total: {len(tickets)} ticket(s)")


def view_ticket():
    ticket_id = input("\n  Enter Ticket ID: ").strip().upper()
    tickets = load_tickets()
    ticket = next((t for t in tickets if t["ticket_id"] == ticket_id), None)
    if not ticket:
        print(f"  [ERROR] Ticket {ticket_id} not found.")
        return
    print("\n" + "="*50)
    print(f"  TICKET DETAILS: {ticket['ticket_id']}")
    print("="*50)
    for key, val in ticket.items():
        print(f"  {key.replace('_',' ').title():<15}: {val}")
    print("="*50)


def update_ticket():
    ticket_id = input("\n  Enter Ticket ID to update: ").strip().upper()
    tickets = load_tickets()
    for i, t in enumerate(tickets):
        if t["ticket_id"] == ticket_id:
            print(f"\n  Updating ticket: {ticket_id}")
            print("  What would you like to update?")
            field = pick_from_list("Field", ["status", "priority", "assigned_to", "resolution", "description"])
            if field == "status":
                new_val = pick_from_list("New Status", STATUSES)
            elif field == "priority":
                new_val = pick_from_list("New Priority", PRIORITIES)
            else:
                new_val = input(f"  New {field}: ").strip()
            tickets[i][field] = new_val
            tickets[i]["updated_at"] = get_timestamp()
            save_tickets(tickets)
            print(f"  [SUCCESS] Ticket {ticket_id} updated: {field} -> {new_val}")
            return
    print(f"  [ERROR] Ticket {ticket_id} not found.")


def search_tickets():
    keyword = input("\n  Search keyword (requester, subject, category): ").strip().lower()
    tickets = load_tickets()
    results = [t for t in tickets if
               keyword in t["requester"].lower() or
               keyword in t["subject"].lower() or
               keyword in t["category"].lower() or
               keyword in t["description"].lower()]
    if not results:
        print("  No matching tickets found.")
    else:
        print(f"\n  Found {len(results)} matching ticket(s):")
        for t in results:
            print(f"  [{t['ticket_id']}] {t['status']} | {t['priority']} | {t['subject']} -> {t['requester']}")


def summary_report():
    tickets = load_tickets()
    if not tickets:
        print("\n  No tickets in the system.")
        return
    print("\n" + "="*40)
    print("  TICKET SUMMARY REPORT")
    print("="*40)
    # Status breakdown
    print("\n  By Status:")
    for s in STATUSES:
        count = sum(1 for t in tickets if t["status"] == s)
        print(f"    {s:<16}: {count}")
    # Priority breakdown
    print("\n  By Priority:")
    for p in PRIORITIES:
        count = sum(1 for t in tickets if t["priority"] == p)
        print(f"    {p:<16}: {count}")
    # Category breakdown
    print("\n  By Category:")
    for c in CATEGORIES:
        count = sum(1 for t in tickets if t["category"] == c)
        if count:
            print(f"    {c:<16}: {count}")
    print("="*40)
    print(f"  Total Tickets: {len(tickets)}")


def main():
    init_csv()
    menu = {
        "1": ("Create new ticket",       create_ticket),
        "2": ("List all tickets",         lambda: list_tickets()),
        "3": ("List open tickets",        lambda: list_tickets("Open")),
        "4": ("View ticket details",      view_ticket),
        "5": ("Update ticket",            update_ticket),
        "6": ("Search tickets",           search_tickets),
        "7": ("Summary report",           summary_report),
        "8": ("Exit",                     None),
    }
    print("\n" + "="*50)
    print("   IT HELP DESK TICKET MANAGER")
    print("="*50)
    while True:
        print("\n  MENU:")
        for key, (label, _) in menu.items():
            print(f"    {key}. {label}")
        choice = input("\n  Select an option: ").strip()
        if choice == "8":
            print("\n  Goodbye!\n")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("  Invalid option. Please try again.")


if __name__ == "__main__":
    main()
