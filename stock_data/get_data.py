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
from stock_data.serializers.parquet import Parquet
from stock_data.serializers.stdout import Stdout

# ***********************
#
# Get the grouped daily for the whole US market for the first and last day of the month to analyze
# find all stocks that start and end under $10
#
# ***********************


logging.basicConfig(level=logging.DEBUG)

basedir = "/tmp/results"
minute_dir = "minute"
ticker_dir = "tickers"
news_dir = "news"
summary_dir = "summary"
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


def get_summary(day):
    return poly.get_all_day(day)


def get_tickers():
    return poly.get_all_tickers()


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
        help="The end date for ticker candle data",
    )
    parser.add_argument(
        "--list_tickers",
        "-lt",
        action="store_true",
        default=False,
        help="List all tickers",
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
        help="The start date for ticker candle data",
    )
    parser.add_argument(
        "--summary",
        action="store",
        help="Get summary for all tickers in market for specified day",
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

    if args.summary:
        s = get_summary(args.summary)
        print(f"Summary has {len(s)} tickers")
        serializer.write(get_summary(args.summary), f"{location}/{summary_dir}/{args.summary}")

    if args.list_tickers:
        serializer.write(get_tickers(), location)

    if args.ticker:
        if args.details:
            serializer.write(get_details(args.ticker), f"{location}/{ticker_dir}/{args.ticker}")

        if args.candles:
            serializer.write(
                get_candles(
                    args.ticker,
                    args.start, 
                    args.end
                ),
                f"{location}/{minute_dir}/{args.ticker}"
            )

        if args.news:
            serializer.write(
                get_news(
                    args.ticker,
                    args.start,
                    args.end
                ),
                f"{location}/{news_dir}/{args.ticker}/{args.start}_{args.end}"
            )


if __name__ == "__main__":
    args = parse_args()
    main(args)
