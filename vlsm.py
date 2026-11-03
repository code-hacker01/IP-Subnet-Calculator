
import ipaddress


def calculate_prefix(hosts):

    # Find the minimum number of bits needed
    # for network and broadcast addresses too
    required_addresses = hosts + 2

    host_bits = (required_addresses - 1).bit_length()

    prefix = 32 - host_bits

    return prefix


def calculate_vlsm(network_input, departments):

    # Convert main network into IPv4 network
    main_network = ipaddress.ip_network(
        network_input, strict=False
    )

    if not isinstance(main_network, ipaddress.IPv4Network):
        raise ValueError("Only IPv4 networks are supported.")

    # Sort departments by hosts in descending order
    departments = sorted(
        departments,
        key=lambda x: x["hosts"],
        reverse=True
    )

    results = []

    # Start allocation from the main network address
    current_address = int(main_network.network_address)

    for department in departments:

        name = department["name"]
        required_hosts = department["hosts"]

        if required_hosts < 1:
            raise ValueError("Host requirement must be positive.")

        # Calculate required subnet prefix
        prefix = calculate_prefix(required_hosts)

        if prefix < main_network.prefixlen:
            raise ValueError(
                f"{name} requires more addresses than the main network provides."
            )

        # Find the next suitable subnet boundary
        subnet_size = 2 ** (32 - prefix)

        current_address = (
            (current_address + subnet_size - 1) // subnet_size
        ) * subnet_size

        # Create subnet
        subnet = ipaddress.ip_network(
            (current_address, prefix)
        )

        # Check whether subnet fits inside main network
        if not subnet.subnet_of(main_network):
            raise ValueError(
                f"Not enough network space for {name}."
            )

        # Calculate usable host range
        if prefix == 32:
            first_host = subnet.network_address
            last_host = subnet.network_address

        else:
            first_host = subnet.network_address + 1
            last_host = subnet.broadcast_address - 1

        if prefix == 32:
            usable_hosts = 1
        elif prefix == 31:
            usable_hosts = 2
        else:
            usable_hosts = subnet.num_addresses - 2

        # Store results
        results.append({
            "Department": name,
            "Required Hosts": required_hosts,
            "Network Address": str(subnet.network_address),
            "CIDR": f"/{prefix}",
            "Subnet Mask": str(subnet.netmask),
            "First Host": str(first_host),
            "Last Host": str(last_host),
            "Broadcast Address": str(subnet.broadcast_address),
            "Usable Hosts": usable_hosts
        })

        # Move to the next available address
        current_address = int(subnet.broadcast_address) + 1

    return results
