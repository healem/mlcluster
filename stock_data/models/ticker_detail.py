# Copyright (C) 2020 Mike Healey
# All rights reserved
#
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from .model import Model
from .ticker_financials import TickerFinancials


@dataclass
class TickerDetail(Model):
    ticker: str
    country: str
    industry: str
    sector: str
    marketcap: int
    employees: int
    url: str = None
    description: str = None
    similar: list = field(default_factory=list)
    financials: Optional[TickerFinancials] = None
