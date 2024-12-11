import datetime
from typing import Type, cast
from sqlite3 import Connection
from rich.console import Console
from rich.style import Style
from beaupy import prompt, confirm, select, select_multiple


from date_helpers import format_date, get_todays_date, validate_date
from conversion_helpers import extract_constant_values_from_string
from datetime import date

from db_interact import read_choices_for_selection_type_from_db, write_new_choice_to_db
from interfaces import Entry, SelectionType

CREATE_NEW = "CREATE NEW"


def create_new_selection(connection: Connection, selection_type: SelectionType, focus_area=None):
    selection = prompt(f"Enter new {selection_type.name}")
    write_new_choice_to_db(connection, selection_type, selection, focus_area=focus_area)
    return str(selection)


def load_and_select_or_create(
    connection: Connection,
    console: Console,
    selection_type: SelectionType,
    focus_area=None,
) -> str:
    console.print(f"Select {selection_type.name}")
    choices = read_choices_for_selection_type_from_db(
        connection, selection_type, focus_area=focus_area
    )
    choices.append(CREATE_NEW)

    selection = select(choices, strict=True)
    assert selection
    if selection == CREATE_NEW:
        return create_new_selection(connection, selection_type, focus_area=focus_area)
    return str(selection)


def get_date():
    if confirm("Use today's date", default_is_yes=True):
        date = get_todays_date()
    else:
        date_text = prompt("Enter a date") 
        date = validate_date(date_text) #
    return date


def get_entry_data(connection: Connection, console: Console, date: date):
    fdate = format_date(date)
    info_style = Style(bold=True)
    focus_area = load_and_select_or_create(
        connection, console, SelectionType.FOCUS_AREA
    )
    console.print(f"{fdate} | {focus_area}", style=info_style)

    project = load_and_select_or_create(
        connection, console, SelectionType.PROJECTS, focus_area=focus_area
    )
    console.print(f"{fdate} | {focus_area} - {project}", style=info_style)

    activity_type = load_and_select_or_create(
        connection, console, SelectionType.ACTIVITY_TYPE
    )
    console.print(
        f"{fdate} | {focus_area} - {project} | {activity_type}", style=info_style
    )

    description = prompt("Descibe work done", target_type=str)
    times_worked = prompt("Enter times worked (ex: 12,34,45)")
    times_worked_values = extract_constant_values_from_string(times_worked)
    console.print(f"{fdate} | {description} for {times_worked_values}", style=info_style)

    entry = Entry(
        date, focus_area, project, activity_type, description, times_worked_values
    )

    return entry
