#!/usr/bin/env python
'''
6. Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.

'''



from netmiko import ConnectHandler
from getpass import getpass

BUFFER = 512


def main():
    """
    main program flow
    """

    password = getpass()
    pynet_rtr1 = {
        'device_type' : 'cisco_ios',
        'ip' : '50.76.53.27',
        'port' : 22,
        'username' : 'pyclass',
        'password' : password,
    }
    pynet_rtr2 = {
        'device_type' : 'cisco_ios',
        'ip' : '50.76.53.27',
        'port' : 8022,
        'username' : 'pyclass',
        'password' : password,
    }
    pynet_jnpr_srx1 = {
        'device_type' : 'juniper',
        'ip' : '50.76.53.27',
        'port' : 9822,
        'username' : 'pyclass',
        'password' : password,
    }

    devices = [pynet_rtr1, pynet_rtr2, pynet_jnpr_srx1]
    for a_device in devices:
        a_device['verbose'] = False
        net_connect = ConnectHandler(**a_device)
        output = net_connect.send_command(u'show arp', strip_command=True, strip_prompt=True)
        print("")
        print("x"*80)
        print("a {} device {}:{}".format(a_device['device_type'], a_device['ip'], a_device['port']))
        print(output)

if __name__ == '__main__':
    main()
