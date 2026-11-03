import ipaddress
from subnet_calculate import calculate_subnet
from vlsm import calculate_vlsm


def display_subnet():

    print("\n========== BASIC SUBNET CALCULATOR ==========")

    ip_input = input("Enter IP address with CIDR: ")

    try:
        result = calculate_subnet(ip_input)

        print("\n========== SUBNET DETAILS ==========")

        for key, value in result.items():
            print(f"{key:<25}: {value}")

    except ValueError as e:
        print("Invalid input:", e)


def display_vlsm():

    print("\n========== VLSM CALCULATOR ==========")

    network_input = input("Enter main network (e.g. 192.168.1.0/24): ")

    departments = []

    try:
        count = int(input("Enter number of departments: "))

        if count <= 0:
            print("Atleast there should be one Department .")
            return

        # Take department information
        for i in range(count):

            print(f"\nDepartment {i + 1}")

            name = input("Enter department name: ")

            hosts = int(input("Enter required number of hosts: "))

            departments.append({
                "name": name,
                "hosts": hosts
            })

        # Perform VLSM calculation
        results = calculate_vlsm(network_input, departments)

        # Display results
        print("\n========== VLSM ALLOCATION RESULTS ==========")

        for result in results:

            print("\n---------------------------------------------")

            for key, value in result.items():

                print(f"{key:<25}: {value}")

        print("\n=============================================")

    except ValueError as e:
        print("Invalid input or allocation error:", e)


# Main program
while True:

    print("\n")
    print("=" * 50)
    print("           IP SUBNET CALCULATOR")
    print("=" * 50)

    print("1. Basic Subnet Calculator")
    print("2. VLSM Calculator")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        display_subnet()

    elif choice == "2":

        display_vlsm()

    elif choice == "3":

        print("\nThank you for using IP Subnet Calculator!")
        break

    else:

        print("\nInvalid choice! Please select 1, 2 or 3.")
