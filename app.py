import os


import plotly.express as px
from dash.dependencies import Input, Output
from dash import dash_table as dt
import plotly.graph_objects as go

import dash
import dash.dcc as dcc
import dash.html as html
# import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd
import get_precip_wy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

options = ['Venado',
           'Santa Rosa']


def get_cur_station(stat = 'Santa Rosa'):
    df = get_precip_wy.get_precip(stat)
    if df is None:
        return None

    df = df.set_index('wy_date')
    df_tot = pd.DataFrame()
    for g, dfi in df.groupby('wy'):
        dfall = dfi.sort_values('wy_date').cumsum()
        dfall.loc[:,'wy'] = g
        df_tot = df_tot.append(dfall)
    df = df_tot.reset_index(drop = False)

    return df

def get_allstations():
    ogdict = {key:get_cur_station(key) for key in options}

    #remove stations witout any data
    dfall = {k: v for k, v in ogdict.items() if v is not None}

    return dfall


def get_group(station, dfall):
    return dfall[station]

def get_station_min_max(df):
    # get min and max years
    dfstats = df[df.wy_date.dt.month==9].groupby('wy').max().sort_values('Value')
    xmin = dfstats.index.values[:2]
    xmind = {f'{xmin[0]} - Driest':xmin[0] }
    xmind[f'{xmin[1]} - Second Driest'] = xmin[1]
    # xmind[f'{xmin[2]} - Third Driest '] =  xmin[2]

    dfstats = df[df.wy_date.dt.month==9].groupby('wy').max().sort_values('Value', ascending=False)
    xmax = dfstats.index.values[:2]
    xmaxd = {f'{xmax[0]} - Wettest':xmax[0] }
    xmaxd[f'{xmax[1]} - Second Wettest'] = xmax[1]
    # xmaxd[f'{xmax[2]} - Third Wettest'] = xmax[2]

    extremes = pd.Series(xmin)
    extremes = extremes.append(pd.Series(xmax))

    return xmind, xmaxd, extremes

dfall = get_allstations()


app.layout = html.Div([
    html.H2('Sonoma County Precipitation and Climatology'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in dfall.keys()],
        value='Santa Rosa'
    ),
    dcc.Graph(id = 'graph')
])

@app.callback(dash.dependencies.Output('graph', 'figure'),
                [dash.dependencies.Input('dropdown', 'value')])
def update_figure(station):
    # filtered_df = df[df.year == selected_year]

    df = get_group(station, dfall)

    # get last 6 years. exclude years in min/max lists
    filtered_df = df.copy()
    maxyear = pd.Timestamp.now().year - 7
    # cur_year = pd.np.arange(maxyear,2030,1)

    xmind, xmaxd, extremes = get_station_min_max(df)

    curf_df = filtered_df.loc[~filtered_df.wy.isin(extremes),:]
    curr_df = curf_df.query(f"wy>={maxyear}")

    fig = px.line(curr_df, x="wy_date", y="Value",
                color="wy", hover_name="wy",height = 1000,
                labels = {"wy_date": "Day of Year",
                "Value": "Precipitation (Inches)", },)

    fig.update_traces(line=dict(width=3))


    for v in xmind.keys():
        cur_df = filtered_df.query(f"wy=={xmind[v]}")
        fig.add_trace(go.Scatter(x=cur_df.loc[:,'wy_date'], y=cur_df.loc[:,'Value'],
                                 mode='none', name=v))

    for v in xmaxd.keys():
        cur_df = filtered_df.query(f"wy=={xmaxd[v]}")
        fig.add_trace(go.Scatter(x=cur_df.loc[:,'wy_date'], y=cur_df.loc[:,'Value'],
                                 mode='none', name=v))


    av_df = filtered_df.groupby('wy_date').mean().rolling(7).mean()
    fig.add_trace(go.Scatter(x=av_df.reset_index().loc[:,'wy_date'], y=av_df.loc[:,'Value'], fill='tozeroy',
                             mode='none', line_color='black',
                             fillcolor='rgba(135,206,235,.5)', name='Historic Daily Average'))
    fig.update_layout(hovermode="x")
    fig.update_traces(mode="lines", hovertemplate='%{y:,d} <i>in.</i>')
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            # opacity = 100,
            font_size=16,
            font_family="Rockwell"
        ))
    fig.update_xaxes(tickformat="%b %d")
    # fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
