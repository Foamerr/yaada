import sys
from scapy.all import srp,Ether,ARP,conf

def arp_ping(netmask="192.168.1.0/24"):
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=netmask), 
              timeout=2)
    return [rcv.sprintf(r"%Ether.src% at %ARP.psrc%") for snd,rcv in ans]
