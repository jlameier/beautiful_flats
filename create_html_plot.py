
import io
from base64 import b64encode

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

buffer = io.StringIO()

### loading ###

df = pd.read_csv('src/data_for_dask.csv')
post_codes = sorted(set(df['address']))
eurpm_flat = {}
for element in post_codes:
    matching_ids = df[df['address'] == element]
    lst_price_postid = []
    lst_machting_ids = matching_ids['address']
    for flat_id in lst_machting_ids.index:
        lst_price_postid.append(df.loc[flat_id]['price']/df.loc[flat_id]['space1'])
    eurpm_flat[element] = sum(lst_price_postid) / len(lst_price_postid)

#############
# df = px.data.iris()
fig = px.scatter(
    df, x=eurpm_flat.keys(), y=eurpm_flat.values())
fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),
    html.A(
        html.Button("Download HTML"),
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )
])

app.run_server(debug=True,host="0.0.0.0", port="8050")


"""

import plotly as py
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import time as dt_tm
from datetime import date as dt_date

from chart_studio import plotly as py
import plotly.tools as plotly_tools
import plotly.graph_objects as go

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
# from mpl_finance import yahoofi
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde

from IPython.display import HTML

x = []
y = []
ma = []

def moving_average(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

date1 = dt_date( 2014, 1, 1 )
date2 = dt_date( 2014, 12, 12 )
quotes = pd.read_csv('yahoofinance-INTC-19950101-20040412.csv',
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True)
if len(quotes) == 0:
    print ("Couldn't connect to yahoo trading database")
else:
    dates = [q for q in quotes.index.values]
    y = [q for q in quotes['Open']]
#    for date in dates:
#        x.append(datetime.fromordinal(int(date))\
#                .strftime('%Y-%m-%d')) # Plotly timestamp format
    x = dates
    ma = moving_average(y, 10)

    xy_data = go.Scatter(x=x, y=y, mode='markers', marker=dict(size=4), name='AAPL')
    # vvv clip first and last points of convolution
    mov_avg = go.Scatter(x=x[5:-4], y=ma[5:-4], \
                         line=dict(width=2, color='red'), name='Moving average')
    data = [xy_data, mov_avg]

    py.iplot(data, filename='apple stock moving average')
"""