import PyQt4
import sys
import gui

if __name__ == "__main__":
    app = PyQt4.QtGui.QApplication(sys.argv)
    mw = gui.mainWindow()
    mw.show()
    app.exec_()

