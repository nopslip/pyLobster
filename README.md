pyLobster
=========

Used to audit HTTP Header processing.  Currently it will send basic SQLi test characters to pre-configured HTTP Header fields. It will parse the returned HTML and alert on known errors. 
 

Dependencies
============
Tested on Python v 2.7.3

Python Requests Library
https://github.com/kennethreitz/requests

  apt-get install python-pip
  pip install requests

Consider turning requests safe_mode on if you are having issues:

  nano /usr/local/lib/python2.7/dist-packages/requests/defaults.py

Advanced tuning can be done on the pool threads as well if you like. This will only be necessary if you are running the script multiple times at once. 

Output Mode
===========
1. Terminal output

2. SQLite 
If you are using SQLite to store your results data you will need to first create a SQLitedb
  sqlite3 results.db
  python create_sqlite3.py

3. JSON-->Elasticsearch 
If Elasticsearch, you can uncomment write_to_ES line in def base_attack. You will need to have an Elasticsearch index set up and running for this to work. 

==========

Show help file:
  python pyLobster.py -h 

Run against a single URL (Lobster will prompt for URL, please be sure to use http:// before URL for now)

  python pyLobster.py

If you want to feed it a list of URL's (from burp export or something)

  python pyLobster.py -f urlList.txt

This list should be formatted like this:

http://google.com
http://yahoo.com
http://ymh.com 

and so on. 

To Do

==========

1. Set AGRV switch for output mode, ie, ElasticSearch, SQLite, Flat File or STDOUT. Switch added but not yet configured to move between types (12/1/2012). 

2. Update SQL error Regexs (completed 12/1/2012) 

3. Switch to follow redirects

4. Detect custom HTTP Headers and reply to those as well

5. Add switch for header test mode: -H 
all -- (every standard header field) 
minimal -- (typical dynamic header fields) will be defualt 
smart -- (see #4, check what headers webserver sets and attack those)
custom -- (choose which header field to test)

6. Beyond SQLi: Add fuzzing capabilities 
7. Add basic SQLi union tests










