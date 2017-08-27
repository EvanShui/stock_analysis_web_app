from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import output_notebook
from bokeh.models import HoverTool
from bokeh.models.widgets import Panel, Tabs
from datetime import date, timedelta
from dateutil.relativedelta import *
import numpy as np
import pandas as pd

def data_to_CDS(start_date):
    df = data.DataReader(name=stock_ticker, data_source="google", start=start_date, end=date.today())
    source = ColumnDataSource(data=dict(
        date=np.array(df['Close'].index, dtype=np.datetime64),
        price=np.array(df['Close'].values)
    ))
    return source

def plot(p, source):
    p.line('date', 'price', source=source)

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]
date_titles = ["week", "month", "3 months", "6 months", "year", "5 years"]
start = datetime.datetime(2016, 3, 1)
source = None
stock_ticker = "ATVI"

hover = HoverTool(tooltips=[
    ("date", "@date{%F}"),
    ("Price", "$@price{0.2f}"),
    ("index", "$index")
],
    formatters={
        "date": "datetime"
    },
    mode="vline"
)
source1 = data_to_CDS(delta_7_days)
source2 = data_to_CDS(delta_month)

p1 = figure(x_axis_type='datetime', width=500, height=200,
           title="week")
p2 = figure(x_axis_type='datetime', width=500, height=200,
            title="month")
figures = [figure(x_axis_type='datetime', width=500, height=200,
           title=title) for title in date_titles]

p1.add_tools(HoverTool(tooltips=[
    ("date", "@date{%F}"),
    ("Price", "$@price{0.2f}"),
    ("index", "$index")
],
    formatters={
        "date": "datetime"
    },
    mode="vline"
))

p2.add_tools(HoverTool(tooltips=[
    ("date", "@date{%F}"),
    ("Price", "$@price{0.2f}"),
    ("index", "$index")
],
    formatters={
        "date": "datetime"
    },
    mode="vline"
))
plot(p1, source1)
plot(p2, source2)
tab1 = Panel(child=p1,title="week")
tab2 = Panel(child=p2,title="month")

sources = [data_to_CDS(date) for date in dates]
source = data_to_CDS(datetime.datetime(2016,3,1))

tabs = Tabs(tabs=[tab1, tab2])
output_file("python_analyzer.html")
show(tabs)