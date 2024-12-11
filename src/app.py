from beaupy import prompt, confirm, select
from rich.console import Console
from db_interact import write_entry_to_db
from prompts import get_date, get_entry_data
from db_interact import init_in_memory_db

max_entries = 10


def handle_entry_after_date(connection, console, date):
    entry = get_entry_data(connection, console, date)
    if confirm(entry.confimation_message, default_is_yes=True):
        write_entry_to_db(connection, entry)
    return 0


def log_entry():
    connection = init_in_memory_db()
    console = Console()
    date = get_date()
    handle_entry_after_date(connection, console, date)
    entries_added = 1

    while confirm(f"Add another entry for {date}?"):
        handle_entry_after_date(connection, console, date)
        entries_added += 1
        if entries_added > max_entries:
            break
    return


if __name__ == "__main__":
    log_entry()
