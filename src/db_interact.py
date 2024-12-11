from pathlib import Path
from interfaces import Entry, SelectionType
import sqlite3
from rich import print as rprint


def init_in_memory_db():
    connection = sqlite3.connect(":memory:")

    DB_INIT_PATH = Path.cwd().parent / "db_creators"
    with open(DB_INIT_PATH / "create.sql", "r") as file:
        create_script = file.read()
    with open(DB_INIT_PATH / "init.sql", "r") as file:
        init_script = file.read()

    with connection:
        connection.executescript(create_script)
        connection.executescript(init_script)

    return connection

# TODO -> split into different functions.. 
def read_choices_for_selection_type_from_db(
    connection: sqlite3.Connection, selection_type: SelectionType, focus_area=None
) -> list[tuple[int, ...] | str]:
    match selection_type:
        case SelectionType.FOCUS_AREA | SelectionType.ACTIVITY_TYPE:
            table_name = selection_type.name.lower()
            rprint(f" table_name should be: [bold blue]{table_name}[/bold blue]")
            with connection:
                c = connection.cursor()
                c.row_factory =  lambda _, row: row[0]
                c.execute(
                    f"SELECT * FROM {table_name}"
                )
                return c.fetchall()
        case SelectionType.PROJECTS:
            assert focus_area
            with connection:
                c = connection.cursor()
                c.row_factory =  lambda _, row: row[0]
                c.execute(
                    """SELECT * FROM projects WHERE project_focus_area = :focus_area""",
                    {"focus_area": focus_area},
                )
                return c.fetchall()


def write_new_choice_to_db(selection_type: SelectionType, selection: str, focus_area=None):
    return 0


def write_entry_to_db(entry: Entry):
    # insert into entry
    # insert into entry_activity
    # insert into dates..
    return 0
