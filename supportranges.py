import pycurl
import cStringIO
import re,sys

def test(debug_type, debug_msg):
    print "debug(%d): %s" % (debug_type, debug_msg)

def accepts_byte_ranges(effective_url):
    """Test if the server supports multi-part file download. Method expects effective (absolute) url."""

    c = pycurl.Curl()
    header = cStringIO.StringIO()
    c.setopt(pycurl.DEBUGFUNCTION, test)
    # Get http header
    c.setopt(c.VERBOSE,True)
    c.setopt(c.URL, effective_url)
    c.setopt(c.NOBODY, 1)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.perform()
    c.close()

    header_text = header.getvalue()
    header.close()

    print header_text

    #Check if server accepts byte-ranges
    match = re.search('Accept-Ranges:\s+bytes', header_text)
    if match:
        return True
    else:
        #If server explicitly specifies "Accept-Ranges: none" in the header, we do not attempt partial download.
        match = re.search('Accept-Ranges:\s+none', header_text)
        if match:
            return False
        else:
            c = pycurl.Curl()
            #print 'hope'
            # There is still hope, try a simple byte range query
            c.setopt(c.RANGE, '0-0') # First byte
            c.setopt(c.URL, effective_url)
            c.setopt(c.NOBODY, 1)
            c.perform()

            http_code = c.getinfo(c.HTTP_CODE)
            c.close()

            if http_code == 206: # Http status code 206 means byte-ranges are accepted
                return True
            else:
                return False

def getprogress(total, existing, upload_t, upload_d):
            try:
                frac = float(existing)
            except:
                frac=0
            print existing
            #sys.stdout.write("\r%s %3i%%\n" % ("File downloaded - ", frac*100))
def getsmptetime(hr,minu,sec):
    zhr=hr
    zminu=minu
    zsec=sec
    if hr<10:
        zhr=str(0)+str(zhr)
    if minu<10:
        zminu=str(0)+str(zminu)
    if sec<10:
        zsec=str(0)+str(zsec)

    return str(zhr)+":"+str(zminu)+":"+str(zsec)

if __name__=="__main__":
            effective_url="http://cache1.tinyvid.net/otaku/3237ep1-Dragon_Ball_Z.mp4"

            print accepts_byte_ranges(effective_url)
            sys.exit(1)
            c = pycurl.Curl()
            #print 'hope'
            #There is still hope, try a simple byte range query
            hr=0
            minu=0
            sec=0

            start=getsmptetime(hr,minu,sec)
            minu+=1
            end=getsmptetime(hr,minu,sec)

            r=start+"-"+end
            print r
            #import sys
            #sys.exit(1)
            c.setopt(pycurl.RANGE,r) # First byte
            c.setopt(c.URL, effective_url)
            #c.setopt(c.NOBODY, 0)
            fp=open('ep1_part1.mp4','wb')
            c.setopt(c.WRITEDATA,fp)
            c.setopt(c.PROGRESSFUNCTION,getprogress)
            c.setopt(c.VERBOSE,True)
            print 'before perform'
            c.perform()
            fp.close()
            print 'after first perform'
            #print 'hope'
            #There is still hope, try a simple byte range query
            start=end
            minu+=1
            end=getsmptetime(hr,minu,sec)
            r=str(start)+"-"+str(end-1)
            print r

            c.setopt(c.RANGE, r) # First byte
            c.setopt(c.URL, effective_url)
            c.setopt(c.NOBODY, 0)
            fp=open('ep1_part2.mp4','wb')
            c.setopt(pycurl.WRITEDATA,fp)

            c.perform()


            #http_code = c.getinfo(c.HTTP_CODE)
            c.close()
