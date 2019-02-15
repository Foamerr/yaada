class IpToMac:

    def __init__(self):
        """
        Initialises an empty dictionary
        """
        self._ip_to_mac = {}

    def set(self, ip, mac):
        # type: (str, str) -> self
        self._ip_to_mac[ip] = mac.lower()
        return self

    def get(self, ip):
        # type: (str) -> str or None
        if ip in self._ip_to_mac:
            return self._ip_to_mac[ip]

    def set_every(self, ip_to_mac):
        # type: (dict) -> self
        self._ip_to_mac = {}
        for ip in ip_to_mac:
            self.set(ip, ip_to_mac[ip])
        return self

    def get_every(self):
        # type: () -> dict
        return self._ip_to_mac

        return None
