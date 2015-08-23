#!/usr/bin/env python



'''
4. SNMP Basics

    a. Create an 'SNMP' directory in your home directory.

$ mkdir SNMP
$ cd SNMP 

    b. Verify that you can import the snmp_helper library.  This is a small library that I created to simplify aspects of PySNMP.

$ python
Python 2.7.5 (default, Feb 11 2014, 07:46:25) 
[GCC 4.8.2 20140120 (Red Hat 4.8.2-13)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> import snmp_helper

    c. Create a script that connects to both routers (pynet-rtr1 and pynet-rtr2) and prints out both the MIB2 sysName and sysDescr.

'''

import snmp_helper
from pprint import pprint as pp

if __name__ == '__main__':

    COMMUNITY_STRING = 'galileo'
    ROUTERS = { 
        'pynet-rtr1' : '50.76.53.27:7961', 
        'pynet-rtr2' : '50.76.53.27:8061' 
    }
    OIDS = {
        'sysName' : '1.3.6.1.2.1.1.5.0',
        'sysDescr' : '1.3.6.1.2.1.1.1.0',
    }
    
    
    for router in ROUTERS.keys():
        
            ip_address, snmp_port = ROUTERS[router].split(':') 
            a_device = ( ip_address, COMMUNITY_STRING, snmp_port )

            pp (a_device)
    
            for oid_name, oid in OIDS.items():
                snmp_data = snmp_helper.snmp_get_oid (a_device, oid=oid, display_errors=True)
                pp (oid_name)
                output = snmp_helper.snmp_extract (snmp_data)
                pp (output)
