import yaml
import netmiko
import time
import jinja2
import getpass
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from virl2_client import ClientLibrary

DEFAULTS = {
    "domainname": "lab.home",
    "mgmt_subnet": "255.255.255.0",
    "mgmt_vrf": "mgmt-vrf",
    "mgmt_vlan": "10",
    "default_gw": "10.144.35.1",
    "dev_username": "cisco",
    "dev_password": "cisco",
    "lab_id": "Lab1",
}

print_lock = Lock()


def config_worker(param):

    netmiko_delay = 0.1

    client = ClientLibrary(
        param["virl_controller"],
        param["virl_username"],
        param["virl_password"],
        ssl_verify=False,
    )
    client.wait_for_lld_connected()

    with print_lock:
        print(f"{param['hostname']}: Connected to VIRL")

    our_lab = client.find_labs_by_title(param["lab_id"])[0]
    our_node = our_lab.get_node_by_label(param["hostname"])

    with print_lock:
        print(
            f"{param['hostname']}: Identified lab and device: /{our_lab.id}/{our_node.id}/0"
        )

    c = netmiko.ConnectHandler(
        device_type="terminal_server",
        host=param["virl_controller"],
        username=param["virl_username"],
        password=param["virl_password"],
    )

    with print_lock:
        print(f"{param['hostname']}: Connected to terminal server")

    c.write_channel("\r\n")
    time.sleep(1)
    c.write_channel("\r\n")
    time.sleep(1)

    c.write_channel(f"open /{our_lab.id}/{our_node.id}/0\r")

    c.write_channel("\r\n")
    time.sleep(1)
    c.write_channel("\r\n")
    time.sleep(1)
    c.write_channel("\r\n")
    time.sleep(1)
    c.write_channel("\r\n")

    with print_lock:
        print(f"{param['hostname']} : Switching to IOS interpreter")
    try:
        netmiko.redispatch(c, device_type="cisco_ios")
    except Exception as e:
        with print_lock:
            print(f"{param['hostname']} : Failed to switch to IOS interpreter. {e}")
    c.find_prompt()
    # c.enable()

    with print_lock:
        print(f"{param['hostname']} : Preparing config")
    try:
        with open("swtemplate.j2", "r") as f:
            template = jinja2.Template(f.read())
        config_to_send = template.render(device=param).split("\n")
    except:
        with print_lock:
            print(f"{param['hostname']} : Failed to prepare config")

    with print_lock:
        print(f"{param['hostname']} : Sending config")

    try:
        # I have found that console messages can upset netmiko,
        # so turn them off with a timed command
        c.send_command_timing("enable", netmiko_delay)
        c.send_command_timing("conf t", netmiko_delay)
        c.send_command_timing("no logging console", netmiko_delay)
        c.send_command_timing("end", netmiko_delay)
        time.sleep(1)
        c.write_channel("\r\n")
        c.find_prompt()
        c.send_config_set(config_to_send)
        with print_lock:
            print(f"{param['hostname']} : Config sent")

    except Exception as e:
        with print_lock:
            print(f"{param['hostname']} : Error, send config failed. {e}")


if __name__ == "__main__":
    with open("devices.yaml", "r") as f:
        devices = yaml.safe_load(f)

    DEFAULTS["virl_controller"] = input("VIRL controller: ")
    DEFAULTS["virl_username"] = input("VIRL username: ")
    DEFAULTS["virl_password"] = getpass.getpass("VIRL password: ")

    with ThreadPoolExecutor(max_workers=5) as executor:
        for device in devices:
            executor.submit(config_worker, ({**DEFAULTS, **device}))
