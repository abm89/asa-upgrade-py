import sys
import os
import netmiko
import getpass
import time
import re

newVersion = input("Please enter the filename for the asa binary: ")

if newVersion != "":
    
    #show boot configuration in running config
    showBoot = "show run boot\n show version"

    host = input("Hostname/IP: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    from netmiko import ConnectHandler
    net_connect = ConnectHandler(device_type='cisco_asa',ip=host,username=username,password=password)
    currentVersion = net_connect.send_command(showBoot)
    print(currentVersion)




    #start configuration
    #print("config t")
    #print("no", currentVersion)
    #print("boot system", newVersion)
    #print("boot system", currentVersion)
    #print("end")
    #print("wr mem")

    #wait for file to save
    print("Waiting for configuration to save...")
    time.sleep(10)

    #check failover status
    print("Checking failover state...")
    showFailover = "sh failover state"
    net_connect = ConnectHandler(device_type='cisco_asa',ip=host,username=username,password=password)
    failoverState = net_connect.send_command(showFailover)
    #print(failoverState)

    #initializes booleans for checking the standby state and configuration sync status
    syncStatus = False
    stdbyStatus = False

    stdbyRed = ['Standby Ready']

    for pattern in stdbyRed:
        print('Looking for "%s" in "%s" ->' % (pattern, failoverState), end=' ')

        if re.search(pattern,failoverState):
            print('Found a match')
            stdbyStatus = True
        else:
            print('no match')

    syncRed = ['Sync Done']
    for pattern in syncRed:
        print('Looking for "%s" in "%s" ->' % (pattern, failoverState), end=' ')

        if re.search(pattern,failoverState):
            print('Found a match')
            syncStatus = True
        else:
            print('no match')

    if syncStatus == True and stdbyStatus == True:

        #start script
        print("Starting upgrade...")


    elif syncStatus == False and stdbyStatus == True:

        print('Configuration Status is not synced. Please check your failover configuration and try again.')
        sys.exit()

    elif syncStatus == True and stdbyStatus == False:

        print('Standby is not in a "ready" state. Please check your failover configuration and try again.')
        sys.exit()

    else:

        print('The standby state is not "ready" and the configuration is not synced. Please check your failover configuration and try again.')
        sys.exit()