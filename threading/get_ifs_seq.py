import yaml
import netmiko
import time

def worker(args):
    print(f'{args["hostname"]}: Connecting')
    c = netmiko.ConnectHandler(device_type='cisco_ios',
                           host=args["address"],
                           username='cisco',
                           password='cisco')
    print(f'{args["hostname"]}: Connected')
    c.find_prompt()
    c.enable()
    print(f'{args["hostname"]}: Getting interfaces')
    c.send_command('show ip int brie')
    print(f'{args["hostname"]}: Finished')

if __name__ == "__main__":
    with open('devices.yaml','r') as f:
        devices = yaml.safe_load(f)

    start=time.time()

    for device in devices:
        #args = {'hostname':device['hostname'], 'address':device['address']}
        worker(device)

    duration = time.time() - start
    print(f'\n\nTotal time taken: {duration}')