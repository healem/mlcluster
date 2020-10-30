# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import argparse
import logging
import os
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from shutil import rmtree

from stock_data.providers.polygon import Polygon
from stock_data.sertializers.parquet import Parquet
from stock_data.serializers.stdout import Stdout


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
key = os.environ.get("POLYGON_KEY")
poly = Polygon(key)


def create_skeleton(base):
    for subdir in [minute_dir, ticker_dir, news_dir]:
        path = Path(f"{base}/{subdir}")
        path.mkdir(parents=True, exist_ok=True)


def delete_skeleton(base):
    rmtree(base)


def get_candles(ticker, start, end):
    return poly.get_minute_aggregate(ticker, start, end)


def get_details(ticker):
    return poly.get_ticker_details(ticker)


def get_news(ticker, start, end):
    return poly.get_ticker_news(ticker, start, end)


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


def parse_args():
    parser = argparse.ArgumentParser(description="Stock data fetcher")
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        default=False,
        help="Get candles, details, and news for the ticker",
    )
    parser.add_argument(
        "--basedir",
        "-b",
        action="store",
        default=basedir,
        help="Top-level of the directory to save the data to",
    )
    parser.add_argument(
        "--candles",
        "-c",
        action="store_true",
        default=False,
        help="Get candles for the ticker",
    )
    parser.add_argument(
        "--details",
        "-d",
        action="store_true",
        default=False,
        help="Get details for the ticker",
    )
    parser.add_argument(
        "--end",
        "-e",
        action="store",
        required=True,
        help="The end date for ticker candle data",
    )
    parser.add_argument(
        "--news",
        "-n",
        action="store_true",
        default=False,
        help="Get news for the ticker",
    )
    parser.add_argument(
        "--out",
        "-o",
        action="store",
        choices=["parquet", "stdout"],
        default="stdout",
        help="How to output the data",
    )
    parser.add_argument(
        "--start",
        "-s",
        action="store",
        required=True,
        help="The start date for ticker candle data",
    )
    parser.add_argument(
        "--ticker",
        "-t",
        action="store",
        help="Get data for the specified ticker and output the results to stdout",
    )

    args = parser.parse_args()

    if args.all:
        args.candles = True
        args.details = True
        args.news = True

    return args


def main(args):
    if args.out == "parquet":
        location = args.basedir
        serializer = Parquet()
    else:
        location = None
        serializer = Stdout()

    if args.ticker:
        if args.details:
            serializer.write(get_details(args.ticker), location)

        if args.candles:
            serializer.write(get_candles(args.ticker, args.start, args.end), location)

        if args.news:
            serializer.write(get_news(args.ticker, args.start, args.end), location)


if __name__ == "__main__":
    args = parse_args()
    main(args)
