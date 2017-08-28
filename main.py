from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import output_notebook
from bokeh.models import HoverTool, OpenURL, TapTool
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
    p.line('date', 'price', source=source, line_width=2)
    p.circle('date', 'price', size=5, source=source, fill_color='white')


def string_to_datetime(string):
    return datetime.datetime.fromtimestamp(string / 1e3)


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
month = str(1)
day = str(1)
year = str(2011)
url ="https://www.google.com/search?q=" + "@date[%F]"
print(url.split("=")[1])
sources_list = [data_to_CDS(date) for date in dates]
figures_list = [figure(x_axis_type='datetime', width=1500, height=400, tools="tap",
           title=title) for title in date_titles]
fig_source_tuple_list = zip(figures_list,sources_list)
fig_date_tuple_list = zip(figures_list, date_titles)
for fig, source in fig_source_tuple_list:
    fig.add_tools(HoverTool(tooltips=[
        ("date", "@date{%F}"),
        ("Price", "$@price{0.2f}"),
        ("index", "$index")
    ],
        formatters={
            "date": "datetime"
        },
        mode="vline"
    ))
    plot(fig, source)
    fig.select(type=TapTool).callback = OpenURL(url=url)
tab_list = [Panel(child=fig, title=date_title) for fig, date_title in fig_date_tuple_list]
tabs = Tabs(tabs=tab_list)
output_file("python_analyzer.html")
show(tabs)

'''
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
tabs = Tabs(tabs=[tab1, tab2])
'''