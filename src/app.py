from beaupy import prompt, confirm, select
from rich.console import Console
from db_interact import write_entry_to_db
from prompts import get_date, get_entry_data
from db_interact import init_in_memory_db

max_entries = 10


def log_entry():
    connection = init_in_memory_db()
    console = Console()
    date = get_date()
    entry = get_entry_data(connection, console, date)
    if confirm(entry.confimation_message):
        write_entry_to_db(entry)

    entries_added = 1

    while confirm(f"Add another entry for {date}?"):
        entry = get_entry_data(connection, console, date)
        if confirm(entry.confimation_message):
            write_entry_to_db(entry)
        entries_added += 1
        if entries_added > max_entries:
            break

    return

    # confirm entry
    # write to db..

    # add another task for today + focus area?
    # add another task for a different day? => while loops?


if __name__ == "__main__":
    log_entry()
