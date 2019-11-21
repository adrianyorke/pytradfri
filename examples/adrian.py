#!/usr/bin/env python3

import time

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

DELAY_SECONDS = 0.5
CONFIG_FILE = "/home/vagrant/ikea/tradfri_standalone_psk.conf"

host = "192.168.10.44"
conf = load_json(CONFIG_FILE)

identity = conf[host].get('identity')
psk = conf[host].get('key')
api_factory = APIFactory(host=host, psk_id=identity, psk=psk)

api = api_factory.request

gateway = Gateway()

devices_command = gateway.get_devices()
devices_commands = api(devices_command)
devices = api(devices_commands)

lights = [dev for dev in devices if dev.has_light_control]

# Print all lights
print(lights)

for _ in range(10):
    dim_command = lights[1].light_control.set_dimmer(0)
    api(dim_command)
    dim_command = lights[2].light_control.set_dimmer(0)
    api(dim_command)
    time.sleep(DELAY_SECONDS)

    dim_command = lights[1].light_control.set_dimmer(254)
    api(dim_command)
    dim_command = lights[2].light_control.set_dimmer(254)
    api(dim_command)
    time.sleep(DELAY_SECONDS)

for i in range(0, 255, 5):
    dim_command = lights[1].light_control.set_dimmer(i)
    api(dim_command)
    dim_command = lights[2].light_control.set_dimmer(i)
    api(dim_command)
    time.sleep(0.1)
