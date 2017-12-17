#!/usr/bin/env python2

import usb.core
import usb.util
import sys

import binascii
import numpy as np
from matplotlib import pyplot as plt


VENDOR_HAN = 0x049f
PRODUCT_DSO = 0x505a

INPOINT = 0x2
OUTPOINT = 0x81
MAXPACKET = 0x200

dev = usb.core.find(idVendor=VENDOR_HAN, idProduct=PRODUCT_DSO)

if dev is None:
    raise ValueError('Device not found')

#dev.reset()
if dev.is_kernel_driver_active(0) == True:
        dev.detach_kernel_driver(0)
dev.set_configuration()

for cfg in dev:
	sys.stdout.write('Configuration: ' + hex(cfg.bConfigurationValue) + '\n')
	for intf in cfg:
		sys.stdout.write('\tInterface: ' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n')
        for ep in intf:
		sys.stdout.write('\t\tEndpoint: ' + hex(ep.bEndpointAddress) + '\n')
	sys.stdout.write('\n------------------------\n\n')

usb.util.claim_interface(dev, 0)

# Command reference - https://elinux.org/Das_Oszi_Protocol
# Read Commands
DSOSETTINGS = 		"\x53\x02\x00\x01\x56"
READCH1 = 		"\x53\x04\x00\x02\x01\x00\x5a"

# Change Commands
CH1VoltDivLEFT = 	"\x53\x04\x00\x13\x1c\x01\x87"

def genericOneShot(COMMAND):
	while True:
		try:
			dev.write(INPOINT, DSOSETTINGS)
			sys.stdout.write("Settings:\n")
			data = dev.read(OUTPOINT, MAXPACKET)
			if len(data) == 0:
				continue
			else:
				#data = ''.join([hex(x) for x in data])
				print data
				return data
				break
		except usb.core.USBError as e:
		    data = None
		    if e.args == ('Operation timed out',):
			sys.stdout.write('No data.\n')
			continue

def streamSamples(CHANNEL):
	while True:
		try:
			dev.write(INPOINT, CHANNEL)
			sys.stdout.write("Written\n")
			data = dev.read(OUTPOINT,MAXPACKET)
			if len(data) > 0:
				data = [int(x) for x in data]
			#data = ''.join([binascii.hexlify(chr(x)) for x in data])
			print data[0]
			if data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x00:
				length = str(data[2]) + str(data[1]).replace("0x", "")
				sys.stdout.write('Packet length: 0x' + str(length) + '\n')
				sys.stdout.write('Data length: ' + str(data[5:8]) + '\n')
			if data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x01:
				length = str(data[2]) + str(data[1]).replace("0x", "")
				sys.stdout.write('Packet length: 0x' + str(length) + '\n')
				length = int(length)
				print length
				if data[5] == 0x00:
					sys.stdout.write('Channel 1\n')
				if data[5] == 0x01:
					sys.stdout.write('Channel 2\n')

				sys.stdout.write('Data: ' + str(data[6:]) + '\n')
			print [hex(x) for x in data]
		except usb.core.USBError as e:
		    data = None
		    if e.args == ('Operation timed out',):
			sys.stdout.write('No data.\n')
		        continue



#genericOneShot(DSOSETTINGS)
streamSamples(READCH1)
#usb.util.release_interface(dev, 0)
usb.util.dispose_resources(dev)


