# from __init__ import *
from sqlite3 import Connection
import polars as pl

from db_commands.connect import connect_to_real_db
from interfaces import ReturnedEntry
from rich import print as rprint
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import plotly.express as px

MINUTES_TO_MS = 60 * 1000


def read_all_entries(connection: Connection):
    # TODO - flags that will control dates, etc..
    query = """SELECT entry_id, entry_date, project_focus_area, entry_project_name, description, minutes_elapsed, ea_activity_type_name
    FROM entry, time_elapsed, entered_activity, projects
    WHERE time_elapsed.time_entry_id = entry.entry_id 
    AND entered_activity.ea_entry_id = entry.entry_id
    AND projects.project_name = entry.entry_project_name
    """

    with connection:
        c = connection.cursor()
        c.row_factory = lambda _, row: ReturnedEntry(*row)
        c.execute(query)
        results = c.fetchall()
        df = pl.DataFrame([r.__dict__ for r in results])

        df = df.with_columns(
            elapsed_time=MINUTES_TO_MS
            * pl.col("minutes").cast(pl.Duration(time_unit="ms"))
        )
        return df


def aggregate_focus_project_date(df: pl.DataFrame):
    return df.group_by("focus_area", "project", "date").agg(
        pl.col("elapsed_time").sum()
    )
