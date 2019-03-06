import netifaces

from scapy.all import srp, conf
from scapy.layers.l2 import Ether, ARP


def arp_ping(netmask="192.168.1.0/24"):
    """
    Returns the IP and MAC-address of all local hosts under with respect to @netmask
    """
    # TODO: Doesn't find actual local host IP even with a long timeout?
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=netmask), timeout=0.2)
    return [rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd, rcv in ans]


def get_default_gateway():
    """
    Returns the default gateway of a host
    """
    gws = netifaces.gateways()
    return str(gws['default'][netifaces.AF_INET][0])


def get_local_host_ip():
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
