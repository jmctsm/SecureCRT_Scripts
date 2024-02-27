# $language = "python3"
# $interface = "1.0"

# part of this is based on the getData script from SecureCRT

import os
import subprocess
import codecs
from datetime import datetime

LOG_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

SCRIPT_TAB = crt.GetScriptTab()

now_date_time = datetime.now()
dt_string = now_date_time.strftime("%d_%m_%Y__%H_%M_%S")

file_name = SCRIPT_TAB.Caption + "_" + dt_string + "_Juniper_Information_Gather.txt"
logFileName = os.path.join(LOG_DIRECTORY, file_name)

SINGLE_COMMANDS = {
    "COMMON COMMANDS": [
        "show interfaces terse",
        "show version",
        "show chassis fpc",
        "show route",
        "show arp",
    ],
    "BGP": [
        "show bgp summary",
        "show bgp group",
        "show bgp neighbor",
        "show route next-hop database",
        "show route protocol bgp",
        "show route protocol bgp terse",
        "show route receive-protocol bgp",
        "show route advertising-protocol bgp",
        # "show route advertising-protocol bgp <neighbor-address> extensive",
        # "show route receive-protocol bgp <neighbor-address>",
        "show route forwarding-table",
        "show route resolution unresolved",
        "show route hidden",
        # "show route community <reg-ex>",
        "show route terse community-name <name>",
        "show route damping",
        'show route aspath-regex "regex"',
        "show route damping history",
        "show route damping decayed",
        "show route damping suppressed",
    ],
    "OSPF": [
        "show ospf overview",
        "show ospf database",
        "show ospf neighbor detail",
        "show ospf route",
        "show ospf statistics",
        "show ospf interface",
        "show ospf log",
        "show route protool ospf",
        # "show route <x.x.x.x> extensive",
        "show ospf database summary ",
        "show ospf database extensive",
        "show bfd session",
    ],
    "RIP": [
        "show rip overview",
        "show rip neighbor",
        "show route protocol rip",
        # "show route advertising-protocol rip <neighbor-address> extensive",
        # "show route receive-protocol rip <neighbor-address>",
        "show rip statistics",
        "show route forwarding-table",
        "show route resolution unresolved",
    ],
    "ISIS": [
        "show isis adjacency",
        "show isis adjacency extensive",
        "show isis interface",
        "show isis interface details",
        "show isis hostname",
        "show isis spflog",
        "show isis statistics",
        "show isis route ",
        "show route protocol isis",
        "show isis database",
        "show isis database detail",
        "show bdf session",
        "show route forwarding-table",
    ],
    "Multicast": [
        "show multicast route   ",
        "show multicast statistics",
        "show multicast sessions",
        "show multicast usage",
        "show multicast interface",
        "show multicast next-hops",
        "show multicast rpf summary",
        # "show interface <if-name> extensive",
    ],
    "MPLS": [
        "show mpls interface ",
        "show mpls lsp",
        "show mpls lsp extensive",
        "show mpls lsp ingress",
        "show mpls lsp transit",
        "show ted database",
    ],
    "VPLS": [
        "show vpls connections extensive",
        "show bgp summary",
        # "show route table <instance-name>.l2vpn.0 extensive",
        "show route table bgp.l2vpn.0 extensive",
        "show route table mpls.0 extensive",
        "show route table inet.3 extensive",
        "show vpls flood extensive",
        "show vpls mac-table",
        "show interfaces terse",
        "show interfaces routing",
        "show route forwarding table family mpls extensive",
        "show route forwarding table family vpls extensive",
        # "show interface ge-x/y/z extensive | no-more",
        "show l2-learning interface",
        "show l2-learning mac-move-buffer extensive",
        "show l2-learning l2alm-peers",
        "show l2-learning debug-statistics events",
        "show l2-learning debug-statistics ipc",
        "show l2-learning debug-statistics mac-events",
        "show l2-learning debug-statistics mac-messages",
        "show l2-learning debug-statistics mac-processing",
        "show l2-learning debug-statistics performance-counters",
        "show l2-learning debug-statistics rtsock",
        "show bridge statistics",
        "show vpls statistics",
        # "show bridge mac-table instance <instance-name> extensive",
        # "show vpls mac-table instance <instance-name> extensive",
        "show route forwarding-table family vpls vpn <instance-name> extensive",
    ],
    "L3VPN": [
        # "show route table <vpn-a>  ",
        # "show route table <vpn-a> hidden",
        # "show route forwarding-table vpn <vpn-a>",
        "show route table bgp.l3vpn.0 ",
        # "show route advertising-protocol bgp x.x.x.x",
        # "show route receive-protocol bgp x.x.x.x",
        "show arp",
        # "show ospf interface instance <vpn-a>",
        # "show ospf neighbor instance <vpn-a>",
        # "show ospf database instance <vpn-a>",
    ],
    "L2VPN": [
        "show l2vpn connections extensive  ",
        # "show route table <vpn-a>",
        "show route table bgp.l2vpn.0 ",
        # "show route advertising-protocol bgp x.x.x.x",
        # "show route receive-protocol bgp x.x.x.x",
        "show route table mpls.o",
        "show route forwarding-table family mpls",
        "show rsvp session extensive",
        "show l2circuit connections extensive",
        "show ldp neighbor detail",
        "show ldp database detail",
        "show route table mpls.o",
    ],
    "CoS": [
        # "show interface xx-x/x/x detail  ",
        # "show interface queue xx-x/x/x both-ingress-egress",
        # "show interfaces XX-X/X/X extensive",
        # "show class-of-service interfaces XX-X/X/X ",
        "show class-of-service code-point-aliases",
        "show class-of-service code-point-aliases dscp",
        "show class-of-service code-point-aliases inet-prec",
        "show class-of-service code-point-aliases exp",
        "show class-of-service forwarding-class",
        # "show class-of-service classifier [name]",
        "show class-of-service scheduler-map",
        "show class-of-service rewrite-rule",
        "show class-of-service drop-profile",
        "show class-of-service forwarding-table",
        "show class-of-service forwarding-table classifier mapping",
        "show class-of-service forwarding-table scheduler-map",
    ],
    "Firewall Filters": [
        "show interfaces filters",
        "show firewall",
        # "show firewall filter <filter-name>",
        # "show firewall filter <name> prefix-action <psa-name> from 1 to 8",
        "show firewall log",
        # "show log <log-file-name>",
        "show policer",
        # "show interface policer XX-X/X/X",
    ],
    "IPv6": [
        "set show interface terse",
        "show route table inet6",
        "show ipv6 neighbor",
        "show interface lo0 extensive | display xml",
    ],
    "SNMP": [
        "show configuration snmp",
        "show snmp statistics extensive # Multiple time with polling activity.",
        # "show snmp mib walk <oid>",
        "show snmp mib walk ipfragfails",
        "show interface lo0 extensive",
        # "show system processes extensive | no-more # Multiple time with polling activity.",
        # "show chassis routing-engine | no-more # Multiple time with polling activity.",
        "show system commit | no-more",
        # "show system statistics # Multiple time with polling activity.",
        # "show system buffers # Multiple time with polling activity.",
        "show system core-dumps",
        # "show route <ip of NMS server>",
        # "show pfe statistics traffic # Multiple time with polling activity.",
        "show interface extensive | no-more",
        "show system process extensive | no-more",
        "show snmp statistics subagents | no-more",
        "show snmp stats-response-statistics",
    ],
    "High CPU": [
        # "show chassis routing-engine (multiple snapshots, atleast 5)",
        # "show system processes extensive (multiple snapshots atleast 5)",
        "show system users",
        "show system connections",
        "show system statistics",
        # "Turn on task accounting and collect the task accounting detail output (three times with a gap of 30 seconds). Do not forget to turn it off after you have finished.",
        # "set task accounting on",
        # "show task accounting detail",
        # "set task accounting off",
        "show task memory detail",
        "show task memory summary",
        "show task io",
        "show task history",
        "show task statistics",
        "show task job",
        "show task jobs",
        "show krt queue",
        "show krt state",
    ],
    "MX Fabric Plane": [
        "show chassis environment cb",
        "show chassis alarms",
        "show chassis hardware",
        "show chassis fabric summary",
        "show chassis fabric map",
        "show chassis fabric fpc",
        "show chassis fabric plane",
        # "show class-of-service fabric statistics (take multiple outputs to see counters incrementing)",
        # "show pfe statistics traffic (take multiple outputs to see counters incrementing)",
        # "request pfe execute target <fpc_no> command",
        "show hsl2 statistics detail",
        # "request pfe execute target <fpc_no> command",
        "show syslog messages",
    ],
    "NG-MPVN": [
        # "show route table<instance-name>.inet.0 | no-more",
        # "show route table<instance-name>.mvpn.0 | no-more",
        # "show route table<instance-name>.inet.0 extensive | no-more",
        # "show route table<instance-name>.mvpn.0 extensive | no-more",
        # "show pim joininstance <instance-name> extensive | no-more",
        # "show multicast route instance <instance-name> extensive | no-more",
        "show interface extensive |no-more",
        # "show pim rps instance <instance-name> extensive | no-more",
        "show mpls lsp p2mp ingress |no-more",
        "show mpls lsp p2mp ingress extensive |no-more",
        "show mpls lsp p2mp | no-more",
        "show mpls lsp | no-more",
        "show bgp summary |no-more",
    ],
    "CGNAT": [
        # "show chassis pic fpc-slot x pic-slot x",
        "show services service-sets cpu-usage",
        "show services service-sets summary",
        "show services service-sets statistics syslog",
        "show services service-sets statistics packet-drops",
        "show services service-sets memory-usage",
        "show services service-sets memory-usage zone",
        "show services stateful-firewall conversations",
        "show services stateful-firewall conversations destination-prefix",
        "show services stateful-firewall statistics extensive",
        "show services stateful-firewall flow-analysis ",
        "show services stateful-firewall flows extensive",
        "show services nat mappings detail",
        "show services nat pool detail",
        "show services nat mappings endpoint-independent",
        "show services nat mappings address-pooling-paired",
    ],
    "Spanning Tree": [
        "show spanning-tree bridge detail",
        "show spanning-tree bridge msti x detail",
        "show spanning-tree interface detail",
        "show spanning-tree mstp configuration detail",
        "show spanning-tree statistics bridge",
        "show spanning-tree statistics interface detail",
        "show spanning-tree statistics message-queues",
        "show spanning-tree statistics routing-instance detail",
        "show spanning-tree stp-buffer see-all",
    ],
    "BFD": [
        "show ppm connections detail",
        "show bfd session extensive | no-more",
        "show ppm interfaces detail | no-more",
        "show ppm adjacencies detail | no-more",
        "show ppm transmissions detail | no-more",
        "show pfe statistics traffic | no-more",
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

    # Instruct WaitForString and ReadString to ignore escape sequences when
    # detecting and capturing data received from the remote (this doesn't
    # affect the way the data is displayed to the screen, only how it is handled
    # by the WaitForString, WaitForStrings, and ReadString methods associated
    # with the Screen object).
    SCRIPT_TAB.Screen.IgnoreEscape = True
    SCRIPT_TAB.Screen.Synchronous = True

    # If this script is run as a login script, there will likely be data
    # arriving from the remote system.  This is one way of detecting when it's
    # safe to start sending data. If this script isn't being run as a login
    # script, then the worst it will do is seemingly pause for one second
    # before determining what the prompt is.
    # If you plan on supplying login information by waiting for username and
    # password prompts within this script, do so right before this while loop.
    while True:
        if not SCRIPT_TAB.Screen.WaitForCursor(1):
            break
    # Once the cursor has stopped moving for about a second, we'll
    # assume it's safe to start interacting with the remote system.

    # Get the shell prompt so that we can know what to look for when
    # determining if the command is completed. Won't work if the prompt
    # is dynamic (e.g. changes according to current working folder, etc)
    rowIndex = SCRIPT_TAB.Screen.CurrentRow
    colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

    prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
    prompt = prompt.strip()

    # Set screen width to 0
    SCRIPT_TAB.Screen.Send("set cli screen-length 0\r")
    SCRIPT_TAB.Screen.WaitForString("\r", 1)
    SCRIPT_TAB.Screen.WaitForString("\n", 1)

    filep = codecs.open(logFileName, "a", "utf-8")

    for index, command_list in SINGLE_COMMANDS.items():
        filep.write(index)
        filep.write("\n\n")
        for command in command_list:
            command = command.strip()

            # Set up the log file for this specific command
            # logFileName = LOG_FILE_TEMPLATE % {"NUM": NN(index + 1, 2)}

            # Send the command text to the remote
            SCRIPT_TAB.Screen.Send(command + "\r")

            # Wait for the command to be echoed back to us.
            SCRIPT_TAB.Screen.WaitForString("\r", 1)
            SCRIPT_TAB.Screen.WaitForString("\n", 1)

            # Use the ReadString() method to get the text displayed while
            # the command was running.  Note also that the ReadString()
            # method captures escape sequences sent from the remote machine
            # as well as displayed text.  As mentioned earlier in comments
            # above, if you want to suppress escape sequences from being
            # captured, set the Screen.IgnoreEscape property = True.
            result = SCRIPT_TAB.Screen.ReadString(prompt)
            result = result.strip()

            # filep = codecs.open(logFileName, "wb+", "utf-8")

            # If you don't want the command logged along with the results, comment
            # out the very next line
            filep.write("Results of command: " + command + os.linesep)

            # Write out the results of the command to our log file
            filep.write(result + os.linesep)

            filep.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        filep.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    # Close the log file
    filep.close()

    # Set screen width to 0
    SCRIPT_TAB.Screen.Send("set cli screen-length 24\r")
    SCRIPT_TAB.Screen.WaitForString("\r", 1)
    SCRIPT_TAB.Screen.WaitForString("\n", 1)

    # Once we're complete, let's bring up the directory containing the
    # log files.
    LaunchViewer(LOG_DIRECTORY)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def LaunchViewer(filename):
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(["open", filename])


main()
