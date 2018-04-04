#!/usr/bin/env python3

##################################################################################
## License
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
##################################################################################


import samsungctl
import time
import logging
import argparse
import signal
import os
import sys


log = None

VERSION = "0.0.3"
AUTHOR="SW Engineer: Garzola Marco"

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("-d","--debug", action="store_true", default= False, help="add verbosity")
parser.add_argument("-s","--port", nargs = 1, metavar =("port"), help="port")
group.add_argument("-c","--channel", metavar =("channel"), help="channel")
group.add_argument("-k","--key", metavar =("key remote"), help="remote key eg. 'KEY_MUTE'")
group.add_argument("-m","--mute", metavar =("mute"), help="mute")
parser.add_argument("ip", help="host ip")
parser.add_argument("-l","--log", nargs = 1, metavar =("log File"), default= False, help=" path file to save log")
parser.add_argument('-v', '--version', action='version', version= VERSION  + "\n" +  AUTHOR)

def handler(signum, frame):
    print('\r\nYou pressed Ctrl+C! Game Over...')
    sys.exit(0)


config = {
    "name": "samsungcli",
    "description": "command line interface 4 samsung TV",
    "id": "tv",
    "host":  "",
    "port": 55000,
    "method": "legacy",
    "timeout": 2,
}

def digit2key(n) :
    print(n)
    if n == "0" :
       return "KEY_0"
    if n == "1" :
       return "KEY_1"
    if n == "2" :
       return "KEY_2"
    if n == "3" :
       return "KEY_3"
    if n == "4" :
       return "KEY_4"
    if n == "5" :
       return "KEY_5"
    if n == "6" :
       return "KEY_6"
    if n == "7" :
       return "KEY_7"
    if n == "8" :
       return "KEY_8"
    if n == "9" :
       return "KEY_9"


def changeChannel(remote , number):
  
   keyNumber = [ digit2key(x) for x in str(number) ]

   log.debug( str(keyNumber) )
   for k in keyNumber:
      remote.control(k)
      time.sleep(0.2)
   remote.control("KEY_ENTER")

if __name__=='__main__':

	log = logging.getLogger()
	signal.signal(signal.SIGINT, handler)        
	args = parser.parse_args()

	if args.debug:
		log_level = logging.DEBUG 
	else:
		log_level = logging.INFO

	if args.log:    
		logging.basicConfig( filename=args.log[0],
				filemode='w',
				format='%(asctime)s,%(levelname)s %(message)s',
				datefmt='%H:%M:%S',
				level=log_level)    
	else:
		logging.basicConfig(format='%(asctime)s,%(levelname)s %(message)s',
				datefmt='%H:%M:%S',
				level=log_level)  
	if args.port:
		config.update({"port" : args.port})
	if args.ip:
		config.update({"host" : args.ip})

	log.debug(config)

	remote = None
	try:
	      remote = samsungctl.Remote(config)
	except:
	      log.error("Connection Problem")
	      sys.exit(1)	

	if args.channel:		
		log.debug("Changing Channel to {}".format(args.channel) )
		changeChannel(remote , args.channel)
	if args.mute:
		log.debug("Muting TV volume")
		remote.control("KEY_MUTE")
	if args.key:
		log.debug("sending KEY {}".format(str(args.key)))
		remote.control(str(args.key))


	sys.exit(0)  
