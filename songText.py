from urllib import unquote
import PyQt4
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox

from songTextDialog import Ui_SongTextDialog

class songTextDialog(QtGui.QDialog, Ui_SongTextDialog):
    def __init__(self, parent=None):
        super(songTextDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.connect(self.okPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.closeDialog)
        self.songTextEdit.setReadOnly(True)
    def setText(self, text):
        self.songTextEdit.appendPlainText(text["text"].replace('amp;', ''))

    def closeDialog(self):
        self.close()
