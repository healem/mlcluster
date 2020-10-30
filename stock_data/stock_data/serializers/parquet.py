# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging
import pandas

from stock_data.serializers.serializer import Serializer


class Parquet(Serializer):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read(self, location):
        df = pandas.read_parquet(location)
        return df

    def write(self, data, location):
        df = pandas.read_json(data)
        df.to_parquet(location)
