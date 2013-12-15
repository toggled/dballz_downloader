import animegui
import pycurl
import sys
from PySide.QtCore import *
from PySide.QtGui import *
link="http://cache1.tinyvid.net/otaku/"
#keyword='<a href="3237ep$-Dragon_Ball_Z.mp4">3237ep$-Dragon_Ball_Z.mp4</a>'
keyword='3237ep$-Dragon_Ball_Z.mp4'

filename='dbz_$.mp4'
start=1
end=291


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
                item=QTableWidgetItem(str(round(self.sizetable[row+1],2)))
                self.tablewidget.setItem(row,1,item)
                item=QTableWidgetItem('0%')
                self.tablewidget.setItem(row,2,item)

        self.threadpool={}
        self.itempool={}
        self.tablewidget.itemChanged.connect(self.handleItemChanged)
        self.stopall.clicked.connect(self.pauseall)
        self.c= pycurl.Curl()
        #self.c.setopt(pycurl.URL, url)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)

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
            print "self.tablewidget.row(item): >>",self.tablewidget.row(item)
            if item.checkState() == Qt.Checked:#resume
                    self.threadpool[self.tablewidget.row(item)]=Workerthread(item,self)
                    self.threadpool[self.tablewidget.row(item)].finished.connect(self.threadDone)
                    #self.connect(self.threadpool[self.tablewidget.row(item)],SIGNAL("threadDone()"),self.threadDone,Qt.DirectConnection)
                    self.itempool[self.tablewidget.row(item)]=item
                    self.threadpool[self.tablewidget.row(item)].start()
                    print 'started'
                    print '-->','\n',self.threadpool

            elif item.checkState()==Qt.Unchecked:
                print self.threadpool
                threadtostop=self.threadpool.get(self.tablewidget.row(item))
                    #threadtostop.exit()
                threadtostop.stop=1
                self.itempool.pop(self.tablewidget.row(item))
                print 'pause'


    def threadDone(self):
        print 'done: ',QThread.currentThread()


    def progress(self,total, existing, upload_t, upload_d):
        existing = existing + os.path.getsize(filename)
        try:
            frac = float(existing)/float(total)
        except:
            frac=0
        sys.stdout.write("\r%s %3i%%" % ("File downloaded - ", frac*100))
        #item=QtableWidgetItem(str(frac*100))
        #self.tablewidget.setItem(i,2,item)#i = which row

    def initial_housekeeping(self):
        from bs4 import BeautifulSoup as bs
        #page=urllib.urlopen(link).read()
        page=open('dbz.htm','r').read()
        soup=bs(page)
        pre=soup.find('pre')
        m=start
        t=keyword.split('$')
        tofind=str(m).join(t)
        #print tofind
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
            self.sizetable[int(epnum)]=(float(nm)/float(1024*1024))
            startidx+=2

        #print self.sizetable

class Workerthread(QThread,mainWindow):
        def __init__(self,item,parent=None):
            QThread.__init__(self)
            self.item=item
            print item
            self.stop=0
            self.mainwindw=parent

        def __del__(self):
            self.stop=1
            self.wait()

        def run(self):
            import time
            print 'thread running'
            for i in range(1000000):

                #if self.stop:
                    #print 'inside i'
                    #print 'thread stopping'
                    #self.emit(SIGNAL('threadDone()'))
                    #break
                #for j in range(1000):
                    time.sleep(1)
                    if self.stop:
                        print 'inside j'
                        print 'thread stopping'
                        return
                        #self.emit(SIGNAL('threadDone()'))
                        #break
                    #print self.mainwindw.tablewidget.row(self.item),'--',self.stop
            print 'ending'


app=QApplication(sys.argv)
form=mainWindow()
form.show()
sys.exit(app.exec_())