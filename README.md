--pyLobster--
=============
Used to audit web servers and applications in how they process HTTP Headers. It sends a series of GET requests with custom crafted HTML Headers and then looks for anomalies (regex's for known errors) in the response data. Tests can reveal SQL Injection vunerabilites and various other issues that are of interest.   

****Disclaimer****
Please make sure that you have the necessary permissions from sites you intend to audit before running this tool. 
 
--Features--
============
1. Basic Error based SQLi tests for:
	User-Agent
	X-Forwarded-For
	Host
	Referer
	Cookies (all fields)

Easy to add tests for any other fields.   

2. Output to Termial, SQLite, or JSON->ElasticSearch

--Usage--
==========
Show help file:

python pyLobster.py -h 

Run against a single URL:\n\n

python pyLobster.py
what url would you like teh Lobster to visit?
http://zacharywolff.com


If you want to feed it a list of URL's (from burp export or something)

  python pyLobster.py -f urlList.txt

check sampleList.txt for expected format


--Dependencies--
================
Tested on Python v 2.7.3 (hopefully works on 3+ too) 

Python Requests Library
https://github.com/kennethreitz/requests

  apt-get install python-pip
  pip install requests

Consider turning requests safe_mode on if you are having issues:

  nano /usr/local/lib/python2.7/dist-packages/requests/defaults.py



--Output Mode--
===============
can be set with the -m swtich

1. defualt: Terminal output

2. SQLite (needs work) 
If you are using SQLite to store your results data you will need to first create a SQLitedb
  sqlite3 results.db
  python create_sqlite3.py

3. JSON--> Elasticsearch 

-m ES 

This output mode is working however you will need to have an ElasticSearc instance ready to recieve POSTed JSON data. 


To Do
==========

1. Detect custom HTTP Headers and reply to those as well

2. Add switch for header test mode: --htm 
all -- (every standard header field) 
minimal -- (typical dynamic header fields) will be defualt 
smart -- (see #4, check what headers webserver sets and attack those)
custom -- (choose which header field to test)

3. Add fuzzing defs 
4. Add basic SQLi union tests










