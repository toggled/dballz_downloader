import pycurl
import cStringIO
from fake_useragent import UserAgent
url="http://cache1.tinyvid.net/otaku/3237ep5-Dragon_Ball_Z.mp4"
def test(debug_type, debug_msg):
     if debug_type!=3:
        print "debug(%d): %s" % (debug_type, debug_msg)

c=pycurl.Curl()
c.setopt(pycurl.URL,url)
c.setopt(c.VERBOSE,True)
c.setopt(pycurl.DEBUGFUNCTION, test)
c.setopt(pycurl.FOLLOWLOCATION,0)
c.setopt(pycurl.NOPROGRESS,0)
c.setopt(c.NOBODY, 1)
header = cStringIO.StringIO()
c.setopt(c.HEADERFUNCTION, header.write)
c.setopt(pycurl.RANGE,"0-10") #2MB
#useragent="Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0"
ua=UserAgent()

useragent=str(ua.opera)
c.setopt(pycurl.USERAGENT,useragent)
try:
	c.perform()
except pycurl.error,e:
	print e
