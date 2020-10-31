# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import json
import logging
import pandas

from pathlib import Path

from stock_data.models.model import Model
from stock_data.serializers.serializer import Serializer


class Parquet(Serializer):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read(self, location):
        df = pandas.read_parquet(location)
        return df

    def write(self, data, location):
        # Make sure the location exists
        path = Path(location)
        path.parent.mkdir(parents=True, exist_ok=True)

        # coerce the data, if needed
        if isinstance(data, list) and isinstance(data[0], Model):
            dicted = []
            for item in data:
                dicted.append(item.to_dict())
        elif isinstance(data, Model):
            dicted = data.to_dict()
        else:
            raise ValueError(f"Unexpected type {type(data)} for storing in parquet.")

        # write out the data
        df = pandas.read_json(json.dumps(dicted))
        df.to_parquet(location)
