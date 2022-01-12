import pandas as pd
import numpy as np
import datetime

def water_year(date):
    ''' 
	this returns an integer water year of the date 
	'''

    def wy(date):
        if date.month < 10:
            return date.year
        else:
            return date.year + 1

    if isinstance(date, pd.Series):
        return date.apply(wy)
    if isinstance(date, datetime.datetime):
        return wy(date)
    elif isinstance(date, pd.DatetimeIndex):
        return [wy(i) for i in date]
    else:
        import warnings
        warnings.warn('not a Series/datetime/DatetimeIndex object')
        # print('not a Series/datetime/DatetimeIndex object')
        return np.nan


def julian_water_year(date):
    '''
    return days from start of water year, creates pseudo date from 2020.
    Args:
        date: SERIES of dates (does not work with datetime index)

    Returns:

    '''

    wy = water_year(date)

    wystart = [datetime.datetime(year-1,10,1,0,0,0) for year in wy]
    wystart = pd.Series(wystart)
    days_from_start = date-wystart
    # df = datetime.datetime(2000,10,1,0,0,0)+days_from_start-pd.to_timedelta(1, unit = 'D')
    df = datetime.datetime(2000, 10, 1, 0, 0, 0) + days_from_start
    df = df.values

    return df
