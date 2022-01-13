import pandas as pd
import helpers


def get_precip(ts, raw = False):
    ts_ids = {'Venado': "1964010",
              'Santa Rosa': "1976010",
              'Ukiah':'1977010'}

    ts = ts_ids[ts]

    t = r"https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=csv&ts_id={:}&from=1990-01-01&"

    url = t.format(ts)
    tab = pd.read_csv(url, sep=';', header=[2])

    if tab.shape[0] ==0:
        return None

    tab.loc[:, 'Date'] = pd.to_datetime(tab.loc[:, '#Timestamp'])

    # tab.loc[:, 'Date'] = pd.to_datetime(tab.loc[:, 'Date']).dt.tz_localize(None)
    tab.loc[:, 'Date'] = pd.to_datetime(tab.loc[:, 'Date']).dt.tz_convert(None)
    if raw:
        tab = tab.set_index('Date', drop=False)
        # tab = tab.resample("1D").mean()
        tab.loc[:, 'wy'] = helpers.water_year(tab.index)
        tab.loc[:, 'wy_date'] = helpers.julian_water_year(tab.rename(columns = {'Date':'ogdate'}).reset_index().loc[:, 'Date'])
        return tab

    tab = tab.set_index('Date', drop=True)
    tab = tab.resample("1D").mean()
    tab.loc[:, 'wy'] = helpers.water_year(tab.index)
    tab.loc[:, 'wy_date'] = helpers.julian_water_year(tab.reset_index().loc[:, 'Date'])

    return tab



def get_cur_station(stat = 'Santa Rosa'):
    __df = get_precip(stat)
    if __df is None:
        return None

    __df = __df.set_index('wy_date')
    df_tot = pd.DataFrame()
    for g, dfi in __df.groupby('wy'):
        dfall_ci = dfi.sort_values('wy_date').cumsum()
        dfall_ci.loc[:, 'wy'] = g
        df_tot = df_tot.append(dfall_ci)
    __df = df_tot.reset_index(drop = False)

    return __df

def get_allstations(options):
    if options is None:
        options = ['Santa Rosa', "Venado"]
    ogdict = {key:get_cur_station(key) for key in options}

    #remove stations witout any data
    __dfall = {k: v for k, v in ogdict.items() if v is not None}

    return __dfall


def get_group(station, dfall_i123):
    return dfall_i123[station]

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