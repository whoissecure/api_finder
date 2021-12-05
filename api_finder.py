#!/usr/bin/python3

import json, requests, re, argparse, threading, time

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, help="File with URLs to inspect.")
parser.add_argument("-j", "--json", required=True, help="Regex file in json format")
parser.add_argument("-o", "--output", help="File to write the output.")
parser.add_argument("-t", "--threads", required=True, help="Number of threads to use")


args = parser.parse_args()

def find_it(url, data, output=False):
    try:
        r = requests.get(url)
        for service in data:
            regex = data.get(service).get("regex")
            keys = ""
            keys = re.findall(regex, r.text)
            keys = list(dict.fromkeys(keys))
            if keys != []:
                for key in keys:
                	found = 0
                	for number in data.get(service).get("links"):
                		if found == 0:
                			link = data.get(service).get("links").get(number).get("link").replace("APIKEYHERE", key)
                			error = data.get(service).get("links").get(number).get("error")
                			method = data.get(service).get("links").get(number).get("method")
                			if method == "get":
	                			c = requests.get(link)
	                		elif method == "post":
	                			post_data = data.get(service).get("links").get(number).get("post_data").replace("APIKEYHERE", key)
	                			c = requests.post(link, data=post_data)
                			if not error in c.text:
                				found = 1
                				msg = "[!] API Key found in " + url + " for " + service + ". Key: \"" + key + '" used in: ' + link.replace("APIKEYHERE", key)
                				print(msg)
                				if output:
               						output.write(msg)

    except:
    	pass

if args.file and args.json and args.threads:
	f = open(args.file, 'r+')
	if args.output:
		w = open(args.output, "w")
	else:
		w = False
	threads = []
	for i in range(int(args.threads)):
		for url in f.readlines():
			url = url.replace('\n', '')
			with open(args.json, "r") as j:
				data = json.loads(j.read())		
				t = threading.Thread(target=find_it, args=(url, data, w))
				threads.append(t)
				t.start()
	
	if args.output:
		if threading.active_count()==0:
			w.close()
	f.close()
else:
	print("Incorrect arguments. Use api_finder.py -h to see help menu.")
