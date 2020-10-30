# Copyright (C) 2020 Mike Healey
# All rights reserved
#
from dataclasses import dataclass
from dataclasses import field

from stock_data.models.model import Model


@dataclass
class TickerNews(Model):
    ticker: str
    title: str
    source: str
    summary: str
    timestamp: str
    url: str
    related_tickers: list = field(default_factory=list)
    keywords: list = field(default_factory=list)
