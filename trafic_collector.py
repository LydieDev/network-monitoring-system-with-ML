import pyshark
import socket

known_services = {
    20: "ftp_data",
    21: "ftp_control",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    67: "dhcp_server",
    68: "dhcp_client",
    69: "tftp",
    80: "http",
    110: "pop3",
    115: "sftp",
    123: "ntp",
    143: "imap",
    161: "snmp",
    179: "bgp",
    194: "irc",
    443: "https",
    989: "ftp_secure_data",
    990: "ftp_secure_control",
    993: "imaps",
    995: "pop3s",
    1723: "pptp",
    3306: "mysql",
    3389: "rdp",
    5060: "sip",
    5061: "sips",
    8080: "http_proxy",
}

def get_connection_state(flag_code):
    flag_int = int(flag_code, 16)
    SYN_FLAG = 0x02
    ACK_FLAG = 0x10
    RST_FLAG = 0x04

    if flag_int & SYN_FLAG and flag_int & ACK_FLAG:
        return 'SF'  
    elif flag_int & SYN_FLAG:
        return 'SO'  
    elif flag_int & RST_FLAG:
        return 'REJ' 
    else:
        return 'SF' 

dst_hosts_info = {}

def get_service_name(port):
    if port in known_services:
        return known_services[port]
    else:
        return "private"

def update_dst_host_info(dst_ip, service_name):
    if dst_ip in dst_hosts_info:
        dst_hosts_info[dst_ip]["total_count"] += 1
        if service_name == dst_hosts_info[dst_ip]["last_service"]:
            dst_hosts_info[dst_ip]["same_srv_count"] += 1
        else:
            dst_hosts_info[dst_ip]["diff_srv_count"] += 1
        dst_hosts_info[dst_ip]["last_service"] = service_name
    else:
        dst_hosts_info[dst_ip] = {
            "total_count": 1,
            "same_srv_count": 1,
            "diff_srv_count": 0,
            "last_service": service_name,
        }

def packet_callback(packet):
    try:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        src_port = packet.tcp.srcport if 'TCP' in packet else packet.udp.srcport if 'UDP' in packet else ""
        dst_port = packet.tcp.dstport if 'TCP' in packet else packet.udp.dstport if 'UDP' in packet else ""
        protocol_type = packet.transport_layer 
        service_name = get_service_name(int(dst_port)) 
        flag = get_connection_state(packet.tcp.flags) if 'TCP' in packet else packet.udp.flags if 'UDP' in packet else 'SF' 
        src_bytes = packet.tcp.len if 'TCP' in packet else "" 
        dst_bytes = packet.length  
        count=1
        update_dst_host_info(dst_ip, service_name)

        same_srv_rate = (dst_hosts_info[dst_ip]["same_srv_count"] / dst_hosts_info[dst_ip]["total_count"])  if dst_hosts_info[dst_ip]["total_count"] > 0 else ""
        diff_srv_rate = (dst_hosts_info[dst_ip]["diff_srv_count"] / dst_hosts_info[dst_ip]["total_count"]) if dst_hosts_info[dst_ip]["total_count"] > 0 else ""
        dst_host_srv_count = dst_hosts_info[dst_ip]["total_count"]
        dst_host_same_srv_rate = same_srv_rate
        packet_data = f"{src_ip},{dst_ip},{src_port},{dst_port},{protocol_type},{service_name},{flag},{src_bytes},{dst_bytes},{count},{same_srv_rate},{diff_srv_rate},{dst_host_srv_count},{dst_host_same_srv_rate}\n"

        with open('captured_traffic.csv', 'a') as f:
            f.write(packet_data)

    except AttributeError as e:
        pass

def capture_wifi_traffic(interface='Wi-Fi 3'):
    print(f"Capture du trafic WiFi sur l'interface {interface}...")

    capture = pyshark.LiveCapture(interface=interface)

    capture.apply_on_packets(packet_callback)

if __name__ == "__main__":
    with open('captured_traffic.csv', 'w') as f:
        f.write("src_ip,dst_ip,src_port,dst_port,protocol_type,service,flag,src_bytes,dst_bytes,count,same_srv_rate,diff_srv_rate,dst_host_srv_count,dst_host_same_srv_rate\n")

    capture_wifi_traffic()