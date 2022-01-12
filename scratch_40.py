# import pandas as pd
# import helpers
#
# def get_precip(ts):
#
#     ts_ids = {'Venado':"1964010"}
#
#     ts = ts_ids[ts]
#
#
#     t = r"https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=csv&ts_id={:}&from=1990-01-01&"
#
#     url = t.format(ts)
#     tab = pd.read_csv(url, sep = ';', header = [2])
#
#     tab.loc[:,'Date'] = pd.to_datetime(tab.loc[:,'#Timestamp'])
#
#     tab.loc[:,'Date'] =pd.to_datetime(tab.loc[:,'Date']).dt.tz_localize(None)
#
#     tab = tab.set_index('Date', drop = True)
#     tab = tab.resample("1D").mean()
#     # print(tab.columns)
#     #
#     # print(tab)
#     # print(tab.Date.dt.year)
#
#     # helpers.water_year(tab.Date)
#     tab.loc[:,'wy'] = helpers.water_year(tab.index)
#     tab.loc[:,'wy_date'] = helpers.julian_water_year(tab.reset_index().loc[:,'Date'])
#
#
#     return tab
import pandas as pd

# import get_precip_wy
#
# # df = get_precip_wy.get_precip('Santa Rosa')
# df = get_precip_wy.get_precip('Santa Rosa')
# df = df.set_index('wy_date')
# df_tot = pd.DataFrame()
# for g, dfi in df.groupby('wy'):
#     dfall = dfi.sort_values('wy_date').cumsum()
#     dfall.loc[:,'wy'] = g
#     df_tot = df_tot.append(dfall)
# df = df_tot.reset_index(drop = False)
#
# # df = df.groupby('wy').cumsum()
# # print(df_tot.index.loc[:,'wy_date'])
# print(df.head())
# xmax = df.reset_index().set_index('wy').loc[:,'Value'].idxmax()
# xmin = df.reset_index().set_index('wy').loc[:,'Value'].idxmin()
# print(xmax)
# print(xmin)
#
# dfstats = df.groupby('wy').max().sort_values('Value')
# xmax = dfstats.index.values[:2]
# xmin = dfstats.index.values[-2:]
# print(xmax)
# print(xmin)
# # print(dfstats)
# # print(df.reset_index().set_index('wy').loc[:,'Value'].head())
# cur_year = pd.Timestamp.now().year - 6
# curr_df = df.query(f"wy>={cur_year}")
#
# print(curr_df)

t = pd.read_json("https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet?Stations=VEN&SensorNums=45&dur_code=D&Start=1980-01-16&End=2022-01-12")

t.loc[:,'date'] = pd.to_datetime(t.loc[:,'obsDate'])
t = t.loc[~(t.loc[:,'value']<-10)]
print(t.loc[:,['date','value']])
t.plot()
