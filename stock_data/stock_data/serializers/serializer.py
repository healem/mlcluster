# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import logging

from abc import ABC
from abc import abstractmethod


class Serializer(ABC):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def read(self, location):
        pass

    @abstractmethod
    def write(self, data, location=None):
        pass
