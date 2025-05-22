#!/usr/bin/python

"""Subnet Network for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Victor Gomez",
    "Rahim Siddiq",
    "Arielle Lauper"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.term import makeTerm
import time
import subprocess

# Run certificate generation script
subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"])

def myNetwork():

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/24')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)           # instantiate switch s1
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)           # instantiate switch s2
    r5 = net.addHost('r5', cls=Node, ip='10.0.1.3/24')      # instantiate router r5
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')               # enable ip forwarding on router r5
    r4 = net.addHost('r4', cls=Node, ip='192.168.0.2/30')   # instantiate router r4
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')               # enable ip forwarding on router r4
    r3 = net.addHost('r3', cls=Node, ip='10.0.0.3/24')      # instantiate router r3
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')               # enable ip forwarding on router r3

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.3')     # instantiate host h1 with router r3 as its default route
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.3')     # instantiate host h2 with router r3 as its default route
    h3 = net.addHost('h3', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.3')     # instantiate host h3 with router r5 as its default route
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.3')     # instantiate host h4 with router r5 as its default route

    info('*** Add links\n')
    net.addLink(h1, s1)     # establish link between host h1 and switch s1
    net.addLink(h2, s1)     # establish link between host h2 and switch s1
    net.addLink(h3, s2)     # establish link between host h3 and switch s2
    net.addLink(h4, s2)     # establish link between host h4 and switch s2
    net.addLink(s2, r5)     # establish link between switch s2 and router r5
    net.addLink(s1, r3)     # establish link between switch s1 and router r3
    net.addLink(r3, r4, intfName1='r3-eth1', params1={'ip': '192.168.0.1/30'}, intfName2='r4-eth0', params2={'ip': '192.168.0.2/30'})  # establish link between router r3 and router r4 & assign IP to Ethernet interfaces
    net.addLink(r4, r5, intfName1='r4-eth1', params1={'ip': '192.168.1.1/30'}, intfName2='r5-eth1', params2={'ip': '192.168.1.2/30'})  # establish link between router r4 and router r5 & assign IP to Ethernet interfaces

    info('*** Starting network\n')
    net.build()
    # static routes for routers
    net['r3'].cmd('ip route add 10.0.1.0/24 via 192.168.0.2 dev r3-eth1')       # add route from router r3 to subnet 10.0.1.0/24
    net['r3'].cmd('ip route add 192.168.1.0/30 via 192.168.0.2 dev r3-eth1')    # add route from router r3 to subnet 192.168.1.0/30
    net['r4'].cmd('ip route add 10.0.0.0/24 via 192.168.0.1 dev r4-eth0')       # add route from router r4 to subnet 10.0.0.0/24
    net['r4'].cmd('ip route add 10.0.1.0/24 via 192.168.1.2 dev r4-eth1')       # add route from router r4 to subnet 10.0.1.0/24
    net['r5'].cmd('ip route add 10.0.0.0/24 via 192.168.1.1 dev r5-eth1')       # add route from router r5 to subnet 10.0.0.0/24
    net['r5'].cmd('ip route add 192.168.0.0/30 via 192.168.1.1 dev r5-eth1')    # add route from router r5 to subnet 192.168.0.0/30
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info('*** Post configure switches and hosts\n')
    try:
        makeTerm(h4, title='Node', term='xterm', display=None, cmd='python3 tpa4_chat_server.py; bash')
        print("Xterm for h4 started successfully.")
    except Exception as e:
        print(f"Failed to start xterm for h4: {e}")
    time.sleep(1)
    try:
        makeTerm(h1, title='Node', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')
        print("Xterm for h1 started successfully.")
    except Exception as e:
        print(f"Failed to start xterm for h1: {e}")
    time.sleep(1)

    try:
        makeTerm(h2, title='Node', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')
        print("Xterm for h2 started successfully.")
    except Exception as e:
        print(f"Failed to start xterm for h2: {e}")
    time.sleep(1)

    try:
        makeTerm(h3, title='Node', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')
        print("Xterm for h3 started successfully.")
    except Exception as e:
        print(f"Failed to start xterm for h3: {e}")
    
    CLI(net)
    net.stop()
    net.stopXterms()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
