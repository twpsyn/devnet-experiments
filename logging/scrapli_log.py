from scrapli import Scrapli
from scrapli.logging import enable_basic_logging
from concurrent.futures import ThreadPoolExecutor

DEVICES = [
    {
        "host": "10.144.32.11",
        "auth_username": "cisco",
        "auth_password": "cisco",
        "platform": "cisco_iosxe",
        "auth_strict_key": False,
        "transport": "ssh2",
    },
    {
        "host": "10.144.32.12",
        "auth_username": "cisco",
        "auth_password": "cisco",
        "platform": "cisco_iosxe",
        "auth_strict_key": False,
        "transport": "ssh2",
    },
]

enable_basic_logging(file="logs/scrapli.log", level="debug", mode="write")


def worker(device):
    conn = Scrapli(**device)
    conn.open()
    ips = conn.send_command("show ip int brie")
    print(ips.result)
    conn.close()


with ThreadPoolExecutor(max_workers=5) as executor:
    for device in DEVICES:
        executor.submit(worker, (device))
