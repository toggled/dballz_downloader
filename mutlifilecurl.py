import pycurl
from StringIO import StringIO

def LoadMulti(urls):
    m = pycurl.CurlMulti()
    handles = {}
    for url in urls:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        data = StringIO()
        header = StringIO()
        c.setopt(pycurl.WRITEFUNCTION, data.write)
        c.setopt(pycurl.HEADERFUNCTION, header.write)                
        handles[url] = dict(data=data, header=header, handle=c)
        m.add_handle(c)
    while 1:
        ret, num_handles = m.perform()
        print num_handles
        if ret != pycurl.E_CALL_MULTI_PERFORM: break
    while num_handles:
        ret = m.select(1.0)
        if ret == -1:  continue
        while 1:
            ret, num_handles = m.perform()
            print num_handles,"H"
            print ret,"dd",pycurl.E_CALL_MULTI_PERFORM
            if ret != pycurl.E_CALL_MULTI_PERFORM: 
               break
    return handles


res = LoadMulti(['http://cache1.tinyvid.net/otaku/3237ep1-Dragon_Ball_Z.mp4', 'http://cache1.tinyvid.net/otaku/3237ep2-Dragon_Ball_Z.mp4', 'http://pycurl.sourceforge.net/doc/curlmultiobject.html'])
for url, d in res.iteritems():
    print url, d['handle'].getinfo(pycurl.HTTP_CODE), len(d['data'].getvalue()), len(d['header'].getvalue())
