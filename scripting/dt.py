"""
A collection of date/time conversion functions and shortcuts.
"""

import datetime

def timestring(dt):
    if dt.day > 9:
        return "%s-%s-%s" % (dt.year, dt.month, dt.day)
    else:
        return "%s-%s-0%s" % (dt.year, dt.month, dt.day)

date_format = r"%Y%m%d"
time_format = r"%H%M%S.%f"
timef_nomicro = r"%H%M%S"
datetime_format = date_format + time_format
datef_delimited = r"%Y-%m-%d"
timef_delimited =  r"%H:%M:%S:%f"
timef_nomicro_delimited = r"%H:%M:%S"
datetime_nomicro_delimited = "%s %s" % (datef_delimited, timef_nomicro_delimited)
default_python_format = r'%Y-%m-%d %H:%M:%S.%f'

def dt2s(format_string):
    """Return a function to convert datetime to string
    
    dt.dt2s(dt.datef_delimited)(dt.today_now())
    """
        
    def fn(dt):
        return dt.strftime(format_string)
    return fn

def s2dt(format_string):
    """Return a function to convert string to datetime

    dt.s2dt(dt.datef_delimited)('2015-07-31')
    """
    def fn(strng):
        return datetime.datetime.strptime(strng, format_string)
    return fn

date_string = dt2s(date_format)
time_string = dt2s(time_format)
datetime_string = dt2s(datetime_format)

date_string_todt = s2dt(date_format)
time_string_todt = s2dt(time_format)
date_delimited_todt = s2dt(datef_delimited)
datetime_string_todt = s2dt(datetime_format)
default_string_todt = s2dt(default_python_format)

def today_now():
    return datetime.datetime.today()

def days(num):
    return datetime.timedelta(num)

def timelist(start_date, end_date, converter=date_delimited_todt):
    startd = converter(start_date)
    total_days = converter(end_date) - startd
    return [timestring(startd + days(x)) for x in range(total_days.days)]

def today():
    return timestring(datetime.datetime.today())

def yesterday():
    return timestring(datetime.datetime.today() - datetime.timedelta(1))

def test_timelist():
    return timelist('2015-07-22', '2015-07-31')

def from_today(end_date_string):
    end_date=s2dt(datetime_nomicro_delimited)(end_date_string)
    return end_date - today_now()
