from enum import Enum
from date_helpers import format_date


from dataclasses import dataclass
from datetime import date


@dataclass
class Entry:
    date: date
    focus_area: str
    project: str
    activity_type: str
    description: str
    times_worked: list[int]

    @property
    def confimation_message(self):
        return f"[bold]\n Confirm entry is correct: \n On {format_date(self.date)} worked on `{self.description}` for {sum(self.times_worked)} minutes \n Focus area: {self.focus_area} | Projects: {self.project} |  Activity type: {self.activity_type} \n"


class SelectionType(Enum):
    FOCUS_AREA = 0  # PhD, Foundations, Blog, CEE243, BACS
    PROJECTS = 1  # PhD -> Geomeppy, SVG2Code, Paper1 (can be multiple), Foundations -> Stats, Vector Calc, G.Theory, Blog -> certain book summaries?, Admin -> NoProject, just descriptions..
    ACTIVITY_TYPE = (
        2  # Focus area agnostic -> coding, reading, writing, gathering resources, etc
    )

@dataclass
class ReturnedEntry:
    id: int
    date: str
    focus_area: str
    project: str
    description: str
    minutes: int
    activity_type: str


