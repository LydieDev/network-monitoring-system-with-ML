# from scapy.all import ARP, Ether, srp

# def scan_devices(ip_range):
#     # Create an ARP request for the specified IP range
#     arp_request = ARP(pdst=ip_range)
    
#     # Create an Ethernet frame with a destination MAC address of broadcast
#     ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    
#     # Combine the ARP request and Ethernet frame
#     packet = ether_frame / arp_request
    
#     # Send the packet and receive the response
#     result = srp(packet, timeout=3, verbose=0)[0]
    
#     # List to store the discovered IP and MAC addresses of devices
#     devices_list = []
    
#     # Parse the responses
#     for sent, received in result:
#         devices_list.append({'ip': received.psrc, 'mac': received.hwsrc})
    
#     return devices_list

# # Specify the IP address range to scan (e.g., "192.168.1.0/24")
# ip_range = "192.168.1.0/24"

# # Execute the scan
# devices = scan_devices(ip_range)

# # Display the results
# for device in devices:
#     print(f"IP: {device['ip']}\tMAC: {device['mac']}")


from scapy.all import IP, ICMP, sr1

def ping(target_ip):
    # Create an IP packet with an ICMP layer
    packet = IP(dst=target_ip) / ICMP()

    # Send the packet and wait for a response
    response = sr1(packet, timeout=2, verbose=0)

    # Check if a response was received
    if response:
        print(f"Response received from {target_ip}")
    else:
        print(f"No response received from {target_ip}")

# Specify the target IP address
target_ip = "8.8.8.8"

# Perform a simple ping using Scapy
ping(target_ip)

