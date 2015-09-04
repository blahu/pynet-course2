#!/usr/bin/env python
"""
3. telnetlib (optional - challenge question)

    Convert the code that I wrote here to a class-based solution (i.e. convert
over from functions to a class with methods).
"""

'''
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass
import re

class Telneto :

    TELNET_PORT = 23
    TELNET_TIMEOUT = 6

    def __init__ (self, ip_address, username, password, prompt, debug=False):

        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.prompt = prompt
        self.debug = debug

        self.remote_conn = self.telnet_connect()

        if not self.login():
            sys.exit("Logging Error")

        output = self.disable_paging()
        if self.debug: print ("Disable_paging ({})".format(output))

    def telnet_connect(self):
        '''
        Establish telnet connection
        '''
        try:
            return telnetlib.Telnet(self.ip_address, self.TELNET_PORT, self.TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")
        except socket.gaierror:
            sys.exit("Remote hostname unknown")
    
    def login(self):
        '''
        Login to network device
        '''
        output = self.remote_conn.read_until("sername:", self.TELNET_TIMEOUT)
        self.remote_conn.write(self.username + '\n')
        time.sleep(1)
        output += self.remote_conn.read_until("ssword:", self.TELNET_TIMEOUT)
        self.remote_conn.write(self.password + '\n')
        time.sleep(1)
        output += self.remote_conn.read_very_eager()

        if self.debug: print ("Login ({})".format(output))

        return self.check_prompt(output)

    def check_prompt(self, output):
        for line in output.splitlines():
            match = re.match ( self.prompt, line)
            if match:
                return True
        
        return False
    

    def send_command(self, cmd):
        '''
        Send a command down the telnet channel
    
        Return the response
        '''
        cmd = cmd.rstrip()
        self.remote_conn.write(cmd + '\n')
        time.sleep(1)
        output = self.remote_conn.read_very_eager()
        if self.check_prompt(output):
            return output
        else:
            sys.exit("Command not finished properly")
    
    def disable_paging(self, paging_cmd='terminal length 0'):
        '''
        Disable the paging of output (i.e. --More--)
        '''
        return self.send_command(paging_cmd)
    
    def close(self):
        '''
        Close telnet connection
        '''
        return self.remote_conn.close()
    
def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()
    kwargs = {
        'ip_address':ip_addr, 
        'username':username, 
        'password':password,
        'prompt':'pynet-rtr1#',
    } 
    remote_conn = Telneto(**kwargs)

    output = remote_conn.send_command('show ip int brief')

    print "\n\n"
    print output
    print "\n\n"

    remote_conn.close()

if __name__ == "__main__":
    main()
