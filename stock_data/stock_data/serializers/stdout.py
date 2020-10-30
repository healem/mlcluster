# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging
import pprint

from stock_data.serializers.serializer import Serializer


class Stdout(Serializer):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read(self, location):
        pass

    def write(self, data, location=None):
        pprint.pprint(data)
