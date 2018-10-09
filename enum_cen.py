
import argparse
import re
import sys
import json
import requests
import csv
import datetime
import os
import time

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
    )

API_URL = "https://www.censys.io/api/v1"
API_ID = ""
API_SECRET = ""
censysPrompt = "censys ~# "
domainPrompt = "enter domain ~# "

try:
    import censys.certificates
except ImportError:
    logging.info("\033[1;31m[!] Failed to import censys module. Run 'pip install censys'\033[1;m")
    sys.exit()

def validate_certificates():
	if not API_ID or not API_SECRET:
	        logging.info("\033[1;31m[!] API KEY or Secret for Censys not provided.\033[1;m" + "\nYou'll have to provide them in the script") 
        	sys.exit()

def encode(val):
		if(type(val) == float or type(val) == list or type(val) == int):
			return val
		else:
			return val.encode("utf8")

def __search__(domain,fun):
	validate_certificates(domain)
	params = {'query' : domain}

	res = requests.post(API_URL + "/search/" + fun, json = params, auth=(API_ID, API_SECRET))
	if res.status_code != 200:
    		print "error occurred: %s" % res.json()["error"]
    		sys.exit(1)

	payload = res.json()
	directory = "files/" + domain
	if not os.path.exists(directory):
		os.makedirs(directory)
	f= open("files/" + domain + "/" + fun + "_" + str(datetime.datetime.now())  + ".json","w+")
	f.write(json.dumps(payload))
	data = payload['results']
	
	c_data = open('files/' + domain + "/" + fun + "_" + str(datetime.datetime.now()) + '.csv', 'w')
	csvwriter = csv.writer(c_data)

	count = 0
	def encode(val):
		if(type(val) == float or type(val) == list or type(val) == int):
			return val
		else:
			return val.encode("utf8")
	for emp in data:
      		if count == 0:
             		header = emp.keys()
             		csvwriter.writerow(header)
             		count += 1
				
		value = [encode(val) for val in emp.values() ] 		
		csvwriter.writerow(value)
	c_data.close()


def clearScr():
	os.system('clear')

def get_domain():
	validate_certificates()
	domain = raw_input(domainPrompt)	
	return domain

if __name__ == '__main__':
	try: 
		if not os.path.exists("files/"):
			os.makedirs("files/")
		print ('''

		}--------------{+} Coded By m4cr0m4rv {+}--------------{

		}--------{+}  github.com/m4cr0m4rv/censys {+}--------{
		''')
		domain = get_domain()
		clearScr()
		print('''
		}--------------{+} Coded By m4cr0m4rv {+}--------------{

		}--------{+}  github.com/m4cr0m4rv/censys {+}--------{
		{1}--Websites
		{2}--IPv4
		{3}--Certificates
		''')
		choice = raw_input(censysPrompt)

		if choice == "1":
			__search__(domain,"websites")

		elif choice == "2":
			__search__(domain,"ipv4")
		elif choice == "2":
			__search__(domain,"certificates")
	except KeyboardInterrupt:
		print(" Finishing up...\n")
		time.sleep(0.25)
 	
