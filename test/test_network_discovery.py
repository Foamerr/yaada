import unittest
from src.discovery import Device
from test.predefined_test import PredefinedTest


class NetworkDiscoveryTest(PredefinedTest):
    ip_to_find = '192.168.56.103'
    mac_to_find = '30:9c:23:d9:73:97'  # '08:00:27:32:f4:6a'
    interface = 'Ethernet'  # enp0s3

    def test_own_ip_address(self):
        self.assertEqual(self.ip_to_find, Device().get_local_ip())

    def test_own_mac_address(self):
        self.assertEqual(self.mac_to_find, Device().get_local_mac())

    # TODO: Test ip to mac mapping


if __name__ == '__main__':
    unittest.main()
