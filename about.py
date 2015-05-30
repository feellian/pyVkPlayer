import PyQt4

from aboutDialog import Ui_AboutDialog

class aboutDialog(PyQt4.QtGui.QDialog, Ui_AboutDialog):
	def __init__(self):
		super(aboutDialog, self).__init__()
		self.setupUi(self)
		self.connect(self.okPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.closeLoginDialog)

	def closeLoginDialog(self):
		self.close()

