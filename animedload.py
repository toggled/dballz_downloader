import animegui
import os
import pycurl
import sys
from PySide.QtCore import *
from PySide.QtGui import *
link="http://cache1.tinyvid.net/otaku/"
#link="http://localhost/"
#keyword='<a href="3237ep$-Dragon_Ball_Z.mp4">3237ep$-Dragon_Ball_Z.mp4</a>'
keyword='3237ep$-Dragon_Ball_Z.mp4'
url=""
filename='dbz_$.mp4'
start=1
end=291

def genurl(index):
    global url
    url = link+str(index).join(keyword.split('$'))
    return url

class mainWindow(QMainWindow,animegui.Ui_MainWindow):
    def __init__(self,parent=None):
        super(mainWindow,self).__init__(parent)
        self.setupUi(self)
        self.initial_housekeeping()
        #QThread.setTerminationEnabled(True)
        for column in range(4):
            for row in range(end):
                item = QTableWidgetItem()
                item.setCheckState(Qt.Unchecked)
                self.tablewidget.setItem(row,3,item)
                item=QTableWidgetItem(filename.split('$')[0]+str(row+1)+filename.split('$')[1])
                self.tablewidget.setItem(row,0,item)
                sizeinbytes=self.sizetable[row+1]
                sizeinmb=sizeinbytes/float(1024*1024)
                item=QTableWidgetItem(str(round(sizeinmb,2)))
                self.tablewidget.setItem(row,1,item)
                item=QTableWidgetItem('0%')
                self.tablewidget.setItem(row,2,item)
                item=QTableWidgetItem()
                self.tablewidget.setItem(row,4,item)

        self.threadpool={}
        self.itempool={}
        self.tablewidget.itemChanged.connect(self.handleItemChanged)
        self.stopall.clicked.connect(self.pauseall)

    def pauseall(self):
        import time
        for rownumber,val in self.threadpool.items():
            val.stop=1
        for rownumber,val in self.itempool.items():
            item=self.itempool.get(rownumber)
            #self.emit(SIGNAL('itemChanged(item)'),item)
            item.setCheckState(Qt.Unchecked)
                #item=
        self.itempool.clear()
        #time.sleep(1)

    def closeEvent(self,event):
            for vals in self.threadpool.values():
                if vals.isRunning():
                    vals.stop=1
            event.accept()

    def handleItemChanged(self,item):
            #print "self.tablewidget.row(item): >>",self.tablewidget.row(item)
            if self.tablewidget.column(item)!=3:
                #print 'returning'
                return
            if item.checkState() == Qt.Checked:#resume
                    #url=
                    if self.threadpool.get(self.tablewidget.row(item),0)==0:
                        print 'brand new'
                        self.threadpool[self.tablewidget.row(item)]=Workerthread(item,self)
                        self.threadpool[self.tablewidget.row(item)].finished.connect(self.threadDone)
                        #self.connect(self.threadpool[self.tablewidget.row(item)],SIGNAL("threadDone()"),self.threadDone,Qt.DirectConnection)
                        self.itempool[self.tablewidget.row(item)]=item
                        self.threadpool[self.tablewidget.row(item)].start()
                        print 'started'
                        print '-->','\n',self.threadpool
                    else:
                        thrd=self.threadpool[self.tablewidget.row(item)]
                        thrd.stop=0
                        print 'dirty',thrd
                        thrd.finished.connect(self.threadDone)
                        self.itempool[self.tablewidget.row(item)]=item
                        thrd.start()

            elif item.checkState()==Qt.Unchecked:
                print self.threadpool
                #print self.itempool
                #print self.tablewidget.column(item)
                threadtostop=self.threadpool.get(self.tablewidget.row(item))
                    #threadtostop.exit()
                print 'tostop',threadtostop
                threadtostop.stop=1
                self.itempool.pop(self.tablewidget.row(item))
                #print 'pause'


    def threadDone(self):
        print 'done: ',QThread.currentThread()


    def initial_housekeeping(self):
        from bs4 import BeautifulSoup as bs
        #import urllib
        #page=urllib.urlopen(link).read()
        page=open('dbz.htm','r').read()
        soup=bs(page)
        pre=soup.find('pre')
        m=start
        t=keyword.split('$')
        tofind=str(m).join(t)
        contents= pre.contents
        startlink=None
        for i in pre:
            if tofind in i:
                startlink=i
                break
        startidx=contents.index(startlink)
        self.sizetable = [0]*(end+1)
        for i in range(end):
            newcont=bs(str(contents[startidx]))
            sent=newcont.find('a').contents[0]
            epnum=sent.split('-')[0].split('ep')[-1]
            nm=contents[startidx+1].strip().split()[-1]
            #print epnum
            self.sizetable[int(epnum)]=(float(nm))
            startidx+=2



        #print self.sizetable

class Workerthread(QThread,mainWindow):
        def __init__(self,item,parent=None):
            QThread.__init__(self)
            self.item=item
            #print item
            self.stop=0
            self.mainwindw=parent
            self.dloadurl=genurl(self.mainwindw.tablewidget.row(self.item)+1)
            self.i=self.mainwindw.tablewidget.row(self.item)
            self.sizeinbytes=parent.sizetable[self.i+1]
            print self.sizeinbytes
            self.downloaded=0
            self.totallength=self.sizeinbytes

        def getprogress(self,total, existing, upload_t, upload_d):
            try:
                frac = (self.downloaded+float(existing))/float(total)
            except:
                frac=0

            #sys.stdout.write("\r%s %3i%%\n" % ("File downloaded - ", frac*100))
           #self.mainwindw.tablewidget.setItem(self.i,2,item)#i = which row
            if self.stop:
                print 'return 1'
                #import time
                #time.sleep(1)
                print 'saved',self.downloaded+float(existing)
                return 1
            item=self.mainwindw.tablewidget.item(self.i,2)
            item.setText("{0:.2f}".format(frac*100)+"%")

        def __del__(self):
            self.stop=1
            self.wait()
            print 'c closed'
            self.c.close()

        def run(self):
            #import time
            c=pycurl.Curl()
            c.setopt(pycurl.URL, self.dloadurl)
            c.setopt(pycurl.FOLLOWLOCATION, 0)
            c.setopt(pycurl.LOW_SPEED_TIME,10)
            c.setopt(pycurl.LOW_SPEED_LIMIT,1024) # if transfer speed is below 1Kbytes/sec for 10 sec
            #self.c.setopt(pycurl.NOBODY,0) #1 means header request.
            #self.c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.NOPROGRESS,0)
            c.setopt(pycurl.PROGRESSFUNCTION,self.getprogress)
            path=os.getcwd()
            savedfilename=self.dloadurl.split('/')[-1]
            self.filename=savedfilename
            filepath=os.path.join(path,savedfilename)
            if os.path.exists(filepath):
                f=open(savedfilename,"ab")
                print 'downladed  var',self.downloaded
                #c.setopt(pycurl.RESUME_FROM,os.path.getsize(savedfilename))
                r=str(self.downloaded+1)+"-"+str(self.totallength)
                print r
                c.setopt(pycurl.RANGE,r)
                item=self.mainwindw.tablewidget.item(self.i,2)
                item.setText("{0:.2f}".format(self.downloaded*100/self.totallength)+"%")

            else:
                f=open(savedfilename,"wb")
            c.setopt(pycurl.WRITEDATA,f)

            while 1:
                try:
                    print 'before perform'
                    self.mainwindw.tablewidget.item(self.i,4).setText("Downloading")
                    c.perform()
                    self.mainwindw.tablewidget.item(self.i,4).setText("Download complete")
                except pycurl.error,e :
                    print e
                    errorcode=e[0]
                    print errorcode
                    if int(errorcode) == 56 or int(errorcode)== 18: #connection reset by host or connection closed(18)
                        print 'connecting again'
                        continue
                    if int(errorcode) == 28:
                        item=self.mainwindw.tablewidget.item(self.i,4)
                        item.setText('speed too slow.')
                    c.close()
                    f.close()
                    break
            if self.stop:
                print 'inside run stop'
                self.downloaded=os.path.getsize(self.filename)
                print self.downloaded
                self.mainwindw.tablewidget.item(self.i,4).setText("Paused")
                f.close()
                return

            #print 'thread running'
            #for i in range(1000000):

                #if self.stop:
                    #print 'inside i'
                    #print 'thread stopping'
                    #self.emit(SIGNAL('threadDone()'))
                    #break
                #for j in range(1000):
                    #time.sleep(1)
                        #if self.stop:
                            #print 'inside j'
                            #print 'thread stopping'
                            #return
                            #self.emit(SIGNAL('threadDone()'))
                        #break
            #print self.mainwindw.tablewidget.row(self.item),'--',self.stop
                        #print 'ending'
app=QApplication(sys.argv)
form=mainWindow()
form.show()
sys.exit(app.exec_())
