#!/usr/bin/env python
'''
2. Use Paramiko to change the 'logging buffered <size>' configuration on pynet-rtr2. This will require that you enter into configuration mode.
'''



import paramiko
from getpass import getpass
from time import sleep
import re



BUFFER=512

def miko_read(remote_conn, prompt):
    """
    this funtion reads all data from paramiko channel if there is data to read
    """
    # sleep before reading to make sure all data is there
    sleep(1)

    # variable that stores data from channel
    output = ''
    # make sure we found the prompt
    found = False

    while (remote_conn.recv_ready() and not found):
        output += remote_conn.recv(BUFFER) 

        match = re.match(prompt, output)
        if match:
            found = True

    return output

def miko_send(remote_conn, command, prompt):
    """
    this function sends the command and returns the output of the command
    """
    # make sure we control if there is \n at the end of the command
    command = command.rstrip()
    command += '\n'

    # send the command
    send_bytes = remote_conn.send(command)

    # read the output of the command
    recv_bytes = miko_read(remote_conn, prompt)
    return recv_bytes


def main():

    pynet_rtr2={
        "hostname" : "50.76.53.27",
        "port" : 8022,
        "username" : "pyclass",
        "password" : getpass(),
        "allow_agent" : False,
        "look_for_keys" : False,
    }
    enable_prompt = r'pynet-rtr2#'
    config_prompt = r'pynet-rtr2(config)#'

    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(**pynet_rtr2)

    remote_conn=remote_conn_pre.invoke_shell()
    output = miko_read(remote_conn, enable_prompt)
    print(output)

    commands = [ 
        (r'terminal length 0', enable_prompt),
        (r'configure terminal', config_prompt),
        (r'logging buffered 12345', config_prompt),
        (r'end', enable_prompt),
        (r'show running-config | include buffered', enable_prompt),
    ]

    for command in commands:
        output = miko_send(remote_conn, command[0], command[1])
        print(output)

if __name__=='__main__':
    main()
