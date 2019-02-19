class Host:

    def __init__(self, mac, ipv4):
        self.mac = mac
        self.ipv4 = ipv4

    def __str__(self):
        return self.mac + "at" + self.ipv4
