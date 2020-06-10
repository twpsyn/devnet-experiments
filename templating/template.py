import yaml
import jinja2

with open('devices.yaml','r') as f:
    devices = yaml.safe_load(f)

with open('swtemplate.j2','r') as f:
    template = jinja2.Template(f.read())

for device in devices:
    print(template.render(device=device))



