'''
This is a very simple python script that simulates customer transactions at
a number of credit card terminals for Mezmo's Pipeline Workshops.

Sends data from N devices to Mezmo's Pipeline platform via RESTFUL Posts.

Usage: python main.py --key MEZMO_KEY --number_devices 7
'''

import time
import random
import argparse
from faker import Faker

from Device import Device

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate customer purchase transactions from simulated edge devices.')
    parser.add_argument('-k', '--key', help='Pipeline key to use', required=True)
    parser.add_argument('-n', '--number_devices', help='Number of devices to simulate', required=True, type=int)
    parser.add_argument('--url', help='Mezmo URL', default='https://pipeline.mezmo.com')
    parser.add_argument('-d', '--debug', help='Debug local logging flag', default=False, action='store_true')
    args = parser.parse_args()
    
    # Seed random
    random.seed(42)
    gen_faker = Faker()


    # Add n devices to a list to manage
    devices = []
    for i in range(args.number_devices):
        devices.append(
            Device(
                  device_id=gen_faker.uuid4()
                , device_name=gen_faker.unix_device()
                , device_vrs='1.{}.{}'.format(random.randint(0, 9), random.randint(0, 9))
                , device_location=gen_faker.local_latlng()
                , device_status='active'
                , mezmo_key=args.key
                , mezmo_url=args.url
                , output_packet=True
                , debug=args.debug
                )
            )

    while True: # Loop forever to simulate edge device
        random.choice(devices).genAndSendTransaction()
        sleeptime = random.uniform(0, 1) # Sleep between 0 and 1 seconds
        time.sleep(sleeptime)