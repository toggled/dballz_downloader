import sys,time
from PySide import QtGui

class MyApp(QtGui.QWidget):
    def init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setGeometry(300,300,280,600)
        self.setWindowTitle('threads')
        self.layout=QtGui.QVBoxLayout(self)
        self.testButton=QtGui.QPushButton("test")
        self.testButton.released.connect(self.test)

        self.listwidget=QtGui.QListWidget(self)
        self.layout.addWidget(self.testButton)
        self.layout.addWidget(self.listwidget)

    def add(self,text):
        """Add item to list widget"""
        print "Add: "+text
        self.listwidget.addItem(text)
        self.listwidget.sortItems()

    def addBatch(self,text="test",iters=6,delay=.3):
        """Add several items to list widget"""
        for i in range(iters):
            time.sleep(delay) # artificial time delay
            self.add(text+" "+str(i))

    def test(self):
        self.listwidget.clear()
        self.addBatch("_non_thread",iters=6,delay=0.3)

app=QtGui.QApplication(sys.argv)
test= MyApp()
test.show()
app.exec_()
