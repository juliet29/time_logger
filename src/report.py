import datetime

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from copy import deepcopy
import seaborn.objects as so
import plotly.express as px
import pandas as pd


from variables import get_db_path
from db_commands.connect import connect_to_real_db 
from db_commands.read import read_all_entries, aggregate_focus_project_date


def make_plot():
    connection = connect_to_real_db(get_db_path())
    df = read_all_entries(connection)
    df_agg = aggregate_focus_project_date(df)
    df_agg = df_agg.group_by("focus_area", "date").agg(pl.col("elapsed_time").sum())

    df_pandas = df_agg.with_columns(elapsed_time=pl.col("elapsed_time").cast(datetime.timedelta)).to_pandas()
    df_pandas["elapsed_time"] = df_pandas["elapsed_time"].dt.to_pytimedelta()

    min_time = df_pandas["elapsed_time"].min()
    max_time = df_pandas["elapsed_time"].max()
    tick_values = pd.timedelta_range(min_time, max_time, periods=8)
    tick_ints = tick_values.astype(int)
    format_timedelta = lambda v: f"{v.components.hours:0>2d}h{v.components.minutes:0>2d}m"
    tick_strings = [format_timedelta(i) for i in tick_values]
    df_pandas["Time"] = df_pandas["elapsed_time"].apply(format_timedelta)

    fig = px.bar(df_pandas, x='date', y='elapsed_time', color="focus_area", hover_name="focus_area", hover_data={"date": True, "focus_area": False, "Time": True, "elapsed_time": False})
    fig.update_layout(yaxis={
            "tickmode": "array",
            "tickvals": tick_ints,
            "ticktext": tick_strings
    })


    fig.show()


if __name__ == "__main__":
    make_plot()