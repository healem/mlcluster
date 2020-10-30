# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging
import requests

from abc import ABC
from abc import abstractmethod


class Provider(ABC):

    def __init__(self, baseurl):
        self.logger = logging.getLogger(__name__)
        self.baseurl = baseurl
        self.session = requests.Session()

    @abstractmethod
    def get_all_tickers(self, locale="us", market="stocks"):
        # Get a list of all tickers in the locale and market
        pass

    @abstractmethod
    def get_minute_aggregate(self, ticker, start_date, end_date):
        # Get the minute OCHLV for the specified ticker and date range
        pass

    @abstractmethod
    def get_ticker_details(self, ticker):
        # Details about the company and the companies financials
        pass

    @abstractmethod
    def get_ticker_news(self, ticker, start_date, end_date):
        # Get news for the ticker
        pass
