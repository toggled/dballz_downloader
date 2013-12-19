import pycurl
import os
import sys
url="http://cache1.tinyvid.net/otaku/3237ep2-Dragon_Ball_Z.mp4"
def test(debug_type, debug_msg):
     if debug_type!=3:
        print "debug(%d): %s" % (debug_type, debug_msg)

c=pycurl.Curl()
c.setopt(c.VERBOSE,True)
c.setopt(pycurl.DEBUGFUNCTION, test)
c.setopt(pycurl.URL,url)
c.setopt(pycurl.FOLLOWLOCATION,0)
c.setopt(pycurl.NOPROGRESS,0)
c.setopt(pycurl.RANGE,"0-2097151") #2MB
filename = url.split("/")[-1].strip()
filepath = os.path.join(os.getcwd(), "dbz2.part1.mp4")
if os.path.exists(filepath):
	f = open(filepath, "ab")
	downloaded = os.path.getsize(filepath)
	c.setopt(pycurl.RESUME_FROM, downloaded)
else:
	f = open(filepath, "wb")
c.setopt(pycurl.WRITEDATA, f)
try:
	c.perform()
except pycurl.error,e:
	print e

c.setopt(pycurl.RANGE,"2097152-4194303") #next 2MB
filepath = os.path.join(os.getcwd(), "dbz2.part2.mp4")
f = open(filepath, "wb")
c.setopt(pycurl.WRITEDATA, f)
try:
	c.perform()
except pycurl.error,e:
	print e
c.close()
