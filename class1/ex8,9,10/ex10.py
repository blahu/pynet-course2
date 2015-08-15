#!/usr/bin/env python
"""
8. Write a Python program using ciscoconfparse that parses this config file. 
Note, this config file is not fully valid (i.e. parts of the configuration are missing). 
The script should find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO') 
and for each crypto map entry print out its children.

9. Find all of the crypto map entries that are using PFS group2

10. Using ciscoconfparse find the crypto maps that are not using AES (based-on the transform set name). 
Print these entries and their corresponding transform set name
"""


from ciscoconfparse import CiscoConfParse as ccp
from pprint import pprint as pp

FILE = 'cisco_ipsec.txt'

# read cisco_ipsec.txt
cfg = ccp ( FILE )


cryptos = cfg.find_objects_wo_child ( r'^crypto map ', r'^ set transform-set AES-SHA' )

for c in cryptos:

    print(c.text)

    transforms = c.re_search_children( r' set transform-set (.*)')
    for l in transforms:
        print (l.text)
    
