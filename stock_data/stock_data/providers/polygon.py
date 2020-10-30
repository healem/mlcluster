# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging
import os

from datetime import datetime

from stock_data.models.candle import Candle
from stock_data.models.ticker import Ticker
from stock_data.models.ticker_detail import TickerDetail
from stock_data.models.ticker_financials import TickerFinancials
from stock_data.models.ticker_news import TickerNews
from stock_data.providers.provider import Provider
from stock_data.utils import get_datetime_from_basic
from stock_data.utils import get_datetime_from_iso


class Polygon(Provider):
    def __init__(self, api_key=None):
        super().__init__("https://api.polygon.io")
        if api_key:
            key = api_key
        else:
            key = os.environ.get("POLYGON_KEY")
        self.session.params["apiKey"] = key

    # ###########   Get all tickers
    def get_all_tickers(self, locale="us", market="stocks"):
        # Get a list of all Tickers in the locale and market
        return self._process_all_tickers(self._get_all_tickers_raw(locale, market))

    @staticmethod
    def _process_all_tickers(tickers_raw):
        tickers = []
        for t in tickers_raw:
            tickers.append(
                Ticker(
                    active=t.get("active"),
                    locale=t.get("locale"),
                    currency=t.get("currency"),
                    market=t.get("market"),
                    name=t.get("name"),
                    ticker=t.get("ticker"),
                )
            )
        return tickers

    def _get_all_tickers_raw(self, locale, market):
        endpoint = f"v2/reference/tickers"
        return self._call_polygon(endpoint, dict(locale=locale, market=market))

    # ###############  Get MINUTE aggregate
    def get_minute_aggregate(self, ticker, start_date, end_date):
        # Get the minute OCHLV for the specified ticker and date range
        return self._process_minute_aggregate(
            self._get_minute_aggregate_raw(ticker, start_date, end_date)
        )

    @staticmethod
    def _process_minute_aggregate(agg):
        candles = []
        logging.info(
            f"Processing {agg.get('resultsCount')} for ticker {agg.get('ticker')}"
        )
        for candle in agg["results"]:
            dt = datetime.fromtimestamp(int(candle.get("t")) / 1000.0)
            candles.append(
                Candle(
                    ticker=agg.get("ticker"),
                    period="minute",
                    year=dt.year,
                    month=dt.month,
                    day=dt.day,
                    hour=dt.hour,
                    minute=dt.minute,
                    day_name=dt.strftime("%A"),
                    open=candle.get("o"),
                    close=candle.get("c"),
                    high=candle.get("h"),
                    low=candle.get("l"),
                    volume=candle.get("v"),
                    number=candle.get("n"),
                    vw=candle.get("vw"),
                )
            )

        return candles

    def _get_minute_aggregate_raw(self, ticker, start_date, end_date):
        endpoint = f"v2/aggs/ticker/{ticker}/range/1/minute/{start_date}/{end_date}"
        return self._call_polygon(endpoint)

    # #############   Get details
    def get_ticker_details(self, ticker):
        # get ticker details
        endpoint = f"v1/meta/symbols/{ticker}/company"
        details = self._call_polygon(endpoint)

        # get ticker financials
        endpoint = f"v2/reference/financials/{ticker}"
        financials = self._call_polygon(endpoint, dict(sort="calendarDate"))

        return self._process_ticker_details(details, financials)

    def _process_ticker_details(self, details, financials):
        fr = financials.get("results", [])[-1]
        fin = TickerFinancials(
            assets=fr.get("assets"),
            cash=fr.get("cashAndEquivalentsUSD"),
            net_income=fr.get("netIncome"),
            debt=fr.get("debtUSD"),
            earnings_per_share=fr.get("earningsPerBasicShareUSD"),
            debt_to_equity=fr.get("debtToEquityRatio"),
            net_profit=fr.get("netIncome"),
            net_margin=fr.get("profitMargin"),
            liabilities=fr.get("totalLiabilities"),
            price_to_earnings=fr.get("priceToEarningsRatio"),
            revenue=fr.get("revenuesUSD"),
            shares=fr.get("shares"),
            sales_per_share=fr.get("salesPerShare"),
            float=fr.get("shares")
        )

        dets = TickerDetail(
            ticker=details.get("symbol"),
            country=details.get("country"),
            industry=details.get("industry"),
            sector=details.get("sector"),
            marketcap=details.get("marketcap"),
            employees=details.get("employees"),
            url=details.get("url"),
            description=details.get("description"),
            similar=details.get("similar"),
            financials=fin
        )
        return dets

    # ################## Get NEWS
    def get_ticker_news(self, ticker, start_date, end_date):
        start = get_datetime_from_basic(start_date)
        end = get_datetime_from_basic(end_date)
        news = []
        done = False
        page = 1
        while not done:
            try:
                items = self._get_ticker_news_raw_page(ticker, page)
            except Exception:
                break

            for item in items:
                this = get_datetime_from_iso(item.get("timestamp"))

                # See if article is in the time window desired
                if this < start:
                    continue
                elif this > end:
                    done = True
                    break
                else:
                    news.append(self._process_news(ticker, item))

            if done:
                break
            else:
                page += 1

        return news

    @staticmethod
    def _process_news(ticker, news_item):
        return TickerNews(
            ticker=ticker,
            title=news_item.get("title"),
            source=news_item.get("source"),
            summary=news_item.get("summary"),
            timestamp=news_item.get("timestamp"),
            url=news_item.get("url"),
            related_tickers=news_item.get("symbols"),
            keywords=news_item.get("keywords")
        )

    def _get_ticker_news_raw_page(self, ticker, page=1):
        endpoint = f"v1/meta/symbols/{ticker}/news"
        return self._call_polygon(endpoint, params=dict(perpage=50, page=page))

    # ################### Call polygon
    def _call_polygon(self, endpoint, params=None):
        target = f"{self.baseurl}/{endpoint}"
        if params:
            response = self.session.get(target, params=params)
        else:
            response = self.session.get(target)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
