import pycurl
import cStringIO
import re

def accepts_byte_ranges(effective_url):
    """Test if the server supports multi-part file download. Method expects effective (absolute) url."""

    c = pycurl.Curl()
    header = cStringIO.StringIO()

    # Get http header
    c.setopt(c.URL, effective_url)
    c.setopt(c.NOBODY, 1)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.perform()
    c.close()

    header_text = header.getvalue()
    header.close()

    #print header_text

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

if __name__=="__main__":
            effective_url="http://cache1.tinyvid.net/otaku/3237ep1-Dragon_Ball_Z.mp4"
            c = pycurl.Curl()
            #print 'hope'
            #There is still hope, try a simple byte range query
            c.setopt(c.RANGE, '1024-2048') # First byte
            c.setopt(c.URL, effective_url)
            c.setopt(c.NOBODY, 0)
            #c.perform()

            #http_code = c.getinfo(c.HTTP_CODE)
            c.close()
            print accepts_byte_ranges(effective_url)
