
import ipaddress


def calculate_subnet(ip_input):

    # Step 1: Convert input into an IP interface
    interface = ipaddress.ip_interface(ip_input)

    # Step 2: Check whether it is IPv4
    if not isinstance(interface, ipaddress.IPv4Interface):
        raise ValueError("Only IPv4 addresses are supported.")

    # Step 3: Get network information
    network = interface.network

    ip_address = interface.ip
    subnet_mask = network.netmask
    network_address = network.network_address
    broadcast_address = network.broadcast_address

    # Step 4: Calculate total and usable hosts
    total_addresses = network.num_addresses

    if network.prefixlen == 32:
        usable_hosts = 1
        first_host = network.network_address
        last_host = network.network_address

    elif network.prefixlen == 31:
        usable_hosts = 2
        first_host = network.network_address
        last_host = network.broadcast_address

    else:
        usable_hosts = total_addresses - 2
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1

    # Step 5: Return results
    return {
        "IP Address": ip_address,
        "CIDR Prefix": f"/{network.prefixlen}",
        "Subnet Mask": subnet_mask,
        "Network Address": network_address,
        "Broadcast Address": broadcast_address,
        "First Usable Host": first_host,
        "Last Usable Host": last_host,
        "Total IP Addresses": total_addresses,
        "Usable Hosts": usable_hosts
    }
