from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(
    filename="logs/netmiko_global.log",
    level=logging.DEBUG,
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
)
logger = logging.getLogger("netmiko")

DEVICES = [
    {
        "host": "10.144.32.11",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "session_log": "logs/R1.log",
    },
    {
        "host": "10.144.32.12",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "session_log": "logs/R2.log",
    },
]
devip = ""

# for device in DEVICES:


def worker(device):
    logging.info(f"Worker started for device {device['host']}")
    conn = ConnectHandler(**device)
    ips = conn.send_command("show ip int brie")
    print(ips)


with ThreadPoolExecutor(max_workers=5) as executor:
    for device in DEVICES:
        executor.submit(worker, (device))
