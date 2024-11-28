# HackTheBox Alert machine file read automation script

Simple python script that sends the XSS payload as POST requests to the appopriate endpoints.
It creates an http server in the background, that returns the data sent to us by the Admin,
url decodes it and prints for us to see. with the -W or --write options we can save the file
for later analysis

##Usage:
~~~Bash
python read.py <URL> <FILE_PATH>
~~~~
