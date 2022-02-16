import re

from scrapli import Scrapli

key_pattern = re.compile(r"New API key: (?P<apikey>\S+)")

device = {
    "host": "10.144.0.2",
    "auth_username": "admin",
    "auth_password": "admin",
    "platform": "fortinet_fortigate",
    "transport": "ssh2",
    "auth_strict_key": False,
    "channel_log": "private/scrapli_fg.log",
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

print(" Connecting ".center(40, '#'))
conn = Scrapli(**device)
conn.open()

print(" Creating API User ".center(40, '#'))

conn.send_configs(create_api_commands)

print(" Generating API Key ".center(40, '#'))

response = conn.send_command("execute api-user generate-key Script_API_User")

key = key_pattern.search(response.result).group("apikey")
print(f"\nAPI key = {key}")
