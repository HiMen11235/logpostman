# About
logpostman is a command line style program for sending syslog data. It can read information from a saved file and send it continuously, or change the source IP address to an arbitrary IP address and send it.
# Requirements
```
Python3.x
scapy=2.4.5
```
# Installation
Clone the Github repository in any directory.
# Usage
With sudo or root privileges, run
```
python3 logpostman.py host -f /file/to/path
```
to continuously send the data in the file to host. (default: 1000events/s)
To send the source IP address as an arbitrary IP address, use
```
python3 logpostman.py host -a yy.yy.yy.yy -f /file/to/
path
```
If you want to send the file as an arbitrary IP address, use python3 logpostman.py
The basic usage is as above, but for other options, please check the help information displayed by -h,--help.
# License
GPLv2