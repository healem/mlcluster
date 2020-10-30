# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import requests_mock

from unittest import TestCase

from stock_data.providers.polygon import Polygon
from stock_data.tests.providers.files.news import news_multi


class TestPolygon(TestCase):
    ticker1 = "TEST"

    def setUp(self) -> None:
        self.poly = Polygon("speicla")

    @requests_mock.Mocker()
    def test_get_news_paged(self, m):
        response = [news_multi[0]]
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=1",
            json=response
        )
        resp = self.poly.get_ticker_news(self.ticker1, "2018-02-06", "2019-02-08")
        print(f"RESPONSE1: {resp}")
        self.assertEqual(len(resp), 1)

        # get second page
        response2 = [news_multi[1]]
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=2",
            json=response2
        )
        resp2 = self.poly.get_ticker_news(self.ticker1, "2018-02-06", "2019-02-08")
        print(f"RESPONSE2: {resp2}")
        self.assertEqual(len(resp2), 2)

    @requests_mock.Mocker()
    def test_get_news_limited_early(self, m):
        response = news_multi
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=1",
            json=response
        )
        resp = self.poly.get_ticker_news(self.ticker1, "2018-02-06", "2019-02-06")
        print(f"RESPONSE1: {resp}")
        self.assertEqual(len(resp), 1)

    @requests_mock.Mocker()
    def test_get_news_limited_late(self, m):
        response = news_multi
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=1",
            json=response
        )
        resp = self.poly.get_ticker_news(self.ticker1, "2018-02-08", "2019-02-08")
        print(f"RESPONSE1: {resp}")
        self.assertEqual(len(resp), 1)

    @requests_mock.Mocker()
    def test_get_news(self, m):
        response = news_multi
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=1",
            json=response
        )
        resp = self.poly.get_ticker_news(self.ticker1, "2018-02-06", "2019-02-08")
        print(f"RESPONSE1: {resp}")
        self.assertEqual(len(resp), 2)

    @requests_mock.Mocker()
    def test_get_news_none(self, m):
        response = news_multi
        m.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker1}/news?apiKey=speicla&perpage=50&page=1",
            json=response
        )
        resp = self.poly.get_ticker_news(self.ticker1, "2020-02-06", "2020-02-08")
        print(f"RESPONSE1: {resp}")
        self.assertEqual(len(resp), 0)
