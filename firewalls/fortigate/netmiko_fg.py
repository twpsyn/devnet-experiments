import re

from netmiko import ConnectHandler

key_pattern = re.compile(r"New API key: (?P<apikey>\S+)")

device = {
    "host": "10.144.0.2",
    "username": "admin",
    "password": "admin",
    "device_type": "fortinet",
    "session_log": "private/netmiko_fg.log",
}

create_api_commands = [
    "config system api-user",
    "edit Script_API_User",
    'set accprofile "super_admin"',
    'set vdom "root"',
    "config trusthost",
    "edit 1",
    "set ipv4-trusthost 0.0.0.0 0.0.0.0",
    "next",
    "end",
    "next",
    "end",
]

print(" Connecting ".center(40, "#"))

conn = ConnectHandler(**device)

print(" Creating API User ".center(40, "#"))

conn.send_config_set(create_api_commands)

print(" Generating API Key ".center(40, "#"))

response = conn.send_command("execute api-user generate-key Script_API_User")

key = key_pattern.search(response).group("apikey")
print(f"\nAPI key = {key}")
