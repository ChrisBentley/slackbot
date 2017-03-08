#!/usr/bin/env python

import pytz
from datetime import datetime, timedelta


def is_timezone_in_dst(zonename):

    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utcnow())

    return now.astimezone(tz).dst() != timedelta(0)


def now():

    # Check if the chosen timezone is currently observing daylight savings time
    dst = is_timezone_in_dst('Europe/London')

    # Get the current utc time
    utc_now = datetime.utcnow()

    if dst:
        # Add an hour if we are currently in dst
        correct_date_time = utc_now + timedelta(hours=1)
    else:
        # Otherwise the time will be in line with UTC time
        correct_date_time = utc_now

    return correct_date_time


(__name__ == '__main__' and now())