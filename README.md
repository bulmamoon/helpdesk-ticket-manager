# HelpDesk Ticket Manager

A command-line IT Help Desk ticketing system built in Python. Designed to simulate real-world ticket tracking workflows used by IT support teams.

## Features

- **Create tickets** with requester info, category, priority, and description
- **List all tickets** or filter by status (Open, In Progress, Resolved, etc.)
- **Update tickets** â change status, priority, assignee, or resolution notes
- **Search tickets** by keyword across requester, subject, category, or description
- **Summary report** â breakdown of tickets by status, priority, and category
- All ticket data persisted to a local **CSV file**

## Technologies

- Python 3.x (standard library only â no external dependencies)

## Getting Started

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/helpdesk-ticket-manager.git
cd helpdesk-ticket-manager

# Run the application
python ticket_manager.py
```

## Project Structure

```
helpdesk-ticket-manager/
âââ ticket_manager.py   # Main application
âââ tickets.csv         # Ticket database (auto-created on first run)
âââ README.md
```

## Ticket Fields

| Field        | Description                                      |
|--------------|--------------------------------------------------|
| ticket_id    | Unique ID (e.g., TKT-AB12C)                     |
| created_at   | Timestamp when ticket was opened                 |
| updated_at   | Timestamp of last update                         |
| requester    | Name of the person who submitted the ticket      |
| category     | Hardware, Software, Network, Account, etc.       |
| priority     | Low / Medium / High / Critical                   |
| subject      | Short description of the issue                   |
| description  | Full details of the issue                        |
| status       | Open / In Progress / Pending User / Resolved / Closed |
| assigned_to  | Technician handling the ticket                   |
| resolution   | Notes on how the issue was resolved              |

## Skills Demonstrated

- IT Help Desk ticketing workflows
- Data persistence with CSV
- CLI application design in Python
- Ticket categorization and prioritization
