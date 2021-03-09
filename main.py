''' Create a simple stocks correlation dashboard.
Choose stocks to compare in the drop down widgets, and make selections
on the plots to update the summary and histograms accordingly.
.. note::
    Running this example requires downloading sample data. See
    the included `README`_ for more information.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve stocks
at your command prompt. Then navigate to the URL
    http://localhost:5006/stocks
.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md
'''
from functools import lru_cache
from os.path import dirname, join

import pandas as pd
import numpy as np

from datetime import datetime, timedelta

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, PreText, Select, Range1d, LinearAxis, RangeTool, HoverTool
from bokeh.plotting import figure

DATA_DIR = join(dirname(__file__), 'data')

DATA_SOURCES = ['Outside temperature', 'Kitchen temperature', 'Bathroom temperature', 'Filament temperature', 'Outside humidity', 'Kitchen humidity', 'Bathroom humidity', 'Filament humidity', 'Outside battery', 'Kitchen battery', 'Bathroom battery', 'Filament battery']

def nix(val, lst):
    return [x for x in lst if x != val]

@lru_cache()
def load_data():
    fname = join(DATA_DIR, 'home_sensors_v1.csv')
    data = pd.read_csv(fname, header=None, parse_dates=['date'],
                       names=['date', 'kitchen_temp', 'kitchen_hum', 'kitchen_bat', 'outside_temp', 'outside_hum', 'outside_bat', 'filament_temp', 'filament_hum', 'filament_bat', 'bathroom_temp', 'bathroom_hum', 'bathroom_bat'])
    data = data.set_index('date')
    return data#pd.DataFrame({ticker: data.c, ticker+'_returns': data.c.diff()})

@lru_cache()
def get_data():
    data = load_data()
    return data

def load_initial_data():
    data = get_data()
    source.data = data
    source_static.data = data

# set up widgets

stats = PreText(text='', width=300, height=400, sizing_mode='fixed', width_policy="fixed", min_width=300)
ticker1 = Select(value='Outside temperature', options=nix('Outside humidity', DATA_SOURCES), sizing_mode='fixed', width=300, height=25)
ticker2 = Select(value='Outside humidity', options=nix('Outside temperature', DATA_SOURCES), sizing_mode='fixed', width=300, height=25)

# set up plots

source = ColumnDataSource(data=dict(date=[], kitchen_temp=[], kitchen_hum=[], kitchen_bat=[], outside_temp=[], outside_hum=[], outside_bat=[], filament_temp=[], filament_hum=[], filament_bat=[], bathroom_temp=[], bathroom_hum=[], bathroom_bat=[], x_data=[], y_data=[]))
source_static = ColumnDataSource(data=dict(date=[], kitchen_temp=[], kitchen_hum=[], kitchen_bat=[], outside_temp=[], outside_hum=[], outside_bat=[], filament_temp=[], filament_hum=[], filament_bat=[], bathroom_temp=[], bathroom_hum=[], bathroom_bat=[]))

load_initial_data()


corr = figure(tools='pan,wheel_zoom,box_select,reset', sizing_mode='stretch_width', width_policy="min", height=400, width=400)#, max_width=500)
corr.circle('x_data', 'y_data', size=2, source=source,
            selection_color="orange", alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)

corr.add_tools(HoverTool(
    tooltips=[
        ( 'Date', '@date{%Y-%m-%d %H:%M:%S}' ),
        ( 'X', '$x' ), # use @{ } for field names with spaces
        ( 'Y', '$y' ),
    ],

    formatters={
        "@date": "datetime", # use 'datetime' formatter for 'date' field
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='mouse',
))

corr.toolbar.active_drag = None
corr.toolbar.logo = None

#corr.sizing_mode = 'scale_both'

# https://docs.bokeh.org/en/latest/docs/reference/colors.html

##########################################
### Main temperature and humidity plot ###
##########################################
tools = 'pan,wheel_zoom,xbox_select,reset'
temp_plot = figure(plot_width=920, plot_height=500, tools=tools, x_axis_type='datetime', active_drag="xbox_select", y_range=(-5, 35), x_range=(datetime.now() - timedelta(days=7), datetime.now()), sizing_mode='stretch_both', width_policy='min', min_width=920)
temp_plot_plot1a = temp_plot.line('date', 'kitchen_temp', source=source_static, legend_label="Kitchen temperature", name="Kitchen temperature")
temp_plot_plot2a = temp_plot.line('date', 'outside_temp', source=source_static, legend_label="Outside temperature", name="Outside temperature", line_color="tomato")
temp_plot_plot3a = temp_plot.line('date', 'bathroom_temp', source=source_static, legend_label="Bathroom temperature", name="Bathroom temperature", line_color="green")
temp_plot_plot4a = temp_plot.line('date', 'filament_temp', source=source_static, legend_label="Filament temperature", name="Filament temperature", line_color="goldenrod", visible=False)

temp_plot_plot1b = temp_plot.circle('date', 'kitchen_temp', size=2, source=source, color=None, selection_color="orange")
temp_plot_plot2b = temp_plot.circle('date', 'outside_temp', size=2, source=source, color=None, selection_color="orange")
temp_plot_plot3b = temp_plot.circle('date', 'bathroom_temp', size=2, source=source, color=None, selection_color="orange")
temp_plot_plot4b = temp_plot.circle('date', 'filament_temp', size=2, source=source, color=None, selection_color="orange")

temp_plot.extra_y_ranges = {"hum": Range1d(start=-5, end=100)}
temp_plot.add_layout(LinearAxis(y_range_name="hum"), 'right')

temp_plot_plot5a = temp_plot.line('date', 'kitchen_hum', source=source_static, y_range_name="hum", legend_label="Kitchen humidity", name="Kitchen humidity", line_dash="dashed", visible=False)
temp_plot_plot6a = temp_plot.line('date', 'outside_hum', source=source_static, y_range_name="hum", legend_label="Outside humidity", name="Outside humidity", line_dash="dashed", line_color="tomato", visible=False)
temp_plot_plot7a = temp_plot.line('date', 'bathroom_hum', source=source_static, y_range_name="hum", legend_label="Bathroom humidity", name="Bathroom humidity", line_dash="dashed", line_color="green", visible=False)
temp_plot_plot8a = temp_plot.line('date', 'filament_hum', source=source_static, y_range_name="hum", legend_label="Filament humidity", name="Filament humidity", line_dash="dashed", line_color="goldenrod", visible=False)

temp_plot_plot5b = temp_plot.circle('date', 'kitchen_hum', size=2, source=source, color=None, selection_color="orange", y_range_name="hum")
temp_plot_plot6b = temp_plot.circle('date', 'outside_hum', size=2, source=source, color=None, selection_color="orange", y_range_name="hum")
temp_plot_plot7b = temp_plot.circle('date', 'bathroom_hum', size=2, source=source, color=None, selection_color="orange", y_range_name="hum")
temp_plot_plot8b = temp_plot.circle('date', 'filament_hum', size=2, source=source, color=None, selection_color="orange", y_range_name="hum")

temp_plot.add_tools(HoverTool(
    tooltips=[
        ( 'Date',   '@date{%Y-%m-%d %H:%M:%S}' ),
        ( 'Value',  '$y' ), # use @{ } for field names with spaces
        ( 'Name', '$name' ),
    ],

    formatters={
        "@date"      : "datetime", # use 'datetime' formatter for 'date' field
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='mouse',
    renderers=[temp_plot_plot1a, temp_plot_plot2a, temp_plot_plot3a, temp_plot_plot4a, temp_plot_plot5a, temp_plot_plot6a, temp_plot_plot7a, temp_plot_plot8a]
))

temp_plot.legend.location = "top_left"
temp_plot.legend.click_policy="hide"

temp_plot.title.text = "Temperature and humidity data"

temp_plot.toolbar.active_drag = None
temp_plot.toolbar.logo = None

#temp_plot.sizing_mode = 'scale_both'

####################################################################################################

##########################################
###             Range tool             ###
##########################################
select = figure(title="Drag the middle and edges of the selection box to change the range of plots",
                plot_height=130, plot_width=920, y_range=temp_plot.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef", height_policy="fixed", min_width=920)

range_tool = RangeTool(x_range=temp_plot.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'kitchen_temp', source=source_static)
select.line('date', 'outside_temp', source=source_static, line_color="tomato")
select.line('date', 'bathroom_temp', source=source_static, line_color="green")
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

select.sizing_mode = 'stretch_width'

####################################################################################################

battery_plot = figure(plot_width=200, plot_height=400, tools=tools, x_axis_type='datetime', active_drag="xbox_select", sizing_mode='stretch_width', height_policy="max", width_policy="max", max_height=400, min_height=200, min_width=100, max_width=3000)
battery_plot.x_range = temp_plot.x_range
battery_plot_plot1a = battery_plot.line('date', 'kitchen_bat', source=source_static, name="Kitchen battery", legend_label="Kitchen battery")
battery_plot_plot2a = battery_plot.line('date', 'outside_bat', source=source_static, line_color="tomato", name="Outside battery", legend_label="Outside battery")
battery_plot_plot3a = battery_plot.line('date', 'bathroom_bat', source=source_static, line_color="green", name="Bathroom battery", legend_label="Bathroom battery")
battery_plot_plot4a = battery_plot.line('date', 'filament_bat', source=source_static, line_color="goldenrod", name="Filament battery", legend_label="Filament battery")

battery_plot_plot1b = battery_plot.circle('date', 'kitchen_bat', size=2, source=source, color=None, selection_color="orange")
battery_plot_plot2b = battery_plot.circle('date', 'outside_bat', size=2, source=source, color=None, selection_color="orange")
battery_plot_plot1b = battery_plot.circle('date', 'bathroom_bat', size=2, source=source, color=None, selection_color="orange")
battery_plot_plot2b = battery_plot.circle('date', 'filament_bat', size=2, source=source, color=None, selection_color="orange")

battery_plot.add_tools(HoverTool(
    tooltips=[
        ( 'Date',   '@date{%Y-%m-%d %H:%M:%S}' ),
        ( 'Value',  '$y' ), # use @{ } for field names with spaces
        ( 'Name', '$name' ),
    ],

    formatters={
        "@date"      : "datetime", # use 'datetime' formatter for 'date' field
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='mouse',
    renderers=[battery_plot_plot1a, battery_plot_plot2a, battery_plot_plot3a, battery_plot_plot4a]
))

battery_plot.legend.location = "bottom_left"
battery_plot.legend.click_policy="hide"

battery_plot.title.text = "Battery"

battery_plot.toolbar.active_drag = None
battery_plot.toolbar.logo = None

#battery_plot.sizing_mode = 'scale_both'

# set up callbacks

def ticker1_change(attrname, old, new):
    ticker2.options = nix(new, DATA_SOURCES)
    update()

def ticker2_change(attrname, old, new):
    ticker1.options = nix(new, DATA_SOURCES)
    update()

def eval_ticker_selection(ticker_val):
    ticker_lut = {'Outside temperature': 'outside_temp',
                  'Kitchen temperature': 'kitchen_temp',
                  'Bathroom temperature': 'bathroom_temp',
                  'Filament temperature': 'filament_temp',
                  'Outside humidity': 'outside_hum',
                  'Kitchen humidity': 'kitchen_hum',
                  'Bathroom humidity': 'bathroom_hum',
                  'Filament humidity': 'filament_hum',
                  'Outside battery': 'outside_bat',
                  'Kitchen battery': 'kitchen_bat',
                  'Bathroom battery': 'bathroom_bat',
                  'Filament battery': 'filament_bat'
    }

    return ticker_lut[ticker_val]


def update(selected=None):

    data = get_data()
    #data = df[['t1', 't2', 't1_returns', 't2_returns']]
    source.data = data
    source_static.data = data

    source.data['x_data'] = source.data[eval_ticker_selection(ticker1.value)]
    source.data['y_data'] = source.data[eval_ticker_selection(ticker2.value)]

    update_stats(data)

    corr.title.text = '%s vs. %s' % (ticker1.value, ticker2.value)
    #temp_plot.title.text, ts2.title.text = "a", "b"

def update_stats(data):
    #print(data['kitchen_temp'].mean(), data['kitchen_temp'].min())
    d = {'Avg': [data['kitchen_temp'].mean(), data['outside_temp'].mean(), data['bathroom_temp'].mean(), data['filament_temp'].mean(),
                 data['kitchen_hum'].mean(), data['outside_hum'].mean(), data['bathroom_hum'].mean(), data['filament_hum'].mean(),
                 data['kitchen_bat'].mean(), data['outside_bat'].mean(), data['bathroom_bat'].mean(), data['filament_bat'].mean()
                ],
         'Min': [data['kitchen_temp'].min(), data['outside_temp'].min(), data['bathroom_temp'].min(), data['filament_temp'].min(),
                 data['kitchen_hum'].min(), data['outside_hum'].min(), data['bathroom_hum'].min(), data['filament_hum'].min(),
                 data['kitchen_bat'].min(), data['outside_bat'].min(), data['bathroom_bat'].min(), data['filament_bat'].min()
                ],
         'Max': [data['kitchen_temp'].max(), data['outside_temp'].max(), data['bathroom_temp'].max(), data['filament_temp'].max(),
                 data['kitchen_hum'].max(), data['outside_hum'].max(), data['bathroom_hum'].max(), data['filament_hum'].max(),
                 data['kitchen_bat'].max(), data['outside_bat'].max(), data['bathroom_bat'].max(), data['filament_bat'].max()
                ]
         }
    df = pd.DataFrame(data=d, index=['Kitchen temp.','Outside temp.','Bathroom temp.','Filament temp.','Kitchen hum.','Outside hum.','Bathroom hum.','Filament hum.', 'Kitchen bat.', 'Outside bat.', 'Bathroom bat.', 'Filament bat.'])
    stats.text = str(df.round(2))

ticker1.on_change('value', ticker1_change)
ticker2.on_change('value', ticker2_change)

def selection_change(attrname, old, new):
    #t1, t2 = ticker1.value, ticker2.value
    data = get_data()
    selected = source.selected.indices
    if selected:
        data = data.iloc[selected, :]
    update_stats(data)

    if temp_plot_plot1a.visible:
        temp_plot_plot1b.visible = True
    else:
        temp_plot_plot1b.visible = False

    if temp_plot_plot2a.visible:
        temp_plot_plot2b.visible = True
    else:
        temp_plot_plot2b.visible = False

    if temp_plot_plot3a.visible:
        temp_plot_plot3b.visible = True
    else:
        temp_plot_plot3b.visible = False

    if temp_plot_plot4a.visible:
        temp_plot_plot4b.visible = True
    else:
        temp_plot_plot4b.visible = False

    if temp_plot_plot5a.visible:
        temp_plot_plot5b.visible = True
    else:
        temp_plot_plot5b.visible = False

    if temp_plot_plot6a.visible:
        temp_plot_plot6b.visible = True
    else:
        temp_plot_plot6b.visible = False

    if temp_plot_plot7a.visible:
        temp_plot_plot7b.visible = True
    else:
        temp_plot_plot7b.visible = False

    if temp_plot_plot8a.visible:
        temp_plot_plot8b.visible = True
    else:
        temp_plot_plot8b.visible = False

source.selected.on_change('indices', selection_change)

# set up layout
main_row = column(temp_plot, select, sizing_mode='stretch_both', width_policy="max", min_width=920)
widgets = column(ticker1, ticker2, stats, sizing_mode='fixed', width=300, height=400)
second_row = row(battery_plot, corr, widgets, sizing_mode='scale_width', height_policy="max", width_policy="min", max_height=400, min_width=920)
#second_row = row(battery_plot, statistics, sizing_mode='scale_width', height_policy="max", max_height=400, width_policy="min", min_width=200)
#widgets = column(ticker1, ticker2, stats)
#main_row = row(corr, widgets)
#series = column(temp_plot, ts2, ts3)
#series2 = column(ts2, ts3)
#series_sum = row(series, series2)
#series_sum2 = column(select, series_sum)

#layout = column(main_row, second_row)

main_layout = column(main_row, sizing_mode='stretch_both', height_policy="min", width_policy="min", min_height=500, min_width=920)
layout = column(main_layout, second_row, sizing_mode='stretch_both', height_policy="min", width_policy="min", min_height=900, min_width=920) 

# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Home sensors"
