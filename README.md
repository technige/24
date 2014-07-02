# Neo4j Python 24 Hackathon

This repository contains a 24 data set in Geoff format for use at a [Neo4j Python Hackathon](http://www.meetup.com/graphdb-london/events/191374552/).

## Installing Load2neo

We'll be using the [Load2neo](http://nigelsmall.com/load2neo) plugin to import the data so you'll need to get that installed.

````
Download Load2neo from http://nigelsmall.com/d/load2neo-0.6.0.zip
Unzip it
Copy geoff-0.5.0.jar and load2neo-0.6.0.jar to /path/to/neo4j/plugins
````

So your plugins directory should look something like this:

````
$ ls -alh plugins/
total 64
drwxr-xr-x   5 markneedham  staff   170B  1 Jul 22:34 .
drwxr-xr-x  14 markneedham  staff   476B  1 Jul 22:32 ..
-rwxr--r--   1 markneedham  staff   374B  1 Jul 22:32 README.txt
-rw-r--r--@  1 markneedham  staff    20K  1 Jul 22:34 geoff-0.5.0.jar
-rw-r--r--@  1 markneedham  staff   6.4K  1 Jul 22:34 load2neo-0.6.0.jar
````

Add the following line to the end of your neo4j-server.properties file:

````
org.neo4j.server.thirdparty_jaxrs_classes=com.nigelsmall.load2neo=/load2neo
````

Restart your Neo4j server.

## Importing the data

Now we need to import the different 24 seasons which are inside the [data](data) directory.

### Mac / Unix / Cygwin users

Execute the following commands:

````
for i in {1..9}
	do curl -X POST http://localhost:7474/load2neo/load/geoff -d @data/24_${i}.geoff; 

done
````

### Windows users

We'll import the data using a browser plugin which can execute a HTTP POST request against the Neo4j server. We've tried out the following ones:

* [DHC REST](https://chrome.google.com/webstore/detail/dhc-rest-http-api-client/aejoelaoggembcahagimdiliamlcdmfm/related?hl=en) - for Chrome
* [Poster](https://addons.mozilla.org/en-US/firefox/addon/poster/) - for Firefox

Here's an example of importing [data/24_1.geoff](data/24_1.geoff) using DHC REST. You'll need to do something similar for each of the files in the [data](data) directory.

<img src="http://i.imgur.com/aLeW81S.png"></img>
