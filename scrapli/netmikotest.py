import yaml
import jinja2
from netmiko import ConnectHandler
from time import time as nowtime

starttime = nowtime()

with open("devices.yaml", "r") as f:
    devices = yaml.safe_load(f)

with open("template.j2", "r") as f:
    template = jinja2.Template(f.read())

for device in devices:

    conn = ConnectHandler(
        host=device["address"],
        username="cisco",
        password="cisco",
        device_type="cisco_ios",
    )

    conf_to_send = template.render(device=device).splitlines()
    conn.send_config_set(conf_to_send)

runtime = nowtime() - starttime
print(f"Took {runtime} seconds to complete")
