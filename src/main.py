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

# python3 src/main.py --key ${KEY} --number_devices ${NUMBER_DEVICES} --output_volume 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate customer purchase transactions from simulated edge devices.')
    parser.add_argument('-k', '--key', help='Pipeline key to use', required=True)
    parser.add_argument('-n', '--number_devices', help='Number of devices to simulate', required=True, type=int)
    parser.add_argument('--url', help='Mezmo URL', default='https://pipeline.mezmo.com')
    parser.add_argument('-d', '--debug', help='Debug local logging flag', default=False, action='store_true')
    parser.add_argument('--output_device', help='Output device data', default=True, action='store_true')
    parser.add_argument('--output_volume', help='Output running volume', default=False, action='store_true')
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
                , output_packet=args.output_device
                , debug=args.debug
                , output_volume=args.output_volume
                )
            )

    while True: # Loop forever to simulate edge device
        random.choice(devices).genAndSendTransaction()
        if args.output_volume and random.uniform(0,1.0) < 0.05: # do this roughly every ten
            total_vol_gb = 0.0
            for device in devices: total_vol_gb+= device.running_volume*1e-6
            print('\nrunning total: {:.5f} GB\n'.format(total_vol_gb)) # in GB
        sleeptime = random.uniform(0, .001) # Sleep between 0 and 1 seconds
        time.sleep(sleeptime)