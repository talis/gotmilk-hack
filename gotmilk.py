#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Author : Russ Hill (based on code by Matt Hawkins)
# Date   : 28/05/2014
#
# Ref :
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os, os.path
import requests
import ConfigParser
import urllib2
import subprocess


config = ConfigParser.ConfigParser()
config.read([os.path.expanduser("~/gotmilk/.gotmilk"), '/etc/gotmilk'])

AUTH_TOKEN = config.get('HipChat', 'token')
HIPCHAT_ROOM_ID = config.get('HipChat', 'roomid')
DELAY = config.getfloat('GotMilk', 'delay')

def internet_on():
	try:
		urllib2.urlopen('https://api.hipchat.com', timeout=1)
		return True
	except urllib2.URLError as err:
		return False

def get_ip():
	cmd = "ifconfig wlan0 | awk '/inet addr/ { print $2 } '"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	process.wait()
	return process.stdout.read().split(':')[1]

def send_message(message):
	# send a message via HipChat
	hipchat_url = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=" + AUTH_TOKEN

	payload = {
		'room_id':HIPCHAT_ROOM_ID,
		'from':'Milkmaid',
		'color':'red',
		'notify':'true',
		'message':message
	}

	r = requests.post(hipchat_url, data=payload)

def wait_for_access():
	while (internet_on() == False):
		time.sleep(2)
	ip_address = get_ip()
	send_message('Milkmaid up and monitoring on '+ ip_address)

wait_for_access() 

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places. 
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  
# Define sensor channels
resistor_channel = 0

# Define previous resistor level
previous_resistor_level = 0
nothing_on_pad_count = 0

while True:
	level_message = "Monitoring..."

	# Read the resistor data
	resistor_level = ReadChannel(resistor_channel)
	resistor_volts = ConvertVolts(resistor_level,2)

	if resistor_level != previous_resistor_level: 
		if resistor_level > 900:
			# Nothing on the pad
			level_message = "Nothing on the pad"
			nothing_on_pad_count += 1
			if nothing_on_pad_count == 5:
				level_message = "Milk has all gone (or been left out of the fridge!)"
				nothing_on_pad_count = 0
		elif 650 <= resistor_level <= 900:
 			# Milk running low
			level_message = "Milk running low - please buy more"
			nothing_on_pad_count = 0
		elif 400 <= resistor_level <= 650:
			# Milk is healthy
			level_message = "Milk level currently okay"
			nothing_on_pad_count = 0
		else:
			# Loads of milk
			level_message = "Lots of milk!"
			nothing_on_pad_count = 0

	# Print out results
	print "--------------------------------------------"  
	print("Pressure : {} ({}V)".format(resistor_level,resistor_volts))
	print level_message  

	previous_resistor_level = resistor_level

	# Wait before repeating loop
	time.sleep(DELAY)
 

