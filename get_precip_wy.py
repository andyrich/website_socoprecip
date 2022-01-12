import pandas as pd
import helpers


def get_precip(ts):
    ts_ids = {'Venado': "1964010",
              'Santa Rosa': "1976010"}

    ts = ts_ids[ts]

    t = r"https://www.kisters.net/sonomacountygroundwater/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=0&format=csv&ts_id={:}&from=1990-01-01&"

    url = t.format(ts)
    tab = pd.read_csv(url, sep=';', header=[2])

    if tab.shape[0] ==0:
        return None

    tab.loc[:, 'Date'] = pd.to_datetime(tab.loc[:, '#Timestamp'])

    tab.loc[:, 'Date'] = pd.to_datetime(tab.loc[:, 'Date']).dt.tz_localize(None)

    tab = tab.set_index('Date', drop=True)
    tab = tab.resample("1D").mean()
    # print(tab.columns)
    #
    # print(tab)
    # print(tab.Date.dt.year)

    # helpers.water_year(tab.Date)
    tab.loc[:, 'wy'] = helpers.water_year(tab.index)
    tab.loc[:, 'wy_date'] = helpers.julian_water_year(tab.reset_index().loc[:, 'Date'])

    return tab
