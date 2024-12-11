from interfaces import Entry, SelectionType
from sqlite3 import Connection
from rich import print as rprint
from date_helpers import format_date


def read_choices_for_selection_type_from_db(
    connection: Connection, selection_type: SelectionType, focus_area=None
) -> list[tuple[int, ...] | str]:
    with connection:
        c = connection.cursor()
        c.row_factory = lambda _, row: row[0]
        match selection_type:
            case SelectionType.FOCUS_AREA | SelectionType.ACTIVITY_TYPE:
                table_name = selection_type.name.lower()
                c.execute(f"SELECT * FROM {table_name}")
                return c.fetchall()
            case SelectionType.PROJECTS:
                assert focus_area
                c.execute(
                    """SELECT * FROM projects WHERE project_focus_area = :focus_area""",
                    {"focus_area": focus_area},
                )
                return c.fetchall()


def write_new_choice_to_db(
    connection: Connection,
    selection_type: SelectionType,
    selection: str,
    focus_area=None,
):
    if selection_type == SelectionType.PROJECTS:
        assert focus_area
    with connection:
        c = connection.cursor()
        match selection_type:
            case SelectionType.FOCUS_AREA:
                c.execute(
                    """INSERT INTO focus_area VALUES (:selection)""",
                    {"selection": selection},
                )
            case SelectionType.PROJECTS:
                c.execute(
                    """INSERT INTO projects VALUES (:selection, :focus_area)""",
                    {"selection": selection, "focus_area": focus_area},
                )
            case SelectionType.ACTIVITY_TYPE:
                c.execute(
                    """INSERT INTO activity_type VALUES (:selection)""",
                    {"selection": selection},
                )
    return 1


def write_entry_to_db(connection: Connection, entry: Entry):
    with connection:
        # insert into entry
        c = connection.cursor()
        c.execute(
            """INSERT INTO entry VALUES (:row_id, :entry_date, :entry_project_name, :description)""",
            {
                "row_id": None,
                "entry_date": format_date(entry.date),
                "entry_project_name": entry.project,
                "description": entry.description,
            },
        )
        entry_id = c.lastrowid
        # insert into entry_activity
        c.execute(
            """INSERT INTO entered_activity VALUES (:entry_id, :activity_type)""",
            {"entry_id": entry_id, "activity_type": entry.activity_type},
        )

        # insert into times..
        minutes_data = [
            {"entry_id": entry_id, "minutes": mins} for mins in entry.times_worked
        ]
        c.executemany(
            """INSERT INTO time_elapsed VALUES (:entry_id, :minutes)
            """,
            minutes_data,
        )
    return 1
