from scrapli import Scrapli
from concurrent.futures import ThreadPoolExecutor
import logging

DEVICES = [
    {
        "host": "10.144.32.11",
        "auth_username": "cisco",
        "auth_password": "cisco",
        "platform": "cisco_iosxe",
        "auth_strict_key": False,
        "transport_options": {"open_cmd": ["-o", "PubkeyAuthentication=no"]}
        # "transport": "ssh2",
    },
    {
        "host": "10.144.32.12",
        "auth_username": "cisco",
        "auth_password": "cisco",
        "platform": "cisco_iosxe",
        "auth_strict_key": False,
        "transport_options": {"open_cmd": ["-o", "PubkeyAuthentication=no"]}
        # "transport": "ssh2",
    },
]

logging.basicConfig(
    filename="logs/scrapli_basic.log",
    level=logging.DEBUG,
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
)


def worker(device):
    conn = Scrapli(**device)
    conn.open()
    ips = conn.send_command("show ip int brie").result
    print(ips)
    conn.close()


with ThreadPoolExecutor(max_workers=5) as executor:
    for device in DEVICES:
        executor.submit(worker, (device))
