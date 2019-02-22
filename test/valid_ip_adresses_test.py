import unittest
from validation import *


class ValidIpAddressesTest(unittest.TestCase):
    valid_ipv4 = '172.16.254.1'
    valid_ipv4_min = '0.0.0.0'
    valid_ipv4_max = '255.255.255.255'
    invalid_ipv4_neg = '-172.16.254.1'
    invalid_ipv4_num = '3'
    invalid_ipv4_max = '256.256.256.256'

    def test_is_valid_ipv4(self):
        self.assertEqual(True, is_ipv4_address(self.valid_ipv4))

    def test_is_valid_ipv4_min(self):
        self.assertEqual(True, is_ipv4_address(self.valid_ipv4_min))

    def test_is_valid_ipv4_max(self):
        self.assertEqual(True, is_ipv4_address(self.valid_ipv4_max))

    def test_is_invalid_ipv4_neg(self):
        self.assertEqual(False, is_ipv4_address(self.invalid_ipv4_neg))

    def test_is_invalid_ipv4_num(self):
        self.assertEqual(False, is_ipv4_address(self.invalid_ipv4_num))

    def test_is_invalid_ipv4_max(self):
        self.assertEqual(False, is_ipv4_address(self.invalid_ipv4_max))

    def test_are_ipv4_valid_all(self):
        self.assertEqual(True, are_valid_address([self.valid_ipv4_max, self.valid_ipv4, self.valid_ipv4_min]))

    def test_are_ipv4_valid_one(self):
        self.assertEqual(True, are_valid_address([self.valid_ipv4]))

    def test_are_ipv4_invalid_all(self):
        self.assertEqual(False, are_valid_address([self.invalid_ipv4_neg, self.invalid_ipv4_num,
                                                   self.invalid_ipv4_max]))

    def test_are_ipv4_invalid_one(self):
        self.assertEqual(False, are_valid_address([self.invalid_ipv4_neg]))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
