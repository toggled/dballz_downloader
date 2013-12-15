import sys
from PyQt4 import QtCore, QtGui


class MyForm(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    
    # Create a start, stop and a line edit to display the times
    self.startButton = QtGui.QPushButton(self.tr("&Start"),self)
    self.stopButton= QtGui.QPushButton(self.tr("&Close"),self)
    self.killButton= QtGui.QPushButton(self.tr("&Kill"),self)
    self.stopButton.setEnabled(False)
    self.label = QtGui.QLabel(self)
    
    # Arrange them in a good layout
    mainLayout = QtGui.QVBoxLayout()
    mainLayout.addWidget(self.startButton)
    mainLayout.addWidget(self.stopButton)
    mainLayout.addWidget(self.killButton)
    mainLayout.addWidget(self.label)
    self.setLayout(mainLayout)
    
    # start the worker thread
    self.thread = Worker(None)
    
    # Now create some connection
    self.connect(self.startButton, QtCore.SIGNAL("clicked()"), self.startCounter)
    self.connect(self.stopButton, QtCore.SIGNAL("clicked()"), self.stopCounter)
    self.connect(self.killButton, QtCore.SIGNAL("clicked()"), self.killThread)
    
    #self.connect(self.thread, QtCore.SIGNAL("finished()"), self.updateUi)
    #self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.updateUi)
    
  def startCounter(self):
    self.startButton.setEnabled(False)
    self.stopButton.setEnabled(True)
    self.thread.render()
    
    
  def stopCounter(self):
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    self.thread.exiting = True
    
  def killThread(self):
    print 'call kill'
    self.thread.terminate()
    self.thread.wait()
    print 'killed'
    
  def updateUi(self):
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
  

class Worker(QtCore.QThread):
  def __init__(self, parent = None):
    super(Worker, self).__init__(parent)
    self.exiting = False
    
  def __del__(self):
    self.exiting = True
    self.wait()

  def render(self):
    self.exiting = False
    self.start()
  
  def run(self):
    while not self.exiting:
      print 'harrrrr'
      k = pow(102144354421,21443444551)
      print 'ramen'
      self.sleep(1)

      
      
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
