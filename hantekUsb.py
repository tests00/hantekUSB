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
MAXPACKET = 0x2000

scope = usb.core.find(idVendor=VENDOR_HAN, idProduct=PRODUCT_DSO)

if scope is None:
    raise ValueError('Scope not found')

usb.util.dispose_resources(scope)

#scope.reset()
if scope.is_kernel_driver_active(0) == True:
        scope.detach_kernel_driver(0)
	
#scope.set_configuration()

for cfg in scope:
	sys.stdout.write('Configuration: ' + hex(cfg.bConfigurationValue) + '\n')
	for intf in cfg:
		sys.stdout.write('\tInterface: ' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n')
        for ep in intf:
		sys.stdout.write('\t\tEndpoint: ' + hex(ep.bEndpointAddress) + '\n')
	sys.stdout.write('\n------------------------\n\n')

usb.util.claim_interface(scope, 0)

# Command reference - https://elinux.org/Das_Oszi_Protocol
# Read Commands
DSOSETTINGS = 		"\x53\x02\x00\x01\x56"
READCH1 = 		"\x53\x04\x00\x02\x01\x00\x5a"

# Change Commands
CH1VoltDivLEFT = 	"\x53\x04\x00\x13\x1c\x01\x87"	

# Debug Commands
LIST =			"\x43\x04\x00\x11\x6c\x73\x37"

def getSettings():
	while True:
		try:
			scope.write(INPOINT, DSOSETTINGS)
			sys.stdout.write("Settings\n")
			data = scope.read(OUTPOINT, MAXPACKET)
			if len(data) > 0:
				data = [int(x) for x in data]
				
			if data[0] == 0x53 and data[3] == 0x81: # Settings response
				length = str(data[2]) + str(data[1]).replace("0x", "")
				sys.stdout.write('Packet length: 0x' + str(length) + '\n')
				
				# None of this is certain, all very rough
				sys.stdout.write('Settings data: ' + str(data[4:-1]) + '\n')

				sys.stdout.write('\tCH1 Enabled: ' + str(data[4]) + '\n')
				sys.stdout.write('\tCH1 Volt/Div: ' + str(data[5]) + '\n')
				sys.stdout.write('\tCH1 Coupling: ' + str(data[6]) + '\n')
				sys.stdout.write('\tCH1 20MHz BW Filter: ' + str(data[7]) + '\n')
				sys.stdout.write('\tCH1 Volt/Div Tuning Type: ' + str(data[8]) + '\n')
				sys.stdout.write('\tCH1 Probe Type: ' + str(data[9]) + '\n')
				sys.stdout.write('\tCH1 Phase: ' + str(data[10]) + '\n')
				sys.stdout.write('\tCH1 Fine Volt/Div: ' + str(data[11]) + '\n')
				sys.stdout.write('\tCH1 Vertical Position: ' + str(data[12:14]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tCH2 Enabled: ' + str(data[14]) + '\n')
				sys.stdout.write('\tCH2 Volt/Div: ' + str(data[15]) + '\n')
				sys.stdout.write('\tCH2 Coupling: ' + str(data[16]) + '\n')
				sys.stdout.write('\tCH2 20MHz BW Filter: ' + str(data[17]) + '\n')
				sys.stdout.write('\tCH2 Volt/Div Tuning Type: ' + str(data[18]) + '\n')
				sys.stdout.write('\tCH2 Probe Type: ' + str(data[19]) + '\n')
				sys.stdout.write('\tCH2 Phase: ' + str(data[20]) + '\n')
				sys.stdout.write('\tCH2 Fine Volt/Div: ' + str(data[21]) + '\n')
				sys.stdout.write('\tCH2 Vertical Position: ' + str(data[22:24]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tTrigger Status: ' + str(data[25]) + '\n')
				sys.stdout.write('\tTrigger Type: ' + str(data[26]) + '\n')
				sys.stdout.write('\tTrigger Source: ' + str(data[27]) + '\n')
				sys.stdout.write('\tTrigger Mode: ' + str(data[28]) + '\n')
				sys.stdout.write('\tCoupling Mode: ' + str(data[29]) + '\n')
				sys.stdout.write('\tTrigger Level Position: ' + str(data[30:32]) + '\n')
				sys.stdout.write('\tTrigger Toggle Frequency: ' + str(data[32:40]) + '\n')
				sys.stdout.write('\tMin Trigger Holdoff: ' + str(data[40:48]) + '\n')
				sys.stdout.write('\tMax Trigger Holdoff: ' + str(data[48:56]) + '\n')
				sys.stdout.write('\tTrigger Holdoff: ' + str(data[56:64]) + '\n')
				sys.stdout.write('\tMisc Triggers: ' + str(data[64:103]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tMain Timebase: ' + str(data[103]) + '\n')
				sys.stdout.write('\tWindow Timebase: ' + str(data[104]) + '\n')
				sys.stdout.write('\tWindow State: ' + str(data[105]) + '\n')
				sys.stdout.write('\tTrigger Delay: ' + str(data[106:114]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tMaths Display: ' + str(data[114]) + '\n')
				sys.stdout.write('\tMaths Mode: ' + str(data[115]) + '\n')
				sys.stdout.write('\tFFT Source: ' + str(data[116]) + '\n')
				sys.stdout.write('\tFFT DB Scale: ' + str(data[117]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tDisplay Type: ' + str(data[118]) + '\n')
				sys.stdout.write('\tPersistency: ' + str(data[119]) + '\n')
				sys.stdout.write('\tDSO Mode: ' + str(data[120]) + '\n')
				sys.stdout.write('\tContrast: ' + str(data[121]) + '\n')
				sys.stdout.write('\tMax Contrast: ' + str(data[122]) + '\n')
				sys.stdout.write('\tGrid Type: ' + str(data[123]) + '\n')
				sys.stdout.write('\tGrid Brightness: ' + str(data[124]) + '\n')
				sys.stdout.write('\tMax Grid Brightness: ' + str(data[125]) + '\n')
				sys.stdout.write('\n')

				sys.stdout.write('\tACQ Mode: ' + str(data[126]) + '\n')
				sys.stdout.write('\tAVG ACQ Count: ' + str(data[127]) + '\n')
				sys.stdout.write('\tACQ Type: ' + str(data[128]) + '\n')
				sys.stdout.write('\tMemory Depth: ' + str(data[129]) + '\n')
				# Also unfinished

			#sys.stdout.write("Response: " + str(data) + "\n")
			
			#return data
			else:
				sys.stdout.write('None')
			break
		except usb.core.USBError as e:
		    data = None
		    if e.args == ('Operation timed out',):
			sys.stdout.write('No data.\n')
			continue

def oneShot(COMMAND):
	while True:
		try:
			scope.write(INPOINT, COMMAND)
			data = scope.read(OUTPOINT, MAXPACKET)
			if len(data) == 0:
				continue
			else:
				data = [hex(x) for x in data]
				sys.stdout.write("Response: " + str(data) + "\n")
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
			scope.write(INPOINT, CHANNEL)
			#sys.stdout.write("Written\n")
			data = scope.read(OUTPOINT,MAXPACKET)
			if len(data) > 0:
				data = [int(x) for x in data]

			if data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x00: # Initial sample length packet
				length = str(data[2]) + str(data[1]).replace("0x", "")
				#sys.stdout.write('Packet length: 0x' + str(length) + '\n')
				sys.stdout.write('Data length: ' + str(data[5:8]) + '\n')
			elif data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x01: # Channel number and initial sample data
				length = str(data[2]) + str(data[1]).replace("0x", "")
				sys.stdout.write('Packet length: 0x' + str(length) + '\n')
				length = int(length)
				print length
				if data[5] == 0x00: # Byte 5 is the Channel number packet
					sys.stdout.write('Channel 1\n')
				if data[5] == 0x01:
					sys.stdout.write('Channel 2\n')
				sys.stdout.write('Data: ' + str(data[6:-1]) + '\n')
				
				sampleCount = len(data[6:-1])
				'''
				plt.axis([0, sampleCount, 0, 255])
				plt.ion()
	
				for i in range(0, sampleCount):
					plt.scatter(i, data[6+i])
				'''
				sys.stdout.write('Number datapoints: ' + str(sampleCount) + '\n')
			elif data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x02: # Subcommand 0x02 means end of data
				sys.stdout.write('Samaple data end.\n')
			elif data[0] == 0x53 and data[3] == 0x82 and data[4] == 0x03: # Subcommand 0x03 means error
				sys.stdout.write('Error. Is the channel in STOP mode?\n')
			else: # Just pure data packet
				print str(data)
		except usb.core.USBError as e:
		    data = None
		    if e.args == ('Operation timed out',):
			sys.stdout.write('No data.\n')
		        continue

def shellCommand(cmd):
	while True:
		try:
			cmdLen = len(cmd) + 2 # add on checksum and command bytes
			cmdLen = chr(cmdLen)
			COMMAND = bytearray("\x43")
			COMMAND.extend(cmdLen)
			COMMAND.extend("\x00\x11" + cmd)
			#print COMMAND
			checkSum = str(hex(sum(bytearray(COMMAND))))
			checkSum = checkSum[-2:]
			checkSum = int(checkSum, 16)
			#print checkSum
			COMMAND.extend(chr(checkSum))
			#print COMMAND
			bytes = bytearray(COMMAND)
			#print bytes
			bytes = [hex(x) for x in bytes]
			#print bytes
			scope.write(INPOINT, str(COMMAND))
			data = scope.read(OUTPOINT, MAXPACKET)
			if len(data) == 0:
				continue
			else:
				data = ''.join([chr(x) for x in data])
				sys.stdout.write("Response: " + str(data) + "\n")
				return data
				break
		except usb.core.USBError as e:
		    data = None
		    if e.args == ('Operation timed out',):
			sys.stdout.write('No data.\n')
			continue

#oneShot(LIST)
shellCommand('ls -al')
#getSettings()
#streamSamples(READCH1)
#usb.util.release_interface(scope, 0)
usb.util.dispose_resources(scope)


