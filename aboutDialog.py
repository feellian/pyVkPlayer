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

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(320, 240)
        self.label = QtGui.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(50, 60, 241, 121))
        self.label.setObjectName(_fromUtf8("label"))
        self.okPushButton = QtGui.QPushButton(AboutDialog)
        self.okPushButton.setGeometry(QtCore.QRect(110, 200, 97, 27))
        self.okPushButton.setObjectName(_fromUtf8("okPushButton"))

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Dialog", None))
        self.label.setText(_translate("AboutDialog", "Copyright(C) 2015 Vladislav Polskikh. IP-12", None))
        self.okPushButton.setText(_translate("AboutDialog", "Ok", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AboutDialog = QtGui.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec_())

