import unittest
from discovery import *


class ValidDefaultGatewayTest(unittest.TestCase):

    def test_is_valid_default_gateway(self):
        gateways = ['192.168.2.254']
        found = get_default_gateway()
        self.assertEqual(True, found in gateways)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
