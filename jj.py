import os
from scapy.all import sniff, wrpcap

def packet_callback(packet):
    # Callback function to process each captured packet
    # You can customize this function to extract specific information from the packets
    print(packet.summary())

# Spécifiez le nom de l'interface réseau que vous souhaitez capturer
interface_name = "Wi-Fi 3"  # Remplacez par le nom de votre interface

# Set the file path to the user's home directory
file_path = os.path.expanduser("capture.pcap")

# Print a message indicating the start of the script
print("Script execution started.")

# Print a message indicating the start of packet capture
print(f"Starting packet capture on interface: {interface_name}...")

try:
    # Perform packet capture on the specified interface and save to the specified file
    sniffed_packets = sniff(iface=interface_name, prn=packet_callback, store=1, count=1000000)  # Adjust count as needed
    wrpcap(file_path, sniffed_packets)
    print(f"Captured packets are saved to: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Print a message indicating the end of the script
print("Script execution complete.")
