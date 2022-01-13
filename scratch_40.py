# # import pandas as pd
# # import helpers
# #
# # def get_precip(ts):
# #
# #     ts_ids = {'Venado':"1964010"}
# #
# #     ts = ts_ids[ts]
# #
# #
# #     t = r"https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=csv&ts_id={:}&from=1990-01-01&"
# #
# #     url = t.format(ts)
# #     tab = pd.read_csv(url, sep = ';', header = [2])
# #
# #     tab.loc[:,'Date'] = pd.to_datetime(tab.loc[:,'#Timestamp'])
# #
# #     tab.loc[:,'Date'] =pd.to_datetime(tab.loc[:,'Date']).dt.tz_localize(None)
# #
# #     tab = tab.set_index('Date', drop = True)
# #     tab = tab.resample("1D").mean()
# #     # print(tab.columns)
# #     #
# #     # print(tab)
# #     # print(tab.Date.dt.year)
# #
# #     # helpers.water_year(tab.Date)
# #     tab.loc[:,'wy'] = helpers.water_year(tab.index)
# #     tab.loc[:,'wy_date'] = helpers.julian_water_year(tab.reset_index().loc[:,'Date'])
# #
# #
# #     return tab
# import pandas as pd
#
# import get_precip_wy
# #
# # # df = get_precip_wy.get_precip('Santa Rosa')
# # df = get_precip_wy.get_precip('Santa Rosa')
# # df = df.set_index('wy_date')
# # df_tot = pd.DataFrame()
# # for g, dfi in df.groupby('wy'):
# #     dfall = dfi.sort_values('wy_date').cumsum()
# #     dfall.loc[:,'wy'] = g
# #     df_tot = df_tot.append(dfall)
# # df = df_tot.reset_index(drop = False)
# #
# # # df = df.groupby('wy').cumsum()
# # # print(df_tot.index.loc[:,'wy_date'])
# # print(df.head())
# # xmax = df.reset_index().set_index('wy').loc[:,'Value'].idxmax()
# # xmin = df.reset_index().set_index('wy').loc[:,'Value'].idxmin()
# # print(xmax)
# # print(xmin)
# #
# # dfstats = df.groupby('wy').max().sort_values('Value')
# # xmax = dfstats.index.values[:2]
# # xmin = dfstats.index.values[-2:]
# # print(xmax)
# # print(xmin)
# # # print(dfstats)
# # # print(df.reset_index().set_index('wy').loc[:,'Value'].head())
# # cur_year = pd.Timestamp.now().year - 6
# # curr_df = df.query(f"wy>={cur_year}")
# #
# # print(curr_df)
# #
# # t = pd.read_json("https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet?Stations=VEN&SensorNums=45&dur_code=D&Start=1980-01-16&End=2022-01-12")
# #
# # t.loc[:,'date'] = pd.to_datetime(t.loc[:,'obsDate'])
# # t = t.loc[~(t.loc[:,'value']<-10)]
# # print(t.loc[:,['date','value']])
# # t.plot()
# import get_precip_wy
# options = ['Venado',
#            'Santa Rosa']
# #
# # def get_cur_station(stat = 'Santa Rosa'):
# #     __df = get_precip_wy.get_precip(stat)
# #     if __df is None:
# #         return None
# #
# #     __df = __df.set_index('wy_date')
# #     df_tot = pd.DataFrame()
# #     for g, dfi in __df.groupby('wy'):
# #         dfall = dfi.sort_values('wy_date').cumsum()
# #         dfall.loc[:,'wy'] = g
# #         df_tot = df_tot.append(dfall)
# #     __df = df_tot.reset_index(drop = False)
# #
# #     return __df
# #
# # def get_allstations():
# #     ogdict = {key:get_cur_station(key) for key in options}
# #
# #     #remove stations witout any data
# #     dfall = {k: v for k, v in ogdict.items() if v is not None}
# #
# #     return dfall
# #
# #
# # def get_group(station, dfall):
# #     return dfall[station]
# #
# # def get_station_min_max(df):
# #     # get min and max years
# #     dfstats = df[df.wy_date.dt.month==9].groupby('wy').max().sort_values('Value')
# #     xmin = dfstats.index.values[:2]
# #     print(xmin)
# #     xmind = {f'{xmin[0]} - Driest':xmin[0] }
# #     xmind[f'{xmin[1]} - Second Driest'] = xmin[1]
# #     # xmind[f'{xmin[2]} - Third Driest '] =  xmin[2]
# #
# #     dfstats = df[df.wy_date.dt.month==9].groupby('wy').max().sort_values('Value', ascending=False)
# #     xmax = dfstats.index.values[:2]
# #     xmaxd = {f'{xmax[0]} - Wettest':xmax[0] }
# #     xmaxd[f'{xmax[1]} - Second Wettest'] = xmax[1]
# #     # xmaxd[f'{xmax[2]} - Third Wettest'] = xmax[2]
# #
# #     extremes = pd.Series(xmin)
# #     extremes = extremes.append(pd.Series(xmax))
# #
# #     return xmind, xmaxd, extremes
#
import get_precip_wy
dfall = get_precip_wy.get_allstations(None)
#
#
# df = dfall['Venado']
# print(df)
# xmind, xmaxd, extremes = get_precip_wy.get_station_min_max(df)
#
# xxx = df.loc[df.wy_date.dt.month==9,:].groupby('wy').max().sort_values('Value')
#
# print(xxx)
#
# # xxx = df.loc[df.wy_date.dt.month==9,:].groupby('wy').max().sort_values('Value')
# xxx = df.loc[df.loc[:,'wy_date'].dt.month==9,:]
# xxx = xxx.query("wy==2020")
#
# print(xxx)
#
# # df.to_csv('sadf.csv')
#
# df = get_precip_wy.get_precip('Venado', True)
# df.to_csv('erase.csv')
# import plotly.graph_objects as go
# import plotly.express as px
# import numpy as np
#
# x = np.linspace(0, 10, 100)
# y1 = 12 - 10 * np.exp(-0.9*x)
# y2 = 10 - 10 * np.exp(-x)
#
# y3 = 6  + 10 * np.exp(-x)
# y4 = 5 + 10 * np.exp(-0.9*x)


colors = px.colors.qualitative.Plotly

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1, fill='tozeroy',  fillcolor=colors[0], line=dict(color=colors[0])))
fig.add_trace(go.Scatter(x=x, y=y2, fill='tozeroy', fillcolor='white', line=dict(color=colors[0])))

fig.add_trace(go.Scatter(x=x, y=y3, fill='tozeroy',  fillcolor=colors[1], line=dict(color=colors[1])))
fig.add_trace(go.Scatter(x=x, y=y4, fill='tozeroy', fillcolor='white', line=dict(color=colors[1])))

fig.update_layout(template="simple_white")
fig.show()