#!/usr/bin/env python

from pprint import pprint as pp


import json,yaml

with open ("ex.yml") as f:
    pp (yaml.load ( f ))

with open ("ex.json") as f:
    pp (json.load ( f ))
