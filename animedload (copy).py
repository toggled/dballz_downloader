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
        for column in range(4):
            for row in range(end):
                item = QTableWidgetItem()
                item.setCheckState(Qt.Unchecked)
                self.tablewidget.setItem(row,3,item)
                item=QTableWidgetItem(filename.split('$')[0]+str(row+1)+filename.split('$')[1])
                self.tablewidget.setItem(row,0,item)
                item=QTableWidgetItem(str(round(self.sizetable[row],2)))
                self.tablewidget.setItem(row,1,item)
                item=QTableWidgetItem('0%')
                self.tablewidget.setItem(row,2,item)

        self.c= pycurl.Curl()
        self.c.setopt(pycurl.URL, url)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)

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
        import urllib
        from bs4 import BeautifulSoup as bs
        #page=urllib.urlopen(link).read()
        page=open('dbz.htm','r').read()
        soup=bs(page)
        pre=soup.find('pre')
        m=start
        t=keyword.split('$')
        tofind=str(m).join(t)
        print tofind
        contents= pre.contents
        startlink=None
        for i in pre:
            if tofind in i:
                startlink=i
                break
        startidx=contents.index(startlink)
        self.sizetable = []
        for i in range(end):
            nm=contents[startidx+1].strip().split()[-1]
            self.sizetable.append(float(nm)/float(1024*1024))
            startidx+=2
        print self.sizetable

app=QApplication(sys.argv)
form=mainWindow()
form.show()
app.exec_()
