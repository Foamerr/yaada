from scapy.all import srp, conf
from scapy.layers.l2 import Ether, ARP


def arp_ping(netmask="192.168.1.0/24"):
    """
    Returns the IP and MAC-address of all local hosts under with respect to @netmask
    """
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=netmask), timeout=2)
    return [rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd, rcv in ans]
