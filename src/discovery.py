import netifaces

from scapy.all import srp, conf
from scapy.layers.l2 import Ether, ARP


def arp_ping(netmask="192.168.1.0/24"):
    """
    Returns the IP and MAC-address of all local hosts under with respect to @netmask
    """
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=netmask), timeout=0.1)
    return [rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd, rcv in ans]


def get_default_gateway():
    """
    Returns the default gateway of a host
    """
    gws = netifaces.gateways()
    return str(gws['default'][netifaces.AF_INET][0])

