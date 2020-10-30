# Copyright (C) 2020 Mike Healey
# All rights reserved
#
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from stock_data.models.model import Model
from stock_data.models.ticker_financials import TickerFinancials


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

    def to_dict(self):
        return dict(
            ticker=self.ticker,
            country=self.country,
            industry=self.industry,
            sector=self.sector,
            marketcap=self.marketcap,
            employees=self.employees,
            url=self.url,
            description=self.description,
            similar=self.similar,
            financials=self.financials.to_dict()
        )
