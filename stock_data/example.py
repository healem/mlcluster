# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging
import os
import pandas
import requests
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from shutil import rmtree


# Get the grouped daily for the whole US market for the first and last day of the month to analyze
# find all stocks that start and end under $10

# Get the following for the above stock:
# monthly aggregates of 1 min for the year
# stock financials, specifically for the float
# ticker news
# ticker details

# save to parquet file in gluster

logging.basicConfig(level=logging.DEBUG)

basedir = "/tmp/results"
minute_dir = "minute"
ticker_dir = "tickers"
news_dir = "news"
baseurl = "https://api.polygon.io"
key = os.environ.get("POLYGON_KEY")
session = requests.Session()
session.params["apiKey"] = key


def create_skeleton():
    for subdir in [minute_dir, ticker_dir, news_dir]:
        path = Path(f"{basedir}/{subdir}")
        path.mkdir(parents=True, exist_ok=True)


def delete_skeleton():
    rmtree(basedir)


def get_next_day(start_day):
    # Expects format year-month-day: 2019-02-20
    year, month, day = start_day.split("-")
    end = datetime(year, month, day) + timedelta(days=1)
    return f"{end.year}-{end.month}-{end.day}"


def get_week_end(week_start):
    # Expects format year-month-day: 2019-02-20
    year, month, day = week_start.split("-")
    end = datetime(year, month, day) + timedelta(days=7)
    return f"{end.year}-{end.month}-{end.day}"


def read_parquet(target_file):
    df = pandas.read_parquet(target_file)
    pandas.set_option('display.max_rows', 1000)
    print(df)
    return df


def write_parquet(input_json, target_file):
    df = pandas.read_json(input_json)
    df.to_parquet(target_file)


def main():
    f = f"{basedir}/aapl-jan"
    fpath = Path(f)
    if fpath.exists():
        fpath.unlink()
    agg = get_minute_aggregate("AAPL", "2020-02-25", "2020-02-32")

    ap = process_aggregate(agg)
    write_parquet(ap, f)
    read_parquet(f)


if __name__ == "__main__":
    main()
