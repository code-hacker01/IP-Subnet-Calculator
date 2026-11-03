
import streamlit as st

from subnet_calculate import calculate_subnet
from vlsm import calculate_vlsm


st.set_page_config(
    page_title="IP Subnet Calculator",
    page_icon="🌐",
    layout="wide"
)

# APPLICATION TITLE

st.title("🌐 IP Subnet Calculator")

st.write(
    "A networking tool to calculate IPv4 subnet details "
    "and perform Variable Length Subnet Masking (VLSM)."
)

st.divider()

# CREATE TABS


basic_tab, vlsm_tab = st.tabs([
    "📡 Basic Subnet Calculator",
    "🔢 VLSM Calculator"
])


# BASIC SUBNET CALCULATOR


with basic_tab:

    st.header("Basic Subnet Calculator")

    st.write(
        "Enter an IPv4 address with its CIDR prefix "
        "to calculate the subnet information."
    )

    ip_input = st.text_input(
        "Enter IP Address with CIDR",
        placeholder="Example: 192.168.1.10/24"
    )

    if st.button("Calculate Subnet", key="basic_button"):

        if not ip_input.strip():

            st.warning("Please enter an IP address.")

        else:

            try:

                result = calculate_subnet(ip_input.strip())

                st.success("Subnet calculated successfully!")

                st.subheader("Subnet Details")

                # Display results in a table
                for key, value in result.items():

                    st.write(f"**{key}:** {value}")

            except ValueError as e:

                st.error(f"Invalid Input: {e}")

# VLSM CALCULATOR


with vlsm_tab:

    st.header("VLSM Calculator")

    st.write(
        "Divide a large network into smaller subnets "
        "according to the host requirements of different departments."
    )

    network_input = st.text_input(
        "Enter Main Network",
        placeholder="Example: 192.168.1.0/24",
        key="network_input"
    )

    st.subheader("Department Requirements")

    st.info(
        "Enter the department name and required number of hosts."
    )

    # Number of departments
    department_count = st.number_input(
        "Number of Departments",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    departments = []

    # Generate input fields dynamically
    for i in range(int(department_count)):

        st.markdown(f"**Department {i + 1}**")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Department Name",
                key=f"name_{i}",
                placeholder="Example: ML"
            )

        with col2:

            hosts = st.number_input(
                "Required Hosts",
                min_value=1,
                value=50,
                step=1,
                key=f"hosts_{i}"
            )

        departments.append({
            "name": name.strip(),
            "hosts": int(hosts)
        })

    st.divider()

    if st.button("Calculate VLSM", key="vlsm_button"):

        if not network_input.strip():

            st.warning("Please enter the main network.")

        elif any(not department["name"] for department in departments):

            st.warning("Please enter all department names.")

        else:

            try:

                # Call VLSM calculation function
                results = calculate_vlsm(
                    network_input.strip(),
                    departments
                )

                st.success("VLSM allocation completed successfully!")

                st.subheader("VLSM Allocation Results")

                # Display results as a table
                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

            except ValueError as e:

                st.error(f"VLSM Error: {e}")


# FOOTER


st.divider()

st.caption(
    "IP Subnet Calculator | Computer Networks Project"
)
