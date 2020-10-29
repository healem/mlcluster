# Copyright (C) 2020 Mike Healey
# All rights reserved
#
from dataclasses import dataclass

from stock_data.models.model import Model


@dataclass
class TickerFinancials(Model):
    assets: float
    cash: float
    net_income: float
    debt: float
    earnings_per_share: float
    debt_to_equity: float
    net_profit: float
    net_margin: float
    liabilities: float
    price_to_earnings: float
    revenue: float
    shares: int
    sales_per_share: float
    float: int
