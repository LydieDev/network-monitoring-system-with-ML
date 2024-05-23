from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_xe",
    host="cisco5.domain.com",
    username="admin",
    password="password",
)

output = net_connect.send_command(
    "show ip arp"
)

cfg_list = [
    "ip access-list extended TEST1",
    "permit ip any host 1.1.1.1",
    "permit ip any host 1.1.1.2",
    "permit ip any host 1.1.1.3",
    "permit ip any host 1.1.1.4",
    "permit ip any host 1.1.1.5",
]
cfg_output = net_connect.send_config_set(cfg_list)
net_connect.save_config()