import datetime
from typing import Type, cast
from sqlite3 import Connection
from rich.console import Console
from beaupy import prompt, confirm, select, select_multiple


from date_helpers import get_todays_date, date_validator
from conversion_helpers import extract_constant_values_from_string
from datetime import date

from db_interact import read_choices_for_selection_type_from_db, write_new_choice_to_db
from interfaces import Entry, SelectionType

CREATE_NEW = "CREATE NEW"


def create_new_selection(selection_type: SelectionType, focus_area=None):
    selection = prompt(f"Enter new {selection_type}")
    write_new_choice_to_db(selection_type, selection, focus_area=focus_area)
    return str(selection)


def load_and_select_or_create(connection: Connection,
    console: Console, selection_type: SelectionType, focus_area=None
) -> str:
    console.print(f"Select {selection_type.name}")
    choices = read_choices_for_selection_type_from_db(connection, selection_type, focus_area=focus_area)

    selection = select(choices, strict=True)
    assert selection
    if selection == CREATE_NEW:
        return create_new_selection(selection_type, focus_area=focus_area)
    return str(selection)



def get_date():
    if confirm("Use today's date"):
        date = get_todays_date()
    else:
        date = prompt("Enter a date", validator=date_validator)  # TODO target types..
    return date


def get_entry_data(connection: Connection, console: Console, date: date):
    focus_area = load_and_select_or_create(connection, console, SelectionType.FOCUS_AREA)
 
    project = load_and_select_or_create(connection, console, SelectionType.PROJECTS, focus_area=focus_area)
    
    activity_type = load_and_select_or_create(connection, 
        console, SelectionType.ACTIVITY_TYPE
    )

    description = prompt("Descibe work done", target_type=str)
    times_worked = prompt("Enter times worked (ex: 12,34,45)")
    times_worked_values = extract_constant_values_from_string(times_worked)

    entry = Entry(
        date, focus_area, project, activity_type, description, times_worked_values
    )

    return entry
