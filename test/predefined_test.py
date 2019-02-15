import unittest
from src.ip_to_mac import IpToMac


class PredefinedTest(unittest.TestCase):

    def set_up(self):
        self.combined_list = IpToMac().set_every({
            '192.168.56.101': '08:00:27:B0:A1:AB',
            '192.168.56.102': '08:00:27:C6:A4:61'})
