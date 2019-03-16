from __future__ import absolute_import, division, print_function

import netifaces

import scapy.config
import scapy.layers.l2
import scapy.route
from scapy.all import *
from scapy.layers.l2 import Ether, ARP


def arp_ping(netmask="192.168.1.0/24"):
    """ Returns the IP and MAC-address of all local hosts with respect to @netmask """
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=netmask), timeout=0.2)
    return [rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd, rcv in ans]


def get_default_gateway():
    """ Returns the default gateway of a host """
    # TODO: Doesn't work when only using enp0s3
    gws = netifaces.gateways()
    return str(gws['default'][netifaces.AF_INET][0])


def get_local_host_ip():
    """ Returns local IP address """
    interfaces = netifaces.interfaces()

    for i in interfaces:
        if i == 'lo':
            continue
        i_face = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if i_face is not None:
            for j in i_face:
                return j['addr']
        else:
            return None


def arp_ping_details(netmask="192.168.2.254/24"):
    """ Returns the IP and MAC-address of all local hosts together with the hostname if possible """
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=netmask), timeout=0.2)
    hosts = []
    print(ans)
    for s, r in ans.res:
        try:
            hostname = socket.gethostbyaddr(r.psrc)
            hosts.append(hostname[0])
        except socket.herror:
            # failed to resolve
            pass
        print(hosts)
    ans.append(hosts)
    return [(rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd, rcv in ans)]


def mac_for_ip(ip):
    """ Returns the MAC address that belongs to @ip """
    for i in netifaces.interfaces():
        addrs = netifaces.ifaddresses(i)
        try:
            if_mac = addrs[netifaces.AF_LINK][0]['addr']
            if_ip = addrs[netifaces.AF_INET][0]['addr']
        except IndexError:  # ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None


def long_to_net(arg):
    if arg <= 0 or arg >= 0xFFFFFFFF:
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


def to_cidr(network_bytes, netmask_bytes):
    network = scapy.utils.ltoa(network_bytes)
    netmask = long_to_net(netmask_bytes)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        print('too big')
        return None
    return net


def scan_and_print_neighbors(net, interface, combinations, timeout=0.01):
    try:
        ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
        for s, r in ans.res:
            mac = r.sprintf("%Ether.src%")
            ip = r.sprintf("%ARP.psrc%")
            combinations[ip] = mac
    except socket.error as e:
        raise


def scan_local_network():
    combinations = {}
    try:
        for network, netmask, _, interface, address in scapy.config.conf.route.routes:
            # Skip lo and default gateway
            if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                continue
            if netmask <= 0 or netmask == 0xFFFFFFFF:
                continue
            net = to_cidr(network, netmask)
            if net:
                scan_and_print_neighbors(net, interface, combinations)
        return combinations
    except ValueError:
        for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
            # Skip lo and default gateway
            if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                continue
            if netmask <= 0 or netmask == 0xFFFFFFFF:
                continue
            net = to_cidr(network, netmask)
            if net:
                scan_and_print_neighbors(net, interface, combinations)
        return combinations


def set_dns_settings(vic, tar):
    global victims, targets
    victims = vic
    targets = tar


def get_dns_settings():
    return victims, targets
