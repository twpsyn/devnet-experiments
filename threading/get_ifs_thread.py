import yaml
import netmiko
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

printlock = Lock()

def worker(args):
    with printlock:
        print(f'{args["hostname"]}: Connecting')
    c = netmiko.ConnectHandler(device_type='cisco_ios',
                           host=args["address"],
                           username='cisco',
                           password='cisco')
    with printlock:
        print(f'{args["hostname"]}: Connected')
    c.find_prompt()
    c.enable()
    with printlock:
        print(f'{args["hostname"]}: Getting interfaces')
    c.send_command('show ip int brie')
    with printlock:
        print(f'{args["hostname"]}: Finished')


if __name__ == "__main__":
    with open('devices.yaml','r') as f:
        devices = yaml.safe_load(f)

    start=time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for device in devices:
            executor.submit(worker, (device))

    duration = time.time() - start
    print(f'\n\nTotal time taken: {duration}')