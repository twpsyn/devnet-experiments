import yaml
import jinja2
from scrapli import Scrapli
from time import time as nowtime

starttime = nowtime()

with open("devices.yaml", "r") as f:
    devices = yaml.safe_load(f)

with open("template.j2", "r") as f:
    template = jinja2.Template(f.read())

for device in devices:

    conn = Scrapli(
        host=device["address"],
        auth_username="cisco",
        auth_password="cisco",
        auth_strict_key=False,
        platform="cisco_iosxe",
        transport_options={"open_cmd": ["-o", "PubkeyAuthentication=no"]}
        # transport="ssh2"
    )

    conn.open()
    conf_to_send = template.render(device=device)
    result = conn.send_config(config=conf_to_send)

runtime = nowtime() - starttime
print(f"Took {runtime} seconds to complete")
