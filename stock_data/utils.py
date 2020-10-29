# Copyright (C) 2020 Mike Healey
# All rights reserved
#

from datetime import datetime


def get_datetime_from_basic(date_string):
    # expected format: 2019-02-26
    year, month, day = date_string.split("-")
    return datetime(int(year), int(month), int(day))


def get_datetime_from_iso(date_string):
    # expected format: 2018-02-07T12:48:47.000Z
    return datetime.fromisoformat(date_string.replace("Z", ""))
