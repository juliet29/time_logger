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

MINUTES_TO_MS = 60*1000


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
        results =  c.fetchall()
        df = pl.DataFrame([r.__dict__ for r in results])
        return df

    
def aggregate_focus_project_date(df:pl.DataFrame):
    df = df.with_columns(
            minutes =MINUTES_TO_MS*pl.col("minutes").cast(pl.Duration(time_unit="ms"))
            )
    # rprint(df)
    d1 = df.group_by("focus_area", "project", "date").agg(pl.col("minutes").sum())
    # rprint(d1.dtypes)
    # rprint(d1.to_pandas())
    # rprint(d1.to_pandas().dtypes)

    return d1

def plot_focus_project_date(df:pl.DataFrame):
    # sns.barplot(df.to_pandas(), x="date", y="minutes", hue="focus_area")
    fig, ax = plt.subplots(nrows=1, figsize=(8, 6))
    dfp = df.to_pandas()
    # sns.barplot(df.to_pandas(), x="date", y="minutes", hue="focus_area", ax=ax)

    dfp.plot(x="date", y="minutes", kind="bar", ax=ax, stacked=True)

    ax.xaxis.set_ticks_position("bottom")
    ax.xaxis.set_major_locator(ticker.AutoLocator())

    # convert the ticks to string
    ticks = ax.get_yticks()
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.set_yticklabels(pd.to_datetime(ticks, unit='ms').strftime('%H:%M'))
    plt.show()


# def plot_focus_project_date_mpl(df:pl.DataFrame):
#     dfp = df.to_pandas()
#     fig = px.bar(df.to_pandas(), x='date', y='minutes', color="focus_area")
#     fig.show(renderer="png")
#     # fig.show()
   


# # TODO this should just not be here tbh.. run file should be outside, in app.py if anything.. 
# if __name__ == "__main__":
#     connection = connect_to_real_db(DB_PATH)
#     df = read_all_entries(connection)
#     df_agg = aggregate_focus_project_date(df)

#     plot_focus_project_date(df_agg)
#     # plot_focus_project_date_mpl(df_agg)

