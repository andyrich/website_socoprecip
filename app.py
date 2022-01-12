import os

import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dash_table as dt
import plotly.graph_objects as go

import dash
import dash.dcc as dcc
import dash.html as html
import pandas as pd
import get_precip_wy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

options = ['Venado',
           'Santa Rosa']


dfall = get_precip_wy.get_allstations(options=options)
today = pd.Timestamp.now().strftime('%A, %B %d %Y')

app.layout = html.Div([
    html.H2(f'Sonoma County Observed Precipitation for {today}'),
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

    df = get_precip_wy.get_group(station, dfall)

    # get last 6 years. exclude years in min/max lists
    filtered_df = df.copy()
    current_year = pd.Timestamp.now().year
    current_year = current_year if pd.Timestamp.now().month<10 else current_year+1
    maxyear = current_year - 7
    # cur_year = pd.np.arange(maxyear,2030,1)

    xmind, xmaxd, extremes = get_precip_wy.get_station_min_max(df)
    extremes = extremes.append(pd.Series([current_year]))

    curf_df = filtered_df.loc[~(filtered_df.wy.isin(extremes)),:]
    curr_df = curf_df.query(f"wy>={maxyear}")

    fig = px.line(curr_df, x="wy_date", y="Value",
                color="wy", hover_name="wy",height = 1000,
                labels = {"wy_date": "Water Year (October 1 - September 30)",
                "Value": "Precipitation (Inches)", },
                  title= station)

    curr_year_df = df.query(f"wy=={current_year}")
    fig.add_trace(go.Scatter(x=curr_year_df.loc[:, 'wy_date'], y=curr_year_df.loc[:, 'Value'],
                             mode='none', name=f"{current_year} - Current Water Year",
                        line = dict(color='firebrick', width=10)))
    # fig.update_traces(line=dict(color="RoyalBlue", width=10),
    #                   selector=dict(name="2022"))
    # fig.update_layout()


    for v in xmind.keys():
        cur_df = filtered_df.query(f"wy=={xmind[v]}")
        fig.add_trace(go.Scatter(x=cur_df.loc[:,'wy_date'], y=cur_df.loc[:,'Value'],
                                 mode='none', name=v))

    for v in xmaxd.keys():
        cur_df = filtered_df.query(f"wy=={xmaxd[v]}")
        fig.add_trace(go.Scatter(x=cur_df.loc[:,'wy_date'], y=cur_df.loc[:,'Value'],
                                 mode='none', name=v))


    av_df = df.groupby('wy_date').mean().rolling(7).mean()
    fig.add_trace(go.Scatter(x=av_df.reset_index().loc[:,'wy_date'], y=av_df.loc[:,'Value'],
                             # fill='None',
                             mode='none', line_color='black',
                             fillcolor='rgba(135,206,235,.5)', name='Historic Daily Average'))

    colors = px.colors.sequential.Cividis_r
    for cnt, quant in enumerate([[10,90], [20,80], ]):
        upper = df.groupby('wy_date').quantile(quant[0]/100).rolling(7).mean()
        lower = df.groupby('wy_date').quantile(quant[1]/100).rolling(7).mean()
        index = upper.reset_index().loc[:,'wy_date'].values
        xxi = upper.loc[:,'Value'].values
        yyi = lower.loc[:,'Value'].values
        print(xxi)
        print(index)
        fig.add_trace(go.Scatter(
            x=np.concatenate([index, index[::-1]]),
            y=np.concatenate([xxi, yyi[::-1]]),
            fill='toself',
            hoveron='points',
            line=dict(color='grey'),
            fillcolor = colors[cnt],
            opacity=0.2,
            name=f'{quant[0]}th - {quant[1]}th Percentile'),
        )


    fig.update_layout(hovermode="x")
    fig.update_traces(mode="lines", hovertemplate='%{y:,d} <i>in.</i>')
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ))
    fig.update_xaxes(tickformat="%b %d")
    fig.update_layout(legend_title_text='Water Year')
    # fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
