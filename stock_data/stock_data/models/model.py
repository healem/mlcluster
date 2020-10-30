# Copyright (C) 2020 Mike Healey
# All rights reserved
#
import json

from dataclasses import asdict as ad
from dataclasses import dataclass


@dataclass
class Model(object):
    def to_dict(self):
        return ad(self)

    def to_json(self):
        return json.dumps(self.to_dict())
