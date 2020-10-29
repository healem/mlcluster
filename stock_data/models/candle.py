# Copyright (C) 2020 Mike Healey
# All rights reserved
#
from dataclasses import dataclass

from stock_data.models.model import Model


@dataclass
class Candle(Model):
    ticker: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    day_name: str
    period: str
    open: float
    close: float
    high: float
    low: float
    volume: int
    number: int
    vw: float
