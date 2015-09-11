#!/usr/bin/env python
'''
6. Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.
9. Bonus Question - Redo exercise6 but have the SSH connections happen
concurrently using either threads or processes (see example). What main issue
is there with using threads in Python?
'''
from netmiko import ConnectHandler
from getpass import getpass
import threading
import time

class ThreadedDevice(threading.Thread):
    """ Generic Network Device polling with threading  """

    def __init__(self, device_type, ip, port, username, password):
        """ initialise threading and then connect to a device """
        threading.Thread.__init__(self)
        self.device = {
            'device_type' : device_type,
            'ip' : ip,
            'port' : port,
            'username' : username,
            'password' : password,
        }
        self.output = ''

    def run(self):
        """ overloaded threading __run__ to connect to the device """
        self.device['verbose'] = False
        net_connect = ConnectHandler(**self.device)
        self.output = net_connect.send_command(u'show arp', strip_command=True,
            strip_prompt=True) 

    def get_arp_table(self):
        outp = "\n"
        outp += "x"*80
        outp += "\n"
        outp += "a {} device {}:{}".format(self.device['device_type'],
            self.device['ip'], self.device['port'])
        outp += "\n"
        return outp + self.output


def main():
    """ main program flow """
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
    start_clock = time.time()
    threads = []
    for a_device in devices:
        a_thread = ThreadedDevice(**a_device)
        threads.append(a_thread)
        a_thread.start()

    for a_thread in threads:
        a_thread.join()
        print a_thread.get_arp_table()

    end_clock = time.time()
    print "\nIt took {} sec to complete".format(end_clock-start_clock)



if __name__ == '__main__':
    main()
