pyLobster
=========

Used to audit dynamic HTTP Header processing. It is currently designed to use basic SQLi test params but new header request values can be added easily. 
 

Dependencies
============
Tested on Python v 2.7.3

Python Requests Library

  apt-get install python-pip
  pip install requests

Consider turning requests safe_mode on if you are having issues
  nano /usr/local/lib/python2.7/dist-packages/requests/defaults.py
advanced tuning can be done on the pool threads as well if you like

If you are using SQLite to store your results data you will need to first create a SQLitedb
  sqlite3 results.db
  python create_sqlite3.py

If Elasticsearch you can uncomment write_to_ES line in base_attack. I will be adding switches for these options in the future. You will need to have an Elasticsearch index set up and running for this to work. more on that at some point. 

Usagehttps://github.com/kennethreitz/requests
==========

Show help file:
  python pyLobster.py -h 

Run against a single URL (if will prompt for URL, please be sure to use http:// before URL for now)
  python pyLobster.py

if you want to feed it a list of URL's (from burp export or something)
  python pyLobster.py -f urlList.txt



Currently it can POST JSON results to Elasticsearch or write desired results to text files. however, there is no switch to move between these options and it has to be done manually in the code. I will fix this very soon. 

To Do

1. Set AGRV switch for output mode, ie, ElasticSearch, SQLite, Flat File or STDOUT

2. Update SQL error Regexs 

3. switch to follow redirects



