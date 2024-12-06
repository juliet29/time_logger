from dataclasses import dataclass
import datetime
from typing import Type, cast
from rich.console import Console
from beaupy import prompt, confirm, select, select_multiple
from enum import Enum
from date_helpers import format_date, get_todays_date, date_validator
from conversion_helpers import extract_constant_values_from_string
from datetime import date

CREATE_NEW = "CREATE NEW"


@dataclass
class Entry:
    date: date
    focus_area: str
    projects: list[str]
    activity_types: list[str]
    description: str
    times_worked: list[int]

    @property
    def confimation_message(self):
        return f"Confirm entry is correct: \n {format_date(self.date)} \n Worked on {self.description} for {sum(self.times_worked)} minutes \n Focus area: {self.focus_area} \n Projects: {self.projects} \n Activity types: {self.activity_types} \n"


class SelectionType(Enum):
    FOCUS_AREA = 0  # PhD, Foundations, Blog, CEE243, BACS
    PROJECT = 1  # PhD -> Geomeppy, SVG2Code, Paper1 (can be multiple), Foundations -> Stats, Vector Calc, G.Theory, Blog -> certain book summaries?, Admin -> NoProject, just descriptions..
    ACTIVITY_TYPE = (
        2  # Focus area agnostic -> coding, reading, writing, gathering resources, etc
    )


def read_choices_for_selection_type_from_db(
    selection_type: SelectionType,
) -> list[tuple[int, ...] | str]:
    return ["bye", "hi", "sigh", "chai"]


def write_new_choice_to_db(selection_type: SelectionType, option):
    return 0


def write_entry_to_db(entry: Entry):
    return 0


def handle_create_new(selections: list[str] | str, selection_type: SelectionType):
    def create_new():
        selection = prompt(f"Enter new {selection_type}")
        write_new_choice_to_db(selection_type, selection)
        return str(selection)

    try:
        selections = cast(list, selections)
        if CREATE_NEW in selections:
            new_selection = create_new()
            selections.append(new_selection)
            return selections
        return selections
    except TypeError:
        selections = cast(str, selections)
        if selections == CREATE_NEW:
            new_selection = create_new()
            return [new_selection]
        return [selections]


def load_and_select_or_create(
    console: Console, selection_type: SelectionType, is_multiselect=False
) -> list[str]:
    console.print(f"Select {selection_type.name}")
    choices = read_choices_for_selection_type_from_db(selection_type)
    # TODO append "CREATE NEW" / other to choices.. => can use preprocessor lambda fx
    if is_multiselect:
        selections = select_multiple(choices, return_indices=False)
        selections = cast(list[str], selections)
        return handle_create_new(selections, selection_type)

    selection = select(choices, strict=True)
    assert selection
    selection = cast(str, selection)
    return handle_create_new(selection, selection_type)


def get_date():
    if confirm("Use today's date"):
        date = get_todays_date()
    else:
        date = prompt("Enter a date", validator=date_validator)  # TODO target types..
    return date


def get_entry_data(console: Console, date: date):
    focus_area = load_and_select_or_create(console, SelectionType.FOCUS_AREA)
    focus_area = cast(str, focus_area)
    project = load_and_select_or_create(console, SelectionType.PROJECT, True)
    activity_type = load_and_select_or_create(
        console, SelectionType.ACTIVITY_TYPE, True
    )

    description = prompt("Descibe work done", target_type=str)
    times_worked = prompt("Enter times worked (ex: 12,34,45)")
    times_worked_values = extract_constant_values_from_string(times_worked)

    entry = Entry(
        date, focus_area, project, activity_type, description, times_worked_values
    )

    return entry
