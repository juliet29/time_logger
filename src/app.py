from beaupy import prompt, confirm, select
from rich.console import Console
from db_commands.connect import connect_to_real_db, init_in_memory_db
from db_commands.entry import write_entry_to_db
from prompts import get_date, get_entry_data
from db_commands.connect import check_db
from variables import get_db_path, MAX_ENTRIES


def handle_entry_after_date(connection, console, date):
    entry = get_entry_data(connection, console, date)
    if confirm(entry.confimation_message, default_is_yes=True):
        write_entry_to_db(connection, entry)
    return 0


def log_entry():
    connection = connect_to_real_db(get_db_path())
    check_db(connection)
    console = Console()
    date = get_date()
    handle_entry_after_date(connection, console, date)
    entries_added = 1

    while confirm(f"Add another entry for {date}?"):
        handle_entry_after_date(connection, console, date)
        entries_added += 1
        if entries_added > MAX_ENTRIES:
            break
    return


if __name__ == "__main__":
    log_entry()
