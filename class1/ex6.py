#!/usr/bin/env python


a_list = range (8)

a_list.append ( {} )

a_list[-1]['ip_addr'] = '10.10.0.1'
a_list[-1]['mask'] = '255.255.255.0'


from pprint import pprint as pp

pp(a_list)



import json
import yaml

with open ("ex.yml", "w") as f:
    yaml.dump( a_list, f, default_flow_style = False)

with open ("ex.json", "w") as f:
    json.dump( a_list, f)

