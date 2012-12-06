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
import os.path

ogBytes = 0
def get_url():
	print "what url would you like teh Lobster to visit?"
	url = raw_input()
	return url    	

# use Requests to grab status code of url. if the remote host does not respond the function will return a status_code of 0. This is to be expected and means we could not contact the remote host. if you want to know why that is you may be able to edit defaults.py of the Requests module to gather more informaiton. 
def check_one(url):
	headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0'}
	try:
		r = requests.get(url, headers=headers, allow_redirects=False)  
		filename, mode, noise, footprint, smart, fpok, bad, learn = cmd_options()		
		global ogBytes
		ogBytes	= r.headers['Content-Length']	
		if noise:
			print "we recieved a status code of: " + str(r.status_code)
			print bcolors.HEADER + "__.::Cookie Set By Server::.__" + bcolors.ENDC 
			print r.headers['set-cookie']
			# print bcolors.OKBLUE + "__.::HTML Data Returned::.__\n" + bcolors.ENDC 
			# print r.text
			print bcolors.OKBLUE + "\nHTTP Headers the server sent to us:" + bcolors.ENDC		
			print str(r.headers) + "\n"
		if there_is_no_binary(r) == True:
			sErr, db, err = sql_error_check(url, r.text) 
			if sErr == True and fpok != True:
				print  bcolors.FAIL + err + " :: Error detected on inital request. False positive potential high!" + bcolors.ENDC + "\nYou can set the --fpok switch to ignore this warning and test the URL(s) anyway.\n" + bcolors.HEADER + "URL not tested." + bcolors.ENDC 
				write_fp_html(url, r.text, db)
				return ("2000", "ghost", "variable") 
		return (r.status_code,r.headers['set-cookie'], r.headers)
	except (requests.ConnectionError, requests.Timeout):
		status = 0
		cookie = 2
                return (status,cookie,"goat")

# finally, lets throw some malformed http headers. 
def attack_loop(url, c, headers):
			filename, mode, noise, footprint, smart, fpok, bad, learn = cmd_options()
			if footprint:
				send_footprint(url, get_footprint_key("key.txt"), noise)
			test, smartTest = set_test_array(headers)		
			test_url(url, test, smartTest)			
			#Don't test cookies if the server didn't set any 
			if c != None: 
				a_9(url,c)
				a_12(url,c)
			
def set_test_array(h):
	filename, mode, noise, footprint, smart, fpok, bad, learn = cmd_options()	
	test = {}
	test[0] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'pyL0bster': ';'}
	test[1] = {'User-Agent': '\''}	
	test[2] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Host': '\''}
	test[3] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'From': '\''}
	test[4] = {'User-Agent': '\"'}
	test[5] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'X-Forwarded-For': '\''}
	test[6] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Referer': '\''}
	test[7] = {'User-Agent': ';'}
	test[8] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Host': ';'}
	test[10] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'X-Forwarded-For': ';'}
	test[11] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Referer': ';'}
	test[13] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', '%00': '%00'}
	test[14] = {'User-Agent': '%00\''}
	test[15] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Host': '%00\''}	
	test[16] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'X-Forwarded-For': '%00\''}
	test[17] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'Referer': '%00\''}
			
	if smart:
		noTest = ['user-agent','x-forwarded-for','referer', 'host', 'from', 'etag', 'accept-ranges', 'age', 'accept-encoding', 'vary', 'last-modified', 'date', 'content-type', 'set-cookie','transfer-encoding', 'accept','accept-language','accept-datetime','cache-control', 'allow', 'content-location', 'expires', 'connection','content-length','content-encoding','pragma']
		smartTest = {}
		c = 0
		for z in h:
			if z.lower() not in noTest:
				smartTest[c] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', z : '\''}
				c += 1
				smartTest[c] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', z : ';'}
				c += 1
	else:
		smartTest = None	

	return (test, smartTest)

def test_url(url, test, smartTest):
	filename, mode, noise, footprint, smart, fpok, bad, learn = cmd_options()		
	if noise:	
		print bcolors.HEADER + "Full Array of Requests to be Sent" + bcolors.ENDC
		print test
		print smartTest
	for i in test:
		at = i
		gtg = 0
		if i != 9 and i !=12:		
			try: 
   				a = requests.get(url, headers=test[i], allow_redirects=False)
				if noise:
					print bcolors.OKBLUE + str(test[i]) + bcolors.ENDC				
				gtg = 1
				if gtg == 1:
					base_attack(a,at,url)
			except (requests.ConnectionError, requests.Timeout):
				attack_fail(url)
	if smart:	
		for t in smartTest:
			at = "s" + str(t)
			gtg = 0
			try: 
   				a = requests.get(url, headers=smartTest[t], allow_redirects=False)

				if noise:
					print bcolors.OKBLUE + str(smartTest[t]) + bcolors.ENDC				
				gtg = 1
				if gtg == 1:	
					base_attack(a,at,url)
			except (requests.ConnectionError, requests.Timeout):
				smart_fail(url)   	
	

#the cookie attack. Premise is simple, send SQLi (or other bogus cookies) back to webserver, parse the returned HTML (sql_error_check) to see if there is an error thrown from the server.
def a_9(url,c):	
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
	headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0'}
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

def a_12(url,c):	
	gtg = 0
	at = 12	
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
	headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0'}
        #lets create our cookie dict/array and add a value for each cookie/key
        cookies = {}
	for name in clist:
		cookies[name] = ';' 
	#ok, time to send our malicious cookies back to the server. 
	try: 
   		a = requests.get(url, cookies=cookies, headers=headers, allow_redirects=False)
		gtg = 1
	except (requests.ConnectionError, requests.Timeout):
		attack_fail(url)  	
	
	if gtg == 1:
		base_attack(a,at,url)


def send_footprint(url, key, noise):
        
	fp = {}
	fp[0] = {'User-Agent': key}
        fp[1] = {'Referer': key}
	# fp[2] = {'Host': key}
	# fp[3] = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0', 'X-Forwarded-For': key}
	try:	
        	for i in fp:   		
			a = requests.get(url, headers=fp[i] , allow_redirects=False)
			if noise:
				print "Footprint: " + str(fp[i]) + " Sent!"
	except (requests.ConnectionError, requests.Timeout):
		print 'Fuck! Footprint fail:' + url
			
	
def get_footprint_key(filename):
	with open(filename) as f:
		return f.read()	


# def attack_x(url):
#	headers = {'User-Agent': '<script>window.location = "http://xxxx"</script>'}

def load_sauce():
	sauce = {}
	sauce[0] = "you\shave\san\serror"
	sauce[1] = "Warning.*supplied\sargument\sis\snot\sa\svalid\sMySQL\sresult"
	sauce[2] = "Warning.*mysql_.*\(\)"
	sauce[4] = "microsoft\sOLE\sDB\sProvider\sfor\sODBC\sDriver"
	sauce[5] = "Microsoft\sOLE\sDB\sProvider\sfor\sSQL\sServer"
	sauce[6] = "\[Microsoft\]\[ODBC Microsoft Access Driver\] Syntax error"
	sauce[7] = "Microsoft OLE DB Provider for ODBC Drivers.*\[Microsoft\]\[ODBC SQL Server Driver\]"
	sauce[8] = "Microsoft OLE DB Provider for ODBC Drivers.*\[Microsoft\]\[ODBC Access Driver\]"
	sauce[9] = "Microsoft JET Database Engine"
	sauce[10] = "ADODB.Command.*error"
	sauce[11] = "Microsoft VBScript runtime"
	sauce[12] = "Type mismatch | VBScript / ASP error"
	sauce[13] = "Server Error.*System\.Data\.OleDb\.OleDbException"
	sauce[14] = ":\squoted\sstring\snot\sproperly\sterminated"
	sauce[15] = "ORA-[0-9][0-9][0-9][0-9]"
	sauce[16] = "Invalid SQL statement or JDBC"
	sauce[17] = "org\.apache\.jasper\.JasperException"
	sauce[18] = "Warning.*failed to open stream"
	sauce[19] = "Fatal Error.*on line"
	sauce[20] = "Fatal Error.*at line"	
	sauce[21] = "\[Microsoft\]\[SQL\sNative\sClient\]\[SQL\sServer\]"
	sauce[22] = "An\sunexpected\serror\shas\soccured!.*MySQL\serror!"
	sauce[23] = "\[Microsoft\]\[ODBC\sDriver\sManager\]\sDriver"
	sauce[24] = "\[Microsoft\]\[ODBC\sSQL\sServer\sDriver\]\[SQL\sServer\]"
	sauce[25] = "\[Microsoft\]\[SQL\sServer\sNative\sClient\s10\.0\]Named\sPipes\sProvider"
	return sauce
		
def sql_error_check(url, html):
	
	sauce = {} 
	sauce = load_sauce()
	
	for i in sauce:
		objMatch = re.search(sauce[i], html, re.M|re.I)
		if objMatch:
			return(True, i, sauce[i])
	no = None
	no1 = None 
	return (False, no, no1)

	
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
	params = a.headers
	filename, mode, noise, footprint, smart, fpok, bad, learn = cmd_options()
	#lets try to make sure its not a binary file of some sort
	if there_is_no_binary(a) == True:
        	try:
			# print a.text			
			if a.text != None:
        	        	sErr, db, err = sql_error_check(url, a.text)
                except():        	
			print a.headers['content-type']
			print "can't be written as text" 
		if mode == "ES" or filename:
			write_to_ES(url,a.status_code,at,params,sErr,db)
		else:                
			std_out(a,at,url,sErr,err)
		if sErr == True:
                	write_error_html(url, a.text, at, db)
		if bad == True and sErr == False and a.headers['Content-Length'] and ogBytes:
			find_byte_anomalies(a,at,url, noise)
		if sErr == False and a.status_code == 500:
			write_500_html(url, a.text, at)

def find_byte_anomalies(a, at, url, noise):
		tbv = a.headers['content-Length']
		if noise:
			print "Legit Bytes: " + str(ogBytes) 
			print "Attack: "  + str(at) + " Bytes: " + tbv 
		highB = int(ogBytes) + 150
		lowB = int(ogBytes) - 150
		if int(tbv) >= int(highB) or int(tbv) <= int(lowB):
			write_byte_anomaly(url, a.text, at, ogBytes, tbv, a.status_code)
	
def there_is_no_binary(a):
	if a.headers['content-type'] != 'image/gif' and a.headers['content-type'] != 'image/png' and a.headers['content-type'] != 'image/jpg' and a.headers['content-type'] != 'application/pdf' and a.headers['content-type'] != 'image/jpeg':
		return True 
	

def std_out(a,at,url, sErr, err):
	# print a.status_code
	if sErr == True:
        	print "Attack Number:", at, " ", bcolors.FAIL + "Succeeded! Error Caught by Regex: " + bcolors.ENDC + "\"" + str(err) + "\"" 
		print bcolors.OKBLUE + "\n..o0(nowHack)0o..\n" + bcolors.ENDC

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


#write log Files 

#Check_one returned "0". Could be that URL is down, could be static of the internets. 
def bad_url(url):
	f = open('bad_url.log','a')
	f.writelines(url + "\n")
	f.close()

#we detected a SQL error on the inital request. While this site still may be vunerable to error base SQLi in the header fields, it should be manually tested because our detection methodology will likely give a False Postive here. 
 
def false_positive_prone(url):
	f = open('false_postive.log','a')
	f.writelines(url + "\n")
	f.close()

def attack_fail(url):
	f = open('attackFail.log','a')
	f.writelines(url + "\n")
	f.close()

def smart_fail(url):
        f = open('smartFail.log','a')
        f.writelines(url + "\n")
        f.close()

def error_500(url):
	f = open('error_500.log','a')
	f.writelines(url + '\n')
	f.close()

def write_logfile(count,url,logfile):
	f = open(str(logfile),'a')
	f.writelines(count + "  " + url+ '\n')
	f.close() 

def check_1_fail(url):
	f = open('write_fail.log','a')
	f.writelines(url + '\n')
	f.close()

# Write HTML Def's
# here we save off the HTML in which an error code has been detected
def write_error_html(url, html, at, db):
	prefix = 'http://' 
	if url.startswith(prefix): 
		url = url[len(prefix):] 
	html = html.encode('ascii', 'replace')
	fname = ("./gold/" + url + '_' + str(at) + "_" + str(db))
	ensure_dir(fname)
	f = open(fname,'w+')
	f.write(html + '\n')
	f.close()

#IF we detect error on first (legit) request then its likely we are going to FP. we will write url to log (for later processing) and also write HTML
def write_fp_html(url, html, err):
	prefix = 'http://' 
	if url.startswith(prefix): 
		url = url[len(prefix):] 
	html = html.encode('ascii', 'replace')
	fname = ("./fp/" + url + '_' + str(err))
	ensure_dir(fname)
	f = open(fname,'w+')
	f.write(html + '\n')
	f.close()

#This is part our learning phase and is on by defualt right now but should get a switch someday. If we made it through check_one with out an Error continued on to base_attack and didn't get a regEx error match but DID get a 500. we save off the HTML to see what the error is and see if it makes sense to create a regEx for it. 
def write_500_html(url, html, at):
	prefix = 'http://' 
	if url.startswith(prefix): 
		url = url[len(prefix):] 
	html = html.encode('ascii', 'replace')
	fname = ("./500/" + url + '_' + str(at))
	ensure_dir(fname)
	f = open(fname,'w+')
	f.write(html + '\n')
	f.close()

def write_byte_anomaly(url, html, at, o, a, s):
	prefix = 'http://' 
	if url.startswith(prefix): 
		url = url[len(prefix):] 
	html = html.encode('ascii', 'replace')
	fname = ("./byte_anom/" + url + '_' + str(at) + "_" + str(o) + "_" + str(a) + "_" + "sc" + str(s))
	ensure_dir(fname)
	f = open(fname,'w+')
	f.write(html + '\n')
	f.close()

# check to see if dir exists, if not create it
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


#here we go
def begin(url):
	
	statusCode, cookie, headers = check_one(url)	
	
	if statusCode == 0:
		bad_url(url)
	
	elif statusCode == "2000":
			false_positive_prone(url)

	elif statusCode == 500:
			error_500(url)
	
	else:
		attack_loop(url,cookie, headers)
    
#main yo
def main():
	filename, Mode , noise, footprint, smart, fpok, bad, learn = cmd_options() 
	
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

def cmd_options():
	parser = OptionParser()
	parser.add_option("-f", dest="filename", help="file name to read url's from", metavar="url_list.txt")
	parser.add_option("-M", dest="mode", help="set the output mode, defualt is stdout, options include ES for ElasticSearch and SQLite for SQLite", default="STDout") 
	parser.add_option("--fpok", action="store_true", help="If we detect an error on our inital (non-malicous) request it's very likely that you will get a false positive for the given URL. by defualt, we will not test URL's with a high FP potential (better if running pyLobster against a large list of URL's). If you would like to test the URL anyway set this switch")
	parser.add_option("-v", action="store_true", help="Show verbose output.")
	parser.add_option("-g", action="store_true", help="Enable footprint mode. Please see manual (non-existant) for additional info on what is needed here and what this feature does.")
	parser.add_option("-l", action="store_true", help="Enable learning mode. If we don't hit regEx error but do get 500 then lets save the HTML for later review.")
	parser.add_option("-s", action="store_true", help="Enable smart mode. This will look at what Headers the webserver is using and test those")
	parser.add_option("--bad", action="store_true", help="Enable Byte Anomaly Detection.")
	(options, args) = parser.parse_args()
	return (options.filename, options.mode, options.v, options.g, options.s, options.fpok, options.bad, options.l)


# Ready Begin
if __name__ == "__main__":
	main()

    

	
