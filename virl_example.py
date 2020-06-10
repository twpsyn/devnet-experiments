import getpass
import netmiko
import logging
from time import sleep

from virl2_client import ClientLibrary

logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(levelname)s %(message)s')

LAB_USERNAME = 'cisco'
LAB_PASSWORD = 'cisco'
VIRL_CONTROLLER = 'virl.twpsyn.com'
VIRL_USERNAME = input('username: ')
VIRL_PASSWORD = getpass.getpass('password: ')

client = ClientLibrary(VIRL_CONTROLLER,
                       VIRL_USERNAME,
                       VIRL_PASSWORD,
                       ssl_verify=False)
client.wait_for_lld_connected()

logging.info("Connected to terminal server")

# this assumes that there's exactly one lab with this title
our_lab = client.find_labs_by_title('Lab1')[0]
xr_node = our_lab.get_node_by_label('S4')

logging.info("Identified lab and device")
# open the Netmiko connection via the terminal server
# (SSH to the controller connects to the terminal server)
c = netmiko.ConnectHandler(device_type='terminal_server',
                           host=VIRL_CONTROLLER,
                           username=VIRL_USERNAME,
                           password=VIRL_PASSWORD)

logging.info("Netmiko connection created")

# send CR, get a prompt on terminal server
c.write_channel('\r\n')
sleep(1)
c.write_channel('\r\n')
sleep(1)

logging.info(f"Opening /{our_lab.id}/{xr_node.id}/0")
# open the connection to the console
c.write_channel(f'open /{our_lab.id}/{xr_node.id}/0\r')

c.write_channel('\r\n')
sleep(1)
c.write_channel('\r\n')
sleep(1)

# router login
# this makes an assumption that it's required to login

#c.write_channel(LAB_USERNAME + '\r')
#c.write_channel(LAB_PASSWORD + '\r')
logging.info("Sending a few carriage returns")
#c.write_channel('\r\n\r\n\r\n')
# switch to Cisco XR mode
netmiko.redispatch(c, device_type='cisco_ios')
c.find_prompt()

# get the list of interfaces
c.enable()
result = c.send_command('show run')
print(result)

# # create the keys
# result = c.send_command('crypto key generate rsa',
#                         expect_string='How many bits in the modul us \[2048\]\: ')
# print(result)

# # send the key length
# c.write_channel('2048\n')

# # retrieve the result
# result = c.send_command('show crypto key mypubkey rsa')
# print(result)
