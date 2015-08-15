#!/usr/bin/env python
"""
8. Write a Python program using ciscoconfparse that parses this config file. 
Note, this config file is not fully valid (i.e. parts of the configuration are missing). 
The script should find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO') 
and for each crypto map entry print out its children.
"""


from ciscoconfparse import CiscoConfParse as ccp
from pprint import pprint as pp

FILE = 'cisco_ipsec.txt'

# read cisco_ipsec.txt
cfg = ccp ( FILE )


cryptos = cfg.find_objects ( r'^crypto map ')

for c in cryptos:
    children = cfg.find_children ( c.text )

    for child in children:
        pp (child)
