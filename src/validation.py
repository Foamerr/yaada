import socket


def are_valid_address(addresses):
    """
    Returns whether or not a list of addresses contains only valid IPv4 or IPv6 addresses.

    :param addresses: list of IP addresses
    :return True if all addresses in addresses are valid IPv4 or IPv6 addresses
    """
    for address in addresses:
        if not is_ipv6_address(address) or is_ipv4_address(address):
            return False
    return True


def is_ipv4_address(address):
    """
    Returns whether or not an address is a valid IPv4 address
    From: https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

    :param address: IP address
    :return True if address is a valid IPv4 address. Otherwise, false
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True


def is_ipv6_address(address):
    """
    Returns whether or not an address is a valid IPv6 address

    :param address: IP address
    :return True if address is a valid IPv6 address. Otherwise, false
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True
