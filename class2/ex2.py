#!/usr/bin/env python
"""
2. telnetlib

    a. Write a script that connects using telnet to the pynet-rtr1 router. Execute the 'show ip int brief' command on the router and return the output.

Try to do this on your own (i.e. do not copy what I did previously). You should be able to do this by using the following items:

telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
remote_conn.read_until(<string_pattern>, TELNET_TIMEOUT)
remote_conn.read_very_eager()
remote_conn.write(<command> + '\n')
remote_conn.close()

"""

import telnetlib
import time
import socket
import sys

TELNET_PORT = 23
TELNET_TIMEOUT = 3


def telnet_connection ( ip_address, port, timeout):
    try:
        remote = telnetlib.Telnet ( ip_address, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout as e:
        remote = None
    return remote


def login ( remote, username, password ):
    output = remote.read_until ( 'sername:', TELNET_TIMEOUT )
    remote.write ( username + '\n' )
    output += remote.read_until ( 'assword:', TELNET_TIMEOUT )
    remote.write ( password + '\n' )

    return output

def send_command ( remote, command):
    command = command.rstrip()
    remote.write ( command + '\n' )
    time.sleep (1)
    return remote.read_very_eager ()

def telnet_close (remote):
    remote.close()

def main ():

    ip_address = '50.76.53.27'
    username   = 'pyclass'
    password   = '88newclass'

    # open telnet conenction to a remote device
    remote = telnet_connection ( ip_address, TELNET_PORT, TELNET_TIMEOUT)
    if remote is None:
        sys.exit ("I cannot connect to {}!".format(ip_address))

    # login to a remote device
    output = login ( remote, username, password )
    print ("<START>{}</FINISH>". format (output))

    output = send_command ( remote, 'show ip interface brief')
    print ("<START>{}</FINISH>". format (output))

    telnet_close ( remote) 

if __name__ == "__main__":

    main ()
