#!/usr/bin/env python3
'''Practice calculating VLSM'''

# * * * * * * * Dependencies * * * * * * * 
import random, os

# * * * * * * * Global Variables * * * * * * * 
IP_address = ""
CIDR = 0
interesting_octet = 0
subnet_mask = ""
wildcard_mask = ""
block_size = 0
network_address = ""
first_host_address = ""
last_host_address = ""
broadcast_address = ""
available_subnets = ""
hosts_per_subnet = ""
persistent_display = ""


# * * * * * * * Functions * * * * * * * 
def generate_IP():
    global IP_address

    IP_address = str(random.randrange(1,255)) + "." + str(random.randrange(0,255)) + "." + str(random.randrange(0,255)) + "." + str(random.randrange(0,255))


def generate_CIDR():
    global CIDR
    
    CIDR = random.randrange(1,31)


def calculate_interesting_octet():
    global interesting_octet

    if CIDR < 8:
        interesting_octet = "1"
    elif CIDR < 16:
        interesting_octet = "2"
    elif CIDR < 24:
        interesting_octet = "3"
    else:
        interesting_octet = "4"


#def ask_question(question, answer, print_a=True):  # DISABLE for LIVE (enable this instead of the next line to print the answers for testing purposes)
def ask_question(question, answer, print_a=False):
    global persistent_display

    if print_a:
        user_answer = input(question + " (" + str(answer) + "): ")
    else:
        user_answer = input(question + ": ")

    while True:
        if str(user_answer) != str(answer):
            user_answer = input("Incorrect. " + question + ": ")
        else:
            os.system("clear")
            persistent_display = persistent_display + "\n" + question + ": " + str(answer)
            print(persistent_display)
            break


def calculate_subnet_mask():
    global subnet_mask

    num_full_octet = int(CIDR / 8)

    i = 0
    while i < num_full_octet:
        subnet_mask = subnet_mask + "255."
        i = i + 1

    int_oct_bits = CIDR - (num_full_octet * 8)
    #print(num_full_octet)
    #print(int_oct_bits)

    i = 8
    int_oct_mask = 0
    while i > (8 - int_oct_bits):
        #print("int_oct_mask = int_oct_mask + 2**(" + str(i-1) + ")")
        int_oct_mask = int_oct_mask + (2**(i-1))
        i = i - 1

    #print(int_oct_mask)
    #print(int_oct_bits)

    subnet_mask = subnet_mask + str(int_oct_mask)

    num_octets = num_full_octet + 1

    while num_octets < 4:
        subnet_mask = subnet_mask + ".0"
        num_octets = num_octets + 1


def calculate_wildcard_mask():
    global wildcard_mask
    wildcard_mask = ""

    subnet_mask_octets_list = subnet_mask.split(".")

    i = 0
    while i < 4:
        wildcard_mask = wildcard_mask + str(255 - int(subnet_mask_octets_list[i])) + "."
        i = i + 1

    wildcard_mask = wildcard_mask[0:len(wildcard_mask)-1]


def calculate_block_size():
    global block_size

    subnet_mask_octets_list = subnet_mask.split(".")

    i = 0
    while True:
        if subnet_mask_octets_list[i] != "255":
            block_size = 256 - int(subnet_mask_octets_list[i])
            break
        i = i + 1


def calculate_network_address():
    global network_address

    # Divide the IP address into octets and put them into a list
    octet_list = IP_address.split(".")

    # Get the value of the interesting octet (for instance, 10.0.0.100/24 would be "100")
    interesting_octet_value = octet_list[int(interesting_octet)-1]

    # Intiger division of the value in the interesting octet by block size times block size to get nearest value
    int_oct_net_address = (int(interesting_octet_value) // block_size) * block_size

    # Add network bits to network_address
    i = 0
    while i < int(interesting_octet)-1:
        network_address = network_address + octet_list[i] + "."
        i = i + 1

    network_address = network_address + str(int_oct_net_address)

    # If the interesting octet is not 4, the network address will include one or more octets of zeros
    while len(network_address.split(".")) < 4:
        network_address = network_address + ".0"


def calculate_first_host_address():
    global first_host_address

    network_address_octet_list = network_address.split(".")

    i = 0
    while i < 3:
        first_host_address = first_host_address + network_address_octet_list[i] + "."
        i = i + 1

    first_host_address = first_host_address + str(int(network_address_octet_list[3]) + 1)


def calculate_last_host_address():
    global last_host_address

    network_address_octet_list = network_address.split(".")
    interesting_octet_value = network_address_octet_list[int(interesting_octet) - 1]

    i = 0
    while i < int(interesting_octet) - 1:
        last_host_address = last_host_address + network_address_octet_list[i] + "."
        i = i + 1

    if int(interesting_octet) < 4:
        last_host_address = last_host_address + str(int(interesting_octet_value) + block_size - 1)

        while len(last_host_address.split(".")) < 3:
            last_host_address = last_host_address + ".255"

        last_host_address = last_host_address + ".254"

    else:
        last_host_address = last_host_address + str(int(interesting_octet_value) + block_size - 2)


def calculate_broadcast_address():
    global broadcast_address, last_host_address

    last_host_octet_list = last_host_address.split(".")
    interesting_octet_value = last_host_octet_list[int(interesting_octet) - 1]

    i = 0
    while i < int(interesting_octet) - 1:
        broadcast_address = broadcast_address + last_host_octet_list[i] + "."
        i = i + 1

    if int(interesting_octet) < 4:
        broadcast_address = broadcast_address + str(int(interesting_octet_value))

        while len(broadcast_address.split(".")) < 4:
            broadcast_address = broadcast_address + ".255"

    else:
        broadcast_address = broadcast_address + str(int(interesting_octet_value) + 1)


def calculate_available_subnets():
    global available_subnets

    available_subnets = int(256 / block_size)


def calculate_hosts_per_subnet():
    global hosts_per_subnet

    hosts_per_subnet = 2**(32-CIDR) - 2


# * * * * * * * Steps * * * * * * * 

def main():
    global IP_address, CIDR, interesting_octet, subnet_mask, block_size, network_address, first_host_address, last_host_address, broadcast_address, available_subnets, hosts_per_subnet, persistent_display

    # Generate a random IP address with CIDR notation
    generate_IP()
    generate_CIDR()

    # Clear the screen and display the random IP address and CIDR to the user
    os.system("clear")
    persistent_display = "IP address: " + IP_address + "/" + str(CIDR)
    print(persistent_display)

    # Calculate all the values
    calculate_interesting_octet()
    calculate_subnet_mask()
    calculate_wildcard_mask()
    calculate_block_size()
    calculate_network_address()
    calculate_first_host_address()
    calculate_last_host_address()
    calculate_broadcast_address()
    calculate_available_subnets()
    calculate_hosts_per_subnet()

    # Ask the user for the values
    ask_question("Interesting octet", interesting_octet)
    ask_question("Subnet mask", subnet_mask)
    ask_question("Wildcard mask", wildcard_mask)
    ask_question("Block size", block_size)
    ask_question("Network address", network_address)
    ask_question("First host address", first_host_address)
    ask_question("Last host address", last_host_address)
    ask_question("Broadcast address", broadcast_address)
    ask_question("Number of available subnets", available_subnets)
    ask_question("Number of hosts per subnet", hosts_per_subnet)


if __name__ == '__main__':
	main()