# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'songTextDialog.ui'
#
# Created: Wed May 15 01:17:41 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SongTextDialog(object):
    def setupUi(self, SongTextDialog):
        SongTextDialog.setObjectName(_fromUtf8("SongTextDialog"))
        SongTextDialog.resize(308, 563)
        self.songTextEdit = QtGui.QPlainTextEdit(SongTextDialog)
        self.songTextEdit.setGeometry(QtCore.QRect(0, 0, 311, 521))
        self.songTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.songTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.songTextEdit.setObjectName(_fromUtf8("songTextEdit"))
        self.okPushButton = QtGui.QPushButton(SongTextDialog)
        self.okPushButton.setGeometry(QtCore.QRect(100, 530, 97, 27))
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))

        self.retranslateUi(SongTextDialog)
        QtCore.QMetaObject.connectSlotsByName(SongTextDialog)

    def retranslateUi(self, SongTextDialog):
        SongTextDialog.setWindowTitle(_translate("SongTextDialog", "Dialog", None))
        self.okPushButton.setText(_translate("SongTextDialog", "Ok", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SongTextDialog = QtGui.QDialog()
    ui = Ui_SongTextDialog()
    ui.setupUi(SongTextDialog)
    SongTextDialog.show()
    sys.exit(app.exec_())

