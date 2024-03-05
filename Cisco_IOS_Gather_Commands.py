# $language = "python3"
# $interface = "1.0"

# part of this is based on the getData script from SecureCRT

import os
import subprocess
import codecs
from datetime import datetime

LOG_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

SCRIPT_TAB = crt.GetScriptTab()

COMMANDS = {
    "System_Information": [
        "show version",
        "show hardware capacity",
        "show inventory",
        "show module",
        "show feature",
        "show feature-set",
        "show hostname",
        "dir all-filesystems",
        "show redundancy",
    ],
    "Routing_Information": [
        "show ip route",
        # "show ip route vrf *",
        # "show ip route summary",
        # "show ipv6 route",
        # "show ipv6 route summary",
    ],
    "Interface_Information": [
        "show interfaces ",
        "show interfaces summary",
        "show ip interface",
        "show ip interface brief",
        "show interface description",
        "show interfaces counters",
        "show etherchannel summary",
        "show interface brief",
        "show interface status",
        "show interface transceiver detail",
        "show ipv6 interface ",
        "show ipv6 interface brief",
    ],
    "ISIS": [
        "show isis neighbor",
        "show isis interface",
        "show isis database",
        # "show isis topology",
    ],
    "OSPF": [
        "show ip ospf interface",
        "show ip ospf database",
        "show ip ospf neighbor",
    ],
    "BGP": [
        "show bgp * summary",
        "show bgp * all detail",
        "show bgp * all neighbors ",
        "show bgp * all ",
        "show bgp vrf all all summ",
        "show bgp l2vpn evpn summ",
    ],
    "L2_Information": [
        "show vlan ",
        "show vlans ",
        "show vlan summary",
        "show spanning-tree",
    ],
    "Multicast": [
        "show ip pim interface",
        "show ip pim rp",
        "show ip igmp groups",
        "show ip mroute",
        "show ip pim neighbor",
    ],
    "Neighbors": [
        "show ip arp",
        "show mac address-table",
        "show lldp neighbor",
        "show cdp neighbors",
    ],
    "Configurations": [
        "show running-config ",
        "show startup-config",
        "show running-config all",
    ],
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)

    if not os.path.isdir(LOG_DIRECTORY):
        crt.Dialog.MessageBox(
            "Log output directory %r is not a directory" % LOG_DIRECTORY
        )
        return

    if not SCRIPT_TAB.Session.Connected:
        crt.Dialog.MessageBox(
            "Not Connected.  Please connect before running this script."
        )
        return

    SCRIPT_TAB.Screen.IgnoreEscape = True
    SCRIPT_TAB.Screen.Synchronous = True

    while True:
        if not SCRIPT_TAB.Screen.WaitForCursor(1):
            break

    rowIndex = SCRIPT_TAB.Screen.CurrentRow
    colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

    prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
    prompt = prompt.strip()

    # Set screen width to 0
    SCRIPT_TAB.Screen.Send("terminal length 0\r")
    SCRIPT_TAB.Screen.WaitForString("\r", 1)
    SCRIPT_TAB.Screen.WaitForString("\n", 1)

    # Get Hostname
    SCRIPT_TAB.Screen.Send("show run | include hostname\r")
    SCRIPT_TAB.Screen.WaitForString("\r", 1)
    SCRIPT_TAB.Screen.WaitForString("\n", 1)
    hostname_result = SCRIPT_TAB.Screen.ReadString(prompt)
    hostname_result = hostname_result.strip().split(" ")

    now_date_time = datetime.now()
    dt_string = now_date_time.strftime("%d_%m_%Y__%H_%M_%S")

    file_name = (
        SCRIPT_TAB.Caption
        + "_"
        + hostname_result[1]
        + "_"
        + dt_string
        + "_Cisco_IOS_Information_Gather.txt"
    )
    logFileName = os.path.join(LOG_DIRECTORY, file_name)

    filep = codecs.open(logFileName, "a", "utf-8")

    filep.write(
        "Commands attempted to run as part of this script for device "
        + hostname_result[1]
    )
    filep.write("\n\n")
    for index, comamnd_list in COMMANDS.items():
        filep.write(index + "\n")
        for command in comamnd_list:
            filep.write("\t" + command + "\n")
    filep.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    for index, command_list in COMMANDS.items():
        filep.write(index + "\n\n")
        for command in command_list:
            command = command.strip()

            # Send the command text to the remote
            SCRIPT_TAB.Screen.Send(command + "\r")

            # Wait for the command to be echoed back to us.
            SCRIPT_TAB.Screen.WaitForString("\r", 1)
            SCRIPT_TAB.Screen.WaitForString("\n", 1)
            result = SCRIPT_TAB.Screen.ReadString(prompt)
            result = result.strip()

            filep.write("Results of command: " + command + os.linesep)

            # Write out the results of the command to our log file
            filep.write(result + os.linesep)

            filep.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    # Close the log file
    filep.close()

    # Set screen width to 0
    SCRIPT_TAB.Screen.Send("terminal length 24\r")
    SCRIPT_TAB.Screen.WaitForString("\r", 1)
    SCRIPT_TAB.Screen.WaitForString("\n", 1)

    # LaunchViewer(LOG_DIRECTORY)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def LaunchViewer(filename):
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(["open", filename])


main()
